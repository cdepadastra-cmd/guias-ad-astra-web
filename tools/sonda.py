"""Sonda puntual: descarga URLs de una lista y guarda estado y primeros bytes en salida/ (se ejecuta en GitHub Actions)."""
import json, os, sys, urllib.request, hashlib
os.makedirs("salida", exist_ok=True)
res = {}
for u in json.load(open(sys.argv[2])):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 guiasadastra.com"}), timeout=40)
        b = r.read()
        n = hashlib.md5(u.encode()).hexdigest()[:10]
        open("salida/%s.bin" % n, "wb").write(b)
        res[u] = {"status": r.status, "len": len(b), "file": n, "ct": r.headers.get("content-type"), "head": b[:600].decode("utf-8", "replace")}
    except Exception as ex:
        res[u] = {"error": str(ex)}
    print(u, res[u].get("status"), res[u].get("len"), res[u].get("error"))
json.dump(res, open("salida/sonda.json", "w"), ensure_ascii=False, indent=1)
