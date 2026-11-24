"""Escalera de progresión de las 9 rutas de iniciación al alpinismo -> static/img/guias/progresion-alpinismo-gredos.svg"""
import os
T = 'font-family="Inter,system-ui,sans-serif"'
R = [("1", "Morezón", "Plataforma", "#4caf50"), ("2", "La Mira", "Plataforma", "#62b84f"), ("3", "Canchal de la Ceja", "El Travieso", "#7cc24e"),
     ("4", "La Mira", "Km 6 · Conventos", "#a5c94a"), ("5", "Cabeza Nevada", "Navalperal", "#cfc845"), ("6", "Cerro de los Huertos", "Canal de la Pluma", "#e6b43c"),
     ("7", "Casquerazo", "Canal de los Machos", "#ef9330"), ("8", "Morezón", "Canal de las Hoyuelas", "#ec6f33"), ("9", "Almanzor", "Portilla del Crampón", "#e8574a")]
W, H = 1070, 520
s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="Escalera de progresión de nueve rutas de iniciación al alpinismo en Gredos, del Morezón al Almanzor">' % (W, H),
     '<rect width="%d" height="%d" rx="18" fill="#1b120c"/>' % (W, H),
     '<text x="30" y="44" %s font-size="22" font-weight="900" fill="#f3e9df">De la primera cumbre al Almanzor</text>' % T,
     '<text x="30" y="68" %s font-size="13" fill="#b9a593">Cada escalón añade algo nuevo: distancia, desnivel, orientación, pendiente, canal y exposición</text>' % T]
bw, x0, base = 110, 26, 470
for i, (n, a, b, c) in enumerate(R):
    h = 60 + i * 36
    x = x0 + i * (bw + 4)
    s.append('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s"/>' % (x, base - h, bw, h, c))
    s.append('<text x="%d" y="%d" %s font-size="26" font-weight="900" fill="#1b120c" text-anchor="middle">%s</text>' % (x + bw / 2, base - h + 34, T, n))
    s.append('<text x="%d" y="%d" %s font-size="12" font-weight="800" fill="#f3e9df" text-anchor="middle">%s</text>' % (x + bw / 2, base - h - 26, T, a))
    s.append('<text x="%d" y="%d" %s font-size="10.5" fill="#b9a593" text-anchor="middle">%s</text>' % (x + bw / 2, base - h - 10, T, b))
for i, (t, a, b) in enumerate([("Caminar con nieve", 0, 2), ("Distancia y autonomía", 3, 4), ("Canales", 5, 7), ("Objetivo", 8, 8)]):
    xa, xb = x0 + a * (bw + 4), x0 + b * (bw + 4) + bw
    s.append('<path d="M%d %d H%d" stroke="#6b5a4a" stroke-width="2"/><text x="%d" y="%d" %s font-size="12" font-weight="700" fill="#e9a53b" text-anchor="middle">%s</text>' % (xa + 4, base + 14, xb - 4, (xa + xb) / 2, base + 34, T, t))
s.append("</svg>")
open(os.path.join(os.path.dirname(__file__), "..", "static", "img", "guias", "progresion-alpinismo-gredos.svg"), "w").write("".join(s))
print("ok")
