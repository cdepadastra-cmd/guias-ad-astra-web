# Web de Guías Ad Astra

La carpeta **`dist/`** es la web completa, lista para subir a cualquier hosting. Las URLs son las mismas que en tu web de Lovable (`/actividades/...`, `/formacion-cursos/`, etc.), así que no pierdes enlaces.

## Qué ha cambiado

- **Alquiler**: sin precio de fin de semana, solo precio por día. Rejilla de 3 artículos por fila (9 artículos = 3 filas completas). El cliente elige día de recogida y devolución, suma unidades con + y −, ve el total y lo envía por **WhatsApp** con fechas, unidades, total, punto de recogida y tallas.
- **Actividades**: cada página tiene un formulario de reserva (opción, día, otro día posible, personas, nombre, comentarios) que envía el mensaje por WhatsApp con el total calculado. El botón «Elegir esta opción» rellena el formulario.
- **Cursos y todas las páginas con texto pegado**: ficha técnica en casillas (época, duración, dónde, precio, grupo), y secciones separadas: sobre el curso, objetivo, contenido en dos columnas, requisitos, incluye / no incluye. Lo mismo en Monte Olimpo (con etapas día a día), Carros de Foc, Senderismo, Cursos de alpinismo (cada nivel en su tarjeta) y Gredos Limpio.
- **Calendario** (`/calendario/`): vista mensual y lista con precio y plazas libres («4 de 10 plazas libres»). Al reservar, la plaza se descuenta y se abre WhatsApp para confirmar. Las páginas de cada curso o actividad muestran sus próximas fechas automáticamente.
- **SEO**: título y descripción únicos por página, datos estructurados (empresa local, productos con precio, cursos, alquiler con precio por día, preguntas frecuentes, migas de pan, eventos del calendario), `sitemap.xml`, `robots.txt`, URLs canónicas a www.guiasadastra.com y textos ampliados en alquiler y boulder con preguntas frecuentes.

## 1. Publicar la web

**Opción fácil (gratis): Netlify**
1. Entra en app.netlify.com/drop y arrastra la carpeta `dist`.
2. En *Domain settings* añade `www.guiasadastra.com` y sigue los pasos para cambiar los DNS donde tengas el dominio.

También vale cualquier hosting (sube el contenido de `dist` a la carpeta pública por FTP).

## 2. Activar el calendario con plazas reales (Google Sheets, 10 minutos)

Hasta que lo actives, el calendario muestra unas **fechas de ejemplo** (marcadas así) desde `dist/data/calendario.json`.

1. Crea una hoja nueva en Google Sheets (por ejemplo «Calendario Ad Astra»).
2. Menú **Extensiones → Apps Script**. Borra lo que haya y pega el contenido de `dist/calendario-google/Code.gs`. Guarda.
3. Arriba elige la función **configurar** y pulsa **▶ Ejecutar**. Acepta los permisos. Se crean las pestañas *Calendario* y *Reservas* con dos filas de ejemplo.
4. **Implementar → Nueva implementación → tipo Aplicación web**. *Ejecutar como*: tú. *Quién tiene acceso*: **Cualquier usuario**. Pulsa Implementar y copia la URL que termina en `/exec`.
5. Abre `dist/config.js` y pega esa URL en `calendarioURL: "..."`. Vuelve a subir la web.

**Cómo lo usas día a día** (desde el ordenador o la app de Google Sheets en el móvil), en la pestaña *Calendario*, una fila por salida:

| columna | qué poner |
|---|---|
| id | un código único, p. ej. `arva-dic-1` |
| fecha / fecha_fin | `2026-12-12` (fecha_fin solo si dura varios días) |
| hora | `9:30` |
| titulo | Curso de ARVA |
| tipo | `Curso` o `Actividad` |
| slug | la parte final de la URL de la página, p. ej. `curso-arva` (así sale también en esa página) |
| precio | 30 (pon 0 si es gratis) |
| plazas_max | 10 |
| plazas_reservadas | 0 — sube sola con cada reserva; bájala a mano si alguien cancela |
| lugar, notas | texto libre |
| publicado | `SI` o `NO` para ocultarla |

Cada reserva queda apuntada en la pestaña *Reservas* (nombre, teléfono, plazas) y te llega un email de aviso. El sistema no deja reservar más plazas de las que quedan.

### Inscripciones de Gredos Limpio
El mismo Apps Script guarda las inscripciones de Gredos Limpio en la pestaña **Inscripciones** (fecha, edición, nombre, apellidos, email, teléfono, localidad, personas y comentarios). Cada inscrito recibe un correo de confirmación y a ti te llega un aviso.
Para activarlo basta con tener desplegado el Apps Script y pegar su URL en `config.js` (`calendarioURL` o `appsScriptURL`). Si ya lo tenías desplegado antes de este cambio, vuelve a pegar el código nuevo de `Code.gs`, ejecuta `configurar` y haz **Implementar → Gestionar implementaciones → Editar → Nueva versión**.
La edición y la fecha se cambian en `data.py` (`GREDOS_LIMPIO`).

## 3. Después de publicar (SEO)

1. Da de alta el dominio en **Google Search Console** y envía `https://www.guiasadastra.com/sitemap.xml`.
2. Revisa tu ficha de **Google Business Profile** y enlaza las páginas de alquiler y boulder.
3. Si cambias de dominio, edita `domain` en `data.py` y vuelve a generar.

## 4. Cambiar textos o precios

Todo el contenido está en `data.py`. Edítalo y ejecuta `python3 build.py`; se regenera `dist/`. (También puedes editar directamente los HTML de `dist`.)

## Revisa antes de publicar

- **Fechas pasadas**: Monte Olimpo (5–11 sep 2026) y Carros de Foc (5–11 ago 2026) ya han pasado; actualiza las fechas en `data.py`. Gredos Limpio muestra la última edición (8 nov 2025).
- En Monte Olimpo la ficha original decía 782 € y el precio 793 €; he dejado 793 €.
- He corregido errores del texto original (Senderismo mencionaba Alicante; Espeleología en Segovia tenía el texto de barranquismo de Gredos).
- Las descripciones de cada sector de **boulder en Zona Centro** y los textos ampliados de alquiler y boulder los he redactado yo para SEO: confirma que todo es correcto.
- Las **fotos** siguen alojadas en Lovable. Si cierras ese proyecto, descárgalas a una carpeta `img/` y cambia la línea `IMG = ...` de `data.py`.
