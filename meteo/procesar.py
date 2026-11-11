# -*- coding: utf-8 -*-
"""Previsión de montaña de Guías Ad Astra a partir de los modelos ECMWF IFS, NOAA GFS y DWD ICON-EU.

Se ejecuta en GitHub Actions cada 6 horas (ver .github/workflows/meteo.yml):
    python3 meteo/procesar.py --out meteo-out
Escribe meteo-out/<macizo>.json (series cada 3 h de cada modelo y resumen diario) y meteo-out/resumen.json.

Datos abiertos:
- ECMWF IFS 0,25°  (open data, CC BY 4.0)          https://www.ecmwf.int/en/forecasts/datasets/open-data
- NOAA GFS 0,25°   (dominio público)                https://registry.opendata.aws/noaa-gfs-bdp-pds/
- DWD ICON-EU 6,5 km (CC BY 4.0)                    https://opendata.dwd.de/weather/nwp/icon-eu/

Para cada macizo se calculan dos puntos:
- base: temperatura a 2 m corregida a la altitud del pueblo (-0,65 °C / 100 m), viento a 10 m y rachas;
- cumbre: temperatura y viento interpolados en la vertical entre el suelo del modelo y los niveles de
  925, 850, 700, 600 y 500 hPa, a la altitud real de la cumbre.
También: precipitación cada 3 h, nubosidad, isocero, cota de nieve y CAPE (energía para tormentas).
"""
import argparse, bz2, concurrent.futures as cf, datetime as dt, json, math, os, sys, tempfile, time, traceback
from zoneinfo import ZoneInfo

import numpy as np
import requests
import eccodes

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from macizos import MACIZOS, REGIONES  # noqa: E402

G = 9.80665
UTC = dt.timezone.utc
TZ = ZoneInfo("Europe/Madrid")
HORAS = 168           # 7 días
PASO = 3              # horas
LEVELS = [925, 850, 700, 600, 500]
UA = {"User-Agent": "guiasadastra-meteo/1.0 (+https://www.guiasadastra.com/meteo/)"}

S = requests.Session()
S.headers.update(UA)
S.mount("https://", requests.adapters.HTTPAdapter(pool_connections=32, pool_maxsize=32,
        max_retries=requests.adapters.Retry(total=4, backoff_factor=1.5, status_forcelist=[429, 500, 502, 503, 504])))

PTS = []
for _m in MACIZOS:
    PTS.append((_m["base"]["lat"], _m["base"]["lon"]))
    PTS.append((_m["cumbre"]["lat"], _m["cumbre"]["lon"]))
NP = len(PTS)


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


# ------------------------------------------------------------------ GRIB -> valores en los puntos
_WCACHE = {}


def _weights(Ni, Nj, lat0, lon0, di, dj, jpos):
    key = (Ni, Nj, round(lat0, 5), round(lon0, 5), round(di, 6), round(dj, 6), jpos)
    if key in _WCACHE:
        return _WCACHE[key]
    glob = abs(Ni * di - 360) < 1e-6
    out = []
    for lat, lon in PTS:
        fy = (lat - lat0) / (dj if jpos else -dj)
        fx = ((lon - lon0) % 360) / di
        j0, i0 = int(math.floor(fy)), int(math.floor(fx))
        wy, wx = fy - j0, fx - i0
        j1, i1 = j0 + 1, i0 + 1
        if glob:
            i1 %= Ni
        if not (0 <= j0 < Nj and 0 <= j1 < Nj and 0 <= i0 < Ni and 0 <= i1 < Ni):
            out.append(None)
            continue
        out.append(((j0 * Ni + i0, (1 - wy) * (1 - wx)), (j0 * Ni + i1, (1 - wy) * wx),
                    (j1 * Ni + i0, wy * (1 - wx)), (j1 * Ni + i1, wy * wx)))
    _WCACHE[key] = out
    return out


def decode(msg_bytes):
    """Un mensaje GRIB (bytes) -> (meta, valores en PTS)."""
    gid = eccodes.codes_new_from_message(msg_bytes)
    try:
        g = lambda k, d=None: (eccodes.codes_get(gid, k) if eccodes.codes_is_defined(gid, k) else d)
        meta = {k: g(k) for k in ("shortName", "typeOfLevel", "level", "startStep", "endStep", "stepType", "gridType",
                                  "dataDate", "dataTime", "units")}
        if meta["gridType"] != "regular_ll":
            raise ValueError("rejilla no soportada: %s" % meta["gridType"])
        Ni, Nj = g("Ni"), g("Nj")
        lat0, lon0 = g("latitudeOfFirstGridPointInDegrees"), g("longitudeOfFirstGridPointInDegrees")
        di, dj = g("iDirectionIncrementInDegrees"), g("jDirectionIncrementInDegrees")
        jpos = bool(g("jScansPositively", 0))
        vals = eccodes.codes_get_values(gid)
        miss = g("missingValue", 9999)
        if g("bitmapPresent", 0):
            vals = np.where(vals == miss, np.nan, vals)
    finally:
        eccodes.codes_release(gid)
    w = _weights(Ni, Nj, lat0, lon0, di, dj, jpos)
    res = np.full(NP, np.nan)
    for k, ww in enumerate(w):
        if ww:
            res[k] = sum(vals[i] * f for i, f in ww)
    return meta, res


