"""Artículos: orientación, vivac y acampada, federarse y rescates, raquetas y esquí de travesía, rutas clásicas de Gredos."""
from arts_util import seccion, tabla, tarjetas, escala, reglas, dos, p, aviso, foto, fotos, ilustracion, blog, ruta_blog, fblog

ARTS = []

# ───────────────────────────── 6. ORIENTACIÓN ─────────────────────────────
ARTS.append(dict(
    path="/orientacion-en-montana-mapa-brujula/",
    corto="Orientación: mapa, brújula y señales",
    card="Cómo leer las curvas de nivel, usar la brújula, entender las señales GR, PR y SL y no perderte aunque falle el GPS.",
    titulo="Orientación en montaña: mapa, brújula y señales de los senderos",
    meta_title="Orientación en montaña: mapa, brújula y señales | Ad Astra",
    meta_desc="Cómo leer un mapa topográfico y sus curvas de nivel, usar la brújula para seguir un rumbo, entender las señales GR, PR y SL y qué hacer si te pierdes.",
    lead="Cómo leer un mapa topográfico y sus curvas de nivel, cómo usar la brújula para seguir un rumbo en la niebla, qué significan las marcas blancas y rojas de los senderos y qué hacer si te pierdes. El GPS ayuda, pero la batería se acaba.",
    hero="/img/fotos/portada-orientacion.webp",
    actions='<a class="btn btn-primary" href="#curvas">Curvas de nivel</a><a class="btn btn-ghost" href="#brujula">Brújula</a><a class="btn btn-ghost" href="#senales">Señales</a>',
    ico="orientacion", og=("Artículo", "Orientación en montaña", "Mapa, brújula y señales GR, PR y SL", "#7cc47f"),
    publicado="2026-11-23",
    cuerpo=(
        seccion("El mapa", "El mapa topográfico: escala y leyenda",
                p("Un mapa topográfico representa el relieve. En España, los de referencia son los del <b>Instituto Geográfico Nacional</b> (IGN): el MTN25 (escala 1:25.000) y el MTN50 (1:50.000), que puedes ver gratis en el visor del IGN o descargar. Para la montaña, la escala ideal es <b>1:25.000</b>.") +
                tabla(["Escala", "1 cm en el mapa son…", "Para qué"], [
                    ["1:25.000", "250 m", "La mejor para la montaña: se ven los caminos, las fuentes y el relieve en detalle."],
                    ["1:50.000", "500 m", "Travesías largas y para tener una visión de conjunto."],
                    ["1:100.000 o más", "1 km o más", "Para planificar el acceso por carretera, no para orientarse en el monte."],
                ]) +
                foto("mtn25-laguna-grande", "Así se ve la Laguna Grande de Gredos en el mapa MTN25 del IGN: las curvas de nivel apretadas marcan las paredes del Circo.", "Mapa topográfico MTN25 del IGN de la Laguna Grande de Gredos con sus curvas de nivel") +
                '<p style="margin-top:14px">La <b>cuadrícula</b> que cruza el mapa es la cuadrícula UTM: cada cuadro mide 1 km en los mapas 1:25.000. Te sirve para calcular distancias de un vistazo y para dar tu posición en coordenadas (las mismas que te da el móvil).</p>') +
        seccion("El relieve", "Cómo leer las curvas de nivel",
                p("Una curva de nivel une todos los puntos que están a la misma altura. Entre dos curvas hay siempre el mismo desnivel, la <b>equidistancia</b>: 10 m en los mapas 1:25.000 del IGN y 20 m en los 1:50.000. Cada cinco curvas hay una más gruesa con su altitud, la <b>curva maestra</b>.") +
                ilustracion("/img/guias/curvas-de-nivel.svg", "Mapa de curvas de nivel con dos cimas, un collado, una vaguada y un espolón, y el perfil del terreno debajo", "Las curvas de nivel y el perfil del terreno que dibujan. Fíjate en la cara este de la cima principal: las curvas casi se tocan y el perfil cae en picado.") +
                tarjetas([
                    ("#e8574a", "Curvas juntas", "Pendiente fuerte. Si están muy pegadas, puede ser un cortado o una pared."),
                    ("#4caf50", "Curvas separadas", "Terreno suave: una llanura, un collado amplio, una ladera tendida."),
                    ("#4fb3e8", "Vaguada o valle", "Las curvas forman una V que apunta hacia arriba (hacia las curvas más altas). Por ahí corre el agua."),
                    ("#e9a53b", "Espolón o cresta", "Las curvas forman una V o una U que apunta hacia abajo. Es el lomo de la montaña."),
                    ("#c78bf0", "Cima", "Curvas cerradas y concéntricas que cada vez son más pequeñas y más altas."),
                    ("#b9a593", "Collado", "Un punto bajo entre dos cimas: dos grupos de curvas cerradas enfrentados, como un reloj de arena."),
                ]) +
                '<p style="margin-top:16px">Con un poco de práctica, el mapa te dice antes de salir dónde va a estar la cuesta más dura, dónde vas a encontrar agua y por dónde es más fácil escapar si cambia el tiempo. Puedes ver el perfil de tu ruta con nuestro <a href="/editor-gpx/">editor GPX</a> o la <a href="/calculadora-rutas/">calculadora de rutas</a>.</p>',
                True, "curvas") +
        seccion("La brújula", "Cómo usar la brújula",
                p("Lo más útil es una brújula de <b>base transparente</b> (de placa), con una flecha de dirección, un limbo que gira con los grados (de 0 a 360) y unas líneas paralelas dentro del limbo. Con ella puedes hacer dos cosas: orientar el mapa y seguir un rumbo.") +
                dos("Orientar el mapa",
                    reglas(["Pon la brújula sobre el mapa.", "Gira el mapa (no la brújula) hasta que las líneas verticales de la cuadrícula queden paralelas a la aguja y el norte del mapa coincida con el norte de la aguja.", "Ahora todo lo que ves en el mapa está en la misma dirección que en el terreno: ese pico de la derecha es ese de ahí."]),
                    "Seguir un rumbo (por ejemplo, en la niebla)",
                    reglas(["<b>1.</b> Pon el borde de la brújula uniendo dónde estás y adónde quieres ir, con la flecha de dirección apuntando hacia el destino.",
                            "<b>2.</b> Gira el limbo hasta que sus líneas queden paralelas a las líneas norte-sur del mapa, con la «N» del limbo hacia el norte del mapa.",
                            "<b>3.</b> Levanta la brújula, ponla horizontal delante del pecho y gira tú sobre ti mismo hasta que la aguja roja quede dentro de la flecha del limbo («el rojo en la caseta»).",
                            "<b>4.</b> La flecha de dirección te marca el rumbo. Elige una referencia en esa dirección (una roca, un árbol), camina hasta ella y repite."])) +
                '<div style="max-width:620px;margin:0 auto">' + foto("brujula-mapa", "Brújula sobre el mapa: la aguja roja apunta al norte magnético.") + '</div>' +
                reglas(["<b>Declinación magnética:</b> el norte de la brújula no es exactamente el norte del mapa. En la península ahora la diferencia es muy pequeña (de menos de 2°) y para caminar se puede ignorar; en otros países puede ser importante.",
                        "<b>Aléjate de lo metálico</b> (el móvil, el piolet, una valla) al tomar el rumbo: desvían la aguja.",
                        "<b>Cuenta pasos o mira el reloj</b> para saber cuánto has avanzado. Un adulto da unos 60–65 dobles pasos cada 100 m en llano."]),
                False, "brujula") +
        seccion("Las señales", "Las marcas de los senderos: GR, PR y SL",
                p("Los senderos homologados por las federaciones de montaña se marcan con dos franjas de pintura horizontales. La de arriba es siempre blanca y la de abajo indica el tipo de sendero:") +
                escala([
                    ("#e8574a", "Blanco y rojo", "GR · Gran Recorrido", "Más de 50 km, normalmente en varias etapas. Por ejemplo, el GR 10 cruza Gredos."),
                    ("#f5c84b", "Blanco y amarillo", "PR · Pequeño Recorrido", "Entre 10 y 50 km, una jornada o menos. Por ejemplo, el PR-AV 17 de la Plataforma a la Laguna Grande."),
                    ("#4caf50", "Blanco y verde", "SL · Sendero Local", "Menos de 10 km y con poca dificultad."),
                ]) +
                ilustracion("/img/guias/senales-senderos.svg", "Marcas de los senderos GR (blanco y rojo), PR (blanco y amarillo) y SL (blanco y verde): continuidad, cambio de dirección y dirección equivocada", "Las marcas de pintura de los senderos homologados.") +
                fotos(("pr-cambio-direccion", "Marca de cambio de dirección de un PR pintada en una roca."), ("pr-poste", "Marcas de continuidad de un PR en un poste.")) +
                tabla(["Marca", "Significado"], [
                    ["Dos franjas paralelas", "Continuidad: vas bien por el sendero."],
                    ["Las franjas en ángulo, o una franja doblada", "Cambio de dirección: el sendero gira hacia donde apunta el ángulo."],
                    ["Una cruz (aspa) con los dos colores", "Dirección equivocada: no sigas por ahí."],
                ]) +
                reglas(["También verás <b>hitos</b> (montones de piedras) en las zonas altas, donde no hay dónde pintar. Ayudan, pero no siempre llevan adonde tú quieres ir.",
                        "Los senderos marcados terminan muchas veces antes de la cumbre: más arriba, el mapa y el criterio son tuyos.",
                        "En los parques naturales y nacionales hay además señalización propia, con postes de madera."]),
                True, "senales") +
        seccion("El GPS", "GPS y móvil: la herramienta perfecta… mientras tenga batería",
                reglas(["<b>Descarga los mapas antes de salir</b> en una aplicación que funcione sin cobertura, y el track de la ruta. Prepara o corrige el tuyo con nuestro <a href=\"/editor-gpx/\">editor GPX</a>.",
                        "<b>Cuida la batería:</b> modo avión (el GPS sigue funcionando), brillo bajo y una batería externa. El frío la gasta mucho más rápido: lleva el móvil en un bolsillo interior.",
                        "<b>Lleva el mapa y la brújula igualmente</b>, y practica con ellos con buen tiempo. En la niebla no es el momento de aprender.",
                        "<b>Comparte tu plan:</b> di a alguien por dónde vas y cuándo piensas volver."])) +
        seccion("Si te pierdes", "Qué hacer si te pierdes",
                escala([
                    ("#e6c32e", "P", "Para", "Detente en cuanto dudes. Seguir «a ver si sale» es lo que convierte un despiste en un problema."),
                    ("#f08a24", "P", "Piensa", "¿Cuál fue el último punto en el que estabas seguro? ¿Cuánto tiempo hace?"),
                    ("#4fb3e8", "O", "Observa", "Busca referencias: cumbres, ríos, caminos. Orienta el mapa. Mira tu posición en el móvil."),
                    ("#4caf50", "D", "Decide", "Vuelve al último punto conocido si puedes. Si no, quédate en un sitio visible y llama al 112."),
                ]) +
                '<p style="margin-top:16px">Si te va a caer la noche, la niebla o el cansancio, es mejor quedarse quieto, abrigado y localizable que seguir bajando por un terreno que no conoces. Practica todo esto en una salida guiada de <a href="/actividades/senderismo-avila-gredos/">senderismo en Gredos</a>.</p>',
                True)
    ),
    faq=[
        ("¿Qué significan las marcas blancas y rojas de los senderos?", "Indican un sendero de Gran Recorrido (GR), de más de 50 km. Las blancas y amarillas son de Pequeño Recorrido (PR) y las blancas y verdes, de Sendero Local (SL). Una cruz con los dos colores significa que ese no es el camino."),
        ("¿Qué es la equidistancia de las curvas de nivel?", "El desnivel que hay entre dos curvas de nivel seguidas. En los mapas 1:25.000 del IGN es de 10 m y en los 1:50.000, de 20 m."),
        ("¿Cómo sé si una pendiente es fuerte en el mapa?", "Por lo juntas que están las curvas de nivel: cuanto más juntas, más empinado. Si están casi pegadas, puede ser un cortado."),
        ("¿Hace falta corregir la declinación magnética en España?", "En la península ahora la declinación es muy pequeña, de menos de 2°, y para caminar se puede ignorar. En otros países o para rumbos muy largos sí conviene corregirla."),
        ("¿Qué hago si me pierdo en la montaña?", "Para, piensa cuál fue el último punto donde estabas seguro, observa el entorno y el mapa y decide: vuelve a ese punto si puedes o quédate en un sitio visible y llama al 112."),
    ],
    fuentes=[
        ("https://www.ign.es/iberpix/visor/", "IGN: visor de mapas Iberpix"),
        ("https://centrodedescargas.cnig.es/", "CNIG: centro de descargas (MTN25, MTN50)"),
        ("https://www.fedme.es/", "FEDME: senderos homologados"),
        ("https://www.montanasegura.com/", "Montaña Segura"),
    ],
))

