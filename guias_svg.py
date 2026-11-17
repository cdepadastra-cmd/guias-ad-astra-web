# -*- coding: utf-8 -*-
"""Dibujos (SVG) de las páginas «Cómo preparar la mochila» y «Teoría de las capas»."""

# ------------------------------------------------------------------ mochila: zonas de carga
MOCHILA = '''<svg class="gd-svg" viewBox="0 0 860 560" role="img" aria-labelledby="mo-t mo-d">
<title id="mo-t">Cómo repartir el peso en la mochila</title>
<desc id="mo-d">Corte de una mochila de lado, con la espalda a la izquierda: abajo lo ligero y voluminoso, pegado a la espalda lo pesado, por fuera lo de peso medio, arriba lo que usas a menudo, en la tapa lo pequeño y por fuera solo lo imprescindible.</desc>
<defs>
 <pattern id="mo-tr" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="rgba(0,0,0,.18)" stroke-width="3"/></pattern>
 <marker id="mo-fl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#f4ead8"/></marker>
</defs>
<!-- persona (de lado) -->
<g fill="#3a2a1f" stroke="#f4ead8" stroke-width="3" stroke-linejoin="round">
 <circle cx="118" cy="92" r="34"/>
 <path d="M104 128 C 92 190 92 250 100 300 L 96 400 L 82 520 L 112 520 L 128 410 L 140 330 L 150 410 L 150 520 L 180 520 L 178 400 L 172 300 C 176 240 170 180 150 128 Z"/>
 <path d="M150 170 C 190 200 196 240 186 280" fill="none"/>
</g>
<text x="118" y="548" class="gd-lb" text-anchor="middle">espalda</text>
<!-- mochila -->
<g stroke="#f4ead8" stroke-width="3" stroke-linejoin="round">
 <path d="M178 120 C 178 98 196 86 222 86 L 380 86 C 404 86 420 102 420 124 L 424 470 C 424 492 408 506 386 506 L 214 506 C 192 506 178 492 178 470 Z" fill="#2a1d14"/>
 <!-- zonas -->
 <path d="M180 400 L 422 400 L 424 470 C 424 492 408 506 386 506 L 214 506 C 192 506 180 492 180 470 Z" fill="#6fb3e0"/>
 <rect x="180" y="210" width="118" height="190" fill="#e8574a"/>
 <rect x="298" y="210" width="124" height="190" fill="#e9a53b"/>
 <rect x="180" y="128" width="242" height="82" fill="#7cc47f"/>
 <path d="M182 128 C 182 104 198 90 222 88 L 380 88 C 402 90 416 104 418 128 Z" fill="#c9a7e8"/>
 <rect x="180" y="210" width="118" height="190" fill="url(#mo-tr)" stroke="none"/>
 <!-- correas -->
 <path d="M178 150 C 150 160 146 200 160 230" fill="none"/>
 <rect x="150" y="380" width="40" height="34" rx="8" fill="#3a2a1f"/>
 <!-- bastones / piolet por fuera -->
 <line x1="436" y1="70" x2="436" y2="500" stroke="#bfb3a3" stroke-width="5"/>
 <path d="M424 120 L 448 120" />
</g>
<!-- números -->
<g class="gd-num" text-anchor="middle">
 <circle cx="300" cy="455" r="17" fill="#1b120c"/><text x="300" y="461">1</text>
 <circle cx="239" cy="305" r="17" fill="#1b120c"/><text x="239" y="311">2</text>
 <circle cx="360" cy="305" r="17" fill="#1b120c"/><text x="360" y="311">3</text>
 <circle cx="300" cy="170" r="17" fill="#1b120c"/><text x="300" y="176">4</text>
 <circle cx="300" cy="108" r="15" fill="#1b120c"/><text x="300" y="114">5</text>
 <circle cx="456" cy="250" r="15" fill="#1b120c"/><text x="456" y="256">6</text>
</g>
<!-- centro de gravedad -->
<g>
 <circle cx="214" cy="288" r="14" fill="#fff" stroke="#1b120c" stroke-width="3"/>
 <path d="M214 274 A14 14 0 0 1 228 288 L214 288Z M214 302 A14 14 0 0 1 200 288 L214 288Z" fill="#1b120c"/>
 <text x="214" y="330" class="gd-lb gd-dk" text-anchor="middle">centro de</text><text x="214" y="346" class="gd-lb gd-dk" text-anchor="middle">gravedad</text>
</g>
<!-- leyenda -->
<g class="gd-ley">
 <rect x="488" y="92" width="20" height="20" rx="4" fill="#c9a7e8"/><text x="518" y="108"><tspan class="gd-b">5 · Tapa:</tspan> lo pequeño y a mano</text>
 <text x="518" y="128" class="gd-s">frontal, mapa, crema, navaja</text>
 <rect x="488" y="150" width="20" height="20" rx="4" fill="#7cc47f"/><text x="518" y="166"><tspan class="gd-b">4 · Arriba:</tspan> lo que usas a menudo</text>
 <text x="518" y="186" class="gd-s">chubasquero, botiquín, comida del día</text>
 <rect x="488" y="208" width="20" height="20" rx="4" fill="#e8574a"/><text x="518" y="224"><tspan class="gd-b">2 · Pegado a la espalda:</tspan></text>
 <text x="518" y="244"><tspan class="gd-b">lo más pesado</tspan></text>
 <text x="518" y="264" class="gd-s">agua, cuerda, hornillo, comida</text>
 <rect x="488" y="286" width="20" height="20" rx="4" fill="#e9a53b"/><text x="518" y="302"><tspan class="gd-b">3 · Hacia fuera:</tspan> peso medio</text>
 <text x="518" y="322" class="gd-s">ropa de abrigo, tienda, neopreno</text>
 <rect x="488" y="344" width="20" height="20" rx="4" fill="#6fb3e0"/><text x="518" y="360"><tspan class="gd-b">1 · Abajo:</tspan> ligero y voluminoso</text>
 <text x="518" y="380" class="gd-s">saco de dormir, ropa de recambio</text>
 <rect x="488" y="402" width="20" height="20" rx="4" fill="#bfb3a3"/><text x="518" y="418"><tspan class="gd-b">6 · Por fuera:</tspan> solo lo imprescindible</text>
 <text x="518" y="438" class="gd-s">bastones, piolet, esterilla</text>
</g>
</svg>'''