def split_messages(blob):
    """Separa un fichero GRIB2 con varios mensajes en una lista de bytes."""
    out, i = [], 0
    while True:
        j = blob.find(b"GRIB", i)
        if j < 0:
            break
        ln = int.from_bytes(blob[j + 8:j + 16], "big") if blob[j + 7] == 2 else int.from_bytes(blob[j + 4:j + 7], "big")
        out.append(blob[j:j + ln])
        i = j + ln
    return out


class Modelo:
    """Campos de un modelo en los puntos: campos[var][valid_time] = np.array(NP)."""
    def __init__(self, nombre, etiqueta, resol):
        self.nombre, self.etiqueta, self.resol = nombre, etiqueta, resol
        self.run = None
        self.campos = {}
        self.acc = {}          # precipitación acumulada desde el inicio: acc[valid_time] = np.array(NP)

    def put(self, var, t, v):
        self.campos.setdefault(var, {})[t] = v


# ------------------------------------------------------------------ ECMWF IFS (open data)
def ecmwf():
    from ecmwf.opendata import Client
    m = Modelo("ecmwf", "ECMWF IFS", "0,25° (~25 km)")
    steps = list(range(0, 145, 3)) + list(range(150, HORAS + 1, 6))
    src = None
    for s in ("azure", "google", "ecmwf", "aws"):
        try:
            c = Client(source=s, model="ifs", resol="0p25")
            run = c.latest(type="fc", step=HORAS, param="2t")
            src = s
            break
        except Exception as ex:
            log("ECMWF: fuente %s no disponible (%s)" % (s, ex))
    if not src:
        raise RuntimeError("ECMWF no disponible")
    m.run = run.replace(tzinfo=UTC)
    log("ECMWF: pasada %s (fuente %s)" % (m.run.strftime("%Y-%m-%d %HZ"), src))
    tmp = tempfile.mkdtemp()

    def bajar(nombre, req):
        cl = c  # un solo cliente: Azure limita los permisos de acceso (SAS) si se piden muchos
        path = os.path.join(tmp, nombre + ".grib2")
        for st in (steps, steps[1:]):  # algunas variables (rachas, precipitación) no tienen paso 0
            try:
                cl.retrieve(date=m.run.strftime("%Y%m%d"), time=m.run.hour, type="fc", step=st, target=path, **req)
                return path
            except Exception as ex:
                err = str(ex)[:160]
        log("ECMWF: %s no disponible (%s)" % (nombre, err))
        return None

    pedidos = {p: {"param": p, "levtype": "sfc"} for p in ("2t", "10u", "10v", "tp", "10fg", "tcc", "mucape")}
    for p, levs in (("t", [925, 850, 700, 500]), ("gh", [925, 850, 700, 500]), ("u", [850, 700, 500]), ("v", [850, 700, 500])):
        pedidos["pl_" + p] = {"param": p, "levtype": "pl", "levelist": levs}
    rutas = {k: bajar(k, v) for k, v in pedidos.items()}
    inv = {}
    for nombre, path in rutas.items():
        if not path:
            continue
        for msg in split_messages(open(path, "rb").read()):
            meta, v = decode(msg)
            sn, tl, lev, st = meta["shortName"], meta["typeOfLevel"], meta["level"], int(meta["endStep"])
            t = m.run + dt.timedelta(hours=st)
            inv[(sn, tl)] = inv.get((sn, tl), 0) + 1
            if tl == "isobaricInhPa":
                m.put((sn, int(lev)), t, v)
            elif sn == "tp":
                m.acc[t] = v * 1000.0
            elif sn == "2t":
                m.put("t2", t, v - 273.15)
            elif sn == "10u":
                m.put("u10", t, v)
            elif sn == "10v":
                m.put("v10", t, v)
            elif sn == "10fg":
                m.put("gust", t, v)
            elif sn == "tcc":
                m.put("tcc", t, v * 100.0 if np.nanmax(v) <= 1.01 else v)
            elif sn == "mucape":
                m.put("cape", t, v)
    log("ECMWF: inventario", sorted(inv.items()))
    m.acc.setdefault(m.run, np.zeros(NP))
    for (sn, lev) in [k for k in m.campos if isinstance(k, tuple)]:
        if sn == "gh":
            pass  # ya en metros geopotenciales
        elif sn == "t":
            m.campos[(sn, lev)] = {t: v - 273.15 for t, v in m.campos[(sn, lev)].items()}
    return m