# ───────────────────────────── 7. VIVAC Y ACAMPADA ─────────────────────────────
ARTS.append(dict(
    path="/vivac-acampada-libre-espana/",
    corto="Vivac y acampada libre en España",
    card="Qué diferencia hay entre vivac y acampada, qué está permitido en Gredos, Guadarrama, Picos, Ordesa o Sierra Nevada.",
    titulo="Vivac y acampada libre en España: qué está permitido",
    meta_title="Vivac y acampada libre en España: qué es legal | Ad Astra",
    meta_desc="Diferencia entre vivac y acampada libre, y qué está permitido en Gredos, Guadarrama, Picos de Europa, Ordesa, Sierra Nevada y Aigüestortes.",
    lead="Dormir en la montaña es una de las mejores experiencias que hay, pero no se puede hacer en cualquier sitio ni de cualquier manera. Qué diferencia hay entre vivac y acampada, y qué dicen las normas de los espacios naturales más visitados.",
    hero="/img/fotos/vivac-noche.webp",
    actions='<a class="btn btn-primary" href="#normas">Normas por zona</a><a class="btn btn-ghost" href="/lista-material-montana/">Material para vivac</a>',
    ico="vivac", og=("Artículo", "Vivac y acampada libre", "Qué está permitido en los parques de España", "#e9a53b"),
    publicado="2026-11-23",
    cuerpo=(
        aviso("<b>Las normas cambian</b> y cada espacio natural tiene las suyas. Este artículo resume lo que dicen las fuentes oficiales en noviembre de 2026, pero antes de ir consulta siempre la web del parque o llama a su centro de visitantes.").replace('style="margin-top:20px', 'style="margin:20px auto;max-width:1100px') +
        seccion("Conceptos", "Vivac, acampada y pernocta: no es lo mismo",
                tarjetas([
                    ("#e9a53b", "Vivac", "Pasar la noche al raso, con saco y esterilla, y como mucho una funda de vivac o una tienda pequeña que se monta al anochecer y se desmonta al amanecer. Es parte de una actividad de montaña (una travesía, una ascensión), no un fin en sí mismo."),
                    ("#e8574a", "Acampada libre", "Instalar una tienda fuera de un camping y quedarse durante el día o varios días en el mismo sitio. Está prohibida en casi todos los espacios naturales protegidos de España."),
                    ("#4fb3e8", "Pernocta en refugio", "Dormir en un refugio guardado (con reserva) o en un refugio libre. En los libres no hay reserva: si está lleno, muchas normas permiten vivaquear al lado."),
                ]) +
                '<p style="margin-top:16px">Fuera de los espacios protegidos, la acampada depende de la normativa de cada comunidad autónoma y de cada ayuntamiento, y en terreno privado necesitas permiso del propietario. Y en verano, en todo el país, <b>hacer fuego en el monte suele estar prohibido</b> (también con hornillos de llama en algunas épocas y zonas de alto riesgo).</p>') +
        seccion("Por zonas", "Qué está permitido en los espacios naturales más visitados",
                tabla(["Espacio", "Qué dicen las normas"], [
                    ["Sierra de Gredos (Parque Regional, Ávila)", "Su plan de ordenación (PORN) <b>prohíbe la acampada libre</b> y la acampada fuera de los lugares señalados. El vivac no aparece regulado de forma expresa: si vas a vivaquear, hazlo de forma discreta, por la noche, lejos de las lagunas y del refugio, y consulta antes con la Casa del Parque o los agentes medioambientales."],
                    ["Sierra de Guadarrama (Parque Nacional)", "Se permite el <b>vivac sin tienda</b> solo en las zonas que fija el plan rector (no en la Laguna de los Pájaros). En la vertiente segoviana, por encima de 2.000 m y fuera del 15 de junio al 15 de octubre, en grupos de hasta 5. En Peñalara (vertiente madrileña), con autorización, máximo 15 personas y sin perros. Una sola noche en el mismo sitio. Junto a los refugios no guardados se permite si están llenos."],
                    ["Picos de Europa (Parque Nacional)", "Acampada libre prohibida. Se permite el vivac por encima de una cota mínima, montando la tienda poco antes del anochecer y recogiéndola tras el amanecer. La cota y las condiciones están en revisión con los nuevos planes rectores de 2026: consulta la web del parque."],
                    ["Ordesa y Monte Perdido (Parque Nacional)", "En el sector de Ordesa, prohibido salvo en la zona de acampada de Góriz, con reserva. En el resto de sectores se permite el vivac por encima de unas cotas mínimas que fija el parque, del atardecer al amanecer."],
                    ["Sierra Nevada (Parque Nacional y Natural)", "Acampada libre prohibida. El vivac y la acampada nocturna en altura requieren <b>comunicación previa</b> por escrito al parque, con grupos de hasta 15 personas, a más de 50 m de las lagunas y 500 m de los refugios guardados y las carreteras."],
                    ["Aigüestortes i Estany de Sant Maurici (Parque Nacional)", "Prohibido pernoctar fuera de los refugios, acampar y vivaquear en todo el parque, salvo en las zonas habilitadas."],
                ]) +
                '<p class="small muted" style="margin-top:10px">Resumen orientativo elaborado a partir de las webs de los parques y de su normativa. No sustituye a la norma vigente.</p>',
                True, "normas") +
        seccion("Buenas prácticas", "Cómo vivaquear sin dejar huella",
                reglas(["<b>Llega tarde y vete pronto.</b> Monta al anochecer y recoge al amanecer.",
                        "<b>Lejos del agua:</b> al menos 50–100 m de lagunas y arroyos, para no contaminarlos ni molestar a la fauna que va a beber.",
                        "<b>No hagas fuego.</b> Usa un hornillo, y solo si está permitido en esa época.",
                        "<b>No construyas</b> muretes de piedras, zanjas alrededor de la tienda ni camas de ramas.",
                        "<b>Llévate toda tu basura</b>, también la orgánica (pieles de fruta, restos de comida).",
                        "<b>Necesidades:</b> lejos del agua y de los caminos, enterradas a 15–20 cm, y el papel de vuelta en una bolsa.",
                        "<b>Grupos pequeños</b> y en silencio: la noche es de la fauna.",
                        "<b>Mira la previsión.</b> Una tormenta o una helada en vivac sin refugio son serias: lo explicamos en <a href=\"/tormentas-en-la-montana/\">tormentas</a> e <a href=\"/hipotermia-congelaciones-botiquin-montana/\">hipotermia</a>."]) +
                '<p style="margin-top:16px">Para no olvidar nada, tienes la lista de vivac en nuestra <a href="/lista-material-montana/">lista de material</a>. Y si quieres vivir la experiencia con guía, mira nuestras <a href="/actividades/trekking-ultra-de-gredos/">travesías por Gredos</a>.</p>')
    ),
    faq=[
        ("¿Es legal la acampada libre en España?", "No hay una ley única: depende de cada comunidad autónoma, ayuntamiento y espacio protegido. En casi todos los parques nacionales y naturales la acampada libre está prohibida, y en algunos se permite el vivac con condiciones."),
        ("¿Qué diferencia hay entre vivac y acampada libre?", "El vivac es pasar la noche al raso o con una tienda ligera que se monta al anochecer y se recoge al amanecer, como parte de una actividad de montaña. La acampada es instalarse con tienda y permanecer durante el día o varios días."),
        ("¿Se puede vivaquear en Gredos?", "El plan de ordenación del Parque Regional de la Sierra de Gredos prohíbe la acampada libre y no regula expresamente el vivac. Si vas a vivaquear, hazlo de forma discreta y consulta antes con la Casa del Parque o los agentes medioambientales."),
        ("¿Dónde se puede vivaquear en Guadarrama?", "Sin tienda y solo en las zonas que fija el plan rector del parque nacional. En la vertiente segoviana, por encima de 2.000 m y fuera del periodo del 15 de junio al 15 de octubre, en grupos de hasta 5 personas. En Peñalara hace falta autorización."),
        ("¿Se puede hacer fuego al vivaquear?", "En general no: hacer fuego en el monte está prohibido en casi todos los espacios naturales y, en verano, en todo el territorio con riesgo de incendio. Usa un hornillo y solo si está permitido en esa época y lugar."),
    ],
    fuentes=[
        ("https://www.parquenacionalsierraguadarrama.es/", "Parque Nacional de la Sierra de Guadarrama"),
        ("https://www.miteco.gob.es/es/parques-nacionales-oapn/red-parques-nacionales/parques-nacionales/picos-europa.html", "MITECO: Parque Nacional de los Picos de Europa"),
        ("https://www.ordesa.net/", "Parque Nacional de Ordesa y Monte Perdido"),
        ("https://www.juntadeandalucia.es/medioambiente/portal/areas-tematicas/espacios-protegidos", "Junta de Andalucía: espacios protegidos (Sierra Nevada)"),
        ("https://parcsnaturals.gencat.cat/es/aiguestortes", "Parcs Naturals de Catalunya: Aigüestortes"),
        ("https://patrimonionatural.org/espacios-naturales/parque-regional/parque-regional-sierra-de-gredos", "Patrimonio Natural de Castilla y León: Sierra de Gredos"),
    ],
))

