/**
 * Guías Ad Astra · Calendario de actividades y cursos con plazas
 * ----------------------------------------------------------------
 * Pega este código en Extensiones > Apps Script de tu Google Sheet.
 * La hoja "Calendario" es tu panel de administración: cada fila es una salida.
 * Cuando alguien reserva en la web, se suman sus plazas en "plazas_reservadas"
 * y se apunta en la hoja "Reservas". Si alguien cancela, baja el número a mano.
 */

var HOJA_CAL = 'Calendario';
var HOJA_RES = 'Reservas';
var COLUMNAS = ['id', 'fecha', 'fecha_fin', 'hora', 'titulo', 'tipo', 'slug', 'precio', 'plazas_max', 'plazas_reservadas', 'lugar', 'notas', 'publicado'];

/** Ejecútalo una vez (botón ▶) para crear las hojas con sus columnas y un ejemplo. */
function configurar() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var cal = ss.getSheetByName(HOJA_CAL) || ss.insertSheet(HOJA_CAL);
  if (cal.getLastRow() === 0) {
    cal.appendRow(COLUMNAS);
    cal.appendRow(['arva-1', '2026-12-12', '', '9:30', 'Curso de ARVA', 'Curso', 'curso-arva', 30, 10, 0, 'Plataforma de Gredos (Ávila)', '', 'SI']);
    cal.appendRow(['barr-1', '2027-01-16', '2027-01-17', '9:00', 'Curso de barranquismo', 'Curso', 'curso-barranquismo', 150, 6, 0, 'Valle del Jerte (Cáceres)', 'Incluye dossier técnico', 'SI']);
    cal.getRange(1, 1, 1, COLUMNAS.length).setFontWeight('bold').setBackground('#f0b445');
    cal.setFrozenRows(1);
    cal.getRange('B:C').setNumberFormat('yyyy-mm-dd');
  }
  var res = ss.getSheetByName(HOJA_RES) || ss.insertSheet(HOJA_RES);
  if (res.getLastRow() === 0) {
    res.appendRow(['fecha_reserva', 'id_salida', 'titulo', 'fecha_salida', 'plazas', 'nombre', 'telefono', 'estado']);
    res.getRange(1, 1, 1, 8).setFontWeight('bold').setBackground('#7fb3a3');
    res.setFrozenRows(1);
  }
}

function leerSalidas_() {
  var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_CAL);
  var datos = sh.getDataRange().getValues();
  var cab = datos.shift().map(function (c) { return String(c).trim(); });
  return datos.map(function (fila, i) {
    var o = { _fila: i + 2 };
    cab.forEach(function (c, j) {
      var v = fila[j];
      if (v instanceof Date) v = Utilities.formatDate(v, Session.getScriptTimeZone(), c === 'hora' ? 'HH:mm' : 'yyyy-MM-dd');
      o[c] = v;
    });
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
    var plazas = Math.max(1, Math.min(20, parseInt(d.plazas, 10) || 1));
    var nombre = String(d.nombre || '').slice(0, 80).trim();
    var tel = String(d.telefono || '').replace(/[^\d+ ]/g, '').slice(0, 20).trim();
    if (!nombre || tel.replace(/\D/g, '').length < 9) return json_({ ok: false, error: 'Revisa el nombre y el teléfono.' });

    var salida = leerSalidas_().filter(function (o) { return String(o.id) === String(d.id); })[0];
    if (!salida) return json_({ ok: false, error: 'Esta fecha ya no está disponible.' });

    var max = Number(salida.plazas_max) || 0, res = Number(salida.plazas_reservadas) || 0, libres = max - res;
    if (plazas > libres) return json_({ ok: false, error: libres > 0 ? 'Solo quedan ' + libres + ' plazas.' : 'Esta fecha está completa.', libres: Math.max(0, libres) });

    var ss = SpreadsheetApp.getActiveSpreadsheet(), sh = ss.getSheetByName(HOJA_CAL);
    var col = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0].map(String).indexOf('plazas_reservadas') + 1;
    sh.getRange(salida._fila, col).setValue(res + plazas);
    ss.getSheetByName(HOJA_RES).appendRow([new Date(), salida.id, salida.titulo, salida.fecha, plazas, nombre, tel, 'Pendiente de confirmar']);

    // Aviso por email (opcional). Cambia la dirección o borra estas líneas si no lo quieres.
    try {
      MailApp.sendEmail('guiasadastra@gmail.com', 'Nueva reserva: ' + salida.titulo + ' (' + salida.fecha + ')',
        nombre + ' (' + tel + ') ha reservado ' + plazas + ' plaza(s).\nQuedan ' + (libres - plazas) + ' de ' + max + '.');
    } catch (err) {}

    return json_({ ok: true, libres: libres - plazas });
  } finally {
    lock.releaseLock();
  }
}
