"""Artículos: escalas de dificultad, material invernal, mal de altura, hipotermia y congelaciones, tormentas."""
from arts_util import seccion, tabla, tarjetas, escala, reglas, dos, p, aviso, foto, fotos, ilustracion, blog

ARTS = []

# ───────────────────────────── 1. ESCALAS DE DIFICULTAD ─────────────────────────────
ARTS.append(dict(
    path="/escalas-dificultad-escalada-ferratas-alpinismo-barrancos/",
    corto="Escalas de dificultad en montaña",
    card="Grados de escalada (francés, UIAA, YDS), ferratas K1–K6, alpinismo F–ABO, hielo WI y barrancos v-a-I explicados.",
    titulo="Escalas de dificultad: escalada, ferratas, alpinismo y barrancos",
    meta_title="Grados de escalada, ferrata, alpinismo y barranco | Ad Astra",
    meta_desc="Qué significa un 6a, una ferrata K3, un alpinismo PD o un barranco v3a2II. Tablas de equivalencias (francés, UIAA, YDS, británico) y cómo leer cada escala.",
    lead="Qué significa un 6a+, una ferrata K4, una ruta de alpinismo AD o un barranco v4a3III. Cómo se lee cada escala, tablas de equivalencias entre sistemas y en qué fijarte para elegir una actividad a tu nivel.",
    hero="7d11c597-caa3-4128-a7f5-68709771380b/curso-iniciacion-escalada-en-roca.webp",
    actions='<a class="btn btn-primary" href="#escalada">Escalada</a><a class="btn btn-ghost" href="#ferratas">Ferratas</a><a class="btn btn-ghost" href="#alpinismo">Alpinismo</a><a class="btn btn-ghost" href="#barrancos">Barrancos</a>',
    ico="escalas", og=("Artículo", "Escalas de dificultad", "Escalada, ferratas, alpinismo y barrancos explicados", "#e9a53b"),
    publicado="2026-11-23",
    cuerpo=(
        seccion("Antes de empezar", "Un grado no lo dice todo",
                p("Cada actividad de montaña tiene su propia escala, y casi todas mezclan dos ideas: la <b>dificultad técnica</b> del paso más duro y el <b>compromiso</b> de la actividad entera (lo larga que es, lo fácil que es darse la vuelta, lo lejos que queda la ayuda). Un grado es una opinión consensuada, no una medida exacta: varía según la zona, la época y quién lo abrió.") +
                tarjetas([
                    ("#e9a53b", "Mira el conjunto", "Una vía de 5c de 300 m con seguros lejanos es mucho más seria que un 6b de 15 m bien equipado. Lee la longitud, el equipamiento y el tipo de roca, no solo el número."),
                    ("#4fb3e8", "Las condiciones cambian el grado", "Nieve, hielo, roca mojada o un barranco con mucho caudal convierten una actividad fácil en otra muy difícil. El grado se da siempre para condiciones normales."),
                    ("#7cc47f", "Empieza por debajo", "En una zona nueva, empieza uno o dos grados por debajo de tu nivel hasta que te hagas a su roca y a su forma de graduar."),
                ])) +
        seccion("Escalada en roca", "Grados de escalada: el sistema francés y sus equivalencias",
                p("En España se usa la <b>escala francesa</b>: un número del 3 al 9, una letra (a, b, c) y a veces un «+». Cada salto de letra es un poco más difícil; el «+» es un medio grado. Hasta el 5 se considera escalada fácil o de iniciación, el 6 es el nivel de escalador habitual, el 7 es un nivel alto, del 8 en adelante es élite y el máximo escalado hasta hoy es el 9c.") +
                tabla(["Francés", "UIAA", "YDS (EE. UU.)", "Británico (técnico)", "Nivel orientativo"], [
                    ["3", "III", "5.4", "—", "Trepada fácil. Hay presas grandes y la pared no es vertical."],
                    ["4a–4c", "IV / IV+", "5.5–5.6", "4a", "Iniciación. Los primeros días de curso."],
                    ["5a–5b", "V– / V", "5.7–5.8", "4b–4c", "Iniciación avanzada."],
                    ["5c", "V+", "5.9", "5a", "Ya hay que poner los pies con precisión."],
                    ["6a / 6a+", "VI / VI+", "5.10a / 5.10b", "5b–5c", "Escalador habitual tras unos meses."],
                    ["6b / 6b+", "VII– / VII", "5.10c / 5.10d", "5c–6a", "Nivel medio consolidado."],
                    ["6c / 6c+", "VII+", "5.11a / 5.11b", "6a–6b", "Nivel medio-alto."],
                    ["7a", "VIII–", "5.11d", "6b", "Nivel alto. Entrenamiento regular."],
                    ["7b", "VIII", "5.12b", "6c", "Muy alto."],
                    ["8a", "IX+ / X–", "5.13b", "7a", "Élite aficionada."],
                    ["9a", "XI", "5.14d", "—", "Élite mundial."],
                    ["9b", "XI+", "5.15b", "—", "Solo unas decenas de escaladores en el mundo."],
                    ["9c", "XII", "5.15d", "—", "El grado más alto escalado hasta hoy (ver abajo)."],
                ]) +
                '<p class="small muted" style="margin-top:10px">Las equivalencias entre sistemas son aproximadas: cada fuente da una tabla algo distinta.</p><p style="margin-top:14px"><b>¿Cuál es el techo actual?</b> El <b>9c</b>. La primera vía de ese grado fue <i>Silence</i> (Flatanger, Noruega), de Adam Ondra en 2017. Después llegaron <i>DNA</i> (Verdon, Francia), de Seb Bouin en 2022, y <i>B.I.G.</i> (Flatanger), de Jakob Schubert en 2023. En España, Jorge Díaz-Rullo propuso 9c para <i>Café Colombia</i>, en Margalef, en 2026.</p>' +
                foto("escalada-rodellar", "<i>El Delfín</i>, un 7c+ en el cañón del Mascún (Rodellar, Huesca), una de las grandes zonas de escalada deportiva de España.") +
                dos("Escalada clásica y de aventura",
                    reglas(["La vía se gradúa por su <b>paso más difícil</b> y a veces se añade el grado obligado (lo mínimo que tienes que escalar sin tirar de los seguros).",
                            "En las vías largas, mira también la <b>longitud</b> y el <b>equipamiento</b>: «vía equipada» (con parabolts), «semiequipada» o «desequipada» (tú pones los seguros: friends, fisureros).",
                            "En las reseñas antiguas de Gredos o Pedriza los grados suelen ser «duros»: un IV+ clásico puede sentirse como un 5b moderno.",
                            "En artificial se usan los grados A0–A5 (con seguros fijos y estribos) o C1–C5 (sin martillo)."]),
                    "Bloque (boulder)",
                    reglas(["En España se usa la <b>escala Fontainebleau</b> (Font), con números y letras como la francesa pero en mayúscula: 4, 5, 6A, 6A+, 6B… hasta 9A.",
                            "Un 6A de bloque <b>no</b> es lo mismo que un 6a de vía: el bloque concentra la dificultad en pocos movimientos y suele ser bastante más duro.",
                            "En EE. UU. se usa la escala V (V0 ≈ 5, V3 ≈ 6A+, V5 ≈ 6C, V10 ≈ 7C+).",
                            "Si te apetece probar, mira nuestras zonas de <a href=\"/actividades/boulder-las-tuerces/\">boulder en Las Tuerces</a> y <a href=\"/actividades/boulder-zona-centro-salamanca-caceres/\">Zona Centro</a>."])),
                False, "escalada") +
        seccion("Vías ferratas", "Grados de las vías ferratas: K1 a K6 y la escala francesa",
                p("Las ferratas se gradúan sobre todo con la <b>escala Hüsler</b> (K1–K6), que mide lo vertical que es la vía, lo que tienes que tirar de brazos y lo buenos que son los apoyos. También verás la <b>escala francesa</b> (F, PD, AD, D, MD, ED) en muchas reseñas.") +
                escala([
                    ("#4caf50", "K1", "Fácil (F)", "Poco vertical, con buenos apoyos y escalones. Para empezar y para niños con experiencia."),
                    ("#9ccc65", "K2", "Poco difícil (PD)", "Tramos verticales cortos, siempre con buenos apoyos. Un primer día bien llevado."),
                    ("#e6c32e", "K3", "Algo difícil (AD)", "Verticales más largos, algún paso desplomado corto. Hace falta algo de fuerza de brazos."),
                    ("#f08a24", "K4", "Difícil (D)", "Verticales largos y desplomes. Hay que tirar mucho de brazos: no es para primerizos."),
                    ("#e8574a", "K5", "Muy difícil (MD)", "Desplomada y continua, con apoyos escasos. Exige fuerza y técnica de escalada."),
                    ("#a55fd6", "K6", "Extremadamente difícil (ED)", "Casi deportiva: muy desplomada y sin apenas grapas. Para muy pocos."),
                ]) +
                foto("ferrata-sacs", "Tramo vertical de una vía ferrata: cable de vida, grapas y mucho patio.") +
                reglas(["Muchas ferratas tienen <b>tramos de distinto grado</b> y a veces una variante más difícil: la reseña suele dar el grado del tramo más duro.",
                        "Fíjate en el <b>tiempo de aproximación y retorno</b> y en si hay escapes: una K3 de cinco horas cansa más que una K4 corta.",
                        "Una ferrata es terreno vertical aunque tenga grapas: casco, arnés y disipador homologado (EN 958) siempre. Y nunca con tormenta: el cable atrae los rayos (lo explicamos en <a href=\"/tormentas-en-la-montana/\">tormentas en la montaña</a>).",
                        "Hacemos ferratas guiadas en <a href=\"/actividades/via-ferrata-salamanca/\">Salamanca</a>, <a href=\"/actividades/via-ferrata-burgos/\">Burgos</a> y <a href=\"/actividades/vias-ferratas-leon/\">León</a>."]),
                True, "ferratas") +
        seccion("Alpinismo", "Grados de alpinismo: de F a ABO, hielo WI y mixto M",
                p("Para valorar una ruta de alpinismo en conjunto se usa la <b>escala francesa de dificultad global</b> (también llamada IFAS). Resume la dificultad técnica, la exposición, la longitud y el compromiso de toda la ruta. Muchas veces va acompañada del grado del paso de roca más difícil (por ejemplo, «AD, IV») o de la inclinación máxima de la nieve («PD, 40°»).") +
                tabla(["Grado", "Nombre", "Qué te vas a encontrar"], [
                    ["F", "Fácil", "Caminar por nieve o pedreras poco inclinadas, alguna trepada corta. Glaciar sencillo. Piolet y crampones, pero apenas cuerda."],
                    ["PD", "Poco difícil", "Pendientes de nieve de hasta 35–40°, crestas fáciles y trepadas de II–III. Ya hace falta saber usar la cuerda."],
                    ["AD", "Algo difícil", "Nieve o hielo de 40–55°, pasos de roca de III–IV. Hay que asegurar algunos largos."],
                    ["D", "Difícil", "Pendientes de 50–70°, roca de IV–V y rutas largas. Asegurar casi todo el tiempo."],
                    ["MD", "Muy difícil", "Hielo de 65–80°, roca de V–VI, ruta larga y con poco escape. En las reseñas francesas aparece como TD (<i>très difficile</i>)."],
                    ["ED / ABO", "Extremadamente difícil / abominable", "Hielo vertical y roca de VI en adelante con gran compromiso. ED1, ED2… indican el escalón dentro del grado."],
                ]) +
                '<p style="margin-top:14px">La subida invernal más clásica de nuestra zona, el <b>Almanzor por la canal de la Portilla del Crampón</b>, ronda el <b>PD</b>: pendientes de 40–50° y riesgo de caída si no sabes frenar con el piolet. Aprende a hacerlo en nuestro <a href="/actividades/cursos-alpinismo/">curso de alpinismo</a>.</p>' +
                foto("escalada-hielo", "Escalada en una cascada de hielo: aquí se usan los grados WI.") +
                blog("Hielo en Gredos, en el blog de Jairo", [("https://jairogredos.blogspot.com/2023/02/cascadas-del-callejon-de-la-lanchuela.html", "Cascadas del Callejón de la Lanchuela"), ("https://jairogredos.blogspot.com/2012/09/escalada-en-hielo-en-los-canalizos.html", "Escalada en hielo en Los Canalizos (Hoya Mayor)"), ("https://jairogredos.blogspot.com/2012/09/picando-hielo-en-el-circo-de-pena-negra.html", "Picando hielo en el Circo de Peña Negra de Becedas")]) +
                dos("Escalada en hielo (WI)",
                    reglas(["<b>WI1–WI2:</b> hielo de 50–60°, fácil de proteger.",
                            "<b>WI3:</b> tramos de 70–80° con descansos. El nivel de entrada a las cascadas.",
                            "<b>WI4:</b> tramos verticales cortos (unos 10 m) seguidos.",
                            "<b>WI5:</b> largos verticales sostenidos, hielo menos regular.",
                            "<b>WI6–WI7:</b> verticales o desplomados, hielo delgado o en coliflor: técnicos y psicológicamente duros.",
                            "Si el hielo es de glaciar en lugar de cascada se escribe <b>AI</b> (Alpine Ice)."]),
                    "Mixto (M) y compromiso",
                    reglas(["La escala <b>M</b> (M1–M13) gradúa la escalada mixta, con piolets y crampones sobre roca y hielo. M4–M5 ya es escalada técnica; M8 o más es dry-tooling de alto nivel.",
                            "El compromiso se indica a veces con números romanos <b>I–VII</b>: I es una ruta corta y cerca del coche; VI–VII son varias jornadas en una pared aislada.",
                            "En Escocia el invierno se gradúa con su propia escala, en números romanos (I–XII)."])),
                False, "alpinismo") +
        seccion("Barrancos", "Grados de barranquismo: vertical, acuático y compromiso",
                p("Los barrancos se gradúan con tres valores que se escriben juntos, por ejemplo <b>v3 a2 II</b>. Es el sistema de la Federación Francesa (FFME), que usa también la española. Cada valor responde a una pregunta:") +
                tabla(["Valor", "Qué mide", "De… a…"], [
                    ["v (vertical)", "La dificultad de los rápeles y destrepes: altura, si son fáciles de montar, si hay pasamanos, si caen dentro del agua.", "v1 (sin rápeles o muy cortos) a v7 (rápeles muy largos, fraccionados, en cascadas potentes)."],
                    ["a (acuático)", "La dificultad en el agua: nado, saltos, toboganes, sifones y la fuerza de la corriente.", "a1 (sin nado o casi) a a7 (corriente muy fuerte, rebufos y peligros serios)."],
                    ["I–VI (compromiso)", "La envergadura: duración, lo fácil que es salir a mitad y lo lejos que queda la ayuda.", "I (unas horas, con escapes) a VI (más de un día o sin escapes)."],
                ]) +
                escala([
                    ("#4caf50", "v1–v2 · a1–a2", "Iniciación", "Rápeles cortos y sencillos, poca agua. El primer barranco."),
                    ("#e6c32e", "v3 · a3", "Intermedio", "Rápeles de hasta 30 m, algo de nado y saltos opcionales. Ya hay que saber montar la cuerda."),
                    ("#f08a24", "v4–v5 · a4", "Avanzado", "Rápeles largos o con agua, corrientes que pueden arrastrarte. Formación y experiencia."),
                    ("#e8574a", "v6–v7 · a5–a7", "Experto", "Rápeles en cascadas fuertes, rebufos y sifones. Muy pocas personas."),
                ]) +
                foto("barranco-rapel", "Rápel dentro de la cascada: la cuerda, la altura y la fuerza del agua deciden los grados v y a.") +
                reglas(["El grado <b>acuático cambia con el caudal</b>: con el agua alta, un barranco a2 puede comportarse como un a4. Consulta el <a href=\"/barrancos-caudal/\">caudal en tiempo real</a> antes de ir.",
                        "En reseñas antiguas verás la escala de 1 a 6 de la Federación Española o letras como «A» y «B». Si la reseña no explica su escala, desconfía del grado.",
                        "¿Quieres empezar? Mira nuestros <a href=\"/actividades/barranquismo-avila/\">barrancos en Ávila</a> o el <a href=\"/actividades/curso-barranquismo/\">curso de barranquismo</a>."]),
                True, "barrancos") +
        seccion("Senderismo", "¿Y las rutas a pie? El método MIDE",
                p("Para las rutas de senderismo y montaña se usa en España el <b>MIDE</b> (Método de Información de Excursiones), que puntúa de 1 a 5 cuatro cosas: el <b>medio</b> (los peligros del terreno y la meteo), el <b>itinerario</b> (lo fácil que es orientarse), el <b>desplazamiento</b> (el tipo de terreno) y el <b>esfuerzo</b> (el tiempo que se tarda). Puedes calcular la ficha MIDE de tu ruta con nuestra <a href=\"/calculadora-rutas/\">calculadora de rutas</a>."))
    ),
    faq=[
        ("¿Qué grado de escalada es para principiantes?", "En la escala francesa, entre el 3 y el 5a. En un curso de iniciación se suele empezar por 4a–4c y en pocos días muchos alumnos suben vías de 5a–5b en polea."),
        ("¿Un 6a francés a qué equivale en UIAA y en YDS?", "Aproximadamente a un VI en la escala UIAA y a un 5.10a en la escala americana YDS. Las equivalencias son orientativas y varían algo según la tabla."),
        ("¿Qué significa K3 en una vía ferrata?", "Es el grado intermedio de la escala Hüsler (K1–K6): tramos verticales más largos y algún paso desplomado corto, que piden algo de fuerza de brazos. Equivale más o menos a AD en la escala francesa."),
        ("¿Qué es un alpinismo PD?", "Poco difícil: pendientes de nieve de hasta 35–40°, crestas fáciles y trepadas de II–III. Hace falta saber usar el piolet, los crampones y la cuerda, aunque no hay largos técnicos."),
        ("¿Qué significa v3a2II en un barranco?", "Que tiene una dificultad vertical 3 (rápeles de hasta unos 30 m, fáciles de montar), una dificultad acuática 2 (algo de agua, nado corto) y un compromiso II (media jornada con algún escape). Es un barranco de nivel intermedio-bajo."),
        ("¿El grado de bloque y el de vía son iguales?", "No. Un 6A de bloque (escala Fontainebleau, en mayúscula) es bastante más difícil que un 6a de vía, porque concentra la dificultad en pocos movimientos."),
    ],
    fuentes=[
        ("https://www.theuiaa.org/", "UIAA: Federación Internacional de Escalada y Montañismo"),
        ("https://www.fedme.es/", "FEDME: Federación Española de Deportes de Montaña y Escalada"),
        ("https://www.ffme.fr/", "FFME: Federación Francesa de Montaña y Escalada (grados de barrancos)"),
        ("https://www.montanasegura.com/", "Montaña Segura: el método MIDE"),
    ],
))

