# -*- coding: utf-8 -*-
"""Estado de los barrancos: caudal de los ríos en los aforos oficiales (SAIH Tajo y SAIH Duero).

Lee los aforos de referencia de cada barranco, guarda un histórico de 72 h (se recupera del rios.json publicado),
calcula la tendencia, aplica los umbrales de los guías y añade la lluvia prevista de la zona (de la previsión de meteo).

    python3 meteo/rios.py --out rios-out [--meteo meteo-out]
Escribe rios-out/rios.json.
"""
import argparse, datetime as dt, json, os, re, ssl, sys, urllib.parse, urllib.request
from zoneinfo import ZoneInfo

MADRID = ZoneInfo("Europe/Madrid")

UTC = dt.timezone.utc
WEB = "https://www.guiasadastra.com"
H = {"User-Agent": "guiasadastra.com (estado de barrancos)", "Accept-Language": "es-ES"}
CA = os.environ.get("SAIH_CA_BUNDLE")  # SAIH Duero no envía su certificado intermedio: se añade al almacén

# ------------------------------------------------------------------ barrancos y sus aforos
# umbrales: lista de (caudal máximo en m3/s, estado, texto), de menos a más; el último con None = "por encima".
BARRANCOS = [
    {"id": "los-hoyos", "nombre": "Barranco de los Hoyos", "lugar": "Jerte (Cáceres)", "macizo": "valle-del-jerte",
     "actividad": "/actividades/barranquismo-en-caceres/",
     "aforo": {"fuente": "tajo", "codigo": "AR42", "buscar": "Jerte", "nombre": "Jerte en El Torno"},
     "umbrales": [(8, "poco", "Poco caudal"), (17, "bueno", "Caudal bueno"),
                  (20, "alto", "Alegre: solo con experiencia y mucho cuidado"), (None, "no", "Muy alto: no recomendable")]},
    {"id": "los-papuos", "nombre": "Garganta de los Papúos", "lugar": "Valle del Jerte (Cáceres)", "macizo": "valle-del-jerte",
     "actividad": "/actividades/barranquismo-en-caceres/",
     "aforo": {"fuente": "tajo", "codigo": "AR42", "buscar": "Jerte", "nombre": "Jerte en El Torno"},
     "umbrales": [(8, "poco", "Poco caudal"), (17, "bueno", "Caudal bueno"),
                  (20, "alto", "Alegre: solo con experiencia y mucho cuidado"), (None, "no", "Muy alto: no recomendable")]},
    {"id": "mazobre", "nombre": "Barranco de Mazobre", "lugar": "Cardaño de Abajo (Palencia)", "macizo": "montana-palentina",
     "actividad": "/actividades/barranquismo-palencia/",
     "aforo": {"fuente": "duero", "codigo": "EA512", "nombre": "Carrión en Triollo"},
     "lluvia": {"fuente": "duero", "codigo": "PL102", "nombre": "Vidrieros"},
     # provisionales: el 27-7-2026 bajaba con poca agua; en el estiaje de 2026 el aforo marcó 0,2-1,2 m3/s
     "provisional": True,
     "umbrales": [(0.5, "poco", "Poco caudal"), (2, "bueno", "Caudal bueno"),
                  (4, "alto", "Caudal alto: con experiencia y mucho cuidado"), (None, "no", "Muy alto: no recomendable")]},
    {"id": "valporquero", "nombre": "Cueva de Valporquero", "lugar": "Valporquero (León)", "macizo": "montanas-de-leon",
     "actividad": "/actividades/barranquismo-cueva-valporquero-sima-de-perlas/",
     "aforo": {"fuente": "duero", "codigo": "EA150", "nombre": "Torío en Matallana"},
     "lluvia": {"fuente": "duero", "codigo": "PL201", "nombre": "Valporquero"},
     # provisionales: se hace todo julio y agosto con caudal normal; en agosto de 2026 el aforo marcó 0,2-1,9 m3/s (máx. 2,8)
     "provisional": True,
     "umbrales": [(2, "bueno", "Caudal normal de verano"), (3.5, "alto", "Más agua de lo normal: con mucho cuidado"),
                  (None, "no", "Muy alto: no recomendable")]},
]


def log(*a):
    print(dt.datetime.now().strftime("%H:%M:%S"), *a, flush=True)


def get(url, data=None, xhr=False, ctx=None, timeout=40):
    h = dict(H)
    if xhr:
        h["X-Requested-With"] = "XMLHttpRequest"
    body = urllib.parse.urlencode(data).encode() if data else None
    return urllib.request.urlopen(urllib.request.Request(url, data=body, headers=h), timeout=timeout, context=ctx).read().decode("utf-8", "ignore")