# ───────────────────────────── 8. FEDERARSE Y RESCATES ─────────────────────────────
ARTS.append(dict(
    path="/federarse-seguro-montana-rescate/",
    corto="Federarse, seguros y rescates",
    card="Qué cubre la licencia federativa de montaña, qué modalidad elegir y quién paga un rescate en España.",
    titulo="Federarse en montaña: qué cubre la licencia y quién paga un rescate",
    meta_title="Licencia de montaña y rescates: quién paga | Ad Astra",
    meta_desc="Qué cubre la licencia federativa de montaña, qué modalidad elegir según adónde vayas y en qué comunidades te pueden cobrar un rescate.",
    lead="Qué cubre la licencia de la federación de montaña, qué modalidad necesitas según adónde vayas, en qué comunidades te pueden cobrar un rescate y cómo pedir ayuda bien. Un trámite de diez minutos que puede ahorrarte mucho dinero y disgustos.",
    hero="/img/fotos/rescate-helicoptero.webp",
    actions='<a class="btn btn-primary" href="#modalidades">Modalidades</a><a class="btn btn-ghost" href="#quien-paga">¿Quién paga el rescate?</a>',
    ico="seguro", og=("Artículo", "Federarse y rescates", "Qué cubre la licencia y quién paga un rescate", "#4fb3e8"),
    publicado="2026-11-23",
    cuerpo=(
        seccion("La licencia", "Qué es la licencia federativa y qué cubre",
                p("La licencia federativa te hace miembro de la federación de montaña de tu comunidad (en Castilla y León, la <b>FDMESCYL</b>) y, según la modalidad, también de la española (<b>FEDME</b>). Lo más importante que incluye es un <b>seguro de accidentes deportivos</b> pensado para la montaña. Se saca normalmente a través de un club y vale para el año natural (de enero a diciembre).") +
                tarjetas([
                    ("#4fb3e8", "Gastos de rescate", "Búsqueda, rescate y evacuación hasta el centro médico, con un límite por siniestro (más alto en el extranjero)."),
                    ("#7cc47f", "Asistencia médica", "En los centros concertados por la aseguradora, sin límite de gasto en España en muchas pólizas."),
                    ("#e9a53b", "Indemnizaciones", "Por fallecimiento o por lesiones permanentes, según un baremo."),
                    ("#c78bf0", "Otras ventajas", "Descuentos en refugios y tiendas, acceso a cursos, a competiciones y a los seguros de las federaciones de otros países en sus refugios."),
                ]) +
                '<p style="margin-top:16px">Por ejemplo, la póliza de la FDMESCYL de 2024 cubría <b>12.000 € de gastos de rescate en España y 24.000 € en el extranjero</b>, con asistencia sanitaria ilimitada en los centros concertados. Las cifras cambian cada año: mira las de la temporada en curso.</p>') +
        seccion("Modalidades", "Qué modalidad elegir",
                p("Las modalidades se diferencian por el <b>ámbito geográfico</b> y por las <b>actividades</b> que cubren. Estas son las de la FDMESCYL (las de otras federaciones son parecidas, aunque cambian los nombres):") +
                tabla(["Modalidad", "Dónde", "Qué actividades"], [
                    ["AU", "Solo Castilla y León", "Todas las de montaña."],
                    ["A", "España, Andorra, Pirineo francés, Portugal y Marruecos", "Senderismo y marcha nórdica sin alta montaña: no cubre el uso de cuerda, crampones ni raquetas."],
                    ["B", "El mismo que la A", "Todas las de montaña: alpinismo, escalada, barrancos, esquí de montaña, ferratas, raquetas…"],
                    ["C", "España, Europa y Marruecos", "Como la B."],
                    ["D", "Todo el mundo, salvo expediciones polares y montañas de más de 7.000 m", "Como la B."],
                    ["E", "Todo el mundo", "Como la B, incluidas las expediciones. Con requisitos de antigüedad."],
                ]) +
                reglas(["Si haces <b>algo más que senderismo</b> (nieve con crampones, escalada, barrancos), necesitas como mínimo la B, aunque no salgas de España.",
                        "Hay <b>licencias de medio año</b> (de julio a diciembre) y suplementos para esquí alpino o BTT.",
                        "Si viajas a los Alpes, a Marruecos o más lejos, revisa que la modalidad cubra ese país."]),
                True, "modalidades") +
        seccion("El rescate", "¿Quién paga un rescate en España?",
                p("En España, los rescates los hacen servicios públicos: la Guardia Civil (GREIM), los bomberos o los grupos de rescate de cada comunidad (en Castilla y León, el Grupo de Rescate de la Junta, con helicóptero). <b>En general son gratuitos</b>, pero varias comunidades tienen leyes o tasas que permiten cobrarlos en casos concretos: cuando hay imprudencia o negligencia (ignorar los avisos, ir sin el material necesario, meterse en una zona prohibida) o en falsas alarmas.") +
                '<div style="max-width:640px;margin:0 auto">' + foto("greim-rescate", "Rescate en helicóptero de la Guardia Civil (GREIM).") + '</div>' +
                tabla(["Comunidad", "Cuándo se puede cobrar"], [
                    ["Cataluña", "Rescates en zonas peligrosas o prohibidas, sin el material necesario o por falsa alarma."],
                    ["Asturias", "Solo en casos claros: desobedecer una orden expresa o negligencia evidente."],
                    ["Cantabria", "Tasa de 2021 para rescates en circunstancias especiales, según el coste."],
                    ["País Vasco", "Ley de 2011, aplicada en muy pocos casos."],
                    ["Castilla y León, Navarra y Canarias", "También contemplan el cobro en determinados supuestos."],
                ]) +
                '<p style="margin-top:14px">En la práctica, el cobro se aplica en pocos casos. Pero un rescate cuesta de media varios miles de euros y un helicóptero, unos 2.000 € por hora: <b>estar federado o tener un seguro que cubra el rescate</b> te evita disgustos. Y en el extranjero (Alpes, Marruecos) el rescate casi siempre se paga.</p>',
                False, "quien-paga") +
        seccion("Pedir ayuda", "Cómo pedir un rescate bien",
                escala([
                    ("#e8574a", "1", "Llama al 112", "En toda España y en la Unión Europea. Si no hay cobertura de tu compañía, intenta igualmente: entra por otra red."),
                    ("#f08a24", "2", "Di dónde estás", "Las coordenadas del móvil (en la app del mapa o en la de 112 de tu comunidad), el nombre del lugar y qué ves alrededor."),
                    ("#e6c32e", "3", "Explica qué pasa", "Qué ha ocurrido, cuántas personas sois, cómo están los heridos y qué tiempo hace."),
                    ("#4caf50", "4", "Guarda batería", "Quédate localizable, no cambies de sitio si no te lo dicen y ahorra batería para que te puedan llamar."),
                ]) +
                reglas(["Para un helicóptero: los brazos en <b>Y</b> («Yes») significan que necesitas ayuda; un brazo arriba y otro abajo, que no.",
                        "Recoge la ropa y todo lo que pueda volar con el rotor y no te acerques al helicóptero hasta que te lo indique la tripulación.",
                        "La mejor forma de no necesitar un rescate es la formación: mira nuestro <a href=\"/actividades/curso-autorrescate/\">curso de autorrescate</a> y el <a href=\"/actividades/curso-arva/\">curso de ARVA y aludes</a>."]),
                True)
    ),
    faq=[
        ("¿Qué cubre la licencia federativa de montaña?", "Un seguro de accidentes deportivos que incluye los gastos de búsqueda, rescate y evacuación, la asistencia médica en centros concertados y las indemnizaciones por lesiones permanentes o fallecimiento, según la modalidad y la póliza de cada año."),
        ("¿Qué licencia necesito para hacer alpinismo o barrancos en España?", "Una modalidad que cubra todas las actividades de montaña, como la B de la FDMESCYL o su equivalente en otras federaciones. La modalidad A solo cubre senderismo sin cuerda, crampones ni raquetas."),
        ("¿Me pueden cobrar un rescate en la montaña?", "En general los rescates son gratuitos, pero varias comunidades (Cataluña, Asturias, Cantabria, País Vasco, Castilla y León, Navarra, Canarias) pueden cobrarlos en casos de imprudencia, falta de material o falsa alarma. Estar federado o tener un seguro de rescate te protege."),
        ("¿Cuánto cuesta un rescate en helicóptero?", "Depende del caso, pero se estima que un rescate cuesta de media entre 5.000 y 8.000 € y que una hora de helicóptero ronda los 2.000 €."),
        ("¿Qué número se llama para un rescate en montaña?", "El 112, en toda España. Coordina al servicio de rescate que corresponda."),
    ],
    fuentes=[
        ("https://www.fdmescyl.com/", "FDMESCYL: Federación de Deportes de Montaña, Escalada y Senderismo de Castilla y León"),
        ("https://deportes.usal.es/wp-content/uploads/2023/12/Reglamento_Licencias_FDMESCYL_2024.pdf", "Reglamento de licencias FDMESCYL 2024 (PDF)"),
        ("https://www.fedme.es/", "FEDME"),
        ("https://theobjective.com/espana/2024-06-26/asturias-cataluna-regiones-obligan-pagar-rescate-montana/", "The Objective: las regiones que te obligan a pagar un rescate (2024)"),
    ],
    nota="No somos un corredor de seguros: este artículo es informativo. Las coberturas exactas son las de la póliza de cada federación y temporada.",
))

# ───────────────────────────── 9. RAQUETAS Y ESQUÍ DE TRAVESÍA ─────────────────────────────
ARTS.append(dict(
    path="/raquetas-de-nieve-y-esqui-de-travesia/",
    corto="Raquetas de nieve y esquí de travesía",
    card="Cómo elegir raquetas, qué material necesitas para el esquí de travesía y cómo moverte seguro por la nieve.",
    titulo="Raquetas de nieve y esquí de travesía: material y primeros pasos",
    meta_title="Raquetas de nieve y esquí de travesía: guía | Ad Astra",
    meta_desc="Cómo elegir raquetas de nieve, qué material necesitas para empezar en el esquí de travesía (esquís, fijaciones, pieles, botas) y cómo ir seguro.",
    lead="Las dos formas más bonitas de recorrer la montaña nevada. Cómo elegir unas raquetas, qué material hace falta para el esquí de travesía (o de montaña), cuál te conviene según tu nivel y qué precauciones hay que tomar.",
    hero="/img/fotos/portada-raquetas.webp",
    actions='<a class="btn btn-primary" href="#raquetas">Raquetas</a><a class="btn btn-ghost" href="#esqui">Esquí de travesía</a><a class="btn btn-ghost" href="#seguridad">Seguridad</a>',
    ico="raquetas", og=("Artículo", "Raquetas y esquí de travesía", "Material y primeros pasos en la nieve", "#bfe0f7"),
    publicado="2026-11-23",
    cuerpo=(
        seccion("Cuál elegir", "Raquetas o esquís: ¿qué me conviene?",
                tabla(["", "Raquetas de nieve", "Esquí de travesía"], [
                    ["Aprendizaje", "Inmediato: si sabes caminar, sabes andar con raquetas.", "Hace falta saber esquiar bien en pista, y fuera de pista es otra cosa."],
                    ["Subida", "Cómoda en nieve blanda; incómoda en pendientes fuertes o nieve dura.", "Muy eficiente gracias a las pieles. Se sube «deslizando»."],
                    ["Bajada", "Igual de lenta que la subida.", "Rápida y muy divertida… si la nieve y tu técnica acompañan."],
                    ["Material", "Barato (raquetas y bastones).", "Caro (esquís, fijaciones, botas, pieles)."],
                    ["Ideal para", "Excursiones por bosques y laderas suaves, iniciarse en la montaña invernal.", "Recorridos largos y cumbres con mucho desnivel."],
                ])) +
        seccion("Raquetas", "Cómo elegir unas raquetas de nieve",
                foto("raquetas-grupo", "Excursión con raquetas por un bosque nevado: la forma más fácil de empezar en la montaña invernal.") +
                reglas(["<b>Tamaño según el peso</b> (con mochila incluida): unas raquetas pequeñas (de unos 20 × 55 cm) sirven hasta unos 80–90 kg en nieve normal; con más peso o con nieve muy polvo, mejor más grandes o con extensiones de cola.",
                        "<b>Crampón o cuchillas:</b> las raquetas de montaña llevan un crampón bajo la fijación y cuchillas laterales que agarran en las travesías y en la nieve dura. Las de paseo con el marco tubular agarran peor en ladera.",
                        "<b>Alza talones:</b> una pieza que levanta el talón en las subidas. Ahorra mucho esfuerzo en las cuestas.",
                        "<b>Fijación:</b> que se ajuste rápido con guantes y sujete bien una bota de montaña.",
                        "<b>Bastones</b> con <b>roseta de nieve</b> (la arandela grande): sin ella se hunden hasta la empuñadura."]) +
                dos("Técnica básica",
                    reglas(["Camina con los pies un poco más separados de lo normal, para no pisarte las raquetas.",
                            "En las subidas, clava la punta y usa el alza talones. En pendientes fuertes, sube en zigzag.",
                            "En las bajadas, deja caer el peso un poco atrás y apoya primero el talón.",
                            "En las travesías de ladera, clava el canto de la raqueta del lado de la pendiente."]),
                    "Cuándo no son suficientes",
                    reglas(["En nieve dura o helada, en pendientes de más de unos 25–30° y en crestas, las raquetas resbalan: hay que cambiarlas por <a href=\"/crampones-piolet-botas-material-invernal/\">crampones y piolet</a>.",
                            "Llévalos en la mochila si la ruta tiene tramos empinados o puede helar por la tarde."])),
                True, "raquetas") +
        seccion("Esquí de travesía", "El material del esquí de travesía (o de montaña)",
                tarjetas([
                    ("#4fb3e8", "Esquís", "Más ligeros que los de pista, con un patín de unos 80–100 mm para todo uso. Más anchos flotan mejor en nieve polvo; más estrechos son más ligeros para subir."),
                    ("#e9a53b", "Fijaciones", "Liberan el talón para subir y lo bloquean para bajar. Las <b>de pines (tech)</b> son las más ligeras y las más usadas; las de raíl o híbridas son más pesadas y parecidas a las de pista."),
                    ("#7cc47f", "Botas", "Con modo de marcha (la caña se desbloquea para caminar) y las inserciones metálicas para las fijaciones de pines. Más ligeras y con más movilidad que las de pista."),
                    ("#c78bf0", "Pieles de foca", "Tiras de tejido que se pegan bajo el esquí: deslizan hacia delante y frenan hacia atrás. Hoy son sintéticas o de mohair (desliza mejor) y se cortan a la medida del esquí."),
                    ("#e8574a", "Cuchillas (harscheisen)", "Se ponen en la fijación para subir por nieve dura o helada en las travesías. Imprescindibles en primavera."),
                    ("#b9a593", "Bastones, casco y ARVA", "Bastones con roseta ancha (mejor telescópicos) y, siempre que haya nieve en pendiente, el equipo de seguridad: ARVA, pala y sonda."),
                ]) +
                reglas(["<b>La técnica de subida:</b> deslizar el esquí sin levantarlo, pasos cortos y regulares, y en las pendientes fuertes, zigzag con <b>vueltas maría</b> (cambios de dirección girando un esquí y luego el otro).",
                        "<b>Empieza alquilando</b> o con un curso: el material es caro y conviene saber qué te gusta antes de comprar.",
                        "En España, las zonas clásicas son el Pirineo, Picos de Europa, Sierra Nevada y, cuando hay nieve, Gredos (el Circo y la Sierra del Barco) y Guadarrama (Peñalara)."]),
                False, "esqui") +
        seccion("Seguridad", "En la nieve, lo primero es el riesgo de aludes",
                p("Con raquetas o con esquís vas a moverte por laderas nevadas, y ahí <b>el peligro de aludes es el mismo</b> que para un alpinista. Antes de salir:") +
                reglas(["Lee el <b>boletín de peligro de aludes</b> de AEMET y nuestro <a href=\"/nieve/\">estado de la nieve</a> por macizo. Te explicamos cómo en <a href=\"/como-leer-la-nieve-y-los-aludes/\">cómo leer la nieve y el peligro de aludes</a>.",
                        "Si tu ruta cruza o pasa bajo laderas de más de 30°, cada persona del grupo debe llevar <b>ARVA, pala y sonda</b> y saber usarlos. Practícalo en nuestro <a href=\"/actividades/curso-arva/\">curso de ARVA y aludes</a>.",
                        "Mira la <a href=\"/meteo/\">previsión de montaña</a>: el viento fuerte forma placas, y el calor de la tarde en primavera desestabiliza la nieve.",
                        "Empieza pronto: en primavera la nieve dura de la mañana se vuelve blanda y peligrosa a mediodía.",
                        "Abrígate bien (<a href=\"/teoria-de-las-capas/\">capas</a>) y protégete del sol: sobre la nieve el UV casi se duplica (<a href=\"/rayos-uv-proteccion-solar-montana/\">gafas de categoría 4 y crema</a>)."]),
                True, "seguridad")
    ),
    faq=[
        ("¿Qué raquetas de nieve comprar para empezar?", "Unas raquetas de montaña de tamaño medio con crampón bajo la fijación, cuchillas laterales y alza talones, y unos bastones con roseta de nieve. Para pesos de más de 80–90 kg con mochila, mejor un tamaño más grande o con extensiones."),
        ("¿Hace falta saber esquiar para el esquí de travesía?", "Sí: conviene esquiar con soltura en pistas rojas y algo fuera de pista. Subir con pieles se aprende rápido; bajar por nieve sin pisar es lo difícil."),
        ("¿Qué son las pieles de foca?", "Tiras de tejido sintético o mohair que se pegan bajo el esquí para subir. Deslizan hacia delante y agarran hacia atrás, así que no te escurres en la cuesta."),
        ("¿Hace falta ARVA para ir con raquetas?", "Si la ruta cruza o pasa por debajo de laderas de más de 30° con nieve, sí: ARVA, pala y sonda para cada persona y saber usarlos. En un bosque llano o en caminos sin pendiente alrededor no es necesario."),
        ("¿Dónde hacer raquetas cerca de Madrid?", "En la Sierra de Guadarrama (Cotos, Peñalara, Navacerrada) y en Gredos (la Plataforma y la Sierra de Villafranca), siempre que haya suficiente nieve y mirando antes el riesgo de aludes."),
    ],
    fuentes=[
        ("https://www.aemet.es/es/eltiempo/prediccion/montana/boletin_peligro_aludes", "AEMET: boletín de peligro de aludes"),
        ("https://www.fedme.es/", "FEDME: esquí de montaña y raquetas"),
        ("https://www.avalanches.org/", "EAWS: Servicios Europeos de Avisos de Aludes"),
    ],
))