# ───────────────────────────── 2. MATERIAL INVERNAL ─────────────────────────────
ARTS.append(dict(
    path="/crampones-piolet-botas-material-invernal/",
    corto="Crampones, piolet y botas de invierno",
    card="Crampones automáticos, semiautomáticos o de correas, 10 o 12 puntas, piolet de travesía o técnico y botas blandas, semirrígidas o rígidas.",
    titulo="Material invernal: crampones, piolet y botas",
    meta_title="Crampones, piolet y botas de montaña: cómo elegir | Ad Astra",
    meta_desc="Crampones automáticos, semiautomáticos o de correas, de 10 o 12 puntas; piolet de travesía o técnico y botas blandas, semirrígidas o rígidas.",
    lead="Qué crampones comprar (automáticos, semiautomáticos o de correas; de 10 o 12 puntas), qué piolet necesitas y de qué largo, y por qué la bota manda: qué crampón va con cada bota.",
    hero="0c5376bd-2231-4c62-b798-6f0139e73cd7/cursos-alpinismo.webp",
    actions='<a class="btn btn-primary" href="#compatibilidad">Tabla de compatibilidad</a><a class="btn btn-ghost" href="#crampones">Crampones</a><a class="btn btn-ghost" href="#piolet">Piolet</a>',
    ico="invernal", og=("Artículo", "Crampones, piolet y botas", "Cómo elegir el material de invierno y qué es compatible", "#bfe0f7"),
    publicado="2026-11-23",
    cuerpo=(
        seccion("Lo primero", "Empieza por la bota: es la que decide",
                p("Los crampones se eligen según la bota, y la bota según lo que vayas a hacer. Lo que importa es <b>lo rígida que es la suela</b> y si tiene <b>rebordes</b> (las muescas de delante y de detrás donde encajan las palancas y los estribos del crampón).") +
                escala([
                    ("#4caf50", "Blanda", "Bota blanda", "Suela flexible que se dobla al caminar, sin rebordes. Solo admite crampones de correas, y mejor si la suela tiene algo de rigidez. Si es una bota de senderismo muy flexible, como mucho microcrampones para caminos helados. Para senderismo invernal."),
                    ("#e6c32e", "Semirrígida", "Bota semirrígida", "Suela bastante rígida y un reborde en el talón. Admite crampones de correas y semiautomáticos. La más versátil para el alpinismo clásico."),
                    ("#e8574a", "Rígida", "Bota rígida", "Suela totalmente rígida, con rebordes delante y detrás. Admite todos los crampones, incluidos los automáticos. Alpinismo técnico, hielo y cascadas."),
                ]) +
                fotos(("bota-crampones", "Bota de montaña con crampones de 12 puntas."), ("crampon-hielo", "Las puntas frontales de un crampón mordiendo el hielo."))) +
        seccion("Crampones", "Automáticos, semiautomáticos o de correas",
                tabla(["Tipo", "Cómo se sujeta", "Bota", "Para qué"], [
                    ["De correas (o «universales»)", "Cestas de plástico delante y detrás y una correa.", "Blanda, semirrígida o rígida", "Senderismo invernal, travesía y alpinismo fácil. Se adaptan a casi cualquier bota de montaña."],
                    ["Semiautomáticos", "Cesta de plástico delante y una palanca (talonera) atrás.", "Semirrígida o rígida", "Alpinismo clásico: corredores, canales, crestas. El más polivalente."],
                    ["Automáticos", "Un estribo metálico delante y una palanca atrás.", "Rígida", "Alpinismo técnico, hielo y mixto. Más precisos y firmes, pero exigen una bota totalmente rígida."],
                ]) +
                dos("¿10 o 12 puntas?",
                    reglas(["<b>10 puntas</b>: más ligeros. Para senderismo invernal, travesía y pendientes moderadas. Suelen ir con puntas frontales más cortas.",
                            "<b>12 puntas</b>: el estándar para el alpinismo. Tienen dos puntas frontales más largas y un segundo par inclinado que permite subir de frente por pendientes fuertes.",
                            "<b>Puntas frontales verticales o monopunta</b>: para hielo y mixto. No hacen falta para el alpinismo clásico.",
                            "<b>Acero o aluminio</b>: el aluminio pesa la mitad pero se desgasta muy rápido en roca y no muerde bien el hielo duro. Para nuestras sierras, mejor acero."]),
                    "Detalles que importan",
                    reglas(["<b>Antizuecos (antibots)</b>: placas de plástico o goma debajo del crampón que evitan que la nieve húmeda se pegue y forme una bola. Imprescindibles: un crampón con zueco no agarra.",
                            "<b>Ajuste</b>: pruébalos en casa con tu bota. Bien puestos, puedes levantar el pie y sacudirlo sin que se muevan, y las puntas frontales sobresalen 2–3 cm de la bota.",
                            "<b>Afilado</b>: con lima, nunca con radial (destempla el acero). Las puntas frontales se afilan por arriba.",
                            "<b>Microcrampones</b> no son crampones: valen para pistas heladas, no para pendientes de nieve dura."])),
                True, "crampones") +
        seccion("Piolet", "Piolet de travesía o técnico",
                p("La norma europea EN 13089 distingue dos tipos: <b>tipo 1 (B, básico)</b> y <b>tipo 2 (T, técnico)</b>. El T aguanta más esfuerzo y se puede usar para hacer anclajes o tracciones en hielo.") +
                tabla(["", "Piolet de travesía (clásico)", "Piolet técnico"], [
                    ["Mango", "Recto o con una curva suave.", "Curvado, con empuñadura ergonómica y a menudo sin pincho (regatón) largo."],
                    ["Pica", "Clásica, poco inclinada: muerde bien al apoyarse y para frenar.", "Muy inclinada y dentada, para clavar en hielo y traccionar."],
                    ["Normalmente", "Tipo B. A veces tipo T.", "Tipo T."],
                    ["Para qué", "Caminar por nieve, apoyarse, autodetenerse, hacer escalones. Uno solo.", "Corredores empinados, hielo y mixto. Se usan dos (una pareja)."],
                    ["Longitud", "50–70 cm. La tendencia actual es más corto (50–60 cm) que antes.", "45–52 cm."],
                ]) +
                '<div style="max-width:360px;margin:0 auto">' + foto("piolet", "Piolet clásico de travesía: mango recto, pica poco inclinada y pala.") + '</div>' +
                reglas(["<b>¿Qué largo?</b> Cogido por la cabeza con el brazo estirado y relajado, el regatón debe llegar más o menos a la mitad de la pantorrilla o al tobillo. Más corto si vas a hacer pendientes fuertes; un poco más largo si es sobre todo para apoyarte al caminar.",
                        "<b>Dragonera o correa</b>: evita perderlo si se te cae al frenar. En terreno técnico mucha gente prefiere no llevarla.",
                        "<b>Saber autodetenerse</b> es más importante que el piolet que tengas. Un resbalón en nieve dura a 35° acelera en segundos. Practícalo en una pendiente con una salida segura o en un <a href=\"/actividades/cursos-alpinismo/\">curso de alpinismo</a>."])) +
        seccion("Compatibilidad", "Tabla de compatibilidad bota–crampón",
                tabla(["Bota ↓ · Crampón →", "De correas", "Semiautomático", "Automático"], [
                    ["Blanda", "✓ (si la suela no es muy flexible)", "✗", "✗"],
                    ["Semirrígida", "✓", "✓", "✗"],
                    ["Rígida", "✓", "✓", "✓"],
                ]) +
                aviso("<b>No fuerces la combinación.</b> Unos crampones semiautomáticos o automáticos en una bota que no es rígida se doblan, se sueltan o se rompen en el peor momento. Si dudas, llévate la bota a la tienda y pruébalo allí."),
                True, "compatibilidad") +
        seccion("Por actividad", "¿Qué me compro?",
                tarjetas([
                    ("#4caf50", "Senderismo invernal", "Bota blanda de montaña (o semirrígida), crampones de correas de 10 puntas con antizuecos y un piolet de travesía de 55–65 cm. Bastones con roseta de nieve."),
                    ("#e6c32e", "Alpinismo clásico (Gredos, Guadarrama, Picos)", "Bota semirrígida, crampones semiautomáticos de 12 puntas y un piolet de travesía tipo T de 50–60 cm. Es el equipo que usamos en el Almanzor o en Peñalara."),
                    ("#e8574a", "Corredores empinados y hielo", "Bota rígida, crampones automáticos (o semiautomáticos de puntas verticales) y dos piolets técnicos."),
                    ("#4fb3e8", "Con raquetas o esquís", "Lo explicamos en el artículo de <a href=\"/raquetas-de-nieve-y-esqui-de-travesia/\">raquetas y esquí de travesía</a>."),
                ]) +
                '<p style="margin-top:20px">Y no te olvides del resto: casco, ropa de invierno (<a href="/teoria-de-las-capas/">la teoría de las capas</a>), gafas de categoría 4 (<a href="/rayos-uv-proteccion-solar-montana/">por qué</a>) y, si hay riesgo de aludes, ARVA, pala y sonda (<a href="/como-leer-la-nieve-y-los-aludes/">cómo leer la nieve</a>). Tienes la lista completa en la <a href="/lista-material-montana/">lista de material</a>. Si no quieres comprar todavía, también <a href="/actividades/alquiler-material-montana/">alquilamos material</a>.</p>')
    ),
    faq=[
        ("¿Qué crampones necesito para el Almanzor en invierno?", "Unos crampones de 12 puntas de acero, semiautomáticos si tu bota es semirrígida (con reborde en el talón) o de correas si es una bota blanda de montaña, siempre con antizuecos. Y piolet, casco y saber autodetenerse."),
        ("¿Puedo poner crampones en unas botas de senderismo?", "En una bota de senderismo muy flexible no se pueden poner crampones de verdad, solo microcrampones para caminos helados. Para crampones de correas necesitas una bota de montaña con la suela algo rígida."),
        ("¿Qué diferencia hay entre crampones automáticos y semiautomáticos?", "Los automáticos llevan un estribo metálico delante y necesitan una bota rígida con reborde delantero. Los semiautomáticos llevan una cesta de plástico delante y sirven también en botas semirrígidas, que solo tienen reborde en el talón."),
        ("¿Qué tamaño de piolet necesito?", "Para la travesía y el alpinismo clásico, entre 50 y 70 cm. Cogido por la cabeza con el brazo relajado, la punta debe quedar por la mitad de la pantorrilla o el tobillo. Para terreno empinado, mejor corto."),
        ("¿Para qué sirven los antizuecos?", "Evitan que la nieve húmeda se pegue bajo el crampón y forme una bola que impide que las puntas agarren. Es una de las causas más comunes de resbalones en primavera."),
    ],
    fuentes=[
        ("https://www.petzl.com/ES/es", "Petzl: compatibilidad entre crampones y calzado"),
        ("https://www.theuiaa.org/safety-standards/", "UIAA: normas de seguridad del material"),
        ("https://www.grivel.com/", "Grivel: crampones y piolets"),
        ("https://www.fedme.es/", "FEDME"),
    ],
    nota="Cada marca matiza la compatibilidad entre sus crampones y las botas: consulta siempre las instrucciones del fabricante.",
))

