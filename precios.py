# -*- coding: utf-8 -*-
"""Precios de la web desde la hoja de Google «Precios web Guías Ad Astra».

build.py llama a aplicar() antes de generar la web. Lee la pestaña «Precios» de la hoja
(columna ID + columna Precio) y sustituye los precios de data.py. Si una celda está vacía o
no es un número entero razonable, se queda el precio de data.py para esa fila.

- PRECIOS_CSV=/ruta/archivo.csv  -> usa un CSV local (pruebas).
- PRECIOS_OFF=1                  -> no lee la hoja (usa solo data.py).
- PRECIOS_ESTRICTO=1             -> si la hoja no responde, el build falla (no se publica nada).
  Sin él, si la hoja no responde se usan los precios de data.py con un aviso.

python3 precios.py csv   -> imprime el CSV con todos los precios actuales de data.py
"""
import csv, io, os, re, sys, urllib.request, urllib.parse
import data

SHEET_ID = os.environ.get("PRECIOS_SHEET_ID", "1MQ0lXOaz-MnG91RpU39D4hgLPp6MWNE9krfj1Iq7A8c")  # «Precios web Guías Ad Astra»
SHEET_TAB = "Precios"
CAMBIOS = []


def _url():
    # exporta la PRIMERA pestaña de la hoja (la de «Precios») tal cual, sin adivinar tipos
    return "https://docs.google.com/spreadsheets/d/%s/export?format=csv" % SHEET_ID


def _slug(t):
    import unicodedata
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return "-".join("".join(c if c.isalnum() else " " for c in t).split())


# ------------------------------------------------------------------ inventario de precios
def filas():
    """Lista ordenada de (id, sección, concepto, precio, aplicar(nuevo))."""
    out, vistos = [], {}

    def add(pid, sec, concepto, precio, setter):
        if pid in vistos:  # el mismo recorrido aparece en varias páginas: una sola fila para todas
            vistos[pid][4].append(setter)
            return
        fila = [pid, sec, concepto, precio, [setter]]
        vistos[pid] = fila
        out.append(fila)

    for a in data.ACTIVITIES:
        sec = a.get("cat", "Actividades")
        if a.get("kind") == "zona":
            sec = None  # sus recorridos ya salen en su actividad
        for o in a.get("options", []) or []:
            if o.get("price"):
                s = sec or {"Barr": "Barranquismo", "Vía ": "Vías ferratas", "Esca": "Escalada"}.get(o["name"][:4], "Montaña")
                add("op:" + _slug(o["name"]), s, "%s · %s" % (o["name"], o.get("place", "")), o["price"],
                    lambda v, o=o: o.__setitem__("price", v))
        if a.get("price") and not a.get("options"):
            add("act:" + a["slug"], sec or "Actividades", a["title"], a["price"], lambda v, a=a: a.__setitem__("price", v))
        for gi, (g, rows) in enumerate(a.get("groups", []) or []):
            for ri, r in enumerate(rows):
                def set_row(v, a=a, gi=gi, ri=ri):
                    g_, rows_ = a["groups"][gi]
                    rows_ = list(rows_)
                    rows_[ri] = tuple(rows_[ri][:3]) + (v,)
                    a["groups"][gi] = (g_, rows_)
                add("cumbre:" + _slug(r[0]), "Ascensiones (" + g + ")", "%s · %s" % (r[0], r[1]), r[3], set_row)
        for pi, p in enumerate(a.get("packs", []) or []):
            if p is data.PACK_ESCALADA or p is data.PACK_FERRATA:
                pid = "extra:" + _slug(p[0])
                concepto = "Añadir a barranco: " + p[0]
            else:
                pid = "extra:%s:%s" % (a["slug"], _slug(p[0]))
                concepto = "Añadir a %s: %s" % (a["title"], p[0])

            def set_pack(v, a=a, pi=pi):
                packs = list(a["packs"])
                packs[pi] = tuple(packs[pi][:2]) + (v,)
                a["packs"] = packs
            add(pid, "Extras combinables", concepto, p[2], set_pack)

    for c in data.COURSES:
        if c.get("niveles"):
            for n in c["niveles"]:
                add("curso:%s:%s" % (c["slug"], _slug(n["name"])), "Cursos", n["name"], n["price"], lambda v, n=n: n.__setitem__("price", v))
        else:
            add("curso:" + c["slug"], "Cursos", c["title"], c["price"], lambda v, c=c: c.__setitem__("price", v))

    for r in data.RENTAL:
        add("alquiler:" + r["id"], "Alquiler (precio por día)", r["name"], r["price"], lambda v, r=r: r.__setitem__("price", v))
    return out


# ------------------------------------------------------------------ textos que llevan el precio escrito
def _min_act(a):
    ps = [o["price"] for o in a.get("options", []) or [] if o.get("price")]
    return min(ps) if ps else a.get("price") or 0


def _rep(s, old, new):
    if not isinstance(s, str) or old == new:
        return s
    return re.sub(r"(?<![\d.,])%d(\s?€)" % old, lambda m: "%d%s" % (new, m.group(1)), s)


