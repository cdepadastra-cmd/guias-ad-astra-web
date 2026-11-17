# -*- coding: utf-8 -*-
"""Dibujos (SVG) de las páginas «Cómo preparar la mochila» y «Teoría de las capas»."""

# ------------------------------------------------------------------ mochila: iconos de material
def _ico(tipo, x, y, s=1.0):
    """Pequeños dibujos del material (en un cuadro de ~44x44 centrado en x,y)."""
    k = '<g transform="translate(%.1f %.1f) scale(%.2f)" stroke="#1b120c" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round">' % (x, y, s)
    d = {
        "saco": '<rect x="-24" y="-13" width="48" height="26" rx="13" fill="#3d6fa3"/><path d="M-10 -13v26M2 -13v26M14 -13v26" stroke="#2a4f77"/><ellipse cx="-24" cy="0" rx="5" ry="13" fill="#5b8fc4"/>',
        "ropa": '<path d="M-20 -14 L-8 -18 Q0 -12 8 -18 L20 -14 L24 0 L16 2 L16 18 L-16 18 L-16 2 L-24 0Z" fill="#7c6bb0"/><path d="M-8 -18 Q0 -8 8 -18" fill="none"/>',
        "agua": '<rect x="-9" y="-14" width="18" height="32" rx="6" fill="#5fb3d9"/><rect x="-6" y="-22" width="12" height="8" rx="2" fill="#e8574a"/><path d="M-9 0h18" stroke="#3b8ab0"/>',
        "comida": '<rect x="-18" y="-10" width="36" height="22" rx="4" fill="#d9a441"/><path d="M-18 -2h36" /><circle cx="-6" cy="5" r="2" fill="#1b120c"/><circle cx="6" cy="5" r="2" fill="#1b120c"/>',
        "hornillo": '<path d="M-14 -4 h28 v14 a6 6 0 0 1 -6 6 h-16 a6 6 0 0 1 -6 -6z" fill="#9aa4ad"/><rect x="-18" y="-8" width="36" height="6" rx="2" fill="#c2c9cf"/><path d="M14 -2 h8" />',
        "cuerda": '<ellipse cx="0" cy="0" rx="20" ry="14" fill="none" stroke="#f3c74f" stroke-width="7"/><ellipse cx="0" cy="0" rx="20" ry="14" fill="none" stroke="#1b120c" stroke-width="1.5"/>',
        "chaqueta": '<path d="M-20 -14 L-8 -18 L0 -10 L8 -18 L20 -14 L24 2 L16 4 L16 18 L-16 18 L-16 4 L-24 2Z" fill="#e8574a"/><path d="M0 -10 V18" /><path d="M-8 -18 Q0 -26 8 -18" fill="#c9443a"/>',
        "botiquin": '<rect x="-17" y="-13" width="34" height="26" rx="5" fill="#f4ead8"/><path d="M0 -7v14M-7 0h14" stroke="#e8574a" stroke-width="5"/>',
        "frontal": '<path d="M-20 4 Q0 -14 20 4" fill="none" stroke="#5a6b7a" stroke-width="6"/><rect x="-8" y="-6" width="16" height="12" rx="4" fill="#f3c74f"/><circle cx="0" cy="0" r="3" fill="#fff"/>',
        "mapa": '<path d="M-20 -12 L-7 -16 L7 -12 L20 -16 V12 L7 16 L-7 12 L-20 16Z" fill="#d6e6c3"/><path d="M-7 -16V12M7 -12V16"/><path d="M-14 4 q8 -10 18 -2" fill="none" stroke="#e8574a" stroke-dasharray="3 3"/>',
        "crema": '<rect x="-8" y="-12" width="16" height="28" rx="5" fill="#f3c74f"/><rect x="-5" y="-18" width="10" height="7" rx="2" fill="#e8574a"/>',
    }[tipo]
    return k + d + "</g>"


