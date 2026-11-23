"""Genera las ilustraciones SVG del artículo de orientación: static/img/guias/senales-senderos.svg y curvas-de-nivel.svg"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.join(os.path.dirname(__file__), "..", "static", "img", "guias")
T = 'font-family="Inter,system-ui,sans-serif"'


# ───────────── Señales GR / PR / SL ─────────────
def marca(x, y, color, tipo):
    """Marca pintada de 2 franjas (blanca arriba, color abajo) centrada en x,y."""
    w, h, g = 74, 13, 7
    if tipo == "sigue":
        return ('<rect x="%d" y="%d" width="%d" height="%d" fill="#fff" rx="2"/>' % (x - w / 2, y - h - g / 2, w, h) +
                '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" rx="2"/>' % (x - w / 2, y + g / 2, w, h, color))
    if tipo == "gira":  # franjas que se doblan hacia la derecha
        p = lambda dy: "M%d %d H%d L%d %d" % (x - w / 2, y + dy, x + 10, x + 34, y + dy + 34)
        return ('<path d="%s" stroke="#fff" stroke-width="%d" fill="none" stroke-linejoin="round"/>' % (p(-h / 2 - g / 2 - 4), h) +
                '<path d="%s" stroke="%s" stroke-width="%d" fill="none" stroke-linejoin="round"/>' % (p(h / 2 + g / 2 + 4), color, h))
    # aspa: dirección equivocada
    return ('<path d="M%d %d L%d %d" stroke="#fff" stroke-width="%d" stroke-linecap="round"/>' % (x - 30, y - 30, x + 30, y + 30, h) +
            '<path d="M%d %d L%d %d" stroke="%s" stroke-width="%d" stroke-linecap="round"/>' % (x + 30, y - 30, x - 30, y + 30, color, h))


def senales():
    filas = [("GR", "Gran Recorrido", "más de 50 km", "#d8322a"), ("PR", "Pequeño Recorrido", "10 a 50 km", "#f2c230"), ("SL", "Sendero Local", "menos de 10 km", "#2f9e44")]
    cols = [("sigue", "Continuidad", "vas bien"), ("gira", "Cambio de dirección", "gira hacia donde apunta"), ("mal", "Dirección equivocada", "por aquí no")]
    W, H = 900, 560
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="Marcas de los senderos GR (blanco y rojo), PR (blanco y amarillo) y SL (blanco y verde): continuidad, cambio de dirección y dirección equivocada">' % (W, H),
         '<defs><filter id="rug"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 .45  0 0 0 0 .42  0 0 0 0 .38  0 0 0 .35 0"/><feComposite in2="SourceGraphic" operator="in"/></filter></defs>',
         '<rect width="%d" height="%d" fill="#1b120c" rx="18"/>' % (W, H)]
    for j, (_, t, sub) in enumerate(cols):
        cx = 330 + j * 200
        s.append('<text x="%d" y="44" text-anchor="middle" %s font-size="17" font-weight="800" fill="#f3e9df">%s</text>' % (cx, T, t))
        s.append('<text x="%d" y="66" text-anchor="middle" %s font-size="13" fill="#b9a593">%s</text>' % (cx, T, sub))
    for i, (sig, nom, dist, col) in enumerate(filas):
        y = 150 + i * 158
        s.append('<text x="30" y="%d" %s font-size="34" font-weight="900" fill="%s">%s</text>' % (y - 6, T, col, sig))
        s.append('<text x="30" y="%d" %s font-size="15" font-weight="700" fill="#f3e9df">%s</text>' % (y + 18, T, nom))
        s.append('<text x="30" y="%d" %s font-size="13" fill="#b9a593">%s</text>' % (y + 38, T, dist))
        for j, (tipo, _, _) in enumerate(cols):
            cx = 330 + j * 200
            s.append('<rect x="%d" y="%d" width="170" height="130" rx="14" fill="#8a8178"/><rect x="%d" y="%d" width="170" height="130" rx="14" fill="#8a8178" filter="url(#rug)"/>' % (cx - 85, y - 65, cx - 85, y - 65))
            s.append(marca(cx - (8 if tipo == "gira" else 0), y - (6 if tipo == "gira" else 0), col, tipo))
    s.append('</svg>')
    return "".join(s)


# ───────────── Curvas de nivel + perfil ─────────────
def terreno():
    x, y = np.meshgrid(np.linspace(0, 10, 400), np.linspace(0, 7, 280))
    dx = x - 3.2
    sx = np.where(dx > 0, 0.7, 3.4)                                                  # cara este empinada, oeste tendida
    z = 1250 + 950 * np.exp(-(dx ** 2 / sx + (y - 3.6) ** 2 / 3.0))
    z += 640 * np.exp(-((x - 7.2) ** 2 / 1.6 + (y - 3.0) ** 2 / 2.0))                  # cima secundaria
    z += 330 * np.exp(-((x - 5.3) ** 2 / 2.5 + (y - 3.3) ** 2 / 0.35))                 # collado entre las dos
    # espolón hacia el noroeste
    u, v = (x - 3.2) * -0.6 + (y - 3.6) * 0.8, (x - 3.2) * 0.8 + (y - 3.6) * 0.6
    z += 260 * np.exp(-(v ** 2 / 0.12)) * np.exp(-((u - 1.6) ** 2) / 1.8)
    # vaguada hacia el sur desde el collado
    z -= 240 * np.exp(-((x - 5.3) ** 2) / 0.12) / (1 + np.exp((y - 2.4) * 3))
    return x, y, z


def curvas():
    x, y, z = terreno()
    W, H, mx, my, sc = 900, 830, 40, 60, 82  # 10 x 7 unidades -> 820 x 574
    niveles = np.arange(1300, 2300, 40)
    cs = plt.contour(x, y, z, levels=niveles)
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="Mapa de curvas de nivel de dos cimas unidas por un collado, con su perfil del terreno debajo">' % (W, H),
         '<rect width="%d" height="%d" fill="#f4efe7" rx="18"/>' % (W, H),
         '<rect x="%d" y="%d" width="820" height="574" fill="#fbf8f2" stroke="#c9b9a6"/>' % (mx, my)]
    s.append('<g stroke="#e3d9cb" stroke-width="1">' + "".join('<path d="M%d %d V%d"/>' % (mx + k * 82, my, my + 574) for k in range(1, 10)) +
             "".join('<path d="M%d %d H%d"/>' % (mx, my + k * 82, mx + 820) for k in range(1, 7)) + "</g>")
    for lev, segs in zip(cs.levels, cs.allsegs):
        maestra = int(lev) % 200 == 100
        for seg in segs:
            if len(seg) < 3:
                continue
            d = "M" + " L".join("%.1f %.1f" % (mx + px * sc, my + (7 - py) * sc) for px, py in seg[::2])
            s.append('<path d="%s" fill="none" stroke="#a0622d" stroke-width="%s" opacity="%s"/>' % (d, 2.2 if maestra else 1, 1 if maestra else .8))
            if maestra and len(seg) > 60:
                px, py = seg[np.argmin(seg[:, 0] * 0.4 + seg[:, 1])]
                s.append('<text x="%.0f" y="%.0f" %s font-size="11" font-weight="700" fill="#8a4f1f" text-anchor="middle" paint-order="stroke" stroke="#fbf8f2" stroke-width="4">%d</text>' % (mx + px * sc, my + (7 - py) * sc + 4, T, lev))
    plt.close("all")
    # cimas y etiquetas
    def pico(px, py, txt, alt):
        X, Y = mx + px * sc, my + (7 - py) * sc
        return ('<path d="M%.0f %.0f l7 12 h-14z" fill="#3b2a1d"/>' % (X, Y - 8) +
                '<text x="%.0f" y="%.0f" %s font-size="13" font-weight="800" fill="#3b2a1d" text-anchor="middle" paint-order="stroke" stroke="#fbf8f2" stroke-width="4">%s %s</text>' % (X, Y - 14, T, txt, alt))
    zz = z
    def alt(px, py):
        i, j = int(py / 7 * 279), int(px / 10 * 399)
        return int(round(zz[i, j], -1))
    s.append(pico(3.2, 3.6, "Cima", "%d m" % alt(3.2, 3.6)))
    s.append(pico(7.2, 3.0, "Cima", "%d m" % alt(7.2, 3.0)))
    etiquetas = [(5.3, 3.75, "Collado", "#2f7fb5"), (5.3, 0.5, "Vaguada", "#2f7fb5"), (1.2, 6.3, "Espolón", "#a0622d"), (4.3, 5.6, "Curvas juntas:", "#d8322a"), (4.3, 5.35, "pendiente fuerte", "#d8322a"), (1.5, 0.45, "Curvas separadas: terreno suave", "#2f9e44")]
    for px, py, t, c in etiquetas:
        s.append('<text x="%.0f" y="%.0f" %s font-size="13" font-weight="800" fill="%s" text-anchor="middle" paint-order="stroke" stroke="#fbf8f2" stroke-width="5">%s</text>' % (mx + px * sc, my + (7 - py) * sc, T, c, t))
    # línea de corte A–B
    ya = 3.3
    s.append('<path d="M%d %.0f H%d" stroke="#1b120c" stroke-width="2" stroke-dasharray="8 6"/>' % (mx + 0.3 * sc, my + (7 - ya) * sc, mx + 9.7 * sc))
    s.append('<text x="%d" y="%.0f" %s font-size="15" font-weight="900" fill="#1b120c">A</text><text x="%d" y="%.0f" %s font-size="15" font-weight="900" fill="#1b120c">B</text>' % (mx + 6, my + (7 - ya) * sc + 5, T, mx + 9.75 * sc, my + (7 - ya) * sc + 5, T))
    # perfil
    fila = z[int(ya / 7 * 279)]
    xs = np.linspace(0.3, 9.7, 200)
    zs = np.interp(xs, np.linspace(0, 10, 400), fila)
    py0, ph = 690, 110  # base y altura del perfil
    zmin, zmax = 1200, 2300
    pts = " L".join("%.1f %.1f" % (mx + a * sc, py0 + ph - (b - zmin) / (zmax - zmin) * ph * 1.0) for a, b in zip(xs, zs))
    s.append('<text x="%d" y="%d" %s font-size="14" font-weight="800" fill="#3b2a1d">Perfil del corte A–B</text>' % (mx, py0 - 18, T))
    s.append('<path d="M%d %d L%s L%d %d Z" fill="#c9a27a" opacity=".55"/>' % (mx + 0.3 * sc, py0 + ph, pts, mx + 9.7 * sc, py0 + ph))
    s.append('<path d="M%s" fill="none" stroke="#a0622d" stroke-width="2.5"/>' % pts)
    s.append('<text x="%d" y="34" %s font-size="13" fill="#6b5a4a">Equidistancia 40 m · curvas maestras cada 200 m · cuadrícula de 1 km</text>' % (mx, T))
    s.append('</svg>')
    return "".join(s)


if __name__ == "__main__":
    open(os.path.join(BASE, "senales-senderos.svg"), "w").write(senales())
    open(os.path.join(BASE, "curvas-de-nivel.svg"), "w").write(curvas())
    print("ok")
