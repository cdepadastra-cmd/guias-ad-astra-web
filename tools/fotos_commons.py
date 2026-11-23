"""Busca y descarga fotos con licencia libre de Wikimedia Commons (se ejecuta en GitHub Actions).
  python tools/fotos_commons.py buscar tools/fotos/busquedas.json   -> salida/buscar.json + miniaturas
  python tools/fotos_commons.py bajar  tools/fotos/elegidas.json    -> salida/<nombre>.jpg + salida/bajar.json (autor y licencia)
"""
import json, os, sys, urllib.parse, urllib.request
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "GuiasAdAstraWeb/1.0 (https://www.guiasadastra.com; guiasadastra web build)"}
os.makedirs("salida", exist_ok=True)


def api(**q):
    q.update(format="json", formatversion=2)
    with urllib.request.urlopen(urllib.request.Request(API + "?" + urllib.parse.urlencode(q), headers=UA), timeout=60) as r:
        return json.load(r)


def baja(u, f):
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120) as r, open(f, "wb") as o:
        o.write(r.read())


def meta(ii):
    m = ii.get("extmetadata", {})
    g = lambda k: (m.get(k) or {}).get("value", "")
    return {"autor": g("Artist"), "licencia": g("LicenseShortName"), "licencia_url": g("LicenseUrl"), "pagina": ii.get("descriptionurl"), "ancho": ii.get("width"), "alto": ii.get("height")}


modo, lista = sys.argv[1], json.load(open(sys.argv[2]))
out = {}
if modo == "buscar":
    for clave, q in lista.items():
        r = api(action="query", generator="search", gsrsearch="filetype:bitmap " + q, gsrnamespace=6, gsrlimit=10,
                prop="imageinfo", iiprop="url|extmetadata|size", iiurlwidth=360)
        res = []
        for i, pg in enumerate(sorted(r.get("query", {}).get("pages", []), key=lambda p: p.get("index", 0))):
            ii = pg["imageinfo"][0]
            f = "salida/%s_%d.jpg" % (clave, i)
            try:
                baja(ii["thumburl"], f)
            except Exception as ex:
                print("error", ex); continue
            res.append(dict(titulo=pg["title"], mini=f, **meta(ii)))
        out[clave] = res
        print(clave, len(res))
    json.dump(out, open("salida/buscar.json", "w"), ensure_ascii=False, indent=1)
else:
    for nombre, titulo in lista.items():
        r = api(action="query", titles=titulo, prop="imageinfo", iiprop="url|extmetadata|size", iiurlwidth=1600)
        ii = r["query"]["pages"][0]["imageinfo"][0]
        baja(ii["thumburl"], "salida/%s.jpg" % nombre)
        out[nombre] = dict(titulo=titulo, **meta(ii))
        print(nombre, titulo)
    json.dump(out, open("salida/bajar.json", "w"), ensure_ascii=False, indent=1)