def _retocar_textos(antes_act, antes_cur):
    for a in data.ACTIVITIES:
        old, new = antes_act[a["slug"]], _min_act(a)
        if old and new and old != new:
            for k in ("seo_title", "seo_desc"):
                if k in a:
                    a[k] = _rep(a[k], old, new)
    for c in data.COURSES:
        if c.get("niveles"):
            c["price"] = min(n["price"] for n in c["niveles"])
        old, new = antes_cur[c["slug"]], c["price"]
        if old != new:
            for k in ("seo_title", "seo_desc"):
                c[k] = _rep(c.get(k), old, new)
            c["ficha"] = [(x, _rep(y, old, new)) for x, y in c.get("ficha", [])]


# ------------------------------------------------------------------ lectura de la hoja
def _leer_csv():
    local = os.environ.get("PRECIOS_CSV")
    if local:
        return open(local, encoding="utf-8").read()
    req = urllib.request.Request(_url(), headers={"User-Agent": "guiasadastra-build"})
    raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    if raw.lstrip().startswith("<"):
        raise RuntimeError("la hoja no es pública (Google devolvió una página web en vez de datos)")
    return raw


def _num(txt):
    t = (txt or "").replace("€", "").replace(" ", "").strip()
    if not t:
        return None
    t = re.sub(r"[.,]0+$", "", t)
    if not re.fullmatch(r"\d{1,4}", t):
        return False
    v = int(t)
    return v if 1 <= v <= 5000 else False


def leer_hoja():
    """Devuelve {id: texto del precio} desde la hoja."""
    texto = _leer_csv()
    rows = list(csv.reader(io.StringIO(texto)))
    if not rows:
        raise RuntimeError("la hoja está vacía")
    cab = [h.strip().lower() for h in rows[0]]
    try:
        i_id = next(i for i, h in enumerate(cab) if h == "id")
        i_p = next(i for i, h in enumerate(cab) if h.startswith("precio"))
    except StopIteration:
        raise RuntimeError("no encuentro las columnas «ID» y «Precio» en la pestaña %s" % SHEET_TAB)
    return {r[i_id].strip(): (r[i_p] if len(r) > i_p else "") for r in rows[1:] if len(r) > i_id and r[i_id].strip()}


def aplicar():
    if os.environ.get("PRECIOS_OFF") or (not SHEET_ID and not os.environ.get("PRECIOS_CSV")):
        print("Precios: uso los de data.py (hoja desactivada)")
        return
    try:
        hoja = leer_hoja()
    except Exception as ex:
        msg = "Precios: no he podido leer la hoja de Google (%s)" % ex
        if os.environ.get("PRECIOS_ESTRICTO"):
            print("::error::" + msg + ". No se publica nada; la web sigue con los últimos precios.")
            sys.exit(1)
        print(("::warning::" if os.environ.get("CI") else "") + msg + ". Uso los precios de data.py.")
        return
    antes_act = {a["slug"]: _min_act(a) for a in data.ACTIVITIES}
    antes_cur = {c["slug"]: c["price"] for c in data.COURSES}
    avisos = []
    inventario = filas()
    for pid, sec, concepto, precio, setters in inventario:
        if pid not in hoja:
            continue
        v = _num(hoja[pid])
        if v is None:
            continue
        if v is False:
            avisos.append("«%s»: «%s» no es un precio válido, se queda en %d €" % (concepto, hoja[pid], precio))
            continue
        if v != precio:
            CAMBIOS.append((concepto, precio, v))
            for s in setters:
                s(v)
    _retocar_textos(antes_act, antes_cur)
    conocidos = {f[0] for f in inventario}
    for pid in hoja:
        if pid not in conocidos:
            avisos.append("fila con ID desconocido «%s» (ignorada)" % pid)
    print("Precios: hoja leída, %d cambios respecto a data.py" % len(CAMBIOS))
    for c, a, n in CAMBIOS:
        print("  %s: %d € -> %d €" % (c, a, n))
    for w in avisos:
        print(("::warning::" if os.environ.get("CI") else "  AVISO ") + "Precios: " + w)


# ------------------------------------------------------------------ ayudas para build.py
def desde_alquiler():
    return min(r["price"] for r in data.RENTAL)


def desde_cat(cat):
    ps = [_min_act(a) for a in data.ACTIVITIES if a.get("cat") == cat and _min_act(a)]
    return min(ps) if ps else 0


def desde_slug(slug):
    for a in data.ACTIVITIES:
        if a["slug"] == slug:
            if a.get("groups"):
                return min(r[3] for _, rows in a["groups"] for r in rows)
            return _min_act(a)
    return 0


if __name__ == "__main__" and sys.argv[1:] == ["csv"]:
    w = csv.writer(sys.stdout)
    w.writerow(["ID", "Sección", "Concepto", "Precio (€)"])
    for pid, sec, concepto, precio, _ in filas():
        w.writerow([pid, sec, concepto, precio])