def _mochila_svg():
    i = _ico
    zonas = (
        # (color, etiqueta, path de la zona)
        ('#5b8fc4', "M190 392 L 410 392 L 410 446 Q 410 476 380 476 L 220 476 Q 190 476 190 446Z"),
        ('#e86a5c', "M190 214 L 292 214 L 292 392 L 190 392Z"),
        ('#e9a53b', "M292 214 L 410 214 L 410 392 L 292 392Z"),
        ('#7cc47f', "M190 132 L 410 132 L 410 214 L 190 214Z"),
    )
    s = ['''<svg class="gd-svg" viewBox="0 0 900 600" role="img" aria-labelledby="mo-t mo-d">
<title id="mo-t">Cómo repartir el peso en la mochila</title>
<desc id="mo-d">Senderista de perfil con la mochila abierta en corte: abajo lo ligero y voluminoso, pegado a la espalda lo pesado, hacia fuera el peso medio, arriba lo que se usa a menudo, en la tapa lo pequeño y por fuera solo bastones y piolet.</desc>
<defs>
 <linearGradient id="mo-cielo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1d14"/><stop offset="1" stop-color="#1b120c"/></linearGradient>
 <linearGradient id="mo-tela" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3b2a1e"/><stop offset="1" stop-color="#2a1d14"/></linearGradient>
 <linearGradient id="mo-piel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f3cfa7"/><stop offset="1" stop-color="#d9a77d"/></linearGradient>
 <radialGradient id="mo-sombra"><stop offset="0" stop-color="#000" stop-opacity=".45"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
 <filter id="mo-ds" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000" flood-opacity=".45"/></filter>
</defs>
<rect width="900" height="600" rx="18" fill="url(#mo-cielo)"/>
<path d="M0 520 L 120 430 L 190 470 L 300 380 L 380 440 L 470 400 L 560 470 L 900 470 L 900 600 L 0 600Z" fill="#241a12"/>
<path d="M0 560 L 900 560 L 900 600 L 0 600Z" fill="#1b120c"/>
<ellipse cx="200" cy="560" rx="150" ry="14" fill="url(#mo-sombra)"/>''']
    # senderista de perfil (mira a la izquierda; la mochila queda a la derecha, en su espalda)
    s.append('''<g stroke="#1b120c" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">
 <path d="M150 380 L 128 470 L 112 552 L 140 554 L 156 474 L 170 410Z" fill="#46596b"/>
 <path d="M168 380 L 190 470 L 196 552 L 224 552 L 214 466 L 196 380Z" fill="#3a4b5c"/>
 <path d="M106 552 h40 v-4 q-6 -8 -18 -8 h-20 q-6 0 -6 6z" fill="#6b4a2f"/><path d="M194 552 h40 v-4 q-6 -8 -18 -8 h-20 q-6 0 -6 6z" fill="#6b4a2f"/>
 <path d="M136 210 Q 130 196 150 190 L 190 190 Q 206 196 202 214 L 206 384 L 140 388Z" fill="#2f7d6d"/>
 <path d="M150 226 Q 120 290 100 330 L 116 340 Q 140 300 170 250Z" fill="#2f7d6d"/>
 <circle cx="108" cy="338" r="10" fill="url(#mo-piel)"/>
 <line x1="104" y1="300" x2="80" y2="556" stroke="#bfb3a3" stroke-width="4"/>
 <path d="M150 192 Q 150 170 160 168 L 176 168 Q 184 172 182 192Z" fill="url(#mo-piel)"/>
 <circle cx="160" cy="140" r="32" fill="url(#mo-piel)"/>
 <path d="M126 130 Q 130 100 162 100 Q 196 102 194 132 Q 176 120 150 122 Q 136 124 126 130Z" fill="#c9443a"/>
 <circle cx="140" cy="138" r="3" fill="#1b120c" stroke="none"/>
 <path d="M132 156 q6 4 12 0" fill="none"/>
</g>''')
    # mochila en corte
    s.append('<g filter="url(#mo-ds)"><path d="M186 132 Q 186 100 216 98 L 384 98 Q 414 100 414 132 L 414 446 Q 414 480 380 480 L 220 480 Q 186 480 186 446Z" fill="url(#mo-tela)" stroke="#f4ead8" stroke-width="3"/></g>')
    for col, d in zonas:
        s.append('<path d="%s" fill="%s" opacity=".92"/>' % (d, col))
    s.append('<path d="M190 214 L 292 214 L 292 392 L 190 392Z" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="6 5" opacity=".7"/>')
    s.append('<path d="M190 132 Q 190 104 218 102 L 382 102 Q 410 104 410 132Z" fill="#b99ad9"/>')
    s.append('<path d="M186 132 H 414 M186 214 H 414 M186 392 H 414 M292 214 V 392" stroke="#1b120c" stroke-width="2" opacity=".55"/>')
    # material dentro de cada zona
    s += [i("frontal", 250, 118, .75), i("mapa", 300, 118, .75), i("crema", 348, 118, .75),
          i("chaqueta", 236, 172, .9), i("botiquin", 300, 172, .95), i("comida", 364, 172, .9),
          i("agua", 220, 262, 1), i("hornillo", 262, 262, .9), i("cuerda", 240, 336, 1.05),
          i("ropa", 330, 262, 1), i("chaqueta", 370, 336, .95),
          i("saco", 260, 436, 1.25), i("ropa", 360, 436, .9)]
    # correas, cinturón y bastones por fuera
    s.append('''<g stroke="#1b120c" stroke-width="3" stroke-linejoin="round">
 <path d="M186 150 Q 162 160 160 200 L 168 300 Q 176 330 186 340" fill="none" stroke="#3b2a1e" stroke-width="10"/>
 <rect x="150" y="370" width="52" height="30" rx="10" fill="#3b2a1e" stroke="#f4ead8" stroke-width="2"/>
 <line x1="430" y1="74" x2="430" y2="470" stroke="#bfb3a3" stroke-width="6" stroke-linecap="round"/>
 <path d="M418 104 h26 l-6 10 h-14z" fill="#bfb3a3"/>
 <path d="M440 120 q22 -6 30 10 l-8 4 q-8 -10 -22 -6z" fill="#9aa4ad"/>
</g>''')
    # centro de gravedad
    s.append('''<g transform="translate(241 300)"><circle r="15" fill="#fff" stroke="#1b120c" stroke-width="3"/><path d="M0 -15 A15 15 0 0 1 15 0 L0 0Z M0 15 A15 15 0 0 1 -15 0 L0 0Z" fill="#1b120c"/></g>
<line x1="241" y1="316" x2="241" y2="556" stroke="#fff" stroke-width="2" stroke-dasharray="5 6" opacity=".55"/>''')
    # números
    for n, (x, y) in enumerate([(300, 470), (204, 228), (396, 228), (300, 146), (300, 96), (446, 300)], 1):
        orden = [1, 2, 3, 4, 5, 6][n - 1]
        s.append('<g transform="translate(%d %d)"><circle r="14" fill="#1b120c" stroke="#f4ead8" stroke-width="2"/><text y="5.5" text-anchor="middle" class="gd-n">%d</text></g>' % (x, y, orden))
    # leyenda
    ley = [("#b99ad9", "5 · Tapa", "lo pequeño y a mano", "frontal, mapa, crema, navaja"),
           ("#7cc47f", "4 · Arriba", "lo que usas a menudo", "chubasquero, botiquín, comida del día"),
           ("#e86a5c", "2 · Pegado a la espalda", "lo más pesado", "agua, cuerda, hornillo, comida"),
           ("#e9a53b", "3 · Hacia fuera", "peso medio", "ropa de abrigo, tienda, neopreno"),
           ("#5b8fc4", "1 · Abajo", "ligero y voluminoso", "saco de dormir, ropa de recambio"),
           ("#bfb3a3", "6 · Por fuera", "solo lo imprescindible", "bastones, piolet, esterilla")]
    y = 92
    for col, t, sub, ej in ley:
        s.append('<rect x="504" y="%d" width="370" height="70" rx="12" fill="#2a1d14" stroke="%s" stroke-width="2"/><rect x="504" y="%d" width="10" height="70" rx="4" fill="%s"/>' % (y, col, y, col))
        s.append('<text x="528" y="%d" class="gd-lt"><tspan class="gd-b">%s:</tspan> %s</text><text x="528" y="%d" class="gd-s">%s</text>' % (y + 28, t, sub, y + 52, ej))
        y += 80
    s.append('<text x="241" y="590" class="gd-lb" text-anchor="middle">centro de gravedad</text>')
    s.append("</svg>")
    return "\n".join(s)


