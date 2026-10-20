# -*- coding: utf-8 -*-
"""Genera la web estática de Guías Ad Astra en ./dist  ->  python3 build.py"""
import json, os, shutil, html, datetime
from data import *

BASE = os.environ.get("BASE", "").rstrip("/")  # p. ej. BASE=/NUEVA para publicar en una subcarpeta
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist" + (("-" + BASE.strip("/")) if BASE else ""))
D = SITE["domain"]
TODAY = datetime.date.today().isoformat()
PAGES = []  # (path, priority) para el sitemap
import hashlib
_ST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
VER = {a: hashlib.md5(open(os.path.join(_ST, a), "rb").read()).hexdigest()[:8] for a in ("css/estilos.css", "js/app.js", "js/calculadora.js", "config.js")}

def e(s):
    return html.escape(str(s), quote=True)

def url(path):
    return D + path

WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.4-2.3-1.4-.8-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.3 2.4 1 2.9.8 3.4.7.5-.1 1.7-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4C2.7 15.6 2.2 13.8 2.2 12 2.2 6.6 6.6 2.2 12 2.2S21.8 6.6 21.8 12 17.4 21.8 12 21.8zM12 0C5.4 0 0 5.4 0 12c0 2.1.6 4.2 1.6 6L0 24l6.2-1.6c1.7 1 3.7 1.5 5.8 1.5 6.6 0 12-5.4 12-12S18.6 0 12 0z"/></svg>'
CHEV = '<svg class="chev" viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" stroke="currentColor" stroke-width="1.6" fill="none"/></svg>'

ORG = {
    "@type": ["LocalBusiness", "SportsActivityLocation"], "@id": D + "/#empresa",
    "name": SITE["name"], "alternateName": "Ad Astra Montaña y Aventura", "url": D + "/",
    "logo": SITE["og_image"], "image": HERO, "telephone": SITE["phone_intl"], "email": SITE["email"],
    "priceRange": "15€ - 800€",
    "address": {"@type": "PostalAddress", "addressLocality": "Fuentes de Béjar", "addressRegion": "Salamanca", "postalCode": "37796", "addressCountry": "ES"},
    "areaServed": ["Ávila", "Salamanca", "Cáceres", "León", "Palencia", "Segovia", "Burgos", "Valladolid", "Madrid", "Sierra de Gredos", "Castilla y León"],
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"}],
    "sameAs": [SITE["instagram"], SITE["facebook"]],
    "founder": {"@type": "Person", "name": "Jairo Hernández"},
}

def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(items)]}

def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

NAV_ACT = [("Todas las actividades", "/actividades/"), ("Barranquismo", "/actividades/?categoria=Barranquismo"), ("Vías ferratas", "/actividades/?categoria=Vías ferratas"),
           ("Alpinismo y ascensiones", "/actividades/?categoria=Ascensiones"), ("Espeleología", "/actividades/?categoria=Espeleología"), ("Escalada y boulder", "/actividades/?categoria=Escalada"),
           ("Senderismo", "/actividades/?categoria=Senderismo"), ("Travesías y viajes", "/actividades/?categoria=Viajes")]
NAV_CUR = [("Todos los cursos", "/formacion-cursos/")] + [(c["disc_label"], "/actividades/%s/" % c["slug"]) for c in COURSES]
NAV_OTR = [("Calculadora de rutas", "/calculadora-rutas/"), ("Organización de eventos", "/actividades/organizacion-eventos-deportivos/"), ("Gredos Limpio", "/actividades/gredos-limpio/"),
           ("Oeste de Gredos", "/actividades/comarca-natural-oeste-de-gredos/"), ("Vía Verde Ruta de la Plata", "/actividades/via-verde-ruta-de-la-plata/")]

def dd(label, items, key, active):
    links = "".join('<a href="%s">%s</a>' % (e(h), e(n)) for n, h in items)
    cur = ' style="color:var(--gold)"' if active == key else ""
    return '<div class="dd"><button type="button" aria-expanded="false"%s>%s %s</button><div class="dd-menu">%s</div></div>' % (cur, label, CHEV, links)

def header(active=""):
    def a(h, n, k):
        return '<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if active == k else "", n)
    return ('<header class="site-header"><div class="wrap"><a class="brand" href="/" aria-label="Guías Ad Astra, inicio">AD ASTRA <small>Montaña y aventura</small></a>'
            '<button class="menu-toggle" aria-expanded="false" aria-controls="nav" aria-label="Abrir menú">☰</button>'
            '<nav class="nav" id="nav" aria-label="Principal">' + a("/", "Inicio", "inicio") +
            dd("Actividades", NAV_ACT, "act", active) + dd("Formación–Cursos", NAV_CUR, "cur", active) +
            a("/actividades/alquiler-material-montana/", "Alquiler", "alq") + a("/calendario/", "Calendario", "cal") + dd("Otros", NAV_OTR, "otr", active) +
            a("/sobre-nosotros/", "Nosotros", "nos") + a("/contacto/", "Contacto", "con") +
            '<a class="btn btn-primary" href="/calendario/">Reservar</a></nav></div></header>')

def footer():
    acts = "".join('<li><a href="/actividades/%s/">%s</a></li>' % (a["slug"], e(a["title"])) for a in ACTIVITIES if a["cat"] in ("Barranquismo", "Vías ferratas", "Escalada"))[:2000]
    return ('<footer class="site-footer"><div class="wrap"><div class="foot-grid">'
            '<div><a class="brand" href="/">AD ASTRA</a><p style="margin-top:14px;max-width:34ch">«Hacia las estrellas». Guías de montaña y aventura en Gredos, Castilla y León y el mundo.</p>'
            '<p style="margin-top:14px"><a href="%s" rel="noopener" target="_blank">Instagram</a> · <a href="%s" rel="noopener" target="_blank">Facebook</a></p></div>' % (SITE["instagram"], SITE["facebook"]) +
            '<div><h4>Contacto</h4><ul><li><a href="tel:%s">%s</a></li><li><a href="mailto:%s">%s</a></li><li><a href="https://wa.me/%s" target="_blank" rel="noopener">WhatsApp</a></li><li>%s</li></ul></div>' % (SITE["phone_intl"], SITE["phone"], SITE["email"], SITE["email"], SITE["wa"], SITE["hours"]) +
            '<div><h4>Bases</h4><ul>%s</ul></div>' % "".join("<li>%s</li>" % b for b in SITE["bases"]) +
            '<div><h4>Más visitado</h4><ul><li><a href="/actividades/alquiler-material-montana/">Alquiler de material</a></li><li><a href="/calendario/">Calendario de cursos</a></li><li><a href="/actividades/boulder-zona-centro-salamanca-caceres/">Boulder en Salamanca</a></li><li><a href="/actividades/boulder-las-tuerces/">Boulder en Las Tuerces</a></li><li><a href="/actividades/barranquismo-avila/">Barranquismo en Gredos</a></li></ul></div>'
            '</div><div class="copy"><span>© %d Guías Ad Astra · Montaña y Aventura</span><span>Empresa de turismo activo · Castilla y León</span></div></div></footer>'
            '<a class="wa-float" href="https://wa.me/%s" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">%s</a>' % (datetime.date.today().year, SITE["wa"], WA_SVG))

