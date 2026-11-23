"""Artículos: orientación, vivac y acampada, federarse y rescates, raquetas y esquí de travesía, rutas clásicas de Gredos."""
from arts_util import seccion, tabla, tarjetas, escala, reglas, dos, p, aviso, foto, fotos, ilustracion

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
    hero="afe67801-cf88-4cef-a3ac-e25e4e971634/senderismo-avila-gredos.webp",
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
    hero="398c4c45-1d97-4c78-a790-e6efe5fea909/otros-media-1.webp",
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
                '<div style="max-width:520px;margin:0 auto">' + foto("vivac-noche", "Noche de vivac bajo las estrellas.") + '</div>' +
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
    hero="41645da1-a007-4ff0-8526-61ca467dddb5/curso-arva.webp",
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
    hero="41645da1-a007-4ff0-8526-61ca467dddb5/curso-arva.webp",
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
    lead="Cuatro rutas que todo montañero debería hacer alguna vez en Gredos, contadas por quienes las recorremos cada semana: la Laguna Grande, el Almanzor (techo del Sistema Central), La Mira y Los Galayos. Datos, dificultad y consejos.",
    hero="afe67801-cf88-4cef-a3ac-e25e4e971634/senderismo-avila-gredos.webp",
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
                foto("laguna-grande-gredos", "La Laguna Grande de Gredos.") +
                reglas(["<b>Cuándo:</b> de mayo a noviembre sin nieve. En invierno el camino se cubre y se hiela, sobre todo en Los Barrerones: crampones y piolet, o raquetas con nieve blanda.",
                        "<b>Ojo con:</b> el viento en Los Barrerones y la vuelta, que tiene una subida de unos 250 m desde la laguna cuando ya estás cansado.",
                        "<b>Agua:</b> hay fuentes en el camino, pero no se garantiza que sea potable. Lleva la tuya.",
                        "<b>Fauna:</b> verás cabras montesas casi seguro. No les des de comer.",
                        "Mira la <a href=\"/meteo/gredos-macizo-central/\">previsión del Macizo Central</a> y la webcam de la Laguna Grande antes de ir."])) +
        seccion("Ruta 2", "El Almanzor, techo del Sistema Central",
                p("Con 2.591 m, el pico Almanzor es la cumbre más alta del Sistema Central. La vía normal sigue el camino de la Laguna Grande y continúa por la <b>Hoya de Antón</b> hasta la <b>canal de la Portilla del Crampón</b>, una canal estrecha y empinada de piedra suelta (de 40–50° en los tramos más fuertes). Desde la Portilla del Crampón (2.538 m) se hace una travesía sobre las Canales Oscuras y una <b>trepada final de grado II</b> hasta el vértice.") +
                foto("almanzor", "El pico Almanzor (2.591 m), techo del Sistema Central.") +
                reglas(["<b>No es una excursión:</b> la canal tiene piedras sueltas (casco) y la trepada final es expuesta. No es para personas con vértigo o sin experiencia de trepar.",
                        "<b>En invierno</b> es una ascensión de alpinismo (PD): nieve de hasta 50°, a menudo dura, y riesgo de aludes en la canal. Crampones, piolet, casco y saber autodetenerse; en algunas condiciones, cuerda. Lo explicamos en <a href=\"/crampones-piolet-botas-material-invernal/\">material invernal</a> y <a href=\"/escalas-dificultad-escalada-ferratas-alpinismo-barrancos/\">escalas de dificultad</a>.",
                        "<b>La bajada</b> por la canal es más delicada que la subida: muchos accidentes pasan ahí.",
                        "Puedes dormir en el refugio Elola (con reserva) y subir de madrugada, con más tiempo y menos gente.",
                        "Si quieres subirlo con seguridad, lo hacemos con guía en verano y en invierno: <a href=\"/actividades/ascensiones-sierra-de-gredos/\">ascensiones en Gredos</a>."])) +
        seccion("Ruta 3", "La Mira, el mejor mirador del Circo",
                p("La Mira (2.343 m) está al este del Circo de Gredos y tiene una de las mejores vistas de la sierra: el Circo, Los Galayos y el valle del Tiétar a tus pies. Desde la Plataforma se sube por la <b>Vereda de la Mira</b> hasta el cordal cimero (unos 2.070 m) y se sigue por la cuerda, pasando por Los Campanarios y la Portilla Pelucas, hasta la cumbre. Cerca de la cima están las ruinas del refugio de Los Pelaos.") +
                foto("la-mira-galayos", "La Mira y Los Galayos.") +
                reglas(["<b>Variante circular:</b> se puede bajar por El Raso y el Puerto del Peón hasta la carretera de la Plataforma (hace falta un segundo coche o caminar por la carretera).",
                        "<b>Cuándo:</b> sin nieve es una ruta larga de cordal sin pasos técnicos. En invierno, la cuerda se hiela y el viento es fuerte: crampones y piolet.",
                        "<b>Orientación:</b> en la cuerda el camino a veces se pierde entre bloques. Con niebla, mapa y brújula (<a href=\"/orientacion-en-montana-mapa-brujula/\">cómo usarlos</a>)."]),
                True) +
        seccion("Ruta 4", "Los Galayos desde Guisando",
                p("Los Galayos son las agujas de granito de la cara sur de Gredos, uno de los lugares de escalada clásica más importantes de España. La ruta sale del aparcamiento de <b>El Nogal del Barranco</b>, encima de Guisando, y sube por el camino de la garganta hasta el <b>refugio Victory</b>, al pie de las agujas (el Gran Galayo, la Galana, el Torreón…). Según la Junta, son unos <b>6,5 km con 870 m de subida y unas 3 horas</b>, de dificultad media-alta.") +
                foto("galayos", "Las agujas de granito de Los Galayos.") +
                reglas(["<b>La subida es dura y continua</b>, por la cara sur: en verano hace mucho calor. Sal temprano y lleva bastante agua.",
                        "<b>El refugio Victory</b> es un refugio de escaladores; consulta si está abierto antes de contar con él.",
                        "<b>Prolongación:</b> los más montañeros siguen hasta la Portilla de los Galayos y bajan al Circo o enlazan con La Mira.",
                        "<b>Escalada:</b> las vías de Los Galayos son clásicas de verdad: graduación dura y seguros que hay que poner. Mira cómo leer los grados en <a href=\"/escalas-dificultad-escalada-ferratas-alpinismo-barrancos/\">escalas de dificultad</a>."])) +
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