MOCHILA = _mochila_svg()


def _excursionista(x, color_mochila, alejada=False):
    """Senderista de perfil con mochila (bien pegada o alejada y alta)."""
    if alejada:
        mochila = '<g transform="rotate(-12 96 120)"><rect x="66" y="40" width="70" height="128" rx="22" fill="%s" stroke="#1b120c" stroke-width="3"/><rect x="74" y="50" width="54" height="26" rx="10" fill="#1b120c" opacity=".2"/></g>' % color_mochila
        cg = (104, 86)
    else:
        mochila = '<rect x="56" y="84" width="54" height="120" rx="18" fill="%s" stroke="#1b120c" stroke-width="3"/><rect x="62" y="94" width="42" height="24" rx="8" fill="#1b120c" opacity=".2"/>' % color_mochila
        cg = (80, 150)
    return ('<g transform="translate(%d 0)" stroke="#1b120c" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">'
            '<path d="M18 200 L 6 270 L -4 330 L 18 330 L 28 272 L 36 214Z" fill="#46596b"/><path d="M34 200 L 52 270 L 56 330 L 78 330 L 70 268 L 56 200Z" fill="#3a4b5c"/>'
            '<path d="M8 96 Q 8 84 22 82 L 46 82 Q 58 86 58 100 L 60 206 L 12 208Z" fill="#2f7d6d"/>'
            '<path d="M22 100 Q 0 140 -14 170 L -2 176 Q 14 146 34 118Z" fill="#2f7d6d"/><circle cx="-8" cy="174" r="8" fill="#e8b88f"/>'
            '<circle cx="30" cy="54" r="24" fill="#e8b88f"/><path d="M6 46 Q 10 26 32 26 Q 56 28 54 50 Q 40 40 22 42Z" fill="#c9443a"/><circle cx="16" cy="54" r="2.5" fill="#1b120c" stroke="none"/>'
            '%s<g transform="translate(%d %d)"><circle r="10" fill="#fff"/><path d="M0 -10 A10 10 0 0 1 10 0 L0 0Z M0 10 A10 10 0 0 1 -10 0 L0 0Z" fill="#1b120c" stroke="none"/></g>'
            '<line x1="%d" y1="%d" x2="%d" y2="336" stroke="#fff" stroke-width="2" stroke-dasharray="5 6" opacity=".7"/></g>') % (x, mochila, cg[0], cg[1], cg[0], cg[1] + 10, cg[0])