# ------------------------------------------------------------------ NOAA GFS (AWS)
GFS_BUCKET = "https://noaa-gfs-bdp-pds.s3.amazonaws.com"
GFS_WANT = {("TMP", "2 m above ground"), ("UGRD", "10 m above ground"), ("VGRD", "10 m above ground"),
            ("GUST", "surface"), ("APCP", "surface"), ("TCDC", "entire atmosphere"), ("CAPE", "surface"),
            ("HGT", "0C isotherm"), ("HGT", "surface")}
for _l in LEVELS:
    for _v in ("TMP", "HGT", "UGRD", "VGRD"):
        GFS_WANT.add((_v, "%d mb" % _l))


NOMADS = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
NOMADS_Q = ("&var_TMP=on&var_HGT=on&var_UGRD=on&var_VGRD=on&var_GUST=on&var_APCP=on&var_TCDC=on&var_CAPE=on"
            "&lev_2_m_above_ground=on&lev_10_m_above_ground=on&lev_surface=on&lev_entire_atmosphere=on&lev_0C_isotherm=on"
            + "".join("&lev_%d_mb=on" % l for l in LEVELS) + "&subregion=&leftlon=-10&rightlon=4&toplat=45&bottomlat=35")


def gfs_nomads(m, steps):
    """Descarga recortada a España desde NOMADS; identifica cada campo por sus metadatos GRIB."""
    def paso(st):
        url = "%s?dir=%%2Fgfs.%s%%2F%02d%%2Fatmos&file=gfs.t%02dz.pgrb2.0p25.f%03d%s" % (NOMADS, m.run.strftime("%Y%m%d"), m.run.hour, m.run.hour, st, NOMADS_Q)
        for intento in range(4):
            rr = S.get(url, timeout=90)
            if rr.status_code == 200 and rr.content[:4] == b"GRIB":
                break
            time.sleep(5 + 10 * intento)
        else:
            raise RuntimeError("NOMADS f%03d: %s" % (st, rr.status_code))
        res = []
        for msg in split_messages(rr.content):
            meta, v = decode(msg)
            sn, tl, lev = meta["shortName"], meta["typeOfLevel"], meta["level"]
            if tl == "isobaricInhPa":
                var = {"t": "TMP", "gh": "HGT", "u": "UGRD", "v": "VGRD"}.get(sn)
                if var:
                    res.append((var, "%d mb" % lev, meta, v))
            elif sn in ("2t", "t") and tl == "heightAboveGround":
                res.append(("TMP", "2 m above ground", meta, v))
            elif sn in ("10u", "u") and tl == "heightAboveGround":
                res.append(("UGRD", "10 m above ground", meta, v))
            elif sn in ("10v", "v") and tl == "heightAboveGround":
                res.append(("VGRD", "10 m above ground", meta, v))
            elif tl == "isothermZero" or (sn == "gh" and tl not in ("surface",)) and "isotherm" in tl.lower():
                res.append(("HGT", "0C isotherm", meta, v))
            elif sn in ("orog", "gh", "h") and tl == "surface":
                res.append(("HGT", "surface", meta, v))
            elif sn in ("gust", "i10fg", "10fg"):
                res.append(("GUST", "surface", meta, v))
            elif sn in ("tp", "prate") and sn == "tp":
                res.append(("APCP", "surface", meta, v))
            elif sn == "tcc":
                res.append(("TCDC", "entire atmosphere", meta, v))
            elif sn == "cape" and tl == "surface":
                res.append(("CAPE", "surface", meta, v))
        return st, res
    with cf.ThreadPoolExecutor(4) as ex:
        return list(ex.map(paso, steps))


