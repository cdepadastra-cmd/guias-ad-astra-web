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


def _senderista():
    """Senderista de cómic de perfil, mirando a la izquierda (pies en y=556, espalda hacia x=200)."""
    T = "#120b07"
    return ('''<g stroke="%s" stroke-width="3.6" stroke-linejoin="round" stroke-linecap="round">
 <path d="M172 376 Q 196 430 214 470 L 222 540 L 196 542 L 188 478 L 158 420Z" fill="#33475a"/>
 <path d="M200 470 Q 204 500 206 536" fill="none" stroke="#24333f" stroke-width="2"/>
 <path d="M186 534 h44 q8 0 8 10 v6 h-58 v-8 q0 -8 6 -8z" fill="#6b4529"/><path d="M180 550 h60" stroke-width="5"/>
 <path d="M150 380 Q 138 430 120 462 L 98 536 L 126 540 L 146 470 L 178 400Z" fill="#46617a"/>
 <path d="M126 466 Q 116 500 110 530" fill="none" stroke="#33475a" stroke-width="2"/>
 <path d="M86 534 h44 q8 0 8 10 v6 h-60 v-8 q0 -8 8 -8z" fill="#7a5132"/><path d="M80 550 h60" stroke-width="5"/>
 <path d="M96 538 l6 -6 M104 538 l6 -6 M112 538 l6 -6" stroke-width="2"/>
 <path d="M136 212 Q 128 192 150 186 L 196 186 Q 214 192 210 216 L 214 384 Q 176 398 138 388Z" fill="#2f8a78"/>
 <path d="M186 196 Q 204 260 200 388 L 214 384 L 210 214Z" fill="#226a5c" stroke="none"/>
 <path d="M160 190 L 156 384" fill="none" stroke="#1b5248" stroke-width="2" stroke-dasharray="4 4"/>
 <rect x="138" y="300" width="24" height="18" rx="4" fill="#226a5c"/>
 <path d="M150 188 L 140 172 L 168 182 L 182 170 L 186 190" fill="#2f8a78"/>
 <path d="M152 222 Q 120 280 96 322 L 116 336 Q 142 292 172 246Z" fill="#2f8a78"/>
 <path d="M116 300 Q 106 314 100 322" fill="none" stroke="#226a5c" stroke-width="6"/>
 <circle cx="104" cy="334" r="12" fill="#3b3b3b"/>
 <line x1="98" y1="296" x2="70" y2="556" stroke="#c9c1b5" stroke-width="5"/><line x1="98" y1="296" x2="70" y2="556" stroke="%s" stroke-width="1.2"/>
 <rect x="94" y="318" width="12" height="26" rx="4" fill="#e8574a"/>
 <path d="M150 186 Q 150 170 158 166 L 178 166 Q 186 172 184 188Z" fill="#d9a27a"/>
 <path d="M134 140 Q 130 100 168 98 Q 202 100 200 140 Q 200 178 166 180 Q 146 180 138 166 L 124 162 Q 120 156 128 150 L 126 146Z" fill="#f1c9a2"/>
 <path d="M176 104 Q 200 112 198 146 Q 192 172 172 178 Q 190 150 176 104Z" fill="#d9a27a" stroke="none"/>
 <ellipse cx="176" cy="140" rx="8" ry="11" fill="#f1c9a2"/><path d="M174 136 q4 4 0 8" fill="none" stroke-width="2"/>
 <path d="M138 166 Q 150 184 172 178 Q 166 168 150 166Z" fill="#7a5132"/>
 <path d="M130 122 Q 128 82 166 80 Q 204 82 204 124 Q 172 112 130 122Z" fill="#e8574a"/>
 <rect x="126" y="114" width="80" height="14" rx="6" fill="#c9443a" transform="rotate(-4 166 121)"/>
 <circle cx="170" cy="74" r="10" fill="#f4ead8"/>
 <ellipse cx="146" cy="138" rx="4.5" ry="5.5" fill="#fff"/><circle cx="144" cy="139" r="2.6" fill="%s" stroke="none"/>
 <path d="M138 128 q8 -5 16 0" fill="none"/>
 <path d="M134 158 q6 3 11 0" fill="none"/>
</g>''') % (T, T, T)


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
    s.append(_senderista())
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
    """El senderista de cómic, más pequeño, con la mochila pegada o alejada y alta."""
    T = "#120b07"
    if alejada:
        mochila = ('<g transform="rotate(-14 230 190)" stroke="%s" stroke-width="3.6" stroke-linejoin="round"><rect x="206" y="108" width="96" height="190" rx="30" fill="%s"/>'
                   '<rect x="218" y="122" width="72" height="40" rx="14" fill="#000" opacity=".18" stroke="none"/><path d="M226 180 h56" stroke-width="2"/></g>') % (T, color_mochila)
        cg = (256, 170)
    else:
        mochila = ('<g stroke="%s" stroke-width="3.6" stroke-linejoin="round"><rect x="200" y="186" width="70" height="196" rx="24" fill="%s"/>'
                   '<rect x="208" y="198" width="54" height="36" rx="12" fill="#000" opacity=".18" stroke="none"/><path d="M212 260 h46" stroke-width="2"/>'
                   '<rect x="136" y="368" width="78" height="24" rx="8" fill="#3b2a1e"/></g>') % (T, color_mochila)
        cg = (226, 290)
    return ('<g transform="translate(%d 6) scale(.62)">%s%s<g transform="translate(%d %d)"><circle r="15" fill="#fff" stroke="%s" stroke-width="3"/>'
            '<path d="M0 -15 A15 15 0 0 1 15 0 L0 0Z M0 15 A15 15 0 0 1 -15 0 L0 0Z" fill="%s"/></g>'
            '<line x1="%d" y1="%d" x2="%d" y2="556" stroke="#fff" stroke-width="3" stroke-dasharray="7 8" opacity=".8"/></g>') % (
        x, _senderista(), mochila, cg[0], cg[1], T, T, cg[0], cg[1] + 16, cg[0])