def _postura_svg():
    return ('''<svg class="gd-svg" viewBox="0 0 860 400" role="img" aria-labelledby="po-t"><title id="po-t">Peso pegado a la espalda frente a peso alejado</title>
<defs><radialGradient id="po-sm"><stop offset="0" stop-color="#000" stop-opacity=".45"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<marker id="po-fl" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#e8574a"/></marker></defs>
<rect x="0" y="0" width="420" height="400" rx="18" fill="#22301f"/><rect x="440" y="0" width="420" height="400" rx="18" fill="#3a1f1a"/>
<rect x="0" y="336" width="420" height="64" rx="0" fill="#1b120c" opacity=".55"/><rect x="440" y="336" width="420" height="64" fill="#1b120c" opacity=".55"/>
<ellipse cx="200" cy="336" rx="90" ry="8" fill="url(#po-sm)"/><ellipse cx="640" cy="336" rx="90" ry="8" fill="url(#po-sm)"/>'''
            + _excursionista(150, "#7cc47f") + _excursionista(590, "#e86a5c", alejada=True) +
            '''<path d="M690 120 C 740 100 760 60 730 30" fill="none" stroke="#e8574a" stroke-width="4" marker-end="url(#po-fl)"/>
<g transform="translate(360 54)"><circle r="28" fill="#7cc47f"/><path d="M-13 1 L-3 11 L14 -10" fill="none" stroke="#1b120c" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g>
<g transform="translate(800 54)"><circle r="28" fill="#e8574a"/><path d="M-11 -11 L11 11 M11 -11 L-11 11" stroke="#1b120c" stroke-width="6" stroke-linecap="round"/></g>
<text x="24" y="366" class="gd-lb"><tspan class="gd-b">Bien:</tspan> peso pegado y centrado.</text><text x="24" y="388" class="gd-s">La vertical del peso cae sobre los pies.</text>
<text x="464" y="366" class="gd-lb"><tspan class="gd-b">Mal:</tspan> peso lejos y alto.</text><text x="464" y="388" class="gd-s">Tira hacia atrás y obliga a encorvarse.</text>
</svg>''')


