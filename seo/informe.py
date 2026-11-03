# -*- coding: utf-8 -*-
"""Seguimiento SEO mensual de guiasadastra.com con datos de DataForSEO.

Uso:  python3 seo/informe.py RANKED.json VOLUMENES.json FECHA(AAAA-MM-DD)
  RANKED.json     -> respuesta de /v3/dataforseo_labs/google/ranked_keywords/live (target guiasadastra.com, ES, es)
  VOLUMENES.json  -> respuesta de /v3/keywords_data/google_ads/search_volume/live con seo/palabras-clave.txt
Escribe seo/historico/FECHA.csv y imprime un resumen en Markdown comparando con el mes anterior.
"""
import csv, glob, json, os, sys

def cargar(path):
    t = open(path, encoding="utf-8").read()
    return json.loads(t[t.index("{"):])

def main(ranked_path, vol_path, fecha):
    base = os.path.dirname(os.path.abspath(__file__))
    claves = [l.strip() for l in open(os.path.join(base, "palabras-clave.txt"), encoding="utf-8") if l.strip() and not l.startswith("#")]
    pos, url = {}, {}
    for task in cargar(ranked_path)["tasks"]:
        for r in task.get("result") or []:
            for it in r.get("items") or []:
                k = it["keyword_data"]["keyword"].lower()
                se = it["ranked_serp_element"]["serp_item"]
                if k not in pos or se["rank_absolute"] < pos[k]:
                    pos[k], url[k] = se["rank_absolute"], se.get("url", "").replace("https://www.guiasadastra.com", "")
    vol = {}
    for task in cargar(vol_path)["tasks"]:
        for r in task.get("result") or []:
            vol[r["keyword"].lower()] = r.get("search_volume")
    prev_files = sorted(f for f in glob.glob(os.path.join(base, "historico", "*.csv")) if os.path.basename(f) < fecha + ".csv")
    prev = {}
    if prev_files:
        for row in csv.DictReader(open(prev_files[-1], encoding="utf-8")):
            prev[row["busqueda"]] = row
    filas = []
    for k in claves:
        p = pos.get(k.lower())
        filas.append({"busqueda": k, "busquedas_mes": vol.get(k.lower()) or "", "posicion": p or "", "pagina": url.get(k.lower(), "")})
    out = os.path.join(base, "historico", fecha + ".csv")
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["busqueda", "busquedas_mes", "posicion", "pagina"]); w.writeheader(); w.writerows(filas)
    # resumen
    total = len(pos)
    top3 = sum(1 for v in pos.values() if v <= 3); top10 = sum(1 for v in pos.values() if v <= 10)
    print("Seguimiento SEO %s · %d búsquedas con la web en el top 100 · %d en el top 10 · %d en el top 3" % (fecha, total, top10, top3))
    print("Comparado con: %s" % (os.path.basename(prev_files[-1])[:-4] if prev_files else "nada (primer mes)"))
    print("")
    print("| Búsqueda | Al mes | Posición | Antes | Cambio |")
    print("| --- | --- | --- | --- | --- |")
    for r in sorted(filas, key=lambda r: -(int(r["busquedas_mes"] or 0))):
        antes = (prev.get(r["busqueda"]) or {}).get("posicion", "")
        a, b = int(antes) if antes else None, int(r["posicion"]) if r["posicion"] else None
        cambio = "nueva" if b and not a and prev else ("sale" if a and not b else ("" if not (a and b) else ("+%d" % (a - b) if a > b else ("%d" % (a - b) if a < b else "="))))
        print("| %s | %s | %s | %s | %s |" % (r["busqueda"], r["busquedas_mes"] or "–", b or "fuera del top 100", a or "–", cambio))
    otras = sorted(((v, k) for k, v in pos.items() if k not in {c.lower() for c in claves}))[:15]
    if otras:
        print("\nOtras búsquedas donde ya aparece la web (mejores posiciones): " + "; ".join("%s (%d)" % (k, v) for v, k in otras))

if __name__ == "__main__":
    main(*sys.argv[1:4])