def gfs():
    m = Modelo("gfs", "NOAA GFS", "0,25° (~25 km)")
    now = dt.datetime.now(UTC)
    base = now.replace(minute=0, second=0, microsecond=0, hour=now.hour - now.hour % 6)
    for k in range(6):
        run = base - dt.timedelta(hours=6 * k)
        u = "%s/gfs.%s/%02d/atmos/gfs.t%02dz.pgrb2.0p25.f%03d.idx" % (GFS_BUCKET, run.strftime("%Y%m%d"), run.hour, run.hour, HORAS)
        if S.head(u, timeout=20).status_code == 200:
            m.run = run
            break
    if not m.run:
        raise RuntimeError("GFS no disponible")
    log("GFS: pasada %s" % m.run.strftime("%Y-%m-%d %HZ"))
    steps = list(range(0, HORAS + 1, PASO))

    def paso(st):
        url = "%s/gfs.%s/%02d/atmos/gfs.t%02dz.pgrb2.0p25.f%03d" % (GFS_BUCKET, m.run.strftime("%Y%m%d"), m.run.hour, m.run.hour, st)
        lines = [l.split(":") for l in S.get(url + ".idx", timeout=60).text.strip().splitlines()]
        sel = []
        for n, l in enumerate(lines):
            if (l[3], l[4]) in GFS_WANT and n + 1 < len(lines):
                sel.append((int(l[1]), int(lines[n + 1][1]) - 1, l[3], l[4], l[5]))
        res = []
        # descarga en bloques contiguos
        i = 0
        while i < len(sel):
            j = i
            while j + 1 < len(sel) and sel[j + 1][0] == sel[j][1] + 1:
                j += 1
            a, b = sel[i][0], sel[j][1]
            blob = S.get(url, headers={"Range": "bytes=%d-%d" % (a, b)}, timeout=120).content
            for s0, s1, var, lev, fc in sel[i:j + 1]:
                piece = blob[s0 - a:s1 - a + 1]
                meta, v = decode(piece)
                res.append((var, lev, meta, v))
            i = j + 1
        return st, res

    try:
        resultados = gfs_nomads(m, steps)
        log("GFS: datos de NOMADS (recorte de España)")
    except Exception as ex_:
        log("GFS: NOMADS falló (%s); uso la copia de AWS" % ex_)
        with cf.ThreadPoolExecutor(4) as ex:
            resultados = list(ex.map(paso, steps))
    buckets = []
    for st, res in resultados:
        t = m.run + dt.timedelta(hours=st)
        for var, lev, meta, v in res:
            if var == "APCP":
                buckets.append((int(meta["startStep"]), int(meta["endStep"]), v))
            elif var == "TMP" and lev.endswith("mb"):
                m.put(("t", int(lev.split()[0])), t, v - 273.15)
            elif var == "HGT" and lev.endswith("mb"):
                m.put(("gh", int(lev.split()[0])), t, v)
            elif var == "UGRD" and lev.endswith("mb"):
                m.put(("u", int(lev.split()[0])), t, v)
            elif var == "VGRD" and lev.endswith("mb"):
                m.put(("v", int(lev.split()[0])), t, v)
            elif var == "TMP":
                m.put("t2", t, v - 273.15)
            elif var == "UGRD":
                m.put("u10", t, v)
            elif var == "VGRD":
                m.put("v10", t, v)
            elif var == "GUST":
                m.put("gust", t, v)
            elif var == "TCDC":
                m.put("tcc", t, v)
            elif var == "CAPE":
                m.put("cape", t, v)
            elif var == "HGT" and lev == "0C isotherm":
                m.put("iso0", t, v)
            elif var == "HGT" and lev == "surface":
                m.put("orog", t, v)
    # precipitación: GFS da cubos que se reinician cada 6 h -> acumulado desde el inicio
    tot = {0: np.zeros(NP)}
    for s0, s1, v in sorted(buckets, key=lambda x: (x[1], x[0])):
        if s0 in tot and s1 not in tot:
            tot[s1] = tot[s0] + v
    for st, v in tot.items():
        m.acc[m.run + dt.timedelta(hours=st)] = v
    log("GFS: %d pasos, %d cubos de precipitación" % (len(resultados), len(buckets)))
    return m


# ------------------------------------------------------------------ DWD ICON-EU
DWD = "https://opendata.dwd.de/weather/nwp/icon-eu/grib"
ICON_SINGLE = ["t_2m", "u_10m", "v_10m", "vmax_10m", "tot_prec", "clct", "hzerocl", "snowlmt", "cape_ml"]
ICON_PL = {"t": [925, 850, 700, 500], "fi": [925, 850, 700, 500], "u": [850, 700, 500], "v": [850, 700, 500]}