POSTURA = _postura_svg()


# ------------------------------------------------------------------ capas: viñetas de cómic
def _monigote(x, y, base, medio=None, fuera=None, cara="feliz"):
    """Muñeco de cómic con hasta tres capas (colores) superpuestas."""
    caras = {
        "feliz": '<path d="M-10 6 Q 0 14 10 6" fill="none" stroke="#1b120c" stroke-width="3"/>',
        "frio": '<path d="M-10 10 L-5 6 L0 10 L5 6 L10 10" fill="none" stroke="#1b120c" stroke-width="3"/>',
        "triste": '<path d="M-10 12 Q 0 4 10 12" fill="none" stroke="#1b120c" stroke-width="3"/>',
    }
    s = '<g transform="translate(%d %d)" stroke="#1b120c" stroke-width="3" stroke-linejoin="round">' % (x, y)
    capas = [c for c in (base, medio, fuera) if c]
    # la capa base entera; las de encima, como chaquetas abiertas que dejan ver las de dentro por el centro
    for k, col in enumerate(capas):
        e = k * 6
        cuerpo = (-32 - e, 32 + e, 58 + e, 40 + e, 30 + e, -30 - e, -40 - e, -58 - e)
        if k == 0:
            s += '<path d="M%d 40 L%d 40 L%d 72 L%d 64 L%d 130 L%d 130 L%d 64 L%d 72 Z" fill="%s"/>' % (cuerpo + (col,))
        else:
            g = 7 + (k - 1) * 10
            s += '<path d="M%d 40 L%d 40 L%d 130 L%d 130 L%d 64 L%d 72 Z" fill="%s"/>' % (-32 - e, -g, -g, -30 - e, -40 - e, -58 - e, col)
            s += '<path d="M%d 40 L%d 40 L%d 72 L%d 64 L%d 130 L%d 130 Z" fill="%s"/>' % (g, 32 + e, 58 + e, 40 + e, 30 + e, g, col)
    s += '<rect x="-24" y="128" width="20" height="64" rx="6" fill="#4a5a6a"/><rect x="4" y="128" width="20" height="64" rx="6" fill="#4a5a6a"/>'
    s += '<rect x="-28" y="188" width="26" height="12" rx="5" fill="#6b4a2f"/><rect x="2" y="188" width="26" height="12" rx="5" fill="#6b4a2f"/>'
    s += '<circle cx="0" cy="12" r="26" fill="#f0c9a0"/><circle cx="-9" cy="6" r="3" fill="#1b120c" stroke="none"/><circle cx="9" cy="6" r="3" fill="#1b120c" stroke="none"/>'
    s += caras[cara]
    if fuera:
        s += '<path d="M-28 4 C -30 -22 30 -22 28 4 L 22 -6 C 10 -14 -10 -14 -22 -6 Z" fill="%s"/>' % fuera
    return s + "</g>"


