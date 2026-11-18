"""Genera ilustraciones con la API de Gemini a partir de un lote JSON.

Uso: python tools/genera_imagenes.py tools/imagenes/lote-capas.json [--solo nombre1,nombre2] [--modelo ID]
La clave se lee de la variable de entorno GEMINI_API_KEY (secreto de GitHub, nunca en el repositorio).
Las imágenes salen en imagenes-generadas/<nombre>.png y no se publican: se revisan antes de usarlas.
"""
import argparse, base64, io, json, os, sys, time, urllib.request, urllib.error
from PIL import Image

API = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent"


def parte_imagen(ruta):
    im = Image.open(ruta).convert("RGB")
    im.thumbnail((1400, 1400))
    b = io.BytesIO(); im.save(b, "JPEG", quality=90)
    return {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(b.getvalue()).decode()}}


def generar(modelo, clave, texto, refs, aspecto):
    cuerpo = {"contents": [{"parts": [parte_imagen(r) for r in refs] + [{"text": texto}]}],
              "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspecto}}}
    req = urllib.request.Request(API % modelo, data=json.dumps(cuerpo).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": clave})
    for intento in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.load(r)
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:600]
            if e.code in (429, 500, 503) and intento < 2:
                print("  reintento tras error", e.code); time.sleep(20 * (intento + 1)); continue
            raise SystemExit("Error %s de la API: %s" % (e.code, msg))
    for c in d.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            datos = p.get("inline_data") or p.get("inlineData")
            if datos:
                return base64.b64decode(datos["data"])
    raise RuntimeError("La respuesta no trae imagen: %s" % json.dumps(d)[:600])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lote"); ap.add_argument("--solo", default=""); ap.add_argument("--modelo", default="")
    a = ap.parse_args()
    clave = os.environ.get("GEMINI_API_KEY", "").strip()
    if not clave:
        raise SystemExit("Falta el secreto GEMINI_API_KEY en GitHub (Settings → Secrets and variables → Actions).")
    lote = json.load(open(a.lote, encoding="utf-8"))
    modelo = a.modelo or lote.get("modelo", "gemini-2.5-flash-image")
    solo = {s.strip() for s in a.solo.split(",") if s.strip()}
    os.makedirs("imagenes-generadas", exist_ok=True)
    fallos = 0
    for it in lote["imagenes"]:
        if solo and it["nombre"] not in solo:
            continue
        texto = lote.get("estilo", "") + "\n\n" + it["prompt"]
        refs = it.get("referencias", lote.get("referencias", []))
        print("Generando", it["nombre"], "con", modelo)
        try:
            png = generar(modelo, clave, texto, refs, it.get("aspecto", lote.get("aspecto", "9:16")))
        except RuntimeError as e:
            print("  ", e); fallos += 1; continue
        with open("imagenes-generadas/%s.png" % it["nombre"], "wb") as f:
            f.write(png)
        print("  ok,", len(png) // 1024, "KB")
    if fallos:
        sys.exit(1)


if __name__ == "__main__":
    main()
