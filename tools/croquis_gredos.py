"""Croquis esquemáticos (orientativos) de las vías clásicas de Gredos -> static/img/guias/croquis-*.svg
No son reproducciones de ningún croquis publicado: se dibujan a partir de los datos de largos, grados y reuniones."""
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "static", "img", "guias")
T = 'font-family="Inter,system-ui,sans-serif"'
COL = {"III": "#7cc47f", "IV": "#4caf50", "IV+": "#9ccc65", "V": "#e6c32e", "V+": "#f08a24", "6a": "#e8574a", "?": "#b9a593"}

VIAS = {
    "torreon-sur": dict(
        titulo="Torreón de los Galayos · Sur Clásica", sub="≈ 130–140 m · V / V+ · granito · cara sur",
        silueta="M120 620 L150 300 L190 170 L230 110 L262 96 L300 120 L330 190 L360 330 L392 620Z",
        cima=(262, 96, "Cima (≈ 2.120 m)"),
        largos=[("L1", "≈ 50 m", "V", "Entrada dura junto a un clavo; reunión en un nicho bajo un pequeño techo."),
                ("L2", "≈ 30 m", "V+", "Travesía corta a la izquierda y fisura vertical que lleva a un sistema de diedros."),
                ("L3", "≈ 50 m", "V", "Más vertical, buena roca; termina en placa tumbada hasta la cadena de la cima.")],
        puntos=[(232, 600), (246, 420), (222, 300), (262, 110)],
        extras=[("rapel", (300, 120), (420, 300), "Acceso y bajada: rápel de 60 m por la cara norte hasta la Plataforma de las Flores")],
    ),
    "hermanitos": dict(
        titulo="Tres Hermanitos (Circo de Gredos)", sub="≈ 2.280 m · tres agujas · vías de 1–2 largos",
        silueta="M40 620 L70 360 L100 250 L135 240 L160 330 L190 360 L215 230 L250 220 L280 330 L310 380 L340 300 L372 290 L400 400 L430 620Z",
        cima=None,
        largos=[("1.º", "≈ 50 m · 2 L", "V+", "Vía Pirineos (cara SO). Fisura hasta un rellano y travesía bajo el gran diedro."),
                ("2.º", "≈ 45 m · 2 L", "V+", "Vía Teógenes (cara SO). Primer largo de buscar la línea, segundo corto y desplomado."),
                ("3.º", "≈ 30 m · 1 L", "IV", "Vía Teógenes (cara N). Fisura con un estrechamiento protegido con clavos.")],
        puntos=None,
        agujas=[(118, 240, "1.º", "V+"), (232, 222, "2.º", "V+"), (356, 292, "3.º", "IV")],
        extras=[],
    ),
    "torozo-gran-diedro": dict(
        titulo="El Torozo · Gran Diedro", sub="≈ 200 m · 6 largos · V+ máx. · cara sur",
        silueta="M90 620 L120 420 L150 260 L200 140 L250 100 L310 120 L350 220 L380 400 L410 620Z",
        cima=(250, 100, "Cima del Torozo"),
        largos=[("L1", "", "IV", ""), ("L2", "", "IV", ""), ("L3", "", "V", ""), ("L4", "", "V", ""), ("L5", "", "V+", "El largo más difícil del diedro."), ("L6", "", "IV", "Salida hacia la cumbre.")],
        puntos=[(230, 610), (238, 530), (226, 450), (240, 370), (232, 290), (246, 200), (250, 112)],
        extras=[("bajada", (300, 120), (420, 250), "Bajada: al collado norte por hitos y canal hacia el oeste")],
    ),
    "pequeno-galayo-apretura": dict(
        titulo="Pequeño Galayo · Sur de la Apretura", sub="≈ 120–150 m · IV/IV+ con un paso de V+ (evitable)",
        silueta="M80 620 L110 450 L140 330 L190 230 L240 170 L280 160 L320 200 L360 330 L400 620Z",
        cima=(280, 160, "Cima del Pequeño Galayo"),
        largos=[("L1", "", "IV", "Diedrito vertical en la pared izquierda de la canal del Gran Galayo; reunión en una gran terraza."),
                ("L2", "", "IV", "Pared vertical de buenos cantos hacia la derecha; reunión en un nicho con clavo."),
                ("L3", "", "IV", "Travesía a la izquierda, chimenea corta, placa y canal-chimenea hasta una gran repisa."),
                ("L4", "", "V+", "Hombro amplio y fisura de V+ (se puede evitar), diedro tumbado hasta el collado.")],
        puntos=[(200, 610), (186, 500), (232, 400), (214, 290), (280, 172)],
        extras=[("rapel", (300, 200), (420, 330), "Bajada: rápel al hombro y destrepe por hitos hacia la canal")],
    ),
    "gran-galayo-gran-diedro": dict(
        titulo="Gran Galayo · Gran Diedro", sub="≈ 100–120 m · IV+ (pasos de V) · cara sureste",
        silueta="M70 620 L110 420 L150 300 L190 200 L250 130 L300 120 L340 170 L370 300 L410 620Z",
        cima=(300, 120, "Cima del Gran Galayo (≈ 2.220 m)"),
        largos=[("L1", "", "IV", "Resalte vertical y expuesto antes de la portilla; terraza inclinada al pie del diedro."),
                ("L2", "≈ 60 m", "IV+", "El gran diedro: un desplome en la primera mitad, final casi en chimenea; clavos."),
                ("L3", "", "III", "Hombrito, diedro tumbado y cueva entre bloques; salida a la derecha a la cima.")],
        puntos=[(170, 600), (190, 500), (262, 230), (292, 132)],
        extras=[("bajada", (320, 140), (430, 300), "Bajada sin rápel: destrepe (III) por hitos a la portilla y canal")],
    ),
}


