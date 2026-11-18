"""Descarga la delimitación oficial de las zonas de aviso de AEMET (Meteoalerta) y la deja simplificada
en zonas-aemet.json: {codigo: {"n": nombre, "p": [[[lat, lon], ...], ...]}}. Además muestra códigos de los CAP actuales."""
import io, json, sys, zipfile, urllib.request, xml.etree.ElementTree as ET
import shapefile  # pyshp
from pyproj import Transformer

URL = "https://www.aemet.es/documentos/es/eltiempo/prediccion/avisos/plan_meteoalerta/AEMET-meteoalerta-delimitacion-zonas.zip"
sys.path.insert(0, "meteo")


def simplifica(pts, tol=0.004):
    if len(pts) < 4:
        return [[round(a, 3), round(o, 3)] for a, o in pts]
    keep = {0, len(pts) - 1}
    pila = [(0, len(pts) - 1)]
    while pila:
        ini, fin = pila.pop()
        (a1, o1), (a2, o2) = pts[ini], pts[fin]
        L = ((a2 - a1) ** 2 + (o2 - o1) ** 2) ** 0.5 or 1e-12
        dmax, idx = 0, None
        for k in range(ini + 1, fin):
            a, o = pts[k]
            d = abs((a2 - a1) * (o1 - o) - (a1 - a) * (o2 - o1)) / L
            if d > dmax:
                dmax, idx = d, k
        if idx is not None and dmax > tol:
            keep.add(idx); pila += [(ini, idx), (idx, fin)]
    return [[round(pts[k][0], 3), round(pts[k][1], 3)] for k in sorted(keep)]


req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 guiasadastra.com"})
z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(req, timeout=120).read()))
print("Archivos:", z.namelist())
shp = [n for n in z.namelist() if n.lower().endswith(".shp")][0]
base = shp[:-4]
prj = z.read(base + ".prj").decode(errors="ignore") if base + ".prj" in z.namelist() else ""
print("Proyección:", prj[:200])
r = shapefile.Reader(shp=io.BytesIO(z.read(shp)), dbf=io.BytesIO(z.read(base + ".dbf")), shx=io.BytesIO(z.read(base + ".shx")), encoding="latin-1")
campos = [f[0] for f in r.fields[1:]]
print("Campos:", campos)
geo = "GEOGCS" in prj and "PROJCS" not in prj
tr = None if geo else Transformer.from_crs(prj and __import__("pyproj").CRS.from_wkt(prj), "EPSG:4326", always_xy=True)
out = {}
for i, sr in enumerate(r.iterShapeRecords()):
    rec = dict(zip(campos, sr.record))
    if i < 3:
        print("Ejemplo:", rec)
    partes = list(sr.shape.parts) + [len(sr.shape.points)]
    polis = []
    for a, b in zip(partes, partes[1:]):
        xy = sr.shape.points[a:b]
        if tr:
            xy = [tr.transform(x, y) for x, y in xy]
        ll = [(y, x) for x, y in xy]
        s = simplifica(ll)
        if len(s) >= 4:
            polis.append(s)
    cod = str(rec.get("COD_Z") or rec.get("cod_z") or i)
    nom = rec.get("NOM_Z") or rec.get("nom_z") or ""
    out[cod] = {"n": nom, "p": polis, "prov": rec.get("NOM_PROV", "")}
json.dump(out, open("zonas-aemet.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("Zonas:", len(out), "tamaño", len(json.dumps(out)) // 1024, "KB")

# códigos que llegan en los CAP de MeteoAlarm, para saber cómo emparejar
feed = ET.fromstring(urllib.request.urlopen("https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-spain", timeout=60).read())
enl = [l.get("href") for l in feed.iter("{http://www.w3.org/2005/Atom}link") if "cap" in (l.get("type") or "")][:6]
for u in enl:
    x = urllib.request.urlopen(u, timeout=60).read().decode(errors="ignore")
    i = x.find("<area")
    print("CAP:", " ".join(x[i:i + 900].split())[:900])
