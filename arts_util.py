"""Piezas HTML comunes para los artículos de montaña (arts_a.py, arts_b.py)."""


def seccion(eyebrow, h2, inner, alt=False, id_=""):
    return '<section class="section%s"%s><div class="wrap"><p class="eyebrow">%s</p><h2>%s</h2>%s</div></section>' % (
        " alt" if alt else "", ' id="%s"' % id_ if id_ else "", eyebrow, h2, inner)


def tabla(cab, filas):
    return ('<div class="gd-tw"><table class="gd-t"><thead><tr>' + "".join("<th>%s</th>" % c for c in cab) + "</tr></thead><tbody>" +
            "".join("<tr>" + "".join(("<th>%s</th>" if i == 0 else "<td>%s</td>") % c for i, c in enumerate(f)) + "</tr>" for f in filas) + "</tbody></table></div>")


def tarjetas(items):
    """items: [(color, título, texto)]"""
    return '<div class="gd-capas">' + "".join('<article style="--c:%s"><h3>%s</h3><p>%s</p></article>' % x for x in items) + "</div>"


def escala(items):
    """items: [(color, valor, nombre, texto)]"""
    return '<div class="gd-escala uv-esc">' + "".join('<div style="--c:%s"><span>%s</span><b>%s</b><p>%s</p></div>' % x for x in items) + "</div>"


def reglas(items):
    return '<ul class="gd-reglas">' + "".join("<li>%s</li>" % x for x in items) + "</ul>"


def dos(t1, h1, t2, h2):
    return '<div class="gd-dos" style="margin-top:22px"><div><h3>%s</h3>%s</div><div><h3>%s</h3>%s</div></div>' % (t1, h1, t2, h2)


def p(txt):
    return '<p class="lead-p">%s</p>' % txt


def aviso(txt):
    return '<div class="panel" style="margin-top:20px;border-left:5px solid #e8574a"><p style="margin:0">%s</p></div>' % txt


import json as _json, os as _os
_CRED = _json.load(open(_os.path.join(_os.path.dirname(__file__), "tools", "fotos", "creditos.json")))


def _credito(n):
    c = _CRED[n]
    lic = ('<a href="%s" target="_blank" rel="noopener">%s</a>' % (c["licencia_url"], c["licencia"])) if c.get("licencia_url") else c["licencia"]
    return 'Foto: <a href="%s" target="_blank" rel="noopener">%s</a> · %s · Wikimedia Commons' % (c["pagina"], c["autor"], lic)


def foto(n, pie, alt=None):
    """Foto libre de Wikimedia Commons (static/img/fotos/<n>.webp) con su pie y su crédito."""
    c = _CRED[n]
    return ('<figure class="gd-foto"><img src="/img/fotos/%s.webp" alt="%s" width="%d" height="%d" loading="lazy" decoding="async">'
            '<figcaption>%s<small>%s</small></figcaption></figure>') % (n, alt or pie, c["w"], c["h"], pie, _credito(n))


def fotos(*items):
    """Varias fotos en fila: fotos(("nombre", "pie"), ...)"""
    return '<div class="gd-fotos">' + "".join(foto(*i) for i in items) + "</div>"


def ilustracion(src, alt, pie):
    return '<figure class="gd-foto gd-ilu"><img src="%s" alt="%s" loading="lazy" decoding="async"><figcaption>%s</figcaption></figure>' % (src, alt, pie)


def blog(titulo, enlaces):
    """Recuadro con enlaces a crónicas del blog de Jairo: enlaces = [(url, texto)]"""
    return ('<div class="panel gd-blog" style="margin-top:18px;border-left:5px solid var(--gold,#e9a53b)"><p class="eyebrow" style="margin:0 0 6px">%s</p><ul class="gd-links" style="margin:0">' % titulo +
            "".join('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % u for u in enlaces) + "</ul></div>")
