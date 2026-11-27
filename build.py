# -*- coding: utf-8 -*-
"""Genera la web estática de Guías Ad Astra en ./dist  ->  python3 build.py"""
import json, os, shutil, html, datetime, sys
from data import *
import precios
precios.aplicar()  # precios desde la hoja de Google (si responde)

BASE = os.environ.get("BASE", "").rstrip("/")  # p. ej. BASE=/NUEVA para publicar en una subcarpeta
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist" + (("-" + BASE.strip("/")) if BASE else ""))
D = SITE["domain"]
TODAY = datetime.date.today().isoformat()
PAGES = []  # (path, priority) para el sitemap
import hashlib
_ST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
ASSETS = ("css/estilos.css", "js/app.js", "js/calculadora.js", "js/topografia.js", "js/meteo.js", "js/rios.js", "js/nieve.js", "js/mochila.js", "js/gpx.js", "js/video3d.js", "config.js")
VER = {a: hashlib.md5(open(os.path.join(_ST, a), "rb").read()).hexdigest()[:8] for a in ASSETS}

def e(s):
    return html.escape(str(s), quote=True)

def url(path):
    return D + path

WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.4-2.3-1.4-.8-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.3 2.4 1 2.9.8 3.4.7.5-.1 1.7-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4C2.7 15.6 2.2 13.8 2.2 12 2.2 6.6 6.6 2.2 12 2.2S21.8 6.6 21.8 12 17.4 21.8 12 21.8zM12 0C5.4 0 0 5.4 0 12c0 2.1.6 4.2 1.6 6L0 24l6.2-1.6c1.7 1 3.7 1.5 5.8 1.5 6.6 0 12-5.4 12-12S18.6 0 12 0z"/></svg>'
CHEV = '<svg class="chev" viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" stroke="currentColor" stroke-width="1.6" fill="none"/></svg>'

ORG = {
    "@type": ["LocalBusiness", "SportsActivityLocation"], "@id": D + "/#empresa",
    "name": SITE["name"], "alternateName": ["Ad Astra Montaña y Aventura", "AdAstra Guías de Montaña", "Guías de montaña Ad Astra", "Ad Astra Guías"], "url": D + "/",
    "logo": {"@type": "ImageObject", "url": D + "/img/logo-512.png", "width": 512, "height": 512}, "image": HERO, "telephone": SITE["phone_intl"], "email": SITE["email"],
    "priceRange": "15€ - 800€",
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"}],
    "address": {"@type": "PostalAddress", "addressLocality": "Fuentes de Béjar", "addressRegion": "Salamanca", "postalCode": "37796", "addressCountry": "ES"},
    "areaServed": ["Ávila", "Salamanca", "Cáceres", "León", "Palencia", "Segovia", "Burgos", "Valladolid", "Madrid", "Sierra de Gredos", "Castilla y León"],
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"}],
    "sameAs": [SITE["instagram"], SITE["facebook"]],
    "founder": {"@type": "Person", "name": "Jairo Hernández"},
}

RELACION = {  # qué enlazar al final de cada herramienta y artículo
    "/meteo/": ["/nieve/", "/rayos-uv-proteccion-solar-montana/", "/barrancos-caudal/", "/como-leer-la-nieve-y-los-aludes/"],
    "/nieve/": ["/meteo/", "/como-leer-la-nieve-y-los-aludes/", "/lista-material-montana/", "/teoria-de-las-capas/"],
    "/barrancos-caudal/": ["/meteo/", "/topografia-barrancos/", "/lista-material-montana/", "/como-preparar-la-mochila/"],
    "/calculadora-rutas/": ["/editor-gpx/", "/video-ruta-3d/", "/meteo/", "/lista-material-montana/"],
    "/editor-gpx/": ["/video-ruta-3d/", "/calculadora-rutas/", "/meteo/", "/como-preparar-la-mochila/"],
    "/video-ruta-3d/": ["/editor-gpx/", "/calculadora-rutas/", "/meteo/", "/teoria-de-las-capas/"],
    "/lista-material-montana/": ["/como-preparar-la-mochila/", "/teoria-de-las-capas/", "/meteo/", "/calculadora-rutas/"],
    "/topografia-barrancos/": ["/barrancos-caudal/", "/lista-material-montana/", "/meteo/", "/editor-gpx/"],
    "/como-leer-la-nieve-y-los-aludes/": ["/nieve/", "/meteo/", "/teoria-de-las-capas/", "/lista-material-montana/"],
    "/como-preparar-la-mochila/": ["/lista-material-montana/", "/teoria-de-las-capas/", "/calculadora-rutas/", "/meteo/"],
    "/rayos-uv-proteccion-solar-montana/": ["/meteo/", "/teoria-de-las-capas/", "/lista-material-montana/", "/como-leer-la-nieve-y-los-aludes/"],
    "/teoria-de-las-capas/": ["/como-preparar-la-mochila/", "/lista-material-montana/", "/meteo/", "/como-leer-la-nieve-y-los-aludes/"],
    "/escalas-dificultad-escalada-ferratas-alpinismo-barrancos/": ["/crampones-piolet-botas-material-invernal/", "/barrancos-caudal/", "/calculadora-rutas/", "/tormentas-en-la-montana/"],
    "/crampones-piolet-botas-material-invernal/": ["/raquetas-de-nieve-y-esqui-de-travesia/", "/como-leer-la-nieve-y-los-aludes/", "/lista-material-montana/", "/escalas-dificultad-escalada-ferratas-alpinismo-barrancos/"],
    "/mal-de-altura-sintomas-prevencion/": ["/hipotermia-congelaciones-botiquin-montana/", "/rayos-uv-proteccion-solar-montana/", "/teoria-de-las-capas/", "/federarse-seguro-montana-rescate/"],
    "/hipotermia-congelaciones-botiquin-montana/": ["/teoria-de-las-capas/", "/tormentas-en-la-montana/", "/federarse-seguro-montana-rescate/", "/meteo/"],
    "/tormentas-en-la-montana/": ["/meteo/", "/barrancos-caudal/", "/hipotermia-congelaciones-botiquin-montana/", "/orientacion-en-montana-mapa-brujula/"],
    "/orientacion-en-montana-mapa-brujula/": ["/editor-gpx/", "/calculadora-rutas/", "/rutas-clasicas-gredos-almanzor-laguna-grande-galayos/", "/federarse-seguro-montana-rescate/"],
    "/vivac-acampada-libre-espana/": ["/lista-material-montana/", "/meteo/", "/tormentas-en-la-montana/", "/rutas-clasicas-gredos-almanzor-laguna-grande-galayos/"],
    "/federarse-seguro-montana-rescate/": ["/hipotermia-congelaciones-botiquin-montana/", "/orientacion-en-montana-mapa-brujula/", "/como-leer-la-nieve-y-los-aludes/", "/mal-de-altura-sintomas-prevencion/"],
    "/raquetas-de-nieve-y-esqui-de-travesia/": ["/nieve/", "/como-leer-la-nieve-y-los-aludes/", "/crampones-piolet-botas-material-invernal/", "/meteo/"],
    "/iniciacion-alpinismo-gredos-rutas-progresivas/": ["/crampones-piolet-botas-material-invernal/", "/como-leer-la-nieve-y-los-aludes/", "/rutas-clasicas-gredos-almanzor-laguna-grande-galayos/", "/meteo/"],
    "/mejores-vias-escalada-gredos/": ["/escalas-dificultad-escalada-ferratas-alpinismo-barrancos/", "/rutas-clasicas-gredos-almanzor-laguna-grande-galayos/", "/tormentas-en-la-montana/", "/meteo/"],
    "/rutas-clasicas-gredos-almanzor-laguna-grande-galayos/": ["/meteo/", "/editor-gpx/", "/video-ruta-3d/", "/crampones-piolet-botas-material-invernal/"],
}


def relacionados(path):
    if path not in RELACION:
        return ""
    todo = {h: (t, d, "Herramienta") for h, t, d, _ in HERRAMIENTAS}
    todo.update({h: (t, d, "Artículo") for h, t, d, _ in ARTICULOS})
    cards = "".join('<a class="rel-card" href="%s"><small>%s</small><b>%s</b><span>%s</span></a>' % (h, todo[h][2], e(todo[h][0]), e(todo[h][1])) for h in RELACION[path] if h in todo)
    return ('<section class="section rel"><div class="wrap"><p class="eyebrow">Sigue explorando</p><h2>Herramientas y artículos relacionados</h2><div class="rel-grid">' + cards +
            '</div><p class="rel-mas"><a href="/herramientas/">Todas las herramientas</a> · <a href="/articulos/">Todos los artículos</a></p></div></section>')


def articulo_ld(path, titulo, desc, publicado):
    slug = path.strip("/")
    return {"@context": "https://schema.org", "@type": "Article", "headline": titulo, "description": desc, "inLanguage": "es",
            "image": D + "/img/og/" + slug + ".png", "datePublished": publicado, "dateModified": TODAY,
            "author": {"@type": "Person", "name": "Jairo Hernández", "url": D + "/sobre-nosotros/", "jobTitle": "Guía de montaña"},
            "publisher": {"@id": D + "/#empresa"}, "mainEntityOfPage": url(path)}


def app_ld(path, nombre, desc, cat="UtilitiesApplication"):
    return {"@context": "https://schema.org", "@type": "WebApplication", "name": nombre, "url": url(path), "applicationCategory": cat, "operatingSystem": "Web",
            "description": desc, "inLanguage": "es", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": 0, "priceCurrency": "EUR"}, "provider": {"@id": D + "/#empresa"}}


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(items)]}

def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

NAV_ACT = [("Todas las actividades", "/actividades/"), ("Barranquismo", "/actividades/?categoria=Barranquismo"), ("Vías ferratas", "/actividades/?categoria=Vías ferratas"),
           ("Alpinismo y ascensiones", "/actividades/?categoria=Ascensiones"), ("Espeleología", "/actividades/?categoria=Espeleología"), ("Escalada y boulder", "/actividades/?categoria=Escalada"),
           ("Senderismo", "/actividades/?categoria=Senderismo"), ("Travesías y viajes", "/actividades/?categoria=Travesías y viajes")]
NAV_CUR = [("Todos los cursos", "/formacion-cursos/"), ("Calendario de cursos", "/calendario/")] + [(c["disc_label"], "/actividades/%s/" % c["slug"]) for c in COURSES]
HER_CAT = {
    "Barrancos y escalada": [("Boulder en Las Tuerces", "/actividades/boulder-las-tuerces/"), ("Boulder en Zona Centro", "/actividades/boulder-zona-centro-salamanca-caceres/"), ("Caudal de barrancos", "/barrancos-caudal/"), ("Topografía de barrancos", "/topografia-barrancos/")],
    "Meteorología y nieve": [("Estado de la nieve", "/nieve/"), ("Meteorología de montaña", "/meteo/")],
    "Planificar rutas": [("Calculadora de rutas", "/calculadora-rutas/"), ("Editor GPX", "/editor-gpx/"), ("Lista de material", "/lista-material-montana/"), ("Vídeo 3D de la ruta", "/video-ruta-3d/")],
}
NAV_HER = [("Todas las herramientas", "/herramientas/")] + sum([[("§" + c, "")] + HER_CAT[c] for c in sorted(HER_CAT)], [])
import arts_a, arts_b, arts_util
NUEVOS = arts_a.ARTS + arts_b.ARTS
ARTICULOS = [
    ("/como-leer-la-nieve-y-los-aludes/", "Cómo leer la nieve y el peligro de aludes", "Cómo cambia el manto, placas de viento, tipos de aludes, el boletín de AEMET y cómo leer una ladera.", "nieve"),
    ("/como-preparar-la-mochila/", "Cómo preparar la mochila", "Dónde va cada cosa, por qué lo pesado va pegado a la espalda y cómo ajustar las correas, con ilustraciones.", "mochila"),
    ("/rayos-uv-proteccion-solar-montana/", "Rayos UV y protección solar", "Qué rayos UV hacen daño, por qué en la montaña te quemas más, qué FPS usar y qué gafas de sol necesitas.", "uv"),
    ("/teoria-de-las-capas/", "La teoría de las capas", "Cómo vestirse para la montaña: base, intermedia, exterior y la capa de reserva, en viñetas.", "capas"),
] + [(a["path"], a["corto"], a["card"], a["ico"]) for a in NUEVOS]
HERRAMIENTAS = [
    ("/meteo/", "Meteorología de montaña", "Previsión a 15 días en cumbre y base para 27 macizos, con viento, nieve, isocero, avisos de AEMET y webcams.", "meteo"),
    ("/nieve/", "Estado de la nieve", "Nieve reciente, placas de viento, costras y nieve húmeda estimadas cada día por macizo, con mapa.", "nieve"),
    ("/barrancos-caudal/", "Caudal de barrancos", "Caudal en tiempo real de los barrancos del Jerte, Mazobre y Valporquero con su estado para hacerlos.", "caudal"),
    ("/calculadora-rutas/", "Calculadora de rutas MIDE", "Tiempo de una ruta por distancia y desnivel, o a partir de tu GPX, con perfil y ficha descargables.", "calc"),
    ("/editor-gpx/", "Editor GPX", "Une, divide y corrige tracks, dibuja tramos, añade waypoints y descarga mapa y perfil en imagen.", "gpx"),
    ("/video-ruta-3d/", "Vídeo 3D de la ruta", "Crea un vídeo de tu ruta sobre el relieve en 3D, con perfil, datos y waypoints. Tipo Relive, gratis.", "video"),
    ("/lista-material-montana/", "Lista de material", "Qué llevar en la mochila para barrancos, escalada, alpinismo, senderismo, montañismo o vivac, para ir tachando.", "lista"),
    ("/topografia-barrancos/", "Topografía de barrancos", "Dibuja el croquis de un barranco con rápeles y destrepes y calcula la cuerda necesaria.", "topo"),
]
ART_CAT = {
    "Equipo y ropa": ["/como-preparar-la-mochila/", "/teoria-de-las-capas/"],
    "Escalada y alpinismo": ["/crampones-piolet-botas-material-invernal/", "/escalas-dificultad-escalada-ferratas-alpinismo-barrancos/", "/mejores-vias-escalada-gredos/", "/iniciacion-alpinismo-gredos-rutas-progresivas/"],
    "Nieve": ["/como-leer-la-nieve-y-los-aludes/", "/raquetas-de-nieve-y-esqui-de-travesia/"],
    "Rutas y orientación": ["/orientacion-en-montana-mapa-brujula/", "/rutas-clasicas-gredos-almanzor-laguna-grande-galayos/", "/vivac-acampada-libre-espana/"],
    "Seguridad y salud": ["/federarse-seguro-montana-rescate/", "/hipotermia-congelaciones-botiquin-montana/", "/mal-de-altura-sintomas-prevencion/", "/rayos-uv-proteccion-solar-montana/", "/tormentas-en-la-montana/"],
}
import unicodedata as _ud
def _orden(t):
    return _ud.normalize("NFD", t.lower()).encode("ascii", "ignore").decode()
_ART_POR_PATH = {h: (h, t, d, ic) for h, t, d, ic in ARTICULOS}
assert sorted(sum(ART_CAT.values(), [])) == sorted(_ART_POR_PATH), "Falta categorizar algún artículo"
ART_GRUPOS = [(c, sorted((_ART_POR_PATH[h] for h in ART_CAT[c]), key=lambda a: _orden(a[1]))) for c in sorted(ART_CAT, key=_orden)]
NAV_ART = [("Todos los artículos", "/articulos/")] + sum([[("§" + c, "")] + [(t, h) for h, t, _, _ in arts] for c, arts in ART_GRUPOS], [])
NAV_OTR = [("Iniciativas de turismo rural", "/iniciativas-turismo-rural/"), ("Creación y mantenimiento de senderos", "/creacion-mantenimiento-senderos/"), ("Route setting", "/route-setting/"), ("Organización de eventos", "/actividades/organizacion-eventos-deportivos/"), ("Gredos Limpio", "/actividades/gredos-limpio/"),
           ("Oeste de Gredos", "/actividades/comarca-natural-oeste-de-gredos/"), ("Vía Verde Ruta de la Plata", "/actividades/via-verde-ruta-de-la-plata/")]

def dd(label, items, key, active):
    links, abierto = "", False
    for n, h in items:
        if n.startswith("§"):
            links += ("</div>" if abierto else "") + '<div class="dd-grupo"><span class="dd-cat">%s</span>' % e(n[1:])
            abierto = True
        else:
            links += '<a href="%s">%s</a>' % (e(h), e(n))
    links += "</div>" if abierto else ""
    cur = ' style="color:var(--gold)"' if active == key else ""
    return '<div class="dd%s"><button' % (" dd-ancho" if any(n.startswith("§") for n, _ in items) else "") + ' type="button" aria-expanded="false"%s>%s %s</button><div class="dd-menu">%s</div></div>' % (cur, label, CHEV, links)

def header(active=""):
    def a(h, n, k):
        return '<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if active == k else "", n)
    return ('<header class="site-header"><div class="wrap"><a class="brand" href="/" aria-label="Guías Ad Astra, inicio"><img src="/img/logo-adastra-112.png" width="42" height="56" alt="Logotipo de Guías Ad Astra"><span>AD ASTRA <small>Montaña y aventura</small></span></a>'
            '<button class="menu-toggle" aria-expanded="false" aria-controls="nav" aria-label="Abrir menú">☰</button>'
            '<nav class="nav" id="nav" aria-label="Principal">' +
            dd("Actividades", NAV_ACT, "act", active) + dd("Formación–Cursos", NAV_CUR, "cur", active) +
            a("/actividades/alquiler-material-montana/", "Alquiler", "alq") + dd("Herramientas", NAV_HER, "her", active) + dd("Artículos", NAV_ART, "art", active) + dd("Otros", NAV_OTR, "otr", active) +
            a("/sobre-nosotros/", "Nosotros", "nos") + a("/contacto/", "Contacto", "con") +
            '<a class="btn btn-primary" href="/calendario/">Reservar</a></nav></div></header>')

def footer():
    acts = "".join('<li><a href="/actividades/%s/">%s</a></li>' % (a["slug"], e(a["title"])) for a in ACTIVITIES if a["cat"] in ("Barranquismo", "Vías ferratas", "Escalada"))[:2000]
    return ('<footer class="site-footer"><div class="wrap"><div class="foot-grid">'
            '<div><a class="brand brand-foot" href="/" aria-label="Guías Ad Astra, inicio"><img src="/img/logo-adastra.png" width="93" height="124" alt="Guías Ad Astra · Guías de montaña y aventura" loading="lazy"></a><p style="margin-top:14px;max-width:34ch">«Hacia las estrellas». Guías de montaña y aventura en Gredos, Castilla y León y el mundo.</p>'
            '<p style="margin-top:14px"><a href="%s" rel="noopener" target="_blank">Instagram</a> · <a href="%s" rel="noopener" target="_blank">Facebook</a></p></div>' % (SITE["instagram"], SITE["facebook"]) +
            '<div><h4>Contacto</h4><ul><li><a href="tel:%s">%s</a></li><li><a href="mailto:%s">%s</a></li><li><a href="https://wa.me/%s" target="_blank" rel="noopener">WhatsApp</a></li><li>%s</li></ul></div>' % (SITE["phone_intl"], SITE["phone"], SITE["email"], SITE["email"], SITE["wa"], SITE["hours"]) +
            '<div><h4>Bases</h4><ul>%s</ul></div>' % "".join("<li>%s</li>" % b for b in SITE["bases"]) +
            '<div><h4>Más visitado</h4><ul><li><a href="/actividades/alquiler-material-montana/">Alquiler de material</a></li><li><a href="/calendario/">Calendario de cursos</a></li><li><a href="/actividades/boulder-zona-centro-salamanca-caceres/">Boulder en Salamanca</a></li><li><a href="/actividades/boulder-las-tuerces/">Boulder en Las Tuerces</a></li><li><a href="/actividades/barranquismo-avila/">Barranquismo en Gredos</a></li></ul></div>'
            '</div><div class="copy"><span>© %d Guías Ad Astra · Montaña y Aventura</span><span>Empresa de turismo activo · Castilla y León</span></div></div></footer>'
            '<a class="wa-float" href="https://wa.me/%s" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">%s</a>' % (datetime.date.today().year, SITE["wa"], WA_SVG))

def page(path, title, desc, body, active="", ld=None, og_type="website", image=None, priority="0.7", noindex=False, head="", scripts=""):
    ld = list(ld or [])
    if path != "/404" and not any(isinstance(x, dict) and x.get("@id") == D + "/#empresa" for x in ld):
        ld.append({"@context": "https://schema.org", "@type": "Organization", "@id": D + "/#empresa", "name": SITE["name"], "url": D + "/", "logo": ORG["logo"], "sameAs": [SITE["instagram"], SITE["facebook"]]})
    slug = path.strip("/").replace("/", "-")
    if not image and slug and os.path.exists(os.path.join(_ST, "img", "og", slug + ".png")):
        image = D + "/img/og/" + slug + ".png"
    image = image or SITE["og_image"]
    body = body + relacionados(path)
    lds = "".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)
    doc = ('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
           '<title>%s</title><meta name="description" content="%s">' % (e(title), e(desc)) +
           ('<meta name="robots" content="noindex">' if (noindex or BASE) else '<meta name="robots" content="index,follow,max-image-preview:large">') +
           '<link rel="canonical" href="%s">' % url(path) +
           '<meta property="og:type" content="%s"><meta property="og:site_name" content="Guías Ad Astra"><meta property="og:locale" content="es_ES">' % og_type +
           '<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s"><meta property="og:image" content="%s"><meta property="og:image:alt" content="%s">' % (e(title), e(desc), url(path), e(image), e(title)) +
           '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="%s"><meta name="twitter:description" content="%s"><meta name="twitter:image" content="%s">' % (e(title), e(desc), e(image)) +
           '<meta name="theme-color" content="#160d09"><meta name="geo.region" content="ES-CL"><meta name="geo.placename" content="Sierra de Gredos, Castilla y León">'
           '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600&family=Barlow:wght@400;500;600&family=Bebas+Neue&display=swap">'
           '<link rel="stylesheet" href="/css/estilos.css"><link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/img/favicon-32.png" type="image/png" sizes="32x32"><link rel="icon" href="/img/favicon-48.png" type="image/png" sizes="48x48"><link rel="icon" href="/img/favicon-192.png" type="image/png" sizes="192x192"><link rel="apple-touch-icon" href="/img/apple-touch-icon.png">' + head + lds +
           '</head><body>' + header(active) + '<main id="contenido">' + body + '</main>' + footer() +
           '<script src="/config.js"></script><script src="/js/app.js" defer></script>' + scripts + '</body></html>')
    for asset in ASSETS:
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

def a_secs(a):
    return a.get("secciones", [])

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
                   '<div style="display:flex;gap:10px;flex-wrap:wrap"><button type="button" class="btn btn-ghost pick" data-pick="%s">Elegir esta opción</button>%s</div></article>'
                   % (e(o["name"]), e(o["place"]), e(o["dur"]), o["price"], "".join("<span>%s</span>" % e(s) for s in o["specs"]), e(o["desc"]), e(o["name"]),
                      ('<a class="btn btn-ghost" href="%s">Ver %s</a>' % (OPTION_URL[o["name"]], "detalles")) if o["name"] in OPTION_URL else ""))
    return '<div class="options">%s</div>' % "".join(out)

# ---------------------------------------------------------------- páginas de actividad
def act_ld(a, path, prices):
    ld = [crumbs_ld([("Inicio", "/"), ("Actividades", "/actividades/"), (a["title"], path)])]
    prod = {"@context": "https://schema.org", "@type": "Service", "name": a["title"], "description": a.get("seo_desc", a["short"]), "image": a["img"],
            "serviceType": a["cat"], "provider": {"@id": D + "/#empresa"}, "areaServed": {"@type": "Country", "name": "España"}, "url": url(path)}
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
        kb = [(x, y) for x, y in a["ficha"]] + [("Precio", "Desde %d € / persona" % min(prices))]
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
    for t, ps in a_secs(a):
        left.append(block(t, prose(ps)))
    if k in ("options", "senderismo"):
        left.append(block("Elige tu opción", options_html(opts)))
    if k == "senderismo":
        left.append(block("Rutas destacadas", '<div class="two">%s</div>' % "".join('<div class="panel"><h3>%s</h3><p class="muted">%s</p></div>' % (e(n), e(d)) for n, d in a["itinerarios"])))
    if k == "list" and not a.get("macizo"):
        left.append(block("Ascensiones por macizo", '<div class="two">%s</div>' % "".join(
            '<a class="panel" href="/actividades/%s/" style="color:var(--fg)"><h3>%s</h3><p class="muted">%s</p></div></a>'.replace("</div></a>", "</a>") % (asc_slug(g), e(g), e(", ".join(n.split(" ")[0] if False else n.rsplit(" ", 2)[0] for n, _, _, _ in rows[:4]))) for g, rows in a["groups"])))
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
    faq = list(a.get("faq", [])) + (auto_faq(a) if k != "list" else [("¿Cuánto cuesta una ascensión guiada?", "Desde %d € por persona según la cumbre y el tamaño del grupo. Elige la cumbre en la tabla y te enviamos el precio exacto." % precios.desde_slug("ascensiones-montana")), ("¿Puedo proponer otra montaña?", "Sí. Escríbenos con la cumbre que te apetece y la fecha y preparamos la ascensión."), ("¿Qué incluye?", "Guía de montaña titulado y seguro. En ascensiones invernales también te asesoramos sobre material, que puedes alquilarnos.")])
    left.append(block("Preguntas frecuentes", faq_html(faq)))
    form = book_form(a["title"], opts if opts else None, a.get("price", 0), opt_label="Cumbre" if k == "list" else ("Nivel" if k == "senderismo" else "Opción"))
    right = '<div class="sticky" style="display:grid;gap:18px">%s%s</div>' % (upcoming(a["slug"]), form)
    body = (hero(a["cat"], e(a["title"]), e(a.get("lead", a["short"])), a["img"], crumbs, '<a class="btn btn-primary" href="#reservar">Reservar</a>') + keybar(kb) +
            '<section class="section"><div class="wrap split"><div class="stack" style="gap:0">%s</div>%s</div></section>' % ("".join(left), right) + related(a))
    ld = act_ld(a, path, prices) + [faq_ld(faq)]
    page(path, a.get("seo_title", a["title"] + " | Guías Ad Astra"), a.get("seo_desc", a["short"]), body, "act", ld, "product", a["img"], "0.8")