# ───────────────────────────── 10. RUTAS CLÁSICAS DE GREDOS ─────────────────────────────
ARTS.append(dict(
    path="/rutas-clasicas-gredos-almanzor-laguna-grande-galayos/",
    corto="Rutas clásicas de Gredos",
    card="Laguna Grande, Almanzor, La Mira y Los Galayos: distancias, desnivel, dificultad y cuándo ir.",
    titulo="Rutas clásicas de Gredos: Laguna Grande, Almanzor, La Mira y Los Galayos",
    meta_title="Rutas clásicas de Gredos: Almanzor y Laguna Grande | Ad Astra",
    meta_desc="Las rutas más clásicas de la Sierra de Gredos: Laguna Grande, Almanzor, La Mira y Los Galayos. Distancia, desnivel, dificultad y cuándo ir.",
    lead="Cuatro rutas que todo montañero debería hacer alguna vez en Gredos, contadas por quienes las recorremos cada semana: la Laguna Grande, el Almanzor (techo del Sistema Central), La Mira y Los Galayos. Y tres de nuestra zona: las Cuatro Lagunas, La Ceja por Hoya Moros y la Laguna del Duque. Datos, dificultad, fotos y crónicas.",
    hero="/img/fotos/portada-gredos.webp",
    actions='<a class="btn btn-primary" href="/meteo/gredos-macizo-central/">Tiempo en Gredos</a><a class="btn btn-ghost" href="/actividades/ascensiones-sierra-de-gredos/">Subir con guía</a>',
    ico="gredos", og=("Artículo", "Rutas clásicas de Gredos", "Laguna Grande, Almanzor, La Mira y Los Galayos", "#7cc47f"),
    publicado="2026-11-23",
    cuerpo=(
        seccion("De un vistazo", "Las cuatro rutas, comparadas",
                tabla(["Ruta", "Salida", "Distancia", "Desnivel", "Dificultad"], [
                    ["Laguna Grande", "Plataforma de Gredos (1.760 m)", "≈ 13 km ida y vuelta", "≈ +650 m", "Media. Camino bueno y marcado."],
                    ["Almanzor (2.591 m)", "Plataforma de Gredos", "≈ 18 km ida y vuelta", "≈ +1.300 m", "Alta. Canal de piedra suelta y trepada final de II."],
                    ["La Mira (2.343 m)", "Plataforma de Gredos", "≈ 16–18 km", "≈ +800–1.000 m", "Media-alta. Larga, por cordal, sin pasos técnicos en verano."],
                    ["Los Galayos (refugio Victory, 1.900 m)", "Nogal del Barranco, Guisando", "≈ 6,5 km (solo ida)", "≈ +870 m", "Media-alta. Subida fuerte y continua."],
                ]) +
                foto("circo-gredos", "El Circo de Gredos con la Laguna Grande, desde Los Barrerones.") +
                '<p class="small muted" style="margin-top:10px">Datos orientativos sin nieve. Calcula el tiempo con tu ritmo en nuestra <a href="/calculadora-rutas/">calculadora de rutas</a>.</p>') +
        seccion("Ruta 1", "La Laguna Grande de Gredos",
                p("La ruta más famosa de Gredos y una de las más bonitas del Sistema Central. Sale de la <b>Plataforma</b> (al final de la carretera de Hoyos del Espino, con aparcamiento de pago) y sigue el <b>PR-AV 17</b>, un camino empedrado que sube por el Prado de las Pozas hasta el mirador de <b>Los Barrerones</b> (2.170 m). Desde ahí aparece de golpe el Circo de Gredos con el Almanzor al fondo, y se baja a la <b>Laguna Grande</b> (1.935 m), con el refugio Elola en su orilla.") +
                ruta_blog("https://jairogredos.blogspot.com/2008/05/laguna-grande.html", "ruta-laguna-grande", "El Circo de Gredos nevado desde Los Barrerones.", "ruta-laguna-grande-2", "Bajando hacia la Laguna Grande en invierno.") +
                reglas(["<b>Cuándo:</b> de mayo a noviembre sin nieve. En invierno el camino se cubre y se hiela, sobre todo en Los Barrerones: crampones y piolet, o raquetas con nieve blanda.",
                        "<b>Ojo con:</b> el viento en Los Barrerones y la vuelta, que tiene una subida de unos 250 m desde la laguna cuando ya estás cansado.",
                        "<b>Agua:</b> hay fuentes en el camino, pero no se garantiza que sea potable. Lleva la tuya.",
                        "<b>Fauna:</b> verás cabras montesas casi seguro. No les des de comer.",
                        "Mira la <a href=\"/meteo/gredos-macizo-central/\">previsión del Macizo Central</a> y la webcam de la Laguna Grande antes de ir."])) +
        seccion("Ruta 2", "El Almanzor, techo del Sistema Central",
                p("Con 2.591 m, el pico Almanzor es la cumbre más alta del Sistema Central. La vía normal sigue el camino de la Laguna Grande y continúa por la <b>Hoya de Antón</b> hasta la <b>canal de la Portilla del Crampón</b>, una canal estrecha y empinada de piedra suelta (de 40–50° en los tramos más fuertes). Desde la Portilla del Crampón (2.538 m) se hace una travesía sobre las Canales Oscuras y una <b>trepada final de grado II</b> hasta el vértice.") +
                ruta_blog("https://jairogredos.blogspot.com/2009/04/almanzor-por-la-canal-este.html", "ruta-almanzor", "El Almanzor en invierno, con el itinerario de subida marcado.", "ruta-almanzor-2", "Cerca de la cumbre del Almanzor en verano.") +
                reglas(["<b>No es una excursión:</b> la canal tiene piedras sueltas (casco) y la trepada final es expuesta. No es para personas con vértigo o sin experiencia de trepar.",
                        "<b>En invierno</b> es una ascensión de alpinismo (PD): nieve de hasta 50°, a menudo dura, y riesgo de aludes en la canal. Crampones, piolet, casco y saber autodetenerse; en algunas condiciones, cuerda. Lo explicamos en <a href=\"/crampones-piolet-botas-material-invernal/\">material invernal</a> y <a href=\"/escalas-dificultad-escalada-ferratas-alpinismo-barrancos/\">escalas de dificultad</a>.",
                        "<b>La bajada</b> por la canal es más delicada que la subida: muchos accidentes pasan ahí.",
                        "Puedes dormir en el refugio Elola (con reserva) y subir de madrugada, con más tiempo y menos gente.",
                        "Si quieres subirlo con seguridad, lo hacemos con guía en verano y en invierno: <a href=\"/actividades/ascensiones-sierra-de-gredos/\">ascensiones en Gredos</a>."])) +
        seccion("Ruta 3", "La Mira, el mejor mirador del Circo",
                p("La Mira (2.343 m) está al este del Circo de Gredos y tiene una de las mejores vistas de la sierra: el Circo, Los Galayos y el valle del Tiétar a tus pies. Desde la Plataforma se sube por la <b>Vereda de la Mira</b> hasta el cordal cimero (unos 2.070 m) y se sigue por la cuerda, pasando por Los Campanarios y la Portilla Pelucas, hasta la cumbre. Cerca de la cima están las ruinas del refugio de Los Pelaos.") +
                ruta_blog("https://jairogredos.blogspot.com/2008/04/la-mira.html", "ruta-la-mira", "Por la cuerda hacia La Mira, sobre un mar de nubes.", "ruta-la-mira-2", "Agujas de granito desde la cuerda de La Mira.") +
                reglas(["<b>Variante circular:</b> se puede bajar por El Raso y el Puerto del Peón hasta la carretera de la Plataforma (hace falta un segundo coche o caminar por la carretera).",
                        "<b>Cuándo:</b> sin nieve es una ruta larga de cordal sin pasos técnicos. En invierno, la cuerda se hiela y el viento es fuerte: crampones y piolet.",
                        "<b>Orientación:</b> en la cuerda el camino a veces se pierde entre bloques. Con niebla, mapa y brújula (<a href=\"/orientacion-en-montana-mapa-brujula/\">cómo usarlos</a>)."]),
                True) +
        seccion("Ruta 4", "Los Galayos desde Guisando",
                p("Los Galayos son las agujas de granito de la cara sur de Gredos, uno de los lugares de escalada clásica más importantes de España. La ruta sale del aparcamiento de <b>El Nogal del Barranco</b>, encima de Guisando, y sube por el camino de la garganta hasta el <b>refugio Victory</b>, al pie de las agujas (el Gran Galayo, la Galana, el Torreón…). Según la Junta, son unos <b>6,5 km con 870 m de subida y unas 3 horas</b>, de dificultad media-alta.") +
                ruta_blog("https://jairogredos.blogspot.com/2009/10/pequeno-galayo.html", "ruta-galayos", "Una de las agujas de Los Galayos.", "ruta-galayos-2", "Al pie de las agujas, tras escalar el Pequeño Galayo.") +
                reglas(["<b>La subida es dura y continua</b>, por la cara sur: en verano hace mucho calor. Sal temprano y lleva bastante agua.",
                        "<b>El refugio Victory</b> es un refugio de escaladores; consulta si está abierto antes de contar con él.",
                        "<b>Prolongación:</b> los más montañeros siguen hasta la Portilla de los Galayos y bajan al Circo o enlazan con La Mira.",
                        "<b>Escalada:</b> las vías de Los Galayos son clásicas de verdad: graduación dura y seguros que hay que poner. Mira cómo leer los grados en <a href=\"/escalas-dificultad-escalada-ferratas-alpinismo-barrancos/\">escalas de dificultad</a>."])) +
        seccion("Gredos occidental", "Nuestras rutas: Cuatro Lagunas, La Ceja–Hoya Moros y Laguna del Duque",
                p("Además de las rutas del Circo, en la parte occidental de Gredos y en la Sierra de Béjar y Candelario hay tres recorridos que son los más característicos de nuestra zona y que hacemos a menudo con grupos. Las actividades guiadas están en la <a href=\"/actividades/comarca-natural-oeste-de-gredos/\">comarca del Oeste de Gredos</a>."), True) +
        seccion("Ruta 5", "La ruta de las Cuatro Lagunas",
                p("En la Sierra del Barco: un recorrido por varias lagunas glaciares al pie de La Covacha (2.399 m), una de las cumbres más altas de Gredos occidental. En invierno las lagunas se hielan y la ruta se convierte en una salida de montaña invernal.") +
                ruta_blog("https://jairogredos.blogspot.com/2008/04/ruta-de-las-cuatro-lagunas-y-la-covacha.html", "ruta-cuatro-lagunas", "Una de las lagunas de la ruta, a medio deshelar.", "ruta-cuatro-lagunas-2", "Laguna helada bajo la cuerda nevada.")) +
        seccion("Ruta 6", "El Canchal de la Ceja por Hoya Moros",
                p("Desde Candelario por el circo glaciar de Hoya Moros hasta el Canchal de la Ceja (2.428 m), techo de Salamanca, con el Calvitero, techo de Extremadura, al lado. En invierno las canales de Hoya Moros son una escuela clásica de corredores de nieve.") +
                ruta_blog("https://jairogredos.blogspot.com/2008/02/circo-de-hoya-moros.html", "ruta-hoya-moros", "El fondo del circo de Hoya Moros.", "ruta-hoya-moros-2", "Subiendo por la nieve hacia La Ceja.")) +
        seccion("Ruta 7", "La Laguna del Duque",
                p("Desde Solana de Ávila, por un paredón de roca que parece inaccesible y que se sube cómodamente hasta la laguna. Una ruta asequible para todos los niveles, que se puede alargar hacia la Laguna de las Cocinillas o el Risco de la Campana.") +
                ruta_blog("https://jairogredos.blogspot.com/2011/12/laguna-del-duque-arroyo-malillo-laguna.html", "ruta-laguna-duque", "La Laguna del Duque.", "ruta-laguna-duque-2", "Lagunilla en la subida por el Arroyo Malillo."), True) +
        seccion("Antes de ir", "Consejos para cualquier ruta en Gredos",
                tarjetas([
                    ("#4fb3e8", "El tiempo cambia rápido", "Niebla, tormentas de verano por la tarde y viento muy fuerte en las cumbres. Mira la <a href=\"/meteo/gredos-macizo-central/\">previsión de cumbre y base</a> y las webcams."),
                    ("#e9a53b", "Madruga", "Para evitar las tormentas, el calor y el aparcamiento lleno. En verano, a mediodía tienes que estar bajando."),
                    ("#7cc47f", "Respeta el parque", "Estás en el Parque Regional de la Sierra de Gredos: no se permite la acampada libre (<a href=\"/vivac-acampada-libre-espana/\">vivac y acampada</a>) ni hacer fuego."),
                    ("#e8574a", "Federado o asegurado", "Un rescate en el Circo es complicado. Lo explicamos en <a href=\"/federarse-seguro-montana-rescate/\">federarse y rescates</a>."),
                ]))
    ),
    faq=[
        ("¿Cuánto se tarda en subir a la Laguna Grande de Gredos?", "Desde la Plataforma, unas 2–2,5 horas de ida y algo menos de vuelta, a un ritmo tranquilo. Son unos 6,5 km por trayecto y unos 650 m de desnivel acumulado entre la ida y la vuelta."),
        ("¿Es difícil subir al Almanzor?", "Sí, es una ruta de dificultad alta: unos 18 km y 1.300 m de desnivel, una canal empinada de piedra suelta y una trepada final de grado II expuesta. En invierno es una ascensión de alpinismo con crampones y piolet."),
        ("¿Cuál es el pico más alto de Gredos?", "El Almanzor, con 2.591 m. Es también el más alto de todo el Sistema Central."),
        ("¿Cuándo es mejor ir a Gredos?", "Sin nieve, de junio a octubre, evitando las tardes de tormenta en verano. En invierno las rutas altas son de alpinismo y solo para personas con material y formación, o con guía."),
        ("¿Se puede dormir en la Laguna Grande?", "En el refugio Elola, con reserva. La acampada libre está prohibida en el Parque Regional de la Sierra de Gredos."),
    ],
    fuentes=[
        ("https://www.turismocastillayleon.com/es/rural-naturaleza/rutas-naturaleza/carril-galayos", "Turismo de Castilla y León: senda del Carril de los Galayos"),
        ("https://guiarutas.es/rutas/castilla-y-leon/almanzor-desde-la-plataforma/", "Guiarutas: el Almanzor desde la Plataforma"),
        ("https://www.montanapegaso.es/carteles/2013/lamira_info.pdf", "Grupo de Montaña Pegaso: ruta a La Mira (PDF)"),
        ("https://patrimonionatural.org/espacios-naturales/parque-regional/parque-regional-sierra-de-gredos", "Patrimonio Natural de Castilla y León: Parque Regional de la Sierra de Gredos"),
        ("https://www.ign.es/iberpix/visor/", "IGN: visor de mapas"),
    ],
    nota="Datos orientativos para condiciones de verano sin nieve. Las condiciones de la montaña cambian: infórmate antes de salir.",
))