def num(s):
    s = (s or "").split()[0].replace(".", "").replace(",", ".") if s else ""
    try:
        return float(s)
    except ValueError:
        return None


# ------------------------------------------------------------------ SAIH Tajo
def tajo(codigo, buscar):
    """Serie horaria de las últimas 24 h de caudal (m3/s) de una estación del SAIH Tajo."""
    base = "https://saihtajo.chtajo.es/"
    res = json.loads(get(base + "search", {"busquedatiemporeal": buscar}, xhr=True))["response"]["results"]
    est = next(r for r in res if r["id"] == codigo)
    d = json.loads(get(base + est["url"], xhr=True))["response"]
    serie = []
    for s in d.get("senales", []):
        if "CAUDAL" in s.get("nombre", "").upper():
            for v in s.get("valores", []):
                try:
                    t = dt.datetime.strptime(v["tiempo"], "%d/%m/%Y %H:%M")
                except (KeyError, ValueError):
                    continue
                if v.get("valor") is not None:  # hora peninsular -> UTC
                    serie.append((t.replace(tzinfo=MADRID).astimezone(UTC), float(v["valor"])))
            break
    return sorted(serie)


# ------------------------------------------------------------------ SAIH Duero
_DUERO = None


def duero():
    """Último dato de todas las estaciones del SAIH Duero (página de tiempo real)."""
    global _DUERO
    if _DUERO is None:
        ctx = ssl.create_default_context(cafile=CA) if CA else None
        h = get("https://www.saihduero.es/datos-tiempo-real/risr", ctx=ctx)
        _DUERO = {}
        for bloque in re.findall(r"\{\s*id:\s*'[^']+'.*?\}", h, re.S):
            campos = dict(re.findall(r"(\w+):\s*'([^']*)'", bloque))
            if campos.get("id"):
                _DUERO.setdefault(campos["id"], {}).update(campos)
    return _DUERO


MESES = {m: i + 1 for i, m in enumerate(["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"])}


def duero_hora(c):
    try:
        dia, mes = c["date"].split()
        hh, mm = c["time"].split(":")
        hoy = dt.datetime.now(UTC)
        t = dt.datetime(hoy.year, MESES[mes[:3].lower()], int(dia), int(hh), int(mm))
        if t > hoy.replace(tzinfo=None) + dt.timedelta(days=2):
            t = t.replace(year=hoy.year - 1)
        return t.replace(tzinfo=MADRID).astimezone(UTC)
    except Exception:
        return None


# ------------------------------------------------------------------ cálculo
def estado(q, umbrales):
    if q is None or not umbrales:
        return None, None
    for lim, k, txt in umbrales:
        if lim is None or q <= lim:
            return k, txt
    return umbrales[-1][1], umbrales[-1][2]


def tendencia(serie, horas=3):
    if len(serie) < 2:
        return None
    t1, q1 = serie[-1]
    prev = [q for t, q in serie if t <= t1 - dt.timedelta(hours=horas)]
    if not prev:
        return None
    q0 = prev[-1]
    dif = q1 - q0
    if abs(dif) < max(0.05, 0.05 * q0):
        return "estable"
    return "sube" if dif > 0 else "baja"