def icon():
    m = Modelo("icon", "DWD ICON-EU", "0,0625° (~6,5 km)")
    now = dt.datetime.now(UTC)
    base = now.replace(minute=0, second=0, microsecond=0, hour=now.hour - now.hour % 6)
    ultimo = 120
    for k in range(5):
        run = base - dt.timedelta(hours=6 * k)
        u = "%s/%02d/tot_prec/icon-eu_europe_regular-lat-lon_single-level_%s_%03d_TOT_PREC.grib2.bz2" % (DWD, run.hour, run.strftime("%Y%m%d%H"), ultimo)
        if S.head(u, timeout=20).status_code == 200:
            m.run = run
            break
    if not m.run:
        raise RuntimeError("ICON-EU no disponible")
    rs, hh = m.run.strftime("%Y%m%d%H"), m.run.hour
    log("ICON-EU: pasada %s" % m.run.strftime("%Y-%m-%d %HZ"))
    steps = list(range(0, ultimo + 1, PASO))
    trabajos = []
    for var in ICON_SINGLE:
        for st in steps:
            trabajos.append((var, None, st, "%s/%02d/%s/icon-eu_europe_regular-lat-lon_single-level_%s_%03d_%s.grib2.bz2" % (DWD, hh, var, rs, st, var.upper())))
    for var, levs in ICON_PL.items():
        for lev in levs:
            for st in steps:
                trabajos.append((var, lev, st, "%s/%02d/%s/icon-eu_europe_regular-lat-lon_pressure-level_%s_%03d_%d_%s.grib2.bz2" % (DWD, hh, var, rs, st, lev, var.upper())))
    trabajos.append(("hsurf", None, 0, "%s/%02d/hsurf/icon-eu_europe_regular-lat-lon_time-invariant_%s_HSURF.grib2.bz2" % (DWD, hh, rs)))

    def bajar(tr):
        var, lev, st, url = tr
        r = S.get(url, timeout=120)
        if r.status_code != 200:
            return tr, None
        meta, v = decode(bz2.decompress(r.content))
        return tr, v

    fallos = 0
    with cf.ThreadPoolExecutor(12) as ex:
        for (var, lev, st, url), v in ex.map(bajar, trabajos):
            if v is None:
                fallos += 1
                continue
            t = m.run + dt.timedelta(hours=st)
            if lev is not None:
                if var == "t":
                    m.put(("t", lev), t, v - 273.15)
                elif var == "fi":
                    m.put(("gh", lev), t, v / G)
                else:
                    m.put((var, lev), t, v)
            elif var == "t_2m":
                m.put("t2", t, v - 273.15)
            elif var == "u_10m":
                m.put("u10", t, v)
            elif var == "v_10m":
                m.put("v10", t, v)
            elif var == "vmax_10m":
                m.put("gust", t, v)
            elif var == "tot_prec":
                m.acc[t] = v
            elif var == "clct":
                m.put("tcc", t, v)
            elif var == "hzerocl":
                m.put("iso0", t, v)
            elif var == "snowlmt":
                m.put("snowl", t, v)
            elif var == "cape_ml":
                m.put("cape", t, v)
            elif var == "hsurf":
                m.put("orog", t, v)
    log("ICON-EU: %d ficheros, %d no disponibles" % (len(trabajos), fallos))
    m.acc.setdefault(m.run, np.zeros(NP))
    return m


# ------------------------------------------------------------------ cálculo por punto
def en_tiempo(serie, t, maxgap=6):
    """Valor de una serie {tiempo: array} en t (lineal entre pasos de hasta maxgap horas)."""
    if not serie:
        return None
    if t in serie:
        return serie[t]
    ts = sorted(serie)
    if t < ts[0] or t > ts[-1]:
        return None
    for a, b in zip(ts, ts[1:]):
        if a < t < b:
            if (b - a).total_seconds() / 3600 > maxgap:
                return None
            f = (t - a).total_seconds() / (b - a).total_seconds()
            return serie[a] * (1 - f) + serie[b] * f
    return None


def perfil_en(alt, sup_h, sup_v, niveles):
    """Interpola en la vertical: sup_h/sup_v = suelo del modelo; niveles = [(altura, valor)]."""
    pts = []
    if sup_h is not None and not np.isnan(sup_h) and sup_v is not None and not np.isnan(sup_v):
        pts.append((sup_h, sup_v))
    for h, v in niveles:
        if h is None or v is None or np.isnan(h) or np.isnan(v):
            continue
        if sup_h is not None and not np.isnan(sup_h) and h <= sup_h + 20:
            continue  # nivel bajo tierra en el modelo
        pts.append((h, v))
    pts.sort()
    if len(pts) < 2:
        return None
    for (h0, v0), (h1, v1) in zip(pts, pts[1:]):
        if h0 <= alt <= h1:
            return v0 + (v1 - v0) * (alt - h0) / (h1 - h0)
    return None


def isocero(sup_h, t2, niveles):
    """Altura de 0 °C a partir del perfil (suelo + niveles), de arriba abajo."""
    pts = []
    if sup_h is not None and not np.isnan(sup_h) and t2 is not None and not np.isnan(t2):
        pts.append((sup_h, t2))
    for h, t in niveles:
        if h is None or t is None or np.isnan(h) or np.isnan(t):
            continue
        if pts and h <= pts[0][0] + 20:
            continue
        pts.append((h, t))
    pts.sort()
    if not pts:
        return None
    if pts[0][1] <= 0:
        return pts[0][0]
    for (h0, t0), (h1, t1) in zip(pts, pts[1:]):
        if t0 > 0 >= t1:
            return h0 + (h1 - h0) * t0 / (t0 - t1)
    return None