def _postura_svg():
    return ('''<svg class="gd-svg" viewBox="0 0 860 400" role="img" aria-labelledby="po-t"><title id="po-t">Peso pegado a la espalda frente a peso alejado</title>
<defs><radialGradient id="po-sm"><stop offset="0" stop-color="#000" stop-opacity=".45"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<marker id="po-fl" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#e8574a"/></marker></defs>
<rect x="0" y="0" width="420" height="400" rx="18" fill="#22301f"/><rect x="440" y="0" width="420" height="400" rx="18" fill="#3a1f1a"/>
<rect x="0" y="336" width="420" height="64" rx="0" fill="#1b120c" opacity=".55"/><rect x="440" y="336" width="420" height="64" fill="#1b120c" opacity=".55"/>
<ellipse cx="200" cy="336" rx="90" ry="8" fill="url(#po-sm)"/><ellipse cx="640" cy="336" rx="90" ry="8" fill="url(#po-sm)"/>'''
            + _excursionista(90, "#7cc47f") + _excursionista(530, "#e86a5c", alejada=True) +
            '''<path d="M690 120 C 740 100 760 60 730 30" fill="none" stroke="#e8574a" stroke-width="4" marker-end="url(#po-fl)"/>
<g transform="translate(360 54)"><circle r="28" fill="#7cc47f"/><path d="M-13 1 L-3 11 L14 -10" fill="none" stroke="#1b120c" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g>
<g transform="translate(800 54)"><circle r="28" fill="#e8574a"/><path d="M-11 -11 L11 11 M11 -11 L-11 11" stroke="#1b120c" stroke-width="6" stroke-linecap="round"/></g>
<text x="24" y="366" class="gd-lb"><tspan class="gd-b">Bien:</tspan> peso pegado y centrado.</text><text x="24" y="388" class="gd-s">La vertical del peso cae sobre los pies.</text>
<text x="464" y="366" class="gd-lb"><tspan class="gd-b">Mal:</tspan> peso lejos y alto.</text><text x="464" y="388" class="gd-s">Tira hacia atrás y obliga a encorvarse.</text>
</svg>''')


POSTURA = _postura_svg()


# ------------------------------------------------------------------ capas: viñetas de cómic
TINTA = "#120b07"
PIEL, PIEL_S = "#f1c9a2", "#d9a27a"