_DEFS = '<defs><marker id="cm-fl" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#6fb3e0"/></marker></defs>'


def _panel(w, h, n, titulo, cuerpo, color):
    """Una viñeta como SVG independiente (en el móvil se apilan una debajo de otra)."""
    return ('<svg class="gd-svg cm-v" viewBox="-2 -2 %d %d" role="img" aria-label="%s">%s%s</svg>'
            % (w + 4, h + 4, titulo, _DEFS, _vineta(0, 0, w, h, n, titulo, cuerpo, color)))


def _vineta(x, y, w, h, n, titulo, cuerpo, color):
    return ('<g transform="translate(%d %d)"><rect width="%d" height="%d" rx="14" fill="#241811" stroke="%s" stroke-width="4"/>'
            '<rect x="12" y="12" width="40" height="40" rx="10" fill="%s"/><text x="32" y="41" class="cm-n" text-anchor="middle">%s</text>'
            '<text x="64" y="40" class="cm-t">%s</text>%s</g>') % (x, y, w, h, color, color, n, titulo, cuerpo)


def _bocadillo(x, y, w, txt, punta="izq"):
    lineas = txt.split("|")
    h = 18 + 22 * len(lineas)
    px = 26 if punta == "izq" else w - 26
    s = '<g transform="translate(%d %d)"><path d="M10 0 H%d a10 10 0 0 1 10 10 V%d a10 10 0 0 1 -10 10 H%d l-10 18 l-4 -18 H10 a10 10 0 0 1 -10 -10 V10 a10 10 0 0 1 10 -10z" fill="#f4ead8" stroke="#1b120c" stroke-width="3"/>' % (
        x, y, w - 10, h - 10, px + 14)
    for k, l in enumerate(lineas):
        s += '<text x="%d" y="%d" class="cm-b" text-anchor="middle">%s</text>' % (w // 2, 30 + 22 * k, l)
    return s + "</g>"


def _sub(t):
    """Tipo de prenda, debajo del título de la viñeta."""
    return '<text x="24" y="80" class="cm-sub">%s</text>' % t


def _gotas(x, y, n=4):
    s = ""
    for k in range(n):
        s += '<path transform="translate(%d %d)" d="M0 0 C 6 10 8 14 0 18 C -8 14 -6 10 0 0z" fill="#6fb3e0" stroke="#1b120c" stroke-width="2"/>' % (x + (k % 2) * 14 + k * 10, y - k * 16)
    return s


def capas_comic():
    W, H = 380, 420
    v = []
    # 1 capa base
    c1 = _monigote(110, 150, "#7cc47f") + _sub("Camiseta y mallas térmicas") + _bocadillo(180, 96, 180, "¡Seco aunque|sude!") + \
        '<g stroke="#6fb3e0" stroke-width="4" fill="none" marker-end="url(#cm-fl)"><path d="M150 230 C 190 230 210 250 240 250"/><path d="M150 260 C 190 262 210 280 240 286"/></g>' + \
        '<text x="250" y="258" class="cm-s">sudor</text><text x="250" y="280" class="cm-s">hacia fuera</text>' + \
        '<text x="24" y="392" class="cm-p">Pegada a la piel. Saca el sudor:</text><text x="24" y="410" class="cm-p">sintética o lana merina. Nunca algodón.</text>'
    v.append(_panel(W, H, "1", "Capa base", c1, "#7cc47f"))
    # 2 capa intermedia
    c2 = _monigote(120, 150, "#7cc47f", "#e9a53b") + _sub("Forro polar o chaqueta de fibra") + _bocadillo(196, 96, 170, "¡Calentito!") + \
        ''.join('<path d="M%d 330 q 8 -14 0 -28 q -8 -14 0 -28" fill="none" stroke="#e8574a" stroke-width="4" stroke-linecap="round"/>' % xx for xx in (70, 100, 140, 170)) + \
        '<text x="24" y="392" class="cm-p">Guarda el calor del cuerpo:</text><text x="24" y="410" class="cm-p">forro polar o chaqueta de fibra.</text>'
    v.append(_panel(W, H, "2", "Capa intermedia", c2, "#e9a53b"))
    # 3 capa exterior
    c3 = _monigote(130, 160, "#7cc47f", "#e9a53b", "#6fb3e0") + _sub("Chaqueta impermeable o cortavientos") + _bocadillo(200, 92, 168, "¡Ni agua|ni viento!", "der") + \
        ''.join('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#bfe0f7" stroke-width="3" stroke-linecap="round"/>' % (xx, yy, xx - 8, yy + 18) for xx, yy in ((40, 112), (70, 136), (52, 170), (226, 214), (262, 194), (300, 232), (250, 262), (40, 226))) + \
        '<g stroke="#f4ead8" stroke-width="4" fill="none" stroke-linecap="round"><path d="M330 300 q -30 -10 -60 0"/><path d="M340 330 q -40 -10 -80 0"/></g>' + \
        '<text x="24" y="392" class="cm-p">Te protege de la lluvia y el viento:</text><text x="24" y="410" class="cm-p">chaqueta con membrana que transpire.</text>'
    v.append(_panel(W, H, "3", "Capa exterior", c3, "#6fb3e0"))
    # 4 capa de abrigo en paradas
    c4 = _monigote(120, 160, "#7cc47f", "#e9a53b", "#c9a7e8", "feliz") + _sub("Plumífero (plumas) o fibra gruesa") + _bocadillo(196, 96, 172, "En la cima|y al parar") + \
        '<g fill="#f4ead8" stroke="#1b120c" stroke-width="2"><circle cx="260" cy="250" r="6"/><circle cx="290" cy="280" r="4"/><circle cx="320" cy="240" r="5"/><circle cx="300" cy="320" r="6"/></g>' + \
        '<text x="24" y="392" class="cm-p">El «extra»: plumífero o chaqueta de</text><text x="24" y="410" class="cm-p">fibra para paradas, frío intenso o emergencias.</text>'
    v.append(_panel(W, H, "4", "Capa de reserva", c4, "#c9a7e8"))
    return '<div class="cm-grid">' + "".join(v) + "</div>"


def capas_errores():
    W, H = 380, 370
    e1 = _monigote(110, 96, "#d9d4cc", cara="frio") + _gotas(170, 206) + _bocadillo(196, 62, 170, "¡Algodón|empapado!", "der") + \
        '<text x="24" y="336" class="cm-p">El algodón retiene el sudor y</text><text x="24" y="354" class="cm-p">al parar te quedas helado.</text>'
    e2 = _monigote(120, 96, "#7cc47f", "#e9a53b", "#c9a7e8", cara="triste") + _gotas(200, 196, 3) + _bocadillo(200, 62, 166, "¡Me cuezo|subiendo!", "der") + \
        '<text x="24" y="336" class="cm-p">Subir con demasiada ropa: sudas,</text><text x="24" y="354" class="cm-p">te mojas por dentro y luego enfrías.</text>'
    return '<div class="cm-grid">' + _panel(W, H, "✗", "Algodón", e1, "#e8574a") + _panel(W, H, "✗", "Demasiado abrigo", e2, "#e8574a") + "</div>"
