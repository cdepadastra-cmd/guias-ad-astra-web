"""Lee el blog jairogredos.blogspot.com (se ejecuta en GitHub Actions).
  python tools/blog_fotos.py blog-listar                -> salida/posts.json + salida/mini/<n>_<k>.jpg (miniaturas de cada entrada)
  python tools/blog_fotos.py blog-bajar tools/fotos/blog.json -> salida/<nombre>.jpg (fotos elegidas, a 1600 px)
"""
import json, os, re, sys, urllib.request, urllib.error
UA = {"User-Agent": "Mozilla/5.0 (GuiasAdAstraWeb)"}
BLOG = "https://jairogredos.blogspot.com"
os.makedirs("salida/mini", exist_ok=True)


def get(u, intentos=6):
    import time
    for k in range(intentos):
        try:
            time.sleep(1.2)
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as ex:
            if ex.code != 429 or k == intentos - 1:
                raise
            time.sleep(20 * (k + 1))


def tam(u, s):
    u = re.sub(r"/s\d+(-[a-z0-9-]+)?/", "/%s/" % s, u)
    return re.sub(r"=s\d+(-[a-z0-9-]+)?$", "=" + s, u)


SOLO = set(json.load(open(sys.argv[2]))) if len(sys.argv) > 2 and sys.argv[1] == "blog-listar" and os.path.exists(sys.argv[2]) else None
if sys.argv[1] == "blog-listar":
    posts, i = [], 1
    while True:
        d = json.loads(get(BLOG + "/feeds/posts/default?alt=json&max-results=150&start-index=%d" % i))
        es = d["feed"].get("entry", [])
        if not es:
            break
        for e in es:
            url = next(l["href"] for l in e["link"] if l["rel"] == "alternate")
            html = e.get("content", {}).get("$t", "")
            thumb = (e.get("media$thumbnail") or {}).get("url")
            if not html and SOLO is not None and len(posts) not in SOLO:
                html = '<img src="%s">' % thumb if thumb else ""
            elif not html:
                try:
                    pg = get(url).decode("utf-8", "ignore")
                    m = re.search(r"class=['\"]post-body[^>]*>(.*?)<div class=['\"]post-footer", pg, re.S)
                    html = m.group(1) if m else pg
                except Exception as ex:
                    print("error", url, ex)
            imgs = list(dict.fromkeys(re.findall(r'(https?://blogger\.googleusercontent\.com/img/[^"\'\s>]+|https?://\d\.bp\.blogspot\.com/[^"\'\s>]+)', html)))
            imgs = [x for x in imgs if not x.endswith((".gif",))]
            texto = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", html)).strip()
            posts.append({"n": len(posts), "titulo": e["title"]["$t"], "url": url,
                          "fecha": e["published"]["$t"][:10], "etiquetas": [c["term"] for c in e.get("category", [])], "imgs": imgs, "texto": texto[:600]})
        i += len(es)
    json.dump(posts, open("salida/posts.json", "w"), ensure_ascii=False, indent=1)
    for p in posts:
        for k, u in enumerate(p["imgs"][:4]):
            try:
                open("salida/mini/%d_%d.jpg" % (p["n"], k), "wb").write(get(tam(u.replace("http://", "https://"), "s320")))
            except Exception as ex:
                print("error", p["n"], k, ex)
    json.dump(posts, open("salida/posts.json", "w"), ensure_ascii=False, indent=1)
    print(len(posts), "entradas")
elif sys.argv[1] == "blog-bajar":
    for nombre, u in json.load(open(sys.argv[2])).items():
        open("salida/%s.jpg" % nombre, "wb").write(get(tam(u.replace("http://", "https://"), "s1600")))
        print(nombre)

if sys.argv[1] == "blog-paginas":
    # Lista de URLs de entradas -> salida/paginas.json + salida/mini/<i>_<k>.jpg (hasta 14 fotos por entrada)
    res = []
    for i, url in enumerate(json.load(open(sys.argv[2]))):
        try:
            pg = get(url).decode("utf-8", "ignore")
        except Exception as ex:
            print("error", url, ex); continue
        m = re.search(r"class=['\"]post-body[^>]*>(.*?)<div class=['\"]post-footer", pg, re.S)
        html = m.group(1) if m else pg
        imgs = []
        for u in re.findall(r'(https?://blogger\.googleusercontent\.com/img/[^"\'\s>]+|https?://\d\.bp\.blogspot\.com/[^"\'\s>]+)', html):
            clave = re.sub(r"/s\d+(-[a-z0-9-]+)?/", "/", u)
            if clave not in [re.sub(r"/s\d+(-[a-z0-9-]+)?/", "/", x) for x in imgs]:
                imgs.append(u)
        texto = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", html)).strip()
        res.append({"i": i, "url": url, "imgs": imgs, "texto": texto[:3000]})
        for k, u in enumerate(imgs[:14]):
            try:
                open("salida/mini/%d_%d.jpg" % (i, k), "wb").write(get(tam(u.replace("http://", "https://"), "s400")))
            except Exception as ex:
                print("error", ex)
        json.dump(res, open("salida/paginas.json", "w"), ensure_ascii=False, indent=1)
    print(len(res), "páginas")