def _osc(col, f=0.78):
    """Color más oscuro (sombras de cómic)."""
    c = col.lstrip("#")
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))


def _cara(expr):
    ojos = ('<ellipse cx="-11" cy="-2" rx="7" ry="8" fill="#fff"/><ellipse cx="11" cy="-2" rx="7" ry="8" fill="#fff"/>'
            '<circle cx="-9" cy="0" r="3.6" fill="%s" stroke="none"/><circle cx="13" cy="0" r="3.6" fill="%s" stroke="none"/>'
            '<circle cx="-8" cy="-1.5" r="1.2" fill="#fff" stroke="none"/><circle cx="14" cy="-1.5" r="1.2" fill="#fff" stroke="none"/>') % (TINTA, TINTA)
    cejas = {"feliz": '<path d="M-19 -15 q8 -6 15 -1 M5 -16 q8 -5 15 1" fill="none"/>',
             "frio": '<path d="M-19 -12 q8 -8 15 -5 M5 -17 q8 3 15 5" fill="none"/>',
             "agobio": '<path d="M-19 -17 q8 4 15 4 M5 -13 q8 -4 15 -4" fill="none"/>'}[expr]
    boca = {"feliz": '<path d="M-10 16 Q 2 28 14 16 Q 2 22 -10 16Z" fill="#7a2e2a"/>',
            "frio": '<path d="M-10 18 l4 -4 l4 4 l4 -4 l4 4 l4 -4" fill="none"/>',
            "agobio": '<path d="M-8 22 Q 2 12 12 22 Q 2 18 -8 22Z" fill="#7a2e2a"/>'}[expr]
    nariz = '<path d="M2 2 q5 7 -1 9" fill="none" stroke-width="2.5"/>'
    mejillas = '<circle cx="-18" cy="10" r="5" fill="#ee8f86" opacity=".55" stroke="none"/><circle cx="20" cy="10" r="5" fill="#ee8f86" opacity=".55" stroke="none"/>'
    if expr == "agobio":
        mejillas = '<ellipse cx="-17" cy="10" rx="8" ry="5" fill="#e8574a" opacity=".6" stroke="none"/><ellipse cx="19" cy="10" rx="8" ry="5" fill="#e8574a" opacity=".6" stroke="none"/>'
    return ojos + cejas + nariz + boca + mejillas