def r(x, nd=0):
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return None
    return round(float(x), nd) if nd else int(round(float(x)))


def series_modelo(m, eje, orog_proxy):
    """Para cada macizo, las series del modelo m en el eje de tiempos."""
    out = {}
    lev_t = sorted({lev for (sn, lev) in [k for k in m.campos if isinstance(k, tuple)] if sn == "t"})
    lev_w = sorted({lev for (sn, lev) in [k for k in m.campos if isinstance(k, tuple)] if sn == "u"})
    orog = m.campos.get("orog")
    orog_v = None
    if orog:
        orog_v = list(orog.values())[0]
    elif orog_proxy is not None:
        orog_v = orog_proxy
    for k, mac in enumerate(MACIZOS):
        b, c = 2 * k, 2 * k + 1
        s = {x: [] for x in ("tv", "tc", "wc", "dc", "wv", "gv", "pr", "cc", "i0", "sl", "cp")}
        for t in eje:
            g = lambda var, p: (lambda a: None if a is None else float(a[p]))(en_tiempo(m.campos.get(var), t))
            t2b, t2c = g("t2", b), g("t2", c)
            hb = float(orog_v[b]) if orog_v is not None else None
            hc = float(orog_v[c]) if orog_v is not None else None
            # base: 2 m corregida a la altitud real
            tv = None if t2b is None else (t2b + ((hb - mac["base"]["alt"]) * 0.0065 if hb is not None and not math.isnan(hb) else 0))
            # cumbre: perfil vertical
            niv_t = [(g(("gh", l), c), g(("t", l), c)) for l in lev_t]
            tc = perfil_en(mac["cumbre"]["alt"], hc, t2c, niv_t)
            if tc is None and t2c is not None and hc is not None and not math.isnan(hc):
                tc = t2c + (hc - mac["cumbre"]["alt"]) * 0.0065
            u10c, v10c = g("u10", c), g("v10", c)
            niv_u = [(g(("gh", l), c), g(("u", l), c)) for l in lev_w]
            niv_v = [(g(("gh", l), c), g(("v", l), c)) for l in lev_w]
            uc = perfil_en(mac["cumbre"]["alt"], None if hc is None else hc + 10, u10c, niv_u)
            vc = perfil_en(mac["cumbre"]["alt"], None if hc is None else hc + 10, v10c, niv_v)
            if (uc is None or vc is None) and u10c is not None and v10c is not None and hc is not None and hc >= mac["cumbre"]["alt"]:
                uc, vc = u10c, v10c  # cumbre por debajo del suelo del modelo: viento a 10 m
            wc = dc = None
            if uc is not None and vc is not None:
                wc = math.hypot(uc, vc) * 3.6
                dc = (math.degrees(math.atan2(-uc, -vc)) + 360) % 360
            u10b, v10b = g("u10", b), g("v10", b)
            wv = None if u10b is None or v10b is None else math.hypot(u10b, v10b) * 3.6
            gb = g("gust", b)
            gv = None if gb is None else gb * 3.6
            # precipitación de las 3 h anteriores (media de base y cumbre)
            a1, a0 = en_tiempo(m.acc, t, 6), en_tiempo(m.acc, t - dt.timedelta(hours=PASO), 6)
            pr = None
            if a1 is not None and a0 is not None:
                pr = max(0.0, float((a1[b] - a0[b] + a1[c] - a0[c]) / 2))
            ccb, ccc = g("tcc", b), g("tcc", c)
            cc = None if ccb is None and ccc is None else np.nanmean([x for x in (ccb, ccc) if x is not None])
            i0 = g("iso0", c)
            if i0 is None or math.isnan(i0):
                i0 = isocero(hc, t2c, niv_t)
            sl = g("snowl", c)
            if sl is None or math.isnan(sl) or sl <= 0:
                sl = None if i0 is None else max(0, i0 - 300)
            cpb, cpc = g("cape", b), g("cape", c)
            cp = None if cpb is None and cpc is None else max(x for x in (cpb, cpc) if x is not None)
            vals = dict(tv=r(tv, 1), tc=r(tc, 1), wc=r(wc), dc=r(dc), wv=r(wv), gv=r(gv), pr=r(pr, 1), cc=r(cc),
                        i0=None if i0 is None else int(round(i0 / 10.0) * 10), sl=None if sl is None else int(round(sl / 10.0) * 10), cp=r(cp))
            for x in s:
                s[x].append(vals[x])
        out[mac["id"]] = s
    return out


