"""Genera las imágenes para redes sociales (1200x630) de herramientas y artículos: static/img/og/<slug>.png"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = "/usr/share/fonts/opentype/inter/"
BASE = os.path.join(os.path.dirname(__file__), "..", "static")
PAGS = [
    ("meteo", "Herramienta gratuita", "Tiempo en montaña", "Previsión a 15 días en cumbre y base · 27 macizos", "#4fb3e8", None),
    ("nieve", "Herramienta gratuita", "Estado de la nieve", "Nieve reciente, placas de viento y costras por macizo", "#bfe0f7", None),
    ("barrancos-caudal", "Herramienta gratuita", "Caudal de barrancos", "En tiempo real: Jerte, Mazobre y Valporquero", "#6fb3e8", None),
    ("calculadora-rutas", "Herramienta gratuita", "Calculadora de rutas MIDE", "Tiempo, perfil y ficha de tu ruta a partir del GPX", "#e9a53b", None),
    ("topografia-barrancos", "Herramienta gratuita", "Topografía de barrancos", "Croquis de rápeles y cuerda necesaria", "#e9a53b", None),
    ("editor-gpx", "Herramienta gratuita", "Editor GPX online", "Une, corta y corrige tracks · waypoints · mapa y perfil", "#4fb3e8", None),
    ("video-ruta-3d", "Herramienta gratuita", "Vídeo 3D de tu ruta", "Tu GPX sobrevolando el relieve, con perfil y waypoints", "#e8574a", None),
    ("lista-material-montana", "Herramienta gratuita", "Lista de material", "Qué llevar en la mochila según la actividad", "#7cc47f", "img/guias/mochila-bien.webp"),
    ("herramientas", "Guías Ad Astra", "Herramientas de montaña", "Tiempo, nieve, caudales, editor GPX, vídeo 3D y más", "#e9a53b", None),
    ("articulos", "Guías Ad Astra", "Artículos de montaña", "Nieve y aludes, mochila y ropa de montaña", "#e9a53b", None),
    ("como-preparar-la-mochila", "Artículo", "Cómo preparar la mochila", "Lo pesado, pegado a la espalda: dónde va cada cosa", "#e9a53b", "img/guias/mochila-zonas.webp"),
    ("rayos-uv-proteccion-solar-montana", "Artículo", "Rayos UV y protección solar", "Qué FPS usar y qué gafas necesitas en la montaña", "#f5c84b", None),
    ("teoria-de-las-capas", "Artículo", "La teoría de las capas", "Cómo vestirse para la montaña, capa a capa", "#c78bf0", None),
    ("como-leer-la-nieve-y-los-aludes", "Artículo", "Cómo leer la nieve y los aludes", "Manto, placas de viento y el boletín de AEMET explicado", "#bfe0f7", "img/guias/boletin-aludes-aemet-guadarrama.webp"),
]


def fuente(n, t):
    return ImageFont.truetype(F + n, t)


def partir(d, txt, f, ancho):
    lineas, l = [], ""
    for w in txt.split():
        prueba = (l + " " + w).strip()
        if d.textlength(prueba, font=f) <= ancho: l = prueba
        else: lineas.append(l); l = w
    return lineas + [l]


def tarjeta(slug, eyebrow, titulo, sub, color, imagen):
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#160d09"); d = ImageDraw.Draw(im)
    # montañas de fondo
    d.polygon([(0, 630), (0, 470), (180, 380), (300, 430), (470, 300), (620, 400), (760, 330), (900, 420), (1060, 350), (1200, 410), (1200, 630)], fill="#24160e")
    d.polygon([(0, 630), (0, 540), (220, 470), (420, 520), (640, 450), (860, 520), (1040, 470), (1200, 520), (1200, 630)], fill="#2d1c12")
    texto_w = 700 if imagen else 1000
    if imagen:
        ph = Image.open(os.path.join(BASE, imagen)).convert("RGB")
        r = min(520 / ph.height, 400 / ph.width); ph = ph.resize((int(ph.width * r), int(ph.height * r)))
        x, y = W - ph.width - 60, (H - ph.height) // 2
        sombra = Image.new("RGBA", (ph.width + 40, ph.height + 40), (0, 0, 0, 0)); ImageDraw.Draw(sombra).rounded_rectangle([20, 20, ph.width + 20, ph.height + 20], 18, fill=(0, 0, 0, 160))
        im.paste(sombra.filter(ImageFilter.GaussianBlur(14)), (x - 20, y - 10), sombra.filter(ImageFilter.GaussianBlur(14)))
        m = Image.new("L", ph.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, ph.width, ph.height], 16, fill=255)
        im.paste(ph, (x, y), m)
    d.rectangle([0, 0, 14, H], fill=color)
    logo = Image.open(os.path.join(BASE, "img/logo-adastra-pin.png")).convert("RGBA"); logo = logo.resize((54, 72))
    im.paste(logo, (70, 56), logo)
    d.text((140, 66), "GUÍAS AD ASTRA", font=fuente("Inter-ExtraBold.otf", 30), fill="#f3e9df")
    d.text((140, 102), "guiasadastra.com", font=fuente("Inter-Medium.otf", 20), fill="#b9a593")
    d.text((70, 196), eyebrow.upper(), font=fuente("Inter-Bold.otf", 24), fill=color)
    ft = fuente("Inter-ExtraBold.otf", 76 if len(titulo) < 24 else 64); y = 236
    for l in partir(d, titulo, ft, texto_w):
        d.text((70, y), l, font=ft, fill="#ffffff"); y += ft.size + 8
    fs = fuente("Inter-Medium.otf", 30); y += 14
    for l in partir(d, sub, fs, texto_w):
        d.text((70, y), l, font=fs, fill="#e2d4c6"); y += 40
    im.save(os.path.join(BASE, "img/og", slug + ".png"), optimize=True)


if __name__ == "__main__":
    for p in PAGS:
        tarjeta(*p)
    print(len(PAGS), "imágenes")