def page(path, title, desc, body, active="", ld=None, og_type="website", image=None, priority="0.7", noindex=False, head="", scripts=""):
    ld = ld or []
    image = image or SITE["og_image"]
    lds = "".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)
    doc = ('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
           '<title>%s</title><meta name="description" content="%s">' % (e(title), e(desc)) +
           ('<meta name="robots" content="noindex">' if (noindex or BASE) else '<meta name="robots" content="index,follow,max-image-preview:large">') +
           '<link rel="canonical" href="%s">' % url(path) +
           '<meta property="og:type" content="%s"><meta property="og:site_name" content="Guías Ad Astra"><meta property="og:locale" content="es_ES">' % og_type +
           '<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s"><meta property="og:image" content="%s">' % (e(title), e(desc), url(path), e(image)) +
           '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="%s"><meta name="twitter:description" content="%s"><meta name="twitter:image" content="%s">' % (e(title), e(desc), e(image)) +
           '<meta name="theme-color" content="#160d09"><meta name="geo.region" content="ES-CL"><meta name="geo.placename" content="Sierra de Gredos, Castilla y León">'
           '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600&family=Barlow:wght@400;500;600&family=Bebas+Neue&display=swap">'
           '<link rel="stylesheet" href="/css/estilos.css"><link rel="icon" href="/favicon.svg" type="image/svg+xml">' + head + lds +
           '</head><body>' + header(active) + '<main id="contenido">' + body + '</main>' + footer() +
           '<script src="/config.js"></script><script src="/js/app.js" defer></script>' + scripts + '</body></html>')
    for asset in ("css/estilos.css", "js/app.js", "js/calculadora.js", "config.js"):
        doc = doc.replace('"/%s"' % asset, '"/%s?v=%s"' % (asset, VER.get(asset, "1")))
    if BASE:
        doc = doc.replace('href="/', 'href="%s/' % BASE).replace('src="/', 'src="%s/' % BASE)
    out = os.path.join(OUT, path.strip("/"), "index.html") if path != "/404" else os.path.join(OUT, "404.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)
    if not noindex:
        PAGES.append((path, priority))

# ---------------------------------------------------------------- piezas
def hero(eyebrow, h1, lead, img_src, crumbs=None, actions="", cls=""):
    cr = ""
    if crumbs:
        parts = []
        for n, p in crumbs:
            parts.append('<a href="%s">%s</a>' % (p, e(n)) if p else "<span>%s</span>" % e(n))
        cr = '<nav class="crumbs" aria-label="Migas de pan">' + '<span aria-hidden="true">/</span>'.join(parts) + "</nav>"
    return ('<section class="hero %s"><img class="bg" src="%s" alt="%s" fetchpriority="high"><div class="wrap">%s<p class="eyebrow">%s</p><h1>%s</h1>%s%s</div></section>'
            % (cls, e(img_src), e(h1), cr, e(eyebrow), h1, '<p class="lead">%s</p>' % lead if lead else "", '<div class="actions">%s</div>' % actions if actions else ""))

def keybar(items):
    return '<section class="keybar"><dl class="wrap">%s</dl></section>' % "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (e(k), e(v)) for k, v in items)

def ticks(items, cls=""):
    return '<ul class="ticks %s">%s</ul>' % (cls, "".join("<li>%s</li>" % e(i) for i in items))

def block(title, inner, eyebrow=""):
    return '<section class="block"><div class="block-title"><h2>%s</h2></div>%s</section>' % (e(title), inner)

def prose(pars):
    return '<div class="prose">%s</div>' % "".join("<p>%s</p>" % e(p) for p in pars)

def price_str(n):
    return ("%d €" % n) if n else "Consultar"

def card(href, img_src, tag, title, desc, price, attrs=""):
    p = '<span class="price"><small>desde</small>%d€</span>' % price if price else '<span class="price" style="font-size:1.3rem">Consultar</span>'
    return ('<a class="card" href="%s" %s><div class="ph"><img src="%s" alt="%s" loading="lazy"></div><div class="body"><span class="tag">%s</span><h3>%s</h3><p>%s</p>'
            '<div class="foot">%s<span class="tag" style="color:var(--muted)">Ver más →</span></div></div></a>' % (href, attrs, e(img_src), e(title), e(tag), e(title), e(desc), p))

def stepper(id_, val=2, mn=1, mx=40, label="Personas"):
    return ('<div class="field"><span class="label" id="%s-l">%s</span><div class="stepper" role="group" aria-labelledby="%s-l"><button type="button" data-step="-1" aria-label="Menos">−</button>'
            '<input id="%s" type="number" min="%d" max="%d" value="%d" inputmode="numeric"><button type="button" data-step="1" aria-label="Más">+</button></div></div>' % (id_, label, id_, id_, mn, mx, val))

def book_form(title, options=None, base_price=0, date=True, heading="Reserva por WhatsApp", note="Te contestamos por WhatsApp para confirmar disponibilidad, punto de encuentro y pago.", opt_label="Opción", full=True, curso=False):
    sel = ""
    if options:
        sel = '<div class="field"><label for="b-opt">%s</label><select id="b-opt" name="opcion">%s</select></div>' % (opt_label, "".join(
            '<option value="%s" data-price="%s">%s%s</option>' % (e(o["name"]), o.get("price") or "", e(o["name"]), (" · %d €" % o["price"]) if o.get("price") else "") for o in options))
    dt = ('<div class="row2"><div class="field"><label for="b-fecha">Día</label><input id="b-fecha" name="fecha" type="date" required></div>'
          '<div class="field"><label for="b-fecha2">Otro día posible</label><input id="b-fecha2" name="fecha2" type="date"></div></div>') if date else ""
    who = ('<div class="row2"><div class="field"><label for="b-nombre">Nombre</label><input id="b-nombre" name="nombre" autocomplete="given-name"></div>'
           '<div class="field"><label for="b-ape">Apellidos</label><input id="b-ape" name="apellidos" autocomplete="family-name"></div></div>'
           '<div class="field"><label for="b-email">Correo electrónico</label><input id="b-email" name="email" type="email" autocomplete="email" inputmode="email"></div>'
           '<div class="field"><label for="b-tel">Teléfono</label><input id="b-tel" name="telefono" type="tel" autocomplete="tel" inputmode="tel"></div>') if full else \
          '<div class="field"><label for="b-nombre">Nombre</label><input id="b-nombre" name="nombre" autocomplete="name"></div>'
    return ('<form class="book" data-book%s data-title="%s" data-price="%s" id="reservar" novalidate><p class="eyebrow">Reserva</p><h2>%s</h2>%s%s%s%s'
            '<div class="field"><label for="b-com">Comentarios (opcional)</label><textarea id="b-com" placeholder="Edades, nivel, si necesitas alquilar material…"></textarea></div>'
            '<div class="total"><span class="label">Total estimado</span><strong data-total></strong></div><p class="err" role="alert"></p>'
            '<button class="btn btn-wa btn-block" type="submit">%s Enviar por WhatsApp</button><p class="hint">%s</p></form>'
            % ((" data-full" if full else "") + (" data-curso" if curso else ""), e(title), base_price or "", heading, sel, dt, stepper("b-pers"), who, WA_SVG, note))

def upcoming(slug):
    return ('<section class="panel" data-upcoming="%s" hidden><p class="eyebrow">Próximas fechas</p><h3>Plazas disponibles</h3><div class="upcoming" data-uplist></div>'
            '<a class="small" href="/calendario/">Ver el calendario completo →</a></section>' % slug)

def faq_html(faq):
    return '<div class="faq">%s</div>' % "".join("<details><summary>%s</summary><p>%s</p></details>" % (e(q), e(a)) for q, a in faq)

def extras_block():
    return block("Completa tu experiencia", '<div class="two"><div class="panel quiet"><h3>Alojamiento</h3><p class="muted">Opciones en la zona en pensión completa, media pensión o solo alojamiento.</p></div>'
                 '<div class="panel quiet"><h3>Desayuno o comida</h3><p class="muted">Un desayuno completo antes de empezar o comida en un restaurante al terminar.</p></div>'
                 '<div class="panel quiet"><h3>Combina actividades</h3><p class="muted">Compatible con multiactividad y escalada en roca. Pregúntanos por un pack.</p></div></div>')

def auto_faq(a):
    t = a["title"]; f = []
    prices = [o["price"] for o in a.get("options", []) if o.get("price")] or ([a["price"]] if a.get("price") else [])
    if prices:
        lo, hi = min(prices), max(prices)
        f.append(("¿Cuánto cuesta %s?" % t.lower().replace("en ", "en ", 1) if False else "¿Cuánto cuesta la actividad de %s?" % t.lower(),
                  "El precio es de %d € por persona%s. Incluye guía titulado, seguro y el material técnico." % (lo, "" if lo == hi else " (hasta %d € según el recorrido)" % hi)))
    if a.get("incluye"):
        f.append(("¿Qué incluye el precio?", ", ".join(a["incluye"]) + "."))
    if a.get("traer"):
        f.append(("¿Qué tengo que llevar?", ", ".join(a["traer"]) + "."))
    if a.get("req"):
        f.append(("¿Qué requisitos hay?", " ".join(a["req"])))
    if a.get("epoca"):
        f.append(("¿Cuál es la mejor época?", a["epoca"]))
    f.append(("¿Cómo reservo?", "Elige la opción, el día y el número de personas en el formulario y envíanos la solicitud por WhatsApp. Te confirmamos disponibilidad y punto de encuentro."))
    return f

def related(a, n=3):
    rel = [x for x in ACTIVITIES if x["cat"] == a["cat"] and x["slug"] != a["slug"]][:n]
    if len(rel) < n:
        rel += [x for x in ACTIVITIES if x["cat"] not in (a["cat"], "Otros") and x not in rel][: n - len(rel)]
    return ('<section class="section alt"><div class="wrap"><div class="section-head"><p class="eyebrow">También te puede gustar</p><h2>Más aventuras</h2></div><div class="grid c3">%s</div></div></section>'
            % "".join(card("/actividades/%s/" % x["slug"], x["img"], x["cat"], x["title"], x["short"], min([o["price"] for o in x.get("options", []) if o.get("price")] or [x.get("price", 0)]) or 0) for x in rel))

def options_html(opts):
    out = []
    for o in opts:
        out.append('<article class="option"><div><h3>%s</h3><p class="meta">%s · %s</p></div><span class="price">%d€</span><div class="specs">%s</div><p>%s</p>'
                   '<button type="button" class="btn btn-ghost pick" data-pick="%s">Elegir esta opción</button></article>'
                   % (e(o["name"]), e(o["place"]), e(o["dur"]), o["price"], "".join("<span>%s</span>" % e(s) for s in o["specs"]), e(o["desc"]), e(o["name"])))
    return '<div class="options">%s</div>' % "".join(out)

# ---------------------------------------------------------------- páginas de actividad
def act_ld(a, path, prices):
    ld = [crumbs_ld([("Inicio", "/"), ("Actividades", "/actividades/"), (a["title"], path)])]
    prod = {"@context": "https://schema.org", "@type": "Product", "name": a["title"], "description": a.get("seo_desc", a["short"]), "image": a["img"],
            "brand": {"@type": "Brand", "name": "Guías Ad Astra"}, "category": a["cat"], "url": url(path)}
    if prices:
        prod["offers"] = {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": min(prices), "highPrice": max(prices), "offerCount": len(prices),
                          "availability": "https://schema.org/InStock", "seller": {"@id": D + "/#empresa"}}
        ld.append(prod)
    ld.append({"@context": "https://schema.org", **ORG})
    return ld

def build_activity(a):
    path = "/actividades/%s/" % a["slug"]
    k = a["kind"]
    if k in ("boulder",):
        return build_boulder(a, path)
    if k == "trip":
        return build_trip(a, path)
    if k == "eventos":
        return build_eventos(a, path)
    if k == "gredoslimpio":
        return build_gredos_limpio(a, path)
    if k == "zona":
        return build_zona(a, path)
    crumbs = [("Inicio", "/"), ("Actividades", "/actividades/"), (a["cat"], "/actividades/?categoria=" + a["cat"])]
    opts = a.get("options", [])
    if k == "list":
        opts = [{"name": n, "price": p} for g, rows in a["groups"] for n, _, _, p in rows]
    prices = [o["price"] for o in opts if o.get("price")] or ([a["price"]] if a.get("price") else [])
    durs = [o["dur"] for o in a.get("options", [])]
    kb = [("Precio", "Desde %d € / persona" % min(prices) if prices else "Consultar")]
    if durs:
        kb.append(("Duración", durs[0] if len(set(durs)) == 1 else "%s a %s" % (durs[0], durs[-1])))
    if a.get("epoca"):
        kb.append(("Temporada", a["epoca"].split(",")[0].split(":")[-1].strip().rstrip(".")[:40] if len(a["epoca"]) > 40 else a["epoca"].rstrip(".")))
    kb.append(("Incluye", "Guía titulado, material y seguro"))
    if k == "senderismo":
        kb = [(x, y) for x, y in a["ficha"]] + [("Precio", "Desde 15 € / persona")]
    left = []
    intro = []
    if a.get("intro"):
        intro.append(prose(a["intro"]))
    if a.get("que_es"):
        intro.append('<div class="prose"><h3 style="color:var(--fg)">%s</h3>%s</div>' % (e(a["que_es"][0]), "".join("<p>%s</p>" % e(p) for p in a["que_es"][1])))
    if a.get("req"):
        intro.append('<div><h3 style="margin-bottom:14px">Requisitos</h3>%s</div>' % ticks(a["req"]))
    if intro:
        left.append(block("La actividad", '<div style="display:grid;gap:28px">%s</div>' % "".join(intro)))
    if k in ("options", "senderismo"):
        left.append(block("Elige tu opción", options_html(opts)))
    if k == "senderismo":
        left.append(block("Rutas destacadas", '<div class="two">%s</div>' % "".join('<div class="panel"><h3>%s</h3><p class="muted">%s</p></div>' % (e(n), e(d)) for n, d in a["itinerarios"])))
    if k == "list":
        groups = []
        for g, rows in a["groups"]:
            trs = "".join('<tr><td>%s</td><td class="hide-s muted">%s</td><td class="hide-s muted">%s</td><td class="p">%d€</td><td><button type="button" class="btn btn-ghost" style="padding:.6em .9em" data-pick="%s">Elegir</button></td></tr>'
                          % (e(n), e(pl), e(du or "—"), p, e(n)) for n, pl, du, p in rows)
            groups.append('<div style="display:grid;gap:12px"><h3>%s</h3><div class="tablewrap"><table class="peaks"><thead><tr><th>Cumbre</th><th class="hide-s">Zona</th><th class="hide-s">Duración</th><th class="p">Precio</th><th><span class="sr">Reservar</span></th></tr></thead><tbody>%s</tbody></table></div></div>' % (e(g), trs))
        left.append(block("Elige tu cumbre", '<p class="hint">%s</p>%s' % (e(a.get("price_note", "")), '<div style="display:grid;gap:36px">%s</div>' % "".join(groups))))
    if a.get("incluye") or a.get("traer"):
        inner = '<div class="two">'
        if a.get("incluye"):
            inner += '<div class="panel"><h3>Nosotros ponemos</h3>%s</div>' % ticks(a["incluye"])
        if a.get("noincluye"):
            inner += '<div class="panel"><h3>No incluye</h3>%s</div>' % ticks(a["noincluye"], "cross")
        if a.get("traer"):
            inner += '<div class="panel"><h3>Tienes que traer</h3>%s</div>' % ticks(a["traer"])
        left.append(block("Qué incluye", inner + "</div>"))
    if a.get("epoca"):
        left.append(block("Mejor época", prose([a["epoca"]])))
    if a.get("packs"):
        left.append(block("Packs de aventura", '<div class="two">%s</div>' % "".join(
            '<div class="panel"><div style="display:flex;justify-content:space-between;gap:12px;align-items:baseline"><h3>%s</h3><span class="price">+%d€</span></div><p class="muted">%s</p></div>' % (e(n), p, e(d)) for n, d, p in a["packs"])))
    faq = auto_faq(a) if k != "list" else [("¿Cuánto cuesta una ascensión guiada?", "Desde 20 € por persona según la cumbre y el tamaño del grupo. Elige la cumbre en la tabla y te enviamos el precio exacto."), ("¿Puedo proponer otra montaña?", "Sí. Escríbenos con la cumbre que te apetece y la fecha y preparamos la ascensión."), ("¿Qué incluye?", "Guía de montaña titulado y seguro. En ascensiones invernales también te asesoramos sobre material, que puedes alquilarnos.")]
    left.append(block("Preguntas frecuentes", faq_html(faq)))
    form = book_form(a["title"], opts if opts else None, a.get("price", 0), opt_label="Cumbre" if k == "list" else ("Nivel" if k == "senderismo" else "Opción"))
    right = '<div class="sticky" style="display:grid;gap:18px">%s%s</div>' % (upcoming(a["slug"]), form)
    body = (hero(a["cat"], e(a["title"]), e(a.get("lead", a["short"])), a["img"], crumbs, '<a class="btn btn-primary" href="#reservar">Reservar</a>') + keybar(kb) +
            '<section class="section"><div class="wrap split"><div class="stack" style="gap:0">%s</div>%s</div></section>' % ("".join(left), right) + related(a))
    ld = act_ld(a, path, prices) + [faq_ld(faq)]
    page(path, a.get("seo_title", a["title"] + " | Guías Ad Astra"), a.get("seo_desc", a["short"]), body, "act", ld, "product", a["img"], "0.8")

def build_trip(a, path):
    crumbs = [("Inicio", "/"), ("Actividades", "/actividades/"), (a["cat"], "/actividades/?categoria=" + a["cat"])]
    left = [block("El viaje", prose(a["intro"]))]
    if a.get("etapas"):
        left.append(block("Etapas día a día", '<ol class="stages">%s</ol>' % "".join('<li><span class="d">%s</span><h4>%s</h4><p>%s</p></li>' % (e(d), e(t), e(s)) for d, t, s in a["etapas"])))
    left.append(block("Requisitos", ticks(a["req"])))
    left.append(block("Material necesario", ticks(a["material"], "cols")))
    left.append(block("Qué incluye", '<div class="two"><div class="panel"><h3>Incluye</h3>%s</div><div class="panel"><h3>No incluye</h3>%s</div></div>' % (ticks(a["incluye"]), ticks(a["noincluye"], "cross"))))
    fechas = dict(a["ficha"]).get("Fechas", "")
    form = book_form("%s (%s)" % (a["title"], fechas), None, a["price"], date=False, heading="Reserva tu plaza", note="Plazas limitadas. Te enviamos el dossier completo y las condiciones de pago por WhatsApp.")
    body = (hero(a["cat"], e(a["title"]), e(a["short"]), a["img"], crumbs, '<a class="btn btn-primary" href="#reservar">Reservar plaza</a>') +
            '<section class="section tight"><div class="wrap"><dl class="ficha">%s</dl></div></section>' % "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (e(k), e(v)) for k, v in a["ficha"]) +
            '<section class="section" style="padding-top:0"><div class="wrap split"><div class="stack" style="gap:0">%s</div><div class="sticky" style="display:grid;gap:18px">%s%s</div></div></section>' % ("".join(left), upcoming(a["slug"]), form) + related(a))
    ld = [crumbs_ld([("Inicio", "/"), ("Actividades", "/actividades/"), (a["title"], path)]),
          {"@context": "https://schema.org", "@type": "TouristTrip", "name": a["title"], "description": a["seo_desc"], "image": a["img"], "url": url(path),
           "provider": {"@id": D + "/#empresa"}, "offers": {"@type": "Offer", "price": a["price"], "priceCurrency": "EUR", "availability": "https://schema.org/LimitedAvailability"},
           "itinerary": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t} for i, (_, t, _) in enumerate(a.get("etapas", []))]}},
          {"@context": "https://schema.org", **ORG}]
    page(path, a["seo_title"], a["seo_desc"], body, "act", ld, "product", a["img"], "0.7")

