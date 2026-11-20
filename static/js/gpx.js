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
    if (!p.length) return { dist: [0], total: 0, up: 0, dn: 0, sm: null, emin: null, emax: null, tiempo: NaN, mov: 0 };
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
  var tracks = [], wpts = [], selId = null, modo = null, marca = [], prev = null, puntoSel = null, dib = null, ocupado = false;
  var hist = [], rehacer = [];
  function copiaW(w) { return { lat: w.lat, lon: w.lon, ele: w.ele, t: w.t, name: w.name }; }
  function foto() { return { t: clonar(tracks), w: wpts.map(copiaW), sel: selId }; }
  function guardar() {
    hist.push(foto());
    if (hist.length > 40) hist.shift();
    rehacer = [];
  }
  function sel() { return tracks.filter(function (t) { return t.id === selId; })[0] || null; }

  /* ---------------------------------------------------------------- interfaz */
  app.innerHTML =
    '<div class="gx-bar"><label class="btn btn-primary gx-abrir"><span id="gx-abrir-t">Abrir GPX, KML o TCX</span><input type="file" id="gx-file" accept=".gpx,.kml,.tcx,application/gpx+xml" multiple hidden></label>' +
    '<button type="button" class="btn btn-ghost" id="gx-demo">Probar con un ejemplo</button>' +
    '<span class="gx-sep"></span><button type="button" class="gx-ib" id="gx-undo" title="Deshacer (Ctrl+Z)" disabled>↶ Deshacer</button><button type="button" class="gx-ib" id="gx-redo" title="Rehacer (Ctrl+Y)" disabled>↷ Rehacer</button>' +
    '<span class="gx-sep"></span><button type="button" class="btn btn-primary" id="gx-save" disabled>Descargar GPX</button></div>' +
    '<p class="gx-priv">Tus archivos no se suben a ningún servidor: todo se procesa en tu navegador.</p>' +
    '<div class="gx-main"><aside class="gx-panel"><div id="gx-lista"></div><div id="gx-crear"></div><div id="gx-tools"></div></aside>' +
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
      if (!t.vis || !t.pts.length) return;
      var ll = t.pts.map(function (p) { return [p.lat, p.lon]; });
      if (t.id === selId) L.polyline(ll, { color: "#000", weight: 7, opacity: 0.45, interactive: false }).addTo(capaTr);
      var pl = L.polyline(ll, { color: t.color, weight: t.id === selId ? 4.5 : 3, opacity: t.id === selId ? 1 : 0.8 }).addTo(capaTr);
      pl.on("click", function (e) { if (!modo && t.id !== selId) { L.DomEvent.stop(e); seleccionar(t.id); } });
      L.circleMarker(ll[0], { radius: 5, color: "#fff", weight: 2, fillColor: "#3fae5a", fillOpacity: 1, interactive: false }).addTo(capaTr);
      L.circleMarker(ll[ll.length - 1], { radius: 5, color: "#fff", weight: 2, fillColor: "#d9372b", fillOpacity: 1, interactive: false }).addTo(capaTr);
    });
    wpts.forEach(function (w) {
      var mk = L.marker([w.lat, w.lon], { draggable: true, icon: L.divIcon({ className: "gx-wpi", html: "<i></i>", iconSize: [18, 18], iconAnchor: [9, 18] }) })
        .bindTooltip(esc(w.name || "Waypoint"), { permanent: true, direction: "top", offset: [0, -16], className: "gx-wpt" }).addTo(capaWp);
      mk.on("dragend", function () { guardar(); var ll = mk.getLatLng(); w.lat = ll.lat; w.lon = ll.lng; w.ele = NaN; altitud(w.lat, w.lon).then(function (v) { w.ele = v; pintarCrear(); }); });
    });
    dibujarExtra();
  }
  function encuadrar(t) {
    var ll = [];
    (t ? [t] : tracks.filter(function (x) { return x.vis; })).forEach(function (x) { x.pts.forEach(function (p) { ll.push([p.lat, p.lon]); }); });
    if (ll.length) map.fitBounds(L.latLngBounds(ll), { padding: [30, 30], maxZoom: 16 });
  }

  /* lista de tracks */
  function pintarLista() {
    if (!tracks.length) { lista.innerHTML = '<p class="gx-vacio">Abre uno o varios archivos (puedes elegir varios a la vez o ir añadiendo más) o dibuja un track nuevo en el mapa.</p>'; return; }
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
    var tieneT = t.pts.length > 0 && isFinite(t.pts[0].t);
    if (t.pts.length < 2) { tools.innerHTML = ""; return; }
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
      '<details class="gx-corr"><summary>Descargar imágenes</summary>' + opcImagenes() +
      '<div class="gx-fila gx-wrap"><button type="button" class="gx-ib" data-img="mapa">Mapa</button><button type="button" class="gx-ib" data-img="perfil">Perfil</button><button type="button" class="gx-ib" data-img="ficha">Ficha (mapa + perfil)</button></div>' +
      '<p class="gx-mini">Del track completo. Para un trozo, usa «Tramo», márcalo en el mapa y descárgalo desde ahí.</p></details>' +
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
    var bi = e.target.closest("[data-img]");
    if (bi) { exportarImagen(bi.getAttribute("data-img"), t.pts, t.name, t.color); return; }
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
    if (e.target.id === "gx-video") { try { sessionStorage.setItem("gx-video", gpxTexto([t], wpts, t.name)); } catch (er) {} }
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
    if (modo === "dibujar" && m !== "dibujar") terminarDibujo();
    modo = m; marca = []; puntoSel = null; prev = null;
    map.getContainer().classList.toggle("gx-cruz", !!m);
    pintarTools(); pintarModo(); dibujarExtra();
  }
  function pintarModo() {
    var t = sel();
    if (modo === "wpt") { modoEl.innerHTML = '<div class="gx-aviso">Pulsa en el mapa donde quieras poner cada waypoint. Luego puedes cambiarles el nombre en la lista o arrastrarlos. <button type="button" class="gx-ib" data-x="salir">Terminar</button></div>'; return; }
    if (modo === "dibujar" && dib && t) {
      modoEl.innerHTML = '<div class="gx-aviso"><span class="gx-sw" role="group" aria-label="Cómo unir los puntos"><button type="button" data-x="ruta-si" class="' + (crearOpc.seguir ? "on" : "") + '">Por caminos</button><button type="button" data-x="ruta-no" class="' + (crearOpc.seguir ? "" : "on") + '">Campo a través</button></span> ' +
        (ocupado ? "Buscando el camino…" : t.pts.length ? "Pulsa en el mapa para seguir dibujando (" + ent(t.pts.length) + " puntos, " + km(stats(t).total) + " km)." : "Pulsa en el mapa para poner el primer punto.") +
        ' <small class="gx-mini">Puedes cambiar entre «Por caminos» y «Campo a través» en cada clic. Atajo: mantén pulsada la tecla Mayúsculas para ir en línea recta.</small>' +
        (dib.pasos.length ? ' <button type="button" class="btn btn-ghost" data-x="atras">Quitar el último tramo</button>' : "") + ' <button type="button" class="btn btn-primary" data-x="salir">Terminar</button></div>';
      return;
    }
    if (!modo || !t) { modoEl.innerHTML = ""; return; }
    var h = '<div class="gx-aviso">';
    if (modo === "dividir") {
      h += marca.length ? "Cortar en el punto " + ent(marca[0] + 1) + " de " + ent(t.pts.length) + '. <button type="button" class="btn btn-primary" data-x="cortar">Dividir aquí</button>' : "Pulsa sobre el track en el punto donde quieres dividirlo.";
    } else if (modo === "tramo") {
      if (marca.length < 2) h += marca.length ? "Ahora pulsa el final del tramo." : "Pulsa el inicio del tramo sobre el track.";
      else {
        var a = Math.min(marca[0], marca[1]), b = Math.max(marca[0], marca[1]), s = 0;
        for (var i = a + 1; i <= b; i++) s += hav(t.pts[i - 1], t.pts[i]);
        h += "Tramo de " + km(s) + " km (" + ent(b - a + 1) + ' puntos). <button type="button" class="btn btn-primary" data-x="quitar">Quitar y unir los extremos</button><button type="button" class="btn btn-ghost" data-x="separar">Quitar y dejar dos tracks</button><button type="button" class="btn btn-ghost" data-x="solo">Quedarme solo con este tramo</button>' +
          '<span class="gx-tramimg">Imágenes del tramo: <button type="button" class="gx-ib" data-ti="mapa">Mapa</button><button type="button" class="gx-ib" data-ti="perfil">Perfil</button><button type="button" class="gx-ib" data-ti="ficha">Ficha</button></span>';
      }
    } else if (modo === "punto") {
      h += puntoSel != null ? "Punto " + ent(puntoSel + 1) + ': arrástralo para moverlo. <button type="button" class="btn btn-ghost" data-x="borrapt">Borrar este punto</button>' : "Pulsa sobre el track para elegir un punto. Luego puedes arrastrarlo o borrarlo (tecla Supr).";
    }
    modoEl.innerHTML = h + ' <button type="button" class="gx-ib" data-x="salir">Terminar</button></div>';
  }
  modoEl.addEventListener("click", function (e) {
    var ti = e.target.getAttribute("data-ti");
    if (ti && modo === "tramo" && marca.length === 2) {
      var t0 = sel(), a0 = Math.min(marca[0], marca[1]), b0 = Math.max(marca[0], marca[1]), sd = stats({ pts: t0.pts.slice(0, a0 + 1) }).total, ed = sd + stats({ pts: t0.pts.slice(a0, b0 + 1) }).total;
      exportarImagen(ti, t0.pts.slice(a0, b0 + 1), t0.name + " (km " + km(sd) + "–" + km(ed) + ")", t0.color); return;
    }
    var x = e.target.getAttribute("data-x"), t = sel(); if (!x) return;
    if (x === "salir") { cambiarModo(null); refrescar(); return; }
    if (x === "atras") { quitarTramoDibujado(); return; }
    if (x === "ruta-si" || x === "ruta-no") { crearOpc.seguir = x === "ruta-si"; pintarModo(); pintarCrear(); return; }
    if (!t) return;
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
    if (e.key === "Escape" && modo) { cambiarModo(null); refrescar(); }
    if (e.key === "Backspace" && modo === "dibujar") { e.preventDefault(); quitarTramoDibujado(); }
  });
  function cercano(t, ll) {
    var best = -1, bd = Infinity, p = { lat: ll.lat, lon: ll.lng };
    for (var i = 0; i < t.pts.length; i++) { var d = hav(p, t.pts[i]); if (d < bd) { bd = d; best = i; } }
    var px = map.latLngToContainerPoint([t.pts[best].lat, t.pts[best].lon]).distanceTo(map.latLngToContainerPoint(ll));
    return px <= 24 ? best : -1;
  }
  map.on("click", function (e) {
    if (modo === "wpt") { ponerWpt(e.latlng); return; }
    if (modo === "dibujar") { clicDibujo(e.latlng, e.originalEvent && e.originalEvent.shiftKey); return; }
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

  /* ---------------------------------------------------------------- crear: dibujar tracks y poner waypoints */
  var crearOpc = { seguir: true, perfil: "hiking-mountain" };
  var crearEl = document.getElementById("gx-crear");
  function pintarCrear() {
    var t = sel();
    var h = '<h3 class="gx-h">Crear</h3><div class="gx-btns gx-btns2">' +
      '<button type="button" class="gx-tb' + (modo === "dibujar" && dib && dib.nuevo ? " on" : "") + '" data-c="nuevo"><b>✎ Dibujar</b><span>track nuevo</span></button>' +
      '<button type="button" class="gx-tb' + (modo === "dibujar" && dib && !dib.nuevo && dib.at === "fin" ? " on" : "") + '" data-c="fin"' + (t && !(dib && dib.nuevo) ? "" : " disabled") + '><b>⟶ Alargar</b><span>por el final</span></button>' +
      '<button type="button" class="gx-tb' + (modo === "dibujar" && dib && !dib.nuevo && dib.at === "ini" ? " on" : "") + '" data-c="ini"' + (t && !(dib && dib.nuevo) ? "" : " disabled") + '><b>⟵ Alargar</b><span>por el principio</span></button>' +
      '<button type="button" class="gx-tb' + (modo === "wpt" ? " on" : "") + '" data-c="wpt"><b>📍 Waypoint</b><span>añadir puntos</span></button></div>' +
      '<label class="gx-op"><input type="checkbox" id="gx-seguir"' + (crearOpc.seguir ? " checked" : "") + '> Seguir senderos y caminos al dibujar (desmárcalo para ir campo a través)</label>' +
      '<div class="gx-fila"><label>Para <select id="gx-perfil"><option value="hiking-mountain"' + (crearOpc.perfil === "hiking-mountain" ? " selected" : "") + '>Ir a pie</option><option value="trekking"' + (crearOpc.perfil === "trekking" ? " selected" : "") + '>Bicicleta</option></select></label></div>' +
      '<p class="gx-mini">Los caminos se calculan con <a href="https://brouter.de" target="_blank" rel="noopener">BRouter</a> sobre los datos de OpenStreetMap; la altitud de los puntos dibujados sale de un modelo del terreno.</p>';
    if (wpts.length) {
      h += '<h3 class="gx-h" style="margin-top:14px">Waypoints <small>(' + wpts.length + ')</small></h3><ul class="gx-wl">' + wpts.map(function (w, i) {
        return '<li data-w="' + i + '"><input class="gx-wnom" value="' + esc(w.name || "") + '" placeholder="Sin nombre" aria-label="Nombre del waypoint"><span>' + (isFinite(w.ele) ? ent(w.ele) + " m" : "") + '</span><button type="button" data-wa="zoom" title="Ver en el mapa">⤢</button><button type="button" data-wa="del" title="Borrar">🗑</button></li>';
      }).join("") + "</ul>";
    }
    crearEl.innerHTML = h;
  }
  crearEl.addEventListener("click", function (e) {
    var b = e.target.closest("[data-c]");
    if (b && !b.disabled) {
      var c = b.getAttribute("data-c");
      if (c === "wpt") { cambiarModo(modo === "wpt" ? null : "wpt"); pintarCrear(); return; }
      var mismo = modo === "dibujar" && dib && ((c === "nuevo" && dib.nuevo) || (!dib.nuevo && dib.at === c));
      cambiarModo(null);
      if (!mismo) empezarDibujo(c);
      refrescar(); return;
    }
    var li = e.target.closest("[data-w]"), a = e.target.getAttribute("data-wa");
    if (!li || !a) return;
    var w = wpts[+li.getAttribute("data-w")];
    if (a === "zoom") map.setView([w.lat, w.lon], Math.max(map.getZoom(), 15));
    if (a === "del") { guardar(); wpts.splice(+li.getAttribute("data-w"), 1); refrescar(); }
  });
  crearEl.addEventListener("change", function (e) {
    if (e.target.id === "gx-seguir") { crearOpc.seguir = e.target.checked; pintarModo(); }
    if (e.target.id === "gx-perfil") crearOpc.perfil = e.target.value;
    if (e.target.classList.contains("gx-wnom")) { guardar(); wpts[+e.target.closest("[data-w]").getAttribute("data-w")].name = e.target.value.trim(); dibujar(); }
  });
  function ponerWpt(ll) {
    guardar();
    var w = { lat: ll.lat, lon: ll.lng, ele: NaN, t: NaN, name: "Waypoint " + (wpts.length + 1) };
    wpts.push(w); refrescar(true);
    var idx = wpts.length - 1;
    altitud(w.lat, w.lon).then(function (v) { w.ele = v; var sp = crearEl.querySelector('[data-w="' + idx + '"] span'); if (sp && isFinite(v)) sp.textContent = ent(v) + " m"; });
    var inp = crearEl.querySelector('[data-w="' + (wpts.length - 1) + '"] .gx-wnom'); if (inp) { inp.focus(); inp.select(); }
  }
  function empezarDibujo(c) {
    guardar();
    var t;
    if (c === "nuevo") { t = nuevoTrack("Track dibujado", []); tracks.push(t); selId = t.id; }
    else { t = sel(); if (!t) return; if (c === "ini") t.pts.reverse(); }
    dib = { id: t.id, nuevo: c === "nuevo", at: c === "ini" ? "ini" : "fin", pasos: [] };
    modo = "dibujar"; map.getContainer().classList.add("gx-cruz");
    if (c === "nuevo") avisar("Pulsa en el mapa para ir poniendo puntos." + (crearOpc.seguir ? " El track seguirá los senderos entre un punto y otro." : ""));
  }
  function trackDib() { return dib ? tracks.filter(function (x) { return x.id === dib.id; })[0] : null; }
  function terminarDibujo() {
    var t = trackDib(); if (!t) { dib = null; return; }
    if (dib.at === "ini") t.pts.reverse();
    if (t.pts.length < 2) { tracks.splice(tracks.indexOf(t), 1); if (dib.nuevo) avisar("Track descartado: hacen falta al menos dos puntos."); }
    dib = null; map.getContainer().classList.remove("gx-cruz");
  }
  function quitarTramoDibujado() {
    var t = trackDib(); if (!t || !dib.pasos.length || ocupado) return;
    var n = dib.pasos.pop(); t.pts.splice(t.pts.length - n, n);
    refrescar(true);
  }
  async function clicDibujo(ll, recto) {
    var t = trackDib(); if (!t || ocupado) return;
    var nuevoP = { lat: ll.lat, lon: ll.lng, ele: NaN, t: NaN }, add = [nuevoP];
    if (t.pts.length && crearOpc.seguir && !recto) {
      ocupado = true; pintarModo();
      try { add = await camino(t.pts[t.pts.length - 1], nuevoP, crearOpc.perfil); }
      catch (er) { avisar("No se ha encontrado camino entre esos puntos: se une en línea recta."); add = [nuevoP]; }
      ocupado = false;
    }
    await Promise.all(add.map(function (p) { return isFinite(p.ele) ? null : altitud(p.lat, p.lon).then(function (v) { p.ele = v; }); }));
    if (!dib || trackDib() !== t) return;
    t.pts = t.pts.concat(add); dib.pasos.push(add.length);
    refrescar(true);
  }
  /* camino por senderos entre dos puntos (BRouter, datos de OpenStreetMap) */
  function camino(a, b, perfil) {
    var u = "https://brouter.de/brouter?lonlats=" + a.lon.toFixed(6) + "," + a.lat.toFixed(6) + "|" + b.lon.toFixed(6) + "," + b.lat.toFixed(6) + "&profile=" + perfil + "&alternativeidx=0&format=geojson";
    return fetch(u).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (g) {
      var c = g.features[0].geometry.coordinates;
      var pts = c.map(function (x) { return { lat: x[1], lon: x[0], ele: x[2] != null ? +x[2] : NaN, t: NaN }; });
      if (pts.length && hav(pts[0], a) < 25) pts.shift();
      if (!pts.length || hav(pts[pts.length - 1], b) > 300) throw new Error("lejos");
      return pts;
    });
  }
  /* altitud del terreno en un punto (teselas Terrarium, Terrain Tiles de AWS Open Data) */
  var teselas = {};
  function altitud(lat, lon) {
    var z = 13, n = Math.pow(2, z), xf = (lon + 180) / 360 * n, yf = (1 - Math.log(Math.tan(lat * R) + 1 / Math.cos(lat * R)) / Math.PI) / 2 * n;
    var x = Math.floor(xf), y = Math.floor(yf), k = z + "/" + x + "/" + y;
    if (!teselas[k]) teselas[k] = new Promise(function (ok, ko) {
      var im = new Image(); im.crossOrigin = "anonymous";
      im.onload = function () { var c = document.createElement("canvas"); c.width = c.height = 256; var cx = c.getContext("2d", { willReadFrequently: true }); cx.drawImage(im, 0, 0); ok(cx); };
      im.onerror = ko; im.src = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/" + k + ".png";
    });
    return teselas[k].then(function (cx) {
      var px = cx.getImageData(Math.min(255, Math.floor((xf - x) * 256)), Math.min(255, Math.floor((yf - y) * 256)), 1, 1).data;
      return Math.round((px[0] * 256 + px[1] + px[2] / 256 - 32768) * 10) / 10;
    }).catch(function () { return NaN; });
  }

  /* ---------------------------------------------------------------- imágenes: mapa, perfil y ficha en PNG */
  var imgOpc = { base: "otm", fmt: "h" };
  var BASES = {
    otm: { n: "Topográfico (OpenTopoMap)", max: 17, url: function (z, x, y) { return "https://" + "abc"[(x + y) % 3] + ".tile.opentopomap.org/" + z + "/" + x + "/" + y + ".png"; }, attr: "© OpenTopoMap (CC-BY-SA) · © colaboradores de OpenStreetMap" },
    ign: { n: "Mapa IGN", max: 17, url: function (z, x, y) { return ign.replace("{c}", "mapa-raster").replace("{f}", "jpeg").replace("{l}", "MTN").replace("{z}", z).replace("{y}", y).replace("{x}", x); }, attr: "© Instituto Geográfico Nacional" },
    pnoa: { n: "Ortofoto PNOA", max: 19, url: function (z, x, y) { return ign.replace("{c}", "pnoa-ma").replace("{f}", "jpeg").replace("{l}", "OI.OrthoimageCoverage").replace("{z}", z).replace("{y}", y).replace("{x}", x); }, attr: "PNOA © Instituto Geográfico Nacional" },
    osm: { n: "OpenStreetMap", max: 18, url: function (z, x, y) { return "https://tile.openstreetmap.org/" + z + "/" + x + "/" + y + ".png"; }, attr: "© colaboradores de OpenStreetMap" }
  };
  function cargarImg(u) {
    return new Promise(function (ok) { var im = new Image(); im.crossOrigin = "anonymous"; im.onload = function () { ok(im); }; im.onerror = function () { ok(null); }; im.src = u; });
  }
  function merc(lat, lon, z) { var n = 256 * Math.pow(2, z); return { x: (lon + 180) / 360 * n, y: (1 - Math.log(Math.tan(lat * R) + 1 / Math.cos(lat * R)) / Math.PI) / 2 * n }; }
  async function dibujarMapaEn(ctx, x0, y0, W, H, pts, color) {
    var b = BASES[imgOpc.base], pad = Math.round(Math.min(W, H) * 0.08);
    var la = pts.map(function (p) { return p.lat; }), lo = pts.map(function (p) { return p.lon; });
    var n0 = Math.max.apply(null, la), s0 = Math.min.apply(null, la), e0 = Math.max.apply(null, lo), w0 = Math.min.apply(null, lo), z = b.max;
    for (; z > 3; z--) { var a1 = merc(n0, w0, z), a2 = merc(s0, e0, z); if (a2.x - a1.x <= W - 2 * pad && a2.y - a1.y <= H - 2 * pad) break; }
    var c1 = merc(n0, w0, z), c2 = merc(s0, e0, z);
    // ampliación fraccionaria (hasta 1,6) para que el recorrido llene la imagen
    var sc = Math.max(1, Math.min(1.6, (W - 2 * pad) / Math.max(1, c2.x - c1.x), (H - 2 * pad) / Math.max(1, c2.y - c1.y))), TS = 256 * sc;
    var cx = (c1.x + c2.x) / 2 * sc, cy = (c1.y + c2.y) / 2 * sc, ox = cx - W / 2, oy = cy - H / 2;
    ctx.save(); ctx.beginPath(); ctx.rect(x0, y0, W, H); ctx.clip();
    ctx.fillStyle = "#e9e4da"; ctx.fillRect(x0, y0, W, H);
    var tx0 = Math.floor(ox / TS), ty0 = Math.floor(oy / TS), tx1 = Math.floor((ox + W) / TS), ty1 = Math.floor((oy + H) / TS), fallos = 0, total = 0;
    var tareas = [];
    for (var tx = tx0; tx <= tx1; tx++) for (var ty = ty0; ty <= ty1; ty++) {
      (function (tx, ty) {
        var nT = Math.pow(2, z), xx = ((tx % nT) + nT) % nT; total++;
        tareas.push(cargarImg(b.url(z, xx, ty)).then(function (im) { if (im) ctx.drawImage(im, x0 + tx * TS - ox, y0 + ty * TS - oy, TS + 0.5, TS + 0.5); else fallos++; }));
      })(tx, ty);
    }
    await Promise.all(tareas);
    var P = function (p) { var m = merc(p.lat, p.lon, z); return [x0 + m.x * sc - ox, y0 + m.y * sc - oy]; };
    var k = Math.max(1, Math.min(W, H) / 900);
    ctx.lineJoin = ctx.lineCap = "round";
    [["rgba(0,0,0,.45)", 9 * k], ["#fff", 7 * k], [color, 4.5 * k]].forEach(function (st) {
      ctx.beginPath(); pts.forEach(function (p, i) { var q = P(p); if (i) ctx.lineTo(q[0], q[1]); else ctx.moveTo(q[0], q[1]); }); ctx.strokeStyle = st[0]; ctx.lineWidth = st[1]; ctx.stroke();
    });
    function bola(p, col, txt) { var q = P(p); ctx.beginPath(); ctx.arc(q[0], q[1], 9 * k, 0, 2 * Math.PI); ctx.fillStyle = col; ctx.fill(); ctx.lineWidth = 3 * k; ctx.strokeStyle = "#fff"; ctx.stroke(); }
    bola(pts[0], "#3fae5a"); bola(pts[pts.length - 1], "#d9372b");
    // waypoints cercanos al recorrido
    ctx.font = "700 " + Math.round(13 * k) + "px Inter, system-ui, sans-serif"; ctx.textBaseline = "middle";
    wpts.forEach(function (w) {
      if (!pts.some(function (p) { return hav(p, w) < 300; })) return;
      var q = P(w); if (q[0] < x0 || q[0] > x0 + W || q[1] < y0 || q[1] > y0 + H) return;
      ctx.beginPath(); ctx.arc(q[0], q[1], 6 * k, 0, 2 * Math.PI); ctx.fillStyle = "#e8574a"; ctx.fill(); ctx.lineWidth = 2 * k; ctx.strokeStyle = "#fff"; ctx.stroke();
      if (w.name) { var tw = ctx.measureText(w.name).width; ctx.fillStyle = "rgba(255,255,255,.88)"; ctx.fillRect(q[0] + 9 * k, q[1] - 10 * k, tw + 10 * k, 20 * k); ctx.fillStyle = "#1b120c"; ctx.fillText(w.name, q[0] + 14 * k, q[1]); }
    });
    // escala
    var mpp = 156543.03392 * Math.cos((n0 + s0) / 2 * R) / Math.pow(2, z) / sc, objetivo = W * 0.18 * mpp, paso = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000].filter(function (v) { return v <= objetivo; }).pop() || 10;
    var lw = paso / mpp, sx = x0 + 16 * k, sy = y0 + H - 22 * k;
    ctx.fillStyle = "rgba(255,255,255,.85)"; ctx.fillRect(sx - 8 * k, sy - 30 * k, lw + 16 * k, 42 * k);
    ctx.fillStyle = "#1b120c"; ctx.fillRect(sx, sy, lw, 4 * k); ctx.fillRect(sx, sy - 6 * k, 2 * k, 10 * k); ctx.fillRect(sx + lw - 2 * k, sy - 6 * k, 2 * k, 10 * k);
    ctx.font = "700 " + Math.round(13 * k) + "px Inter, system-ui, sans-serif"; ctx.textBaseline = "bottom"; ctx.textAlign = "left"; ctx.fillText(paso >= 1000 ? paso / 1000 + " km" : paso + " m", sx, sy - 6 * k);
    // atribución
    ctx.font = "500 " + Math.round(11 * k) + "px Inter, system-ui, sans-serif"; ctx.textAlign = "right"; ctx.textBaseline = "bottom";
    var at = b.attr + " · guiasadastra.com", aw = ctx.measureText(at).width;
    ctx.fillStyle = "rgba(255,255,255,.8)"; ctx.fillRect(x0 + W - aw - 14 * k, y0 + H - 20 * k, aw + 14 * k, 20 * k); ctx.fillStyle = "#333"; ctx.fillText(at, x0 + W - 7 * k, y0 + H - 4 * k);
    ctx.restore();
    return { fallos: fallos, total: total };
  }
  function dibujarPerfilEn(ctx, x0, y0, W, H, pts, color) {
    var st = stats({ pts: pts }), k = Math.max(1, W / 1600);
    ctx.save(); ctx.fillStyle = "#fff"; ctx.fillRect(x0, y0, W, H);
    if (!st.sm) { ctx.fillStyle = "#666"; ctx.font = "600 " + 20 * k + "px Inter, system-ui"; ctx.fillText("Este track no tiene altitud", x0 + 30 * k, y0 + H / 2); ctx.restore(); return st; }
    var L0 = x0 + 70 * k, R0 = x0 + W - 24 * k, T0 = y0 + 24 * k, B0 = y0 + H - 46 * k;
    var e0 = Math.floor(st.emin / 50) * 50, e1 = Math.ceil(st.emax / 50) * 50; if (e1 - e0 < 100) e1 = e0 + 100;
    var X = function (d) { return L0 + (R0 - L0) * d / (st.total || 1); }, Y = function (v) { return B0 - (B0 - T0) * (v - e0) / (e1 - e0); };
    ctx.font = "600 " + Math.round(14 * k) + "px Inter, system-ui, sans-serif"; ctx.fillStyle = "#555"; ctx.strokeStyle = "#e3ddd5"; ctx.lineWidth = 1 * k;
    var pa = [50, 100, 200, 250, 500, 1000].filter(function (v) { return (e1 - e0) / v <= 6; })[0] || 2000;
    ctx.textAlign = "right"; ctx.textBaseline = "middle";
    for (var v = Math.ceil(e0 / pa) * pa; v <= e1; v += pa) { ctx.beginPath(); ctx.moveTo(L0, Y(v)); ctx.lineTo(R0, Y(v)); ctx.stroke(); ctx.fillText(ent(v) + " m", L0 - 8 * k, Y(v)); }
    var pk = [0.5, 1, 2, 5, 10, 20, 50].filter(function (q) { return st.total / 1000 / q <= 12; })[0] || 100;
    ctx.textAlign = "center"; ctx.textBaseline = "top";
    for (var q = 0; q * 1000 <= st.total + 1; q += pk) { ctx.beginPath(); ctx.moveTo(X(q * 1000), T0); ctx.lineTo(X(q * 1000), B0); ctx.stroke(); ctx.fillText(String(q).replace(".", ",") + " km", X(q * 1000), B0 + 10 * k); }
    var g = ctx.createLinearGradient(0, T0, 0, B0); g.addColorStop(0, color); g.addColorStop(1, "rgba(255,255,255,.2)");
    ctx.beginPath(); ctx.moveTo(L0, B0); pts.forEach(function (p, i) { ctx.lineTo(X(st.dist[i]), Y(st.sm[i])); }); ctx.lineTo(R0, B0); ctx.closePath();
    ctx.globalAlpha = 0.55; ctx.fillStyle = g; ctx.fill(); ctx.globalAlpha = 1;
    ctx.beginPath(); pts.forEach(function (p, i) { if (i) ctx.lineTo(X(st.dist[i]), Y(st.sm[i])); else ctx.moveTo(X(0), Y(st.sm[0])); }); ctx.strokeStyle = color; ctx.lineWidth = 3 * k; ctx.stroke();
    ctx.strokeStyle = "#999"; ctx.lineWidth = 1.5 * k; ctx.beginPath(); ctx.moveTo(L0, T0); ctx.lineTo(L0, B0); ctx.lineTo(R0, B0); ctx.stroke();
    // cumbre y waypoints
    var imax = st.sm.indexOf(Math.max.apply(null, st.sm));
    ctx.fillStyle = "#1b120c"; ctx.font = "700 " + Math.round(14 * k) + "px Inter, system-ui, sans-serif"; ctx.textBaseline = "bottom";
    ctx.fillText("▲ " + ent(st.sm[imax]) + " m", Math.min(R0 - 50 * k, Math.max(L0 + 50 * k, X(st.dist[imax]))), Y(st.sm[imax]) - 6 * k);
    wpts.forEach(function (w) {
      var bi = -1, bd = 300; pts.forEach(function (p, i) { var d = hav(p, w); if (d < bd) { bd = d; bi = i; } });
      if (bi < 0) return;
      var wx = X(st.dist[bi]), wy = Y(st.sm[bi]);
      ctx.strokeStyle = "#e8574a"; ctx.setLineDash([4 * k, 4 * k]); ctx.beginPath(); ctx.moveTo(wx, wy); ctx.lineTo(wx, B0); ctx.stroke(); ctx.setLineDash([]);
      ctx.beginPath(); ctx.arc(wx, wy, 5 * k, 0, 2 * Math.PI); ctx.fillStyle = "#e8574a"; ctx.fill();
      if (w.name) { ctx.save(); ctx.translate(wx + 4 * k, wy - 10 * k); ctx.rotate(-Math.PI / 4); ctx.fillStyle = "#1b120c"; ctx.font = "600 " + Math.round(12 * k) + "px Inter, system-ui, sans-serif"; ctx.textAlign = "left"; ctx.fillText(w.name, 0, 0); ctx.restore(); }
    });
    ctx.restore();
    return st;
  }
  function cabecera(ctx, x0, y0, W, nombre, st, color) {
    var k = Math.max(1, W / 1600);
    ctx.fillStyle = "#fff"; ctx.fillRect(x0, y0, W, 120 * k);
    ctx.fillStyle = color; ctx.fillRect(x0, y0, 10 * k, 120 * k);
    ctx.fillStyle = "#1b120c"; ctx.font = "800 " + Math.round(34 * k) + "px Inter, system-ui, sans-serif"; ctx.textBaseline = "top"; ctx.textAlign = "left";
    var t = nombre; while (ctx.measureText(t).width > W - 80 * k && t.length > 5) t = t.slice(0, -2); if (t !== nombre) t += "…";
    ctx.fillText(t, x0 + 34 * k, y0 + 20 * k);
    var datos = [km(st.total) + " km", "+" + ent(st.up) + " m", "−" + ent(st.dn) + " m"];
    if (st.emax != null) datos.push("máx. " + ent(st.emax) + " m");
    if (isFinite(st.tiempo)) datos.push(dur(st.tiempo));
    ctx.font = "600 " + Math.round(20 * k) + "px Inter, system-ui, sans-serif"; ctx.fillStyle = "#555"; ctx.fillText(datos.join("   ·   "), x0 + 34 * k, y0 + 72 * k);
    ctx.textAlign = "right"; ctx.fillStyle = "#b5671a"; ctx.font = "800 " + Math.round(16 * k) + "px Inter, system-ui, sans-serif"; ctx.fillText("guiasadastra.com", x0 + W - 24 * k, y0 + 24 * k);
  }
  function guardarPng(cv, nombre) {
    cv.toBlob(function (bl) {
      var a = document.createElement("a"); a.href = URL.createObjectURL(bl); a.download = nombre.replace(/[\\/:*?"<>|]+/g, "-").slice(0, 80) + ".png";
      document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 800);
    }, "image/png");
  }
  async function exportarImagen(tipo, pts, nombre, color) {
    if (!pts || pts.length < 2) return;
    avisar("Preparando la imagen…");
    var vert = imgOpc.fmt === "v", W = vert ? 1400 : 2000, cv = document.createElement("canvas"), ctx = cv.getContext("2d"), st = stats({ pts: pts }), r = null;
    try {
      if (tipo === "perfil") { cv.width = 2000; cv.height = 820; cabecera(ctx, 0, 0, 2000, nombre, st, color); dibujarPerfilEn(ctx, 0, 150, 2000, 670, pts, color); }
      else if (tipo === "mapa") { cv.width = W; cv.height = vert ? 2000 : 1400; r = await dibujarMapaEn(ctx, 0, 0, cv.width, cv.height, pts, color); }
      else { cv.width = W; var hm = vert ? 1500 : 1200, hp = vert ? 520 : 600; cv.height = 150 + hm + hp; cabecera(ctx, 0, 0, W, nombre, st, color); r = await dibujarMapaEn(ctx, 0, 150, W, hm, pts, color); dibujarPerfilEn(ctx, 0, 150 + hm, W, hp, pts, color); }
      guardarPng(cv, nombre + " - " + tipo);
      if (r && r.fallos) avisar("Imagen descargada, pero " + r.fallos + " de " + r.total + " trozos del mapa no se han podido cargar. Prueba con otro mapa.");
      else avisar("Imagen descargada.");
    } catch (er) { console.error(er); avisar("No se ha podido crear la imagen con este mapa. Prueba con otro."); }
  }
  function opcImagenes() {
    return '<div class="gx-fila gx-wrap"><label>Mapa <select data-io="base">' + Object.keys(BASES).map(function (k) { return '<option value="' + k + '"' + (imgOpc.base === k ? " selected" : "") + ">" + BASES[k].n + "</option>"; }).join("") + "</select></label>" +
      '<label>Formato <select data-io="fmt"><option value="h"' + (imgOpc.fmt === "h" ? " selected" : "") + '>Horizontal</option><option value="v"' + (imgOpc.fmt === "v" ? " selected" : "") + ">Vertical</option></select></label></div>";
  }
  document.addEventListener("change", function (e) { var k = e.target.getAttribute && e.target.getAttribute("data-io"); if (k) imgOpc[k] = e.target.value; document.querySelectorAll('[data-io="' + k + '"]').forEach(function (x) { x.value = imgOpc[k]; }); });

  /* ---------------------------------------------------------------- flujo general */
  var avisoT;
  function avisar(txt) {
    var a = document.getElementById("gx-toast");
    if (!a) { a = document.createElement("div"); a.id = "gx-toast"; a.className = "gx-toast"; a.setAttribute("role", "status"); document.body.appendChild(a); }
    a.textContent = txt; a.classList.add("on"); clearTimeout(avisoT); avisoT = setTimeout(function () { a.classList.remove("on"); }, 4200);
  }
  function seleccionar(id) { if (modo === "dibujar") terminarDibujo(); selId = id; modo = null; marca = []; puntoSel = null; prev = null; map.getContainer().classList.remove("gx-cruz"); refrescar(); }
  function refrescar(mantenerRes) {
    if (selId != null && !sel()) selId = tracks.length ? tracks[0].id : null;
    if (selId == null && tracks.length) selId = tracks[0].id;
    var res = mantenerRes && $("gx-res") ? $("gx-res").innerHTML : "";
    pintarLista(); pintarCrear(); pintarTools(); pintarModo(); dibujar(); pintarPerfil();
    if (res && $("gx-res")) $("gx-res").innerHTML = res;
    $("gx-undo").disabled = !hist.length; $("gx-redo").disabled = !rehacer.length;
    $("gx-save").disabled = !tracks.length && !wpts.length;
    $("gx-abrir-t").textContent = tracks.length ? "Añadir más GPX" : "Abrir GPX, KML o TCX";
    $("gx-drop").style.display = tracks.length || wpts.length || modo ? "none" : "";
    $("gx-save").textContent = tracks.some(function (t) { return t.marcado; }) ? "Descargar los marcados" : "Descargar GPX";
  }
  function restaurar(h) { tracks = h.t; wpts = h.w || wpts; selId = h.sel; modo = null; dib = null; prev = null; map.getContainer().classList.remove("gx-cruz"); refrescar(); }
  function deshacer() { if (!hist.length || ocupado) return; rehacer.push(foto()); restaurar(hist.pop()); }
  function hacerOtraVez() { if (!rehacer.length || ocupado) return; hist.push(foto()); restaurar(rehacer.pop()); }
  $("gx-undo").addEventListener("click", deshacer);
  $("gx-redo").addEventListener("click", hacerOtraVez);
  $("gx-save").addEventListener("click", function () {
    var ms = tracks.filter(function (t) { return t.marcado; }), lst = ms.length ? ms : tracks;
    var nombre = !lst.length ? "Waypoints" : lst.length === 1 ? lst[0].name : (lst[0].name + " y " + (lst.length - 1) + " más");
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