def svg(k, v):
    W, H = 900, 680
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="Croquis esquemático de %s">' % (W, H, v["titulo"]),
         '<defs><linearGradient id="g%s" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8d8378"/><stop offset="1" stop-color="#5d554d"/></linearGradient></defs>' % k,
         '<rect width="%d" height="%d" rx="18" fill="#1b120c"/>' % (W, H),
         '<path d="%s" fill="url(#g%s)" stroke="#a89c8e" stroke-width="2"/>' % (v["silueta"], k),
         # fisuras decorativas
         '<g stroke="#4a433c" stroke-width="2" fill="none" opacity=".6"><path d="M180 600 l20 -120 l-10 -80"/><path d="M330 590 l-14 -150 l10 -60"/></g>']
    if v.get("puntos"):
        pts = v["puntos"]
        for i in range(len(pts) - 1):
            g = v["largos"][min(i, len(v["largos"]) - 1)][2]
            s.append('<path d="M%d %d L%d %d" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % (pts[i] + pts[i + 1] + (COL.get(g, "#fff"),)))
        s.append('<path d="M%d %d" />' % pts[0])
        s.append('<text x="%d" y="%d" %s font-size="13" font-weight="800" fill="#f3e9df" text-anchor="middle">Inicio</text>' % (pts[0][0], pts[0][1] + 4 + 16, T))
        for i, (x, y) in enumerate(pts[1:-1], 1):
            s.append('<circle cx="%d" cy="%d" r="9" fill="#1b120c" stroke="#f3e9df" stroke-width="3"/>' % (x, y))
            s.append('<text x="%d" y="%d" %s font-size="12" font-weight="800" fill="#f3e9df">R%d</text>' % (x + 14, y + 4, T, i))
        for i in range(len(pts) - 1):
            lab = v["largos"][i] if i < len(v["largos"]) else None
            if not lab:
                continue
            mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
            s.append('<text x="%d" y="%d" %s font-size="13" font-weight="900" fill="#fff" text-anchor="end" paint-order="stroke" stroke="#1b120c" stroke-width="4">%s %s</text>' % (mx - 14, my + 4, T, lab[0], lab[2]))
    if v.get("agujas"):
        for x, y, n, g in v["agujas"]:
            s.append('<path d="M%d 600 Q%d %d %d %d" stroke="%s" stroke-width="5" fill="none" stroke-linecap="round"/>' % (x - 10, x - 30, (y + 600) // 2, x, y + 10, COL[g]))
            s.append('<circle cx="%d" cy="%d" r="7" fill="#f3e9df"/>' % (x, y + 6))
            s.append('<text x="%d" y="%d" %s font-size="15" font-weight="900" fill="#fff" text-anchor="middle" paint-order="stroke" stroke="#1b120c" stroke-width="4">%s · %s</text>' % (x, y - 12, T, n, g))
    if v.get("cima"):
        x, y, t = v["cima"]
        s.append('<text x="%d" y="%d" %s font-size="13" font-weight="800" fill="#e9a53b" text-anchor="middle">%s</text>' % (x, y - 14, T, t))
    for tipo, (x1, y1), (x2, y2), t in v["extras"]:
        x2 = min(x2, 430)
        s.append('<path d="M%d %d Q%d %d %d %d" stroke="#4fb3e8" stroke-width="3" stroke-dasharray="8 6" fill="none"/>' % (x1, y1, x2 + 10, y1, x2, y2))
        s.append('<path d="M%d %d l-6 -10 h12z" fill="#4fb3e8"/>' % (x2, y2 + 6))
        s.append('<text x="24" y="%d" %s font-size="13" font-weight="700" fill="#4fb3e8">↘ %s</text>' % (H - 44, T, t))
    # leyenda / largos a la derecha
    x0 = 470
    s.append('<text x="%d" y="54" %s font-size="22" font-weight="900" fill="#f3e9df">%s</text>' % (x0 - 10, T, v["titulo"] if len(v["titulo"]) < 34 else v["titulo"].split(" · ")[0]))
    if " · " in v["titulo"] and len(v["titulo"]) >= 34:
        s.append('<text x="%d" y="80" %s font-size="17" font-weight="800" fill="#e9a53b">%s</text>' % (x0 - 10, T, v["titulo"].split(" · ")[1]))
    s.append('<text x="%d" y="106" %s font-size="13" fill="#b9a593">%s</text>' % (x0 - 10, T, v["sub"]))
    y = 146
    for n, l, g, d in v["largos"]:
        s.append('<rect x="%d" y="%d" width="54" height="24" rx="6" fill="%s"/>' % (x0 - 10, y - 17, COL.get(g, "#888")))
        s.append('<text x="%d" y="%d" %s font-size="13" font-weight="900" fill="#1b120c" text-anchor="middle">%s</text>' % (x0 + 17, y, T, g))
        s.append('<text x="%d" y="%d" %s font-size="14" font-weight="800" fill="#f3e9df">%s %s</text>' % (x0 + 54, y, T, n, l))
        # descripción en varias líneas
        palabras, linea, yy = d.split(), "", y + 20
        for w in palabras:
            if len(linea + " " + w) > 46:
                s.append('<text x="%d" y="%d" %s font-size="12" fill="#cbbcab">%s</text>' % (x0 + 54, yy, T, linea.strip())); yy += 16; linea = ""
            linea += " " + w
        if linea.strip():
            s.append('<text x="%d" y="%d" %s font-size="12" fill="#cbbcab">%s</text>' % (x0 + 54, yy, T, linea.strip())); yy += 16
        y = max(yy + 18, y + 38)
    s.append('<text x="%d" y="%d" %s font-size="11" fill="#8a7d6e">Croquis esquemático y orientativo de Guías Ad Astra. No sustituye a una reseña actualizada.</text>' % (24, H - 18, T))
    s.append("</svg>")
    return "".join(s)


if __name__ == "__main__":
    for k, v in VIAS.items():
        open(os.path.join(BASE, "croquis-%s.svg" % k), "w").write(svg(k, v))
    print("ok", len(VIAS))