def _persona(x, y, capas, expr="feliz", gorro=None, capucha=None, manchas=False):
    """Personaje de cómic de frente (pies en y+300). capas: colores de dentro a fuera.
    Las capas de encima van abiertas por delante para que se vean las de dentro."""
    s = ['<g transform="translate(%d %d)" stroke="%s" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round">' % (x, y, TINTA)]
    s.append('<ellipse cx="0" cy="300" rx="74" ry="10" fill="#000" opacity=".35" stroke="none"/>')
    # piernas y botas
    s.append('<path d="M-40 176 L-44 270 L-10 270 L-4 186Z" fill="#3f5468"/><path d="M40 176 L44 270 L10 270 L4 186Z" fill="#3f5468"/>')
    s.append('<path d="M-26 200 L-24 262" stroke="#2c3b49" stroke-width="2"/><path d="M26 200 L24 262" stroke="#2c3b49" stroke-width="2"/>')
    s.append('<path d="M-48 266 h40 v16 q0 8 -8 8 h-34 q-8 0 -8 -8z" fill="#7a5132"/><path d="M8 266 h40 v16 q0 8 -8 8 h-34 q-8 0 -8 -8z" fill="#7a5132"/>')
    s.append('<path d="M-56 284 h48 M8 284 h48" stroke-width="5"/><path d="M-36 270 l8 6 M-28 270 l8 6 M28 270 l-8 6 M36 270 l-8 6" stroke-width="2"/>')
    # cuello
    s.append('<path d="M-11 50 h22 v24 h-22z" fill="%s"/>' % PIEL_S)
    for k, col in enumerate(capas):
        e, sh = k * 5, _osc(col)
        manga = 186 - 8 * k  # las de dentro asoman por los puños
        # mangas
        s.append('<path d="M-46 82 Q-72 96 -78 %d L-58 %d Q-56 130 -44 118Z" fill="%s"/>' % (manga, manga + 2, col))
        s.append('<path d="M46 82 Q72 96 78 %d L58 %d Q56 130 44 118Z" fill="%s"/>' % (manga, manga + 2, col))
        s.append('<path d="M-60 120 Q-64 %d -70 %d" fill="none" stroke="%s" stroke-width="5" opacity=".7"/>' % (manga - 30, manga - 4, sh))
        s.append('<path d="M60 120 Q64 %d 70 %d" fill="none" stroke="%s" stroke-width="5" opacity=".7"/>' % (manga - 30, manga - 4, sh))
        if k == 0:
            s.append('<path d="M-46 82 Q-30 68 -12 70 Q0 80 12 70 Q30 68 46 82 L50 188 Q0 198 -50 188Z" fill="%s"/>' % col)
            s.append('<path d="M20 90 Q 34 140 26 188 Q 40 190 50 188 L46 82 Q 36 76 28 74Z" fill="%s" opacity=".55" stroke="none"/>' % sh)
            if manchas:
                s.append('<path d="M-30 110 q10 -8 18 2 q6 12 -6 16 q-14 2 -12 -18z M8 140 q12 -6 16 6 q2 12 -10 12 q-10 -4 -6 -18z" fill="%s" opacity=".55" stroke="none"/>' % _osc(col, .62))
        else:
            g = 6 + (k - 1) * 11
            s.append('<path d="M-%d 70 Q-30 66 -46 82 L-50 %d Q-30 %d -%d %dZ" fill="%s"/>' % (14 + e, 188 + e, 194 + e, g, 192, col))
            s.append('<path d="M%d 70 Q30 66 46 82 L50 %d Q30 %d %d %dZ" fill="%s"/>' % (14 + e, 188 + e, 194 + e, g, 192, col))
            s.append('<path d="M-%d 74 L-%d 192" stroke="%s" stroke-width="2" stroke-dasharray="3 3"/>' % (g + 3, g + 3, _osc(col, .55)))
            s.append('<path d="M%d 74 L%d 192" stroke="%s" stroke-width="2" stroke-dasharray="3 3"/>' % (g + 3, g + 3, _osc(col, .55)))
            s.append('<path d="M28 96 Q 38 140 34 190 L48 188 L46 84Z" fill="%s" opacity=".55" stroke="none"/>' % sh)
            # cuello de la prenda
            s.append('<path d="M-%d 70 L-%d 52 L-6 72Z" fill="%s"/><path d="M%d 70 L%d 52 L6 72Z" fill="%s"/>' % (14 + e, 20 + e, col, 14 + e, 20 + e, col))
            s.append('<rect x="%d" y="150" width="20" height="14" rx="3" fill="%s"/>' % (-40 - e // 2, sh))
    # manos
    s.append('<circle cx="-68" cy="196" r="11" fill="%s"/><circle cx="68" cy="196" r="11" fill="%s"/>' % (PIEL, PIEL))
    # cabeza
    s.append('<ellipse cx="-33" cy="36" rx="7" ry="10" fill="%s"/><ellipse cx="33" cy="36" rx="7" ry="10" fill="%s"/>' % (PIEL, PIEL))
    s.append('<path d="M-32 30 Q-34 -6 0 -8 Q34 -6 32 30 Q32 64 0 66 Q-32 64 -32 30Z" fill="%s"/>' % PIEL)
    s.append('<path d="M14 0 Q30 14 28 44 Q22 58 10 62 Q24 40 14 0Z" fill="%s" opacity=".6" stroke="none"/>' % PIEL_S)
    if capucha:
        s.append('<path d="M-40 40 Q-46 -24 0 -26 Q46 -24 40 40 L32 34 Q34 -6 0 -10 Q-34 -6 -32 34Z" fill="%s"/>' % capucha)
    elif gorro:
        s.append('<path d="M-34 14 Q-34 -26 0 -28 Q34 -26 34 14Z" fill="%s"/><rect x="-36" y="6" width="72" height="14" rx="6" fill="%s"/><circle cx="0" cy="-32" r="9" fill="#f4ead8"/>' % (gorro, _osc(gorro)))
    else:
        s.append('<path d="M-32 18 Q-36 -14 -4 -16 Q30 -18 34 14 Q24 2 14 8 L10 -2 Q4 8 -8 4 L-12 -4 Q-18 10 -32 18Z" fill="#5a3a24"/>')
    s.append('<g transform="translate(0 30)">%s</g>' % _cara(expr))
    s.append("</g>")
    return "".join(s)


_DEFS = ('<defs><marker id="cm-fl" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#bfe0f7" stroke="#120b07" stroke-width="1"/></marker>'
         '<pattern id="cm-ht" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="1.7" fill="#fff" opacity=".07"/></pattern></defs>')


def _panel(w, h, n, titulo, cuerpo, color, sub, pie):
    """Viñeta de cómic: fondo de trama, título en cartela, tipo de prenda y pie de texto en recuadro."""
    pie_l = pie.split("|")
    hp = 18 + 20 * len(pie_l)
    pie_svg = '<rect x="14" y="%d" width="%d" height="%d" rx="4" fill="#f3c74f" stroke="%s" stroke-width="3"/>' % (h - hp - 14, w - 28, hp, TINTA)
    pie_svg += "".join('<text x="26" y="%d" class="cm-pie">%s</text>' % (h - hp - 14 + 24 + 20 * k, t) for k, t in enumerate(pie_l))
    return ('<svg class="gd-svg cm-v" viewBox="-4 -4 %d %d" role="img" aria-label="%s: %s">%s'
            '<rect width="%d" height="%d" rx="6" fill="#2a1d14" stroke="%s" stroke-width="6"/>'
            '<rect x="6" y="6" width="%d" height="%d" rx="3" fill="url(#cm-ht)"/>'
            '<path d="M%d 6 L%d 160 M%d 6 L%d 120" stroke="%s" stroke-width="10" opacity=".12"/>'
            '<rect x="14" y="14" width="%d" height="44" rx="4" fill="%s" stroke="%s" stroke-width="3" transform="rotate(-1.5 14 14)"/>'
            '<text x="28" y="45" class="cm-t">%s · %s</text>'
            '<text x="18" y="86" class="cm-sub">%s</text><g transform="translate(0 22)">%s</g>%s</svg>') % (
        w + 8, h + 8, titulo, sub, _DEFS, w, h, TINTA, w - 12, h - 12, w - 40, w - 120, w - 10, w - 60, color,
        min(w - 28, 26 + 15 * (len(titulo) + 4)), color, TINTA, n, titulo, sub, cuerpo, pie_svg)


def _bocadillo(x, y, w, txt, punta="izq"):
    lineas = txt.split("|")
    h = 20 + 24 * len(lineas)
    px = 30 if punta == "izq" else w - 40
    s = ('<g transform="translate(%d %d)"><path d="M14 0 H%d q14 0 14 14 V%d q0 14 -14 14 H%d l-16 22 l2 -22 H14 q-14 0 -14 -14 V14 q0 -14 14 -14z" '
         'fill="#fffaf0" stroke="%s" stroke-width="3.4" stroke-linejoin="round"/>') % (x, y, w - 14, h - 14, px + 18, TINTA)
    for k, l in enumerate(lineas):
        s += '<text x="%d" y="%d" class="cm-b" text-anchor="middle">%s</text>' % (w // 2, 32 + 24 * k, l)
    return s + "</g>"


def _gotas(x, y, n=4, col="#6fb3e0"):
    s = ""
    for k in range(n):
        s += '<path transform="translate(%d %d) scale(1.15)" d="M0 0 C 6 10 8 14 0 18 C -8 14 -6 10 0 0z" fill="%s" stroke="%s" stroke-width="2"/>' % (x + (k % 2) * 16 + k * 8, y - k * 18, col, TINTA)
    return s


def capas_comic():
    W, H = 400, 500
    v = []
    c1 = _persona(130, 112, ["#6cc47a"]) + _bocadillo(222, 100, 164, "¡Seco aunque|sude!") + \
        '<g stroke="#bfe0f7" stroke-width="5" fill="none" stroke-linecap="round" marker-end="url(#cm-fl)"><path d="M196 230 C 236 226 256 244 296 246"/><path d="M196 262 C 236 262 256 282 296 290"/></g>' + \
        '<g stroke="#bfe0f7" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"><path d="M310 236 l16 -4 M312 252 l18 2 M312 280 l16 -2 M312 298 l16 6"/></g>'
    v.append(_panel(W, H, "1", "Capa base", c1, "#6cc47a", "Camiseta y mallas térmicas", "Pegada a la piel. Saca el sudor hacia fuera:|sintética o lana merina. Nunca algodón."))
    c2 = _persona(130, 112, ["#6cc47a", "#e9a53b"]) + _bocadillo(222, 100, 164, "¡Calentito!") + \
        ''.join('<path d="M%d 300 q 9 -14 0 -28 q -9 -14 0 -28" fill="none" stroke="#e8574a" stroke-width="5" stroke-linecap="round"/>' % xx for xx in (250, 286, 322))
    v.append(_panel(W, H, "2", "Capa intermedia", c2, "#e9a53b", "Forro polar o chaqueta de fibra", "Guarda el calor del cuerpo y deja|salir la humedad."))
    c3 = _persona(140, 112, ["#6cc47a", "#e9a53b", "#4fa3dc"], capucha="#4fa3dc") + _bocadillo(232, 100, 156, "¡Ni agua|ni viento!", "der") + \
        ''.join('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#bfe0f7" stroke-width="3.5" stroke-linecap="round"/>' % (xx, yy, xx - 9, yy + 20) for xx, yy in ((30, 112), (64, 140), (40, 190), (250, 236), (290, 214), (330, 252), (270, 290), (36, 252), (350, 196))) + \
        '<g stroke="#f4ead8" stroke-width="5" fill="none" stroke-linecap="round" opacity=".85"><path d="M378 320 q -34 -12 -70 0"/><path d="M386 350 q -46 -12 -92 0"/></g>'
    v.append(_panel(W, H, "3", "Capa exterior", c3, "#4fa3dc", "Chaqueta impermeable o cortavientos", "Para la lluvia, la nieve y el viento: chaqueta|con membrana que transpire."))
    c4 = _persona(130, 112, ["#6cc47a", "#e9a53b", "#b48be0"], gorro="#e8574a") + _bocadillo(222, 100, 164, "En la cima|y al parar") + \
        '<g fill="#fffaf0" stroke="%s" stroke-width="2"><circle cx="270" cy="252" r="7"/><circle cx="306" cy="284" r="5"/><circle cx="338" cy="240" r="6"/><circle cx="316" cy="324" r="7"/><circle cx="356" cy="296" r="4"/></g>' % TINTA
    v.append(_panel(W, H, "4", "Capa de reserva", c4, "#b48be0", "Plumífero (plumas) o fibra gruesa", "El «extra» para paradas, frío intenso|o emergencias: encima de todo."))
    return '<div class="cm-grid">' + "".join(v) + "</div>"


def capas_errores():
    W, H = 400, 480
    e1 = _persona(130, 104, ["#d9d4cc"], expr="frio", manchas=True) + _gotas(220, 270) + _bocadillo(222, 96, 164, "¡Algodón|empapado!", "der") + \
        '<g stroke="#bfe0f7" stroke-width="3" fill="none" stroke-linecap="round"><path d="M40 170 q-8 10 0 20 q8 10 0 20"/><path d="M220 170 q8 10 0 20 q-8 10 0 20"/></g>'
    e2 = _persona(130, 104, ["#6cc47a", "#e9a53b", "#b48be0"], expr="agobio", gorro="#e8574a") + _gotas(222, 266, 3) + _bocadillo(222, 96, 164, "¡Me cuezo|subiendo!", "der") + \
        ''.join('<path d="M%d 96 q 8 -12 0 -24 q -8 -12 0 -24" fill="none" stroke="#f4ead8" stroke-width="4" stroke-linecap="round" opacity=".7"/>' % xx for xx in (96, 130, 164))
    return '<div class="cm-grid">' + _panel(W, H, "✗", "Algodón", e1, "#e8574a", "Camiseta de algodón", "Retiene el sudor y, al parar,|te quedas helado.") + \
        _panel(W, H, "✗", "Demasiado abrigo", e2, "#e8574a", "Todas las capas subiendo", "Sudas, te mojas por dentro|y luego te enfrías.") + "</div>"