def build_boulder(a, path):
    crumbs = [("Inicio", "/"), ("Actividades", "/actividades/"), ("Escalada", "/actividades/?categoria=Escalada")]
    left = [block("Sobre la zona", prose(a["texto"]))]
    if a.get("sectores"):
        left.append(block("Sectores de boulder", '<div class="two">%s</div>' % "".join(
            '<div class="panel"><span class="tag">%s</span><h3>%s</h3><p class="muted">%s</p></div>' % (e(z), e(n), e(d)) for n, z, d in a["sectores"])))
    mapa = ('<iframe class="map" src="%s" loading="lazy" title="Mapa de sectores de %s" referrerpolicy="no-referrer-when-downgrade"></iframe>'
            '<div style="display:flex;flex-wrap:wrap;gap:12px"><a class="btn btn-ghost" href="%s" target="_blank" rel="noopener">Abrir en Google Maps</a>%s</div>'
            % (e(a["map_embed"]), e(a["title"]), e(a["map_link"]), ('<a class="btn btn-ghost" href="%s" target="_blank" rel="noopener">%s</a>' % (e(a["pdf"]), e(a["pdf_label"]))) if a.get("pdf") else ""))
    left.append(block("Mapa de sectores", '<div style="display:grid;gap:16px">%s</div>' % mapa))
    left.append(block("Cómo es el boulder", '<div class="two"><div class="panel"><h3>Material</h3>%s</div><div class="panel"><h3>Buenas prácticas</h3>%s</div></div>' % (
        ticks(["Pies de gato", "Magnesio y cepillo", "Crash pad (colchoneta)", "Ropa cómoda y agua"]),
        ticks(["Aparca en los lugares habilitados", "Limpia el magnesio de las presas", "No dejes residuos ni marcas", "Respeta la fauna y la vegetación"]))))
    left.append(block("Salidas guiadas de boulder", prose(["¿Primera vez? Te llevamos a los mejores bloques de tu nivel con crash pads, te enseñamos a caer y a hacer spotting y te ayudamos a leer los problemas. También hacemos sesiones para grupos y familias."])))
    left.append(block("Preguntas frecuentes", faq_html(a["faq"])))
    form = book_form("Salida guiada de boulder · " + a["title"], None, 0, heading="Pide tu salida guiada", note="Precio según grupo y duración. Te respondemos por WhatsApp con la propuesta.")
    body = (hero("Escalada · Boulder", e(a["h1"]), e(a["lead"]), a["img"], crumbs, '<a class="btn btn-primary" href="#mapa">Ver mapa de sectores</a><a class="btn btn-ghost" href="#reservar">Salida guiada</a>') + keybar(a["datos"]) +
            '<section class="section" id="mapa"><div class="wrap split"><div class="stack" style="gap:0">%s</div><div class="sticky" style="display:grid;gap:18px">%s%s</div></div></section>' % ("".join(left), upcoming(a["slug"]), form) + related(a))
    ld = [crumbs_ld([("Inicio", "/"), ("Actividades", "/actividades/"), (a["title"], path)]), faq_ld(a["faq"]),
          {"@context": "https://schema.org", "@type": ["TouristAttraction", "Place"], "name": a["h1"], "description": a["seo_desc"], "image": a["img"], "url": url(path),
           "touristType": "Escaladores", "hasMap": a["map_link"], "address": {"@type": "PostalAddress", "addressRegion": a["zona"], "addressCountry": "ES"}},
          {"@context": "https://schema.org", **ORG}]
    page(path, a["seo_title"], a["seo_desc"], body, "act", ld, "article", a["img"], "0.8")