ASC_TXT = {
    "Sierra de Gredos": "El Almanzor (2.592 m), techo del Sistema Central, y las grandes cumbres que rodean el Circo de Gredos: La Galana, Cabeza Nevada, La Mira y Los Galayos, además del Canchal de la Ceja en la Sierra de Béjar. Granito, lagunas glaciares y algunos de los paisajes de alta montaña más bonitos de la península.",
    "Montaña Palentina": "Curavacas, Espigüete y Peña Prieta, los tres colosos de Fuentes Carrionas, en el extremo oriental de la Cordillera Cantábrica. Cumbres de más de 2.400 m con vistas a los Picos de Europa.",
    "Sierra de Guadarrama": "Peñalara, techo de la Comunidad de Madrid, La Maliciosa y El Yelmo en La Pedriza: ascensiones cerca de Madrid y Segovia, perfectas para iniciarse o para la montaña invernal.",
    "Picos de Europa": "Torrecerredo, la cumbre más alta de la Cordillera Cantábrica, Peña Santa de Castilla, Peña Vieja, Tesorero y Peña Castil: caliza, canales y jous en el Parque Nacional más antiguo de España.",
    "Sanabria": "El Coriscao y las cumbres que rodean el lago de Sanabria, en el noroeste de Zamora: lagunas glaciares y paisajes de alta montaña poco frecuentados.",
    "Pirineos": "Aneto, Posets y Monte Perdido, los tresmiles más deseados, junto a cumbres como el Midi d'Ossau, Anayet, Garmo Negro o la Mesa de los Tres Reyes, del Pirineo navarro al aragonés y el francés.",
}

def asc_slug(g):
    return "ascensiones-" + precios._slug(g)

def build_ascensiones_macizos():
    base = next(x for x in ACTIVITIES if x["slug"] == "ascensiones-montana")
    for g, rows in base["groups"]:
        cumbres = [n.rsplit(" ", 2)[0] for n, _, _, _ in rows]
        a = dict(base, slug=asc_slug(g), macizo=True, groups=[(g, rows)],
                 title="Ascensiones guiadas en %s" % g,
                 short="Ascensiones con guía de montaña titulado en %s: %s." % (g, ", ".join(cumbres[:4])),
                 lead=ASC_TXT.get(g, "Ascensiones guiadas en %s." % g),
                 seo_title=("Ascensiones guiadas en %s: %s | Desde %d€" % (g, ", ".join(cumbres[:2]), min(p for *_, p in rows)))[:70],
                 seo_desc=("Ascensiones con guía de montaña en %s: %s. Precio por persona según la cumbre y el tamaño del grupo." % (g, ", ".join(cumbres[:5])))[:158])
        build_activity(a)

def build_trip(a, path):
    crumbs = [("Inicio", "/"), ("Actividades", "/actividades/"), ("Travesías y viajes", "/actividades/?categoria=Travesías y viajes")]
    left = [block("El viaje", prose(a["intro"]))]
    if a.get("etapas"):
        left.append(block("Etapas día a día", '<ol class="stages">%s</ol>' % "".join('<li><span class="d">%s</span><h4>%s</h4><p>%s</p></li>' % (e(d), e(t), e(s)) for d, t, s in a["etapas"])))
    left.append(block("Requisitos", ticks(a["req"])))
    left.append(block("Material necesario", ticks(a["material"], "cols")))
    left.append(block("Qué incluye", '<div class="two"><div class="panel"><h3>Incluye</h3>%s</div><div class="panel"><h3>No incluye</h3>%s</div></div>' % (ticks(a["incluye"]), ticks(a["noincluye"], "cross"))))
    for t, ps in a_secs(a):
        left.append(block(t, prose(ps)))
    if a.get("faq"):
        left.append(block("Preguntas frecuentes", faq_html(a["faq"])))
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
    if a.get("faq"):
        ld.append(faq_ld(a["faq"]))
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
    left.append('<div id="mapa-sectores"></div>' + block("Mapa de sectores", '<div style="display:grid;gap:16px">%s</div>' % mapa))
    left.append(block("Cómo es el boulder", '<div class="two"><div class="panel"><h3>Material</h3>%s</div><div class="panel"><h3>Buenas prácticas</h3>%s</div></div>' % (
        ticks(["Pies de gato", "Magnesio y cepillo", "Crash pad (colchoneta)", "Ropa cómoda y agua"]),
        ticks(["Aparca en los lugares habilitados", "Limpia el magnesio de las presas", "No dejes residuos ni marcas", "Respeta la fauna y la vegetación"]))))
    left.append(block("Preguntas frecuentes", faq_html(a["faq"])))
    info = ('<aside class="panel infobox"><p class="eyebrow">Ficha de la zona</p><h2 class="h3">%s</h2><dl class="kv">%s</dl>'
            '<div style="display:grid;gap:10px;margin-top:16px"><a class="btn btn-primary btn-block" href="#mapa-sectores">Ver mapa de sectores</a>'
            '<a class="btn btn-ghost btn-block" href="%s" target="_blank" rel="noopener">Abrir en Google Maps</a>%s</div>'
            '<p class="hint" style="margin-top:14px">Información orientativa. Respeta siempre la regulación de la zona y el entorno natural.</p></aside>'
            % (e(a["title"]), "".join('<dt>%s</dt><dd>%s</dd>' % (e(k), e(v)) for k, v in [("Zona", a["zona"])] + list(a["datos"])), e(a["map_link"]),
               ('<a class="btn btn-ghost btn-block" href="%s" target="_blank" rel="noopener">%s</a>' % (e(a["pdf"]), e(a["pdf_label"]))) if a.get("pdf") else ""))
    otras = [x for x in ACTIVITIES if x.get("kind") == "boulder" and x["slug"] != a["slug"]]
    if otras:
        info += '<div class="panel"><p class="eyebrow">Más zonas de boulder</p>%s</div>' % "".join('<p style="margin-top:8px"><a href="/actividades/%s/">%s →</a></p>' % (x["slug"], e(x["title"])) for x in otras)
    body = (hero("Escalada · Boulder", e(a["h1"]), e(a["lead"]), a["img"], crumbs, '<a class="btn btn-primary" href="#mapa-sectores">Ver mapa de sectores</a>' + ('<a class="btn btn-ghost" href="%s" target="_blank" rel="noopener">Croquis PDF</a>' % e(a["pdf"]) if a.get("pdf") else "")) + keybar(a["datos"]) +
            '<section class="section" id="mapa"><div class="wrap split"><div class="stack" style="gap:0">%s</div><div class="sticky" style="display:grid;gap:18px">%s</div></div></section>' % ("".join(left), info) + related(a))
    ld = [crumbs_ld([("Inicio", "/"), ("Actividades", "/actividades/"), (a["title"], path)]), faq_ld(a["faq"]),
          {"@context": "https://schema.org", "@type": ["TouristAttraction", "Place"], "name": a["h1"], "description": a["seo_desc"], "image": a["img"], "url": url(path),
           "touristType": "Escaladores", "hasMap": a["map_link"], "address": {"@type": "PostalAddress", "addressRegion": a["zona"], "addressCountry": "ES"}},
          {"@context": "https://schema.org", **ORG}]
    page(path, a["seo_title"], a["seo_desc"], body, "her", ld, "article", a["img"], "0.8")

def build_eventos(a, path):
    body = (hero("Otros", e(a["title"]), e(a["short"]), a["img"], [("Inicio", "/"), ("Otros", "")], '<a class="btn btn-wa" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">%s Pide información</a>' % (SITE["wa"], e("Hola, quiero información sobre organización de eventos deportivos."), WA_SVG)) +
            '<section class="section"><div class="wrap stack"><div><div class="section-head"><p class="eyebrow">Qué hacemos</p><h2>Te organizamos o asesoramos</h2><p class="lead">Nos encargamos de la organización y la seguridad de tu prueba, de principio a fin.</p></div><div class="two">%s</div></div>'
            % "".join('<div class="panel"><h3>%s</h3><p class="muted">%s</p></div>' % (e(n), e(d)) for n, d in a["servicios"]) +
            '<div><div class="section-head"><p class="eyebrow">Experiencia</p><h2>Eventos en los que trabajamos</h2></div><div class="evlist">%s</div></div></div></section>'
            % "".join('<article class="evrow" style="grid-template-columns:minmax(0,1fr)"><div class="evinfo"><span class="tag">%s</span><h3>%s</h3><p class="meta">%s</p>%s</div></article>' % (e(ev[1]), e(ev[0]), e(ev[2]), ('<p style="margin-top:8px"><a href="%s"%s>%s →</a></p>' % (e(ev[3]), ' target="_blank" rel="noopener"' if ev[3].startswith("http") else "", "Web oficial" if ev[3].startswith("http") else "Más información")) if len(ev) > 3 else "") for ev in a["eventos"]))
    page(path, a["seo_title"], a["seo_desc"], body, "otr", [crumbs_ld([("Inicio", "/"), (a["title"], path)]), {"@context": "https://schema.org", **ORG}], image=a["img"], priority="0.5")

def build_gredos_limpio(a, path):
    G = GREDOS_LIMPIO
    fecha = G["fecha"] or "Fecha por confirmar"
    prog = [(G["hora"], "Quedada en la Casa del Parque de Hoyos del Espino. Visita, instrucciones y subida juntos a la Plataforma."), ("10:00", "Comienzo de la limpieza desde la Plataforma de Gredos."), ("14:00", "Regreso a la Plataforma para terminar la jornada todos juntos.")]
    if G["abiertas"]:
        form = ('<form class="book" id="inscripcion" data-inscripcion data-evento="Gredos Limpio" data-edicion="%s" novalidate><p class="eyebrow">Inscripción gratuita</p><h2>Apúntate</h2><p class="muted">%s · %s</p><p class="hint">La inscripción es individual: si venís varias personas, cada una debe inscribirse con sus datos.</p>'
                '<div class="row2"><div class="field"><label for="i-nombre">Nombre</label><input id="i-nombre" name="nombre" autocomplete="given-name"></div><div class="field"><label for="i-ape">Apellidos</label><input id="i-ape" name="apellidos" autocomplete="family-name"></div></div>'
                '<div class="field"><label for="i-email">Correo electrónico</label><input id="i-email" name="email" type="email" autocomplete="email" inputmode="email"></div>'
                '<div class="row2"><div class="field"><label for="i-tel">Teléfono</label><input id="i-tel" name="telefono" type="tel" autocomplete="tel" inputmode="tel"></div><div class="field"><label for="i-loc">Localidad</label><input id="i-loc" name="localidad" autocomplete="address-level2"></div></div>'
                '<input type="text" name="web" class="trampa" tabindex="-1" autocomplete="off" aria-hidden="true"><div class="field"><label for="i-com">Comentarios (opcional)</label><textarea id="i-com" name="comentarios" placeholder="Club o asociación, si vienes con alguno…"></textarea></div>'
                '<label class="check" style="align-items:flex-start"><input type="checkbox" name="privacidad" id="i-priv" style="margin-top:3px"> <span>Acepto que Guías Ad Astra guarde estos datos para gestionar mi inscripción y el seguro de la jornada.</span></label>'
                '<p class="err" role="alert"></p><button class="btn btn-primary btn-block" type="submit">Enviar inscripción</button>'
                '<div class="notice ok" data-ok hidden></div><p class="hint">Tus datos se guardan en nuestra lista de inscritos. No los compartimos con nadie salvo la aseguradora de la jornada.</p></form>'
                % (e(G["edicion"]), e(G["edicion"]), e(fecha)))
    else:
        form = '<div class="panel"><p class="eyebrow">Inscripciones</p><h3>Inscripciones cerradas</h3><p class="muted">Anunciaremos la próxima edición en esta página y en nuestras redes.</p></div>'
    body = (hero("Voluntariado ambiental", "Gredos Limpio", "Cada otoño, antes de que llegue la nieve, limpiamos el Circo de Gredos entre todos los amantes de la sierra. Desde 2013.", a["img"], [("Inicio", "/"), ("Otros", "")],
                 '<a class="btn btn-primary" href="#inscripcion">Apúntate</a>') +
            keybar([("Edición", G["edicion"]), ("Fecha", fecha), ("Lugar", "Hoyos del Espino (Ávila)"), ("Inscripción", "Gratuita")]) +
            '<section class="section"><div class="wrap split"><div class="stack" style="gap:0">' +
            block("Qué es", prose(["Gredos Limpio es una concentración para los amantes de Gredos y de la montaña. Intentamos limpiar todo lo posible la sierra antes de que las nieves tapen los residuos del verano.", "Los asistentes se mueven con libertad por las zonas de actuación, aunque siempre intentamos ir en grupos."])) +
            block("Zona de actuación", prose(["Entre la Plataforma de Gredos, el Puerto de Candeleda, Prao Pozas, el Morezón y la Laguna Grande, en el Circo de Gredos (Macizo Central)."])) +
            block("Programa", '<ol class="stages">%s</ol><p class="hint">Horarios aproximados. Quien quiera volver antes o quedarse más puede hacerlo bajo su responsabilidad.</p>' % "".join('<li><span class="d">%s</span><p>%s</p></li>' % (h, e(t)) for h, t in prog)) +
            block("Qué ofrecemos y qué llevar", '<div class="two"><div class="panel"><h3>Te damos</h3>%s</div><div class="panel"><h3>Trae</h3>%s</div></div>' % (
                ticks(["Seguro de accidentes (colaboración de Patrimonio Natural)", "Acceso gratuito a la Plataforma de Gredos", "Visita guiada a la Casa del Parque", "Bolsas de basura y guantes"]),
                ticks(["Ropa de abrigo o impermeable según el tiempo", "Agua", "Algo de comer para durante y después"]))) +
            '</div><div class="sticky">%s</div></div></section>' % form)
    page(path, a["seo_title"], a["seo_desc"], body, "otr", [crumbs_ld([("Inicio", "/"), (a["title"], path)])], image=a["img"], priority="0.5")

def build_zona(a, path):
    items = [x for x in ACTIVITIES if x["slug"] in a["links"] and x["slug"] != a["slug"]]
    cards = "".join(card("/actividades/%s/" % x["slug"], x["img"], x["cat"], x["title"], x["short"], min_price(x)) for x in items)
    left = [block(t, prose(ps)) for t, ps in a["secciones"]]
    left.insert(1, block("Lugares imprescindibles", '<div class="two">%s</div>' % "".join('<div class="panel"><h3>%s</h3><p class="muted">%s</p></div>' % (e(n), e(dsc)) for n, dsc in a["lugares"])))
    left.append(block("Actividades guiadas en la zona", options_html(a["options"])))
    left.append(block("Preguntas frecuentes", faq_html(a["faq"])))
    form = book_form(a["title"], a["options"], 0, heading="Reserva tu actividad", opt_label="Actividad")
    body = (hero("Zonas · Guías Ad Astra", e(a["h1"]), e(a["lead"]), a["img"], [("Inicio", "/"), (a["title"], "")], '<a class="btn btn-primary" href="#reservar">Reservar actividad</a><a class="btn btn-ghost" href="#actividades">Ver actividades</a>') +
            keybar(a["keybar"]) +
            '<section class="section"><div class="wrap split"><div class="stack" style="gap:0">%s</div><div class="sticky">%s</div></div></section>' % ("".join(left), form) +
            '<section class="section alt" id="actividades"><div class="wrap"><div class="section-head"><p class="eyebrow">Más actividades cerca</p><h2>Aventura en la zona</h2></div><div class="grid c3">%s</div></div></section>' % cards)
    pl = dict(a["place_ld"]); pl["@context"] = "https://schema.org"; pl["description"] = a["seo_desc"]; pl["url"] = url(path); pl["image"] = a["img"]
    pl["containsPlace"] = [{"@type": "Place", "name": n} for n in pl.get("containsPlace", [])]
    offers = {"@context": "https://schema.org", "@type": "ItemList", "name": "Actividades guiadas: " + a["title"], "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": o["name"], "description": o["desc"], "provider": {"@id": D + "/#empresa"},
                                                       "offers": {"@type": "Offer", "price": o["price"], "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "url": url(path) + "#reservar"}}} for i, o in enumerate(a["options"])]}
    ld = [crumbs_ld([("Inicio", "/"), (a["title"], path)]), pl, offers, faq_ld(a["faq"]), {"@context": "https://schema.org", **ORG}]
    page(path, a["seo_title"], a["seo_desc"], body, "otr", ld, "article", a["img"], "0.8")

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
# Dibujos de línea del material de alquiler (SVG en línea, usan el color del texto)
_HELMET = '<path d="M8 30C8 18 16 11 24 11s16 7 16 19z"/><path d="M5 30h38"/><path d="M19 12v6M29 12v6M24 11v7"/><path d="M13 30q1 8 11 8t11-8"/>'
_SUIT = '<path d="M17 7l7 4 7-4 10 6-4 9-4-2v21H15V20l-4 2-4-9z"/><path d="M24 11v29"/><path d="M15 27h18"/>'
_HARNESS = '<path d="M7 15q17 9 34 0v6q-17 9-34 0z"/><ellipse cx="16" cy="33" rx="7" ry="5"/><ellipse cx="32" cy="33" rx="7" ry="5"/><path d="M21 25q3 6 6 0"/>'
_EIGHT = '<circle cx="24" cy="14" r="6"/><circle cx="24" cy="14" r="2.5"/><circle cx="24" cy="31" r="10"/><circle cx="24" cy="31" r="5"/>'
_LANYARD = '<rect x="20" y="5" width="8" height="12" rx="2"/><path d="M24 17q-8 8-11 18M24 17q8 8 11 18"/><path d="M10 35a3.5 5.5 0 1 0 7 0a3.5 5.5 0 1 0-7 0zM31 35a3.5 5.5 0 1 0 7 0a3.5 5.5 0 1 0-7 0z"/>'
RENT_ICON = {
    "casco": _HELMET,
    "neopreno": _SUIT,
    "equipo-barrancos": '<g transform="translate(-3 3) scale(.8)">' + _SUIT + '</g><g transform="translate(24 -2) scale(.5)">' + _HELMET + '</g>',
    "arnes-barrancos": '<g transform="translate(-2 0) scale(.82)">' + _HARNESS + '</g><path d="M20 26q8 2 14 12"/><g transform="translate(29 30) scale(.4)">' + _EIGHT + '</g>',
    "escarpines": '<path d="M13 9h11v18q0 3 3 4l11 3q4 1 4 5v2H12q-2 0-2-3v-8q3-4 3-10z"/><path d="M10 37h32"/><path d="M13 14h11"/>',
    "descensor": _EIGHT,
    "bidon": '<rect x="13" y="8" width="22" height="6" rx="2"/><rect x="15" y="14" width="18" height="27" rx="4"/><path d="M15 22h18M15 32h18"/>',
    "set-disipador": _LANYARD,
    "equipo-ferrata": '<g transform="translate(0 4) scale(.85)">' + _LANYARD + '</g><g transform="translate(25 -1) scale(.5)">' + _HELMET + '</g>',
    "arnes-escalada": _HARNESS,
    "piolet": '<path d="M15 42L32 11"/><path d="M26 9q9-2 17 5"/><path d="M26 9l-5-3-2 4"/><path d="M15 42l-2 4"/>',
    "crampones": '<path d="M6 24h34l5 4M40 24l6-2"/><path d="M9 24v7M15 24v7M21 24v7M27 24v7M33 24v7"/><path d="M12 24q0-11 12-11t12 11"/><path d="M18 13l-2 11M30 13l2 11"/>',
}
def rent_icon(rid):
    g = RENT_ICON.get(rid)
    if not g:
        return ""
    return '<svg class="rent-ico" viewBox="0 0 48 48" width="44" height="44" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % g

def build_rental():
    path = "/actividades/alquiler-material-montana/"
    cats = [("Barranquismo", "Material de barranquismo"), ("Vías ferratas", "Material de vía ferrata"), ("Escalada", "Material de escalada"), ("Alpinismo", "Material de alpinismo e invernal")]
    def row(r):
        return ('<tr class="rent-card%s" data-id="%s" data-name="%s" data-price="%d"><td><div class="rent-it">%s<div><b>%s</b><small>%s</small></div></div></td><td class="p">%d €</td>'
                '<td><div class="stepper" role="group" aria-label="Unidades de %s"><button type="button" data-step="-1" aria-label="Quitar una">−</button><input type="number" min="0" max="20" value="0" inputmode="numeric" aria-label="Unidades"><button type="button" data-step="1" aria-label="Añadir una">+</button></div></td></tr>'
                % (" hl" if r["id"].startswith("equipo") else "", r["id"], e(r["name"]), r["price"], rent_icon(r["id"]), e(r["name"]), e(r["desc"]), r["price"], e(r["name"])))
    tables = "".join(
        '<div class="rent-tbl"><h3>%s</h3><table><thead><tr><th>Material</th><th class="p">Precio/día</th><th class="u">Unidades</th></tr></thead><tbody>%s</tbody></table></div>'
        % (e(t), "".join(row(r) for r in sorted([r for r in RENTAL if c in r["cats"]], key=lambda r: (not r["id"].startswith("equipo"), -r["price"]))))
        for c, t in cats)
    puntos = "".join('<option>%s</option>' % b for b in RENTAL_PICKUP)
    body = (hero("Alquiler", "Alquiler de material de montaña y barranquismo", "Neoprenos, arneses, cascos, disipadores de ferrata, piolets y crampones. Precio por día con IVA incluido. Recogida en Fuentes de Béjar (Salamanca) o en Valladolid.",
                 img("e3722879-d648-4dbe-b361-b365f07e1692/otros-media-5.webp"), [("Inicio", "/"), ("Alquiler de material", "")], '<a class="btn btn-primary" href="#catalogo">Elegir material</a>') +
            keybar([("Precio", "Por unidad y día"), ("IVA", "Incluido"), ("Recogida", "Fuentes de Béjar · Valladolid"), ("Reserva", "Por WhatsApp en 1 minuto")]) +
            '<section class="section" id="catalogo"><div class="wrap" id="alquiler-app"><div class="section-head"><p class="eyebrow">Catálogo</p><h2>Elige fechas y unidades</h2><p class="muted">Indica el día de recogida y el de devolución, suma las unidades que necesitas y envíanos la solicitud por WhatsApp. Te confirmamos disponibilidad al momento.</p></div>'
            '<div class="datebar"><div class="field"><label for="r-desde">Recogida</label><input id="r-desde" type="date"></div><div class="field"><label for="r-hasta">Devolución</label><input id="r-hasta" type="date"></div>'
            '<div class="field"><span class="label">Días de alquiler</span><span class="days" id="r-dias">—</span></div><div class="field"><label for="r-punto">Recogida en</label><select id="r-punto">%s</select></div></div>'
            '<div class="rent-tables">%s</div></div></section>' % (puntos, tables) +
            '<section class="section alt"><div class="wrap"><div class="section-head"><p class="eyebrow">Cómo funciona</p><h2>Alquilar es así de fácil</h2></div><ol class="steps3">'
            '<li><h3>Elige fechas</h3><p>Día de recogida y de devolución. Si es un solo día, deja la devolución igual.</p></li>'
            '<li><h3>Suma unidades</h3><p>Pulsa + en cada material de la tabla. Verás el total estimado abajo.</p></li>'
            '<li><h3>Envía por WhatsApp</h3><p>Te confirmamos disponibilidad, tallas y punto de recogida. Pagas al recoger.</p></li></ol></div></section>'
            '<section class="section"><div class="wrap split"><div class="stack" style="gap:0">' +
            block("Material técnico revisado para cada actividad", prose([
                "Somos guías titulados y usamos este mismo material en nuestras actividades: lo revisamos después de cada uso y lo retiramos cuando toca. Todo está homologado para su uso.",
                "Para barranquismo tenemos neoprenos bipieza de 5 mm, escarpines de 3 mm, arneses específicos con culera y cabos de anclaje, descensores de ocho, bidones estancos y el equipo completo para que solo traigas bañador y toalla. Ideal para los barrancos de Gredos, el Valle del Jerte, las Arribes del Duero o León.",
                "Para vías ferratas alquilamos sets disipadores homologados, arneses y cascos: todo lo necesario para la ferrata del Cancho de la Muela en Candelario, las de Burgos o las de León.",
                "Para alpinismo y montaña invernal tenemos piolets de travesía y crampones de 12 puntas de correas, compatibles con cualquier bota. Perfectos para Gredos, Guadarrama o la Montaña Palentina en invierno.",
            ])) +
            block("Dónde recoger el material", '<div class="two"><div class="panel"><h3>Alquiler de material de montaña en Valladolid</h3><p class="muted">Recogida y devolución en Valladolid capital, con cita previa por WhatsApp. Ideal si vas a Picos de Europa, Palencia, León, Burgos o Gredos: crampones y piolet para invierno, equipo de vía ferrata (arnés, disipador y casco) y equipo completo de barranquismo.</p></div>'
                  '<div class="panel"><h3>Alquiler de material en Béjar, Candelario y Gredos (Salamanca)</h3><p class="muted">Recogida en Fuentes de Béjar, a pocos minutos de Béjar, Candelario, La Covatilla y la vía ferrata de La Muela. Perfecto para rutas invernales por la Sierra de Béjar y Gredos y para barrancos del Valle del Jerte y del Ambroz.</p></div></div>') +
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
        {"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": "Alquiler " + r["name"].lower(), "description": r["desc"], "image": r["img"], "serviceType": "Alquiler de material de " + r["cats"][0].lower(),
                                                       "provider": {"@id": D + "/#empresa"},
                                                       "offers": {"@type": "Offer", "price": r["price"], "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "businessFunction": "http://purl.org/goodrelations/v1#LeaseOut",
                                                                  "priceSpecification": {"@type": "UnitPriceSpecification", "price": r["price"], "priceCurrency": "EUR", "unitCode": "DAY", "valueAddedTaxIncluded": True}, "seller": {"@id": D + "/#empresa"}}}}
        for i, r in enumerate(RENTAL)]}
    svc = {"@context": "https://schema.org", "@type": "Service", "serviceType": "Alquiler de material de montaña, barranquismo, vías ferratas y alpinismo", "provider": {"@id": D + "/#empresa"},
           "areaServed": ["Salamanca", "Béjar", "Fuentes de Béjar", "Ávila", "Cáceres", "Valladolid", "Zamora", "Segovia"], "url": url(path)}
    ld = [crumbs_ld([("Inicio", "/"), ("Alquiler de material", path)]), items_ld, svc, faq_ld(RENTAL_FAQ), {"@context": "https://schema.org", **ORG}]
    page(path, "Alquiler de material de montaña y barranquismo | Salamanca y Valladolid",
         "Alquila neopreno, arnés, casco, set de vía ferrata, piolet y crampones desde %d €/día. Recogida en Fuentes de Béjar (Salamanca) o Valladolid. Reserva por WhatsApp." % precios.desde_alquiler(),
         body, "alq", ld, "website", img("e89d2f67-e4c0-4443-8f1f-9f4f13528f9f/otros-media-6.webp"), "0.9")

# ---------------------------------------------------------------- listados
def min_price(x):
    return min([o["price"] for o in x.get("options", []) if o.get("price")] or [x.get("price", 0)]) or 0