# ------------------------------------------------------------------ resumen diario
def mediana(vals):
    v = [x for x in vals if x is not None]
    if not v:
        return None
    v.sort()
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def icono(pr, nieve, tormenta, nubes):
    if tormenta:
        return "tormenta"
    if pr is not None and pr >= 2:
        return "nieve" if nieve else "lluvia"
    if pr is not None and pr >= 0.3:
        return "nieve-debil" if nieve else "chubascos"
    if nubes is None:
        return "sol"
    return "sol" if nubes < 25 else "poco-nuboso" if nubes < 60 else "nuboso" if nubes < 85 else "cubierto"


def dias(eje, modelos_series, mac_id):
    """Resumen por día local (consenso = mediana de los modelos disponibles)."""
    ms = {m: s[mac_id] for m, s in modelos_series.items()}
    n = len(eje)
    cons = {x: [mediana([ms[m][x][i] for m in ms]) for i in range(n)] for x in ("tv", "tc", "wc", "dc", "wv", "gv", "pr", "cc", "i0", "sl", "cp")}
    def dir_media(i):  # media circular de la dirección del viento
        d = [ms[m]["dc"][i] for m in ms if ms[m]["dc"][i] is not None]
        if not d:
            return None
        sx, sy = sum(math.sin(math.radians(v)) for v in d), sum(math.cos(math.radians(v)) for v in d)
        return (math.degrees(math.atan2(sx, sy)) + 360) % 360
    cons["dc"] = [dir_media(i) for i in range(n)]
    for x in cons:
        nd = 1 if x in ("tv", "tc", "pr") else 0
        cons[x] = [None if v is None else (round(v, 1) if nd else (int(round(v / 10.0) * 10) if x in ("i0", "sl") else int(round(v)))) for v in cons[x]]
    grupos = {}
    for i, t in enumerate(eje):
        d = (t - dt.timedelta(minutes=90)).astimezone(TZ).date()
        grupos.setdefault(d, []).append(i)
    out = []
    for d, idx in sorted(grupos.items())[:8]:
        if len(idx) < 3:
            continue
        val = lambda x: [cons[x][i] for i in idx if cons[x][i] is not None]
        prs = val("pr")
        pr = round(sum(prs), 1) if prs else None
        nieve_c = sum((cons["pr"][i] or 0) for i in idx if cons["tc"][i] is not None and cons["tc"][i] <= 0.5)
        nieve_b = sum((cons["pr"][i] or 0) for i in idx if cons["tv"][i] is not None and cons["tv"][i] <= 1.0)
        # tormenta: algún modelo con CAPE >= 500 J/kg y precipitación >= 0,3 mm en el mismo tramo
        votos = 0
        for m in ms:
            if any((ms[m]["cp"][i] or 0) >= 500 and (ms[m]["pr"][i] or 0) >= 0.3 for i in idx):
                votos += 1
        diurnas = [cons["cc"][i] for i in idx if cons["cc"][i] is not None and 8 <= eje[i].astimezone(TZ).hour <= 20]
        nubes = sum(diurnas) / len(diurnas) if diurnas else None
        wcs = [(cons["wc"][i], cons["dc"][i]) for i in idx if cons["wc"][i] is not None]
        wmax = max(wcs) if wcs else (None, None)
        gvs = val("gv")
        tc, tv, i0 = val("tc"), val("tv"), val("i0")
        # acuerdo entre modelos (precipitación del día y máxima en cumbre)
        prm, tmm = [], []
        for m in ms:
            p = [ms[m]["pr"][i] for i in idx if ms[m]["pr"][i] is not None]
            tt = [ms[m]["tc"][i] for i in idx if ms[m]["tc"][i] is not None]
            if len(p) >= len(idx) - 1:
                prm.append(sum(p))
            if tt:
                tmm.append(max(tt))
        acuerdo = None
        if len(prm) >= 2 or len(tmm) >= 2:
            dp = (max(prm) - min(prm)) if len(prm) >= 2 else 0
            dtm = (max(tmm) - min(tmm)) if len(tmm) >= 2 else 0
            rel = dp / max(3.0, max(prm) if prm else 0)
            acuerdo = "alto" if (dp < 2 or rel < 0.35) and dtm < 2.5 else "bajo" if (dp >= 8 and rel > 0.6) or dtm >= 5 else "medio"
        avisos = []
        if wmax[0] is not None and wmax[0] >= 70:
            avisos.append("Viento muy fuerte en cumbres")
        elif wmax[0] is not None and wmax[0] >= 50:
            avisos.append("Viento fuerte en cumbres")
        if votos >= 2:
            avisos.append("Tormentas probables")
        elif votos == 1:
            avisos.append("Posibles tormentas")
        if nieve_c >= 10:
            avisos.append("Nevada importante en cumbres")
        if tc and min(tc) <= -10:
            avisos.append("Frío intenso en cumbres")
        if tv and max(tv) >= 34:
            avisos.append("Calor")
        if pr is not None and pr >= 30:
            avisos.append("Lluvia abundante")
        out.append({
            "fecha": d.isoformat(), "horas": len(idx) * PASO,
            "icono": icono(pr, nieve_c >= max(0.3, 0.5 * (pr or 0)), votos >= 2 or (votos == 1 and len(ms) == 1), nubes),
            "tv_min": r(min(tv), 0) if tv else None, "tv_max": r(max(tv), 0) if tv else None,
            "tc_min": r(min(tc), 0) if tc else None, "tc_max": r(max(tc), 0) if tc else None,
            "wc_max": r(wmax[0]), "wc_dir": r(wmax[1]), "gv_max": r(max(gvs)) if gvs else None,
            "pr": pr, "nieve_c": round(nieve_c), "nieve_b": round(nieve_b),
            "i0_min": min(i0) if i0 else None, "i0_max": max(i0) if i0 else None,
            "nubes": r(nubes), "tormenta": votos, "acuerdo": acuerdo, "avisos": avisos,
        })
    return out, cons