def build_eventos(a, path):
    body = (hero("Otros", e(a["title"]), e(a["short"]), a["img"], [("Inicio", "/"), ("Otros", "")], '<a class="btn btn-wa" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">%s Pide información</a>' % (SITE["wa"], e("Hola, quiero información sobre organización de eventos deportivos."), WA_SVG)) +
            '<section class="section"><div class="wrap stack"><div><div class="section-head"><p class="eyebrow">Qué hacemos</p><h2>Te organizamos o asesoramos</h2><p class="lead">Nos encargamos de la organización y la seguridad de tu prueba, de principio a fin.</p></div><div class="two">%s</div></div>'
            % "".join('<div class="panel"><h3>%s</h3><p class="muted">%s</p></div>' % (e(n), e(d)) for n, d in a["servicios"]) +
            '<div><div class="section-head"><p class="eyebrow">Experiencia</p><h2>Eventos en los que trabajamos</h2></div><div class="evlist">%s</div></div></div></section>'
            % "".join('<article class="evrow" style="grid-template-columns:minmax(0,1fr)"><div class="evinfo"><span class="tag">%s</span><h3>%s</h3><p class="meta">%s</p></div></article>' % (e(z), e(n), e(d)) for n, z, d in a["eventos"]))
    page(path, a["seo_title"], a["seo_desc"], body, "otr", [crumbs_ld([("Inicio", "/"), (a["title"], path)]), {"@context": "https://schema.org", **ORG}], image=a["img"], priority="0.5")

def build_gredos_limpio(a, path):
    prog = [("9:30", "Quedada en la Casa del Parque de Hoyos del Espino. Visita, instrucciones y subida juntos a la Plataforma."), ("10:00", "Comienzo de la limpieza desde la Plataforma de Gredos."), ("14:00", "Regreso a la Plataforma para terminar la jornada todos juntos.")]
    body = (hero("Voluntariado ambiental", "Gredos Limpio", "Cada otoño, antes de que llegue la nieve, limpiamos el Circo de Gredos entre todos los amantes de la sierra. Desde 2013.", a["img"], [("Inicio", "/"), ("Otros", "")],
                 '<a class="btn btn-wa" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">%s Apúntate</a>' % (SITE["wa"], e("Hola, quiero apuntarme a Gredos Limpio."), WA_SVG)) +
            keybar([("Última edición", "XIII · 8 nov 2025"), ("Lugar", "Hoyos del Espino (Ávila)"), ("Inscripción", "Gratuita"), ("Quedada", "9:30 Casa del Parque")]) +
            '<section class="section"><div class="wrap split"><div class="stack" style="gap:0">' +
            block("Qué es", prose(["Gredos Limpio es una concentración para los amantes de Gredos y de la montaña. Intentamos limpiar todo lo posible la sierra antes de que las nieves tapen los residuos del verano.", "Los asistentes se mueven con libertad por las zonas de actuación, aunque siempre intentamos ir en grupos."])) +
            block("Zona de actuación", prose(["Entre la Plataforma de Gredos, el Puerto de Candeleda, Prao Pozas, el Morezón y la Laguna Grande, en el Circo de Gredos (Macizo Central)."])) +
            block("Programa", '<ol class="stages">%s</ol><p class="hint">Horarios aproximados. Quien quiera volver antes o quedarse más puede hacerlo bajo su responsabilidad.</p>' % "".join('<li><span class="d">%s</span><p>%s</p></li>' % (h, e(t)) for h, t in prog)) +
            block("Qué ofrecemos y qué llevar", '<div class="two"><div class="panel"><h3>Te damos</h3>%s</div><div class="panel"><h3>Trae</h3>%s</div></div>' % (
                ticks(["Seguro de accidentes (colaboración de Patrimonio Natural)", "Acceso gratuito a la Plataforma de Gredos", "Visita guiada a la Casa del Parque", "Bolsas de basura y guantes"]),
                ticks(["Ropa de abrigo o impermeable según el tiempo", "Agua", "Algo de comer para durante y después"]))) +
            '</div><div class="sticky">%s</div></div></section>' % upcoming(a["slug"]))
    page(path, a["seo_title"], a["seo_desc"], body, "otr", [crumbs_ld([("Inicio", "/"), (a["title"], path)])], image=a["img"], priority="0.5")

def build_zona(a, path):
    items = [x for x in ACTIVITIES if x["slug"] in a["links"]]
    cards = "".join(card("/actividades/%s/" % x["slug"], x["img"], x["cat"], x["title"], x["short"], min([o["price"] for o in x.get("options", []) if o.get("price")] or [x.get("price", 0)]) or 0) for x in items)
    body = (hero("Zonas", e(a["title"]), e(a["lead"]), a["img"], [("Inicio", "/"), ("Otros", "")]) +
            '<section class="section"><div class="wrap"><div class="section-head"><p class="eyebrow">Actividades en la zona</p><h2>Qué hacer</h2></div><div class="grid c3">%s</div></div></section>' % cards)
    page(path, a["seo_title"], a["seo_desc"], body, "otr", [crumbs_ld([("Inicio", "/"), (a["title"], path)])], image=a["img"], priority="0.5")

# ---------------------------------------------------------------- cursos
def build_course(c):
    path = "/actividades/%s/" % c["slug"]
    crumbs = [("Inicio", "/"), ("Formación y cursos", "/formacion-cursos/"), (c["disc_label"], "/formacion-cursos/?disciplina=" + c["disc"])]
    left = [block("Sobre el curso", '<div style="display:grid;gap:24px">%s<div class="panel" style="border-color:var(--line-2)"><span class="tag">Objetivo</span><p style="font-size:1.08rem">%s</p></div></div>' % (prose(c["intro"]), e(c["objetivo"])))] if c.get("objetivo") else [block("Sobre el curso", prose(c["intro"]))]
    if c.get("niveles"):
        lv = "".join('<article class="option"><div><h3>%s</h3><p class="meta">%s</p></div><span class="price">%d€</span><p>%s</p><div style="grid-column:1/-1">%s</div><button type="button" class="btn btn-ghost pick" data-pick="%s">Reservar este curso</button></article>'
                     % (e(n["name"]), e(n["dur"]), n["price"], e(n["info"]), ticks(n["contenido"], "cols"), e(n["name"])) for n in c["niveles"])
        left.append(block("Elige tu curso", '<div class="options">%s</div>' % lv))
    if c.get("contenido"):
        left.append(block("Contenido", ticks(c["contenido"], "cols")))
    if c.get("requisitos"):
        left.append(block("Requisitos", ticks(c["requisitos"])))
    left.append(block("Qué incluye", '<div class="two"><div class="panel"><h3>Incluye</h3>%s</div><div class="panel"><h3>No incluye</h3>%s</div></div>%s' % (
        ticks(c["incluye"]), ticks(c["noincluye"], "cross"), ('<div class="notice">%s <a href="/actividades/alquiler-material-montana/">Ver alquiler de material</a></div>' % e(c["nota"])) if c.get("nota") else "")))
    left.append(extras_block())
    faq = [("¿Cuánto cuesta el %s?" % c["title"].lower(), "Desde %d € por persona. Incluye %s." % (c["price"], ", ".join(x.lower() for x in c["incluye"]))),
           ("¿Dónde se hace?", dict(c["ficha"]).get("Dónde", "Castilla y León") + "."),
           ("¿Cuándo hay fechas?", "Consulta las próximas convocatorias en esta página o en el calendario. Si ninguna te encaja, pídenos otra fecha para tu grupo."),
           ("¿Cómo reservo plaza?", "Pulsa «Reservar plaza» en una fecha del calendario: tu plaza queda apartada y nos llega tu mensaje por WhatsApp para confirmar.")]
    left.append(block("Preguntas frecuentes", faq_html(faq)))
    opts = [{"name": n["name"], "price": n["price"]} for n in c["niveles"]] if c.get("niveles") else None
    form = book_form(c["title"], opts, c["price"], heading="¿Otra fecha o grupo propio?", note="Para un grupo o una fecha que no está en el calendario. Te respondemos por WhatsApp.", opt_label="Curso", full=True, curso=True)
    body = (hero("Formación · " + c["disc_label"], e(c["title"]), e(c["short"]), c["img"], crumbs, '<a class="btn btn-primary" href="#fechas">Ver fechas y plazas</a>') +
            '<section class="section tight"><div class="wrap"><dl class="ficha">%s</dl></div></section>' % "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (e(k), e(v)) for k, v in c["ficha"]) +
            '<section class="section" style="padding-top:0" id="fechas"><div class="wrap split"><div class="stack" style="gap:0">%s</div><div class="sticky" style="display:grid;gap:18px">%s%s</div></div></section>' % ("".join(left), upcoming(c["slug"]), form))
    ld = [crumbs_ld([("Inicio", "/"), ("Formación y cursos", "/formacion-cursos/"), (c["title"], path)]), faq_ld(faq),
          {"@context": "https://schema.org", "@type": "Course", "name": c["title"], "description": c["seo_desc"], "image": c["img"], "url": url(path), "inLanguage": "es",
           "provider": {"@type": "Organization", "name": "Guías Ad Astra", "sameAs": D + "/"},
           "offers": {"@type": "Offer", "category": "Paid", "price": c["price"], "priceCurrency": "EUR", "availability": "https://schema.org/InStock"},
           "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Onsite", "location": dict(c["ficha"]).get("Dónde", "Castilla y León"),
                                 "courseWorkload": "PT6H" if "6 horas" in str(c["ficha"]) else ("P2D" if "2 días" in str(c["ficha"]) else "PT4H")}}]
    page(path, c["seo_title"], c["seo_desc"], body, "cur", ld, "product", c["img"], "0.8")