# ───────────────────────────── 3. MAL DE ALTURA ─────────────────────────────
ARTS.append(dict(
    path="/mal-de-altura-sintomas-prevencion/",
    corto="Mal de altura",
    card="Síntomas del mal agudo de montaña, edema cerebral y pulmonar, cómo aclimatarse y cuándo bajar.",
    titulo="Mal de altura: síntomas, prevención y qué hacer",
    meta_title="Mal de altura: síntomas, prevención y qué hacer | Ad Astra",
    meta_desc="Qué es el mal agudo de montaña, a partir de qué altitud aparece, cómo reconocer el edema cerebral y pulmonar, cómo aclimatarse y cuándo hay que bajar.",
    lead="Qué es el mal agudo de montaña, a partir de qué altura aparece, cómo reconocer a tiempo los casos graves (edema cerebral y pulmonar) y cómo aclimatarse bien para el Toubkal, el Mont Blanc o el Kilimanjaro.",
    hero="9e905542-b5a0-4f9d-b7f3-a115afc0e1ea/otros-media-11.webp",
    actions='<a class="btn btn-primary" href="#sintomas">Síntomas</a><a class="btn btn-ghost" href="#aclimatar">Cómo aclimatarse</a>',
    ico="altura", og=("Artículo", "Mal de altura", "Síntomas, prevención y cuándo hay que bajar", "#4fb3e8"),
    publicado="2026-11-23",
    cuerpo=(
        seccion("Por qué pasa", "Menos presión, menos oxígeno",
                p("El aire de la montaña tiene la misma proporción de oxígeno que el del mar (un 21 %), pero la <b>presión es menor</b> y en cada respiración entra menos oxígeno a la sangre. A 3.000 m hay un 30 % menos de presión que a nivel del mar; a 5.500 m, la mitad. El cuerpo se adapta (respira más, el corazón late más deprisa y con los días fabrica más glóbulos rojos), pero necesita tiempo. Si subes más rápido de lo que te adaptas, aparece el mal de altura.") +
                fotos(("toubkal-senderistas", "Subiendo al Toubkal (4.167 m), en el Atlas: a esta altura el mal de altura ya es frecuente."), ("aconcagua", "La cara sur del Aconcagua (6.961 m): por encima de 5.500 m el cuerpo no llega a adaptarse del todo.")) +
                tabla(["Altitud", "Ejemplos", "Qué esperar"], [
                    ["Hasta 2.500 m", "Gredos, Guadarrama, Picos de Europa", "Prácticamente no hay mal de altura. Puedes notar más cansancio y peor sueño."],
                    ["2.500–3.500 m", "Mulhacén (3.479 m), Aneto (3.404 m), Teide (3.715 m)", "Puede aparecer un mal agudo de montaña leve, sobre todo si duermes alto o subes en teleférico."],
                    ["3.500–5.500 m", "Toubkal (4.167 m), Mont Blanc (4.808 m)", "Es frecuente sin aclimatación. Ya pueden aparecer los edemas."],
                    ["Más de 5.500 m", "Kilimanjaro (5.895 m), Aconcagua (6.961 m)", "El cuerpo no se adapta del todo: solo se puede estar un tiempo limitado."],
                ])) +
        seccion("Síntomas", "Cómo reconocer cada forma de mal de altura",
                tarjetas([
                    ("#e6c32e", "Mal agudo de montaña (MAM)", "Dolor de cabeza en las primeras 6–24 horas tras subir, junto con alguno de estos: náuseas o falta de apetito, cansancio, mareo o insomnio. Es como una resaca. Es el más común y, si no subes más, se pasa en uno a tres días."),
                    ("#e8574a", "Edema cerebral de altura (ECGA)", "Es un MAM que empeora: dolor de cabeza muy fuerte que no cede, vómitos, <b>falta de coordinación</b> (no puede caminar en línea recta talón con punta), confusión, somnolencia, comportamiento raro. Es una emergencia: puede ser mortal en horas."),
                    ("#a55fd6", "Edema pulmonar de altura (EPGA)", "Ahogo desproporcionado al esfuerzo que llega a notarse <b>en reposo</b>, tos seca y luego con espuma o sangre, labios morados, gran cansancio. Suele aparecer la segunda o tercera noche en altura. También es una emergencia."),
                ]) +
                aviso("<b>Prueba rápida de ataxia:</b> pide a la persona que camine en línea recta poniendo el talón de un pie justo delante de la punta del otro. Si se tambalea o no puede, sospecha edema cerebral y <b>baja ya</b>."),
                False, "sintomas") +
        seccion("Qué hacer", "La regla de oro: no subas con síntomas, baja si empeoras",
                reglas(["<b>Con un MAM leve:</b> no subas más. Descansa, bebe, come algo ligero y toma un analgésico (paracetamol o ibuprofeno). Si a las 24 horas estás bien, puedes seguir subiendo con calma.",
                        "<b>Si los síntomas empeoran a pesar del descanso, baja.</b> Muchas veces basta con bajar 300–1.000 m para mejorar mucho.",
                        "<b>Edema cerebral o pulmonar:</b> bajar inmediatamente, aunque sea de noche, acompañado y con ayuda. Oxígeno si lo hay. Pedid rescate.",
                        "<b>Nunca dejes solo</b> a alguien con mal de altura: puede empeorar y desorientarse.",
                        "Si tienes mal de altura, asume que es mal de altura hasta que se demuestre lo contrario (no «un poco de cansancio»).",
                        "Los medicamentos como la acetazolamida o la dexametasona pueden ayudar a prevenir o tratar, pero <b>los tiene que pautar un médico</b>. Consulta en una consulta de viajero o de medicina de montaña antes del viaje."]),
                True) +
        seccion("Prevención", "Cómo aclimatarse",
                reglas(["<b>Sube despacio.</b> Por encima de 3.000 m, no aumentes la altura a la que duermes más de 300–500 m por día.",
                        "<b>Un día de descanso cada 3–4 días</b> (o cada 1.000 m de desnivel acumulado) durmiendo a la misma altura.",
                        "<b>«Sube alto, duerme bajo»:</b> los días de aclimatación sube a una cota más alta y vuelve a dormir abajo.",
                        "<b>Bebe suficiente</b> (la orina debe ser clara) y evita el alcohol y las pastillas para dormir los primeros días.",
                        "<b>Come hidratos de carbono</b> y no te pegues palizas los primeros días.",
                        "<b>Tener buena forma física no protege.</b> Hay gente muy en forma que lo pasa mal y gente sedentaria que se aclimata bien. Lo mejor que predice cómo te va a ir es cómo te fue en otras ocasiones.",
                        "Si ya tuviste un edema, consulta a un médico antes de volver a la altura."]) +
                '<p style="margin-top:16px">Por eso los programas de nuestros viajes al <a href="/actividades/ascension-al-toubkal/">Toubkal</a> o el <a href="/actividades/trekking-tour-del-mont-blanc/">Tour del Mont Blanc</a> incluyen días de aproximación antes de las cotas altas.</p>',
                False, "aclimatar")
    ),
    faq=[
        ("¿A partir de qué altura da el mal de altura?", "Puede empezar a partir de unos 2.500 m, sobre todo si se duerme a esa altura o se sube muy rápido (en coche o teleférico). Por debajo de 2.500 m es muy raro."),
        ("¿Puede dar mal de altura en Sierra Nevada o en el Teide?", "Sí, puede aparecer un mal agudo de montaña leve en el Mulhacén o el Teide, sobre todo si se sube muy rápido desde el nivel del mar o se duerme en el refugio. Los edemas graves son muy raros a esas alturas."),
        ("¿Cuáles son los primeros síntomas del mal de altura?", "Dolor de cabeza a las pocas horas de subir, acompañado de náuseas o falta de apetito, cansancio, mareo o dificultad para dormir."),
        ("¿Qué hago si tengo mal de altura?", "No sigas subiendo. Descansa, bebe y toma un analgésico. Si en 24 horas no mejoras o empeoras, baja. Si hay falta de coordinación, confusión o ahogo en reposo, baja inmediatamente y pide ayuda."),
        ("¿Estar en forma evita el mal de altura?", "No. La forma física no protege del mal de altura. Lo que protege es subir despacio y dar tiempo al cuerpo para aclimatarse."),
    ],
    fuentes=[
        ("https://www.theuiaa.org/mountain-medicine/", "UIAA: comisión médica y recomendaciones"),
        ("https://www.wms.org/", "Wilderness Medical Society: guías clínicas de enfermedad de altura"),
        ("https://www.sanidad.gob.es/areas/sanidadExterior/laSaludTambienViaja/home.htm", "Ministerio de Sanidad: la salud también viaja"),
        ("https://www.semam.org/", "SEMAM: Sociedad Española de Medicina y Auxilio en Montaña"),
    ],
    nota="Este artículo es divulgativo y no sustituye el consejo de un médico. Antes de un viaje a gran altura, pide cita en una consulta de medicina del viajero o de montaña.",
))

