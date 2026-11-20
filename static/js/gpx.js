/* Guías Ad Astra · Editor de tracks GPX: unir, dividir, recortar, invertir, corregir errores del GPS y exportar.
   Todo se hace en el navegador: los archivos no salen del ordenador de quien lo usa. */
(function () {
  "use strict";
  var app = document.getElementById("gx-app");
  if (!app) return;
  var COLORES = ["#e9a53b", "#4fb3e8", "#e8574a", "#7cc47f", "#c78bf0", "#f07ab8", "#f5e15b", "#5fd3c4"];
  var R = Math.PI / 180;

  /* ---------------------------------------------------------------- utilidades */
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function hav(a, b) {
    var dLat = (b.lat - a.lat) * R, dLon = (b.lon - a.lon) * R;
    var x = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(a.lat * R) * Math.cos(b.lat * R) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    return 2 * 6371000 * Math.asin(Math.min(1, Math.sqrt(x)));
  }
  function km(m) { return (m / 1000).toLocaleString("es-ES", { maximumFractionDigits: m < 10000 ? 2 : 1 }); }
  function ent(n) { return Math.round(n).toLocaleString("es-ES"); }
  function dur(ms) {
    if (!isFinite(ms) || ms <= 0) return "–";
    var m = Math.round(ms / 60000), h = Math.floor(m / 60);
    return h ? h + " h " + String(m % 60).padStart(2, "0") + " min" : m + " min";
  }
  function copia(p) { return { lat: p.lat, lon: p.lon, ele: p.ele, t: p.t }; }
  function clonar(trs) { return trs.map(function (t) { return { id: t.id, name: t.name, color: t.color, vis: t.vis, marcado: t.marcado, pts: t.pts.map(copia) }; }); }
  var sigId = 1;
  function nuevoTrack(name, pts, color) {
    return { id: sigId++, name: name || "Track", color: color || COLORES[(sigId - 2) % COLORES.length], vis: true, marcado: false, pts: pts };
  }

  /* ---------------------------------------------------------------- lectura de archivos */
  function leerArchivo(text, nombre) {
    var doc = new DOMParser().parseFromString(text, "application/xml");
    if (doc.getElementsByTagName("parsererror").length) throw new Error(nombre + ": no es un GPX, KML o TCX válido.");
    var salida = [], base = nombre.replace(/\.[^.]+$/, "");
    function hijo(n, tag) { var x = n.getElementsByTagName(tag)[0]; return x ? x.textContent : null; }
    function punto(n) {
      var e = hijo(n, "ele"), t = hijo(n, "time");
      return { lat: +n.getAttribute("lat"), lon: +n.getAttribute("lon"), ele: e != null ? parseFloat(e) : NaN, t: t ? Date.parse(t) : NaN };
    }
    var trks = doc.getElementsByTagName("trk");
    for (var i = 0; i < trks.length; i++) {
      var nm = trks[i].getElementsByTagName("name")[0], segs = trks[i].getElementsByTagName("trkseg");
      for (var s = 0; s < segs.length; s++) {
        var pts = Array.prototype.map.call(segs[s].getElementsByTagName("trkpt"), punto);
        if (pts.length > 1) salida.push({ name: (nm ? nm.textContent.trim() : base) + (segs.length > 1 ? " (" + (s + 1) + ")" : ""), pts: pts });
      }
    }
    var rtes = doc.getElementsByTagName("rte");
    for (var r = 0; r < rtes.length; r++) {
      var rp = Array.prototype.map.call(rtes[r].getElementsByTagName("rtept"), punto), rn = rtes[r].getElementsByTagName("name")[0];
      if (rp.length > 1) salida.push({ name: rn ? rn.textContent.trim() : base + " (ruta)", pts: rp });
    }
    if (!salida.length) {
      var tp = doc.getElementsByTagName("Trackpoint"), tcx = [];
      for (var j = 0; j < tp.length; j++) {
        var la = hijo(tp[j], "LatitudeDegrees"), lo = hijo(tp[j], "LongitudeDegrees");
        if (la == null || lo == null) continue;
        var al = hijo(tp[j], "AltitudeMeters"), ti = hijo(tp[j], "Time");
        tcx.push({ lat: +la, lon: +lo, ele: al != null ? parseFloat(al) : NaN, t: ti ? Date.parse(ti) : NaN });
      }
      if (tcx.length > 1) salida.push({ name: base, pts: tcx });
      var coords = doc.getElementsByTagName("coordinates");
      for (var k = 0; k < coords.length; k++) {
        var kp = [];
        coords[k].textContent.trim().split(/\s+/).forEach(function (c) {
          var v = c.split(","); if (v.length >= 2) kp.push({ lat: +v[1], lon: +v[0], ele: v[2] != null ? parseFloat(v[2]) : NaN, t: NaN });
        });
        if (kp.length > 1) salida.push({ name: base + (coords.length > 1 ? " (" + (k + 1) + ")" : ""), pts: kp });
      }
    }
    salida.forEach(function (x) { x.pts = x.pts.filter(function (p) { return isFinite(p.lat) && isFinite(p.lon); }); });
    salida = salida.filter(function (x) { return x.pts.length > 1; });
    if (!salida.length) throw new Error(nombre + ": no hemos encontrado ningún track ni ruta.");
    var wp = Array.prototype.map.call(doc.getElementsByTagName("wpt"), function (n) { var p = punto(n); p.name = (hijo(n, "name") || "").trim(); return p; });
    return { tracks: salida, wpts: wp };
  }

  /* ---------------------------------------------------------------- cálculos */
  function eleSuave(p, dist) {
    var ele = p.map(function (x) { return x.ele; }), ok = ele.some(isFinite);
    if (!ok) return null;
    var last = ele.find(isFinite);
    for (var a = 0; a < ele.length; a++) { if (isFinite(ele[a])) last = ele[a]; else ele[a] = last; }
    var sm = ele.slice();
    for (var b = 0, lo = 0, hi = 0, sum = 0; b < ele.length; b++) {
      while (hi < ele.length && dist[hi] - dist[b] <= 30) { sum += ele[hi]; hi++; }
      while (dist[b] - dist[lo] > 30) { sum -= ele[lo]; lo++; }
      sm[b] = sum / (hi - lo);
    }
    return sm;
  }
  function stats(tr) {
    var p = tr.pts, d = [0];
    for (var i = 1; i < p.length; i++) d.push(d[i - 1] + hav(p[i - 1], p[i]));
    var sm = eleSuave(p, d), up = 0, dn = 0, emin = null, emax = null;
    if (sm) {
      var ref = sm[0];
      for (var j = 1; j < sm.length; j++) {
        var dd = sm[j] - ref;
        if (dd >= 3) { up += dd; ref = sm[j]; } else if (dd <= -3) { dn -= dd; ref = sm[j]; }
      }
      sm.forEach(function (v) { emin = emin == null ? v : Math.min(emin, v); emax = emax == null ? v : Math.max(emax, v); });
    }
    var t0 = p[0].t, t1 = p[p.length - 1].t, mov = 0;
    if (isFinite(t0) && isFinite(t1)) {
      for (var k = 1; k < p.length; k++) {
        var dt = p[k].t - p[k - 1].t;
        if (dt > 0 && hav(p[k - 1], p[k]) / (dt / 1000) > 0.25) mov += dt;  // > 0,9 km/h: en marcha
      }
    }
    return { dist: d, total: d[d.length - 1], up: up, dn: dn, sm: sm, emin: emin, emax: emax, tiempo: isFinite(t0) && isFinite(t1) ? t1 - t0 : NaN, mov: mov };
  }

  /* corrección automática: devuelve el track corregido y lo que ha quitado */
  function corregir(pts, o) {
    var tieneT = pts.length > 2 && isFinite(pts[0].t) && isFinite(pts[pts.length - 1].t);
    var info = { saltos: [], paradas: 0, enParadas: 0, simpl: 0, antes: pts.length };
    var p = pts.map(copia);
    // 1. saltos del GPS: puntos a los que habría que llegar a una velocidad imposible, o picos de ida y vuelta
    if (o.saltos) {
      var vmax = o.vmax / 3.6, out = [p[0]];
      // el primer punto suele ser el peor (el GPS aún no tenía buena señal)
      if (p.length > 3 && tieneT) {
        var v01 = hav(p[0], p[1]) / Math.max(1, (p[1].t - p[0].t) / 1000), v12 = hav(p[1], p[2]) / Math.max(1, (p[2].t - p[1].t) / 1000);
        if (v01 > vmax && v12 <= vmax) { info.saltos.push(p[0]); out = [p[1]]; p = p.slice(1); }
      }
      for (var i = 1; i < p.length; i++) {
        var a = out[out.length - 1], b = p[i], c = p[i + 1], quitar = false;
        var dab = hav(a, b);
        if (tieneT && isFinite(a.t) && isFinite(b.t)) {
          var dt = (b.t - a.t) / 1000;
          if (dt <= 0 ? dab > 15 : dab / dt > vmax) quitar = true;
        }
        if (!quitar && c) {  // pico: se va y vuelve al mismo sitio
          var dbc = hav(b, c), dac = hav(a, c);
          if (dab > o.pico && dbc > o.pico && dab + dbc > 4 * dac + 2 * o.pico) quitar = true;
        }
        if (quitar && c) info.saltos.push(b); else out.push(b);
      }
      p = out;
    }
    // 2. paradas: puntos que bailan alrededor del mismo sitio
    if (o.paradas) {
      var res = [], n = 0;
      while (n < p.length) {
        var m = n + 1;
        while (m < p.length && hav(p[n], p[m]) <= o.radio) m++;
        var cnt = m - n, largo = false;
        if (cnt >= 3) {
          if (tieneT && isFinite(p[n].t) && isFinite(p[m - 1].t)) largo = (p[m - 1].t - p[n].t) >= o.tmin * 1000;
          else {  // sin horas: muchos puntos que dan vueltas sin avanzar
            var rec = 0; for (var q = n + 1; q < m; q++) rec += hav(p[q - 1], p[q]);
            largo = cnt >= 8 && rec > 3 * o.radio;
          }
        }
        if (largo && cnt > 2) {
          var lat = 0, lon = 0, es = [];
          for (var z = n; z < m; z++) { lat += p[z].lat; lon += p[z].lon; if (isFinite(p[z].ele)) es.push(p[z].ele); }
          es.sort(function (x, y) { return x - y; });
          var cen = { lat: lat / cnt, lon: lon / cnt, ele: es.length ? es[es.length >> 1] : NaN, t: p[n].t };
          res.push(cen);
          if (tieneT) res.push({ lat: cen.lat, lon: cen.lon, ele: cen.ele, t: p[m - 1].t });  // conserva la duración de la parada
          info.paradas++; info.enParadas += cnt - (tieneT ? 2 : 1);
          n = m;
        } else { res.push(p[n]); n++; }
      }
      p = res;
    }
    // 3. simplificar (Douglas-Peucker en metros)
    if (o.simplificar && p.length > 2) {
      var lat0 = p[0].lat * R, kx = 6371000 * Math.cos(lat0) * R, ky = 6371000 * R;
      var X = p.map(function (x) { return x.lon * kx; }), Y = p.map(function (x) { return x.lat * ky; });
      var keep = new Uint8Array(p.length); keep[0] = keep[p.length - 1] = 1;
      var pila = [[0, p.length - 1]], tol = o.tol;
      while (pila.length) {
        var s = pila.pop(), i0 = s[0], i1 = s[1], dx = X[i1] - X[i0], dy = Y[i1] - Y[i0], L = Math.hypot(dx, dy) || 1e-9, dm = 0, im = -1;
        for (var w = i0 + 1; w < i1; w++) {
          var dist = Math.abs(dy * (X[w] - X[i0]) - dx * (Y[w] - Y[i0])) / L;
          if (dist > dm) { dm = dist; im = w; }
        }
        if (dm > tol) { keep[im] = 1; pila.push([i0, im], [im, i1]); }
      }
      var antes = p.length;
      p = p.filter(function (_, k) { return keep[k]; });
      info.simpl = antes - p.length;
    }
    // 4. suavizar la altitud
    if (o.altitud) {
      var dd = [0]; for (var u = 1; u < p.length; u++) dd.push(dd[u - 1] + hav(p[u - 1], p[u]));
      var sm = eleSuave(p, dd);
      if (sm) p.forEach(function (x, k) { x.ele = Math.round(sm[k] * 10) / 10; });
    }
    info.despues = p.length;
    return { pts: p, info: info };
  }

  /* ---------------------------------------------------------------- exportar */
  function gpxTexto(trs, wpts, nombre) {
    function f(n, d) { return Number(n).toFixed(d); }
    function pt(tag, p, extra) {
      return "<" + tag + ' lat="' + f(p.lat, 7) + '" lon="' + f(p.lon, 7) + '">' + (isFinite(p.ele) ? "<ele>" + f(p.ele, 1) + "</ele>" : "") +
        (isFinite(p.t) ? "<time>" + new Date(p.t).toISOString().replace(/\.000Z$/, "Z") + "</time>" : "") + (extra || "") + "</" + tag + ">";
    }
    var x = '<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.1" creator="Guías Ad Astra · Editor GPX (guiasadastra.com)" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n' +
      "<metadata><name>" + esc(nombre) + "</name><time>" + new Date().toISOString().replace(/\.\d+Z$/, "Z") + "</time></metadata>\n";
    (wpts || []).forEach(function (w) { x += pt("wpt", w, w.name ? "<name>" + esc(w.name) + "</name>" : "") + "\n"; });
    trs.forEach(function (t) {
      x += "<trk><name>" + esc(t.name) + "</name><trkseg>\n" + t.pts.map(function (p) { return pt("trkpt", p); }).join("\n") + "\n</trkseg></trk>\n";
    });
    return x + "</gpx>\n";
  }
  function descargar(texto, nombre) {
    var b = new Blob([texto], { type: "application/gpx+xml" }), a = document.createElement("a");
    a.href = URL.createObjectURL(b); a.download = nombre.replace(/[\\/:*?"<>|]+/g, "-").slice(0, 80) + ".gpx";
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  /* ---------------------------------------------------------------- estado */
  var tracks = [], wpts = [], selId = null, modo = null, marca = [], prev = null, puntoSel = null;
  var hist = [], rehacer = [];
  function guardar() {
    hist.push({ t: clonar(tracks), sel: selId });
    if (hist.length > 40) hist.shift();
    rehacer = [];
  }
  function sel() { return tracks.filter(function (t) { return t.id === selId; })[0] || null; }

  /* ---------------------------------------------------------------- interfaz */
  app.innerHTML =
    '<div class="gx-bar"><label class="btn btn-primary gx-abrir">Abrir GPX, KML o TCX<input type="file" id="gx-file" accept=".gpx,.kml,.tcx,application/gpx+xml" multiple hidden></label>' +
    '<button type="button" class="btn btn-ghost" id="gx-demo">Probar con un ejemplo</button>' +
    '<span class="gx-sep"></span><button type="button" class="gx-ib" id="gx-undo" title="Deshacer (Ctrl+Z)" disabled>↶ Deshacer</button><button type="button" class="gx-ib" id="gx-redo" title="Rehacer (Ctrl+Y)" disabled>↷ Rehacer</button>' +
    '<span class="gx-sep"></span><button type="button" class="btn btn-primary" id="gx-save" disabled>Descargar GPX</button></div>' +
    '<p class="gx-priv">Tus archivos no se suben a ningún servidor: todo se procesa en tu navegador.</p>' +
    '<div class="gx-main"><aside class="gx-panel"><div id="gx-lista"></div><div id="gx-tools"></div></aside>' +
    '<div class="gx-der"><div class="gx-mapa" id="gx-mapa"><div class="gx-drop" id="gx-drop"><b>Arrastra aquí tus archivos GPX</b><span>o pulsa «Abrir GPX»</span></div></div><div id="gx-modo"></div><div class="gx-perfil" id="gx-perfil"></div></div></div>';
  var $ = function (id) { return document.getElementById(id); };
  var lista = $("gx-lista"), tools = $("gx-tools"), perfilEl = $("gx-perfil"), modoEl = $("gx-modo");

  /* mapa */
  var map = L.map("gx-mapa", { preferCanvas: true, zoomControl: true }).setView([40.3, -5.2], 9);
  var ign = "https://www.ign.es/wmts/{c}?service=WMTS&request=GetTile&version=1.0.0&Format=image/{f}&layer={l}&style=default&tilematrixset=GoogleMapsCompatible&TileMatrix={z}&TileRow={y}&TileCol={x}";
  var capas = {
    "Topográfico": L.tileLayer("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", { maxZoom: 17, subdomains: "abc", attribution: '&copy; <a href="https://opentopomap.org">OpenTopoMap</a> · &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' }),
    "Mapa IGN": L.tileLayer(ign.replace("{c}", "mapa-raster").replace("{f}", "jpeg").replace("{l}", "MTN"), { maxZoom: 20, attribution: '&copy; <a href="https://www.ign.es">Instituto Geográfico Nacional</a>' }),
    "Ortofoto PNOA": L.tileLayer(ign.replace("{c}", "pnoa-ma").replace("{f}", "jpeg").replace("{l}", "OI.OrthoimageCoverage"), { maxZoom: 20, attribution: 'PNOA &copy; <a href="https://www.ign.es">Instituto Geográfico Nacional</a>' }),
    "OpenStreetMap": L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' })
  };
  capas["Topográfico"].addTo(map);
  L.control.layers(capas, null, { position: "topright" }).addTo(map);
  L.control.scale({ imperial: false }).addTo(map);
  var capaTr = L.layerGroup().addTo(map), capaExtra = L.layerGroup().addTo(map), capaWp = L.layerGroup().addTo(map);
  var cursor = L.circleMarker([0, 0], { radius: 6, color: "#fff", weight: 2, fillColor: "#e8574a", fillOpacity: 1, interactive: false });

  function dibujar() {
    capaTr.clearLayers(); capaWp.clearLayers();
    tracks.forEach(function (t) {
      if (!t.vis) return;
      var ll = t.pts.map(function (p) { return [p.lat, p.lon]; });
      if (t.id === selId) L.polyline(ll, { color: "#000", weight: 7, opacity: 0.45, interactive: false }).addTo(capaTr);
      var pl = L.polyline(ll, { color: t.color, weight: t.id === selId ? 4.5 : 3, opacity: t.id === selId ? 1 : 0.8 }).addTo(capaTr);
      pl.on("click", function (e) { if (!modo && t.id !== selId) { L.DomEvent.stop(e); seleccionar(t.id); } });
      L.circleMarker(ll[0], { radius: 5, color: "#fff", weight: 2, fillColor: "#3fae5a", fillOpacity: 1, interactive: false }).addTo(capaTr);
      L.circleMarker(ll[ll.length - 1], { radius: 5, color: "#fff", weight: 2, fillColor: "#d9372b", fillOpacity: 1, interactive: false }).addTo(capaTr);
    });
    wpts.forEach(function (w) { L.circleMarker([w.lat, w.lon], { radius: 4, color: "#1b120c", weight: 1, fillColor: "#fff", fillOpacity: 1 }).bindTooltip(esc(w.name || "Punto")).addTo(capaWp); });
    dibujarExtra();
  }
  function encuadrar(t) {
    var ll = [];
    (t ? [t] : tracks.filter(function (x) { return x.vis; })).forEach(function (x) { x.pts.forEach(function (p) { ll.push([p.lat, p.lon]); }); });
    if (ll.length) map.fitBounds(L.latLngBounds(ll), { padding: [30, 30], maxZoom: 16 });
  }

  /* lista de tracks */
  function pintarLista() {
    if (!tracks.length) { lista.innerHTML = '<p class="gx-vacio">Abre uno o varios archivos para empezar. Puedes abrir varios a la vez para unirlos.</p>'; return; }
    var h = '<h3 class="gx-h">Tracks <small>(' + tracks.length + ")</small></h3><ul class=\"gx-tracks\">";
    tracks.forEach(function (t, i) {
      var s = stats(t);
      h += '<li class="gx-tr' + (t.id === selId ? " on" : "") + '" data-id="' + t.id + '"><div class="gx-tr1"><input type="checkbox" class="gx-chk" title="Marcar para unir o descargar"' + (t.marcado ? " checked" : "") + '>' +
        '<input type="color" class="gx-col" value="' + t.color + '" title="Color"><input class="gx-nom" value="' + esc(t.name) + '" aria-label="Nombre del track"></div>' +
        '<div class="gx-st">' + km(s.total) + " km · +" + ent(s.up) + " / −" + ent(s.dn) + " m · " + ent(t.pts.length) + " puntos" + (isFinite(s.tiempo) ? " · " + dur(s.tiempo) : "") + "</div>" +
        '<div class="gx-acc"><button type="button" data-a="ver" title="' + (t.vis ? "Ocultar" : "Mostrar") + '">' + (t.vis ? "👁" : "◌") + '</button><button type="button" data-a="zoom" title="Ver en el mapa">⤢</button>' +
        '<button type="button" data-a="sube" title="Subir"' + (i ? "" : " disabled") + '>▲</button><button type="button" data-a="baja" title="Bajar"' + (i < tracks.length - 1 ? "" : " disabled") + '>▼</button>' +
        '<button type="button" data-a="inv" title="Invertir el sentido">⇄</button><button type="button" data-a="dup" title="Duplicar">⧉</button><button type="button" data-a="gpx" title="Descargar este track">⬇</button><button type="button" data-a="del" title="Borrar">🗑</button></div></li>';
    });
    h += "</ul>";
    var marcados = tracks.filter(function (t) { return t.marcado; });
    h += '<div class="gx-unir"><button type="button" class="btn btn-ghost" id="gx-join"' + (marcados.length < 2 ? " disabled" : "") + '>Unir los marcados (' + marcados.length + ")</button>" +
      '<label class="gx-op"><input type="checkbox" id="gx-orient" checked> Girar los tracks que estén al revés</label></div>';
    lista.innerHTML = h;
  }
  lista.addEventListener("click", function (e) {
    var li = e.target.closest(".gx-tr"); if (!li) return;
    var id = +li.getAttribute("data-id"), t = tracks.filter(function (x) { return x.id === id; })[0], i = tracks.indexOf(t);
    var b = e.target.closest("[data-a]");
    if (!b) { if (!e.target.closest("input")) seleccionar(id); return; }
    var a = b.getAttribute("data-a");
    if (a === "ver") { t.vis = !t.vis; refrescar(); return; }
    if (a === "zoom") { encuadrar(t); return; }
    if (a === "gpx") { descargar(gpxTexto([t], [], t.name), t.name); return; }
    guardar();
    if (a === "sube" && i > 0) { tracks.splice(i, 1); tracks.splice(i - 1, 0, t); }
    if (a === "baja" && i < tracks.length - 1) { tracks.splice(i, 1); tracks.splice(i + 1, 0, t); }
    if (a === "inv") { t.pts.reverse(); if (isFinite(t.pts[0].t)) avisar("Invertido. Las horas del track quedan en orden inverso: muchas apps las ignoran, pero si te molesta puedes quitarlas con «Quitar las horas»."); }
    if (a === "dup") { var c = nuevoTrack(t.name + " (copia)", t.pts.map(copia)); tracks.splice(i + 1, 0, c); }
    if (a === "del") { tracks.splice(i, 1); if (selId === id) selId = tracks.length ? tracks[Math.max(0, i - 1)].id : null; }
    refrescar();
  });
  lista.addEventListener("change", function (e) {
    var li = e.target.closest(".gx-tr"); if (!li) { return; }
    var t = tracks.filter(function (x) { return x.id === +li.getAttribute("data-id"); })[0];
    if (e.target.classList.contains("gx-chk")) { t.marcado = e.target.checked; pintarLista(); }
    else if (e.target.classList.contains("gx-col")) { guardar(); t.color = e.target.value; dibujar(); pintarPerfil(); }
    else if (e.target.classList.contains("gx-nom")) { guardar(); t.name = e.target.value.trim() || "Track"; }
  });
  lista.addEventListener("click", function (e) {
    if (e.target.id !== "gx-join") return;
    var ms = tracks.filter(function (t) { return t.marcado; });
    if (ms.length < 2) return;
    guardar();
    var orient = $("gx-orient").checked, pts = ms[0].pts.map(copia);
    if (orient && ms.length > 1) {  // el primero se orienta hacia el segundo
      var a0 = pts[0], a1 = pts[pts.length - 1], b = ms[1].pts;
      if (Math.min(hav(a0, b[0]), hav(a0, b[b.length - 1])) < Math.min(hav(a1, b[0]), hav(a1, b[b.length - 1]))) pts.reverse();
    }
    ms.slice(1).forEach(function (t) {
      var q = t.pts.map(copia), fin = pts[pts.length - 1];
      if (orient && hav(fin, q[q.length - 1]) < hav(fin, q[0])) q.reverse();
      if (hav(fin, q[0]) < 1) q.shift();
      pts = pts.concat(q);
    });
    var bases = ms.map(function (t) { return t.name.replace(/ \((\d+|copia)\)$/, ""); });
    var nombre = bases.every(function (x) { return x === bases[0]; }) ? bases[0] : bases.join(" + ").slice(0, 90);
    var nuevo = nuevoTrack(nombre, pts, ms[0].color);
    var pos = tracks.indexOf(ms[0]);
    tracks = tracks.filter(function (t) { return !t.marcado; });
    tracks.splice(Math.min(pos, tracks.length), 0, nuevo);
    selId = nuevo.id;
    avisar("Unidos " + ms.length + " tracks en uno. Los originales se han quitado (puedes deshacer).");
    refrescar();
  });

  /* herramientas del track seleccionado */
  var opc = { saltos: true, vmax: 15, pico: 25, paradas: true, radio: 20, tmin: 60, simplificar: false, tol: 3, altitud: false };
  var ACT = { pie: { n: "A pie", v: 15 }, bici: { n: "Bici", v: 80 }, esqui: { n: "Esquí", v: 100 }, coche: { n: "Coche o moto", v: 200 } };
  function pintarTools() {
    var t = sel();
    if (!t) { tools.innerHTML = ""; return; }
    var tieneT = isFinite(t.pts[0].t);
    tools.innerHTML =
      '<h3 class="gx-h">Editar «' + esc(t.name) + '»</h3><div class="gx-btns">' +
      '<button type="button" class="gx-tb' + (modo === "dividir" ? " on" : "") + '" data-m="dividir"><b>✂ Dividir</b><span>en un punto</span></button>' +
      '<button type="button" class="gx-tb' + (modo === "tramo" ? " on" : "") + '" data-m="tramo"><b>⌫ Tramo</b><span>quitar o recortar</span></button>' +
      '<button type="button" class="gx-tb' + (modo === "punto" ? " on" : "") + '" data-m="punto"><b>✥ Puntos</b><span>mover o borrar</span></button></div>' +
      '<details class="gx-corr" open><summary>Corrección automática</summary>' +
      '<label class="gx-op"><input type="checkbox" data-o="saltos"' + (opc.saltos ? " checked" : "") + '> Quitar saltos y picos del GPS</label>' +
      '<div class="gx-fila"><label>Actividad <select id="gx-act">' + Object.keys(ACT).map(function (k) { return '<option value="' + k + '"' + (ACT[k].v === opc.vmax ? " selected" : "") + ">" + ACT[k].n + "</option>"; }).join("") + '</select></label>' +
      '<label>Vel. máx. <input type="number" data-o="vmax" value="' + opc.vmax + '" min="3" max="400" step="1"> km/h</label></div>' +
      '<label class="gx-op"><input type="checkbox" data-o="paradas"' + (opc.paradas ? " checked" : "") + '> Limpiar las paradas (el GPS «baila» en el sitio)</label>' +
      '<div class="gx-fila"><label>Radio <input type="number" data-o="radio" value="' + opc.radio + '" min="3" max="100"> m</label>' + (tieneT ? '<label>Mínimo <input type="number" data-o="tmin" value="' + opc.tmin + '" min="10" max="3600" step="10"> s</label>' : "") + "</div>" +
      '<label class="gx-op"><input type="checkbox" data-o="simplificar"' + (opc.simplificar ? " checked" : "") + '> Simplificar (menos puntos, misma forma)</label>' +
      '<div class="gx-fila"><label>Tolerancia <input type="number" data-o="tol" value="' + opc.tol + '" min="0.5" max="50" step="0.5"> m</label></div>' +
      '<label class="gx-op"><input type="checkbox" data-o="altitud"' + (opc.altitud ? " checked" : "") + '> Suavizar la altitud</label>' +
      '<div class="gx-fila"><button type="button" class="btn btn-ghost" id="gx-ver">Ver qué se quita</button><button type="button" class="btn btn-primary" id="gx-apl">Aplicar</button></div><div id="gx-res"></div></details>' +
      '<details class="gx-corr"><summary>Más opciones</summary><div class="gx-fila gx-wrap">' +
      '<button type="button" class="gx-ib" id="gx-notime"' + (tieneT ? "" : " disabled") + '>Quitar las horas</button>' +
      '<button type="button" class="gx-ib" id="gx-noele">Quitar la altitud</button>' +
      '<button type="button" class="gx-ib" id="gx-cerrar">Cerrar el circuito</button>' +
      '<a class="gx-ib" href="/video-ruta-3d/" id="gx-video">Hacer vídeo 3D ▶</a></div></details>';
  }
  tools.addEventListener("click", function (e) {
    var b = e.target.closest("[data-m]");
    if (b) { cambiarModo(modo === b.getAttribute("data-m") ? null : b.getAttribute("data-m")); return; }
    var t = sel(); if (!t) return;
    if (e.target.id === "gx-ver") { previsualizar(); return; }
    if (e.target.id === "gx-apl") {
      var r = corregir(t.pts, opc);
      if (r.pts.length < 2) { avisar("La corrección dejaría el track sin puntos: revisa los valores."); return; }
      guardar(); t.pts = r.pts; prev = null;
      $("gx-res").innerHTML = resumen(r.info, true);
      refrescar(true); return;
    }
    if (e.target.id === "gx-notime") { guardar(); t.pts.forEach(function (p) { p.t = NaN; }); refrescar(); avisar("Horas quitadas."); }
    if (e.target.id === "gx-noele") { guardar(); t.pts.forEach(function (p) { p.ele = NaN; }); refrescar(); avisar("Altitud quitada."); }
    if (e.target.id === "gx-cerrar") { guardar(); var f = t.pts[0]; t.pts.push({ lat: f.lat, lon: f.lon, ele: f.ele, t: NaN }); refrescar(); avisar("Añadido un punto final igual al de salida."); }
    if (e.target.id === "gx-video") { try { sessionStorage.setItem("gx-video", gpxTexto([t], [], t.name)); } catch (er) {} }
  });
  tools.addEventListener("change", function (e) {
    var k = e.target.getAttribute("data-o");
    if (e.target.id === "gx-act") { opc.vmax = ACT[e.target.value].v; pintarTools(); }
    else if (k) { opc[k] = e.target.type === "checkbox" ? e.target.checked : +e.target.value; }
    if (prev) previsualizar();
  });
  function resumen(i, hecho) {
    var partes = [];
    if (opc.saltos) partes.push("<b>" + i.saltos.length + "</b> saltos o picos del GPS");
    if (opc.paradas) partes.push("<b>" + i.paradas + "</b> paradas (" + i.enParadas + " puntos)");
    if (opc.simplificar) partes.push("<b>" + i.simpl + "</b> puntos sobrantes al simplificar");
    return '<p class="gx-ok">' + (hecho ? "Hecho: " : "Se quitarían ") + (partes.join(", ") || "nada") + ". Puntos: " + ent(i.antes) + " → " + ent(i.despues) + "." + (hecho ? " Puedes deshacerlo." : "") + "</p>";
  }
  function previsualizar() {
    var t = sel(); if (!t) return;
    var r = corregir(t.pts, opc);
    prev = { pts: r.pts, saltos: r.info.saltos };
    $("gx-res").innerHTML = resumen(r.info, false) + '<p class="gx-ley"><i style="background:#e8574a"></i>saltos que se quitan <i style="background:#fff;border:2px solid #4fb3e8"></i>track corregido</p>';
    dibujarExtra();
  }

  /* modos de edición sobre el mapa */
  function cambiarModo(m) {
    modo = m; marca = []; puntoSel = null; prev = null;
    map.getContainer().classList.toggle("gx-cruz", !!m);
    pintarTools(); pintarModo(); dibujarExtra();
  }
  function pintarModo() {
    var t = sel();
    if (!modo || !t) { modoEl.innerHTML = ""; return; }
    var h = '<div class="gx-aviso">';
    if (modo === "dividir") {
      h += marca.length ? "Cortar en el punto " + ent(marca[0] + 1) + " de " + ent(t.pts.length) + '. <button type="button" class="btn btn-primary" data-x="cortar">Dividir aquí</button>' : "Pulsa sobre el track en el punto donde quieres dividirlo.";
    } else if (modo === "tramo") {
      if (marca.length < 2) h += marca.length ? "Ahora pulsa el final del tramo." : "Pulsa el inicio del tramo sobre el track.";
      else {
        var a = Math.min(marca[0], marca[1]), b = Math.max(marca[0], marca[1]), s = 0;
        for (var i = a + 1; i <= b; i++) s += hav(t.pts[i - 1], t.pts[i]);
        h += "Tramo de " + km(s) + " km (" + ent(b - a + 1) + ' puntos). <button type="button" class="btn btn-primary" data-x="quitar">Quitar y unir los extremos</button><button type="button" class="btn btn-ghost" data-x="separar">Quitar y dejar dos tracks</button><button type="button" class="btn btn-ghost" data-x="solo">Quedarme solo con este tramo</button>';
      }
    } else if (modo === "punto") {
      h += puntoSel != null ? "Punto " + ent(puntoSel + 1) + ': arrástralo para moverlo. <button type="button" class="btn btn-ghost" data-x="borrapt">Borrar este punto</button>' : "Pulsa sobre el track para elegir un punto. Luego puedes arrastrarlo o borrarlo (tecla Supr).";
    }
    modoEl.innerHTML = h + ' <button type="button" class="gx-ib" data-x="salir">Terminar</button></div>';
  }
  modoEl.addEventListener("click", function (e) {
    var x = e.target.getAttribute("data-x"), t = sel(); if (!x || !t) return;
    if (x === "salir") { cambiarModo(null); return; }
    guardar();
    var i = tracks.indexOf(t);
    if (x === "cortar") {
      var k = marca[0];
      if (k <= 0 || k >= t.pts.length - 1) { hist.pop(); avisar("Elige un punto que no sea el primero ni el último."); return; }
      var b = nuevoTrack(t.name + " (2)", t.pts.slice(k).map(copia));
      t.pts = t.pts.slice(0, k + 1); t.name = t.name + " (1)";
      tracks.splice(i + 1, 0, b);
      avisar("Dividido en dos tracks.");
    }
    if (x === "quitar" || x === "separar" || x === "solo") {
      var a0 = Math.min(marca[0], marca[1]), b0 = Math.max(marca[0], marca[1]);
      if (x === "solo") t.pts = t.pts.slice(a0, b0 + 1);
      else {
        var ini = t.pts.slice(0, a0 + 1), fin = t.pts.slice(b0);
        if (x === "quitar") t.pts = ini.concat(fin.slice(ini.length && fin.length && ini[ini.length - 1] === fin[0] ? 1 : 0));
        else {
          if (ini.length < 2 || fin.length < 2) { t.pts = ini.length >= 2 ? ini : fin; }
          else { t.pts = ini; tracks.splice(i + 1, 0, nuevoTrack(t.name + " (2)", fin.map(copia))); }
        }
      }
      if (t.pts.length < 2) { tracks.splice(tracks.indexOf(t), 1); selId = tracks.length ? tracks[0].id : null; }
    }
    if (x === "borrapt") { borrarPunto(); return; }
    cambiarModo(null); refrescar();
  });
  function borrarPunto() {
    var t = sel(); if (!t || puntoSel == null) return;
    if (t.pts.length <= 2) { avisar("Un track necesita al menos dos puntos."); return; }
    t.pts.splice(puntoSel, 1);
    puntoSel = Math.min(puntoSel, t.pts.length - 1);
    refrescar(true); pintarModo(); dibujarExtra();
  }
  document.addEventListener("keydown", function (e) {
    if (e.target.matches("input,select,textarea")) return;
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z") { e.preventDefault(); deshacer(); }
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "y") { e.preventDefault(); hacerOtraVez(); }
    if ((e.key === "Delete" || e.key === "Backspace") && modo === "punto" && puntoSel != null) { e.preventDefault(); guardar(); borrarPunto(); }
    if (e.key === "Escape" && modo) cambiarModo(null);
  });
  function cercano(t, ll) {
    var best = -1, bd = Infinity, p = { lat: ll.lat, lon: ll.lng };
    for (var i = 0; i < t.pts.length; i++) { var d = hav(p, t.pts[i]); if (d < bd) { bd = d; best = i; } }
    var px = map.latLngToContainerPoint([t.pts[best].lat, t.pts[best].lon]).distanceTo(map.latLngToContainerPoint(ll));
    return px <= 24 ? best : -1;
  }
  map.on("click", function (e) {
    var t = sel(); if (!modo || !t) return;
    var k = cercano(t, e.latlng);
    if (k < 0) { avisar("Pulsa más cerca del track seleccionado."); return; }
    if (modo === "dividir") marca = [k];
    else if (modo === "tramo") marca = marca.length >= 2 ? [k] : marca.concat([k]);
    else if (modo === "punto") puntoSel = k;
    pintarModo(); dibujarExtra(); pintarPerfil();
  });
  function dibujarExtra() {
    capaExtra.clearLayers();
    var t = sel(); if (!t) return;
    if (prev) {
      L.polyline(prev.pts.map(function (p) { return [p.lat, p.lon]; }), { color: "#fff", weight: 2, dashArray: "5 5", interactive: false }).addTo(capaExtra);
      prev.saltos.forEach(function (p) { L.circleMarker([p.lat, p.lon], { radius: 5, color: "#fff", weight: 1.5, fillColor: "#e8574a", fillOpacity: 1, interactive: false }).addTo(capaExtra); });
    }
    if (modo === "dividir" && marca.length) L.circleMarker([t.pts[marca[0]].lat, t.pts[marca[0]].lon], { radius: 8, color: "#fff", weight: 3, fillColor: "#e9a53b", fillOpacity: 1 }).addTo(capaExtra);
    if (modo === "tramo" && marca.length) {
      marca.forEach(function (k) { L.circleMarker([t.pts[k].lat, t.pts[k].lon], { radius: 7, color: "#fff", weight: 3, fillColor: "#e8574a", fillOpacity: 1 }).addTo(capaExtra); });
      if (marca.length === 2) {
        var a = Math.min(marca[0], marca[1]), b = Math.max(marca[0], marca[1]);
        L.polyline(t.pts.slice(a, b + 1).map(function (p) { return [p.lat, p.lon]; }), { color: "#e8574a", weight: 7, opacity: 0.85, interactive: false }).addTo(capaExtra);
      }
    }
    if (modo === "punto") {
      var b0 = map.getBounds(), vis = [];
      t.pts.forEach(function (p, k) { if (b0.contains([p.lat, p.lon])) vis.push(k); });
      if (vis.length <= 600) vis.forEach(function (k) { L.circleMarker([t.pts[k].lat, t.pts[k].lon], { radius: 3, color: t.color, weight: 1, fillColor: "#fff", fillOpacity: 1, interactive: false }).addTo(capaExtra); });
      if (puntoSel != null) {
        var p = t.pts[puntoSel], m = L.marker([p.lat, p.lon], { draggable: true, autoPan: true }).addTo(capaExtra);
        m.on("dragend", function () { guardar(); var ll = m.getLatLng(); p.lat = ll.lat; p.lon = ll.lng; refrescar(true); pintarModo(); dibujarExtra(); });
      }
    }
  }
  map.on("moveend", function () { if (modo === "punto") dibujarExtra(); });

  /* perfil de altitud del seleccionado */
  var perfilDatos = null;
  function pintarPerfil() {
    var t = sel();
    if (!t) { perfilEl.innerHTML = ""; perfilDatos = null; return; }
    var s = stats(t);
    var cab = '<div class="gx-pcab"><b>' + esc(t.name) + "</b><span>" + km(s.total) + " km</span><span>+" + ent(s.up) + " m</span><span>−" + ent(s.dn) + " m</span>" +
      (s.emax != null ? "<span>" + ent(s.emin) + "–" + ent(s.emax) + " m</span>" : "") + (isFinite(s.tiempo) ? "<span>" + dur(s.tiempo) + " total · " + dur(s.mov) + " en marcha</span>" : "") + "</div>";
    if (!s.sm) { perfilEl.innerHTML = cab + '<p class="gx-vacio">Este track no tiene altitud.</p>'; perfilDatos = null; return; }
    var W = 900, H = 170, L0 = 44, R0 = 10, T0 = 10, B0 = 22, e0 = Math.floor(s.emin / 50) * 50, e1 = Math.ceil(s.emax / 50) * 50 || e0 + 50;
    if (e1 - e0 < 100) e1 = e0 + 100;
    var X = function (d) { return L0 + (W - L0 - R0) * d / (s.total || 1); }, Y = function (v) { return T0 + (H - T0 - B0) * (1 - (v - e0) / (e1 - e0)); };
    var step = Math.max(1, Math.floor(t.pts.length / 1500)), d = "";
    for (var i = 0; i < t.pts.length; i += step) d += (d ? "L" : "M") + X(s.dist[i]).toFixed(1) + " " + Y(s.sm[i]).toFixed(1);
    d += "L" + X(s.total).toFixed(1) + " " + Y(s.sm[s.sm.length - 1]).toFixed(1);
    var g = '<svg viewBox="0 0 ' + W + " " + H + '" class="gx-psvg" preserveAspectRatio="none">';
    var paso = [50, 100, 200, 250, 500].filter(function (p) { return (e1 - e0) / p <= 5; })[0] || 1000;
    for (var v = Math.ceil(e0 / paso) * paso; v <= e1; v += paso) g += '<line x1="' + L0 + '" x2="' + (W - R0) + '" y1="' + Y(v) + '" y2="' + Y(v) + '" stroke="rgba(255,255,255,.08)"/><text x="' + (L0 - 5) + '" y="' + (Y(v) + 4) + '" text-anchor="end">' + v + "</text>";
    var pk = [0.5, 1, 2, 5, 10, 20, 50].filter(function (p) { return s.total / 1000 / p <= 10; })[0] || 100;
    for (var k = pk; k * 1000 < s.total; k += pk) g += '<text x="' + X(k * 1000) + '" y="' + (H - 6) + '" text-anchor="middle">' + k + " km</text>";
    if (modo === "tramo" && marca.length === 2) {
      var a = Math.min(marca[0], marca[1]), b = Math.max(marca[0], marca[1]);
      g += '<rect x="' + X(s.dist[a]) + '" y="' + T0 + '" width="' + Math.max(1, X(s.dist[b]) - X(s.dist[a])) + '" height="' + (H - T0 - B0) + '" fill="rgba(232,87,74,.25)"/>';
    }
    g += '<path d="' + d + "L" + X(s.total) + " " + (H - B0) + "L" + L0 + " " + (H - B0) + 'Z" fill="' + t.color + '" opacity=".22"/><path d="' + d + '" fill="none" stroke="' + t.color + '" stroke-width="2"/>';
    g += '<line id="gx-pl" x1="0" x2="0" y1="' + T0 + '" y2="' + (H - B0) + '" stroke="#fff" stroke-width="1" visibility="hidden"/></svg><div class="gx-ptip" id="gx-ptip"></div>';
    perfilEl.innerHTML = cab + '<div class="gx-pw">' + g + "</div>";
    perfilDatos = { t: t, s: s, X: X, W: W, L0: L0, R0: R0 };
  }
  perfilEl.addEventListener("mousemove", function (e) {
    var svg = perfilEl.querySelector("svg"); if (!svg || !perfilDatos) return;
    var r = svg.getBoundingClientRect(), P = perfilDatos, x = (e.clientX - r.left) / r.width * P.W;
    var dd = (x - P.L0) / (P.W - P.L0 - P.R0) * P.s.total;
    if (dd < 0 || dd > P.s.total) return;
    var lo = 0, hi = P.s.dist.length - 1;
    while (hi - lo > 1) { var m = (lo + hi) >> 1; if (P.s.dist[m] < dd) lo = m; else hi = m; }
    var p = P.t.pts[hi], ln = document.getElementById("gx-pl"), tip = document.getElementById("gx-ptip");
    ln.setAttribute("x1", P.X(P.s.dist[hi])); ln.setAttribute("x2", P.X(P.s.dist[hi])); ln.setAttribute("visibility", "visible");
    tip.style.left = (P.X(P.s.dist[hi]) / P.W * 100) + "%"; tip.style.display = "block";
    tip.textContent = km(P.s.dist[hi]) + " km · " + (P.s.sm ? ent(P.s.sm[hi]) + " m" : "") + (isFinite(p.t) ? " · " + new Date(p.t).toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" }) : "");
    cursor.setLatLng([p.lat, p.lon]).addTo(map);
  });
  perfilEl.addEventListener("mouseleave", function () {
    cursor.remove(); var ln = document.getElementById("gx-pl"), tip = document.getElementById("gx-ptip");
    if (ln) ln.setAttribute("visibility", "hidden"); if (tip) tip.style.display = "none";
  });

  /* ---------------------------------------------------------------- flujo general */
  var avisoT;
  function avisar(txt) {
    var a = document.getElementById("gx-toast");
    if (!a) { a = document.createElement("div"); a.id = "gx-toast"; a.className = "gx-toast"; a.setAttribute("role", "status"); document.body.appendChild(a); }
    a.textContent = txt; a.classList.add("on"); clearTimeout(avisoT); avisoT = setTimeout(function () { a.classList.remove("on"); }, 4200);
  }
  function seleccionar(id) { selId = id; modo = null; marca = []; puntoSel = null; prev = null; map.getContainer().classList.remove("gx-cruz"); refrescar(); }
  function refrescar(mantenerRes) {
    if (selId != null && !sel()) selId = tracks.length ? tracks[0].id : null;
    if (selId == null && tracks.length) selId = tracks[0].id;
    var res = mantenerRes && $("gx-res") ? $("gx-res").innerHTML : "";
    pintarLista(); pintarTools(); pintarModo(); dibujar(); pintarPerfil();
    if (res && $("gx-res")) $("gx-res").innerHTML = res;
    $("gx-undo").disabled = !hist.length; $("gx-redo").disabled = !rehacer.length;
    $("gx-save").disabled = !tracks.length;
    $("gx-drop").style.display = tracks.length ? "none" : "";
    $("gx-save").textContent = tracks.some(function (t) { return t.marcado; }) ? "Descargar los marcados" : "Descargar GPX";
  }
  function deshacer() { if (!hist.length) return; rehacer.push({ t: clonar(tracks), sel: selId }); var h = hist.pop(); tracks = h.t; selId = h.sel; modo = null; prev = null; refrescar(); }
  function hacerOtraVez() { if (!rehacer.length) return; hist.push({ t: clonar(tracks), sel: selId }); var h = rehacer.pop(); tracks = h.t; selId = h.sel; modo = null; prev = null; refrescar(); }
  $("gx-undo").addEventListener("click", deshacer);
  $("gx-redo").addEventListener("click", hacerOtraVez);
  $("gx-save").addEventListener("click", function () {
    var ms = tracks.filter(function (t) { return t.marcado; }), lst = ms.length ? ms : tracks;
    var nombre = lst.length === 1 ? lst[0].name : (lst[0].name + " y " + (lst.length - 1) + " más");
    descargar(gpxTexto(lst, wpts, nombre), nombre);
  });

  function cargar(texto, nombre) {
    try {
      var r = leerArchivo(texto, nombre);
      if (tracks.length) guardar();
      var primero = null;
      r.tracks.forEach(function (x) { var t = nuevoTrack(x.name, x.pts); tracks.push(t); primero = primero || t; });
      wpts = wpts.concat(r.wpts);
      selId = primero.id; refrescar(); encuadrar();
      avisar("Abierto «" + nombre + "»: " + r.tracks.length + (r.tracks.length === 1 ? " track" : " tracks") + (r.wpts.length ? " y " + r.wpts.length + " puntos de interés" : "") + ".");
    } catch (er) { avisar(er.message); }
  }
  function archivos(fl) {
    Array.prototype.forEach.call(fl, function (f) {
      if (f.size > 40e6) { avisar(f.name + ": es demasiado grande."); return; }
      var rd = new FileReader(); rd.onload = function () { cargar(rd.result, f.name); }; rd.readAsText(f);
    });
  }
  $("gx-file").addEventListener("change", function (e) { archivos(e.target.files); e.target.value = ""; });
  $("gx-demo").addEventListener("click", function () {
    fetch("/data/ejemplo-gpx-con-errores.gpx").then(function (r) { return r.text(); }).then(function (t) { cargar(t, "ejemplo-gpx-con-errores.gpx"); });
  });
  ["dragenter", "dragover"].forEach(function (ev) { app.addEventListener(ev, function (e) { e.preventDefault(); app.classList.add("gx-arr"); }); });
  ["dragleave", "drop"].forEach(function (ev) { app.addEventListener(ev, function (e) { e.preventDefault(); if (ev === "drop" || !app.contains(e.relatedTarget)) app.classList.remove("gx-arr"); }); });
  app.addEventListener("drop", function (e) { if (e.dataTransfer && e.dataTransfer.files.length) archivos(e.dataTransfer.files); });
  window.addEventListener("beforeunload", function (e) { if (hist.length) { e.preventDefault(); e.returnValue = ""; } });
  refrescar();
  // utilidades expuestas para pruebas
  window.__gx = { corregir: corregir, leer: leerArchivo, gpx: gpxTexto, map: map, estado: function () { return tracks; } };
})();