def lluvia_prevista(macizo, meteo_dir):
    """Lluvia prevista (mm) en el macizo: próximas 24 h, 24-48 h y por día, de la previsión de meteo."""
    try:
        if meteo_dir and os.path.exists(os.path.join(meteo_dir, macizo + ".json")):
            doc = json.load(open(os.path.join(meteo_dir, macizo + ".json"), encoding="utf-8"))
        else:
            doc = json.loads(get("%s/meteo/datos/%s.json" % (WEB, macizo)))
    except Exception as ex:
        log("sin previsión de", macizo, ex)
        return None
    t0 = dt.datetime.strptime(doc["t0"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=UTC)
    ahora = dt.datetime.now(UTC)
    pr = doc["consenso"]["pr"]
    hs = doc.get("h") or [i * doc["paso"] for i in range(len(pr))]
    p24 = p48 = 0.0
    for h, p in zip(hs, pr):
        t = t0 + dt.timedelta(hours=h)
        if p is None or t <= ahora:
            continue
        if t <= ahora + dt.timedelta(hours=24):
            p24 += p
        elif t <= ahora + dt.timedelta(hours=48):
            p48 += p
    dias = [{"fecha": d["fecha"], "pr": d.get("pr"), "icono": d.get("icono"), "i0_max": d.get("i0_max")} for d in doc.get("dias", [])[:4]]
    return {"p24": round(p24, 1), "p48": round(p48, 1), "dias": dias, "macizo": doc.get("nombre")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="rios-out")
    ap.add_argument("--meteo", default=None)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    ahora = dt.datetime.now(UTC)
    # histórico publicado (para la tendencia y la gráfica de las estaciones que solo dan el último dato)
    hist = {}
    try:
        prev = json.loads(get("%s/meteo/rios/rios.json?n=%d" % (WEB, ahora.timestamp())))
        for k, v in prev.get("historico", {}).items():
            hist[k] = [(dt.datetime.strptime(t, "%Y-%m-%dT%H:%MZ").replace(tzinfo=UTC), q) for t, q in v]
        log("histórico recuperado:", {k: len(v) for k, v in hist.items()})
    except Exception as ex:
        log("sin histórico previo (%s)" % ex)

    lecturas, lluvias, errores = {}, {}, []
    for b in BARRANCOS:
        af = b["aforo"]
        clave = "%s:%s" % (af["fuente"], af["codigo"])
        if clave in lecturas:
            continue
        try:
            if af["fuente"] == "tajo":
                serie = tajo(af["codigo"], af["buscar"])
            else:
                c = duero().get(af["codigo"], {})
                q, t = num(c.get("q")), duero_hora(c)
                serie = [(t, q)] if (q is not None and t) else []
            viejo = [x for x in hist.get(clave, []) if x[0] >= ahora - dt.timedelta(hours=72)]
            junt = {t: q for t, q in viejo}
            junt.update({t: q for t, q in serie})
            lecturas[clave] = sorted(junt.items())
            log(clave, af["nombre"], "último:", lecturas[clave][-1] if lecturas[clave] else None)
        except Exception as ex:
            errores.append("%s: %s" % (af["nombre"], ex))
            log("ERROR", af["nombre"], ex)
            lecturas[clave] = hist.get(clave, [])
        ll = b.get("lluvia")
        if ll:
            try:
                c = duero().get(ll["codigo"], {})
                lluvias[b["id"]] = {"nombre": ll["nombre"], "p1h": num(c.get("p")), "t": c.get("t"),
                                    "hora": duero_hora(c).strftime("%Y-%m-%dT%H:%MZ") if duero_hora(c) else None}
            except Exception as ex:
                log("ERROR pluviómetro", ll["nombre"], ex)

    salida = []
    for b in BARRANCOS:
        af = b["aforo"]
        clave = "%s:%s" % (af["fuente"], af["codigo"])
        serie = lecturas.get(clave, [])
        q = serie[-1][1] if serie else None
        t = serie[-1][0] if serie else None
        k, txt = estado(q, b["umbrales"])
        viejo = t is not None and ahora - t > dt.timedelta(hours=6)
        salida.append({
            "id": b["id"], "nombre": b["nombre"], "lugar": b["lugar"], "actividad": b["actividad"],
            "aforo": {"nombre": af["nombre"], "codigo": af["codigo"], "fuente": "SAIH Tajo" if af["fuente"] == "tajo" else "SAIH Duero"},
            "q": None if q is None else round(q, 2), "hora": t.strftime("%Y-%m-%dT%H:%MZ") if t else None, "dato_antiguo": viejo,
            "tendencia": tendencia(serie), "max24": round(max([x[1] for x in serie if x[0] >= ahora - dt.timedelta(hours=24)] or [0]), 2) if serie else None,
            "estado": k, "estado_txt": txt,
            "umbrales": [{"hasta": u[0], "estado": u[1], "txt": u[2]} for u in b["umbrales"]] if b["umbrales"] else None,
            "provisional": bool(b.get("provisional")),
            "serie": [(x[0].strftime("%Y-%m-%dT%H:%MZ"), round(x[1], 2)) for x in serie if x[0] >= ahora - dt.timedelta(hours=48)],
            "lluvia_ahora": lluvias.get(b["id"]),
            "prevision": lluvia_prevista(b["macizo"], a.meteo),
        })
    out = {"generado": ahora.strftime("%Y-%m-%dT%H:%MZ"), "barrancos": salida, "errores": errores,
           "historico": {k: [(t.strftime("%Y-%m-%dT%H:%MZ"), q) for t, q in v] for k, v in lecturas.items()}}
    json.dump(out, open(os.path.join(a.out, "rios.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    log("rios.json escrito:", [(s["id"], s["q"], s["estado"]) for s in salida])
    if len(errores) == len({(b["aforo"]["fuente"], b["aforo"]["codigo"]) for b in BARRANCOS}):
        sys.exit(1)


if __name__ == "__main__":
    main()