# ───────────────────────────── 4. HIPOTERMIA, CONGELACIONES Y BOTIQUÍN ─────────────────────────────
ARTS.append(dict(
    path="/hipotermia-congelaciones-botiquin-montana/",
    corto="Hipotermia, congelaciones y botiquín",
    card="Cómo reconocer y tratar la hipotermia y las congelaciones, y qué llevar en el botiquín de montaña.",
    titulo="Hipotermia y congelaciones: qué hacer, y el botiquín de montaña",
    meta_title="Hipotermia y congelaciones en montaña: qué hacer | Ad Astra",
    meta_desc="Cómo reconocer la hipotermia leve, moderada y grave, qué hacer con una congelación (y qué no) y qué llevar en el botiquín de montaña.",
    lead="Cómo reconocer la hipotermia a tiempo, qué hacer (y qué no) con una congelación, y qué llevar en un botiquín de montaña realista. Primeros auxilios básicos para cuando la ayuda está lejos.",
    hero="052618bc-b465-47b0-bb3d-0583d186f366/curso-autorrescate.webp",
    actions='<a class="btn btn-primary" href="#hipotermia">Hipotermia</a><a class="btn btn-ghost" href="#congelaciones">Congelaciones</a><a class="btn btn-ghost" href="#botiquin">Botiquín</a>',
    ico="botiquin", og=("Artículo", "Hipotermia y congelaciones", "Qué hacer y qué llevar en el botiquín de montaña", "#e8574a"),
    publicado="2026-11-23",
    cuerpo=(
        aviso("<b>En una emergencia, llama al 112.</b> Funciona aunque no tengas cobertura de tu compañía si hay otra red disponible. Indica dónde estás (coordenadas del móvil), qué ha pasado, cuántas personas hay y cómo están.").replace('style="margin-top:20px', 'style="margin:20px auto;max-width:1100px') +
        seccion("Hipotermia", "Hipotermia: cuando el cuerpo pierde más calor del que produce",
                p("La hipotermia es la bajada de la temperatura interna por debajo de 35 °C. No hace falta un frío extremo: <b>la mayoría de las hipotermias en montaña ocurren entre 0 y 10 °C</b>, con viento y ropa mojada (por la lluvia o el sudor), en alguien cansado, que no ha comido o que se ha quedado quieto por una lesión. También en barrancos, por el agua fría.") +
                escala([
                    ("#e6c32e", "Leve", "35–32 °C", "Tiritona intensa, manos torpes, piel fría y pálida. La persona está consciente y habla con normalidad, aunque algo apática."),
                    ("#f08a24", "Moderada", "32–28 °C", "<b>Deja de tiritar</b> aunque siga teniendo frío. Confusión, habla torpe, somnolencia, tropiezos, decisiones raras (a veces se quita ropa)."),
                    ("#e8574a", "Grave", "Menos de 28 °C", "Inconsciente, respiración y pulso muy lentos y débiles. Puede parecer muerta. Riesgo de parada cardiaca."),
                ]) +
                dos("Qué hacer",
                    reglas(["<b>Para la pérdida de calor:</b> busca refugio del viento y la lluvia, aísla del suelo (esterilla, mochila, cuerdas) y quita la ropa mojada solo si puedes poner seca enseguida.",
                            "<b>Abriga</b> por capas, con gorro y guantes, y envuelve todo en una manta térmica o una bolsa de vivac (un «burrito»).",
                            "<b>Calor externo</b> en el pecho, las axilas y la espalda: bolsas de calor, botellas de agua caliente envueltas en ropa o el cuerpo de un compañero.",
                            "<b>Si está consciente y puede tragar</b>, bebidas calientes y dulces y algo de comida con azúcar.",
                            "<b>Moderada o grave:</b> manipula a la persona con mucho cuidado y en horizontal, sin frotarla ni hacerla caminar. Pide rescate."]),
                    "Qué no hacer",
                    reglas(["<b>No des alcohol</b>: da sensación de calor pero hace perder más.",
                            "<b>No frotes</b> la piel ni des masajes en las extremidades.",
                            "<b>No metas</b> a una persona con hipotermia moderada o grave en agua caliente.",
                            "<b>No la dejes sola</b> ni la hagas caminar si ya no tirita: los movimientos bruscos pueden provocar una arritmia.",
                            "Una persona con hipotermia grave que parece muerta puede no estarlo: «nadie está muerto hasta que está caliente y muerto». Si no respira, empieza la RCP y no pares hasta que llegue el rescate."])) +
                '<div style="max-width:560px;margin:0 auto">' + foto("manta-termica", "La manta térmica pesa unos 50 gramos y debería ir siempre en el botiquín: con la cara plateada hacia el cuerpo, ayuda a retener el calor.") + '</div>',
                False, "hipotermia") +
        seccion("Congelaciones", "Congelaciones: los dedos, la nariz y las orejas",
                p("La congelación es la lesión de un tejido que llega a helarse. Afecta sobre todo a los dedos de los pies y las manos, la nariz, las orejas y las mejillas. La favorecen el viento, la humedad, las botas o los crampones demasiado apretados, la deshidratación, el tabaco y la altitud.") +
                tabla(["Grado", "Cómo se ve", "Pronóstico"], [
                    ["Superficial (1.º)", "Piel blanca o grisácea, dura al tacto pero blanda debajo, hormigueo y pérdida de sensibilidad. Al calentar se pone roja e hinchada.", "Se recupera en días sin secuelas."],
                    ["2.º grado", "Al recalentar aparecen ampollas con líquido claro en las primeras 24 horas.", "Suele curar en semanas."],
                    ["3.º grado", "Ampollas con sangre, piel que luego se vuelve negra.", "Puede dejar secuelas."],
                    ["4.º grado", "Tejido duro y frío en profundidad (afecta al músculo y el hueso). No hay ampollas; luego se ennegrece.", "Riesgo de amputación."],
                ]) +
                dos("Qué hacer",
                    reglas(["<b>Superficial:</b> calienta la zona con el cuerpo (los dedos en las axilas o la tripa de un compañero, la cara con la mano enguantada). Vuelve a abrigarla y vigila.",
                            "<b>Profunda:</b> si hay riesgo de que se vuelva a congelar (todavía tienes que caminar por la nieve), <b>no la recalientes</b>: es mejor caminar con el pie congelado que congelarlo dos veces.",
                            "Cuando ya estés a salvo, recalienta en agua a 37–39 °C (que no queme al meter el codo) durante 30–60 minutos. Duele mucho: toma ibuprofeno.",
                            "Seca sin frotar, cubre con gasas secas separando los dedos y <b>ve al hospital</b>."]),
                    "Qué no hacer",
                    reglas(["<b>No frotes</b> la zona, y menos con nieve: rompe el tejido dañado.",
                            "<b>No la acerques al fuego</b>, a una estufa o al tubo de escape: al no sentir, te quemarás.",
                            "<b>No revientes las ampollas.</b>",
                            "<b>No fumes</b> ni bebas alcohol."])),
                True, "congelaciones") +
        seccion("Prevención", "Para que no pase",
                tarjetas([
                    ("#4fb3e8", "Ropa por capas y seca", "Quítate capas antes de sudar y ponte la de abrigo antes de enfriarte. Lleva siempre una capa de reserva y guantes y calcetines de repuesto. Lo explicamos en <a href=\"/teoria-de-las-capas/\">la teoría de las capas</a>."),
                    ("#e9a53b", "Come y bebe", "El cuerpo produce calor quemando comida. Pica algo cada hora y bebe caliente en invierno (un termo pesa poco)."),
                    ("#7cc47f", "Mira la previsión", "El viento multiplica el frío: con 0 °C y 50 km/h de viento, la sensación es de unos -8 °C. Lo tienes en nuestra <a href=\"/meteo/\">previsión de montaña</a>."),
                    ("#e8574a", "Botas y crampones holgados", "Los pies necesitan circulación: unos calcetines demasiado gruesos en una bota justa enfrían más."),
                ])) +
        seccion("Botiquín", "El botiquín de montaña: lo que sí llevar",
                p("Un botiquín de montaña tiene que ser ligero, impermeable y con cosas que sepas usar. Este es el que llevamos nosotros en una salida de un día, para un grupo pequeño:") +
                dos("Heridas y lesiones",
                    reglas(["Guantes de nitrilo.", "Suero fisiológico en monodosis y antiséptico (clorhexidina).", "Gasas, apósitos y tiritas de varios tamaños.", "Apósitos de hidrocoloide o parches para ampollas.", "Esparadrapo o cinta de tela y venda cohesiva o elástica.", "Tiras de aproximación (puntos de papel).", "Una férula moldeable tipo SAM.", "Tijeras pequeñas y pinzas."]),
                    "Medicación y otros",
                    reglas(["Analgésicos y antiinflamatorios (paracetamol, ibuprofeno).", "Antihistamínico (alergias, picaduras).", "Tu medicación personal, y la del grupo si alguien tiene alergias graves (autoinyector de adrenalina) o diabetes.", "Sales de rehidratación.", "Crema solar y protector labial.", "<b>Manta térmica</b> y, en invierno, una bolsa de vivac ligera.", "Bolsas de calor químicas.", "Silbato, frontal y el móvil cargado (y una batería)."])) +
                '<p style="margin-top:16px">Revisa las fechas de caducidad cada temporada. Y lo más importante: <b>formación</b>. Un curso de primeros auxilios en montaña o nuestro <a href="/actividades/curso-autorrescate/">curso de autorrescate</a> valen más que cualquier botiquín.</p>',
                False, "botiquin")
    ),
    faq=[
        ("¿Cuáles son los primeros síntomas de la hipotermia?", "Tiritona intensa, manos torpes que no aciertan con la cremallera, piel fría y pálida y algo de apatía. Si la persona deja de tiritar sin haberse calentado, la hipotermia está empeorando."),
        ("¿Se puede tener hipotermia sin que haga mucho frío?", "Sí. La mayoría de las hipotermias en montaña pasan entre 0 y 10 °C, con viento y ropa mojada por la lluvia o el sudor, en personas cansadas o lesionadas que se quedan quietas."),
        ("¿Hay que frotar una congelación?", "No. Frotar, y menos con nieve, daña todavía más el tejido. Se calienta con el calor del cuerpo o, ya a salvo, con agua a 37–39 °C."),
        ("¿Qué debe llevar un botiquín de montaña?", "Guantes, material para limpiar y cubrir heridas, parches para ampollas, venda y esparadrapo, una férula moldeable, analgésicos y antiinflamatorios, antihistamínico, tu medicación personal, manta térmica y bolsas de calor."),
        ("¿Qué número llamo para un rescate en montaña?", "El 112, en toda España. Coordina el rescate con el servicio que corresponda (Guardia Civil, bomberos o el grupo de rescate de la comunidad)."),
    ],
    fuentes=[
        ("https://www.theuiaa.org/mountain-medicine/", "UIAA: recomendaciones de la comisión médica"),
        ("https://www.wms.org/", "Wilderness Medical Society: guías de hipotermia y congelación"),
        ("https://www.cruzroja.es/", "Cruz Roja Española: primeros auxilios"),
        ("https://www.semam.org/", "SEMAM: Sociedad Española de Medicina y Auxilio en Montaña"),
    ],
    nota="Este artículo es divulgativo y no sustituye a un curso de primeros auxilios ni la atención médica.",
))