# ───────────────────────────── 11. MEJORES VÍAS DE ESCALADA DE GREDOS ─────────────────────────────
_BL = "https://jairogredos.blogspot.com/"
ARTS.append(dict(
    path="/mejores-vias-escalada-gredos/",
    corto="Las mejores vías de escalada de Gredos",
    card="Sur del Torreón, Tres Hermanitos, Gran Diedro del Torozo, Sur de la Apretura y Gran Diedro del Gran Galayo.",
    titulo="Las mejores vías clásicas de escalada de Gredos",
    meta_title="Mejores vías de escalada clásica en Gredos | Ad Astra",
    meta_desc="Reseña de cinco clásicas de Gredos: Sur del Torreón, Tres Hermanitos, Gran Diedro del Torozo, Sur de la Apretura y Gran Diedro del Gran Galayo. Con fotos.",
    lead="Cinco vías de granito que todo escalador de clásica debería hacer en Gredos: la Sur del Torreón de los Galayos, los Tres Hermanitos del Circo, el Gran Diedro del Torozo, la Sur de la Apretura al Pequeño Galayo y el Gran Diedro del Gran Galayo. Largos, grados, material, bajadas, fotos y enlace al croquis original de cada una.",
    hero="/img/fotos/escalada-galayos-cordada.webp",
    actions='<a class="btn btn-primary" href="#resumen">Las cinco vías</a><a class="btn btn-ghost" href="/actividades/curso-iniciacion-escalada-en-roca/">Curso de escalada</a>',
    ico="escalada", og=("Artículo", "Vías clásicas de Gredos", "Torreón, Hermanitos, Torozo, Pequeño y Gran Galayo", "#e9a53b"),
    publicado="2026-11-24", cat="Escalada y alpinismo",
    cuerpo=(
        seccion("Antes de nada", "Escalada clásica en granito: lo que hay que saber",
                p("Gredos es una de las grandes escuelas de escalada clásica de España. Sus vías son de <b>granito</b>, cortas comparadas con las del Pirineo pero con mucho ambiente, y casi todas se abrieron entre los años 30 y 70. Eso quiere decir dos cosas: los <b>grados son «de los de antes»</b> (un IV+ de Galayos puede parecerte un 5b largo de deportiva) y <b>casi todo el seguro lo pones tú</b>, con friends y fisureros, con algún clavo viejo de recuerdo.") +
                tarjetas([
                    ("#e9a53b", "Material de base", "Dos cuerdas de 60 m (o una de 60 m en las vías cortas), un juego de friends hasta el n.º 3 (algún n.º 4 ayuda en los diedros), fisureros, 10–12 cintas, cordinos y material de reunión. Casco siempre."),
                    ("#4fb3e8", "Clavos y reuniones", "Los clavos que encuentres pueden tener 50 años: refuérzalos con tus seguros. Las cadenas de rápel de las cimas sí suelen estar en buen estado, pero revísalas."),
                    ("#7cc47f", "Época", "De mayo a octubre. En verano, madruga: las tormentas de tarde son habituales y el granito mojado con líquenes resbala muchísimo (lo explicamos en <a href=\"/tormentas-en-la-montana/\">tormentas</a>)."),
                ]) +
                '<p style="margin-top:16px">Si no tienes claro cómo se leen los grados, mira las <a href="/escalas-dificultad-escalada-ferratas-alpinismo-barrancos/">escalas de dificultad</a>. Y si quieres empezar con seguridad, tenemos un <a href="/actividades/curso-iniciacion-escalada-en-roca/">curso de iniciación a la escalada en roca</a>.</p>') +
        seccion("Resumen", "Las cinco vías de un vistazo",
                tabla(["Vía", "Dónde", "Longitud", "Largos", "Dificultad"], [
                    ["<a href=\"#torreon\">Sur Clásica del Torreón</a>", "Galayos", "≈ 130–140 m", "3–4", "V / V+"],
                    ["<a href=\"#hermanitos\">Tres Hermanitos</a>", "Circo de Gredos", "30–50 m cada aguja", "1–2 por aguja", "IV a V+"],
                    ["<a href=\"#torozo\">Gran Diedro del Torozo</a>", "Puerto del Pico", "≈ 200 m", "6", "V+ (IV–V+)"],
                    ["<a href=\"#apretura\">Sur de la Apretura</a>", "Galayos (Pequeño Galayo)", "≈ 120–150 m", "4–6", "IV/IV+ (un paso de V+ evitable)"],
                    ["<a href=\"#gran-diedro\">Gran Diedro</a>", "Galayos (Gran Galayo)", "≈ 100–120 m", "3", "IV+ (pasos de V)"],
                ]) +
                '<p class="small muted" style="margin-top:10px">Datos orientativos recopilados de varias reseñas; los metros y los grados varían de una fuente a otra. Los croquis originales están enlazados en cada vía, en las webs de sus autores.</p>',
                True, "resumen") +
        seccion("Los Galayos", "Cómo llegar a Los Galayos",
                p("Las tres vías de Galayos salen del <b>refugio Victory</b> (unos 1.950 m), al pie de las agujas. Se llega desde el aparcamiento del <b>Nogal del Barranco</b>, encima de Guisando, por el camino de la garganta: unos 6,5 km y 870 m de subida, entre 2 y 3 horas con la mochila de escalada. Otra opción, más larga y sin camino en algún tramo, es entrar desde el norte por Los Pelaos. Lo contamos en <a href=\"/rutas-clasicas-gredos-almanzor-laguna-grande-galayos/\">rutas clásicas de Gredos</a>.") +
                '<div class="gd-fotos">' + fblog("escalada-galayos-agujas", "Las agujas de granito de Los Galayos.", _BL + "2009/10/pequeno-galayo.html") +
                fblog("escalada-galayos-reunion", "Reunión en el Pequeño Galayo.", _BL + "2009/10/pequeno-galayo.html") + '</div>') +
        seccion("Vía 1", "Sur Clásica al Torreón de los Galayos (V/V+)",
                p("El <b>Torreón</b> es la aguja más espectacular de Galayos: vertical por todas sus caras, sin ningún camino fácil a la cumbre (la cumbre sur se alcanzó por primera vez en 1947). Su vía Sur es la gran clásica de la sierra y una de las más bonitas del Sistema Central.") +
                '<p class="gd-croquis"><b>Croquis original:</b> <a href="http://pelegrinajes.blogspot.com/2012/05/aroma-galayero-el-torreon.html" target="_blank" rel="noopener">blog Pelegrinajes</a> · ' + '<a href="https://jairogredos.blogspot.com/2011/12/torreon-de-los-galayos.html" target="_blank" rel="noopener">croquis de la Sur Directa en la crónica de Jairo</a> · <a href="https://pablovelasco73.blogspot.com/2020/08/sur-del-torreon-galayos-130m-v.html" target="_blank" rel="noopener">reseña de Pablo Velasco</a>' + '</p>' +
                '<div class="gd-fotos">' + fblog("torreon-largo-final", "En el último largo de la Sur del Torreón.", "https://jairogredos.blogspot.com/2011/12/torreon-de-los-galayos.html") + fblog("torreon-rapel", "El rápel de acceso a la cara sur.", "https://jairogredos.blogspot.com/2011/12/torreon-de-los-galayos.html") + "</div>" +
                dos("La vía",
                    reglas(["<b>Acceso al pie:</b> desde el Victory se sube por la Trocha Palomo hasta la <b>Plataforma de las Flores</b>, en la cara norte, y desde allí se baja un <b>rápel de 60 m</b> a la cara sur. Las zapatillas de aproximación se quedan en la plataforma.",
                            "<b>L1 (≈ 50 m, V):</b> la entrada es dura, junto a un clavo. Se termina en un nicho bajo un pequeño techo, con un puente de roca para reforzar la reunión.",
                            "<b>L2 (≈ 30 m, V+):</b> travesía corta a la izquierda hasta una fisura vertical que entra en un sistema de diedros. Muy buen largo.",
                            "<b>L3 (≈ 50 m, V):</b> más vertical, con buena roca, hasta una placa tumbada que lleva a la cadena de la cumbre. Asegura desde la cadena: es expuesto.",
                            "Hay una variante, la <b>Sur Directa</b> (≈ 140–150 m, V+), con la que comparte la parte alta."]),
                    "Material y bajada",
                    reglas(["Dos cuerdas de 60 m (imprescindibles para el rápel).", "Juego de friends con predominio de medidas pequeñas y fisureros; unas 12–15 cintas.",
                            "<b>Bajada:</b> rápel de 60 m desde la cadena de la cumbre por la cara norte hasta la Plataforma de las Flores, y destrepe con cuidado (mejor encordados) hasta la canal y el refugio.",
                            "Cuenta con una jornada larga: unas 9–10 horas de coche a coche.",
                            "<a href=\"" + _BL + "2011/12/torreon-de-los-galayos.html\" target=\"_blank\" rel=\"noopener\">Crónica del Torreón en el blog de Jairo →</a>"])),
                False, "torreon") +
        seccion("Vía 2", "Los Tres Hermanitos del Circo de Gredos (IV a V+)",
                p("Tres agujas de granito alineadas en el <b>cordal de Cerraíllos</b>, entre el Morezón y el Casquerazo, encima del refugio Elola y la Laguna Grande, con el Almanzor de fondo. Se numeran de izquierda a derecha y en una jornada se pueden subir las tres. Muy cerca está el Risco del Perro que Fuma.") +
                '<p class="gd-croquis"><b>Croquis original:</b> <a href="http://pelegrinajes.blogspot.com/2014/07/tres-hermanitos-de-gredos.html" target="_blank" rel="noopener">blog Pelegrinajes</a> · ' + '<a href="https://cuadernodemonte.wordpress.com/2012/08/24/circo-de-gredos-los-hermanitos/" target="_blank" rel="noopener">Cuaderno de monte</a> · <a href="http://acerando-el-largo.blogspot.com/2011/07/escalada-de-los-tres-hermanitos-gredos.html" target="_blank" rel="noopener">Acerando el largo</a>' + '</p>' +
                fotos(("hermanitos-laguna", "Los Tres Hermanitos desde la Laguna Grande."), ("hermanitos-cerca", "Las agujas de los Hermanitos.")) +
                dos("Las vías",
                    reglas(["<b>3.º Hermanito · vía Teógenes (IV, ≈ 30 m, 1 largo, cara N):</b> la más fácil y la primera que se escaló (se atribuye a Teógenes Díaz, en solitario, hacia 1932). Fisura con un estrechamiento protegido con clavos.",
                            "<b>2.º Hermanito · vía Teógenes (V+, ≈ 45 m, 2 largos, cara SO):</b> abierta en 1951. El primer largo pide buscar bien la línea; el segundo es corto, desplomado y con una salida expuesta.",
                            "<b>1.º Hermanito · vía Pirineos (V+, ≈ 50 m, 2 largos, cara SO):</b> abierta en 1973. Fisura hasta un rellano y travesía bajo el gran diedro que separa sus dos cumbres; los últimos pasos son los más expuestos.",
                            "Hay vías más duras en las tres agujas (diedros de V/V+ en la cara norte del 2.º, la Folliot en el 1.º…)."]),
                    "Acceso, material y bajada",
                    reglas(["<b>Acceso:</b> de la Plataforma al refugio Elola (unas 2 h 30) y de allí, por hitos hacia la portilla de los Machos y canales sencillas (II), una hora más.",
                            "Fisureros y friends hasta el n.º 3. Una cuerda doble o dos cuerdas de 60 m.",
                            "<b>Bajada:</b> rápel desde la cadena de cada cumbre, por la misma cara (unos 30 m en el 2.º y el 3.º). Cuidado al recuperar las cuerdas: se enganchan.",
                            "Puedes hacerlo en dos días durmiendo en el refugio Elola."])),
                True, "hermanitos") +
        seccion("Vía 3", "Gran Diedro del Torozo (V+)",
                p("El <b>Torozo</b> es la punta occidental del Macizo Oriental de Gredos, encima del Puerto del Pico, con una cara sur de hasta 400 m sobre el valle de las Cinco Villas. Su aproximación es mucho más corta que la de Galayos, y el <b>Gran Diedro</b>, abierto en 1972, es su gran clásica.") +
                '<p class="gd-croquis"><b>Croquis original:</b> ' + '<a href="https://www.sanestebandelvalle.es/pdf/escalada_torozo.pdf" target="_blank" rel="noopener">guía de escalada del Torozo (Ayto. de San Esteban del Valle, PDF)</a> · <a href="https://summitpost.org/torozo/151045" target="_blank" rel="noopener">SummitPost</a>' + '</p>' +
                fotos(("torozo", "El Torozo desde el valle."), ("torozo-nieve", "El Torozo nevado.")) +
                dos("La vía",
                    reglas(["Unos <b>200 m en 6 largos</b>: IV, IV, V, V, V+ y IV.", "Sigue un gran diedro muy evidente desde abajo: la línea no tiene pérdida.",
                            "El quinto largo es el más difícil y el más físico.", "Las reuniones suelen estar equipadas; entre medias, seguros tuyos."]),
                    "Acceso, material y bajada",
                    reglas(["<b>Acceso:</b> desde el Puerto del Pico (aparcamiento, fuente y bar). Se sigue la senda que sale detrás del restaurante y, por la cueva de pastores, una vereda hacia el este lleva al pie de las vías. Unos 30–45 minutos.",
                            "Juego de friends y fisureros, unas 10 cintas y dos cuerdas de 60 m.",
                            "<b>Bajada:</b> de la cumbre al collado norte siguiendo hitos (hay un rápel instalado a la derecha si la roca está mojada o con hielo) y por una canal hacia el oeste.",
                            "Al estar orientado al sur, es una buena opción en primavera y otoño. En verano, solo a primera hora."])),
                False, "torozo") +
        seccion("Vía 4", "Sur de la Apretura al Pequeño Galayo (IV/IV+)",
                p("La vía más asequible de este artículo y una de las más escaladas de Galayos: ideal como primera clásica en Gredos. Fue abierta en 1952 y sube al Pequeño Galayo por la parte baja de la canal del Gran Galayo. Mucha gente la encadena con el Gran Diedro del Gran Galayo en el mismo día.") +
                '<p class="gd-croquis"><b>Croquis original:</b> <a href="http://pelegrinajes.blogspot.com/2014/08/pequeno-y-gran-galayo.html" target="_blank" rel="noopener">blog Pelegrinajes</a> · ' + '<a href="https://guiasoeste.com/sur-de-la-apretura-y-gran-diedro-galayos/" target="_blank" rel="noopener">Guías Oeste</a> · <a href="https://www.ukclimbing.com/logbook/crags/galayos-20797/sur_de_la_apretura-744364" target="_blank" rel="noopener">UKClimbing</a>' + '</p>' +
                dos("La vía",
                    reglas(["<b>Inicio:</b> un diedrito vertical en la pared izquierda, al pie de la canal del Gran Galayo.",
                            "<b>L1:</b> hasta una gran terraza con bloques para montar la reunión.",
                            "<b>L2:</b> pared vertical de buenos cantos derivando a la derecha hasta una canal; reunión en un nicho con un clavo.",
                            "<b>L3:</b> travesía a la izquierda hasta un espolón, chimenea corta (mejor en oposición que con la mochila dentro), placa y canal-chimenea hasta una repisa grande.",
                            "<b>L4:</b> se sube a un hombro amplio y de ahí a una <b>fisura de V+</b> (bien protegible), y un diedro tumbado hasta el collado y la cumbre. El V+ se puede evitar.",
                            "Se suele graduar <b>IV+</b>, aunque casi todo es IV salvo el paso final."]),
                    "Material y bajada",
                    reglas(["Friends hasta el n.º 3 y un juego de fisureros. Con una cuerda de 60 m vas sobrado; con 40 m tendrás que montar más reuniones.",
                            "<b>Bajada:</b> rápel corto hasta el hombro y destrepe por hitos. Los hitos se separan: abajo y a la derecha, a la canal del Gran Galayo y el refugio; arriba y a la izquierda, al pie del Gran Diedro.",
                            "<a href=\"" + _BL + "2009/10/pequeno-galayo.html\" target=\"_blank\" rel=\"noopener\">Crónica del Pequeño Galayo en el blog de Jairo →</a>"])) +
                '<div class="gd-fotos">' + fblog("escalada-pequeno-galayo", "Escalando en el Pequeño Galayo.", _BL + "2009/10/pequeno-galayo.html") +
                fblog("escalada-galayos-cordada", "Cordada en las placas de Galayos.", _BL + "2009/10/pequeno-galayo.html") + "</div>",
                True, "apretura") +
        seccion("Vía 5", "Gran Diedro del Gran Galayo (IV+)",
                p("El <b>Gran Galayo</b> (unos 2.220 m) es la cumbre más alta de las agujas. Su Gran Diedro, de unos 60 m, se ve desde el refugio y es uno de los largos más bonitos de la sierra. Es la continuación natural de la Sur de la Apretura.") +
                '<p class="gd-croquis"><b>Croquis original:</b> <a href="http://pelegrinajes.blogspot.com/2014/08/pequeno-y-gran-galayo.html" target="_blank" rel="noopener">blog Pelegrinajes</a> · ' + '<a href="https://guiasoeste.com/sur-de-la-apretura-y-gran-diedro-galayos/" target="_blank" rel="noopener">Guías Oeste</a> · <a href="https://www.ukclimbing.com/logbook/crags/galayos-20797/gran_diedro-453110" target="_blank" rel="noopener">UKClimbing</a>' + '</p>' +
                '<div class="gd-fotos">' + fblog("gran-diedro-sol", "El sol entrando en el Gran Diedro del Gran Galayo.", "https://jairogredos.blogspot.com/2012/09/gran-diedro-al-gran-galayo.html") + fblog("gran-diedro-escalando", "Escalando el Gran Diedro.", "https://jairogredos.blogspot.com/2012/09/gran-diedro-al-gran-galayo.html") + "</div>" +
                dos("La vía",
                    reglas(["<b>Entrada:</b> un resalte vertical y expuesto antes de la portilla del Gran Galayo (protégelo) y una terraza inclinada donde empieza el diedro.",
                            "<b>El diedro (≈ 60 m, IV+):</b> un desplome en la primera mitad marca la dificultad. Hacia los dos tercios hay una reunión con tres clavos. Al final se convierte casi en chimenea: se entra para chapar un clavo alto y se sale por fuera. Todos los pasos tienen clavos.",
                            "<b>Salida:</b> un hombrito con clavo, un diedro tumbado hasta un collado y un tramo fácil que acaba en una cueva entre bloques; se atraviesa y se sale a la derecha a la cumbre.",
                            "Se gradúa IV+, aunque algunos pasos son de V. A la izquierda hay variantes más difíciles."]),
                    "Material y bajada",
                    reglas(["Friends hasta el n.º 3 (un n.º 4 ayuda al final del diedro) y fisureros.",
                            "<b>Bajada sin rápel:</b> por hitos hasta la portilla, con trepadas y destrepes de hasta III, y por la canal al refugio. También se puede volver hacia Los Pelaos por la Trocha Palomo.",
                            "<a href=\"" + _BL + "2012/09/gran-diedro-al-gran-galayo.html\" target=\"_blank\" rel=\"noopener\">Crónica del Gran Diedro en el blog de Jairo →</a>"])),
                False, "gran-diedro")
    ),
    faq=[
        ("¿Cuál es la vía más fácil de Galayos?", "Entre las clásicas, la Sur de la Apretura al Pequeño Galayo: casi toda de IV, con un paso de V+ al final que se puede evitar. Es muy habitual encadenarla con el Gran Diedro del Gran Galayo."),
        ("¿Qué grado tiene la Sur del Torreón de los Galayos?", "La Sur Clásica tiene unos 130–140 m en 3 o 4 largos, de V a V+. Se accede rapelando 60 m desde la Plataforma de las Flores y se baja también en rápel de 60 m."),
        ("¿Qué material hace falta para escalar en Galayos?", "Dos cuerdas de 60 m, un juego de friends hasta el n.º 3 (algún n.º 4 ayuda), fisureros, 10–15 cintas, material de reunión, casco y calzado de aproximación."),
        ("¿Cuánto se tarda en llegar al refugio Victory?", "Desde el aparcamiento del Nogal del Barranco, en Guisando, entre 2 y 3 horas, con unos 870 m de subida."),
        ("¿Dónde están los Tres Hermanitos de Gredos?", "En el cordal de Cerraíllos, entre el Morezón y el Casquerazo, encima del refugio Elola y la Laguna Grande. Se llega en unas 3 horas y media desde la Plataforma de Gredos."),
    ],
    fuentes=[
        ("https://summitpost.org/galayos/150896", "SummitPost: Galayos"),
        ("https://summitpost.org/torozo/151045", "SummitPost: Torozo (Gran Diedro)"),
        ("https://www.sanestebandelvalle.es/pdf/escalada_torozo.pdf", "Ayuntamiento de San Esteban del Valle: escalada en el Torozo (PDF)"),
        ("https://pablovelasco73.blogspot.com/2020/08/sur-del-torreon-galayos-130m-v.html", "Pablo Velasco: Sur del Torreón"),
        ("https://picosyaventura.com/torreon-de-los-galayos-por-la-via-sur-directa/", "Picos y Aventura: el Torreón por la Sur Directa"),
        ("https://guiasoeste.com/sur-de-la-apretura-y-gran-diedro-galayos/", "Guías Oeste: Sur de la Apretura y Gran Diedro"),
        ("https://cuadernodemonte.wordpress.com/2012/08/24/circo-de-gredos-los-hermanitos/", "Cuaderno de monte: los Hermanitos"),
        ("https://sobreescalada.com/2019/10/07/escalada-circo-de-gredos-pared-del-refugio-el-escudo-placa-ecualicer-tres-hermanitos-y-perro-que-fuma/", "Sobre escalada: Circo de Gredos"),
        ("https://www.destinoclimbing.com/castilla-y-leon/escalada-en-galayos/", "Destino Climbing: escalada en Galayos"),
        ("http://pelegrinajes.blogspot.com/2012/05/aroma-galayero-el-torreon.html", "Pelegrinajes: el Torreón"),
        ("http://pelegrinajes.blogspot.com/2014/07/tres-hermanitos-de-gredos.html", "Pelegrinajes: Tres Hermanitos de Gredos"),
        ("http://pelegrinajes.blogspot.com/2014/08/pequeno-y-gran-galayo.html", "Pelegrinajes: Pequeño y Gran Galayo"),
    ],
    nota="Reseña elaborada con nuestras palabras a partir de varias fuentes. Las vías de montaña cambian (clavos que se caen, bloques sueltos): consulta reseñas actualizadas y valora siempre tu nivel.",
))

