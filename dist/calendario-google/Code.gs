/**
 * Guías Ad Astra · Calendario de actividades y cursos con plazas
 * ----------------------------------------------------------------
 * Pega este código en Extensiones > Apps Script de tu Google Sheet.
 * La hoja "Calendario" es tu panel de administración: cada fila es una salida.
 * Las inscripciones a Gredos Limpio se guardan en la hoja "Inscripciones".
 * Cuando alguien reserva en la web, se suman sus plazas en "plazas_reservadas"
 * y se apunta en la hoja "Reservas". Si alguien cancela, baja el número a mano.
 */

// ID de la hoja de Google. Si el script está dentro de la propia hoja (Extensiones > Apps Script) puede quedarse vacío.
var HOJA_ID = '';
function libro_() { return HOJA_ID ? SpreadsheetApp.openById(HOJA_ID) : SpreadsheetApp.getActiveSpreadsheet(); }

var HOJA_CAL = 'Calendario';
var HOJA_RES = 'Reservas';
var HOJA_INS = 'Inscripciones';
var COLUMNAS = ['id', 'fecha', 'fecha_fin', 'hora', 'titulo', 'tipo', 'slug', 'precio', 'plazas_max', 'plazas_reservadas', 'lugar', 'notas', 'publicado'];

/** Ejecútalo una vez (botón ▶) para crear las hojas con sus columnas y un ejemplo. */
function configurar() {
  var ss = libro_();
  var cal = ss.getSheetByName(HOJA_CAL) || ss.insertSheet(HOJA_CAL);
  if (cal.getLastRow() === 0) {
    cal.appendRow(COLUMNAS);
    cal.appendRow(['arva-1', '2026-12-12', '', '9:30', 'Curso de ARVA', 'Curso', 'curso-arva', 30, 10, 0, 'Plataforma de Gredos (Ávila)', '', 'SI']);
    cal.appendRow(['barr-1', '2027-01-16', '2027-01-17', '9:00', 'Curso de barranquismo', 'Curso', 'curso-barranquismo', 150, 6, 0, 'Valle del Jerte (Cáceres)', 'Incluye dossier técnico', 'SI']);
    cal.getRange(1, 1, 1, COLUMNAS.length).setFontWeight('bold').setBackground('#f0b445');
    cal.setFrozenRows(1);
    cal.getRange('B:C').setNumberFormat('yyyy-mm-dd');
    cal.getRange('D:D').setNumberFormat('@');
  }
  var res = ss.getSheetByName(HOJA_RES) || ss.insertSheet(HOJA_RES);
  if (res.getLastRow() === 0) {
    res.appendRow(['fecha_reserva', 'id_salida', 'titulo', 'fecha_salida', 'plazas', 'nombre', 'apellidos', 'email', 'telefono', 'estado']);
    res.getRange(1, 1, 1, 10).setFontWeight('bold').setBackground('#7fb3a3');
    res.setFrozenRows(1);
  }
  var ins = ss.getSheetByName(HOJA_INS);
  if (!ins) { // si la primera pestaña ya tiene la cabecera de inscripciones, se reutiliza
    ss.getSheets().forEach(function (s) { if (!ins && String(s.getRange(1, 1).getValue()) === 'fecha_inscripcion') { s.setName(HOJA_INS); ins = s; } });
    if (!ins) ins = ss.insertSheet(HOJA_INS);
  }
  if (ins.getLastRow() === 0) {
    ins.appendRow(['fecha_inscripcion', 'evento', 'edicion', 'nombre', 'apellidos', 'email', 'telefono', 'localidad', 'personas', 'comentarios']);
    ins.getRange(1, 1, 1, 10).setFontWeight('bold').setBackground('#e9a53b');
    ins.setFrozenRows(1);
  }
}