# ------------------------------------------------------------------ principal
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="meteo-out")
    ap.add_argument("--modelos", default="ecmwf,gfs,icon")
    ap.add_argument("--limite", type=int, default=22, help="minutos máximos de descarga")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    funcs = {"ecmwf": ecmwf, "gfs": gfs, "icon": icon}
    modelos = {}
    inicio = time.time()

    def lanzar(nombre):
        t0 = time.time()
        res = funcs[nombre]()
        log("%s listo en %.0f s" % (nombre, time.time() - t0))
        return res
    ex = cf.ThreadPoolExecutor(3)
    futs = {ex.submit(lanzar, nombre): nombre for nombre in a.modelos.split(",")}
    try:
        for f in cf.as_completed(futs, timeout=a.limite * 60):
            try:
                modelos[futs[f]] = f.result()
            except Exception:
                log("ERROR en %s:\n%s" % (futs[f], traceback.format_exc()))
    except cf.TimeoutError:
        log("Tiempo máximo (%d min): sigo sin %s" % (a.limite, ", ".join(n for f, n in futs.items() if not f.done())))
    ex.shutdown(wait=False, cancel_futures=True)
    log("Descargas: %.0f s" % (time.time() - inicio))
    if not modelos:
        sys.exit("Ningún modelo disponible: no se publica nada.")
    now = dt.datetime.now(UTC)
    t0 = now.replace(minute=0, second=0, microsecond=0, hour=now.hour - now.hour % PASO)
    eje = [t0 + dt.timedelta(hours=PASO * i) for i in range(HORAS // PASO + 1)]
    orog_proxy = None
    if "gfs" in modelos and modelos["gfs"].campos.get("orog"):
        orog_proxy = list(modelos["gfs"].campos["orog"].values())[0]
    series = {n: series_modelo(m, eje, orog_proxy if n == "ecmwf" else None) for n, m in modelos.items()}
    info = {n: {"nombre": m.etiqueta, "resol": m.resol, "pasada": m.run.strftime("%Y-%m-%dT%H:%MZ")} for n, m in modelos.items()}
    gen = now.strftime("%Y-%m-%dT%H:%MZ")
    resumen = {"generado": gen, "modelos": info, "regiones": REGIONES, "macizos": []}
    for mac in MACIZOS:
        ds, cons = dias(eje, series, mac["id"])
        doc = {"id": mac["id"], "nombre": mac["nombre"], "region": mac["region"], "base": mac["base"], "cumbre": mac["cumbre"],
               "generado": gen, "modelos": info, "t0": eje[0].strftime("%Y-%m-%dT%H:%MZ"), "paso": PASO,
               "series": {n: s[mac["id"]] for n, s in series.items()}, "consenso": cons, "dias": ds}
        json.dump(doc, open(os.path.join(a.out, mac["id"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
        resumen["macizos"].append({"id": mac["id"], "nombre": mac["nombre"], "corto": mac["corto"], "region": mac["region"],
                                   "base": mac["base"], "cumbre": mac["cumbre"], "dias": ds})
        d0 = ds[0] if ds else {}
        log("%-28s hoy: cumbre %s/%s °C, viento %s km/h, precip %s mm, isocero %s m, %s" % (
            mac["id"], d0.get("tc_min"), d0.get("tc_max"), d0.get("wc_max"), d0.get("pr"), d0.get("i0_min"), ",".join(d0.get("avisos", []))))
    json.dump(resumen, open(os.path.join(a.out, "resumen.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    log("Escritos %d macizos con modelos: %s" % (len(MACIZOS), ", ".join(modelos)))
    sys.stdout.flush()
    os._exit(0)  # no esperar a descargas que se hayan quedado colgadas


if __name__ == "__main__":
    main()