# ───────────────────────────── 5. TORMENTAS ─────────────────────────────
ARTS.append(dict(
    path="/tormentas-en-la-montana/",
    corto="Tormentas en la montaña",
    card="Cómo prever una tormenta, calcular a qué distancia está el rayo y qué hacer si te pilla en la montaña.",
    titulo="Tormentas en la montaña: cómo preverlas y qué hacer",
    meta_title="Tormenta en la montaña: qué hacer si te pilla | Ad Astra",
    meta_desc="Cómo prever una tormenta de verano, a qué distancia cae el rayo, dónde no estar y qué postura adoptar si te pilla en la montaña o en una ferrata.",
    lead="Las tormentas de verano son uno de los mayores peligros de nuestras sierras. Cómo preverlas, cómo saber a qué distancia está el rayo, dónde no hay que estar y qué hacer si te pilla en plena cresta, en una ferrata o en un barranco.",
    hero="24195f49-7868-4e49-a166-35003ba5de58/via-ferrata-salamanca.webp",
    actions='<a class="btn btn-primary" href="/meteo/">Ver la previsión de tormentas</a><a class="btn btn-ghost" href="#que-hacer">Qué hacer</a>',
    ico="tormenta", og=("Artículo", "Tormentas en la montaña", "Cómo preverlas y qué hacer si te pillan", "#c78bf0"),
    publicado="2026-11-23",
    cuerpo=(
        seccion("Antes de salir", "Cómo se forma una tormenta de verano y cómo preverla",
                p("La típica tormenta de verano en la montaña es de <b>evolución diurna</b>: el sol calienta el suelo por la mañana, el aire caliente y húmedo sube por las laderas, se forman cúmulos y, si la atmósfera es inestable, a primera hora de la tarde crecen hasta convertirse en cumulonimbos con rayos, granizo y rachas de viento. Por eso la regla de oro es <b>madrugar y estar bajando a mediodía</b>.") +
                fotos(("cumulonimbo", "Un cumulonimbo crece sobre las montañas: la típica tormenta de tarde de verano."), ("rayo-montana", "Rayo sobre una montaña: las cumbres y crestas son los puntos más expuestos.")) +
                tarjetas([
                    ("#4fb3e8", "Mira la previsión", "Busca avisos de tormenta en AEMET y la probabilidad de precipitación por la tarde. En nuestra <a href=\"/meteo/\">previsión de montaña</a> tienes el icono de tormenta por horas y los avisos oficiales en el mapa."),
                    ("#e9a53b", "Mira el cielo", "Cúmulos que a media mañana ya crecen hacia arriba como coliflores, nubes que se oscurecen por la base o una tormenta que se ve venir a lo lejos: es hora de cambiar de plan."),
                    ("#7cc47f", "Planifica la retirada", "Ten pensado dónde puedes escapar de la cresta o de la ferrata, y una hora límite para dar la vuelta. Y respétala."),
                ])) +
        seccion("La distancia", "¿A qué distancia está la tormenta?",
                p("La luz del rayo llega casi al instante y el sonido del trueno viaja a unos 340 m por segundo. <b>Cuenta los segundos entre el relámpago y el trueno y divide entre 3</b>: es la distancia en kilómetros.") +
                escala([
                    ("#4caf50", "Más de 30 s", "Más de 10 km", "La tormenta está lejos, pero puede acercarse rápido: vigila hacia dónde va."),
                    ("#f08a24", "30 s o menos", "Menos de 10 km", "<b>Ya estás en zona de riesgo.</b> Los rayos pueden caer a más de 10 km del núcleo. Busca un lugar seguro ya."),
                    ("#e8574a", "Menos de 10 s", "Menos de 3 km", "Peligro inmediato. Adopta la postura de seguridad si no has llegado a un sitio protegido."),
                ]) +
                '<p style="margin-top:16px">Es la <b>regla 30/30</b>: si entre el rayo y el trueno pasan 30 segundos o menos, protégete; y no vuelvas a la zona expuesta hasta <b>30 minutos después del último trueno</b>.</p>',
                True) +
        seccion("Qué hacer", "Si la tormenta te pilla en la montaña",
                dos("Dónde no estar",
                    reglas(["<b>Cumbres, crestas y collados</b>: eres el punto más alto.",
                            "<b>Árboles aislados</b>, postes, torres, cruces de cumbre y vértices geodésicos.",
                            "<b>Cables, escaleras y grapas</b> de una ferrata, vallas y alambradas: conducen la corriente a mucha distancia.",
                            "<b>Agua</b>: lagunas, arroyos y fondos de barranco (además, pueden crecer de golpe).",
                            "<b>Entradas de cuevas y bajo bloques</b> o viseras de roca: la corriente puede saltar por el hueco y atravesarte.",
                            "<b>En grupo apiñado</b>: un rayo puede afectar a todos."]),
                    "Qué hacer",
                    reglas(["<b>Baja</b> cuanto antes de crestas y cimas, hacia terreno más bajo y uniforme, mejor en un bosque denso de árboles de altura similar.",
                            "<b>Sepárate del grupo</b> unos 15–20 m entre personas, para que un rayo no os afecte a todos y alguien pueda ayudar.",
                            "<b>Quítate lo metálico</b> que sobresalga (piolets, bastones) y déjalo a unos metros. No hace falta quitarse la ropa ni el reloj.",
                            "<b>Si el rayo es inminente</b> (pelo de punta, zumbido en las rocas o el metal, chispazos): agáchate en cuclillas sobre la mochila o una esterilla, con <b>los pies juntos</b>, la cabeza entre las rodillas y las manos tapando los oídos. No te tumbes.",
                            "<b>En una ferrata</b>, sal del cable en cuanto puedas por el escape más cercano. Si no hay escape, aléjate del cable lo que permita tu seguridad y no te quedes en el tramo más alto.",
                            "<b>En un barranco</b>, sal por la vía de escape más próxima y espera fuera, en alto, a que pase la crecida."])),
                False, "que-hacer") +
        seccion("Si cae un rayo", "Primeros auxilios a una persona alcanzada",
                reglas(["<b>Tocarla no es peligroso:</b> el cuerpo no queda cargado. Si sigue la tormenta, llévala a un sitio más seguro.",
                        "<b>Llama al 112.</b>",
                        "Si no respira, <b>empieza la RCP</b> de inmediato. Muchas víctimas de un rayo sufren una parada respiratoria que se recupera con la reanimación. Si hay varias víctimas, atiende primero a las que parecen muertas (al revés que en otros accidentes).",
                        "Busca quemaduras de entrada y salida, fracturas por la caída y lesiones en los oídos y los ojos, y abriga para evitar la hipotermia."]),
                True) +
        seccion("Otros peligros", "Granizo, viento, frío y crecidas",
                tarjetas([
                    ("#bfe0f7", "Granizo", "Protege la cabeza (casco) y busca un sitio a cubierto sin meterte en una cueva o bajo un bloque."),
                    ("#b9a593", "Rachas de viento", "Antes de la tormenta llegan rachas muy fuertes que pueden tirarte en una cresta. Asegura la mochila y baja."),
                    ("#4fb3e8", "Bajada de temperatura", "En pocos minutos puede caer más de 10 °C, con lluvia o granizo: riesgo de <a href=\"/hipotermia-congelaciones-botiquin-montana/\">hipotermia</a>, incluso en verano."),
                    ("#e8574a", "Crecidas", "Una tormenta aguas arriba puede hacer crecer un barranco en minutos aunque donde estés no llueva. Mira el <a href=\"/barrancos-caudal/\">caudal de barrancos</a> y la previsión antes de entrar."),
                ]))
    ),
    faq=[
        ("¿Cómo saber a qué distancia está una tormenta?", "Cuenta los segundos entre el relámpago y el trueno y divide entre 3: es la distancia en kilómetros. Si son 30 segundos o menos (10 km), ya estás en zona de riesgo."),
        ("¿Qué postura hay que adoptar si va a caer un rayo?", "En cuclillas sobre la mochila o una esterilla, con los pies juntos, la cabeza baja y las manos en los oídos. No hay que tumbarse, para tocar el suelo con la menor superficie posible."),
        ("¿Es seguro refugiarse en una cueva durante una tormenta?", "Solo si es grande y profunda y te puedes alejar de la entrada y de las paredes. Las cuevas pequeñas, las grietas y las viseras de roca son peligrosas: la corriente puede saltar por el hueco."),
        ("¿Se puede hacer una vía ferrata con tormenta?", "No. El cable y las grapas conducen la corriente del rayo a mucha distancia. Si hay previsión de tormentas, empieza muy temprano o déjalo para otro día."),
        ("¿Cuánto hay que esperar después de una tormenta?", "Al menos 30 minutos después del último trueno antes de volver a las zonas expuestas."),
    ],
    fuentes=[
        ("https://www.aemet.es/es/eltiempo/prediccion/montana", "AEMET: predicción para montaña"),
        ("https://www.aemet.es/es/eltiempo/prediccion/avisos", "AEMET: avisos meteorológicos"),
        ("https://www.proteccioncivil.es/", "Protección Civil: recomendaciones ante tormentas"),
        ("https://www.weather.gov/safety/lightning", "Servicio Meteorológico de EE. UU. (NWS): seguridad ante rayos"),
    ],
))