function leerSalidas_() {
  var sh = libro_().getSheetByName(HOJA_CAL);
  // Se leen los valores tal y como se ven en la hoja (evita desfases de zona horaria en fechas y horas)
  var datos = sh.getDataRange().getDisplayValues();
  var cab = datos.shift().map(function (c) { return String(c).trim(); });
  return datos.map(function (fila, i) {
    var o = { _fila: i + 2 };
    cab.forEach(function (c, j) { o[c] = String(fila[j]).trim(); });
    return o;
  }).filter(function (o) { return o.id && o.fecha && String(o.publicado || 'SI').toUpperCase() !== 'NO'; });
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

/** La web pide la lista de salidas. */
function doGet(e) {
  var salidas = leerSalidas_().map(function (o) {
    var max = Number(o.plazas_max) || 0, res = Number(o.plazas_reservadas) || 0;
    return { id: String(o.id), fecha: o.fecha, fecha_fin: o.fecha_fin || '', hora: o.hora || '', titulo: o.titulo, tipo: o.tipo,
             slug: o.slug || '', precio: Number(o.precio) || 0, plazas_max: max, plazas_libres: Math.max(0, max - res),
             lugar: o.lugar || '', notas: o.notas || '' };
  });
  return json_({ events: salidas });
}

/** La web envía una reserva: resta plazas de forma segura (sin sobreventa). */
function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var d = JSON.parse(e.postData.contents || '{}');
    if (d.action === 'inscripcion') return inscribir_(d);
    var plazas = Math.max(1, Math.min(20, parseInt(d.plazas, 10) || 1));
    var nombre = String(d.nombre || '').slice(0, 80).trim();
    var apellidos = String(d.apellidos || '').slice(0, 120).trim();
    var email = String(d.email || '').slice(0, 120).trim();
    var tel = String(d.telefono || '').replace(/[^\d+ ]/g, '').slice(0, 20).trim();
    if (!nombre || tel.replace(/\D/g, '').length < 9) return json_({ ok: false, error: 'Revisa el nombre y el teléfono.' });

    var salida = leerSalidas_().filter(function (o) { return String(o.id) === String(d.id); })[0];
    if (!salida) return json_({ ok: false, error: 'Esta fecha ya no está disponible.' });
    if ((!apellidos || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)))
      return json_({ ok: false, error: 'Necesitamos nombre, apellidos, correo y teléfono.' });

    var max = Number(salida.plazas_max) || 0, res = Number(salida.plazas_reservadas) || 0, libres = max - res;
    if (plazas > libres) return json_({ ok: false, error: libres > 0 ? 'Solo quedan ' + libres + ' plazas.' : 'Esta fecha está completa.', libres: Math.max(0, libres) });

    var ss = libro_(), sh = ss.getSheetByName(HOJA_CAL);
    var col = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0].map(String).indexOf('plazas_reservadas') + 1;
    sh.getRange(salida._fila, col).setValue(res + plazas);
    ss.getSheetByName(HOJA_RES).appendRow([new Date(), salida.id, salida.titulo, salida.fecha, plazas, nombre, apellidos, email, tel, 'Pendiente de confirmar']);

    // Aviso por email (opcional). Cambia la dirección o borra estas líneas si no lo quieres.
    try {
      MailApp.sendEmail('guiasadastra@gmail.com', 'Nueva reserva: ' + salida.titulo + ' (' + salida.fecha + ')',
        nombre + ' ' + apellidos + ' (' + tel + (email ? ', ' + email : '') + ') ha reservado ' + plazas + ' plaza(s).\nQuedan ' + (libres - plazas) + ' de ' + max + '.');
    } catch (err) {}

    return json_({ ok: true, libres: libres - plazas });
  } finally {
    lock.releaseLock();
  }
}

/** Inscripción a un evento gratuito (Gredos Limpio): guarda una fila en la hoja "Inscripciones". */
function inscribir_(d) {
  var t = function (v, n) { return String(v || '').slice(0, n || 120).trim(); };
  var nombre = t(d.nombre, 80), apellidos = t(d.apellidos), email = t(d.email), tel = t(d.telefono, 20).replace(/[^\d+ ]/g, '');
  var personas = Math.max(1, Math.min(20, parseInt(d.personas, 10) || 1));
  if (!nombre || !apellidos || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || tel.replace(/\D/g, '').length < 9)
    return json_({ ok: false, error: 'Revisa nombre, apellidos, correo y teléfono.' });
  var ss = libro_();
  var sh = ss.getSheetByName(HOJA_INS);
  if (!sh) { configurar(); sh = ss.getSheetByName(HOJA_INS); }
  sh.appendRow([new Date(), t(d.evento), t(d.edicion), nombre, apellidos, email, tel, t(d.localidad), personas, t(d.comentarios, 500)]);
  try {
    MailApp.sendEmail(email, 'Inscripción recibida: ' + t(d.edicion),
      'Hola ' + nombre + ',\n\nHemos recibido tu inscripción a ' + t(d.edicion) + (personas > 1 ? ' para ' + personas + ' personas' : '') + '.\n' +
      'Te enviaremos los detalles de la jornada unos días antes.\n\n¡Gracias por cuidar Gredos!\nGuías Ad Astra · 621 075 048');
    MailApp.sendEmail('guiasadastra@gmail.com', 'Nueva inscripción: ' + t(d.edicion), nombre + ' ' + apellidos + ' (' + tel + ', ' + email + ') · ' + personas + ' persona(s).');
  } catch (err) {}
  return json_({ ok: true });
}

/** Ejecuta esta función una vez si necesitas volver a dar permisos (correo y hoja). */
function autorizar() {
  Logger.log(MailApp.getRemainingDailyQuota());
  Logger.log(libro_().getName());
}