# ---------------------------------------------------------------- alquiler
def build_rental():
    path = "/actividades/alquiler-material-montana/"
    cats = ["Barranquismo", "Vías ferratas", "Escalada", "Alpinismo"]
    chips = '<button class="chip" data-val="" aria-pressed="true">Todo</button>' + "".join('<button class="chip" data-val="%s" aria-pressed="false">%s</button>' % (c, c) for c in cats)
    cards = "".join(
        '<article class="card rent-card" data-id="%s" data-name="%s" data-price="%d" data-cat="%s"><div class="ph"><img src="%s" alt="Alquiler de %s para %s" loading="lazy"></div>'
        '<div class="body"><span class="tag">%s</span><h3>%s</h3><p>%s</p><div class="foot"><span class="price">%d€<small style="margin:0 0 0 4px">/día</small></span>'
        '<div class="stepper" role="group" aria-label="Unidades de %s"><button type="button" data-step="-1" aria-label="Quitar una">−</button><input type="number" min="0" max="20" value="0" inputmode="numeric" aria-label="Unidades"><button type="button" data-step="1" aria-label="Añadir una">+</button></div></div></div></article>'
        % (r["id"], e(r["name"]), r["price"], "|".join(r["cats"]), e(r["img"]), e(r["name"].lower()), e(" y ".join(r["cats"]).lower()), e(" · ".join(r["cats"])), e(r["name"]), e(r["desc"]), r["price"], e(r["name"])) for r in RENTAL)
    puntos = "".join('<option>%s</option>' % b for b in RENTAL_PICKUP)
    body = (hero("Alquiler", "Alquiler de material de montaña y barranquismo", "Neoprenos, arneses, cascos, disipadores de ferrata, piolets y crampones. Precio por día con IVA incluido. Recogida en Fuentes de Béjar (Salamanca) o en Valladolid.",
                 img("e3722879-d648-4dbe-b361-b365f07e1692/otros-media-5.webp"), [("Inicio", "/"), ("Alquiler de material", "")], '<a class="btn btn-primary" href="#catalogo">Elegir material</a>') +
            keybar([("Precio", "Por unidad y día"), ("IVA", "Incluido"), ("Recogida", "Fuentes de Béjar · Valladolid"), ("Reserva", "Por WhatsApp en 1 minuto")]) +
            '<section class="section" id="catalogo"><div class="wrap" id="alquiler-app"><div class="section-head"><p class="eyebrow">Catálogo</p><h2>Elige fechas y unidades</h2><p class="muted">Indica el día de recogida y el de devolución, suma las unidades que necesitas y envíanos la solicitud por WhatsApp. Te confirmamos disponibilidad al momento.</p></div>'
            '<div class="datebar"><div class="field"><label for="r-desde">Recogida</label><input id="r-desde" type="date"></div><div class="field"><label for="r-hasta">Devolución</label><input id="r-hasta" type="date"></div>'
            '<div class="field"><span class="label">Días de alquiler</span><span class="days" id="r-dias">—</span></div><div class="field"><label for="r-punto">Recogida en</label><select id="r-punto">%s</select></div></div>'
            '<div class="chips" data-filter="#rgrid" data-key="cat" style="margin-bottom:22px">%s</div><div class="grid c4" id="rgrid">%s</div></div></section>' % (puntos, chips, cards) +
            '<section class="section alt"><div class="wrap"><div class="section-head"><p class="eyebrow">Cómo funciona</p><h2>Alquilar es así de fácil</h2></div><ol class="steps3">'
            '<li><h3>Elige fechas</h3><p>Día de recogida y de devolución. Si es un solo día, deja la devolución igual.</p></li>'
            '<li><h3>Suma unidades</h3><p>Pulsa + en cada artículo. Verás el total estimado abajo.</p></li>'
            '<li><h3>Envía por WhatsApp</h3><p>Te confirmamos disponibilidad, tallas y punto de recogida. Pagas al recoger.</p></li></ol></div></section>'
            '<section class="section"><div class="wrap split"><div class="stack" style="gap:0">' +
            block("Material técnico revisado para cada actividad", prose([
                "Somos guías titulados y usamos este mismo material en nuestras actividades: lo revisamos después de cada uso y lo retiramos cuando toca. Todo está homologado para su uso.",
                "Para barranquismo tenemos neoprenos bipieza de 5 mm, escarpines de 3 mm, arneses específicos con culera y descensor, y el equipo completo para que solo traigas bañador y toalla. Ideal para los barrancos de Gredos, el Valle del Jerte, las Arribes del Duero o León.",
                "Para vías ferratas alquilamos sets disipadores homologados, arneses y cascos: todo lo necesario para la ferrata del Cancho de la Muela en Candelario, las de Burgos o las de León.",
                "Para alpinismo y montaña invernal tenemos piolets de travesía y crampones de 12 puntas de correas, compatibles con cualquier bota. Perfectos para Gredos, Guadarrama o la Montaña Palentina en invierno.",
            ])) +
            block("Condiciones del alquiler", ticks(["Precios por unidad y día, IVA incluido.", "Se paga en el momento de la entrega y se firma un contrato de alquiler.", "El material se devuelve en el mismo lugar de entrega o donde indique la empresa.", "Un retraso en la devolución sin avisar se cobra como un día más de alquiler."])) +
            block("Preguntas frecuentes", faq_html(RENTAL_FAQ)) +
            '</div><div class="sticky"><div class="panel"><p class="eyebrow">Puntos de recogida</p><h3>Dónde recoger</h3>%s<a class="btn btn-wa" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">%s Preguntar por WhatsApp</a></div></div></div></section>'
            % (ticks(RENTAL_PICKUP), SITE["wa"], e("Hola, tengo una duda sobre el alquiler de material."), WA_SVG) +
            '<div class="mbar" hidden><div class="wrap"><div class="sum"><b id="m-total">0 €</b><span id="m-info"></span></div><button class="btn btn-wa" id="m-open" type="button">%s Revisar y enviar</button></div></div>' % WA_SVG +
            '<dialog id="r-dlg"><form class="dlg" id="r-form" novalidate><div class="dlg-head"><div><p class="eyebrow">Tu alquiler</p><h2>Revisa y envía</h2></div><button type="button" class="icon-btn" data-close aria-label="Cerrar">×</button></div>'
            '<p class="muted" id="r-when"></p><ul class="basket-list" id="r-list"></ul><div class="total"><span class="label">Total estimado</span><strong id="r-sum"></strong></div>'
            '<div class="field"><label for="r-nombre">Nombre</label><input id="r-nombre" autocomplete="name"></div>'
            '<div class="field"><label for="r-notas">Tallas o notas (opcional)</label><textarea id="r-notas" placeholder="Ej.: neoprenos talla M y L, altura 1,70 y 1,85"></textarea></div>'
            '<p class="err" id="r-err" role="alert"></p><button class="btn btn-wa btn-block" type="submit">%s Enviar por WhatsApp</button><p class="hint">Es una solicitud: te confirmamos disponibilidad por WhatsApp. Pagas al recoger.</p></form></dialog>' % WA_SVG)
    items_ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Alquiler de material de montaña", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": {"@type": "Product", "name": "Alquiler " + r["name"].lower(), "description": r["desc"], "image": r["img"], "category": "Alquiler de material de " + r["cats"][0].lower(),
                                                       "brand": {"@type": "Brand", "name": "Guías Ad Astra"},
                                                       "offers": {"@type": "Offer", "price": r["price"], "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "businessFunction": "http://purl.org/goodrelations/v1#LeaseOut",
                                                                  "priceSpecification": {"@type": "UnitPriceSpecification", "price": r["price"], "priceCurrency": "EUR", "unitCode": "DAY", "valueAddedTaxIncluded": True}, "seller": {"@id": D + "/#empresa"}}}}
        for i, r in enumerate(RENTAL)]}
    svc = {"@context": "https://schema.org", "@type": "Service", "serviceType": "Alquiler de material de montaña, barranquismo, vías ferratas y alpinismo", "provider": {"@id": D + "/#empresa"},
           "areaServed": ["Salamanca", "Béjar", "Fuentes de Béjar", "Ávila", "Cáceres", "Valladolid", "Zamora", "Segovia"], "url": url(path)}
    ld = [crumbs_ld([("Inicio", "/"), ("Alquiler de material", path)]), items_ld, svc, faq_ld(RENTAL_FAQ), {"@context": "https://schema.org", **ORG}]
    page(path, "Alquiler de material de barranquismo, ferratas y alpinismo | Béjar (Salamanca) y Valladolid",
         "Alquila neopreno de barranquismo, arnés, casco, set de vía ferrata, piolet y crampones desde 4€/día con IVA. Recogida en Fuentes de Béjar (Salamanca) o Valladolid. Reserva por WhatsApp.",
         body, "alq", ld, "website", img("e89d2f67-e4c0-4443-8f1f-9f4f13528f9f/otros-media-6.webp"), "0.9")

# ---------------------------------------------------------------- listados
def min_price(x):
    return min([o["price"] for o in x.get("options", []) if o.get("price")] or [x.get("price", 0)]) or 0