# ───────────────────────────── 12. INICIACIÓN AL ALPINISMO EN GREDOS ─────────────────────────────
def _ruta_alp(n, titulo, ficha, texto, aprende, ojo, fotos_, enlaces, alt=False, id_=""):
    """Bloque de una ruta de la progresión: ficha de datos, texto, qué se aprende, precauciones, fotos y crónicas del blog."""
    datos = '<div class="gd-ficha">' + "".join('<div><span>%s</span><b>%s</b></div>' % x for x in ficha) + "</div>"
    fot = '<div class="gd-fotos">' + "".join(fblog(a, b, enlaces[0][0]) for a, b in fotos_) + "</div>" if fotos_ else ""
    blogs = '<p style="margin:8px 0 0"><b>Crónicas en el blog de Jairo:</b> ' + " · ".join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (u, t) for u, t in enlaces) + "</p>"
    return seccion("Ruta %d" % n, titulo, datos + p(texto) + dos("Qué aprendes", reglas(aprende), "Ojo con", reglas(ojo)) + fot + blogs, alt, id_)


_B = "https://jairogredos.blogspot.com/"
ARTS.append(dict(
    path="/iniciacion-alpinismo-gredos-rutas-progresivas/",
    corto="Iniciación al alpinismo en Gredos: 9 rutas",
    card="Nueve rutas de menos a más para aprender alpinismo en Gredos: del Morezón a La Ceja, Cabeza Nevada, las canales del Circo y el Almanzor.",
    titulo="Iniciación al alpinismo en Gredos: 9 rutas progresivas",
    meta_title="Iniciación al alpinismo en Gredos: 9 rutas progresivas",
    meta_desc="Nueve rutas para aprender alpinismo en Gredos de menos a más: Morezón, La Mira, La Ceja, Cabeza Nevada, las canales del Circo y el Almanzor.",
    lead="El alpinismo se aprende escalón a escalón. Te proponemos nueve rutas invernales en Gredos ordenadas de la más fácil a la más difícil: primero caminar con nieve, luego distancia y autonomía, después las canales del Circo y, al final, el Almanzor. Con datos, qué aprendes en cada una y las crónicas de Jairo.",
    hero="/img/fotos/alp-portada.webp",
    actions='<a class="btn btn-primary" href="#resumen">Ver las 9 rutas</a><a class="btn btn-ghost" href="/actividades/cursos-alpinismo/">Curso de alpinismo</a>',
    ico="invernal", og=("Artículo", "Iniciación al alpinismo en Gredos", "9 rutas progresivas, del Morezón al Almanzor", "#bfe0f7"),
    publicado="2026-11-24",
    cuerpo=(
        seccion("Cómo funciona", "Una progresión, no una lista",
                p("La mayoría de los accidentes de iniciación en invierno vienen de saltarse pasos: ir al Almanzor sin haber caminado nunca con crampones, o meterse en una canal sin saber frenar una caída con el piolet. Esta progresión ordena nueve rutas clásicas de Gredos para que cada una añada <b>una sola cosa nueva</b> a lo que ya sabes.") +
                ilustracion("/img/guias/progresion-alpinismo-gredos.svg", "Escalera de progresión de nueve rutas de iniciación al alpinismo en Gredos", "Las nueve rutas, de la más fácil a la más difícil.") +
                tarjetas([
                    ("#4caf50", "Rutas 1–3 · Caminar con nieve", "Cumbres sin pasos técnicos: aprender a andar con crampones, llevar el piolet, abrigarse y orientarse con niebla."),
                    ("#cfc845", "Rutas 4–5 · Distancia y autonomía", "Jornadas largas con mucho desnivel: ritmo, horarios, hora límite y elegir la línea en terreno abierto."),
                    ("#ef9330", "Rutas 6–8 · Canales", "Las canales del Circo de Gredos: pendiente sostenida, técnica de crampones y piolet, casco y valorar la nieve."),
                    ("#e8574a", "Ruta 9 · El Almanzor", "Todo lo anterior junto, más una trepada final expuesta y una bajada delicada."),
                ]) +
                reglas(["<b>Pasa a la siguiente</b> cuando la anterior te salga cómoda, y siempre con buenas condiciones. Repite las que te cuesten.",
                        "<b>Mira antes</b> la <a href=\"/meteo/gredos-macizo-central/\">previsión de cumbre</a>, el <a href=\"/nieve/\">estado de la nieve</a> y el boletín de aludes (te explicamos cómo en <a href=\"/como-leer-la-nieve-y-los-aludes/\">cómo leer la nieve</a>).",
                        "<b>Material:</b> botas semirrígidas, crampones, piolet, ropa por capas, gafas de categoría 4 y frontal. Casco desde las canales. ARVA, pala y sonda donde haya riesgo de aludes. Lo explicamos en <a href=\"/crampones-piolet-botas-material-invernal/\">crampones, piolet y botas</a>.",
                        "<b>Antes de las canales</b> tienes que saber autodetenerte con el piolet. Es lo que practicamos en el <a href=\"/actividades/cursos-alpinismo/\">curso de alpinismo</a>."])) +
        seccion("Resumen", "Las 9 rutas de un vistazo",
                tabla(["#", "Ruta", "Salida", "Distancia", "Desnivel", "Dificultad"], [
                    ["1", "<a href=\"#r1\">Morezón (2.393 m)</a>", "Plataforma de Gredos", "≈ 10 km", "≈ +650 m", "F · caminar con nieve"],
                    ["2", "<a href=\"#r2\">La Mira (2.343 m)</a>", "Plataforma de Gredos", "≈ 16–18 km", "≈ +800–1.000 m", "F · cordal largo"],
                    ["3", "<a href=\"#r3\">Canchal de la Ceja (2.428 m)</a>", "Plataforma del Travieso", "≈ 10 km", "≈ +650 m", "F · altiplano expuesto"],
                    ["4", "<a href=\"#r4\">La Mira por los Conventos</a>", "Km 6 (Alto del Durano)", "≈ 19 km", "≈ +1.000 m", "F · jornada larga"],
                    ["5", "<a href=\"#r5\">Cabeza Nevada (2.431 m)</a>", "Navalperal de Tormes", "≈ 20–24 km", "≈ +1.200 m", "F+ · desnivel y autonomía"],
                    ["6", "<a href=\"#r6\">Cerro de los Huertos por la canal de la Pluma</a>", "Plataforma de Gredos", "≈ 15 km", "≈ +1.000 m", "Primera canal"],
                    ["7", "<a href=\"#r7\">Casquerazo (2.436 m) por la canal de los Machos</a>", "Plataforma de Gredos", "≈ 15 km", "≈ +1.100 m", "Canal y cresta final (I)"],
                    ["8", "<a href=\"#r8\">Morezón por la canal de las Hoyuelas</a>", "Plataforma de Gredos", "≈ 14 km", "≈ +1.000 m", "Canal más técnica"],
                    ["9", "<a href=\"#r9\">Almanzor (2.591 m)</a>", "Plataforma de Gredos", "≈ 18 km", "≈ +1.300 m", "PD · canal y trepada de II"],
                ]) +
                '<p class="small muted" style="margin-top:10px">Datos orientativos de ida y vuelta, recopilados de varias reseñas. En invierno los tiempos dependen mucho de la nieve: con nieve blanda puedes tardar el doble.</p>',
                True, "resumen") +
        _ruta_alp(1, "Morezón desde la Plataforma de Gredos",
                  [("Altitud", "2.393 m"), ("Salida", "Plataforma (1.770 m)"), ("Distancia", "≈ 10 km i/v"), ("Desnivel", "≈ +650 m"), ("Horario", "≈ 5 h"), ("Dificultad", "F")],
                  "La primera cumbre invernal ideal: se sube por la amplia cuerda del Cuento, sin pasos técnicos, y desde arriba se ve todo el Circo de Gredos con el Almanzor enfrente. Es la mejor forma de estrenar crampones y piolet en un terreno que perdona.",
                  ["Caminar con crampones en nieve dura y blanda.", "Llevar el piolet en la mano del lado de la ladera.", "Gestionar capas, el frío y el viento de la cuerda."],
                  ["El viento en la cuerda, que puede ser muy fuerte.", "La niebla en la bajada: la cuerda es ancha y es fácil desviarse."],
                  [("alp-morezon", "Llegando al Morezón con nieve."), ("alp-morezon-2", "Vistas desde la cuerda del Morezón.")],
                  [(_B + "2008/04/morezn.html", "Morezón 2.393 m")], False, "r1") +
        _ruta_alp(2, "La Mira desde la Plataforma de Gredos",
                  [("Altitud", "2.343 m"), ("Salida", "Plataforma (1.770 m)"), ("Distancia", "≈ 16–18 km"), ("Desnivel", "≈ +800–1.000 m"), ("Horario", "≈ 7–8 h"), ("Dificultad", "F")],
                  "Misma salida y bastante más distancia: se sube por la Vereda de la Mira hasta el cordal y se sigue la cuerda, por Los Campanarios y la Portilla Pelucas, hasta la cumbre, con el refugio de Los Pelaos al lado. Un balcón sobre el Circo, Los Galayos y el valle del Tiétar.",
                  ["Mantener un ritmo constante en una jornada larga.", "Orientarse en un cordal con niebla con mapa y brújula (lo explicamos en <a href=\"/orientacion-en-montana-mapa-brujula/\">orientación</a>).", "Comer y beber sin parar demasiado."],
                  ["El camino se pierde entre bloques en la cuerda.", "La vuelta es larga: calcula una hora límite para darte la vuelta."],
                  [("ruta-la-mira", "Por la cuerda hacia La Mira.")],
                  [(_B + "2008/04/la-mira.html", "La Mira 2.341 m")], True, "r2") +
        _ruta_alp(3, "Canchal de la Ceja desde la Plataforma del Travieso",
                  [("Altitud", "2.428 m"), ("Salida", "El Travieso (1.870 m)"), ("Distancia", "≈ 10 km i/v"), ("Desnivel", "≈ +650 m"), ("Horario", "≈ 4–5 h"), ("Dificultad", "F")],
                  "El techo de Salamanca, en la Sierra de Béjar y Candelario. Desde el Travieso se sube por la fuente de la Goterita hasta los altiplanos del Calvitero (techo de Extremadura) y, tras un collado, a La Ceja. Ruta corta pero muy expuesta al viento y con unos altiplanos donde perderse con niebla es facilísimo.",
                  ["Orientarse en terreno abierto y sin referencias.", "Decidir cuándo darse la vuelta por el tiempo.", "Primeras laderas algo más inclinadas."],
                  ["Las ventiscas y la niebla en los altiplanos.", "Tras nevadas fuertes pueden hacer falta raquetas."],
                  [("alp-ceja", "En los altiplanos del Calvitero, camino de La Ceja."), ("alp-ceja-2", "Lagunas glaciares desde la cuerda.")],
                  [(_B + "2008/11/paseo-el-travieso-cuerda-del-calvitero.html", "Paseo El Travieso – Cuerda del Calvitero"), (_B + "2008/02/calvitero-la-ceja-el-torreon.html", "Virgen del Calvitero, La Ceja y Calvitero")], False, "r3") +
        _ruta_alp(4, "La Mira desde el km 6 por la Garganta de los Conventos",
                  [("Altitud", "2.343 m"), ("Salida", "Km 6, Alto del Durano"), ("Distancia", "≈ 19 km"), ("Desnivel", "≈ +1.000 m"), ("Horario", "≈ 7 h 30"), ("Dificultad", "F")],
                  "La misma cumbre que la ruta 2, pero desde abajo: se entra por la finca de La Covacha, se pasa a la Garganta de los Conventos y se sube por su margen hasta el Collado de las Yeguas y el refugio de Los Pelaos. La vuelta se puede hacer por el Puerto del Peón. Aquí ya no hay carretera que te deje alto: todo el desnivel es tuyo.",
                  ["Gestionar una jornada larga con nieve de todo tipo, de la húmeda de abajo a la dura de arriba.", "Planificar horarios y puntos de retirada.", "Subir con mochila de invierno durante muchas horas."],
                  ["Los días cortos de invierno: sal de noche y lleva frontal.", "Cruzar arroyos con nieve y hielo en la garganta."],
                  [("ruta-la-mira-2", "En la cuerda de La Mira.")],
                  [(_B + "2010/04/la-mira-desde-el-km6.html", "La Mira desde el Km 6"), (_B + "2010/12/plataforma-de-gredos-la-mira-garganta.html", "Plataforma, La Mira, Garganta de los Conventos y Km 6")], True, "r4") +
        _ruta_alp(5, "Cabeza Nevada desde Navalperal de Tormes",
                  [("Altitud", "2.431 m"), ("Salida", "Navalperal (1.303 m)"), ("Distancia", "≈ 20–24 km"), ("Desnivel", "≈ +1.200 m"), ("Horario", "≈ 9 h"), ("Dificultad", "F+")],
                  "La ruta más larga y solitaria de la lista. Desde Navalperal de Tormes se cruza el Tormes por el puente de Gredos y se sube por la Garganta del Pinar hasta las lagunas de Majalaescoba y la Laguna Bajera. De ahí, una subida empinada lleva a la Portilla del Pluviómetro y, por la cuerda, a la cumbre. Se puede volver por el mismo camino o bajar a la Laguna Grande y la Plataforma (con un segundo coche).",
                  ["Autonomía: horas de marcha lejos de todo.", "Elegir la mejor línea de subida en una ladera abierta.", "Las primeras pendientes serias, entre la Laguna Bajera y la portilla, donde ya hay que saber frenar con el piolet."],
                  ["El tramo de la Laguna Bajera a la portilla, empinado y a veces helado.", "La duración: frontal obligatorio y salida muy temprano."],
                  [("alp-cabeza-nevada", "Subiendo hacia Cabeza Nevada."), ("alp-cabeza-nevada-2", "La cara norte nevada.")],
                  [(_B + "2008/11/cabeza-nevada.html", "Cabeza Nevada (2008)"), (_B + "2009/03/cabeza-nevada.html", "Cabeza Nevada (2009)"), (_B + "2010/03/travesia-navalperal-cabeza-nevada.html", "Travesía Navalperal – Cabeza Nevada – Plataforma")], False, "r5") +
        _ruta_alp(6, "Cerro de los Huertos por la canal de la Pluma",
                  [("Altitud", "≈ 2.450 m"), ("Salida", "Plataforma (1.770 m)"), ("Distancia", "≈ 15 km i/v"), ("Desnivel", "≈ +1.000 m"), ("Horario", "≈ 7–8 h"), ("Dificultad", "Primera canal")],
                  "Primera canal de la progresión. Desde la Plataforma se baja a la Laguna Grande (unas 2 h 30) y se cruza hacia el oeste del Circo, al macizo del Cerro de los Huertos. La canal tiene una pendiente moderada y sostenida y sale a la cumbre, con vistas al Almanzor y a los Cuchillares.",
                  ["Técnica de crampones en pendiente: en pato, de lado y de frente.", "Piolet en apoyo y en ancla en la canal.", "Ponerse el casco y valorar el estado de la nieve en la canal: dura, costra, blanda."],
                  ["Las canales del Circo acumulan nieve venteada: mira el riesgo de aludes.", "La bajada en pendiente cansa más que la subida."],
                  [("alp-huertos", "Entrando en el Circo hacia el Cerro de los Huertos."), ("alp-huertos-2", "Laderas nevadas del Circo.")],
                  [(_B + "2009/02/cerro-de-los-huertos.html", "Cerro de los Huertos"), (_B + "2008/08/cerro-de-los-huertos.html", "Cerro de los Huertos y Cuchillar del Cerro")], True, "r6") +
        _ruta_alp(7, "Casquerazo por la canal de los Machos",
                  [("Altitud", "2.436 m"), ("Salida", "Plataforma (1.770 m)"), ("Distancia", "≈ 15 km i/v"), ("Desnivel", "≈ +1.100 m"), ("Horario", "≈ 8 h"), ("Dificultad", "Canal y cresta (I)")],
                  "Desde el refugio Elola se cruza por las placas del lado oeste hacia el Charco de la Esmeralda y se sube la canal de los Machos, larga y empinada, hasta la Portilla de los Machos (2.382 m). Una canal secundaria lleva a la cresta y, por unos pasos fáciles pero expuestos (I), a la pequeña cumbre del Casquerazo.",
                  ["Mantener el ritmo en una canal larga y abrir huella por relevos.", "Salir de la canal por la cornisa o la portilla.", "Moverse por una cresta expuesta con crampones; los primeros tramos donde puede hacer falta la cuerda."],
                  ["Las cornisas a la salida de la canal.", "La cresta final con hielo: si no lo ves claro, la portilla ya es un buen objetivo."],
                  [("alp-machos", "Camino de la canal de los Machos."), ("alp-machos-2", "Los Cuchillares nevados desde el Circo.")],
                  [(_B + "2008/07/casquerazo.html", "Casquerazo 2.494 m"), (_B + "2020/02/canal-facil-cuhillar-de-la-navajas.html", "Canal Fácil, Cuchillar de las Navajas y Canal de los Machos")], False, "r7") +
        _ruta_alp(8, "Morezón por la canal de las Hoyuelas",
                  [("Altitud", "2.393 m"), ("Salida", "Plataforma (1.770 m)"), ("Distancia", "≈ 14 km i/v"), ("Desnivel", "≈ +1.000 m"), ("Horario", "≈ 7–8 h"), ("Dificultad", "Canal más técnica")],
                  "La misma cumbre que la ruta 1, pero por su cara del Circo: desde la Laguna Grande se sube por la zona de Las Hoyuelas, bajo el Risco de las Hoyuelas, hasta el cordal del Morezón. Es la canal más técnica antes del Almanzor y la mejor prueba para saber si estás preparado para él.",
                  ["Pendiente sostenida durante mucho rato.", "Montar las primeras reuniones y asegurar en nieve.", "Bajar por terreno técnico o elegir una bajada más fácil (por la cuerda del Cuento)."],
                  ["Pendiente de nieve dura: una caída no se para sola.", "Calcula bien la hora: la nieve se ablanda a mediodía."],
                  [("alp-hoyuelas", "Subiendo por Las Hoyuelas."), ("alp-hoyuelas-2", "En la parte alta de la canal.")],
                  [(_B + "2009/12/navasomera-las-hoyuelas-canal-sur-de-la.html", "Navasomera, Las Hoyuelas y Canal de las Hoyuelas"), (_B + "2011/12/cuchillar-de-cerraillos-risco-de-las.html", "Cuchillar de Cerraíllos, Risco de las Hoyuelas y Morezón")], True, "r8") +
        _ruta_alp(9, "El Almanzor",
                  [("Altitud", "2.591 m"), ("Salida", "Plataforma (1.770 m)"), ("Distancia", "≈ 18 km i/v"), ("Desnivel", "≈ +1.300 m"), ("Horario", "≈ 9–10 h"), ("Dificultad", "PD · trepada de II")],
                  "El techo del Sistema Central y el objetivo de toda la progresión. Se sube por la Laguna Grande y la Hoya de Antón a la canal de la Portilla del Crampón (pendientes de 40–50° en invierno), se cruza por encima de las Canales Oscuras y una trepada final de II, expuesta, lleva al vértice. Te lo contamos con detalle en <a href=\"/rutas-clasicas-gredos-almanzor-laguna-grande-galayos/\">rutas clásicas de Gredos</a>.",
                  ["Juntar todo lo anterior en una jornada exigente.", "Encordarse en la trepada final y la bajada (destrepe o rápel).", "Gestionar el grupo y el horario hasta el final."],
                  ["La bajada de la canal, donde pasan muchos accidentes.", "El riesgo de aludes en la canal tras nevadas o con viento."],
                  [("ruta-almanzor", "El Almanzor en invierno, con el itinerario de subida marcado."), ("ruta-almanzor-2", "Cerca de la cumbre del Almanzor.")],
                  [(_B + "2008/02/almanzor.html", "Almanzor 2.592 m"), (_B + "2009/04/almanzor-por-la-canal-este.html", "Almanzor por la Canal Este"), (_B + "2011/12/almanzor-nocturno-y-morezon.html", "Almanzor nocturno y Morezón")], False, "r9") +
        seccion("Y después", "¿Listo para el siguiente nivel?",
                p("Si has hecho las nueve rutas con soltura, estás preparado para el alpinismo de Picos de Europa, el Pirineo o los primeros cuatromiles de los Alpes. Antes, comprueba que sabes:") +
                reglas(["Autodetenerte con el piolet en cualquier postura.", "Moverte con crampones en nieve dura y en roca mezclada.", "Montar una reunión en nieve y asegurar a un compañero.", "Leer el boletín de aludes y decidir sobre el terreno.", "Orientarte con niebla con mapa, brújula y GPS.", "Darte la vuelta a tiempo."]) +
                '<p style="margin-top:16px">Te ayudamos a dar cada paso con nuestro <a href="/actividades/cursos-alpinismo/">curso de alpinismo</a> y las <a href="/actividades/ascensiones-sierra-de-gredos/">ascensiones guiadas en Gredos</a>.</p>', True)
    ),
    faq=[
        ("¿Cuál es la ruta más fácil para empezar en el alpinismo en Gredos?", "El Morezón desde la Plataforma de Gredos: unos 10 km y 650 m de desnivel por una cuerda amplia, sin pasos técnicos, ideal para estrenar crampones y piolet."),
        ("¿Hace falta cuerda en estas rutas?", "En las cinco primeras, normalmente no. En las canales (rutas 6 a 8) puede hacer falta según las condiciones, y en el Almanzor es recomendable para la trepada final y la bajada."),
        ("¿Cuándo hay nieve en Gredos?", "Normalmente de diciembre a abril, aunque varía mucho de un año a otro. Las canales del Circo suelen estar en buenas condiciones a finales de invierno y en primavera, con nieve transformada por la mañana."),
        ("¿Qué es una canal?", "Un corredor estrecho entre paredes de roca que en invierno se llena de nieve. Son la vía natural de subida a muchas cumbres del Circo, pero concentran la caída de piedras y de aludes."),
        ("¿Necesito ARVA para estas rutas?", "En las canales del Circo y en cualquier ladera de más de 30° con nieve, sí: ARVA, pala y sonda para cada persona y saber usarlos."),
    ],
    fuentes=[
        ("https://summitpost.org/morez-n/392970", "SummitPost: Morezón"),
        ("https://summitpost.org/from-plataforma-del-travieso-normal/157704", "SummitPost: La Ceja desde El Travieso"),
        ("https://www.terranostrum.es/senderismo/avila/valle-del-tormes-gredos/sendero-a-la-mira-por-los-conventos", "Terranostrum: La Mira por los Conventos"),
        ("https://www.montanapegaso.es/carteles/2013/lamira_info.pdf", "Grupo de Montaña Pegaso: La Mira (PDF)"),
        ("https://www.montanapegaso.es/carteles/2013/cabezanevada_info.pdf", "Grupo de Montaña Pegaso: Cabeza Nevada (PDF)"),
        ("https://summitpost.org/pe-n-de-casquerazo/962301", "SummitPost: Casquerazo y Portilla de los Machos"),
        ("https://summitpost.org/risco-de-las-hoyuelas/962849", "SummitPost: Risco de las Hoyuelas"),
        ("https://guiarutas.es/rutas/castilla-y-leon/almanzor-desde-la-plataforma/", "Guiarutas: el Almanzor desde la Plataforma"),
    ],
    nota="Datos orientativos recopilados de varias reseñas y de las crónicas de Jairo. En invierno las condiciones lo cambian todo: infórmate antes de salir y, si dudas, date la vuelta.",
))