# ------------------------------------------------------------------ mochila: bien / mal
POSTURA = '''<svg class="gd-svg" viewBox="0 0 760 344" role="img" aria-labelledby="po-t">
<title id="po-t">Peso pegado a la espalda frente a peso alejado</title>
<g stroke="#f4ead8" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">
 <!-- bien -->
 <g transform="translate(70 20)">
  <circle cx="80" cy="40" r="24" fill="#3a2a1f"/>
  <path d="M70 66 L 64 170 L 52 270 M 64 170 L 96 270 M 70 90 L 110 150" fill="none"/>
  <rect x="20" y="70" width="44" height="100" rx="14" fill="#7cc47f"/>
  <circle cx="44" cy="120" r="8" fill="#fff" stroke="#1b120c"/>
  <line x1="44" y1="128" x2="44" y2="292" stroke-dasharray="6 6" stroke="#7cc47f"/>
  <line x1="20" y1="292" x2="120" y2="292"/>
 </g>
 <!-- mal -->
 <g transform="translate(420 20)">
  <circle cx="98" cy="44" r="24" fill="#3a2a1f"/>
  <path d="M92 70 L 80 170 L 64 270 M 80 170 L 112 270 M 90 92 L 130 140" fill="none"/>
  <rect x="-4" y="40" width="64" height="120" rx="16" fill="#e8574a" transform="rotate(-8 28 100)"/>
  <circle cx="22" cy="84" r="8" fill="#fff" stroke="#1b120c"/>
  <line x1="22" y1="92" x2="22" y2="292" stroke-dasharray="6 6" stroke="#e8574a"/>
  <line x1="0" y1="292" x2="140" y2="292"/>
  <path d="M10 70 C -20 60 -30 30 -10 10" fill="none" stroke="#e8574a" marker-end="url(#mo-fl)"/>
 </g>
</g>
<text x="40" y="330" class="gd-lb"><tspan class="gd-b">Bien:</tspan> peso pegado; la vertical cae sobre los pies</text>
<text x="420" y="330" class="gd-lb"><tspan class="gd-b">Mal:</tspan> peso lejos y alto; tira hacia atrás</text>
<g class="gd-ok"><circle cx="270" cy="60" r="26" fill="#7cc47f"/><path d="M257 61 L 267 71 L 285 50" fill="none" stroke="#1b120c" stroke-width="5"/></g>
<g class="gd-ok"><circle cx="630" cy="60" r="26" fill="#e8574a"/><path d="M618 48 L 642 72 M 642 48 L 618 72" stroke="#1b120c" stroke-width="5"/></g>
</svg>'''

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