def build_activities_index():
    order = ["Barranquismo", "Vías ferratas", "Ascensiones", "Espeleología", "Escalada", "Senderismo", "Travesías", "Viajes", "Otros"]
    chips = '<button class="chip" data-val="" aria-pressed="true">Todas</button>' + "".join('<button class="chip" data-val="%s" aria-pressed="false">%s</button>' % (c, c) for c in order)
    secs = ""
    for c in order:
        items = [x for x in ACTIVITIES if x["cat"] == c]
        if c == "Otros":
            items = [{"slug": "alquiler-material-montana", "img": img("e3722879-d648-4dbe-b361-b365f07e1692/otros-media-5.webp"), "cat": "Otros", "title": "Alquiler de material", "short": "Neoprenos, arneses, cascos, disipadores, piolets y crampones por días."}] + items
        if not items:
            continue
        secs += '<section class="cat-section"><h2>%s</h2><div class="grid c3">%s</div></section>' % (c, "".join(card("/actividades/%s/" % x["slug"], x["img"], x["cat"], x["title"], x["short"], min_price(x), 'data-cat="%s"' % c) for x in items))
    body = (hero("Actividades", "Elige tu aventura", "Barranquismo, vías ferratas, espeleología, ascensiones, senderismo, escalada y viajes con guías titulados en Gredos, Castilla y León y el mundo.", HERO, [("Inicio", "/"), ("Actividades", "")]) +
            '<section class="section"><div class="wrap"><div class="chips" data-filter="#acts" data-key="cat" data-param="categoria" style="margin-bottom:36px">%s</div><div id="acts">%s</div></div></section>' % (chips, secs))
    ld = [crumbs_ld([("Inicio", "/"), ("Actividades", "/actividades/")]), {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": url("/actividades/%s/" % x["slug"]), "name": x["title"]} for i, x in enumerate(ACTIVITIES)]}]
    page("/actividades/", "Actividades de aventura en Gredos y Castilla y León | Guías Ad Astra", "Barranquismo, vías ferratas, espeleología, ascensiones, senderismo, boulder y viajes en Ávila, Salamanca, Cáceres, León, Palencia, Segovia y Burgos. Reserva por WhatsApp.", body, "act", ld, priority="0.9")

def build_courses_index():
    chips = '<button class="chip" data-val="" aria-pressed="true">Todos</button>' + "".join('<button class="chip" data-val="%s" aria-pressed="false">%s</button>' % (c["disc"], c["disc_label"]) for c in COURSES)
    cards = "".join(card("/actividades/%s/" % c["slug"], c["img"], c["disc_label"], c["title"], c["short"], c["price"], 'data-disc="%s"' % c["disc"]) for c in COURSES)
    body = (hero("Formación", "Formación y cursos de montaña", "Cursos de barranquismo, escalada, autorrescate, alpinismo y ARVA con guías titulados. Grupos reducidos y fechas con plazas en el calendario.", img("0c5376bd-2231-4c62-b798-6f0139e73cd7/cursos-alpinismo.webp"),
                 [("Inicio", "/"), ("Formación y cursos", "")], '<a class="btn btn-primary" href="/calendario/">Ver calendario de cursos</a>') +
            '<section class="section"><div class="wrap"><div class="chips" data-filter="#courses" data-key="disc" data-param="disciplina" style="margin-bottom:30px">%s</div><div class="grid c3" id="courses">%s</div></div></section>' % (chips, cards) +
            '<section class="section alt"><div class="wrap split"><div class="stack" style="gap:0">' +
            block("Por qué formarte con nosotros", prose(["Somos guías de montaña titulados y diseñamos cada curso para que salgas siendo más autónomo y seguro en el monte.", "Trabajamos en grupos pequeños (de 6 a 10 personas según el curso), con material técnico común incluido y un dossier para que repases en casa."])) +
            '</div><div>%s</div></div></section>' % '<div class="panel"><p class="eyebrow">Calendario</p><h3>Fechas con plazas</h3><p class="muted">Consulta las próximas convocatorias y reserva tu plaza en un minuto.</p><a class="btn btn-primary" href="/calendario/">Ver calendario</a></div>')
    ld = [crumbs_ld([("Inicio", "/"), ("Formación y cursos", "/formacion-cursos/")]), {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": url("/actividades/%s/" % c["slug"]), "name": c["title"]} for i, c in enumerate(COURSES)]}]
    page("/formacion-cursos/", "Cursos de montaña: barranquismo, escalada, alpinismo y ARVA | Guías Ad Astra", "Cursos de barranquismo, iniciación a la escalada, autorrescate, alpinismo y ARVA en Castilla y León con guías titulados. Consulta fechas y plazas.", body, "cur", ld, priority="0.9")

def build_calendar():
    body = (hero("Calendario", "Calendario de actividades y cursos", "Fechas confirmadas con plazas limitadas. Reserva tu plaza y te escribimos por WhatsApp para confirmar.", img("41645da1-a007-4ff0-8526-61ca467dddb5/curso-arva.webp"), [("Inicio", "/"), ("Calendario", "")]) +
            '<section class="section"><div class="wrap" data-calendar><div class="cal-top"><div class="chips"><button class="chip" data-tipo-btn="" aria-pressed="true">Todo</button><button class="chip" data-tipo-btn="curso" aria-pressed="false">Cursos</button><button class="chip" data-tipo-btn="actividad" aria-pressed="false">Actividades</button></div>'
            '<div class="cal-nav"><button class="icon-btn" data-prev aria-label="Mes anterior">‹</button><h2 data-mtitle></h2><button class="icon-btn" data-next aria-label="Mes siguiente">›</button></div></div>'
            '<div class="month" data-month></div><div class="legend" style="margin:14px 0 40px"><span><i style="background:#f0b445"></i>Curso</span><span><i style="background:#7fb3a3"></i>Actividad</span><span><i style="background:var(--line-2)"></i>Completo</span></div>'
            '<div class="section-head"><p class="eyebrow">Próximas fechas</p><h2>Reserva tu plaza</h2></div><div class="evlist" data-evlist><div class="empty">Cargando fechas…</div></div></div></section>'
            '<section class="section alt"><div class="wrap two"><div class="panel"><h3>¿No ves tu fecha?</h3><p class="muted">Organizamos cursos y actividades para grupos en el día que elijas.</p><a class="btn btn-wa" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">%s Pedir otra fecha</a></div>'
            '<div class="panel"><h3>Cómo funciona</h3>%s</div></div></section>' % (SITE["wa"], e("Hola, quería consultar fechas para un curso o actividad."), WA_SVG,
                                                                                 ticks(["Elige una fecha con plazas libres.", "Indica cuántas plazas quieres, tu nombre y teléfono.", "Tu plaza queda apartada y se abre WhatsApp para confirmar contigo."])))
    page("/calendario/", "Calendario de cursos y actividades de montaña | Plazas disponibles", "Próximas fechas de cursos de barranquismo, alpinismo, escalada, ARVA y salidas guiadas en Gredos y Castilla y León. Consulta plazas libres y reserva online.", body, "cal",
         [crumbs_ld([("Inicio", "/"), ("Calendario", "/calendario/")])], priority="0.9")

def build_home():
    feat = ["barranquismo-avila", "via-ferrata-salamanca", "barranquismo-cueva-valporquero-sima-de-perlas", "ascensiones-montana", "boulder-zona-centro-salamanca-caceres", "monte-olimpo"]
    cards = "".join(card("/actividades/%s/" % x["slug"], x["img"], x["cat"], x["title"], x["short"], min_price(x)) for s in feat for x in ACTIVITIES if x["slug"] == s)
    ccards = "".join(card("/actividades/%s/" % c["slug"], c["img"], c["disc_label"], c["title"], c["short"], c["price"]) for c in COURSES[:3])
    tick = "".join("%s<em>✦</em>" % t for t in ["Barranquismo", "Vías ferratas", "Escalada", "Espeleología", "Ascensiones", "Trekking", "Cursos", "Viajes"] * 2)
    body = (hero("Hacia las estrellas", "Vive la aventura", "Barrancos, ferratas, cuevas y cumbres con guías titulados en Gredos, Castilla y León y el mundo.", HERO, None,
                 '<a class="btn btn-primary" href="/actividades/">Reserva tu actividad</a><a class="btn btn-ghost" href="/calendario/">Calendario de cursos</a>', "home") +
            '<div class="ticker" aria-hidden="true"><div>%s</div></div>' % tick +
            '<section class="section"><div class="wrap"><div class="section-head row"><div><p class="eyebrow">Actividades destacadas</p><h2>Tu próxima aventura</h2></div><a class="btn btn-ghost" href="/actividades/">Ver todas</a></div><div class="grid c3">%s</div></div></section>' % cards +
            '<section class="section alt"><div class="wrap"><div class="stats"><div><b>+10</b><span>años guiando</span></div><div><b>8</b><span>provincias</span></div><div><b>100%%</b><span>guías titulados</span></div></div></div></section>'
            '<section class="section"><div class="wrap"><div class="section-head row"><div><p class="eyebrow">Formación</p><h2>Cursos de montaña</h2></div><a class="btn btn-ghost" href="/calendario/">Fechas y plazas</a></div><div class="grid c3">%s</div></div></section>' % ccards +
            '<section class="section alt"><div class="wrap about"><img src="%s" alt="Material de alquiler: neopreno de barranquismo" loading="lazy" style="background:#e9e6e2;object-fit:contain"><div style="display:grid;gap:18px"><p class="eyebrow">Alquiler de material</p><h2>Equípate para tu aventura</h2>'
            '<p class="lead">Neoprenos, arneses, cascos, disipadores, piolets y crampones desde 4 € al día. Eliges fechas y unidades y nos lo envías por WhatsApp.</p><div><a class="btn btn-primary" href="/actividades/alquiler-material-montana/">Alquilar material</a></div></div></div></section>' % img("e89d2f67-e4c0-4443-8f1f-9f4f13528f9f/otros-media-6.webp") +
            '<section class="section"><div class="wrap about"><img src="%s" alt="Jairo Hernández, guía de montaña de Guías Ad Astra" loading="lazy"><div style="display:grid;gap:18px"><p class="eyebrow">Quiénes somos</p><h2>Pasión por la montaña desde Gredos</h2>'
            '<p class="lead">Guías Ad Astra («hacia las estrellas», en latín) nace de la pasión de Jairo Hernández por la montaña y todos los deportes que en ella se pueden practicar.</p><div><a class="btn btn-ghost" href="/sobre-nosotros/">Conócenos</a></div></div></div></section>' % JAIRO +
            '<section class="cta-band"><div class="wrap"><h2>Tu próxima cumbre te espera</h2><a class="btn" href="/calendario/">Ver fechas y reservar</a></div></section>')
    ld = [{"@context": "https://schema.org", **ORG}, {"@context": "https://schema.org", "@type": "WebSite", "name": "Guías Ad Astra", "url": D + "/", "inLanguage": "es"}]
    page("/", "Guías Ad Astra | Barranquismo, vías ferratas y montaña en Gredos", "Aventura guiada en Gredos y Castilla y León: barranquismo, vías ferratas, escalada, espeleología, cursos y alquiler de material. Guías titulados. Reserva por WhatsApp.", body, "inicio", ld, priority="1.0")

def build_about():
    body = (hero("Nosotros", "Hacia las estrellas", "Pasión por la montaña desde la Sierra de Gredos.", JAIRO, [("Inicio", "/"), ("Sobre nosotros", "")]) +
            '<section class="section"><div class="wrap about"><img src="%s" alt="Jairo Hernández, fundador de Guías Ad Astra" loading="lazy"><div class="prose" style="font-size:1.1rem">'
            '<p><strong>Guías Ad Astra</strong> («hacia las estrellas», en latín) nace de la pasión de Jairo Hernández por la montaña y por todos los deportes que en ella se pueden practicar.</p>'
            '<p>Diseñamos actividades en todos los ámbitos, adaptadas a cada nivel, para que vivas con nosotros una experiencia única: barrancos, ferratas, cuevas, cumbres, cursos de formación y viajes.</p>'
            '<p>Trabajamos desde tres bases, Fuentes de Béjar (Salamanca), Vallespinoso de Cervera (Palencia) y Valladolid, y guiamos en ocho provincias y fuera de España.</p>'
            '<p>Además organizamos eventos como la Ultra de Gredos y las jornadas de voluntariado Gredos Limpio desde 2013.</p>'
            '<p><a class="btn btn-primary" href="/actividades/">Ver actividades</a></p></div></div></section>' % JAIRO)
    page("/sobre-nosotros/", "Sobre nosotros | Guías Ad Astra, guías de montaña en Gredos", "Jairo Hernández y el equipo de Guías Ad Astra: guías de montaña titulados en Gredos y Castilla y León, con actividades adaptadas a todos los niveles.", body, "nos",
         [crumbs_ld([("Inicio", "/"), ("Sobre nosotros", "/sobre-nosotros/")])], priority="0.5")

def build_contact():
    body = (hero("Contacto", "Hablemos de aventura", "Llámanos o escríbenos por WhatsApp para organizar tu actividad, curso o alquiler.", HERO, [("Inicio", "/"), ("Contacto", "")]) +
            '<section class="section"><div class="wrap contact-grid">'
            '<div class="panel"><p class="eyebrow">WhatsApp</p><b>%s</b><p class="muted">La forma más rápida de reservar.</p><a class="btn btn-wa" href="https://wa.me/%s" target="_blank" rel="noopener">%s Escribir</a></div>' % (SITE["phone"], SITE["wa"], WA_SVG) +
            '<div class="panel"><p class="eyebrow">Teléfono</p><b><a href="tel:%s" style="color:inherit">%s</a></b><p class="muted">%s</p></div>' % (SITE["phone_intl"], SITE["phone"], SITE["hours"]) +
            '<div class="panel"><p class="eyebrow">Email</p><b style="font-size:1.25rem"><a href="mailto:%s" style="color:inherit">%s</a></b></div>' % (SITE["email"], SITE["email"]) +
            '<div class="panel"><p class="eyebrow">Bases</p>%s</div></div></section>' % ticks(SITE["bases"]))
    page("/contacto/", "Contacto y reservas | Guías Ad Astra", "Contacta con Guías Ad Astra: 621 075 048 · WhatsApp · guiasadastra@gmail.com. Bases en Fuentes de Béjar (Salamanca), Vallespinoso de Cervera (Palencia) y Valladolid.", body, "con",
         [crumbs_ld([("Inicio", "/"), ("Contacto", "/contacto/")]), {"@context": "https://schema.org", **ORG}], priority="0.6")

def build_404():
    excusas = [
        "Una cabra montés se ha comido esta página. Es lo que tiene dejarla al sol.",
        "El guía jura que este sendero estaba aquí ayer.",
        "Esta página se fue a hacer el Almanzor y todavía no ha bajado.",
        "Hemos rapelado hasta aquí y resulta que la cuerda no llegaba.",
        "La niebla de Gredos se ha tragado este enlace. Vuelve cuando levante.",
        "Alguien movió el hito de piedras. Siempre hay alguien.",
        "Esta página está en un barranco sin cobertura. Prueba más abajo.",
        "Nos equivocamos de collado. Pasa hasta en las mejores cordadas.",
    ]
    links = [("Barranquismo", "/actividades/?categoria=Barranquismo"), ("Vías ferratas", "/actividades/?categoria=Vías ferratas"),
             ("Cursos", "/formacion-cursos/"), ("Alquiler de material", "/actividades/alquiler-material-montana/"), ("Calendario", "/calendario/"), ("Contacto", "/contacto/")]
    body = ("""<section class="lost"><canvas id="stars" aria-hidden="true"></canvas>
<svg class="ridge" viewBox="0 0 1440 260" preserveAspectRatio="none" aria-hidden="true"><path d="M0 260V170l110-60 70 40 120-110 90 80 60-30 130 120 110-90 80 50 140-130 100 90 70-40 150 120 110-70 100 60V260z" fill="#1f130d"/><path d="M0 260v-40l160-50 120 40 200-70 140 60 180-50 160 50 200-60 140 50 140-30v100z" fill="#160d09"/></svg>
<div class="wrap lost-in">
  <p class="eyebrow">Error 404 · Altitud desconocida</p>
  <div class="num" aria-label="404"><span>4</span>
    <button class="compass" id="compass" type="button" aria-label="Agitar la brújula para otra excusa">
      <svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="54" fill="none" stroke="currentColor" stroke-width="6"/><circle cx="60" cy="60" r="44" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2 6"/>
      <text x="60" y="24" text-anchor="middle">N</text><text x="60" y="106" text-anchor="middle">S</text><text x="102" y="65" text-anchor="middle">E</text><text x="18" y="65" text-anchor="middle">O</text>
      <g id="needle"><path d="M60 18 70 60H50z" fill="#e9a53b"/><path d="M60 102 50 60h20z" fill="#f3e9df"/><circle cx="60" cy="60" r="6" fill="#160d09" stroke="#f3e9df" stroke-width="2"/></g></svg>
    </button><span>4</span></div>
  <h1>Te has perdido en la montaña</h1>
  <p class="lead excuse" id="excuse" aria-live="polite">""" + e(excusas[0]) + """</p>
  <p class="hint">Pulsa la brújula si quieres otra excusa (tenemos muchas).</p>
  <div class="actions"><a class="btn btn-primary" href="/">Volver al campamento base</a><a class="btn btn-ghost" href="https://wa.me/""" + SITE["wa"] + """" target="_blank" rel="noopener">Pedir rescate por WhatsApp</a></div>
  <div class="paths"><span class="label">O sigue uno de estos senderos balizados</span><div class="chips">""" +
        "".join('<a class="chip" href="%s">%s</a>' % (e(h), e(n)) for n, h in links) + """</div></div>
</div></section>
<style>
.lost{position:relative;isolation:isolate;overflow:hidden;min-height:calc(100vh - 68px);display:flex;align-items:center;background:radial-gradient(120% 80% at 70% 0%,#2a1a12 0%,var(--bg) 60%)}
.lost #stars{position:absolute;inset:0;width:100%;height:100%;z-index:-2}
.lost .ridge{position:absolute;left:0;right:0;bottom:0;width:100%;height:32vh;z-index:-1}
.lost-in{display:grid;gap:18px;justify-items:start;padding-block:60px 30vh}
.lost .num{display:flex;align-items:center;gap:clamp(6px,2vw,18px);font-family:var(--display);font-size:clamp(7rem,22vw,15rem);line-height:.85;color:transparent;background:var(--grad);-webkit-background-clip:text;background-clip:text}
.lost .num span{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.compass{width:clamp(5.6rem,17vw,11.5rem);height:clamp(5.6rem,17vw,11.5rem);border:0;background:none;padding:0;color:var(--gold);cursor:pointer;border-radius:50%}
.compass svg{width:100%;height:100%;overflow:visible}
.compass text{font:600 13px var(--label);fill:var(--muted)}
#needle{transform-origin:60px 60px;animation:lost 3.2s ease-in-out infinite}
.compass.spin #needle{animation:spin .9s cubic-bezier(.2,.7,.3,1)}
@keyframes lost{0%{transform:rotate(-35deg)}25%{transform:rotate(50deg)}45%{transform:rotate(10deg)}70%{transform:rotate(140deg)}100%{transform:rotate(-35deg)}}
@keyframes spin{to{transform:rotate(1080deg)}}
.lost h1{font-size:clamp(2.2rem,6vw,4rem)}
.excuse{min-height:3.3em;font-size:1.3rem;color:var(--fg)}
.excuse.pop{animation:pop .4s ease}
@keyframes pop{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.lost .actions{display:flex;flex-wrap:wrap;gap:12px}
.paths{display:grid;gap:12px;margin-top:12px}
.paths .chip{text-decoration:none}
@media (prefers-reduced-motion:reduce){#needle,.compass.spin #needle,.excuse.pop{animation:none}}
</style>
<script>
(function(){
  var ex=""" + json.dumps(excusas, ensure_ascii=False) + """,i=0,c=document.getElementById("compass"),t=document.getElementById("excuse");
  c.addEventListener("click",function(){i=(i+1+Math.floor(Math.random()*(ex.length-1)))%ex.length;c.classList.remove("spin");void c.offsetWidth;c.classList.add("spin");
    t.classList.remove("pop");void t.offsetWidth;t.textContent=ex[i];t.classList.add("pop");});
  var cv=document.getElementById("stars"),x=cv.getContext("2d"),s=[],shoot=null,still=matchMedia("(prefers-reduced-motion: reduce)").matches;
  function size(){cv.width=cv.offsetWidth*devicePixelRatio;cv.height=cv.offsetHeight*devicePixelRatio;s=[];for(var k=0;k<Math.min(260,cv.width*cv.height/9000);k++)s.push({x:Math.random()*cv.width,y:Math.random()*cv.height*.75,r:Math.random()*1.4*devicePixelRatio+.3,p:Math.random()*6});}
  function draw(tm){x.clearRect(0,0,cv.width,cv.height);
    s.forEach(function(a){var o=.35+.65*Math.abs(Math.sin(tm/1400+a.p));x.globalAlpha=o;x.fillStyle="#f3e9df";x.beginPath();x.arc(a.x,a.y,a.r,0,7);x.fill();});
    if(!shoot&&Math.random()<.006)shoot={x:Math.random()*cv.width*.7,y:Math.random()*cv.height*.3,l:0};
    if(shoot){shoot.l+=14*devicePixelRatio;var g=x.createLinearGradient(shoot.x+shoot.l,shoot.y+shoot.l*.4,shoot.x+shoot.l-120,shoot.y+shoot.l*.4-48);g.addColorStop(0,"rgba(240,180,69,.9)");g.addColorStop(1,"rgba(240,180,69,0)");
      x.globalAlpha=1;x.strokeStyle=g;x.lineWidth=2*devicePixelRatio;x.beginPath();x.moveTo(shoot.x+shoot.l,shoot.y+shoot.l*.4);x.lineTo(shoot.x+shoot.l-120,shoot.y+shoot.l*.4-48);x.stroke();if(shoot.l>cv.width*.5)shoot=null;}
    if(!still)requestAnimationFrame(draw);}
  size();addEventListener("resize",size);requestAnimationFrame(draw);
})();
</script>""")
    page("/404", "Te has perdido en la montaña | Guías Ad Astra", "La página que buscas no existe o ha cambiado de sitio.", body, "", noindex=True)


def build_calculator():
    path = "/calculadora-rutas/"
    faq = [
        ("¿Cómo se calcula el tiempo de una ruta de montaña con el MIDE?", "Se calcula por separado el tiempo por distancia (5 km/h en pistas, 4 km/h en sendas y 3 km/h en malas sendas) y por desnivel (400 m/h de subida y 600 m/h de bajada). La duración es el mayor de los dos más la mitad del menor. Es tiempo de marcha efectiva, sin paradas."),
        ("¿Qué tipo de camino elijo?", "Pistas para pistas forestales y carreteras; sendas para caminos de herradura, sendas lisas y prados; malas sendas para canchales, pedreras, cauces de ríos o sendas muy rotas. Si la ruta mezcla tipos, elige el que más abunde."),
        ("¿Qué es el esfuerzo MIDE?", "Es la valoración de 1 a 5 del esfuerzo necesario según las horas de marcha: 1 hasta 1 h, 2 de 1 a 3 h, 3 de 3 a 6 h, 4 de 6 a 10 h y 5 más de 10 h."),
        ("¿Por qué no se suman los dos tiempos?", "Porque mientras subes también avanzas. Sumarlos daría tiempos demasiado largos; quedarse con el mayor, demasiado cortos. Sumar la mitad del menor se ajusta bien a la realidad."),
        ("¿El tiempo incluye las paradas?", "No: el MIDE da tiempo de marcha efectiva. Se recomienda sumar entre un 10 % y un 20 % para descansos, hidratación e imprevistos; puedes elegirlo en «Margen para paradas»."),
        ("¿Qué archivos de track puedo subir?", "GPX (el más habitual en Wikiloc, Strava, Garmin, Komoot o Suunto), KML de Google Earth y TCX. El archivo se lee en tu propio móvil u ordenador: no se sube a ningún servidor."),
        ("¿Puedo descargar el perfil y el mapa?", "Sí. Después de cargar el track, descarga en PNG el perfil de altitud, el mapa o una ficha completa con los datos, el perfil y el mapa juntos, lista para compartir."),
        ("¿Por qué el desnivel puede diferir del de otras apps?", "Cada app filtra el ruido del GPS de una forma. Nosotros suavizamos las altitudes para no inflar el desnivel con pequeños saltos del GPS, así que suele salir algo menor que el desnivel «en bruto»."),
    ]
    body = (hero("Herramientas", "Calculadora de rutas de montaña", "Escribe la distancia, el desnivel y el tipo de camino y te decimos cuánto vas a tardar según el MIDE. O sube tu track GPX y descarga su perfil, su mapa y la ficha de la ruta.", HERO, [("Inicio", "/"), ("Calculadora de rutas", "")],
                 '<a class="btn btn-primary" href="#calculadora">Calcular duración</a><a class="btn btn-ghost" href="#track">Analizar un track</a>') +
            '<section class="section" id="calculadora"><div class="wrap calc-grid">'
            '<form class="panel calc-form" id="calc" novalidate><p class="eyebrow">Calculadora</p><h2 style="font-size:2.2rem">Duración de la ruta</h2>'
            '<div class="field"><label for="c-km">Distancia</label><div class="unit-in"><input id="c-km" type="number" inputmode="decimal" min="0" step="0.1" value="12"><span>km</span></div></div>'
            '<div class="row2"><div class="field"><label for="c-up">Desnivel de subida</label><div class="unit-in"><input id="c-up" type="number" inputmode="numeric" min="0" step="10" value="800"><span>m+</span></div></div>'
            '<div class="field"><label for="c-down">Desnivel de bajada</label><div class="unit-in"><input id="c-down" type="number" inputmode="numeric" min="0" step="10" placeholder="igual que la subida"><span>m−</span></div></div></div>'
            '<div id="ajustes" style="display:grid;gap:16px"><div class="field"><span class="label">Tipo de camino</span><div class="seg" role="radiogroup" aria-label="Tipo de camino">'
            '<label><input type="radio" name="firme" value="pista"><span>Pistas · 5 km/h</span></label><label><input type="radio" name="firme" value="senda" checked><span>Sendas · 4 km/h</span></label><label><input type="radio" name="firme" value="mala"><span>Malas sendas · 3 km/h</span></label></div>'
            '<p class="hint">Pistas y carreteras; caminos, sendas lisas y prados; malas sendas, canchales y cauces. Si la ruta mezcla tipos, elige el que más abunde.</p></div>'
            '<div class="field"><label for="c-paradas">Margen para paradas</label><select id="c-paradas"><option value="0">Sin paradas (marcha efectiva)</option><option value="0.10">+10 % · descansos breves</option><option value="0.15">+15 % · descansos y comer</option><option value="0.20">+20 % · grupo, fotos e imprevistos</option></select></div></div></form>'
            '<div class="calc-out" id="calc-out" aria-live="polite"></div></div></section>' +
            '<section class="section alt" id="track"><div class="wrap" style="display:grid;grid-template-columns:minmax(0,1fr);gap:26px"><div class="section-head" style="margin:0"><p class="eyebrow">Analiza tu track</p><h2>Sube un GPX y mira el perfil</h2>'
            '<p class="muted">Distancia, desnivel, altitudes, pendiente máxima, duración estimada, perfil interactivo y mapa. El archivo no sale de tu dispositivo.</p></div>'
            '<label class="drop" id="trk-drop" for="trk-file"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#e9a53b" stroke-width="1.6" aria-hidden="true"><path d="M3 19l5-9 4 6 3-4 6 7z"/><path d="M12 3v8m-3-3 3 3 3-3"/></svg>'
            '<b>Arrastra aquí tu track</b><span class="muted">o pulsa para elegirlo · GPX, KML o TCX</span><input type="file" id="trk-file" accept=".gpx,.kml,.tcx,application/gpx+xml,application/vnd.google-earth.kml+xml"></label>'
            '<div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center"><button type="button" class="btn btn-ghost" id="trk-demo" data-src="/data/ejemplo-laguna-grande.gpx">Probar con un ejemplo de Gredos</button><p class="err" id="trk-err" role="alert"></p></div>'
            '<div id="trk-res" hidden style="display:grid;gap:20px"><div class="trk-head"><h3 id="trk-name" style="font-size:2rem"></h3><a class="small" href="#calculadora">Cambiar ritmo ↑</a></div>'
            '<dl class="trk-stats" id="trk-stats"></dl><div><p class="label" style="margin-bottom:10px">Perfil de altitud · pasa el dedo o el ratón por encima</p><div class="prof" id="trk-prof"></div></div>'
            '<div id="trk-map" hidden></div><p class="hint" id="trk-note"></p>'
            '<div class="dl-row"><span class="label">Descargar imagen</span><div style="display:flex;flex-wrap:wrap;gap:10px"><button type="button" class="btn btn-primary" data-dl="ficha">Ficha completa</button><button type="button" class="btn btn-ghost" data-dl="perfil">Perfil</button><button type="button" class="btn btn-ghost" data-dl="mapa" hidden>Mapa</button></div></div></div></div></section>' +
            '<section class="section"><div class="wrap split"><div class="stack" style="gap:0">' +
            block("Cómo calculamos el tiempo", '<div style="display:grid;gap:18px">' + prose([
                "Seguimos el MIDE (Método de Información de Excursiones), el sistema con el que las federaciones de montaña valoran las rutas. Da el tiempo de marcha efectiva, sin paradas:"]) +
                '<div class="formula"><b>Tiempo por distancia</b> = km ÷ velocidad del camino (pistas 5 km/h · sendas 4 km/h · malas sendas 3 km/h)<br><b>Tiempo por desnivel</b> = metros de subida ÷ 400 m/h + metros de bajada ÷ 600 m/h<br><b>Duración</b> = el mayor de los dos + la mitad del menor</div>' +
                prose(["Ejemplo: 12 km por pista con 800 m de subida y 250 m de bajada. Por distancia: 12 ÷ 5 = 2 h 24 min. Por desnivel: 800 ÷ 400 + 250 ÷ 600 = 2 h 25 min. Duración: 2 h 25 min + 1 h 12 min = unas 3 h 35 min de marcha efectiva.",
                       "Con un track, el cálculo se hace por tramos de 250 m que se suman, como pide el MIDE. Así una ruta con subidas y bajadas fuertes sale más realista que con los totales.",
                       "El tiempo da el «esfuerzo necesario» del MIDE, de 1 a 5: 1 hasta 1 h, 2 de 1 a 3 h, 3 de 3 a 6 h, 4 de 6 a 10 h y 5 más de 10 h. Las otras tres valoraciones del MIDE (medio, itinerario y desplazamiento) dependen del terreno y no se pueden sacar de un track.",
                       "Recomendamos sumar entre un 10 % y un 20 % para descansos, hidratación e imprevistos. Nieve, calor, piedra suelta, niños o mochilas pesadas pueden alargar bastante la ruta: sal siempre con margen de luz."]) +
                '<p><a href="https://mide.montanasegura.com/mide/" target="_blank" rel="noopener">Más información sobre el método MIDE (Montaña Segura) →</a></p></div>') +
            block("Preguntas frecuentes", faq_html(faq)) +
            '</div><div class="sticky"><div class="panel"><p class="eyebrow">¿Mejor con guía?</p><h3>Te llevamos nosotros</h3><p class="muted">Rutas guiadas por Gredos para todos los niveles, desde 15 € por persona.</p>'
            '<a class="btn btn-primary" href="/actividades/senderismo-avila-gredos/">Senderismo en Gredos</a><a class="btn btn-ghost" href="/actividades/ascensiones-montana/">Ascensiones</a></div></div></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Calculadora de rutas", path)]), faq_ld(faq),
          {"@context": "https://schema.org", "@type": "WebApplication", "name": "Calculadora de rutas de montaña", "url": url(path), "applicationCategory": "TravelApplication", "operatingSystem": "Web",
           "description": "Calcula la duración de una ruta de senderismo o montaña a partir de distancia y desnivel, y analiza tracks GPX con perfil de altitud.", "offers": {"@type": "Offer", "price": 0, "priceCurrency": "EUR"},
           "provider": {"@id": D + "/#empresa"}}]
    head = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">'
    scripts = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin="" defer></script><script src="/js/calculadora.js" defer></script>'
    page(path, "Calculadora MIDE de tiempo de rutas y perfil de GPX | Guías Ad Astra",
         "Calcula la duración de una ruta de senderismo con el método MIDE a partir de distancia y desnivel. Sube tu track GPX y descarga el perfil de altitud, el mapa y la ficha de la ruta gratis.",
         body, "otr", ld, priority="0.8", head=head, scripts=scripts)

# ---------------------------------------------------------------- build
def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"), OUT)
    cfg = os.path.join(OUT, "config.js")
    c = open(cfg, encoding="utf-8").read().replace('calendarioURL: ""', 'calendarioURL: "",\n  // Carpeta donde está publicada la web ("" si está en la raíz del dominio)\n  base: "%s"' % BASE)
    open(cfg, "w", encoding="utf-8").write(c)
    build_home(); build_activities_index(); build_courses_index(); build_calendar(); build_rental(); build_about(); build_contact(); build_404(); build_calculator()
    for a in ACTIVITIES:
        build_activity(a)
    for c in COURSES:
        build_course(c)
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        "  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n" % (url(p), TODAY, pr) for p, pr in PAGES) + "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
    if BASE:
        os.remove(os.path.join(OUT, "sitemap.xml")) if os.path.exists(os.path.join(OUT, "sitemap.xml")) else None
        open(os.path.join(OUT, ".htaccess"), "w").write("ErrorDocument 404 %s/404.html\n" % BASE)
        print("Versión de prueba en", BASE, "(noindex, sin sitemap)"); return
    open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nDisallow: /calendario-google/\n\nSitemap: %s/sitemap.xml\n" % D)
    print("Páginas generadas:", len(PAGES) + 1)

if __name__ == "__main__":
    main()