def build_activities_index():
    order = ["Barranquismo", "Vías ferratas", "Ascensiones", "Espeleología", "Escalada", "Senderismo", "Travesías", "Viajes", "Otros"]
    chips = '<button class="chip" data-val="" aria-pressed="true">Todas</button>' + "".join('<button class="chip" data-val="%s" aria-pressed="false">%s</button>' % (c, c) for c in order if c not in ("Travesías", "Viajes")).replace('<button class="chip" data-val="Otros"', '<button class="chip" data-val="Travesías y viajes" aria-pressed="false">Travesías y viajes</button><button class="chip" data-val="Otros"')
    secs = ""
    for c in order:
        items = [x for x in ACTIVITIES if x["cat"] == c]
        if c == "Otros":
            items = [{"slug": "alquiler-material-montana", "img": img("e3722879-d648-4dbe-b361-b365f07e1692/otros-media-5.webp"), "cat": "Otros", "title": "Alquiler de material", "short": "Neoprenos, arneses, cascos, disipadores, piolets y crampones por días."}] + items
        if not items:
            continue
        secs += '<section class="cat-section"><h2>%s</h2><div class="grid c3">%s</div></section>' % (c, "".join(card("/actividades/%s/" % x["slug"], x["img"], x["cat"], x["title"], x["short"], min_price(x), 'data-cat="%s"' % (c + "|Travesías y viajes" if c in ("Travesías", "Viajes") else c)) for x in items))
    body = (hero("Actividades", "Elige tu aventura", "Barranquismo, vías ferratas, espeleología, ascensiones, senderismo, escalada y viajes con guías titulados en Gredos, Castilla y León y el mundo.", HERO, [("Inicio", "/"), ("Actividades", "")]) +
            '<section class="section"><div class="wrap"><div class="chips" data-filter="#acts" data-key="cat" data-param="categoria" style="margin-bottom:36px">%s</div><div id="acts">%s</div></div></section>' % (chips, secs) +
            '<section class="section alt"><div class="wrap"><div class="section-head"><p class="eyebrow">Recorridos</p><h2>Barrancos, ferratas, cuevas y rutas</h2><p class="muted">Todos los recorridos que guiamos, con su precio y duración.</p></div><div class="two">%s</div></div></section>'
            % "".join('<a class="panel" href="%s" style="display:block"><h3>%s</h3><p class="muted">%s · %s · %d€</p></a>' % (p_, e(o["name"]), e(o["place"]), e(o["dur"]), o["price"]) for _, o, p_ in OPTION_PAGES))
    ld = [crumbs_ld([("Inicio", "/"), ("Actividades", "/actividades/")]), {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": url("/actividades/%s/" % x["slug"]), "name": x["title"]} for i, x in enumerate(ACTIVITIES)]}]
    page("/actividades/", "Actividades de aventura en Gredos y Castilla y León | Ad Astra", "Barranquismo, vías ferratas, espeleología, ascensiones, senderismo y viajes en Ávila, Salamanca, Cáceres, León, Palencia, Segovia y Burgos con guías titulados.", body, "act", ld, priority="0.9")

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
    page("/formacion-cursos/", "Cursos de montaña: barranquismo, escalada, alpinismo y ARVA", "Cursos de barranquismo, iniciación a la escalada, autorrescate, alpinismo y ARVA en Castilla y León con guías titulados. Consulta fechas y plazas.", body, "cur", ld, priority="0.9")

def build_calendar():
    body = (hero("Calendario", "Calendario de actividades", "Fechas confirmadas con plazas limitadas. Elige un día, reserva tu plaza y te escribimos por WhatsApp para confirmar.", img("41645da1-a007-4ff0-8526-61ca467dddb5/curso-arva.webp"), [("Inicio", "/"), ("Calendario", "")]) +
            '<section class="section"><div class="wrap"><div class="section-head" style="text-align:center"><h2>Calendario de actividades</h2><p class="muted">Consulta disponibilidad y reserva tu plaza. Los días en rojo están completos.</p></div>'
            '<div class="calx" data-calendar><div class="calx-cal"><div class="cal-nav"><button class="icon-btn" data-prev aria-label="Mes anterior">‹</button><h3 data-mtitle></h3><button class="icon-btn" data-next aria-label="Mes siguiente">›</button></div>'
            '<div class="cmonth" data-month></div><div class="legend calx-leg"><span><i class="ok"></i>Disponible</span><span><i class="low"></i>Últimas plazas</span><span><i class="full"></i>Completo</span></div></div>'
            '<div class="calx-day" data-day><p class="muted">Cargando fechas…</p></div></div></div></section>'
            '<section class="section alt"><div class="wrap two"><div class="panel"><h3>¿No ves tu fecha?</h3><p class="muted">Organizamos actividades para grupos en el día que elijas.</p><a class="btn btn-wa" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener">%s Pedir otra fecha</a></div>'
            '<div class="panel"><h3>Cómo funciona</h3>%s</div></div></section>' % (SITE["wa"], e("Hola, quería consultar fechas para una actividad."), WA_SVG,
                                                                                 ticks(["Elige un día marcado en el calendario.", "Pulsa «Reservar», indica cuántas plazas quieres, tu nombre y teléfono.", "Tu plaza queda apartada y se abre WhatsApp para confirmar contigo."])))
    page("/calendario/", "Calendario de cursos y actividades de montaña | Ad Astra", "Próximas fechas de cursos de barranquismo, alpinismo, escalada, ARVA y salidas guiadas en Gredos y Castilla y León. Consulta plazas libres y reserva online.", body, "cur",
         [crumbs_ld([("Inicio", "/"), ("Calendario", "/calendario/")])], priority="0.9")

def build_home():
    feat = ["barranquismo-avila", "via-ferrata-salamanca", "barranquismo-cueva-valporquero-sima-de-perlas", "ascensiones-montana", "boulder-zona-centro-salamanca-caceres", "monte-olimpo"]
    cards = "".join(card("/actividades/%s/" % x["slug"], x["img"], x["cat"], x["title"], x["short"], min_price(x)) for s in feat for x in ACTIVITIES if x["slug"] == s)
    ccards = "".join(card("/actividades/%s/" % c["slug"], c["img"], c["disc_label"], c["title"], c["short"], c["price"]) for c in COURSES[:3])
    tick = "".join("%s<em>✦</em>" % t for t in ["Barranquismo", "Vías ferratas", "Escalada", "Espeleología", "Ascensiones", "Trekking", "Cursos", "Viajes"] * 2)
    body = (hero("Hacia las estrellas · Vive la aventura", "Guías de montaña en Gredos y Castilla y León", "Barranquismo, vías ferratas, espeleología, senderismo, ascensiones, cursos y alquiler de material con guías titulados. Bases en Fuentes de Béjar (Salamanca) y Valladolid.", HERO, None,
                 '<a class="btn btn-primary" href="/actividades/">Reserva tu actividad</a><a class="btn btn-ghost" href="/calendario/">Calendario de cursos</a>', "home") +
            '<div class="ticker" aria-hidden="true"><div>%s</div></div>' % tick +
            '<section class="section"><div class="wrap"><div class="section-head row"><div><p class="eyebrow">Actividades destacadas</p><h2>Tu próxima aventura</h2></div><a class="btn btn-ghost" href="/actividades/">Ver todas</a></div><div class="grid c3">%s</div></div></section>' % cards +
            '<section class="section alt"><div class="wrap"><div class="stats"><div><b>+10</b><span>años guiando</span></div><div><b>8</b><span>provincias</span></div><div><b>100%%</b><span>guías titulados</span></div></div></div></section>'
            '<section class="section"><div class="wrap"><div class="section-head row"><div><p class="eyebrow">Formación</p><h2>Cursos de montaña</h2></div><a class="btn btn-ghost" href="/calendario/">Fechas y plazas</a></div><div class="grid c3">%s</div></div></section>' % ccards +
            '<section class="section alt"><div class="wrap about"><img src="%s" alt="Material de alquiler: neopreno de barranquismo" loading="lazy" style="background:#e9e6e2;object-fit:contain"><div style="display:grid;gap:18px"><p class="eyebrow">Alquiler de material</p><h2>Equípate para tu aventura</h2>'
            '<p class="lead">Neoprenos, arneses, cascos, disipadores, piolets y crampones desde %d € al día. Eliges fechas y unidades y nos lo envías por WhatsApp.</p><div><a class="btn btn-primary" href="/actividades/alquiler-material-montana/">Alquilar material</a></div></div></div></section>' % (img("e89d2f67-e4c0-4443-8f1f-9f4f13528f9f/otros-media-6.webp"), precios.desde_alquiler()) +
            '<section class="section"><div class="wrap about"><img src="%s" alt="Jairo Hernández, guía de montaña de Guías Ad Astra" loading="lazy"><div style="display:grid;gap:18px"><img class="about-logo" src="/img/logo-adastra-pin.png" width="120" height="160" alt="Logotipo de Guías Ad Astra, guías de montaña y aventura" loading="lazy"><p class="eyebrow">Quiénes somos</p><h2>Pasión por la montaña desde Gredos</h2>'
            '<p class="lead">Guías Ad Astra («hacia las estrellas», en latín) nace de la pasión de Jairo Hernández por la montaña y todos los deportes que en ella se pueden practicar.</p><div><a class="btn btn-ghost" href="/sobre-nosotros/">Conócenos</a></div></div></div></section>' % JAIRO +
            '<section class="section alt"><div class="wrap"><div class="section-head"><p class="eyebrow">Qué hacemos</p><h2>Empresa de turismo activo en Gredos, Salamanca, Ávila y Valladolid</h2></div><div class="prose" style="max-width:none;columns:2 340px;column-gap:48px">'
            '<p><strong>Guías Ad Astra</strong> es una empresa de turismo activo con guías de montaña titulados. Trabajamos desde Fuentes de Béjar, en la Sierra de Béjar y el oeste de Gredos, y desde Valladolid, y guiamos en Ávila, Salamanca, Cáceres, León, Palencia, Segovia, Burgos y Madrid.</p>'
            '<p>Hacemos <a href="/actividades/barranquismo-avila/">barranquismo en Gredos</a> (Arbillas, Río Mayor, Solana), <a href="/actividades/barranquismo-en-caceres/">barrancos del Valle del Jerte</a> como <a href="/actividades/barranquismo-en-caceres/barranco-de-los-papuos/">los Papúos</a>, la <a href="/actividades/barranquismo-cueva-valporquero-sima-de-perlas/">cueva de Valporquero</a> y barrancos en Salamanca, León, Palencia y Segovia.</p>'
            '<p>Guiamos <a href="/actividades/via-ferrata-salamanca/">la vía ferrata de La Muela en la Sierra de Béjar</a> y <a href="/actividades/vias-ferratas-leon/">vías ferratas en León</a> y <a href="/actividades/via-ferrata-burgos/">Burgos</a>, <a href="/actividades/senderismo-avila-gredos/">rutas de senderismo por Gredos</a>, <a href="/actividades/senderismo-salamanca/">Salamanca</a>, <a href="/actividades/senderismo-montana-palentina/">la Montaña Palentina</a> y <a href="/actividades/senderismo-valladolid/">Valladolid</a>, <a href="/actividades/ascensiones-montana/">ascensiones al Almanzor y otras cumbres</a> y <a href="/actividades/espeleologia-segovia/">espeleología</a>.</p>'
            '<p>Damos <a href="/formacion-cursos/">cursos de barranquismo, escalada, alpinismo, autorrescate y ARVA</a>, con fechas y plazas en el <a href="/calendario/">calendario</a>, y tenemos <a href="/actividades/alquiler-material-montana/">alquiler de material de montaña en Valladolid y Béjar</a>: neoprenos, equipos de vía ferrata, piolets y crampones.</p>'
            '</div></div></section>'
            '<section class="cta-band"><div class="wrap"><h2>Tu próxima cumbre te espera</h2><a class="btn" href="/calendario/">Ver fechas y reservar</a></div></section>')
    ld = [{"@context": "https://schema.org", **ORG}, {"@context": "https://schema.org", "@type": "WebSite", "name": "Guías Ad Astra", "url": D + "/", "inLanguage": "es"}]
    page("/", "Guías Ad Astra | Barranquismo, vías ferratas y montaña en Gredos", "Aventura guiada en Gredos y Castilla y León: barranquismo, vías ferratas, escalada, espeleología, cursos y alquiler de material con guías titulados.", body, "inicio", ld, priority="1.0")

def build_about():
    body = (hero("Nosotros", "Hacia las estrellas", "Pasión por la montaña desde la Sierra de Gredos.", JAIRO, [("Inicio", "/"), ("Sobre nosotros", "")]) +
            '<section class="section"><div class="wrap about"><img src="%s" alt="Jairo Hernández, fundador de Guías Ad Astra" loading="lazy"><div class="prose" style="font-size:1.1rem"><img class="about-logo" src="/img/logo-adastra-pin.png" width="120" height="160" alt="Logotipo de Guías Ad Astra, guías de montaña y aventura" loading="lazy">'
            '<p><strong>Guías Ad Astra</strong> («hacia las estrellas», en latín) nace de la pasión de Jairo Hernández por la montaña y por todos los deportes que en ella se pueden practicar.</p>'
            '<p>Diseñamos actividades en todos los ámbitos, adaptadas a cada nivel, para que vivas con nosotros una experiencia única: barrancos, ferratas, cuevas, cumbres, cursos de formación y viajes.</p>'
            '<p>Trabajamos desde nuestras bases de Fuentes de Béjar (Salamanca) y Valladolid, y guiamos en ocho provincias y fuera de España.</p>'
            '<p>Además organizamos eventos como la Ultra de Gredos, el Desafío Fuenterrico y las jornadas de voluntariado Gredos Limpio desde 2013.</p>'
            '<p><a class="btn btn-primary" href="/actividades/">Ver actividades</a></p></div></div></section>' % JAIRO)
    page("/sobre-nosotros/", "Sobre nosotros | Guías Ad Astra, guías de montaña en Gredos", "Jairo Hernández y el equipo de Guías Ad Astra: guías de montaña titulados en Gredos y Castilla y León, con actividades adaptadas a todos los niveles.", body, "nos",
         [crumbs_ld([("Inicio", "/"), ("Sobre nosotros", "/sobre-nosotros/")]), {"@context": "https://schema.org", "@type": "AboutPage", "name": "Sobre Guías Ad Astra", "url": url("/sobre-nosotros/"), "about": {"@id": D + "/#empresa"}}, {"@context": "https://schema.org", **ORG}], priority="0.5")

def build_contact():
    body = (hero("Contacto", "Hablemos de aventura", "Llámanos o escríbenos por WhatsApp para organizar tu actividad, curso o alquiler.", HERO, [("Inicio", "/"), ("Contacto", "")]) +
            '<section class="section"><div class="wrap contact-grid">'
            '<div class="panel"><p class="eyebrow">WhatsApp</p><b>%s</b><p class="muted">La forma más rápida de reservar.</p><a class="btn btn-wa" href="https://wa.me/%s" target="_blank" rel="noopener">%s Escribir</a></div>' % (SITE["phone"], SITE["wa"], WA_SVG) +
            '<div class="panel"><p class="eyebrow">Teléfono</p><b><a href="tel:%s" style="color:inherit">%s</a></b><p class="muted">%s</p></div>' % (SITE["phone_intl"], SITE["phone"], SITE["hours"]) +
            '<div class="panel"><p class="eyebrow">Email</p><b style="font-size:1.25rem"><a href="mailto:%s" style="color:inherit">%s</a></b></div>' % (SITE["email"], SITE["email"]) +
            '<div class="panel"><p class="eyebrow">Bases</p>%s</div></div></section>' % ticks(SITE["bases"]))
    page("/contacto/", "Contacto y reservas | Guías Ad Astra", "Contacta con Guías Ad Astra: 621 075 048 · WhatsApp · guiasadastra@gmail.com. Bases en Fuentes de Béjar (Salamanca) y Valladolid.", body, "con",
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
    page("/404", "Te has perdido en la montaña | Guías Ad Astra", "La página que buscas no existe o ha cambiado de sitio. Vuelve al inicio o explora nuestras actividades, cursos y alquiler de material de montaña.", body, "", noindex=True)


def build_calculator():
    path = "/calculadora-rutas/"
    faq = [
        ("¿Cómo se calcula el tiempo de una ruta de montaña con el MIDE?", "Se calcula por separado el tiempo por distancia (5 km/h en pistas, 4 km/h en sendas y 3 km/h en malas sendas) y por desnivel (400 m/h de subida y 600 m/h de bajada). La duración es el mayor de los dos más la mitad del menor. Es tiempo de marcha efectiva, sin paradas."),
        ("¿Qué tipo de camino elijo?", "Pistas para pistas forestales y carreteras; sendas para caminos de herradura, sendas lisas y prados; malas sendas para canchales, pedreras, cauces de ríos o sendas muy rotas. Si la ruta mezcla tipos, elige el que más abunde."),
        ("¿Qué es el esfuerzo MIDE?", "Es la valoración de 1 a 5 del esfuerzo necesario según las horas de marcha: 1 hasta 1 h, 2 de 1 a 3 h, 3 de 3 a 6 h, 4 de 6 a 10 h y 5 más de 10 h."),
        ("¿Por qué no se suman los dos tiempos?", "Porque mientras subes también avanzas. Sumarlos daría tiempos demasiado largos; quedarse con el mayor, demasiado cortos. Sumar la mitad del menor se ajusta bien a la realidad."),
        ("¿El tiempo incluye las paradas?", "No: el MIDE da tiempo de marcha efectiva. Se recomienda sumar entre un 10 % y un 20 % para descansos, hidratación e imprevistos; puedes elegirlo en «Margen para paradas»."),
        ("¿Qué archivos de track puedo subir?", "GPX (el más habitual en Wikiloc, Strava, Garmin, Komoot o Suunto), KML de Google Earth y TCX. El archivo se lee en tu propio móvil u ordenador: no se sube a ningún servidor."),
        ("¿Y si mi track no tiene altitudes?", "Muchos tracks dibujados a mano o exportados desde algunas apps no traen altitudes. En ese caso las calculamos automáticamente con un modelo digital del terreno, con una precisión aproximada de ±10 m, y obtienes igualmente el perfil y el desnivel."),
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
            '<div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center"><button type="button" class="btn btn-ghost" id="trk-demo" data-src="/data/ejemplo-laguna-grande.gpx">Probar con un ejemplo de Gredos</button><p class="err" id="trk-err" role="alert"></p></div><p id="trk-status" role="status" hidden></p>'
            '<div id="trk-res" hidden style="display:grid;gap:20px"><div class="trk-head"><h3 id="trk-name" style="font-size:2rem"></h3><a class="small" href="#calculadora">Cambiar ritmo ↑</a></div>'
            '<dl class="trk-stats" id="trk-stats"></dl><div><div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;align-items:center;margin-bottom:10px"><p class="label">Perfil de altitud · pasa el ratón para ver el punto en el mapa y pincha para fijarlo</p><button type="button" class="btn btn-ghost" id="trk-unpin" hidden style="padding:.55em .9em">Quitar punto fijado</button></div><div class="prof" id="trk-prof"></div></div>'
            '<div id="trk-map" hidden></div><p class="hint" id="trk-note"></p>'
            '<div class="dl-row"><span class="label">Descargar imagen</span><div style="display:flex;flex-wrap:wrap;gap:10px"><button type="button" class="btn btn-primary" data-dl="ficha">Ficha completa</button><button type="button" class="btn btn-ghost" data-dl="perfil">Perfil</button><button type="button" class="btn btn-ghost" data-dl="mapa">Mapa</button></div></div></div></div></section>' +
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
            '</div><div class="sticky"><div class="panel"><p class="eyebrow">¿Mejor con guía?</p><h3>Te llevamos nosotros</h3><p class="muted">Rutas guiadas por Gredos para todos los niveles, desde ' + str(precios.desde_slug("senderismo-avila-gredos")) + ' € por persona.</p>'
            '<a class="btn btn-primary" href="/actividades/senderismo-avila-gredos/">Senderismo en Gredos</a><a class="btn btn-ghost" href="/actividades/ascensiones-montana/">Ascensiones</a></div></div></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Calculadora de rutas", path)]), faq_ld(faq),
          {"@context": "https://schema.org", "@type": "WebApplication", "name": "Calculadora de rutas de montaña", "url": url(path), "applicationCategory": "TravelApplication", "operatingSystem": "Web",
           "description": "Calcula la duración de una ruta de senderismo o montaña a partir de distancia y desnivel, y analiza tracks GPX con perfil de altitud.", "offers": {"@type": "Offer", "price": 0, "priceCurrency": "EUR"},
           "provider": {"@id": D + "/#empresa"}}]
    head = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">'
    scripts = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin="" defer></script><script src="/js/calculadora.js" defer></script>'
    page(path, "Calculadora MIDE de tiempo de rutas y perfil GPX | Ad Astra",
         "Calcula gratis la duración de una ruta con el método MIDE según distancia y desnivel. Sube tu GPX y descarga el perfil, el mapa y la ficha de la ruta.",
         body, "her", ld, priority="0.8", head=head, scripts=scripts)


def build_topografia():
    path = "/topografia-barrancos/"
    faq = [
        ("¿Qué es la topografía de un barranco?", "Es el croquis del descenso: un perfil del cauce de arriba abajo con cada rápel, destrepe y tramo andando, su altura y su instalación. Es lo primero que se consulta para preparar un barranco y saber cuánta cuerda llevar."),
        ("¿Qué significan R, D y A?", "R es un rápel y el número son sus metros (R13 = rápel de 13 m). D es un destrepe, un paso que se baja sin cuerda o con ayuda (D3 = destrepe de 3 m). A es un tramo andando por el cauce, y solo se indica cuando es largo (A250 = 250 m andando)."),
        ("¿Cuánta cuerda necesito para un barranco?", "Como mínimo el doble del rápel más largo, porque la cuerda se monta doble para poder recuperarla desde abajo, más un par de metros de margen. La herramienta te lo calcula. Lleva siempre una cuerda de reserva."),
        ("¿Qué pongo en instalación y lado?", "La instalación es el tipo de anclaje de la cabecera (químicos, parabolt, spits o natural) y el lado indica dónde está mirando aguas abajo: izquierda, centro o derecha. Así aparece como en los croquis: «R13 - químicos, centro»."),
        ("¿Se guarda lo que hago?", "Sí, en tu propio navegador: si cierras la página y vuelves, la topografía sigue ahí. Con «Copiar enlace» puedes compartirla con quien quieras, y con las descargas la guardas en PNG o SVG."),
        ("¿Puedo usarla para mis propios barrancos?", "Claro. Es gratuita y no hace falta registrarse. Si quieres hacer el barranco con guía, también te llevamos nosotros."),
    ]
    body = (hero("Herramientas", "Topografía de barrancos", "Añade los tramos del barranco (rápeles, destrepes y tramos andando) y se dibuja la topografía al momento, lista para descargar y compartir.", img("8bb5ab91-bfa6-4c71-b8e0-37ba64a982bd/barranquismo-avila.webp"), [("Inicio", "/"), ("Topografía de barrancos", "")],
                 '<a class="btn btn-primary" href="#topo">Empezar</a><a class="btn btn-ghost" href="/calculadora-rutas/">Calculadora de rutas</a>') +
            '<section class="section" id="topo"><div class="wrap topo-grid">'
            '<div class="panel topo-ed"><p class="eyebrow">Datos del barranco</p>'
            '<div class="row2"><div class="field"><label for="topo-nombre">Nombre</label><input id="topo-nombre" placeholder="Barranco de…"></div><div class="field"><label for="topo-zona">Zona</label><input id="topo-zona" placeholder="Pueblo, provincia"></div></div>'
            '<div class="row2"><div class="field"><label for="topo-etq">Etiqueta de los rápeles</label><select id="topo-etq"><option value="metros">Metros (R13)</option><option value="numero">Número y metros (R1 · 13 m)</option><option value="federativo">Federativo (R1-13m-C)</option></select></div>'
            '<div style="display:grid;gap:8px;align-self:end"><label class="tp-chk"><input type="checkbox" id="topo-anc" checked> Dibujar anclaje y flecha</label><label class="tp-chk"><input type="checkbox" id="topo-ley" checked> Añadir leyenda</label></div></div><div class="tp-tools" style="gap:14px"><label class="tp-chk"><input type="checkbox" id="topo-pi"> Parking al inicio</label><label class="tp-chk"><input type="checkbox" id="topo-pf"> Parking al final</label></div>'
            '<p class="eyebrow" style="margin-top:8px">Tramos de arriba abajo</p><ol class="tp-list" id="topo-list"></ol>'
            '<div class="tp-add"><button type="button" class="btn btn-primary" data-add="r">+ Rápel</button><button type="button" class="btn btn-ghost" data-add="d">+ Destrepe</button><button type="button" class="btn btn-ghost" data-add="p">+ Pasamanos</button><button type="button" class="btn btn-ghost" data-add="a">+ Tramo andando</button></div>'
            '<div class="tp-tools"><button type="button" class="link-btn" id="topo-ejemplo">Cargar ejemplo</button><button type="button" class="link-btn" id="topo-nuevo">Empezar de cero</button></div></div>'
            '<div class="topo-out"><div class="topo-view" id="topo-svg" aria-live="polite"></div><dl class="trk-stats" id="topo-stats"></dl>'
            '<div class="dl-row"><span class="label">Descargar y compartir</span><div style="display:flex;flex-wrap:wrap;gap:10px"><button type="button" class="btn btn-primary" id="topo-png">PNG</button><button type="button" class="btn btn-ghost" id="topo-jpg">JPG</button><button type="button" class="btn btn-ghost" id="topo-svgdl">SVG</button><button type="button" class="btn btn-ghost" id="topo-link">Copiar enlace</button></div></div>'
            '<p class="hint" id="topo-msg" role="status"></p></div></div></section>' +
            '<section class="section alt"><div class="wrap split"><div class="stack" style="gap:0">' +
            block("Cómo se lee una topografía", prose([
                "Cada rápel lleva una R seguida de sus metros (R13 es un rápel de 13 m), con el anclaje dibujado arriba y una flecha que marca la bajada. Al lado se indica la instalación y el lado de la cabecera mirando aguas abajo: «R13 - químicos, centro».",
                "Los destrepes llevan una D y su altura (D3). Son pasos que se bajan sin cuerda o con una cuerda de ayuda. Los pasamanos con cuerda fija llevan Pc y su longitud.",
                "Con el formato federativo las etiquetas siguen el orden de cada tipo y el lado de la instalación mirando aguas abajo: R1-7m-C es el primer rápel, de 7 m, con la cabecera en el centro; d2-3m es el segundo destrepe; Pc1-2m-C el primer pasamanos. I es izquierda, C centro y D derecha.",
                "Los anclajes se dibujan con una X: X es parabolt, Xs spits y Xq químicos; el anclaje natural, con un círculo. Si hay dos anclajes, debajo se dibuja si están unidos por cadena o por cordino. El rápel destrepable lleva una insignia morada, el punto sin retorno una señal de prohibido y el parking una P. La leyenda de la imagen recoge solo los símbolos que has usado.",
                "Los tramos andando por el cauce no llevan nada, salvo los largos, que llevan una A y la distancia (A250). Si un rápel acaba en una poza, se dibuja en azul; si en la poza hay un remolino se marca con una espiral, y cualquier peligro o incidencia (un rebufo, un sifón, un tronco atascado…) con una señal de exclamación y una nota.",
                "Para saber cuánta cuerda llevar, cuenta el doble del rápel más largo: la herramienta te lo calcula. Lleva siempre una cuerda de reserva y revisa el estado de las instalaciones antes de colgarte."])) +
            block("Preguntas frecuentes", faq_html(faq)) +
            '</div><div class="sticky"><div class="panel"><p class="eyebrow">¿Mejor con guía?</p><h3>Barrancos guiados</h3><p class="muted">Ponemos el material, el seguro y la experiencia. Desde ' + str(precios.desde_cat("Barranquismo")) + ' € por persona.</p>'
            '<a class="btn btn-primary" href="/actividades/barranquismo-avila/">Barranquismo en Gredos</a><a class="btn btn-ghost" href="/actividades/curso-barranquismo/">Curso de barranquismo</a></div></div></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Topografía de barrancos", path)]), faq_ld(faq),
          {"@context": "https://schema.org", "@type": "WebApplication", "name": "Topografía de barrancos", "url": url(path), "applicationCategory": "DesignApplication", "operatingSystem": "Web",
           "description": "Dibuja la topografía de un barranco añadiendo rápeles, destrepes y tramos andando. Calcula la cuerda necesaria y descarga el croquis en PNG o SVG.",
           "offers": {"@type": "Offer", "price": 0, "priceCurrency": "EUR"}, "provider": {"@id": D + "/#empresa"}}]
    page(path, "Topografía de barrancos: croquis de rápeles | Ad Astra",
         "Crea gratis la topografía de un barranco: añade rápeles (R), destrepes (D) y tramos andando, calcula la cuerda necesaria y descarga el croquis en PNG o JPG.",
         body, "her", ld, priority="0.7", scripts='<script src="/js/topografia.js" defer></script>')

# ---------------------------------------------------------------- meteorología de montaña
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "meteo"))
from macizos import MACIZOS, REGIONES, WEBCAMS  # noqa: E402

METEO_IMG = img("0c5376bd-2231-4c62-b798-6f0139e73cd7/cursos-alpinismo.webp")
METEO_ACT = {
    "gredos-macizo-central": ["senderismo-avila-gredos", "ascensiones-montana", "barranquismo-avila"],
    "gredos-macizo-oriental": ["barranquismo-avila", "senderismo-avila-gredos"],
    "sierra-de-candelario": ["via-ferrata-salamanca", "senderismo-salamanca", "barranquismo-salamanca", "comarca-natural-oeste-de-gredos"],
    "sierra-del-barco": ["senderismo-avila-gredos", "ascensiones-montana", "barranquismo-avila"],
    "los-galayos": ["barranquismo-avila", "ascensiones-montana", "senderismo-avila-gredos"],
    "valle-del-jerte": ["barranquismo-en-caceres", "senderismo-salamanca", "via-ferrata-salamanca"],
    "sierra-de-francia": ["boulder-zona-centro-salamanca-caceres", "barranquismo-salamanca"],
    "las-quilamas": ["barranquismo-salamanca", "via-ferrata-salamanca"],
    "guadarrama": ["barranquismo-madrid-segovia", "espeleologia-segovia", "cursos-alpinismo"],
    "ayllon": ["barranquismo-madrid-segovia", "espeleologia-segovia"],
    "picos-de-europa": ["ascensiones-montana", "vias-ferratas-leon"],
    "montanas-de-leon": ["barranquismo-cueva-valporquero-sima-de-perlas", "vias-ferratas-leon", "barranquismo-leon"],
    "puerto-de-san-isidro": ["vias-ferratas-leon", "barranquismo-leon", "barranquismo-cueva-valporquero-sima-de-perlas"],
    "puerto-de-san-glorio": ["ascensiones-montana", "senderismo-montana-palentina", "vias-ferratas-leon"],
    "alto-campoo": ["senderismo-montana-palentina", "barranquismo-palencia", "boulder-las-tuerces"],
    "sierra-de-tonda": ["senderismo-salamanca", "via-ferrata-salamanca", "barranquismo-salamanca"],
    "macizo-de-ubina": ["vias-ferratas-leon", "barranquismo-leon", "ascensiones-montana"],
    "pirineo-navarro": ["ascensiones-montana"],
    "montana-palentina": ["senderismo-montana-palentina", "barranquismo-palencia", "boulder-las-tuerces", "ascensiones-montana"],
    "ordesa-monte-perdido": ["ascensiones-montana", "cursos-alpinismo"],
    "aneto-posets": ["ascensiones-montana", "cursos-alpinismo"],
    "aiguestortes-carros-de-foc": ["trekking-carros-de-foc", "ascensiones-montana"],
    "sierra-nevada": ["ascensiones-montana", "cursos-alpinismo"],
}
METEO_FAQ = [
    ("¿De dónde salen estos datos?", "De los propios modelos meteorológicos, no de otras webs del tiempo: ECMWF IFS (Centro Europeo, 9 km), GFS (servicio meteorológico de EE. UU., 25 km), ICON-EU (servicio alemán, 6,5 km) y AROME (Météo-France, 2,5 km, el de alta resolución para viento y tormentas en las primeras 51 horas). Cada 6 horas descargamos su última pasada y calculamos la previsión de cada macizo."),
    ("¿Qué diferencia hay entre la cumbre y la base?", "La base es el pueblo o punto de partida habitual, con la temperatura a 2 metros corregida a su altitud. La cumbre es la cima de referencia del macizo: la temperatura y el viento se calculan en la vertical, a su altitud real, con los datos del modelo en altura (850, 700, 600 y 500 hPa). Es lo que vas a encontrar arriba, no en el valle."),
    ("¿Qué es la isocero y la cota de nieve?", "La isocero es la altitud a la que la temperatura del aire es 0 °C. La cota de nieve suele estar unos 300 metros por debajo: por encima de ella, si precipita, lo hace en forma de nieve. ICON-EU la calcula directamente y en los demás modelos se estima a partir de la isocero."),
    ("¿Por qué se muestran varios modelos?", "Porque ningún modelo acierta siempre. Mostramos la mediana de los tres como previsión principal y cada modelo por separado en las gráficas y en la comparación. Si coinciden, la previsión es fiable; si discrepan mucho, hay incertidumbre y conviene tener un plan B."),
    ("¿Cómo se calcula el riesgo de tormenta?", "Con la energía disponible para la convección (CAPE) y la precipitación prevista en el mismo tramo de 3 horas. Si un modelo lo marca, la tormenta es posible; si lo marcan dos o más, probable. En verano, las tormentas de montaña suelen formarse por la tarde: madruga y planifica estar fuera de las cumbres a mediodía."),
    ("¿Sustituye a los avisos oficiales?", "No. Es una previsión automática para planificar actividades. Consulta siempre los avisos de AEMET y el boletín de peligro de aludes en invierno, y ante la duda, no subas."),
]

def meteo_metodo():
    return block("Cómo se hace esta previsión", prose([
        "Cada 6 horas un proceso automático descarga la última pasada de cuatro modelos meteorológicos: ECMWF IFS (Centro Europeo de Previsión a Plazo Medio, el de referencia en Europa), GFS (NOAA, Estados Unidos), ICON-EU (DWD, servicio meteorológico alemán, con más resolución pero solo a 5 días) y AROME (Météo-France, 2,5 km). AROME es de la misma familia que el HARMONIE-AROME de AEMET: con una rejilla tan fina ve bien el relieve, por eso es el más fiable para el viento en cordales y collados, pero solo llega a 51 horas y no cubre Sierra Nevada.",
        "Hasta el día 7 la previsión combina los cuatro modelos (o los tres de mayor alcance); del día 8 al 10, ECMWF y GFS; y del 11 al 15 solo GFS, que es el único modelo libre que llega tan lejos. Por eso esos últimos días se marcan como «tendencia»: sirven para ver si viene un cambio de tiempo, no para planificar a la hora.",
        "En la cumbre, el viento de AROME es el viento real a 10 metros sobre el relieve del modelo; el de los otros tres es el viento en atmósfera libre a la altitud de la cima, que suele ser algo más fuerte. Con los cuatro tienes el rango completo.",
        "Para cada macizo calculamos dos puntos. En la cumbre, la temperatura y el viento se interpolan en la vertical entre el suelo del modelo y los niveles de 925, 850, 700, 600 y 500 hPa, a la altitud real de la cima: así se evita el error típico de las previsiones por municipio, que dan el tiempo del pueblo. En la base, la temperatura a 2 metros se corrige a la altitud del pueblo.",
        "La previsión principal es la mediana de los modelos disponibles. En las gráficas y en la comparación verás cada modelo por separado: cuanto más se parezcan, más fiable es la previsión.",
        "Datos: ECMWF (CC BY 4.0), NOAA/NCEP GFS (dominio público), DWD ICON-EU (CC BY 4.0) y Météo-France AROME (Licence Ouverte Etalab 2.0). Previsión elaborada por Guías Ad Astra. Es orientativa: consulta también los avisos de AEMET."]))

def meteo_selector(sel=None):
    """Desplegables cordillera -> sierra/macizo; meteo.js carga la previsión en la misma página."""
    reg_sel = next((m["region"] for m in MACIZOS if m["id"] == sel), "")
    lista = [{"id": m["id"], "nombre": m["nombre"], "corto": m["corto"], "region": m["region"],
              "cumbre": "%s %s m" % (m["cumbre"]["nombre"], "{:,}".format(m["cumbre"]["alt"]).replace(",", ".")),
              "base": "%s %s m" % (m["base"]["nombre"], "{:,}".format(m["base"]["alt"]).replace(",", ".")),
              "cams": WEBCAMS.get(m["id"], {})} for m in MACIZOS]
    ops_reg = '<option value="">Todas</option>' + "".join('<option%s>%s</option>' % (' selected' if rg == reg_sel else "", e(rg)) for rg in REGIONES)
    ops_mac = '<option value="">Todas las sierras</option>' + "".join(
        '<option value="%s"%s>%s</option>' % (m["id"], ' selected' if m["id"] == sel else "", e(m["nombre"])) for m in MACIZOS if not reg_sel or m["region"] == reg_sel)
    return ('<form class="mt-selbar" id="mt-selbar" action="/meteo/" onsubmit="return false">'
            '<label><span>Cordillera</span><select id="mt-reg" aria-label="Cordillera">%s</select></label>'
            '<label><span>Sierra o macizo</span><select id="mt-sel" aria-label="Sierra o macizo">%s</select></label></form>'
            '<script type="application/json" id="mt-lista">%s</script>') % (ops_reg, ops_mac, json.dumps(lista, ensure_ascii=False).replace("</", "<\\/"))

CAUDAL_FAQ = [
    ("¿De dónde salen los caudales?", "De los aforos oficiales de las confederaciones hidrográficas: el SAIH Tajo para el Valle del Jerte y el SAIH Duero para León y Palencia. Son datos en tiempo real y provisionales: a veces un aforo deja de enviar datos o da un valor erróneo."),
    ("¿Qué significa cada color?", "Lo marcan nuestros guías según su experiencia en cada barranco: verde, caudal bueno; amarillo, poco caudal; naranja, caudal alto, solo con experiencia y mucho cuidado; rojo, no recomendable. Donde todavía no hay umbrales se muestra solo el caudal y su tendencia."),
    ("¿Por qué se mira un aforo que no está en el propio barranco?", "Casi ningún barranco tiene aforo propio. Se usa el del río principal más cercano, que sube y baja a la vez que el barranco: lo importante es comparar con los valores con los que el guía conoce el barranco."),
    ("¿Sirve para decidir si entro?", "Es una ayuda, no una garantía. Una tormenta puede subir el caudal en minutos y el aforo puede tardar en reflejarlo. Mira también la previsión de lluvia y, ante la duda, no entres. Con nuestros guías la decisión se toma en el sitio."),
]


NIEVE_FAQ = [
    ("¿Cómo se calcula el estado de la nieve?", "Con los mismos modelos de nuestra página de meteorología (ECMWF, GFS, ICON y AROME). Guardamos lo que ha pasado en los últimos días y lo juntamos con la previsión de los próximos tres: nieve nueva en cumbre, viento después de las nevadas, días de deshielo seguidos de noches de helada, lluvia sobre la nieve e isocero. Con eso estimamos qué tipo de nieve vas a encontrar."),
    ("¿Es un boletín de aludes?", "No. Es una estimación orientativa hecha con modelos meteorológicos, sin observaciones de campo ni sondeos del manto. Donde existe un boletín oficial de peligro de aludes (Pirineo), enlazamos el boletín, que es el que manda."),
    ("¿Por qué el espesor del manto parece bajo?", "Los modelos calculan la nieve en su punto de rejilla, que está a menos altura que la cumbre real y no ve ventisqueros ni canales. Úsalo para comparar días y zonas, no como medida exacta."),
    ("¿Qué significa costra de rehielo?", "Cuando de día se funde la capa superficial y de noche vuelve a helar, a primera hora la nieve está dura como el hielo: hacen falta crampones y piolet y una caída no se para fácilmente. Con el sol se va ablandando, antes en las solanas."),
]


def build_nieve():
    path = "/nieve/"
    cams = json.dumps({k: v for k, v in WEBCAMS.items()}, ensure_ascii=False).replace("</", "<\\/")
    body = (hero("Herramientas", "Estado de la nieve", "Estimación del estado de la nieve en %d macizos: nieve reciente y prevista, placas de viento, costra de rehielo y nieve húmeda, calculada con los modelos meteorológicos y los datos de los últimos días." % len(MACIZOS), METEO_IMG,
                 [("Inicio", "/"), ("Estado de la nieve", "")], '<a class="btn btn-primary" href="#estado">Ver el estado</a><a class="btn btn-ghost" href="/meteo/">Meteorología</a>') +
            '<section class="section" id="estado"><div class="wrap"><div id="nv-lista" class="nv"><p class="mt-cargando">Cargando el estado de la nieve…</p></div></div></section>'
            '<script type="application/json" id="nv-cams">' + cams + '</script>' +
            '<section class="section alt"><div class="wrap split"><div class="stack" style="gap:0">' + block("Preguntas frecuentes", faq_html(NIEVE_FAQ)) +
            '</div><div class="sticky"><div class="panel"><p class="eyebrow">Importante</p><p>Esto no es un boletín de peligro de aludes. Consulta siempre el boletín oficial donde lo haya, valora el terreno y la nieve sobre el sitio y lleva el material adecuado (ARVA, pala y sonda en terreno de aludes).</p><p><a href="/como-leer-la-nieve-y-los-aludes/">Cómo leer la nieve y el peligro de aludes →</a></p></div></div></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Estado de la nieve", path)]), faq_ld(NIEVE_FAQ)]
    ld.append(app_ld(path, "Estado de la nieve por macizo", "Estimación diaria del estado de la nieve: nieve reciente, placas de viento, costras y nieve húmeda."))
    page(path, "Estado de la nieve hoy en Gredos, Picos y Pirineos | Ad Astra",
         "Estado de la nieve por macizo: nieve reciente y prevista, placas de viento, costras y nieve húmeda en Gredos, Guadarrama, Picos, Pirineos y Sierra Nevada.",
         body, "her", ld, priority="0.6", scripts='<script src="/js/nieve.js" defer></script>')


import guias_svg  # noqa: E402

MOCHILA_FAQ = [
    ("¿Dónde va lo más pesado de la mochila?", "Pegado a la espalda y centrado, entre los omóplatos. Así el centro de gravedad queda cerca del tuyo y la mochila no tira hacia atrás. En terreno técnico (trepadas, nieve, barrancos) bájalo un poco, a la altura de la mitad de la espalda: pierdes algo de comodidad pero ganas mucho equilibrio."),
    ("¿Qué peso es razonable llevar?", "Como orientación, no más del 20 % de tu peso en travesías con vivac y bastante menos en una salida de un día. Cada kilo de más se nota en las rodillas en la bajada: revisa la lista y quita lo que no vayas a usar."),
    ("¿En qué orden se ajustan las correas?", "Con la mochila cargada: primero el cinturón sobre las crestas de la cadera, que debe llevar la mayor parte del peso; después las hombreras; luego los tensores de carga (las cintas de encima de los hombros, a unos 45°) y por último la correa de pecho. Al final, cierra los compresores laterales para que nada baile."),
]

CAPAS_FAQ = [
    ("¿Por qué no se debe llevar algodón en la montaña?", "Porque absorbe el sudor y tarda mucho en secarse. Mientras andas no lo notas, pero en cuanto paras o sopla el viento esa humedad pegada a la piel te enfría muy rápido. Para la capa base usa fibras sintéticas o lana merina."),
    ("¿Plumón o fibra sintética?", "El plumón abriga más con menos peso y se comprime mejor, pero mojado pierde casi todo su abrigo. La fibra sintética abriga algo menos y pesa más, pero sigue abrigando húmeda. Para lluvia, barrancos o mucho sudor, fibra; para frío seco y paradas, plumón."),
    ("¿Hace falta una chaqueta de membrana si hace buen tiempo?", "En montaña el tiempo cambia rápido y arriba siempre hace más frío y viento. Una chaqueta impermeable ligera pesa poco y es lo que te protege si te pilla una tormenta: llévala siempre en la mochila."),
    ("¿Cómo se aplica a las piernas, las manos y la cabeza?", "Igual pero más simple: unas mallas térmicas bajo el pantalón si hace frío, y cubrepantalón impermeable con lluvia o nieve. En manos, guantes finos más unos gordos o manoplas encima. En la cabeza, buff y gorro: por ahí se pierde mucho calor."),
]


COMIC_FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bangers&family=Comic+Neue:wght@700&display=swap">'


ZONAS_MOCHILA = [
    ("#b48be0", "5", "Tapa:", "lo pequeño y a mano", "frontal, mapa, crema, navaja"),
    ("#7cc47f", "4", "Arriba:", "lo que usas a menudo", "chubasquero, botiquín, comida del día"),
    ("#e8574a", "2", "Pegado a la espalda:", "lo más pesado", "agua, cuerda, hornillo, comida"),
    ("#e9a53b", "3", "Hacia fuera:", "peso medio", "ropa de abrigo, tienda, neopreno"),
    ("#4f8fd6", "1", "Abajo:", "ligero y voluminoso", "saco de dormir, ropa de recambio"),
    ("#bfb3a3", "6", "Todo el bulto:", "compacto y ceñido", "que no pase de la cabeza ni cuelgue bajo la cadera; fuera, solo bastones o piolet"),
]


def build_mochila():
    path = "/como-preparar-la-mochila/"
    ajustes = [("Cinturón", "Ponlo sobre las crestas de la cadera y apriétalo: ahí debe ir la mayor parte del peso."),
               ("Hombreras", "Ajústalas para que abracen el hombro sin cargar el peso sobre él."),
               ("Tensores de carga", "Las cintas de encima de los hombros, a unos 45°: acercan la parte de arriba de la mochila a la espalda."),
               ("Correa de pecho", "A la altura del esternón, sin que te apriete al respirar: estabiliza las hombreras."),
               ("Compresores", "Ciérralos para que la carga no se mueva. Ajusta el cinturón otra vez al empezar a andar.")]
    reglas = ["Lo más pesado, pegado a la espalda y centrado: el centro de gravedad cerca del tuyo.",
              "En terreno técnico (trepadas, nieve, barrancos) baja un poco esa carga para ganar equilibrio.",
              "Abajo, lo ligero y voluminoso que no vas a necesitar hasta la noche: saco, ropa de recambio.",
              "Arriba y en la tapa, lo que usas durante el día: chubasquero, botiquín, frontal, mapa.",
              "Reparte el peso igual a derecha e izquierda y rellena huecos para que nada se mueva.",
              "Por fuera, lo mínimo: todo lo que cuelga se engancha, se moja y desequilibra."]
    body = (hero("Artículos", "Cómo preparar la mochila", "Cómo repartir el peso para que la mochila no te tire hacia atrás, cómo ajustarla y una lista para cada actividad que vas tachando mientras la preparas.", img("afe67801-cf88-4cef-a3ac-e25e4e971634/senderismo-avila-gredos.webp"),
                 [("Inicio", "/"), ("Artículos", "/articulos/"), ("Cómo preparar la mochila", "")], '<a class="btn btn-primary" href="/lista-material-montana/">Lista de material</a><a class="btn btn-ghost" href="/teoria-de-las-capas/">Teoría de las capas</a>') +
            '<section class="section"><div class="wrap"><p class="eyebrow">El reparto del peso</p><h2>Lo pesado, pegado a la espalda</h2>'
            '<div class="gd-zonas"><figure><img src="/img/guias/mochila-zonas.webp" width="569" height="994" loading="lazy" alt="Senderista con la mochila abierta en corte: cada zona con su material y el centro de gravedad pegado a la espalda"></figure>'
            '<ol class="gd-ley">' + "".join('<li style="--c:%s"><span>%s</span><div><b>%s</b> %s<small>%s</small></div></li>' % z for z in ZONAS_MOCHILA) + '</ol></div>'
            '<ul class="gd-reglas">' + "".join("<li>%s</li>" % e(x) for x in reglas) + '</ul>'
            '<div class="gd-bm"><figure class="ok"><img src="/img/guias/mochila-bien.webp" width="403" height="994" loading="lazy" alt="Bien: mochila pegada a la espalda, la vertical del peso cae sobre los pies"><figcaption><b>Bien:</b> peso pegado y centrado. La vertical del peso cae sobre los pies.</figcaption></figure>'
            '<figure class="ko"><img src="/img/guias/mochila-mal.webp" width="506" height="994" loading="lazy" alt="Mal: mochila alejada de la espalda y alta, tira hacia atrás"><figcaption><b>Mal:</b> peso lejos y alto. Tira hacia atrás y obliga a encorvarse.</figcaption></figure></div></div></section>'
            '<section class="section alt"><div class="wrap"><p class="eyebrow">El ajuste</p><h2>En este orden, con la mochila cargada</h2><ol class="gd-pasos">' +
            "".join('<li><b>%s</b><span>%s</span></li>' % (e(a), e(b)) for a, b in ajustes) + '</ol></div></section>'
            '<section class="section" id="lista"><div class="wrap"><div class="panel lista-cta"><div><p class="eyebrow">Qué llevar</p><h2>Lista de material por actividad</h2>'
            '<p>Barrancos, escalada deportiva y clásica, alpinismo, senderismo, montañismo y vivac: elige la actividad y ve tachando lo que ya has metido en la mochila. Se guarda en tu navegador y la puedes imprimir.</p></div>'
            '<a class="btn btn-primary" href="/lista-material-montana/">Abrir la lista de material</a></div></div></section>' +
            '<section class="section alt"><div class="wrap split"><div class="stack" style="gap:0">' + block("Preguntas frecuentes", faq_html(MOCHILA_FAQ)) +
            '</div><div class="sticky"><div class="panel"><p class="eyebrow">Con guía</p><p>En nuestras actividades te decimos qué traer y ponemos el material técnico. Si te falta algo, también lo <a href="/actividades/alquiler-material-montana/">alquilamos</a>.</p></div></div></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Artículos", "/articulos/"), ("Cómo preparar la mochila", path)]), faq_ld([x for x in MOCHILA_FAQ if "lista" not in x[0]]),
          articulo_ld(path, "Cómo preparar la mochila de montaña", "Dónde va cada cosa en la mochila, cómo repartir el peso y cómo ajustarla, con ilustraciones.", "2026-11-18")]
    page(path, "Cómo preparar la mochila de montaña | Ad Astra",
         "Dónde va cada cosa en la mochila, por qué lo pesado va pegado a la espalda y cómo ajustar las correas, con ilustraciones. Y la lista de material por actividad.",
         body, "art", ld, priority="0.6", scripts=COMIC_FONTS)


LISTA_FAQ = [
    ("¿Se guarda lo que marco?", "Sí, en tu propio navegador: si cierras la página y vuelves, lo marcado sigue ahí. Cada actividad tiene su lista por separado, y con «Desmarcar todo» empiezas de cero para la siguiente salida."),
    ("¿Puedo añadir cosas mías?", "Sí: escribe abajo lo que quieras añadir y se queda en la lista de esa actividad. Lo que añadas también se guarda en tu navegador y lo puedes quitar con la ×."),
    ("¿La puedo imprimir?", "Sí, con el botón «Imprimir la lista». Sale limpia, sin menús, para que la taches a boli."),
    ("¿Qué actividades tiene?", "Barrancos, escalada deportiva, escalada clásica, alpinismo, senderismo, montañismo y vivac. A todas se les suma lo básico de seguridad, comida y agua que hay que llevar siempre."),
    ("¿Lleváis vosotros el material técnico en las actividades guiadas?", "Sí: en nuestras actividades ponemos el material técnico (cuerdas, arneses, cascos, neoprenos…) y te decimos qué traer. Si quieres salir por tu cuenta, también alquilamos material."),
]


def build_lista_material():
    path = "/lista-material-montana/"
    body = (hero("Herramientas", "Lista de material de montaña", "Qué llevar en la mochila según la actividad: elige barrancos, escalada, alpinismo, senderismo, montañismo o vivac y ve tachando lo que ya tienes preparado.", img("afe67801-cf88-4cef-a3ac-e25e4e971634/senderismo-avila-gredos.webp"),
                 [("Inicio", "/"), ("Herramientas", "/herramientas/"), ("Lista de material", "")]) +
            '<section class="section" id="lista"><div class="wrap"><div id="mo-app" class="mo"><p class="muted">Cargando la lista…</p></div></div></section>'
            '<section class="section alt"><div class="wrap split"><div class="stack" style="gap:0">' + block("Preguntas frecuentes", faq_html(LISTA_FAQ)) +
            '</div><div class="sticky"><div class="panel"><p class="eyebrow">Antes de cargarla</p><p>Lo que llevas importa tanto como dónde lo metes: lo pesado, pegado a la espalda. Lo explicamos con dibujos en <a href="/como-preparar-la-mochila/">cómo preparar la mochila</a>, y qué ropa ponerte en <a href="/teoria-de-las-capas/">la teoría de las capas</a>.</p>'
            '<p>¿Te falta algo? <a href="/actividades/alquiler-material-montana/">Alquilamos material</a> en Valladolid y Béjar.</p></div></div></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Herramientas", "/herramientas/"), ("Lista de material", path)]), faq_ld(LISTA_FAQ),
          app_ld(path, "Lista de material de montaña", "Listas de material para barrancos, escalada, alpinismo, senderismo, montañismo y vivac para ir tachando.")]
    page(path, "Lista de material de montaña por actividad | Ad Astra",
         "Qué llevar a la montaña: listas de material para barrancos, escalada, alpinismo, senderismo, montañismo y vivac que vas tachando. Gratis e imprimible.",
         body, "her", ld, priority="0.7", scripts='<script src="/js/mochila.js" defer></script>')


HER_ICO = {k: '<svg viewBox="0 0 64 64" aria-hidden="true">%s</svg>' % v for k, v in {
    "meteo": '<circle cx="24" cy="24" r="10" fill="#f5c84b"/><path d="M18 46h28a9 9 0 0 0 0-18 13 13 0 0 0-25 3 8 8 0 0 0-3 15z" fill="#e8eef3"/>',
    "nieve": '<g stroke="#bfe0f7" stroke-width="4" stroke-linecap="round"><path d="M32 8v48M11 20l42 24M11 44l42-24"/></g>',
    "caudal": '<path d="M6 30q8-8 16 0t16 0 16 0M6 42q8-8 16 0t16 0 16 0" fill="none" stroke="#6fb3e0" stroke-width="5" stroke-linecap="round"/>',
    "calc": '<rect x="14" y="8" width="36" height="48" rx="6" fill="#e9a53b"/><rect x="20" y="14" width="24" height="10" rx="2" fill="#1b120c"/><g fill="#1b120c"><circle cx="24" cy="34" r="3"/><circle cx="32" cy="34" r="3"/><circle cx="40" cy="34" r="3"/><circle cx="24" cy="44" r="3"/><circle cx="32" cy="44" r="3"/><circle cx="40" cy="44" r="3"/></g>',
    "gpx": '<path d="M10 50 L24 26 L34 38 L54 12" fill="none" stroke="#4fb3e8" stroke-width="5" stroke-linejoin="round"/><circle cx="10" cy="50" r="5" fill="#3fae5a"/><circle cx="54" cy="12" r="5" fill="#e8574a"/>',
    "video": '<path d="M4 50 L22 22 L32 34 L44 14 L60 50Z" fill="#6b5a4a"/><path d="M44 14 L50 26 L44 23 L40 27Z" fill="#fff"/><circle cx="48" cy="48" r="12" fill="#e8574a"/><path d="M45 42v12l10-6z" fill="#fff"/>',
    "lista": '<rect x="14" y="8" width="36" height="48" rx="5" fill="#f3e9df"/><g stroke="#7cc47f" stroke-width="4" fill="none" stroke-linecap="round"><path d="M20 22l4 4 7-8M20 38l4 4 7-8"/></g><g stroke="#8a7564" stroke-width="3"><path d="M35 23h10M35 39h10"/></g>',
    "topo": '<path d="M16 8v48M16 18h20M16 32h26M16 46h18" stroke="#e9a53b" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="16" cy="18" r="4" fill="#e8574a"/><circle cx="16" cy="32" r="4" fill="#e8574a"/><circle cx="16" cy="46" r="4" fill="#e8574a"/>',
}.items()}


def build_herramientas():
    path = "/herramientas/"
    _her = {h: (h, t, d, ic) for h, t, d, ic in HERRAMIENTAS}

    def tarjeta(h):
        if h in _her:
            _, t, d, ic = _her[h]
            return '<a class="art-card" href="%s"><span class="art-ico">%s</span><div><h3>%s</h3><p>%s</p><span class="art-mas">Abrir la herramienta →</span></div></a>' % (h, HER_ICO[ic], e(t), e(d))
        t = next(n for n, x in sum(HER_CAT.values(), []) if x == h)
        return '<a class="art-card" href="%s"><span class="art-ico">%s</span><div><h3>%s</h3><p>%s</p><span class="art-mas">Ver la zona →</span></div></a>' % (h, ART_ICO["escalada"], e(t), "Guía de boulder con los bloques, sectores y accesos.")
    body = (hero("Herramientas", "Herramientas de montaña gratis", "Previsión del tiempo en cumbre, estado de la nieve, caudal de barrancos, editor GPX, vídeo 3D de tus rutas y más. Gratis, sin registro y hechas por guías de montaña.", METEO_IMG,
                 [("Inicio", "/"), ("Herramientas", "")]) +
            "".join('<section class="section%s"><div class="wrap"><p class="eyebrow">Herramientas</p><h2>%s</h2><div class="art-grid art-grid2">' % (" alt" if k % 2 else "", e(c)) +
                    "".join(tarjeta(h) for _, h in HER_CAT[c]) + '</div></div></section>' for k, c in enumerate(sorted(HER_CAT))) +
            '<section class="section"><div class="wrap"><p class="rel-mas">Y para aprender: <a href="/articulos/">artículos de técnica, seguridad, material y rutas</a>.</p></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Herramientas", path)]),
          {"@context": "https://schema.org", "@type": "ItemList", "name": "Herramientas de montaña de Guías Ad Astra", "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "url": url(h), "name": t} for i, (h, t, _, _) in enumerate(HERRAMIENTAS)]}]
    page(path, "Herramientas de montaña gratis: tiempo, nieve, GPX | Ad Astra",
         "Herramientas gratis para la montaña: previsión en cumbre a 15 días, estado de la nieve, caudal de barrancos, editor GPX, vídeo 3D de rutas y lista de material.",
         body, "her", ld, priority="0.8")



BPA_NOTAS = [  # (x %, y %, título, explicación) sobre la imagen del boletín de Guadarrama del 29-1-2026
    (76, 4, "La zona.", "Cada boletín cubre un macizo entero, aquí la Sierra de Guadarrama. Las condiciones de tu ladera pueden ser mejores o peores que la media."),
    (24, 10.5, "Fecha de emisión.", "Jueves 29 de enero. En Guadarrama sale los jueves y vale para el fin de semana: no uses el de la semana anterior."),
    (46, 14, "Día de validez.", "«Pronóstico para el viernes, día 30»: lo de este recuadro es para el viernes. Debajo vienen los avances del sábado y del domingo. Todo vale fuera de las pistas de esquí balizadas y abiertas."),
    (35, 21, "Nivel de peligro.", "«Notable (Limitado)»: el primer nivel es el de las cotas altas y el que va entre paréntesis, el de las bajas. Es decir, 3 arriba y 2 abajo."),
    (64, 22, "Icono del nivel.", "El rombo naranja con dos exclamaciones es el icono europeo del nivel 3. La parte negra de la montaña señala en qué cotas se da ese nivel: las altas."),
    (8, 33, "Distribución por cotas.", "El triángulo dice dónde está cada nivel: por encima de 2.100 m, 3 (notable); por debajo, 2 (limitado)."),
    (27, 38.3, "Problema típico.", "Cada fila es un problema, del más al menos importante. Aquí, <b>placas de viento</b> (la manga de viento sobre la ladera) y <b>nieve reciente</b> (los copos). El de abajo del domingo, con sol y termómetro, es <b>nieve húmeda</b>."),
    (40, 38.3, "Cota.", "La parte negra de la montaña son las cotas afectadas. «2000 ↑»: por encima de 2.000 m. La montaña entera en negro: a todas las cotas. «2100 ↓» (domingo): por debajo de 2.100 m."),
    (61.5, 43, "Orientaciones.", "La rosa tiene ocho sectores (N, NE, E…). Los que están en negro son las orientaciones donde está el problema. Aquí está entera en negro, es decir, todas; lo normal es que sean solo unas pocas, por ejemplo N, NE y E tras viento del oeste."),
    (72.5, 41, "Tamaño esperable.", "Escala de 1 a 5. <b>1</b>, pequeño: difícilmente sepulta, pero puede arrastrarte y tirarte. <b>2</b>, mediano: puede sepultar, herir o matar a una persona. <b>3</b>, grande: puede sepultar un coche o destruir una caseta. <b>4</b> y <b>5</b>: muy grande y extremo. Aquí, placas de tamaño 2 y nieve reciente de tamaño 1."),
    (92, 41, "Innivación observada.", "Dato medido el 28 de enero: desde qué cota hay nieve continua en las caras norte (N) y sur (S). Aquí, desde unos 1.800 m en las dos."),
    (46, 50, "Avances para el fin de semana.", "El sábado se mantiene igual. El domingo sigue el nivel 3 arriba, pero la nieve reciente da paso a nieve húmeda por debajo de 2.100 m: aviso de calentamiento."),
]


GPX_FAQ = [
    ("¿Se suben mis tracks a algún servidor?", "No. El editor funciona entero en tu navegador: los archivos se leen y se guardan en tu propio ordenador. Ni nosotros ni nadie los ve."),
    ("¿Qué corrige la corrección automática?", "Tres cosas típicas de los GPS: los saltos (puntos sueltos a cientos de metros que aparecen cuando se pierde la señal, sobre todo al empezar o en valles cerrados), las paradas en las que el GPS sigue apuntando puntos que «bailan» alrededor del mismo sitio y suman metros y desnivel falsos, y el exceso de puntos. Antes de aplicarla puedes ver en el mapa qué se va a quitar."),
    ("¿Cómo uno dos tracks?", "Ábrelos a la vez (o uno detrás de otro), marca la casilla de los que quieras unir y pulsa «Unir los marcados». Se unen en el orden de la lista, que puedes cambiar con las flechas, y si alguno está en sentido contrario se gira solo."),
    ("¿Cómo quito un trozo del track?", "Selecciona el track, pulsa «Tramo», marca en el mapa el inicio y el final del trozo y elige: quitarlo y unir los extremos, quitarlo dejando dos tracks separados o quedarte solo con ese trozo."),
    ("¿Qué formatos puedo abrir?", "GPX (de Garmin, Wikiloc, Strava, Komoot, OruxMaps, Suunto…), KML de Google Earth y TCX. Siempre guarda en GPX 1.1, que abre cualquier GPS o aplicación."),
    ("¿Puedo dibujar un track o un trozo a mano?", "Sí. Con «Dibujar» creas un track nuevo pinchando en el mapa, y con «Alargar» lo continúas por el final o por el principio. Si dejas marcada la opción «Seguir senderos y caminos», entre un clic y el siguiente el track va por los caminos de OpenStreetMap (calculados con BRouter); si no, en línea recta. La altitud se añade sola."),
    ("¿Cómo añado waypoints?", "Pulsa «Waypoint» y pincha en el mapa donde quieras cada uno. Les puedes cambiar el nombre en la lista, arrastrarlos para moverlos o borrarlos, y se guardan en el GPX que descargues. También se leen los que traigan tus archivos."),
    ("¿Puedo descargar el mapa y el perfil en imagen?", "Sí, en «Descargar imágenes»: el mapa con el recorrido, el perfil de altitud o una ficha con las dos cosas y los datos de la ruta, en PNG y con el mapa que elijas (topográfico, IGN, ortofoto u OpenStreetMap). Para un trozo, márcalo con «Tramo» y descárgalo desde ahí."),
    ("Me he equivocado, ¿puedo volver atrás?", "Sí: el botón «Deshacer» (o Ctrl+Z) recupera los últimos 40 cambios."),
]


def build_editor_gpx():
    path = "/editor-gpx/"
    body = (hero("Herramientas", "Editor de tracks GPX", "Une, divide y recorta tracks, dibuja tramos por los senderos, añade waypoints, limpia los errores del GPS y descarga el mapa y el perfil en imagen. Gratis y sin subir tus archivos a ningún sitio.", METEO_IMG,
                 [("Inicio", "/"), ("Editor GPX", "")]) +
            '<section class="section gx-sec"><div class="wrap"><div id="gx-app" class="gx"><noscript>El editor necesita JavaScript.</noscript></div></div></section>'
            '<section class="section alt"><div class="wrap"><p class="eyebrow">Qué puedes hacer</p><h2>Un editor GPX completo, en el navegador</h2><div class="gd-capas">' +
            "".join('<article style="--c:%s"><h3>%s</h3><p>%s</p></article>' % x for x in [
                ("#4fb3e8", "Unir y dividir tracks", "Abre varios GPX a la vez, ordénalos y únelos en uno solo: si alguno va al revés, se gira solo. O corta un track en dos en el punto que elijas."),
                ("#e8574a", "Quitar y recortar tramos", "Marca el inicio y el final de un trozo y quítalo, sepáralo en otro track o quédate solo con él. También puedes mover o borrar puntos uno a uno."),
                ("#7cc47f", "Corregir errores del GPS", "Quita los saltos que da el GPS cuando pierde señal y limpia las paradas en las que los puntos bailan en el sitio y suman metros y desnivel falsos."),
                ("#e9a53b", "Dibujar rutas", "Crea un track nuevo o alarga uno existente pinchando en el mapa, campo a través o siguiendo los senderos de OpenStreetMap, con la altitud del terreno."),
                ("#c78bf0", "Waypoints", "Añade, mueve y nombra puntos de interés: fuentes, collados, avituallamientos… Se guardan en el GPX y salen en el vídeo 3D."),
                ("#f07ab8", "Mapa y perfil en imagen", "Descarga en PNG el mapa del recorrido sobre topográfico, IGN u ortofoto, el perfil de altitud o una ficha con todo, del track completo o de un tramo."),
            ]) + '</div><p style="margin-top:22px">Funciona con los archivos de Garmin, Wikiloc, Strava, Komoot, Suunto, Coros u OruxMaps, y guarda en GPX 1.1, que abre cualquier GPS o aplicación. Para planificar el tiempo de la ruta usa la <a href="/calculadora-rutas/">calculadora MIDE</a>, y para compartirla, el <a href="/video-ruta-3d/">vídeo 3D</a>.</p></div></section>'
            '<section class="section"><div class="wrap split"><div class="stack" style="gap:0">' + block("Preguntas frecuentes", faq_html(GPX_FAQ)) +
            '</div><div class="sticky"><div class="panel"><p class="eyebrow">Atajos</p><ul class="gd-reglas"><li><b>Ctrl + Z / Ctrl + Y:</b> deshacer y rehacer.</li><li><b>Supr:</b> borra el punto elegido en el modo «Puntos».</li><li><b>Esc:</b> sale del modo de edición.</li><li>Pasa el ratón por el perfil para ver cada punto en el mapa.</li></ul>'
            '<p><a href="/video-ruta-3d/">Haz un vídeo 3D de tu ruta →</a></p><p><a href="/calculadora-rutas/">Calcula el tiempo con el método MIDE →</a></p></div></div></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Editor GPX", path)]), faq_ld(GPX_FAQ),
          {"@context": "https://schema.org", "@type": "WebApplication", "name": "Editor de tracks GPX", "url": url(path), "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web",
           "description": "Editor GPX gratuito en el navegador: unir, dividir y recortar tracks, mover o borrar puntos y corregir errores del GPS.", "offers": {"@type": "Offer", "price": 0, "priceCurrency": "EUR"}, "provider": {"@id": D + "/#empresa"}}]
    head = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">'
    scripts = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin="" defer></script><script src="/js/gpx.js" defer></script>'
    page(path, "Editor GPX online gratis: unir, cortar y corregir | Ad Astra",
         "Edita tracks GPX gratis: une, divide y recorta, dibuja tramos, añade waypoints, corrige saltos del GPS y descarga mapa y perfil. Sin subir tus archivos.",
         body, "her", ld, priority="0.7", head=head, scripts=scripts)


VIDEO3D_FAQ = [
    ("¿Cuesta algo o tengo que registrarme?", "No. Es gratis, sin registro y sin marcas de agua de terceros: solo lleva un pequeño logo de Guías Ad Astra en una esquina."),
    ("¿Se sube mi track a algún sitio?", "No. El vídeo se crea en tu propio navegador: el track no sale de tu ordenador. Lo único que se descarga de internet son las imágenes del mapa y del relieve."),
    ("¿Qué navegador necesito?", "Uno actualizado de ordenador: Chrome, Edge, Safari o Firefox (versión 130 o posterior). En el móvil también funciona, pero tarda más. Si tu navegador no puede crear el vídeo, te lo dirá."),
    ("¿Cuánto tarda en crearse?", "Depende del ordenador y de la conexión: un vídeo de 30 segundos suele tardar entre uno y tres minutos. Se crea fotograma a fotograma, así que aunque tarde, el vídeo sale fluido."),
    ("¿Qué mapas puedo usar?", "La ortofoto del PNOA del Instituto Geográfico Nacional (la mejor calidad en España), el satélite Sentinel-2 para fuera de España, el mapa topográfico del IGN y OpenTopoMap. El relieve 3D sale de los datos abiertos Terrain Tiles."),
    ("¿Salen los waypoints en el vídeo?", "Sí. Se leen los waypoints del GPX que estén a menos de 500 m del recorrido, y también puedes añadir puntos escribiendo el kilómetro y el nombre, o quitar los que no quieras. Aparecen con su nombre sobre el mapa y en el perfil, y al llegar a cada uno la cámara se para un momento y sale un cartel con el nombre, el kilómetro y la altitud."),
    ("¿Puedo subirlo a Instagram o a Strava?", "Sí: elige el formato vertical para Reels e historias, o el horizontal para YouTube. El vídeo es MP4 y lleva incluidas las atribuciones de los mapas que piden sus licencias."),
]


def build_video3d():
    path = "/video-ruta-3d/"
    body = (hero("Herramientas", "Vídeo 3D de tu ruta", "Sube tu track y crea un vídeo de la ruta sobrevolando el relieve en 3D, con el perfil, la distancia y el desnivel. Gratis, sin registro y sin subir tu GPX a ningún sitio.", METEO_IMG,
                 [("Inicio", "/"), ("Vídeo 3D de la ruta", "")]) +
            '<section class="section gx-sec"><div class="wrap"><div id="v3-app" class="v3"><noscript>Esta herramienta necesita JavaScript.</noscript></div></div></section>'
            '<section class="section alt"><div class="wrap"><p class="eyebrow">Cómo se hace</p><h2>Tu ruta en vídeo 3D en cuatro pasos</h2><ol class="gd-pasos">' +
            "".join('<li><b>%s</b><span>%s</span></li>' % x for x in [
                ("Sube el track", "Arrastra tu GPX, KML o TCX (de tu reloj, Wikiloc, Strava, Komoot…). Si tiene errores del GPS, límpialo antes en el editor GPX."),
                ("Elige el estilo", "Mapa (ortofoto del PNOA, satélite, topográfico IGN u OpenTopoMap), formato horizontal, vertical o cuadrado, duración, cámara y color."),
                ("Añade tus puntos", "Los waypoints del archivo salen solos; puedes quitarlos o añadir otros por kilómetro. Al llegar a cada uno, el vídeo se para y muestra el nombre."),
                ("Crea y descarga el MP4", "Mira la animación y crea el vídeo: se genera fotograma a fotograma en tu ordenador y lo descargas listo para Instagram, YouTube o WhatsApp."),
            ]) + '</ol><p style="margin-top:22px">Es una alternativa gratuita a Relive para hacer vídeos de rutas de senderismo, montaña, trail o bici: sin registro, sin límite de vídeos y sin subir tu track a ningún servidor.</p></div></section>'
            '<section class="section"><div class="wrap split"><div class="stack" style="gap:0">' + block("Preguntas frecuentes", faq_html(VIDEO3D_FAQ)) +
            '</div><div class="sticky"><div class="panel"><p class="eyebrow">Consejo</p><p>Si tu track tiene saltos del GPS o paradas que dibujan una maraña, límpialo antes en el <a href="/editor-gpx/">editor GPX</a>: desde allí puedes mandarlo directamente a esta herramienta con «Hacer vídeo 3D».</p></div></div></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Vídeo 3D de la ruta", path)]), faq_ld(VIDEO3D_FAQ),
          {"@context": "https://schema.org", "@type": "WebApplication", "name": "Vídeo 3D de rutas", "url": url(path), "applicationCategory": "MultimediaApplication", "operatingSystem": "Web",
           "description": "Crea gratis un vídeo de tu ruta sobre un mapa 3D con relieve y perfil a partir de un archivo GPX.", "offers": {"@type": "Offer", "price": 0, "priceCurrency": "EUR"}, "provider": {"@id": D + "/#empresa"}}]
    head = '<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@5.24.0/dist/maplibre-gl.css" crossorigin="">'
    scripts = '<script src="https://unpkg.com/maplibre-gl@5.24.0/dist/maplibre-gl.js" crossorigin="" defer></script><script src="/js/video3d.js" defer></script>'
    page(path, "Vídeo 3D de tu ruta GPX gratis, tipo Relive | Ad Astra",
         "Crea gratis un vídeo de tu ruta en 3D sobre el relieve, con perfil, desnivel y waypoints. Sube tu GPX y descarga el MP4 en horizontal, vertical o cuadrado.",
         body, "her", ld, priority="0.7", head=head, scripts=scripts)


UV_FAQ = [
    ("¿Hace falta crema en invierno o con nubes?", "Sí. Las nubes finas dejan pasar la mayor parte de la radiación UV, y en invierno la nieve la refleja casi entera: en una cumbre nevada de enero el índice UV puede ser tan alto como en una playa de primavera. Lo que baja en invierno es la temperatura, no tanto la radiación en la montaña."),
    ("¿Un FPS 50 protege el doble que un 25?", "No. Un FPS 15 filtra alrededor del 93 % de los UVB, un 30 cerca del 97 % y un 50 alrededor del 98 %. La diferencia de verdad está en la cantidad que te pones y en renovarla: casi todo el mundo se echa menos de la mitad de lo necesario, y entonces el FPS real se queda muy por debajo del que pone el bote."),
    ("¿Qué significa el logo UVA en un círculo?", "Que la protección frente a los UVA es al menos un tercio del FPS que indica el envase, como recomienda la Comisión Europea. Los UVA no queman, pero envejecen la piel y también intervienen en el cáncer de piel, así que busca siempre ese logo."),
    ("¿Qué gafas de sol necesito en la montaña?", "De categoría 3 para un día normal de verano y de categoría 4 sobre nieve, glaciar o a mucha altitud. Que filtren el 100 % de los UV (pone «UV 400» o «100 % UV») y que tapen bien por los lados. Las de categoría 4 no sirven para conducir."),
    ("¿Qué es la ceguera de la nieve?", "Una quemadura de la córnea por la radiación UV reflejada en la nieve (fotoqueratitis). No se nota en el momento: a las 6–12 horas aparecen dolor intenso, sensación de arena en los ojos, lagrimeo y no poder abrir los ojos. Suele curarse en uno o dos días, pero en la montaña te deja sin ver. Se evita con gafas de categoría 4 bien cerradas, también con el día nublado."),
    ("¿Dónde veo el índice UV de cada día?", "En nuestra previsión de meteorología de montaña, para la cumbre y la base de cada sierra, con el máximo del día, la hora y el consejo de protección."),
]


def build_uv():
    path = "/rayos-uv-proteccion-solar-montana/"
    seccion = lambda eyebrow, h2, inner, alt=False: '<section class="section%s"><div class="wrap"><p class="eyebrow">%s</p><h2>%s</h2>%s</div></section>' % (" alt" if alt else "", eyebrow, h2, inner)
    tabla = lambda cab, filas: '<div class="gd-tw"><table class="gd-t"><thead><tr>' + "".join("<th>%s</th>" % c for c in cab) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(("<th>%s</th>" if i == 0 else "<td>%s</td>") % c for i, c in enumerate(f)) + "</tr>" for f in filas) + "</tbody></table></div>"
    espectro = ('<svg viewBox="0 0 900 330" role="img" aria-label="Los UVC no llegan al suelo; los UVB se quedan en la capa superficial de la piel y queman; los UVA entran más hondo y envejecen la piel" style="width:100%;height:auto;display:block;border-radius:16px">'
                '<rect width="900" height="330" fill="#f4efe7"/>'
                '<rect x="0" y="0" width="900" height="70" fill="#cfe5f5"/><text x="20" y="40" font-family="Inter,system-ui,sans-serif" font-size="17" font-weight="800" fill="#1d3b57">Capa de ozono</text>'
                '<rect x="0" y="62" width="900" height="16" fill="#8fb8d8"/>'
                '<rect x="0" y="220" width="900" height="38" fill="#f2c9a8"/><rect x="0" y="258" width="900" height="72" fill="#e6a98a"/>'
                '<text x="20" y="244" font-family="Inter,system-ui,sans-serif" font-size="14" font-weight="700" fill="#6b3a22">Epidermis</text><text x="20" y="300" font-family="Inter,system-ui,sans-serif" font-size="14" font-weight="700" fill="#6b3a22">Dermis</text>'
                '<g font-family="Inter,system-ui,sans-serif" font-weight="800">'
                '<path d="M210 10 L210 66" stroke="#8a4fc7" stroke-width="10" stroke-linecap="round"/><text x="228" y="38" font-size="20" fill="#8a4fc7">UVC</text><text x="228" y="58" font-size="13" font-weight="600" fill="#5c3a80">la frena el ozono</text>'
                '<path d="M470 10 L470 232" stroke="#e8574a" stroke-width="10" stroke-linecap="round"/><text x="488" y="150" font-size="20" fill="#c23a2c">UVB</text><text x="488" y="170" font-size="13" font-weight="600" fill="#8a2a20">quema · se queda en la superficie</text>'
                '<path d="M730 10 L730 300" stroke="#e9a53b" stroke-width="10" stroke-linecap="round"/><text x="748" y="150" font-size="20" fill="#b5671a">UVA</text><text x="748" y="170" font-size="13" font-weight="600" fill="#7a4512">entra hondo · envejece</text>'
                '</g></svg>')
    body = (hero("Artículos", "Rayos UV y protección solar en la montaña", "Qué rayos UV hacen daño, por qué en la montaña te quemas más, qué significa cada FPS y qué categoría de gafas necesitas. Todo lo que hay que saber para no volver de la cumbre quemado.", img("afe67801-cf88-4cef-a3ac-e25e4e971634/senderismo-avila-gredos.webp"),
                 [("Inicio", "/"), ("Artículos", "/articulos/"), ("Rayos UV y protección solar", "")], '<a class="btn btn-primary" href="/meteo/">Ver el índice UV de hoy</a><a class="btn btn-ghost" href="#fps">Qué FPS usar</a>') +
            seccion("Lo básico", "Qué son los rayos UV y cuáles hacen daño",
                    '<p class="lead-p">La radiación ultravioleta es la parte de la luz del sol que no vemos. Se divide en tres tipos según su longitud de onda, y cada uno hace una cosa distinta:</p>'
                    '<div class="gd-fig">' + espectro + '</div>' +
                    tabla(["Tipo", "Longitud de onda", "Qué hace"], [
                        ["UVC", "100–280 nm", "Es la más dañina, pero la capa de ozono la absorbe por completo: no llega al suelo."],
                        ["UVB", "280–315 nm", "La responsable de las quemaduras. Se queda en la capa superficial de la piel y daña directamente su ADN: es la que más se relaciona con el cáncer de piel. También quema los ojos (ceguera de la nieve)."],
                        ["UVA", "315–400 nm", "Llega en mucha más cantidad, todo el año y atraviesa las nubes y el cristal. No quema, pero entra más hondo: envejece la piel, produce manchas y también participa en el cáncer de piel."],
                    ]) + '<p style="margin-top:16px">Así que hay que protegerse de los dos que llegan: los UVB (que miden el FPS) y los UVA (que mide el logo UVA del envase).</p>') +
            seccion("En la montaña", "Por qué en la montaña te quemas más",
                    '<div class="gd-capas">' + "".join('<article style="--c:%s"><h3>%s</h3><p>%s</p></article>' % x for x in [
                        ("#4fb3e8", "La altitud", "Hay menos atmósfera por encima que filtre la radiación: según la OMS, el UV sube alrededor de un 10 % por cada 1.000 m. En una cumbre de 2.500 m recibes en torno a un 25 % más que en el valle."),
                        ("#ffffff", "La nieve", "La nieve fresca refleja hasta el 80 % de la radiación UV, que te llega por debajo: a la barbilla, la nariz, las orejas y los ojos. Es la razón de las quemaduras raras de esquiadores y alpinistas."),
                        ("#e9a53b", "La hora y la época", "Entre las 12 y las 16 h (hora oficial de verano) llega la mayor parte de la radiación del día. En primavera, con mucha nieve y el sol ya alto, se juntan los dos peores factores."),
                        ("#b9a593", "Las nubes engañan", "Las nubes finas o dispersas dejan pasar casi toda la radiación, y como no sientes calor, no te das cuenta. Solo las nubes gruesas y continuas la reducen de verdad."),
                        ("#7cc47f", "El viento y el frío", "Te refrescan y no notas que te estás quemando. La quemadura aparece horas después, cuando ya estás en casa."),
                        ("#6fb3e8", "El agua", "En barrancos, ríos y lagos, el agua refleja parte de la radiación, y mojado la crema dura menos."),
                    ]) + "</div>", True) +
            seccion("El índice UV", "Cómo leer el índice UV",
                    '<p class="lead-p">El índice UV mide la radiación que quema la piel en una escala que empieza en 0 y en España puede pasar de 11 en verano en la montaña. Es el número que te damos cada día en nuestra <a href="/meteo/">previsión de montaña</a>, para la cumbre y la base de cada sierra.</p>' +
                    '<div class="gd-escala uv-esc">' + "".join('<div style="--c:%s"><span>%s</span><b>%s</b><p>%s</p></div>' % x for x in [
                        ("#4caf50", "0–2", "Bajo", "Poco riesgo. Gafas de sol si hay nieve; crema si vas a estar muchas horas."),
                        ("#e6c32e", "3–5", "Moderado", "Crema solar, gafas de sol y gorra en las horas centrales."),
                        ("#f08a24", "6–7", "Alto", "Protección alta (FPS 30–50), gafas de categoría 3, gorra y buscar la sombra a mediodía."),
                        ("#e8574a", "8–10", "Muy alto", "FPS 50 renovado cada 2 horas, gafas de categoría 3–4, ropa que cubra. Una piel clara se quema en menos de 15 minutos."),
                        ("#a55fd6", "11+", "Extremo", "Todo lo anterior, sin excepciones. Habitual en verano en cumbres altas y en primavera sobre nieve."),
                    ]) + "</div>") +
            '<section class="section alt" id="fps"><div class="wrap"><p class="eyebrow">La crema</p><h2>Qué significa cada factor de protección (FPS)</h2>'
            '<p class="lead-p">El FPS (o SPF) indica cuánto protege frente a los UVB, es decir, frente a la quemadura. Un FPS 30 quiere decir, en teoría, que tardarías 30 veces más en quemarte que sin nada… siempre que te pongas la cantidad correcta, cosa que casi nadie hace. Por eso en la Unión Europea los envases los agrupan en cuatro categorías:</p>' +
            tabla(["Categoría", "FPS", "UVB que filtra", "Para qué"], [
                ["Baja", "6–10", "≈ 83–90 %", "No es suficiente para la montaña."],
                ["Media", "15–25", "≈ 93–96 %", "Días con índice UV bajo o moderado, a poca altitud y pocas horas al sol."],
                ["Alta", "30–50", "≈ 97–98 %", "La opción normal para un día de montaña o barranco en verano."],
                ["Muy alta", "50+", "≈ 98 % o más", "Nieve, glaciar, alta montaña, índice UV muy alto o extremo, pieles muy claras, niños y cicatrices."],
            ]) +
            '<div class="gd-dos" style="margin-top:26px"><div><h3>Cómo ponértela para que funcione</h3><ul class="gd-reglas">'
            '<li><b>Cantidad:</b> unos 2 mg por cm² de piel. En la práctica, una cucharadita para la cara y el cuello, y unas seis para todo el cuerpo. Con la mitad, el FPS real se queda en mucho menos de la mitad.</li>'
            '<li><b>Antes de salir:</b> 15–30 minutos antes de exponerte, con la piel seca.</li>'
            '<li><b>Renuévala:</b> cada 2 horas y siempre después de sudar mucho, de mojarte o de secarte con la toalla. «Resistente al agua» solo significa que aguanta unos 40 minutos en el agua (80 si pone «muy resistente»).</li>'
            '<li><b>Los sitios olvidados:</b> orejas, nariz, nuca, la parte baja de la barbilla (por el reflejo de la nieve), el cuero cabelludo si tienes poco pelo y el dorso de las manos.</li>'
            '<li><b>Labios:</b> un protector labial con FPS; se queman y se agrietan muchísimo en altura.</li></ul></div>'
            '<div><h3>Cómo elegirla</h3><ul class="gd-reglas">'
            '<li><b>Busca el logo UVA en un círculo:</b> garantiza que la protección frente a los UVA es al menos un tercio del FPS.</li>'
            '<li><b>«Amplio espectro»</b> o «UVA/UVB» en el envase: protege de los dos.</li>'
            '<li><b>En formato barra o stick</b> para la cara y los labios: no se derrama en la mochila y se pone con los guantes a medio quitar.</li>'
            '<li><b>Mira la fecha:</b> la crema del año pasado abierta pierde eficacia.</li>'
            '<li><b>Ojo con algunos medicamentos</b> (ciertos antibióticos, antiinflamatorios o anticonceptivos): pueden hacer la piel más sensible al sol. Pregunta en la farmacia.</li></ul></div></div></div></section>' +
            seccion("Los ojos", "Gafas de sol: la categoría importa",
                    '<p class="lead-p">La categoría de unas gafas indica cuánta luz visible dejan pasar (lo oscuras que son). La protección frente a los UV es otra cosa: tiene que poner «UV 400» o «100 % UV». En la montaña necesitas las dos cosas.</p>' +
                    tabla(["Categoría", "Luz que pasa", "Para qué"], [
                        ["0", "80–100 %", "Transparentes o casi: interiores o días muy cubiertos."],
                        ["1", "43–80 %", "Luz solar débil."],
                        ["2", "18–43 %", "Luz solar media: ciudad, días con algo de nubes."],
                        ["3", "8–18 %", "Luz solar fuerte: la normal para la montaña en verano, la playa y el agua."],
                        ["4", "3–8 %", "Luz solar extrema: nieve, glaciar y alta montaña. No sirven para conducir."],
                    ]) +
                    '<ul class="gd-reglas" style="margin-top:18px"><li><b>Que cierren por los lados</b> (o con protectores laterales): sobre la nieve, la radiación también entra de lado y de abajo.</li>'
                    '<li><b>Ceguera de la nieve:</b> es una quemadura de la córnea que aparece horas después (dolor intenso, sensación de arena, no poder abrir los ojos). Pasa también con el día nublado. Lleva siempre unas gafas de repuesto en grupo.</li>'
                    '<li><b>Lentes polarizadas</b> quitan los reflejos del agua y la nieve, pero no protegen más de los UV por sí mismas. Las fotocromáticas son cómodas si cambias mucho de luz.</li></ul>', True) +
            seccion("Más allá de la crema", "La mejor protección es la que no se borra",
                    '<div class="gd-capas">' + "".join('<article style="--c:%s"><h3>%s</h3><p>%s</p></article>' % x for x in [
                        ("#e9a53b", "Ropa", "Una camiseta de manga larga ligera protege más que cualquier crema y no hay que renovarla. Algunas prendas técnicas indican su factor de protección UPF (50+ es excelente)."),
                        ("#4fb3e8", "Gorra, buff y sombrero", "Gorra con visera o sombrero de ala para la cara y la nuca; el buff, para el cuello y la cara en la nieve o con viento."),
                        ("#7cc47f", "Planificación", "Empieza temprano y deja las horas centrales para las zonas de sombra o el descanso. Mira el índice UV del día en la previsión."),
                        ("#e8574a", "Hidratación", "Con sol fuerte y altitud se pierde mucha agua sin darte cuenta: bebe a menudo."),
                    ]) + '</div><p style="margin-top:20px">¿Qué ropa llevar? Te lo contamos en <a href="/teoria-de-las-capas/">la teoría de las capas</a>, y qué meter en la mochila, en la <a href="/lista-material-montana/">lista de material</a>.</p>') +
            '<section class="section alt"><div class="wrap split"><div class="stack" style="gap:0">' + block("Preguntas frecuentes", faq_html(UV_FAQ)) +
            '</div><div class="sticky"><div class="panel"><p class="eyebrow">Fuentes</p><ul class="gd-links">'
            '<li><a href="https://www.sanidad.gob.es/areas/sanidadAmbiental/riesgosAmbientales/ultravioleta/home.htm" target="_blank" rel="noopener">Ministerio de Sanidad: radiación ultravioleta</a></li>'
            '<li><a href="https://www.who.int/uv/faq/whatisuv/en/" target="_blank" rel="noopener">Organización Mundial de la Salud: el índice UV</a></li>'
            '<li><a href="https://eur-lex.europa.eu/eli/reco/2006/647/oj/eng" target="_blank" rel="noopener">Recomendación 2006/647/CE sobre productos de protección solar</a></li>'
            '<li><a href="https://www.consumer.es/salud/como-leer-etiquetas-protectores-solares" target="_blank" rel="noopener">Consumer: cómo leer las etiquetas de los protectores solares</a></li>'
            '<li><a href="https://www.ocu.org/salud/bienestar-prevencion/informe/consejos-gafas-de-sol" target="_blank" rel="noopener">OCU: gafas de sol, consejos de compra</a></li></ul>'
            '<p class="small muted">Este artículo es divulgativo y no sustituye el consejo de un dermatólogo u oftalmólogo.</p></div></div></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Artículos", "/articulos/"), ("Rayos UV y protección solar", path)]), faq_ld(UV_FAQ),
          articulo_ld(path, "Rayos UV y protección solar en la montaña", "Qué rayos UV hacen daño, por qué en la montaña te quemas más, qué significa cada FPS y qué gafas de sol necesitas.", "2026-11-23")]
    page(path, "Rayos UV y protección solar en la montaña | Ad Astra",
         "UVA, UVB y UVC: cuáles hacen daño y por qué en la montaña te quemas más. Qué significa cada FPS, cómo ponerte la crema y qué categoría de gafas usar.",
         body, "art", ld, priority="0.6")


def build_nuevos():
    for a in NUEVOS:
        path = a["path"]
        crumbs = [("Inicio", "/"), ("Artículos", "/articulos/"), (a["corto"], "")]
        fuentes = "".join('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, e(t)) for u, t in a["fuentes"])
        body = (hero("Artículos", a["titulo"], a["lead"], a["hero"] if a["hero"].startswith("/") else img(a["hero"]), crumbs, a.get("actions", "")) + a["cuerpo"] +
                '<section class="section alt"><div class="wrap split"><div class="stack" style="gap:0">' + block("Preguntas frecuentes", faq_html(a["faq"])) +
                '</div><div class="sticky"><div class="panel"><p class="eyebrow">Fuentes</p><ul class="gd-links">' + fuentes + '</ul>' +
                ('<p class="small muted">%s</p>' % a["nota"] if a.get("nota") else "") + arts_util.credito_portada(a["hero"]) + '</div></div></div></section>')
        ld = [crumbs_ld([("Inicio", "/"), ("Artículos", "/articulos/"), (a["corto"], path)]), faq_ld(a["faq"]),
              articulo_ld(path, a["titulo"], a["meta_desc"], a["publicado"])]
        page(path, a["meta_title"], a["meta_desc"], body, "art", ld, priority="0.6")


LEER_NIEVE_FAQ = [
    ("¿A partir de qué inclinación puede salir un alud?", "Los aludes de placa salen casi siempre en laderas de 30° o más, y la mayoría entre 35° y 45°. Por debajo de 30° es raro que se desencadenen, pero un alud que sale más arriba puede llegar hasta ti: cuenta también la pendiente que tienes encima."),
    ("¿Qué es una placa de viento?", "Una capa de nieve que el viento ha transportado y compactado a sotavento de crestas, collados y cambios de pendiente. Puede ser blanda o dura, pero es cohesiva: si debajo hay una capa débil, se rompe de golpe y desliza entera. Es el problema de aludes más habitual en nuestras sierras."),
    ("Si el boletín dice peligro 2 (limitado), ¿puedo ir tranquilo?", "No del todo. Con peligro 2 se dan cerca de un tercio de las muertes por aludes y con 3 (notable), alrededor de la mitad, porque son los niveles en los que más gente sale. El nivel te dice cuánto cuidado poner; dónde está el problema te lo dicen las orientaciones, las cotas y el tipo de problema del boletín."),
    ("¿Hay boletín de aludes para Gredos?", "No. AEMET publica boletín para el Pirineo navarro y aragonés, Picos de Europa, las sierras del Cordel y Peña Labra y la Sierra de Guadarrama. En Gredos, el de Guadarrama orienta sobre la situación general del Sistema Central, pero hay que completarlo con la previsión, el estado de la nieve y lo que observes sobre el terreno."),
    ("¿El ARVA evita que te pille un alud?", "No: solo sirve para que tus compañeros te encuentren rápido si quedas sepultado, y para encontrar tú a otro. Por eso va siempre con pala y sonda, y hay que practicar. Lo que evita el alud es la elección del terreno y del momento."),
    ("¿Qué hago si un compañero queda sepultado?", "Fíjate en el punto donde lo viste por última vez, comprueba que no hay peligro de otro alud, llama al 112 (o que lo haga otro) y empieza la búsqueda con el ARVA ya, sin esperar a nadie. Localiza con la sonda y palea con método. Los primeros 15 minutos son decisivos."),
]


def build_leer_nieve():
    path = "/como-leer-la-nieve-y-los-aludes/"
    cambios = [
        ("Asentamiento y redondeo", "#7cc47f", "Con temperaturas suaves y poca diferencia de temperatura dentro del manto, los cristales se redondean y se unen. La nieve se asienta, pierde espesor y gana cohesión: el manto se estabiliza. Pasa en los días siguientes a una nevada sin frío intenso."),
        ("Facetas y cubiletes", "#e8574a", "Con frío intenso, noches despejadas y poco espesor de nieve, el suelo está mucho más caliente que la superficie. Esa diferencia hace crecer cristales angulosos (facetas) y, en la base, cubiletes huecos. No se unen entre sí: son las capas débiles que duran semanas."),
        ("Escarcha de superficie", "#9fc6e6", "En noches frías, claras y sin viento se forman cristales de escarcha sobre la nieve, como plumas que brillan al sol. Mientras están en superficie no pasa nada; si la siguiente nevada los entierra, forman una de las capas débiles más traicioneras."),
        ("Fusión y rehielo", "#e9a53b", "El sol o el calor funden la superficie y por la noche se vuelve a helar. Sale una costra dura por la mañana, que se ablanda a lo largo del día. Es la nieve típica de primavera: segura a primera hora si ha helado bien, cada vez más húmeda e inestable según avanza la mañana."),
        ("Costras de lluvia y de viento", "#c9a7e8", "La lluvia sobre la nieve deja al helarse una costra lisa; el viento, una superficie dura y pulida. Una vez enterradas son una superficie de deslizamiento para la nieve que caiga encima, y a veces generan facetas en sus bordes."),
    ]
    tipos = [
        ("Alud de placa", "Una capa cohesiva se rompe a la vez en una fractura lineal y desliza entera sobre una capa débil. Es el que causa la gran mayoría de los accidentes, porque lo suele provocar la propia víctima o alguien de su grupo."),
        ("Alud de nieve suelta", "Empieza en un punto y se va abriendo en forma de pera. Lo forma nieve sin cohesión: reciente y seca en pendientes fuertes, o húmeda con calor. Suele ser más pequeño, pero en terreno expuesto te puede arrastrar y tirar por un cortado."),
        ("Alud de nieve húmeda", "Nieve pesada y lenta, que sale con calor o lluvia, sobre todo en las horas centrales del día y en solanas. Arrastra mucho material y al pararse se endurece como el cemento."),
        ("Deslizamiento basal", "Todo el manto se desliza sobre el suelo, normalmente sobre hierba o roca lisa. Avisa con grietas abiertas en la nieve (bocas de ballena), pero puede caer en cualquier momento y no depende de que lo pises."),
    ]
    problemas = [
        ("Nieve reciente", "#f5d33b", "La sobrecarga de una nevada importante, sobre todo si cae con viento o sobre una superficie lisa.",
         "Durante la nevada y los 2 o 3 días siguientes, en casi todas las orientaciones.", "Esperar a que se asiente. Como referencia, más de 30 cm de nieve nueva (menos con viento o frío) ya es una señal de alarma."),
        ("Nieve venteada (placas de viento)", "#f08a24", "La nieve transportada por el viento a sotavento de crestas, collados, canales y cambios de pendiente.",
         "Durante y después del viento; se puede formar en horas, incluso sin nevar.", "Reconocer y evitar las acumulaciones en laderas empinadas. Saber de dónde ha soplado el viento los últimos días."),
        ("Capas débiles persistentes", "#e8574a", "Capas de facetas, cubiletes o escarcha enterradas en el manto viejo.",
         "Semanas o meses. Más en umbrías y zonas protegidas del viento, y donde el manto es fino.", "Muy difícil de ver: hay que fiarse del boletín, de los whumpfs y de un margen amplio. Cuidado al pasar de zonas de poca nieve a zonas de mucha."),
        ("Nieve húmeda", "#9fc6e6", "El agua de fusión o de lluvia que entra en el manto y le quita cohesión.",
         "Horas o días: en las solanas según calienta el día, en todas las orientaciones si llueve.", "Madrugar y volver pronto. Si la noche no ha helado (noches nubladas o templadas), el problema está ahí desde el principio."),
        ("Deslizamientos basales", "#c9a7e8", "Todo el manto deslizando sobre hierba o losas de roca.",
         "Días o meses; a cualquier hora, más en la segunda mitad del día en primavera.", "No pararse debajo de las grietas de deslizamiento ni pasar por encima de ellas."),
    ]
    escala = [("1", "Débil", "#cce8a6", "Condiciones generalmente estables. Solo con sobrecargas fuertes en pendientes extremas aisladas."),
              ("2", "Limitado", "#f5e15b", "Estable en la mayoría del terreno, pero se pueden desencadenar placas con sobrecargas fuertes en las pendientes indicadas."),
              ("3", "Notable", "#f5a442", "Condiciones peligrosas. Se puede desencadenar un alud con el paso de una sola persona en las pendientes indicadas. Algunos aludes espontáneos grandes."),
              ("4", "Fuerte", "#e8574a", "Muy peligroso: desencadenamiento probable con una sola persona en muchas pendientes. Muchos aludes espontáneos grandes."),
              ("5", "Muy fuerte", "#8e2a24", "Extraordinario: numerosos aludes espontáneos muy grandes, también en terreno moderadamente empinado.")]
    alarmas = ["Aludes recientes en laderas parecidas a la tuya: es la señal más clara de todas.",
               "Un «whumpf»: el ruido sordo del manto que se hunde bajo tus pies. Hay una capa débil que acaba de colapsar.",
               "Grietas que salen disparadas desde tus esquís o tus botas.",
               "Más de 30 cm de nieve nueva en las últimas 72 horas, o menos si ha caído con viento.",
               "Viento que mueve nieve: penachos en las crestas, nieve que vuela, cornisas creciendo.",
               "Calentamiento rápido, lluvia sobre la nieve o una noche sin helar: bolas que ruedan, te hundes hasta la rodilla."]
    laderas = [("Inclinación", "Mide la pendiente en el mapa antes de salir (muchas apps de mapas tienen una capa de pendientes) y sobre el terreno. A partir de 30° estás en terreno de aludes, y cuenta también la pendiente que tienes encima, no solo la que pisas."),
               ("Orientación", "Las umbrías (norte) guardan las capas débiles más tiempo porque reciben poco sol. Las solanas (sur) se humedecen antes con el calor del día. El boletín indica qué orientaciones son las peligrosas: mira la rosa de los vientos y compara con tu ruta."),
               ("Altitud", "Por encima del bosque el viento mueve mucha más nieve y hay más placas. La cota también marca dónde nieva o llueve y hasta dónde llega el rehielo nocturno."),
               ("Forma del terreno", "Las placas suelen romper en convexidades (donde la ladera se vuelve más empinada), en canales, depresiones y bajo cornisas. Las lomas y cordales suaves y anchos suelen ser los pasos más seguros."),
               ("Trampas del terreno", "Lo que hay debajo cuenta tanto como la ladera: un barranco, una hoya o un arroyo donde la nieve se acumula metros, un cortado, rocas o árboles contra los que golpear. Un alud pequeño en una trampa puede ser mortal."),
               ("Espesor del manto", "Donde hay poca nieve (rocas que asoman, bordes de crestas) las capas débiles son más fáciles de romper. Las transiciones de manto fino a grueso son puntos típicos de desencadenamiento.")]
    antes = ["Lee el boletín de peligro de aludes del día: nivel, problema típico, orientaciones y cotas. Si no hay boletín para tu zona, el más cercano te da una idea general.",
             "Mira cómo ha sido la última semana: nevadas, viento (de dónde y con qué fuerza), lluvia, noches que no helaron. Lo tienes en nuestra página de meteorología y en el estado de la nieve.",
             "Elige la ruta según las condiciones, no al revés: busca lomas y bosque, evita canales y laderas de sotavento cargadas. Prepara alternativas más fáciles y un horario de vuelta.",
             "ARVA, pala y sonda para cada persona del grupo, comprobación del ARVA al salir y práctica de búsqueda. Nunca vayas solo a terreno de aludes y deja dicho a dónde vas."]
    durante = ["Observa todo el día: nieve que se mueve, aludes recientes, whumpfs, grietas, cambios de temperatura. Si las señales no coinciden con lo que esperabas, cambia el plan.",
               "Pasa de uno en uno por las laderas dudosas, con distancia entre personas, y espera en sitios seguros: fuera de la trayectoria de los aludes, en lomas o detrás de rocas grandes.",
               "No te pares ni te reagrupes en el fondo de canales o al pie de pendientes.",
               "En primavera, madruga: sube con la nieve dura y sal de las pendientes antes de que se ablande. Si te hundes hasta la bota y la nieve hace bolas, es hora de irse.",
               "Darse la vuelta siempre es una opción válida. La montaña sigue ahí mañana."]
    rescate = [("Observa", "Fíjate en el punto donde viste a la persona por última vez: ahí empieza la zona de búsqueda. Comprueba que no hay peligro de otro alud."),
               ("Avisa", "Llama al 112 (o que llame alguien mientras los demás buscan). Todos los ARVA del grupo en modo búsqueda."),
               ("Busca con el ARVA", "Recorre la zona en franjas hasta captar señal, sigue la señal y afina cerca de la nieve en cruz."),
               ("Sondea", "Sondea en espiral desde el punto más bajo que marque el ARVA hasta tocar a la persona; deja la sonda clavada."),
               ("Palea", "Empieza un poco por debajo de la sonda, en forma de V, cambiando de palista. Libera primero la cara y las vías respiratorias.")]
    seccion = lambda eyebrow, h2, inner, alt=False, ide="": '<section class="section%s"%s><div class="wrap"><p class="eyebrow">%s</p><h2>%s</h2>%s</div></section>' % (" alt" if alt else "", ' id="%s"' % ide if ide else "", eyebrow, h2, inner)
    tarjetas = lambda items: '<div class="gd-capas">' + "".join('<article style="--c:%s"><h3>%s</h3><p>%s</p></article>' % (c, e(t), e(x)) for t, c, x in items) + "</div>"
    body = (hero("Artículos", "Cómo leer la nieve y el peligro de aludes", "Cómo cambia el manto, cómo se forman las placas de viento, los tipos de aludes y cómo leer una ladera antes de meterte en ella. Lo que miramos los guías cada día de invierno.", METEO_IMG,
                 [("Inicio", "/"), ("Artículos", "/articulos/"), ("Cómo leer la nieve", "")], '<a class="btn btn-primary" href="#laderas">Leer una ladera</a><a class="btn btn-ghost" href="#boletin">El parte de AEMET</a>') +
            '<section class="section"><div class="wrap"><div class="panel" style="border-color:#e8574a"><p class="eyebrow" style="color:#e8574a">Antes de nada</p><p>Esta guía sirve para entender lo que ves y lo que dice el boletín, pero <b>no sustituye a un curso de nieve y aludes</b> ni a la experiencia. En terreno de aludes ve siempre con ARVA, pala y sonda, sabiendo usarlos y acompañado.</p></div></div></section>' +
            seccion("El manto", "La nieve cambia en cuanto cae",
                    '<p class="lead-p">El manto es una pila de capas, una por cada nevada, episodio de viento o de calor. Dentro, los cristales se transforman sin parar (es lo que se llama metamorfismo) y eso decide si las capas se unen entre sí o si queda una débil entre dos fuertes. Un alud de placa necesita las dos cosas: una capa cohesiva arriba y una débil debajo.</p>'
                    '<div class="gd-fig">' + guias_svg.nieve_manto() + '</div>' + tarjetas(cambios)) +
            seccion("El viento", "Placas de viento: el problema más habitual",
                    '<p class="lead-p">El viento es el gran constructor de aludes. A partir de unos 20–30 km/h ya mueve la nieve suelta: la arranca de la ladera por donde sopla (barlovento) y la deposita al otro lado de crestas y collados (sotavento), en canales y en cambios de pendiente. Ahí forma placas y cornisas, a veces en pocas horas y sin que esté nevando.</p>'
                    '<div class="gd-fig">' + guias_svg.nieve_viento() + '</div>'
                    '<ul class="gd-reglas"><li><b>Barlovento:</b> nieve dura, ondulada o con surcos (sastrugi), rocas que asoman. Poca nieve, normalmente más segura.</li>'
                    '<li><b>Sotavento:</b> superficies lisas y redondeadas, «almohadas», nieve que suena hueca o más blanda que alrededor, cornisas encima. Ahí están las placas.</li>'
                    '<li><b>Las placas duras engañan:</b> parecen firmes porque sostienen tu peso, pero pueden romper más arriba de donde estás y llevarse toda la ladera.</li>'
                    '<li><b>Las cornisas</b> se rompen más atrás de lo que parece: no te acerques al borde por arriba ni te quedes debajo, sobre todo con viento o calor.</li></ul>', True) +
            seccion("Tipos de aludes", "Cómo se rompe la nieve",
                    '<div class="gd-pasos gd-pasos-sin">' + "".join('<li><b>%s</b><span>%s</span></li>' % (e(t), e(x)) for t, x in tipos) + '</div>') +
            seccion("Los problemas típicos", "Lo que vas a leer en el boletín",
                    '<p class="lead-p">Los servicios de aludes europeos describen la situación con cinco problemas típicos. Cada uno se reconoce, se sitúa y se gestiona de una forma distinta: saber cuál hay ese día es más útil que el número del nivel de peligro.</p>'
                    '<div class="gd-tw"><table class="gd-t"><thead><tr><th>Problema</th><th>Qué es</th><th>Cuándo y dónde</th><th>Cómo gestionarlo</th></tr></thead><tbody>' +
                    "".join('<tr><th><i class="gd-pt" style="background:%s"></i>%s</th><td>%s</td><td>%s</td><td>%s</td></tr>' % (c, e(n), e(q), e(d), e(g)) for n, c, q, d, g in problemas) +
                    '</tbody></table></div><p class="muted small">Además pueden aparecer las cornisas como problema propio, o «problema no diferenciado» cuando no domina ninguno: eso no significa que no haya peligro.</p>', True) +
            seccion("La escala europea", "Los cinco niveles de peligro",
                    '<div class="gd-escala">' + "".join('<div style="--c:%s"><span>%s</span><b>%s</b><p>%s</p></div>' % (c, n, e(t), e(x)) for n, t, c, x in escala) + '</div>'
                    '<p class="lead-p" style="margin-top:18px">El nivel 3 (notable) se da aproximadamente un 30 % del invierno y concentra cerca de la mitad de las muertes por aludes; el 2 (limitado), alrededor de un tercio. No es que sean los más peligrosos: es que en esos días sale mucha gente y la nieve parece buena. Fíjate en el problema, las orientaciones y las cotas que señala el boletín.</p>') +
            seccion("El boletín de AEMET", "Cómo leer el parte de aludes",
                    '<p class="lead-p">AEMET publica el <b>boletín de información nivológica y de peligro de aludes</b> siguiendo la escala y los problemas típicos europeos. Vale para el terreno fuera de las pistas de esquí balizadas y abiertas. Se consulta en <a href="https://www.aemet.es/es/eltiempo/prediccion/montana" target="_blank" rel="noopener">aemet.es → Predicción → Montaña</a>, eligiendo la zona.</p>'
                    '<div class="gd-dos"><div><h3>Qué zonas y cuándo sale</h3><ul class="gd-reglas">'
                    '<li><b>Pirineo navarro y aragonés:</b> a diario, válido para el día siguiente. Suele empezar a finales de noviembre o en diciembre.</li>'
                    '<li><b>Guadarrama y sierras del Cordel y Peña Labra:</b> una vez por semana (normalmente el jueves), válido de viernes a domingo.</li>'
                    '<li><b>Picos de Europa:</b> una vez por semana (normalmente el viernes por la mañana), válido de viernes a domingo.</li>'
                    '<li>En estas tres zonas la temporada suele arrancar a finales de diciembre o en enero, según la nieve. <b>Gredos no tiene boletín</b>.</li>'
                    '<li>El Pirineo catalán lo cubre el ICGC, y el Arán, su propio servicio.</li></ul></div>'
                    '<div><h3>Lo que trae, en orden</h3><ol class="gd-reglas">'
                    '<li><b>Estimación del nivel de peligro:</b> el nivel (1 a 5) del día, con los problemas típicos, las cotas, las orientaciones, el tamaño de los aludes esperables y la distribución (si es en pocos sitios o generalizado). En los semanales, también un avance para los días siguientes.</li>'
                    '<li><b>Estado del manto y observaciones recientes:</b> desde qué cota hay nieve continua, espesores y cómo son las capas.</li>'
                    '<li><b>Evolución del manto y peligro de aludes:</b> qué va a cambiar ese día y por qué.</li>'
                    '<li><b>Predicción meteorológica:</b> el tiempo, con los datos de la atmósfera libre (isocero y viento en altura).</li>'
                    '<li><b>Evolución para los siguientes días:</b> hacia dónde va el peligro.</li></ol></div></div>'
                    '<h3 style="margin-top:30px">Cómo leerlo, paso a paso</h3><ol class="gd-pasos">'
                    '<li><b>El nivel</b><span>Fíjate si cambia con la altitud (un nivel por encima de una cota y otro por debajo) o a lo largo del día: con nieve húmeda puede subir por la tarde.</span></li>'
                    '<li><b>El problema</b><span>Nieve reciente, venteada, capas débiles persistentes, nieve húmeda o deslizamientos basales. Te dice qué buscar y cómo evitarlo (lo tienes explicado arriba).</span></li>'
                    '<li><b>Dónde</b><span>Las cotas y la rosa de orientaciones marcan las laderas peligrosas. Compáralas con tu ruta: ¿pasas por esas orientaciones y por encima de esa cota, en pendientes de más de 30°?</span></li>'
                    '<li><b>Cuándo</b><span>Si el problema es nieve húmeda, la hora importa: madruga y sal de las pendientes antes de que caliente.</span></li>'
                    '<li><b>El texto</b><span>Lee el estado del manto y la evolución: ahí están los detalles que no caben en los iconos (dónde se observaron aludes, qué capa preocupa, cómo influye el viento previsto).</span></li>'
                    '<li><b>Compruébalo en el terreno</b><span>El boletín describe una zona amplia. Busca sobre el sitio las señales del problema que anuncia y, si lo que ves es peor, hazle caso al terreno.</span></li></ol>'
                    '<h3 style="margin-top:38px">Un parte real, explicado</h3><p>Boletín de AEMET para Guadarrama emitido el jueves 29 de enero de 2026. Cada número de la imagen corresponde a una explicación.</p>'
                    '<div class="bpa"><figure class="bpa-fig"><div class="bpa-img"><img src="/img/guias/boletin-aludes-aemet-guadarrama.webp" width="794" height="1006" loading="lazy" alt="Boletín de peligro de aludes de AEMET para Guadarrama del 29 de enero de 2026: nivel notable por encima de 2.100 m y limitado por debajo, con placas de viento y nieve reciente">' +
                    "".join('<span class="bpa-n" style="left:%s%%;top:%s%%">%d</span>' % (x, y, k + 1) for k, (x, y, _, _) in enumerate(BPA_NOTAS)) +
                    '</div><figcaption>Fuente: <a href="https://www.aemet.es/es/eltiempo/prediccion/montana" target="_blank" rel="noopener">AEMET</a>, boletín de información nivológica y de peligro de aludes de Guadarrama.</figcaption></figure>'
                    '<ol class="bpa-lista">' + "".join('<li><span class="bpa-n">%d</span><div><b>%s</b> %s</div></li>' % (k + 1, e(t), x) for k, (_, _, t, x) in enumerate(BPA_NOTAS)) + '</ol></div>'
                    '<div class="panel" style="margin-top:22px"><p class="eyebrow">Lo que nos dice este parte</p>'
                    '<p><b>Viernes:</b> por encima de 2.100 m el peligro es notable (3), así que una sola persona puede desencadenar una placa de viento en las laderas empinadas. Las placas están por encima de 2.000 m y en todas las orientaciones, algo poco habitual que indica viento cambiante. Los aludes serían de tamaño mediano, suficientes para sepultar a una persona. La nieve reciente añade aludes pequeños a cualquier cota. En la práctica: nada de laderas de más de 30° cargadas en la parte alta; mejor lomas anchas y pendientes suaves, y mucha atención al pasar cerca de crestas y collados.</p>'
                    '<p><b>Domingo:</b> el viento sigue siendo el problema arriba, pero la nieve reciente da paso a la <b>nieve húmeda por debajo de 2.100 m</b>: llega un calentamiento. Toca madrugar y salir de las pendientes antes de las horas centrales.</p>'
                    '<p class="small muted">La imagen es solo la primera página. En las siguientes vienen el estado del manto, la evolución y la previsión meteorológica, que explican el porqué de estos iconos: léelas siempre.</p></div>', False, "boletin") +
            '<section class="section alt" id="laderas"><div class="wrap"><p class="eyebrow">Sobre el terreno</p><h2>Cómo leer una ladera</h2>'
            '<div class="gd-fig">' + guias_svg.nieve_pendiente() + '</div>' +
            '<div class="gd-pasos gd-pasos-sin">' + "".join('<li><b>%s</b><span>%s</span></li>' % (e(t), e(x)) for t, x in laderas) + '</div>'
            '<h3 style="margin-top:34px">Señales de alarma</h3><p>Si ves cualquiera de estas, el manto te está avisando: aléjate de las pendientes de más de 30°.</p>'
            '<ul class="gd-reglas gd-alarma">' + "".join("<li>%s</li>" % e(x) for x in alarmas) + '</ul></div></section>' +
            seccion("Planificar", "Antes de salir y durante la actividad",
                    '<div class="gd-dos"><div><h3>Antes de salir</h3><ul class="gd-reglas">' + "".join("<li>%s</li>" % e(x) for x in antes) + '</ul></div>'
                    '<div><h3>Durante la actividad</h3><ul class="gd-reglas">' + "".join("<li>%s</li>" % e(x) for x in durante) + '</ul></div></div>') +
            seccion("Si ocurre", "Rescate de un compañero: cada minuto cuenta",
                    '<p class="lead-p">Si una persona sepultada se saca en los primeros 15 minutos, la gran mayoría sobrevive; a partir de ahí las posibilidades caen muy deprisa. El rescate lo hace el propio grupo: la ayuda de fuera casi nunca llega a tiempo.</p>'
                    '<ol class="gd-pasos">' + "".join('<li><b>%s</b><span>%s</span></li>' % (e(t), e(x)) for t, x in rescate) + '</ol>', True) +
            '<section class="section"><div class="wrap split"><div class="stack" style="gap:0">' + block("Preguntas frecuentes", faq_html(LEER_NIEVE_FAQ)) +
            '</div><div class="sticky"><div class="panel"><p class="eyebrow">Boletines y datos</p><ul class="gd-links">'
            '<li><a href="https://www.aemet.es/es/eltiempo/prediccion/montana" target="_blank" rel="noopener">AEMET: predicción de montaña y boletín de aludes</a> (Pirineo, Picos de Europa, Cordel y Peña Labra, Guadarrama)</li>'
            '<li><a href="https://www.icgc.cat/" target="_blank" rel="noopener">ICGC</a> (Institut Cartogràfic i Geològic de Catalunya): boletín del Pirineo catalán</li>'
            '<li><a href="/nieve/">Estado de la nieve</a> y <a href="/meteo/">meteorología</a> de nuestras sierras</li></ul>'
            '<p class="small muted">Problemas típicos y escala de peligro según el <a href="https://www.avalanches.org/" target="_blank" rel="noopener">EAWS</a> (servicios europeos de aviso de aludes).</p></div>'
            '<div class="panel" style="margin-top:16px"><p class="eyebrow">Aprende con guías</p><p>En nuestros <a href="/actividades/cursos-alpinismo/">cursos de alpinismo</a> practicamos sobre el terreno la lectura de la nieve, el uso del ARVA y el rescate.</p></div></div></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Artículos", "/articulos/"), ("Cómo leer la nieve", path)]), faq_ld(LEER_NIEVE_FAQ)]
    ld.append(articulo_ld(path, "Cómo leer la nieve y el peligro de aludes", "Cómo cambia el manto, placas de viento, tipos de aludes, el boletín de AEMET explicado y cómo leer una ladera.", "2026-11-19"))
    page(path, "Cómo leer la nieve y el peligro de aludes | Ad Astra",
         "Manto de nieve, placas de viento, tipos de aludes, el boletín de AEMET explicado paso a paso y cómo leer una ladera antes de meterte en ella.",
         body, "art", ld, priority="0.6")


ART_ICO = {
    "nieve": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M4 54 L24 22 L32 32 L40 18 L60 54Z" fill="#6b5a4a"/><path d="M24 22 L18 32 L24 30 L28 34 L32 32Z M40 18 L35 27 L40 25 L44 29 L47 28Z" fill="#fff"/><path d="M40 18 L60 54 L50 54 L44 40Z" fill="#e8574a" opacity=".55"/></svg>',
    "mochila": '<svg viewBox="0 0 64 64" aria-hidden="true"><rect x="16" y="12" width="32" height="44" rx="10" fill="#e9a53b"/><rect x="20" y="30" width="24" height="14" rx="4" fill="#c27f1f"/><path d="M24 12 Q32 2 40 12" fill="none" stroke="#8a5a14" stroke-width="4"/><rect x="16" y="18" width="32" height="8" rx="3" fill="#c27f1f"/></svg>',
    "uv": '<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="12" fill="#f5c84b"/><g stroke="#f5c84b" stroke-width="4" stroke-linecap="round"><path d="M32 6v8M32 50v8M6 32h8M50 32h8M13 13l6 6M45 45l6 6M13 51l6-6M45 19l6-6"/></g><text x="32" y="37" text-anchor="middle" font-family="Inter,sans-serif" font-size="13" font-weight="900" fill="#1b120c">UV</text></svg>',
    "capas": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M14 20 L24 12 H40 L50 20 L46 28 L42 26 V54 H22 V26 L18 28Z" fill="#6fb3e0"/><path d="M22 26 V54 H42 V26" fill="none" stroke="#e9a53b" stroke-width="4"/><path d="M28 12 Q32 18 36 12" fill="none" stroke="#7cc47f" stroke-width="4"/></svg>',
    "escalas": '<svg viewBox="0 0 64 64" aria-hidden="true"><rect x="8" y="44" width="12" height="12" rx="2" fill="#4caf50"/><rect x="26" y="30" width="12" height="26" rx="2" fill="#e6c32e"/><rect x="44" y="12" width="12" height="44" rx="2" fill="#e8574a"/></svg>',
    "invernal": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M20 8 L26 8 L26 56 L20 56Z" fill="#b9a593"/><path d="M8 10 Q24 2 44 12 L40 16 Q24 10 12 14Z" fill="#bfe0f7"/><path d="M34 40 H58 V46 H34Z" fill="#6b5a4a"/><g fill="#bfe0f7"><path d="M36 46 l2 8 l2-8Z M42 46 l2 8 l2-8Z M48 46 l2 8 l2-8Z M54 46 l2 8 l2-8Z"/></g></svg>',
    "altura": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M4 56 L26 16 L36 32 L42 24 L60 56Z" fill="#6b5a4a"/><path d="M26 16 L20 28 L26 26 L30 30Z" fill="#fff"/><circle cx="50" cy="14" r="8" fill="none" stroke="#4fb3e8" stroke-width="4"/><text x="50" y="18" text-anchor="middle" font-family="Inter,sans-serif" font-size="10" font-weight="900" fill="#4fb3e8">O₂</text></svg>',
    "botiquin": '<svg viewBox="0 0 64 64" aria-hidden="true"><rect x="8" y="18" width="48" height="36" rx="8" fill="#e8574a"/><path d="M24 18 V12 H40 V18" fill="none" stroke="#a93226" stroke-width="4"/><path d="M28 26 H36 V32 H42 V40 H36 V46 H28 V40 H22 V32 H28Z" fill="#fff"/></svg>',
    "tormenta": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M16 36 A10 10 0 0 1 18 16 A14 14 0 0 1 44 14 A10 10 0 0 1 50 36Z" fill="#8a7d9e"/><path d="M34 32 L24 48 H32 L28 60 L42 42 H34 L38 32Z" fill="#f5c84b"/></svg>',
    "orientacion": '<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="24" fill="#f3e9df" stroke="#7cc47f" stroke-width="5"/><path d="M32 12 L38 32 L32 52 L26 32Z" fill="#b9a593"/><path d="M32 12 L38 32 H26Z" fill="#e8574a"/><circle cx="32" cy="32" r="3" fill="#1b120c"/></svg>',
    "vivac": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M6 54 L32 14 L58 54Z" fill="#e9a53b"/><path d="M32 14 L24 54 H40Z" fill="#a8701e"/><circle cx="50" cy="12" r="6" fill="#f3e9df"/><circle cx="53" cy="10" r="5" fill="#1b120c"/></svg>',
    "seguro": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M32 6 L54 14 V30 Q54 48 32 58 Q10 48 10 30 V14Z" fill="#4fb3e8"/><path d="M28 22 H36 V28 H42 V36 H36 V42 H28 V36 H22 V28 H28Z" fill="#fff"/></svg>',
    "raquetas": '<svg viewBox="0 0 64 64" aria-hidden="true"><ellipse cx="22" cy="34" rx="10" ry="22" fill="none" stroke="#4fb3e8" stroke-width="5"/><path d="M14 30 H30 M14 40 H30" stroke="#4fb3e8" stroke-width="3"/><path d="M44 6 L50 58" stroke="#e8574a" stroke-width="6" stroke-linecap="round"/><path d="M40 52 Q52 60 58 48" fill="none" stroke="#e8574a" stroke-width="4"/></svg>',
    "escalada": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M6 58 L22 14 L30 10 L40 18 L58 58Z" fill="#8d8378"/><path d="M24 56 L26 40 L32 30 L30 18" stroke="#e9a53b" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="32" cy="30" r="4" fill="#f3e9df"/><circle cx="26" cy="40" r="4" fill="#f3e9df"/></svg>',
    "gredos": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M2 56 L18 26 L26 36 L36 12 L46 30 L52 22 L62 56Z" fill="#6b5a4a"/><path d="M36 12 L31 24 L36 21 L40 26Z" fill="#fff"/><ellipse cx="34" cy="50" rx="10" ry="3" fill="#4fb3e8"/></svg>',
}


def build_articulos():
    path = "/articulos/"
    cards = "".join('<a class="art-card" href="%s"><span class="art-ico">%s</span><div><h2>%s</h2><p>%s</p><span class="art-mas">Leer el artículo →</span></div></a>' % (h, ART_ICO[ic], e(t), e(d)) for h, t, d, ic in ARTICULOS)
    body = (hero("Artículos", "Artículos de montaña", "Guías prácticas escritas por nuestros guías: nieve y aludes, material de invierno, grados de dificultad, seguridad, orientación, rutas de Gredos y más.", METEO_IMG,
                 [("Inicio", "/"), ("Artículos", "")]) +
            "".join('<section class="section%s"><div class="wrap"><p class="eyebrow">Artículos</p><h2>%s</h2><div class="art-grid art-grid2">' % (" alt" if i % 2 else "", e(c)) +
                    "".join('<a class="art-card" href="%s"><span class="art-ico">%s</span><div><h3>%s</h3><p>%s</p><span class="art-mas">Leer el artículo →</span></div></a>' % (h, ART_ICO[ic], e(t), e(d)) for h, t, d, ic in arts) +
                    '</div></div></section>' for i, (c, arts) in enumerate(ART_GRUPOS)))
    ld = [crumbs_ld([("Inicio", "/"), ("Artículos", path)]), {"@context": "https://schema.org", "@type": "ItemList", "name": "Artículos de montaña de Guías Ad Astra", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": url(h), "name": t} for i, (h, t, _, _) in enumerate(ARTICULOS)]}]
    page(path, "Artículos de montaña: técnica, seguridad y rutas | Ad Astra",
         "Guías prácticas de montaña: nieve y aludes, crampones y piolet, grados de escalada, mal de altura, tormentas, orientación, vivac y rutas de Gredos.",
         body, "art", ld, priority="0.6")


PRENDAS = {
    "1": ["Camiseta térmica (manga corta o larga)", "Mallas térmicas", "Calcetines técnicos", "Braga de cuello fina"],
    "2": ["Forro polar", "Chaqueta de fibra (tipo Primaloft)", "Softshell fino", "Chaleco"],
    "3": ["Chaqueta impermeable de membrana (tipo Gore-Tex)", "Cortavientos", "Softshell", "Cubrepantalón impermeable"],
    "4": ["Plumífero (plumas)", "Chaqueta de fibra gruesa", "Guantes gordos o manoplas", "Gorro"],
}


def build_capas():
    path = "/teoria-de-las-capas/"
    capas = [("1", "Capa base", "#7cc47f", "Va pegada a la piel y su trabajo es sacar el sudor hacia fuera para que la piel esté seca. Camiseta (y mallas si hace frío) de fibra sintética, lana merina o mezcla. La merina abriga aunque esté húmeda y no huele; la sintética seca antes."),
             ("2", "Capa intermedia", "#e9a53b", "Guarda el calor del cuerpo. Un forro polar transpira bien y sirve casi siempre; una chaqueta fina de fibra abriga más y se guarda en poco sitio. Elige el grosor según el frío: si subes sudando, es demasiado."),
             ("3", "Capa exterior", "#6fb3e0", "Protege de la lluvia, la nieve y el viento. Una chaqueta con membrana impermeable y transpirable para el mal tiempo, o un cortavientos o softshell cuando solo hay viento. Las cremalleras de ventilación ayudan a no empaparte por dentro."),
             ("4", "Capa de reserva", "#c9a7e8", "No siempre se cuenta, pero en montaña es clave: un plumífero o chaqueta de fibra que va en la mochila para la cima, las paradas, una espera o una emergencia. Te la pones al parar, encima de todo, y te la quitas antes de volver a andar.")]
    tabla = [("Calor (más de 20 °C)", "Camiseta técnica de manga corta", "—", "Cortavientos ligero en la mochila"),
             ("Templado (10 a 20 °C)", "Camiseta técnica", "Forro polar fino en la mochila", "Chaqueta impermeable en la mochila"),
             ("Fresco (0 a 10 °C)", "Camiseta térmica de manga larga", "Forro polar", "Chaqueta impermeable + plumífero ligero para parar"),
             ("Frío (bajo 0 °C)", "Camiseta y mallas térmicas (merina)", "Forro polar grueso o chaqueta de fibra", "Chaqueta y cubrepantalón impermeables + plumífero, guantes dobles y gorro")]
    consejos = ["Empieza a andar con un poco de frío: en diez minutos entrarás en calor.",
                "Quita capa antes de empezar a sudar, no después; ponte la de reserva en cuanto pares.",
                "Lo que sobra, a la mochila: es mejor parar un minuto que empaparse.",
                "Ventila: abre cremalleras al subir y ciérralas en las crestas con viento.",
                "Lleva siempre una capa seca de recambio y, en invierno, guantes de repuesto."]
    body = (hero("Artículos", "La teoría de las capas", "Cómo vestirse para la montaña: tres capas que se ponen y se quitan según el esfuerzo y el tiempo, más una de reserva para las paradas. Explicado en viñetas.", METEO_IMG,
                 [("Inicio", "/"), ("Artículos", "/articulos/"), ("Teoría de las capas", "")], '<a class="btn btn-primary" href="#vinetas">Ver las viñetas</a><a class="btn btn-ghost" href="/como-preparar-la-mochila/">Preparar la mochila</a>') +
            '<section class="section" id="vinetas"><div class="wrap"><p class="eyebrow">La idea</p><h2>Varias capas finas abrigan más que una gorda</h2>'
            '<p class="lead-p">El aire que queda entre capa y capa también aísla, y con varias prendas puedes ajustar el abrigo a cada momento: quitar al subir, poner al parar. El objetivo es estar seco y a buena temperatura todo el día.</p>'
            '<div class="gd-fig gd-cm">' + guias_svg.capas_comic() + '</div>'
            '<div class="gd-capas">' + "".join('<article style="--c:%s"><span>%s</span><h3>%s</h3><ul class="gd-prendas">%s</ul><p>%s</p></article>' % (c, n, e(t), "".join("<li>%s</li>" % e(pr) for pr in PRENDAS[n]), e(x)) for n, t, c, x in capas) + '</div></div></section>'
            '<section class="section alt"><div class="wrap"><p class="eyebrow">Qué ponerse</p><h2>Según la temperatura</h2><div class="gd-tw"><table class="gd-t"><thead><tr><th>Tiempo</th><th>1 · Base</th><th>2 · Intermedia</th><th>3 y 4 · Exterior y reserva</th></tr></thead><tbody>' +
            "".join("<tr><th>%s</th><td>%s</td><td>%s</td><td>%s</td></tr>" % tuple(e(x) for x in f) for f in tabla) +
            '</tbody></table></div><p class="muted small">Orientativo: cuenta también el viento, la altitud (unos 6 °C menos por cada 1.000 m) y lo intensa que sea la actividad.</p></div></section>'
            '<section class="section"><div class="wrap"><p class="eyebrow">Errores típicos</p><h2>Lo que no hay que hacer</h2><div class="gd-fig gd-cm">' + guias_svg.capas_errores() + '</div>'
            '<ul class="gd-reglas">' + "".join("<li>%s</li>" % e(x) for x in consejos) + '</ul></div></section>' +
            '<section class="section alt"><div class="wrap split"><div class="stack" style="gap:0">' + block("Preguntas frecuentes", faq_html(CAPAS_FAQ)) +
            '</div><div class="sticky"><div class="panel"><p class="eyebrow">Fuentes</p><p class="small">Basado en las guías de <a href="https://www.salomon.com/es-es/running/trail-running-advice/how-properly-dress-layers-the-three-layer-system/" rel="noopener" target="_blank">Salomon</a> y <a href="https://www.iloveski.org/es/2021/10/01/sistema-por-capas-vestirse-en-la-montana/" rel="noopener" target="_blank">iLoveSki</a> y en la experiencia de nuestros guías.</p></div></div></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Artículos", "/articulos/"), ("Teoría de las capas", path)]), faq_ld(CAPAS_FAQ)]
    ld.append(articulo_ld(path, "La teoría de las capas: cómo vestirse para la montaña", "Capa base, intermedia, exterior y de reserva explicadas en viñetas, con el tipo de prenda de cada una.", "2026-11-18"))
    page(path, "Teoría de las capas: cómo vestirse en montaña | Ad Astra",
         "La teoría de las tres capas (base, intermedia y exterior) más la capa de reserva, explicada con viñetas: qué ponerse según la temperatura y errores típicos.",
         body, "art", ld, priority="0.6", scripts=COMIC_FONTS)


def build_caudales():
    path = "/barrancos-caudal/"
    body = (hero("Herramientas", "Caudal de los barrancos", "Estado de nuestros barrancos con el caudal de los aforos oficiales del SAIH Tajo y del SAIH Duero, la tendencia de las últimas horas y la lluvia prevista. Se actualiza cada hora.", METEO_IMG,
                 [("Inicio", "/"), ("Caudal de barrancos", "")], '<a class="btn btn-primary" href="#estado">Ver el estado</a><a class="btn btn-ghost" href="/meteo/">Meteorología</a>') +
            '<section class="section" id="estado"><div class="wrap"><div id="rio-lista" class="rio"><p class="mt-cargando">Cargando caudales…</p></div></div></section>' +
            '<section class="section alt"><div class="wrap split"><div class="stack" style="gap:0">' + block("Preguntas frecuentes", faq_html(CAUDAL_FAQ)) +
            '</div><div class="sticky"><div class="panel"><p class="eyebrow">Aviso</p><p>Datos oficiales en tiempo real, provisionales. Los umbrales son orientativos y los fija Guías Ad Astra para sus barrancos. En barrancos, la última palabra la tiene siempre lo que se ve en el sitio.</p></div></div></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Caudal de barrancos", path)]), faq_ld(CAUDAL_FAQ)]
    ld.append(app_ld(path, "Caudal de barrancos en tiempo real", "Caudal de los barrancos de los Hoyos, Papúos, Mazobre y Valporquero con los aforos del SAIH Tajo y Duero."))
    page(path, "Caudal de barrancos hoy: Jerte, Mazobre y Valporquero | Ad Astra",
         "Caudal en tiempo real de los barrancos de los Hoyos, Papúos, Mazobre y Valporquero con los aforos del SAIH Tajo y Duero, tendencia y lluvia prevista.",
         body, "her", ld, priority="0.6", scripts='<script src="/js/rios.js" defer></script>')


def build_meteo():
    path = "/meteo/"
    regiones = ", ".join(REGIONES)
    body = (hero("Herramientas", "Meteorología de montaña", "Previsión a 15 días en cumbre y en el pueblo base para %d macizos de España, calculada cada 6 horas directamente con los modelos ECMWF, GFS, ICON y AROME." % len(MACIZOS), METEO_IMG,
                 [("Inicio", "/"), ("Meteorología de montaña", "")], '<a class="btn btn-primary" href="#previsiones">Ver previsiones</a><a class="btn btn-ghost" href="#como">Cómo se calcula</a>') +
            keybar([("Macizos", "%d" % len(MACIZOS)), ("Modelos", "ECMWF · GFS · ICON · AROME"), ("Alcance", "15 días"), ("Actualización", "4 veces al día")]) +
            '<section class="section" id="previsiones"><div class="wrap">' + meteo_selector() + '<div id="mt-index" class="mt"><p class="mt-cargando">Cargando previsiones…</p></div><div id="mt-mac" class="mt" hidden></div>'
            '<noscript><ul>' + "".join('<li><a href="/meteo/%s/">%s</a></li>' % (m["id"], e(m["nombre"])) for m in MACIZOS) + '</ul></noscript></div></section>' +
            '<section class="section alt" id="como"><div class="wrap split"><div class="stack" style="gap:0">' + meteo_metodo() + block("Preguntas frecuentes", faq_html(METEO_FAQ)) +
            '</div><div class="sticky"><div class="panel"><p class="eyebrow">Macizos</p>' + "".join(
                '<h3 style="font-size:1.2rem;margin-top:6px">%s</h3><p>%s</p>' % (e(rg), " · ".join('<a href="/meteo/%s/">%s</a>' % (m["id"], e(m["corto"])) for m in MACIZOS if m["region"] == rg)) for rg in REGIONES) +
            '</div></div></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Meteorología de montaña", path)]), faq_ld(METEO_FAQ)]
    ld.append(app_ld(path, "Meteorología de montaña", "Previsión del tiempo en montaña a 15 días en cumbre y base, con varios modelos y avisos de AEMET.", "WeatherApplication"))
    page(path, "Tiempo en montaña: previsión a 15 días en cumbre | Ad Astra",
         "Previsión del tiempo en montaña a 15 días para %d macizos: temperatura y viento en cumbre, nieve, isocero y tormentas. Modelos ECMWF, GFS, ICON y AROME." % len(MACIZOS),
         body, "her", ld, priority="0.8", scripts='<script src="/js/meteo.js" defer></script>')
    for m in MACIZOS:
        build_meteo_macizo(m)

def build_meteo_macizo(m):
    path = "/meteo/%s/" % m["id"]
    c, b = m["cumbre"], m["base"]
    fmt = lambda x: "{:,}".format(x).replace(",", ".")
    h1 = "Tiempo en %s" % m["nombre"]
    lead = "Previsión de montaña a 15 días en %s (%s m) y %s (%s m): temperatura, viento en cumbre, precipitación, nieve, isocero y tormentas. %s" % (c["nombre"], fmt(c["alt"]), b["nombre"], fmt(b["alt"]), m["texto"])
    acts = [x for x in ACTIVITIES if x["slug"] in METEO_ACT.get(m["id"], [])]
    otros = [x for x in MACIZOS if x["region"] == m["region"] and x["id"] != m["id"]]
    lateral = ""
    if acts:
        lateral += '<div class="panel"><p class="eyebrow">Con guía en la zona</p>' + "".join(
            '<a class="btn btn-ghost btn-block" href="/actividades/%s/">%s</a>' % (x["slug"], e(x["title"])) for x in acts) + '</div>'
    if otros:
        lateral += '<div class="panel"><p class="eyebrow">%s</p>%s<a href="/meteo/">Todos los macizos</a></div>' % (e(m["region"]), "".join('<a href="/meteo/%s/">%s</a>' % (x["id"], e(x["nombre"])) for x in otros))
    body = (hero("Meteorología de montaña", e(h1), e(lead), METEO_IMG, [("Inicio", "/"), ("Meteorología", "/meteo/"), (m["nombre"], "")]) +
            keybar([("Cumbre", "%s · %s m" % (c["nombre"], fmt(c["alt"]))), ("Base", "%s · %s m" % (b["nombre"], fmt(b["alt"]))), ("Modelos", "ECMWF · GFS · ICON · AROME"), ("Actualización", "4 veces al día")]) +
            '<section class="section" id="previsiones"><div class="wrap">' + meteo_selector(m["id"]) + '<div id="mt-mac" class="mt" data-id="%s"><p class="mt-cargando">Cargando previsión…</p></div></div></section>' % m["id"] +
            '<section class="section alt"><div class="wrap split"><div class="stack" style="gap:0">' + meteo_metodo() + block("Preguntas frecuentes", faq_html(METEO_FAQ[:4])) +
            '</div><div class="sticky" style="display:grid;gap:18px">' + lateral + '</div></div></section>')
    ld = [crumbs_ld([("Inicio", "/"), ("Meteorología de montaña", "/meteo/"), (m["nombre"], path)]), faq_ld(METEO_FAQ[:4]),
          {"@context": "https://schema.org", "@type": "Place", "name": c["nombre"], "geo": {"@type": "GeoCoordinates", "latitude": c["lat"], "longitude": c["lon"], "elevation": c["alt"]},
           "containedInPlace": {"@type": "Place", "name": m["nombre"]}}]
    nom = {"gredos-macizo-central": "Gredos y el Almanzor", "gredos-macizo-oriental": "Gredos Oriental"}.get(m["id"], m["nombre"])
    title = "Tiempo en %s: previsión de montaña a 15 días" % nom
    if len(title) > 64:
        title = "Tiempo en %s: previsión de montaña" % nom
    desc = _short("Previsión meteorológica de montaña en %s: tiempo en %s (%s m) y %s a 15 días, viento en cumbre, nieve, isocero y tormentas con ECMWF, GFS, ICON y AROME." % (m["nombre"], c["nombre"], fmt(c["alt"]), b["nombre"]), 158)
    page(path, title, desc, body, "her", ld, priority="0.6", scripts='<script src="/js/meteo.js" defer></script>')

def build_service(s):
    path = "/%s/" % s["slug"]
    form = ('<form class="book" data-book data-presupuesto data-full data-title="%s" data-price="" id="reservar" novalidate><p class="eyebrow">Sin compromiso</p><h2>Pide información</h2>'
            '<div class="row2"><div class="field"><label for="s-nombre">Nombre</label><input id="s-nombre" name="nombre" autocomplete="given-name"></div><div class="field"><label for="s-ape">Apellidos</label><input id="s-ape" name="apellidos" autocomplete="family-name"></div></div>'
            '<div class="field"><label for="s-ent">Entidad (opcional)</label><input id="s-ent" name="entidad" autocomplete="organization" placeholder="Ayuntamiento, club, empresa…"></div>'
            '<div class="field"><label for="s-email">Correo electrónico</label><input id="s-email" name="email" type="email" autocomplete="email" inputmode="email"></div>'
            '<div class="field"><label for="s-tel">Teléfono</label><input id="s-tel" name="telefono" type="tel" autocomplete="tel" inputmode="tel"></div>'
            '<div class="field"><label for="s-com">Cuéntanos tu proyecto</label><textarea id="s-com" placeholder="Zona, fechas, número de personas o lo que necesites…"></textarea></div>'
            '<p class="err" role="alert"></p><button class="btn btn-wa btn-block" type="submit">%s Enviar por WhatsApp</button><p class="hint">Te respondemos en 24-48 horas con una propuesta.</p></form>' % (e(s["title"]), WA_SVG))
    left = [block("Qué hacemos", prose(s["intro"])),
            block("Servicios", '<div class="two">%s</div>' % "".join('<div class="panel"><h3>%s</h3><p class="muted">%s</p></div>' % (e(t), e(x)) for t, x in s["servicios"])),
            block("Para quién", ticks(s["para"], "cols")),
            block("Cómo trabajamos", '<ol class="stages">%s</ol>' % "".join('<li><span class="d">Paso %d</span><h4>%s</h4><p>%s</p></li>' % (i + 1, e(t), e(x)) for i, (t, x) in enumerate(s["proceso"]))),
            block("Preguntas frecuentes", faq_html(s["faq"]))]
    body = (hero("Servicios profesionales", e(s["title"]), e(s["lead"]), s["img"], [("Inicio", "/"), ("Otros", ""), (s["title"], "")], '<a class="btn btn-primary" href="#reservar">Pedir información</a>') +
            '<section class="section"><div class="wrap split"><div class="stack" style="gap:0">%s</div><div class="sticky">%s</div></div></section>' % ("".join(left), form))
    ld = [crumbs_ld([("Inicio", "/"), (s["title"], path)]), faq_ld(s["faq"]),
          {"@context": "https://schema.org", "@type": "Service", "name": s["title"], "description": s["seo_desc"], "serviceType": s["title"], "provider": {"@id": D + "/#empresa"},
           "areaServed": ["Salamanca", "Ávila", "Cáceres", "Valladolid", "Castilla y León"], "url": url(path),
           "hasOfferCatalog": {"@type": "OfferCatalog", "name": s["title"], "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": x}} for t, x in s["servicios"]]}},
          {"@context": "https://schema.org", **ORG}]
    page(path, s["seo_title"], s["seo_desc"], body, "otr", ld, image=s["img"], priority="0.6")

# ---------------------------------------------------------------- build
# ---------------------------------------------------------------- páginas de cada barranco, ferrata, cueva o ruta
import unicodedata as _ud
def slugify(t):
    t = _ud.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return "-".join("".join(c if c.isalnum() else " " for c in t).split())

def _option_pages():
    """Una página por cada recorrido con nombre propio (barranco, ferrata, cueva, ruta), dentro de su actividad."""
    out, seen = [], set()
    for a in ACTIVITIES:
        if a.get("kind") not in ("options", "zona") or a["slug"] in ("via-ferrata-salamanca", "barranquismo-cueva-valporquero-sima-de-perlas"):
            continue
        for o in a.get("options", []):
            n = o["name"]
            if n.startswith("Cueva de Valporquero") or n.startswith("Cancho de la Muela") or n.startswith("Vía ferrata de La Muela") or n.startswith("Nivel "):
                continue
            k = slugify(n)
            if k in seen:
                continue
            seen.add(k)
            out.append((a, o, "/actividades/%s/%s/" % (a["slug"], k)))
    return out
OPTION_PAGES = _option_pages()
OPTION_URL = {o["name"]: p for _, o, p in OPTION_PAGES}

def _short(t, n):
    return t if len(t) <= n else t[: n - 1].rsplit(" ", 1)[0] + "…"

def build_option(a, o, path):
    n, place, region = o["name"], o["place"], o["place"].split("(")[-1].rstrip(")") if "(" in o["place"] else o["place"]
    tipo = ("barranco" if "arranco" in n else "vía ferrata" if "ferrata" in n.lower() else "cueva" if n.startswith("Cueva") else "ruta")
    h1 = "%s con guía" % n
    crumbs = [("Inicio", "/"), ("Actividades", "/actividades/"), (a["title"], "/actividades/%s/" % a["slug"]), (n, "")]
    specs = list(o.get("specs", []))
    kb = [("Dónde", place), ("Duración", o["dur"]), ("Precio", "%d € / persona" % o["price"]), ("Incluye", "Guía titulado, material y seguro")]
    art = ("el " if n.startswith("Barranco") else "la " if n.startswith(("Cueva", "Vía", "Ruta", "Ascensión", "Escalada")) else "") + (n[0].lower() + n[1:] if n.startswith(("Barranco", "Cueva", "Vía", "Ruta", "Ascensión", "Escalada")) else n)
    left = [block("Cómo es", prose([o["desc"]]) + (ticks(specs) if specs else ""))]
    if a.get("intro"):
        left.append(block("La actividad", prose(a["intro"])))
    if a.get("incluye") or a.get("traer"):
        inner = '<div class="two">'
        if a.get("incluye"):
            inner += '<div class="panel"><h3>Nosotros ponemos</h3>%s</div>' % ticks(a["incluye"])
        if a.get("traer"):
            inner += '<div class="panel"><h3>Tienes que traer</h3>%s</div>' % ticks(a["traer"])
        left.append(block("Qué incluye", inner + "</div>"))
    if a.get("epoca"):
        left.append(block("Mejor época", prose([a["epoca"]])))
    if a.get("que_es"):
        left.append(block(a["que_es"][0], prose(a["que_es"][1])))
    if a.get("req"):
        left.append(block("Requisitos", ticks(a["req"])))
    faq = [("¿Dónde es %s?" % art,
            "En %s. Te enviamos el punto de encuentro exacto y cómo llegar al confirmar la reserva." % place),
           ("¿Cuánto dura?", "Unas %s en total, contando aproximación, actividad y regreso." % o["dur"].replace(" aprox.", "")),
           ("¿Cuánto cuesta %s con guía?" % art,
            "%d € por persona, con guía titulado, seguro y el material técnico." % o["price"]),
           ("¿Hace falta experiencia?", o["desc"] + " Te asesoramos al reservar para elegir la opción que mejor encaja con tu grupo."),
           ("¿Cómo reservo?", "Elige el día y el número de personas en el formulario y envíanos la solicitud por WhatsApp. Te confirmamos disponibilidad y punto de encuentro.")]
    left.append(block("Preguntas frecuentes", faq_html(faq)))
    sib = [(oo, pp) for aa, oo, pp in OPTION_PAGES if aa is a and pp != path]
    if sib:
        left.append(block("Otras opciones: %s" % a["title"], '<div class="two">%s</div>' % "".join(
            '<a class="panel" href="%s" style="display:block"><h3>%s</h3><p class="muted">%s · %s · %d€</p></a>' % (pp, e(oo["name"]), e(oo["place"]), e(oo["dur"]), oo["price"]) for oo, pp in sib)))
    form = book_form("%s (%s)" % (n, a["title"]), [o], o["price"], opt_label="Opción")
    body = (hero(a["cat"], e(h1), e(o["desc"]), a["img"], crumbs, '<a class="btn btn-primary" href="#reservar">Reservar</a><a class="btn btn-ghost" href="/actividades/%s/">Ver todas las opciones</a>' % a["slug"]) + keybar(kb) +
            '<section class="section"><div class="wrap split"><div class="stack" style="gap:0">%s</div><div class="sticky" style="display:grid;gap:18px">%s</div></div></section>' % ("".join(left), form) + related(a))
    pf = place.replace(" (", ", ").rstrip(")")
    title = "%s con guía (%s) | %d€" % (n, pf, o["price"])
    if o.get("seo_title"):
        title = o["seo_title"] % o["price"] if "%d" in o["seo_title"] else o["seo_title"]
    elif len(title) > 62:
        title = "%s con guía, %s | %d€" % (n, region, o["price"])
    if not o.get("seo_title") and len(title) > 62:
        title = "%s con guía | %d€" % (n, o["price"])
    first = o["desc"].split(". ")[0].rstrip(".") + "."
    desc = "%s con guías titulados en %s: %s, %d € por persona con material y seguro. %s" % (n, pf, o["dur"], o["price"], first)
    if len(desc) > 160:
        desc = _short(desc, 158)
    ld = [crumbs_ld([("Inicio", "/"), ("Actividades", "/actividades/"), (a["title"], "/actividades/%s/" % a["slug"]), (n, path)]),
          {"@context": "https://schema.org", "@type": "Service", "name": h1, "description": desc, "image": a["img"], "serviceType": a["cat"], "url": url(path),
           "provider": {"@id": D + "/#empresa"},
           "offers": {"@type": "Offer", "price": o["price"], "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "url": url(path) + "#reservar", "seller": {"@id": D + "/#empresa"}}},
          {"@context": "https://schema.org", "@type": "TouristAttraction", "name": n, "address": {"@type": "PostalAddress", "addressLocality": place.split("(")[0].strip(), "addressRegion": region, "addressCountry": "ES"}},
          faq_ld(faq)]
    page(path, title, desc, body, "act", ld, "product", a["img"], "0.7")

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"), OUT)
    cfg = os.path.join(OUT, "config.js")
    c = open(cfg, encoding="utf-8").read().replace('calendarioURL: ""', 'calendarioURL: "",\n  // Carpeta donde está publicada la web ("" si está en la raíz del dominio)\n  base: "%s"' % BASE)
    open(cfg, "w", encoding="utf-8").write(c)
    build_home(); build_activities_index(); build_courses_index(); build_calendar(); build_rental(); build_about(); build_contact(); build_404(); build_calculator(); build_topografia(); build_meteo(); build_caudales(); build_nieve(); build_mochila(); build_capas(); build_leer_nieve(); build_articulos(); build_editor_gpx(); build_video3d(); build_lista_material(); build_herramientas(); build_uv(); build_nuevos()
    for a in ACTIVITIES:
        build_activity(a)
    build_ascensiones_macizos()
    for a, o, p in OPTION_PAGES:
        build_option(a, o, p)
    for c in COURSES:
        build_course(c)
    for s in SERVICES:
        build_service(s)
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        "  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n" % (url(p), TODAY, pr) for p, pr in PAGES) + "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
    # Catálogo para el calendario: si en la hoja falta precio, título o tipo, la web los toma de aquí (por slug)
    catalogo = {c["slug"]: {"titulo": c["title"], "tipo": "Curso", "precio": c["price"], "img": c["img"], "desc": c.get("seo_desc", c.get("short", ""))} for c in COURSES}
    catalogo.update({x["slug"]: {"titulo": x["title"], "tipo": "Actividad", "precio": min_price(x) or 0, "img": x["img"], "desc": x.get("seo_desc", x.get("short", ""))} for x in ACTIVITIES if x["slug"] not in catalogo})
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    json.dump(catalogo, open(os.path.join(OUT, "data", "catalogo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if BASE:
        os.remove(os.path.join(OUT, "sitemap.xml")) if os.path.exists(os.path.join(OUT, "sitemap.xml")) else None
        open(os.path.join(OUT, ".htaccess"), "w").write("ErrorDocument 404 %s/404.html\n" % BASE)
        print("Versión de prueba en", BASE, "(noindex, sin sitemap)"); return
    # redirecciones 301 desde las direcciones de la web antigua (para no perder posicionamiento al publicar en la raíz)
    old = {"%s.html" % x["slug"]: "/actividades/%s/" % x["slug"] for x in ACTIVITIES + COURSES}
    old.update({"cursos-barranquismo.html": "/actividades/curso-barranquismo/", "contacto-reservas.html": "/contacto/", "contacto.html": "/contacto/",
                "calendario-actividades-gredos.html": "/calendario/", "calendario.html": "/calendario/", "sobre-nosotros.html": "/sobre-nosotros/",
                "actividades.html": "/actividades/", "formacion-cursos.html": "/formacion-cursos/", "cursos.html": "/formacion-cursos/",
                "proximamente.html": "/", "blog.html": "/", "route-setting.html": "/route-setting/", "iniciativas-turismo-rural.html": "/iniciativas-turismo-rural/",
                "creacion-mantenimiento-senderos.html": "/creacion-mantenimiento-senderos/", "calculadora-rutas.html": "/calculadora-rutas/"})
    # Resto de direcciones del sitemap de la web antigua (www.guiasadastra.com/sitemap.xml, 77 páginas)
    A, CU = "/actividades/", "/formacion-cursos/"
    old.update({
        "base.html": "/", "page22.html": "/", "page46.html": "/", "page54.html": "/", "gredos-infinito.html": "/", "guias-de-gredos.html": "/sobre-nosotros/",
        "multiaventura-gredos.html": A, "gredos-oeste.html": A + "comarca-natural-oeste-de-gredos/",
        "alquiler-material-montana.html": A + "alquiler-material-montana/",
        "barranquismo.html": A + "barranquismo-avila/", "barranquismo-avila-gredos.html": A + "barranquismo-avila/",
        "barranco-de-papuos.html": A + "barranquismo-avila/", "barranco-del-arbillas.html": A + "barranquismo-avila/",
        "barranquismo-en-salamanca.html": A + "barranquismo-salamanca/", "barranquismo-en-madrid.html": A + "barranquismo-madrid-segovia/",
        "senderismo.html": A + "senderismo-avila-gredos/", "senderismo-avila-gredo.html": A + "senderismo-avila-gredos/",
        "el-desafio-de-los-galayos.html": A + "senderismo-avila-gredos/",
        "grandes-travesias.html": A + "trekking-carros-de-foc/", "grandes-travesias-espana.html": A + "trekking-carros-de-foc/",
        "vias-ferratas-valladolid.html": A + "via-ferrata-burgos/", "espeleologia-valladolid.html": A + "espeleologia-segovia/",
        "escalada-palencia.html": A + "boulder-las-tuerces/", "escalada-salamanca.html": A + "boulder-zona-centro-salamanca-caceres/",
        "escalada-leon.html": A + "curso-iniciacion-escalada-en-roca/", "escalada-zamora.html": A + "curso-iniciacion-escalada-en-roca/",
        "escalada-segovia.html": A + "curso-iniciacion-escalada-en-roca/",
        "servicio-routte-setting-equipador.html": "/route-setting/", "creacion-mantenimiento-inventario-de-senderos.html": "/creacion-mantenimiento-senderos/",
        "cursos-formacion.html": CU, "cursos-orientacion.html": CU, "curso-vias-ferratas.html": CU,
        "curso-alpinismo-nivel1.html": A + "cursos-alpinismo/", "curso-alpinismo-nivel2.html": A + "cursos-alpinismo/", "curso-autodetenciones.html": A + "cursos-alpinismo/",
        "reservas-barranquismo.html": "/calendario/", "reservas-vias-ferratas.html": "/calendario/", "reservas-escalada.html": "/calendario/",
        "reservas-senderismo.html": "/calendario/", "reservas-espeleologia.html": "/calendario/", "reservas-travesias.html": "/calendario/",
        "reservas-rutas-invernales.html": "/calendario/",
        # páginas antiguas que existían en el servidor aunque no estaban en el sitemap
        "alquiler-material.html": A + "alquiler-material-montana/", "barrancos-avila.html": A + "barranquismo-avila/",
        "curso-alpinismo.html": A + "cursos-alpinismo/", "cursos-escalada.html": A + "curso-iniciacion-escalada-en-roca/",
        "cursos-escalada2.html": A + "curso-iniciacion-escalada-en-roca/", "senderismo-salamanca-bejar-alberca.html": A + "senderismo-avila-gredos/",
        "BOULDER-LAS-TUERCES-PALENCIA.pdf": "/media/b3fa4166-e520-42c1-b9f6-311b0b33ec26/otros-media-3.pdf",
    })
    open(os.path.join(OUT, ".htaccess"), "w").write("ErrorDocument 404 /404.html\n"
        "# Dirección única: guiasadastra.com (sin www) lleva siempre a https://www.guiasadastra.com\n"
        "<IfModule mod_rewrite.c>\nRewriteEngine On\nRewriteCond %{HTTP_HOST} ^guiasadastra\\.com$ [NC]\nRewriteRule ^(.*)$ https://www.guiasadastra.com/$1 [R=301,L]\n</IfModule>\n"
        "# Las páginas se revisan siempre (así los cambios se ven al momento); fotos, CSS y JS sí se guardan en caché\n"
        "<IfModule mod_headers.c>\n<FilesMatch \"\\.(html|xml|txt|json)$\">\nHeader set Cache-Control \"no-cache\"\n</FilesMatch>\n"
        "# Cabeceras de seguridad\nHeader set X-Content-Type-Options \"nosniff\"\nHeader set Referrer-Policy \"strict-origin-when-cross-origin\"\n"
        "Header set X-Frame-Options \"SAMEORIGIN\"\nHeader set Permissions-Policy \"camera=(), microphone=(), geolocation=()\"\n</IfModule>\n"
        "<Files \".ftp-deploy-sync-state.json\">\nRequire all denied\n</Files>\n"
        "# Direcciones de la web antigua -> nuevas (301)\n" + "".join(
        "RedirectMatch 301 ^/%s$ %s%s\n" % (k.replace(".", "\\."), D, v) for k, v in sorted(old.items())) +
        "# Zonas de meteo renombradas\nRedirectMatch 301 ^/meteo/valle-del-tietar/?$ %s/meteo/los-galayos/\nRedirectMatch 301 ^/meteo/la-vera/?$ %s/meteo/sierra-del-barco/\n" % (D, D) +
        "# Actividades retiradas\nRedirectMatch 301 ^/actividades/espeleologia-leon(/.*)?$ %s/actividades/barranquismo-cueva-valporquero-sima-de-perlas/\n" % D +
        "# La versión de prueba /NUEVA ya no existe: lleva a la misma página en la web principal\nRedirectMatch 301 ^/NUEVA(/.*)?$ %s$1\n" % D)
    # Resumen para buscadores con IA (ChatGPT, Perplexity, Gemini, Claude…): https://llmstxt.org
    L = ["# Guías Ad Astra · Montaña y Aventura", "",
         "> Empresa de turismo activo y guías de montaña titulados con bases en Fuentes de Béjar (Salamanca) y Valladolid. "
         "Barranquismo, vías ferratas, espeleología, escalada, ascensiones, senderismo, trekking, cursos de montaña y alquiler de material "
         "en Ávila, Salamanca, Cáceres, León, Palencia, Segovia, Burgos y Madrid. Reservas por WhatsApp en el %s." % SITE["phone"], "",
         "- Teléfono y WhatsApp: %s · Email: %s · Horario: %s" % (SITE["phone"], SITE["email"], SITE["hours"]),
         "- Instagram: %s · Facebook: %s" % (SITE["instagram"], SITE["facebook"]),
         "- Organizan la Ultra de Gredos, el Desafío Fuenterrico y las jornadas de voluntariado Gredos Limpio (desde 2013).", "",
         "## Actividades guiadas"]
    L += ["- [%s](%s/actividades/%s/): %s%s" % (x["title"], D, x["slug"], x["short"], (" Desde %s €." % min_price(x)) if min_price(x) else "") for x in ACTIVITIES if x["cat"] != "Otros"]
    L += ["", "## Barrancos, vías ferratas, cuevas y rutas concretas"]
    L += ["- [%s](%s%s): %s, %s, %d €." % (o["name"], D, p_, o["place"], o["dur"], o["price"]) for _, o, p_ in OPTION_PAGES]
    L += ["", "## Cursos de formación"]
    L += ["- [%s](%s/actividades/%s/): %s Desde %s €." % (c["title"], D, c["slug"], c["short"], c["price"]) for c in COURSES]
    L += ["", "## Alquiler de material", "- [Alquiler de material de montaña y barranquismo](%s/actividades/alquiler-material-montana/): neoprenos, arneses, cascos, sets de vía ferrata, piolets y crampones desde %d €/día. Recogida en Fuentes de Béjar (Salamanca) o Valladolid." % (D, precios.desde_alquiler()),
          "", "## Servicios para entidades"]
    L += ["- [%s](%s/%s/): %s" % (s["title"], D, s["slug"], s["short"]) for s in SERVICES]
    L += ["- [Organización de eventos deportivos](%s/actividades/organizacion-eventos-deportivos/)" % D,
          "", "## Información útil", "- [Calendario de cursos y salidas con plazas libres](%s/calendario/)" % D,
          "- [Calculadora de tiempo de rutas (método MIDE) y perfil de GPX](%s/calculadora-rutas/)" % D,
          "- [Meteorología de montaña](%s/meteo/): previsión a 15 días en cumbre y en el pueblo base para %d macizos (Gredos, Picos de Europa, Pirineos, Sierra Nevada…), calculada cada 6 horas con los modelos ECMWF, GFS, ICON-EU y AROME." % (D, len(MACIZOS)),
          "- [Boulder en Las Tuerces (Palencia)](%s/actividades/boulder-las-tuerces/) y [boulder en Salamanca, Ávila y Cáceres](%s/actividades/boulder-zona-centro-salamanca-caceres/): mapas de sectores y croquis." % (D, D),
          "- [Contacto](%s/contacto/) · [Sobre nosotros](%s/sobre-nosotros/)" % (D, D), ""]
    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write("\n".join(L))
    open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nDisallow: /calendario-google/\n\nSitemap: %s/sitemap.xml\n" % D)
    print("Páginas generadas:", len(PAGES) + 1)

if __name__ == "__main__":
    main()