def _gotas(x, y, n=4):
    s = ""
    for k in range(n):
        s += '<path transform="translate(%d %d)" d="M0 0 C 6 10 8 14 0 18 C -8 14 -6 10 0 0z" fill="#6fb3e0" stroke="#1b120c" stroke-width="2"/>' % (x + (k % 2) * 14 + k * 10, y - k * 16)
    return s


def capas_comic():
    W, H = 380, 420
    v = []
    # 1 capa base
    c1 = _monigote(110, 150, "#7cc47f") + _bocadillo(180, 70, 180, "¡Seco aunque|sude!") + \
        '<g stroke="#6fb3e0" stroke-width="4" fill="none" marker-end="url(#cm-fl)"><path d="M150 230 C 190 230 210 250 240 250"/><path d="M150 260 C 190 262 210 280 240 286"/></g>' + \
        '<text x="250" y="258" class="cm-s">sudor</text><text x="250" y="280" class="cm-s">hacia fuera</text>' + \
        '<text x="24" y="392" class="cm-p">Pegada a la piel. Saca el sudor:</text><text x="24" y="410" class="cm-p">sintética o lana merina. Nunca algodón.</text>'
    v.append(_panel(W, H, "1", "Capa base", c1, "#7cc47f"))
    # 2 capa intermedia
    c2 = _monigote(120, 150, "#7cc47f", "#e9a53b") + _bocadillo(196, 70, 170, "¡Calentito!") + \
        ''.join('<path d="M%d 330 q 8 -14 0 -28 q -8 -14 0 -28" fill="none" stroke="#e8574a" stroke-width="4" stroke-linecap="round"/>' % xx for xx in (70, 100, 140, 170)) + \
        '<text x="24" y="392" class="cm-p">Guarda el calor del cuerpo:</text><text x="24" y="410" class="cm-p">forro polar o chaqueta de fibra.</text>'
    v.append(_panel(W, H, "2", "Capa intermedia", c2, "#e9a53b"))
    # 3 capa exterior
    c3 = _monigote(130, 160, "#7cc47f", "#e9a53b", "#6fb3e0") + _bocadillo(200, 64, 168, "¡Ni agua|ni viento!", "der") + \
        ''.join('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#bfe0f7" stroke-width="3" stroke-linecap="round"/>' % (xx, yy, xx - 8, yy + 18) for xx, yy in ((40, 80), (70, 110), (52, 160), (226, 210), (262, 190), (300, 230), (250, 260), (40, 220))) + \
        '<g stroke="#f4ead8" stroke-width="4" fill="none" stroke-linecap="round"><path d="M330 300 q -30 -10 -60 0"/><path d="M340 330 q -40 -10 -80 0"/></g>' + \
        '<text x="24" y="392" class="cm-p">Te protege de la lluvia y el viento:</text><text x="24" y="410" class="cm-p">chaqueta con membrana que transpire.</text>'
    v.append(_panel(W, H, "3", "Capa exterior", c3, "#6fb3e0"))
    # 4 capa de abrigo en paradas
    c4 = _monigote(120, 160, "#7cc47f", "#e9a53b", "#c9a7e8", "feliz") + _bocadillo(196, 70, 172, "En la cima|y al parar") + \
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
