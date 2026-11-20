/* Guías Ad Astra · Vídeo 3D de una ruta: anima el track sobre el relieve con su perfil y lo guarda en MP4.
   Todo ocurre en el navegador: el track no sale del ordenador de quien lo usa. */
(function () {
  "use strict";
  var app = document.getElementById("v3-app");
  if (!app || !window.maplibregl) return;
  var R = Math.PI / 180;

  /* ---------------------------------------------------------------- utilidades */
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function hav(a, b) {
    var dLat = (b.lat - a.lat) * R, dLon = (b.lon - a.lon) * R;
    var x = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(a.lat * R) * Math.cos(b.lat * R) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    return 2 * 6371000 * Math.asin(Math.min(1, Math.sqrt(x)));
  }
  function km(m) { return (m / 1000).toLocaleString("es-ES", { minimumFractionDigits: 1, maximumFractionDigits: 1 }); }
  function ent(n) { return Math.round(n).toLocaleString("es-ES"); }
  function dur(ms) { var m = Math.round(ms / 60000), h = Math.floor(m / 60); return h ? h + " h " + String(m % 60).padStart(2, "0") : m + " min"; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function suave(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function angLerp(a, b, t) { var d = ((b - a + 540) % 360) - 180; return a + d * t; }

  /* ---------------------------------------------------------------- lectura del track */
  function leer(text, nombre) {
    var doc = new DOMParser().parseFromString(text, "application/xml");
    if (doc.getElementsByTagName("parsererror").length) throw new Error("El archivo no es un GPX, KML o TCX válido.");
    function h(n, t) { var x = n.getElementsByTagName(t)[0]; return x ? x.textContent : null; }
    function pt(n) { var e = h(n, "ele"), t = h(n, "time"); return { lat: +n.getAttribute("lat"), lon: +n.getAttribute("lon"), ele: e != null ? parseFloat(e) : NaN, t: t ? Date.parse(t) : NaN }; }
    var cand = [];
    Array.prototype.forEach.call(doc.getElementsByTagName("trk"), function (trk) {
      var p = Array.prototype.map.call(trk.getElementsByTagName("trkpt"), pt);
      cand.push({ name: h(trk, "name"), pts: p });
    });
    Array.prototype.forEach.call(doc.getElementsByTagName("rte"), function (r) { cand.push({ name: h(r, "name"), pts: Array.prototype.map.call(r.getElementsByTagName("rtept"), pt) }); });
    if (!cand.length) {
      var tp = doc.getElementsByTagName("Trackpoint"), p2 = [];
      for (var j = 0; j < tp.length; j++) {
        var la = h(tp[j], "LatitudeDegrees"), lo = h(tp[j], "LongitudeDegrees");
        if (la == null) continue;
        var al = h(tp[j], "AltitudeMeters"), ti = h(tp[j], "Time");
        p2.push({ lat: +la, lon: +lo, ele: al != null ? parseFloat(al) : NaN, t: ti ? Date.parse(ti) : NaN });
      }
      if (p2.length) cand.push({ name: null, pts: p2 });
      Array.prototype.forEach.call(doc.getElementsByTagName("coordinates"), function (c) {
        var kp = [];
        c.textContent.trim().split(/\s+/).forEach(function (s) { var v = s.split(","); if (v.length >= 2) kp.push({ lat: +v[1], lon: +v[0], ele: v[2] != null ? parseFloat(v[2]) : NaN, t: NaN }); });
        cand.push({ name: null, pts: kp });
      });
    }
    cand.forEach(function (c) { c.pts = c.pts.filter(function (p) { return isFinite(p.lat) && isFinite(p.lon); }); });
    cand.sort(function (a, b) { return b.pts.length - a.pts.length; });
    if (!cand.length || cand[0].pts.length < 2) throw new Error("No hemos encontrado ningún track en el archivo.");
    var docName = (doc.querySelector("metadata > name") || {}).textContent;
    return { name: (cand[0].name || docName || nombre.replace(/\.[^.]+$/, "")).trim(), pts: cand[0].pts };
  }

  /* prepara el track: distancias, altitud suavizada, remuestreo y rumbo de la cámara */
  function preparar(tr) {
    var p = tr.pts, d = [0];
    for (var i = 1; i < p.length; i++) d.push(d[i - 1] + hav(p[i - 1], p[i]));
    var total = d[d.length - 1];
    var ele = p.map(function (x) { return x.ele; }), hayEle = ele.some(isFinite);
    if (hayEle) {
      var last = ele.find(isFinite);
      for (var a = 0; a < ele.length; a++) { if (isFinite(ele[a])) last = ele[a]; else ele[a] = last; }
      var sm = ele.slice();
      for (var b = 0, lo = 0, hi = 0, sum = 0; b < ele.length; b++) {
        while (hi < ele.length && d[hi] - d[b] <= 30) { sum += ele[hi]; hi++; }
        while (d[b] - d[lo] > 30) { sum -= ele[lo]; lo++; }
        sm[b] = sum / (hi - lo);
      }
      ele = sm;
    }
    var up = [0];
    if (hayEle) { var ref = ele[0], acc = 0; for (var u = 1; u < ele.length; u++) { var dd = ele[u] - ref; if (dd >= 3) { acc += dd; ref = ele[u]; } else if (dd <= -3) ref = ele[u]; up.push(acc); } }
    // remuestreo a N puntos equidistantes para la cámara
    var N = 1200, S = [], k = 0;
    for (var n = 0; n < N; n++) {
      var dist = total * n / (N - 1);
      while (k < d.length - 2 && d[k + 1] < dist) k++;
      var f = d[k + 1] > d[k] ? (dist - d[k]) / (d[k + 1] - d[k]) : 0;
      S.push({ lat: lerp(p[k].lat, p[k + 1].lat, f), lon: lerp(p[k].lon, p[k + 1].lon, f) });
    }
    // camino suavizado (media móvil) para que la cámara no tiemble
    var w = Math.max(3, Math.round(N * 0.025)), C = [];
    for (var c = 0; c < N; c++) {
      var la = 0, lo2 = 0, cn = 0;
      for (var j2 = Math.max(0, c - w); j2 <= Math.min(N - 1, c + w); j2++) { la += S[j2].lat; lo2 += S[j2].lon; cn++; }
      C.push({ lat: la / cn, lon: lo2 / cn });
    }
    // rumbo mirando hacia delante, suavizado como vector
    var ade = Math.max(8, Math.round(N * 0.05)), bx = [], by = [], B = [];
    for (var q = 0; q < N; q++) {
      var A0 = C[Math.max(0, q - 2)], A1 = C[Math.min(N - 1, q + ade)];
      if (q + ade >= N) A1 = C[N - 1];
      var y = (A1.lon - A0.lon) * Math.cos(A0.lat * R), x = A1.lat - A0.lat, an = Math.atan2(y, x);
      if (!x && !y && q) an = Math.atan2(by[q - 1], bx[q - 1]);
      bx.push(Math.cos(an)); by.push(Math.sin(an));
    }
    var w2 = Math.round(N * 0.04);
    for (var r2 = 0; r2 < N; r2++) {
      var sx = 0, sy = 0;
      for (var j3 = Math.max(0, r2 - w2); j3 <= Math.min(N - 1, r2 + w2); j3++) { sx += bx[j3]; sy += by[j3]; }
      B.push(Math.atan2(sy, sx) / R);
    }
    var lats = p.map(function (x) { return x.lat; }), lons = p.map(function (x) { return x.lon; });
    var t0 = p[0].t, t1 = p[p.length - 1].t;
    return { name: tr.name, pts: p, d: d, total: total, ele: hayEle ? ele : null, up: up, C: C, B: B, N: N,
      bounds: [[Math.min.apply(null, lons), Math.min.apply(null, lats)], [Math.max.apply(null, lons), Math.max.apply(null, lats)]],
      tiempo: isFinite(t0) && isFinite(t1) && t1 > t0 ? [t0, t1] : null,
      emin: hayEle ? Math.min.apply(null, ele) : null, emax: hayEle ? Math.max.apply(null, ele) : null };
  }
  /* posición sobre el track a una distancia dada */
  function enDist(T, dist) {
    var lo = 0, hi = T.d.length - 1;
    while (hi - lo > 1) { var m = (lo + hi) >> 1; if (T.d[m] < dist) lo = m; else hi = m; }
    var f = T.d[hi] > T.d[lo] ? (dist - T.d[lo]) / (T.d[hi] - T.d[lo]) : 0;
    var a = T.pts[lo], b = T.pts[hi];
    return { i: lo, f: f, lat: lerp(a.lat, b.lat, f), lon: lerp(a.lon, b.lon, f), ele: T.ele ? lerp(T.ele[lo], T.ele[hi], f) : null,
      up: T.up.length > 1 ? lerp(T.up[lo], T.up[hi], f) : 0, t: isFinite(a.t) && isFinite(b.t) ? lerp(a.t, b.t, f) : NaN };
  }

  /* ---------------------------------------------------------------- interfaz */
  var FORMATOS = { h: { n: "Horizontal 16:9", w: 1280, h: 720, hd: [1920, 1080] }, v: { n: "Vertical 9:16 (móvil, Reels)", w: 720, h: 1280, hd: [1080, 1920] }, c: { n: "Cuadrado 1:1", w: 1080, h: 1080, hd: [1080, 1080] } };
  var ign = "https://www.ign.es/wmts/{c}?service=WMTS&request=GetTile&version=1.0.0&Format=image/jpeg&layer={l}&style=default&tilematrixset=GoogleMapsCompatible&TileMatrix={z}&TileRow={y}&TileCol={x}";
  var MAPAS = {
    pnoa: { n: "Satélite PNOA (España)", tiles: [ign.replace("{c}", "pnoa-ma").replace("{l}", "OI.OrthoimageCoverage")], max: 19, attr: "Ortofoto PNOA © Instituto Geográfico Nacional" },
    s2: { n: "Satélite Sentinel-2 (todo el mundo)", tiles: ["https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/{z}/{y}/{x}.jpg"], max: 15, attr: "Sentinel-2 cloudless 2016 by EOX IT Services GmbH (contiene datos modificados de Copernicus Sentinel)" },
    ign: { n: "Mapa topográfico IGN (España)", tiles: [ign.replace("{c}", "mapa-raster").replace("{l}", "MTN")], max: 17, attr: "Mapa © Instituto Geográfico Nacional" },
    otm: { n: "OpenTopoMap (todo el mundo)", tiles: ["https://a.tile.opentopomap.org/{z}/{x}/{y}.png", "https://b.tile.opentopomap.org/{z}/{x}/{y}.png", "https://c.tile.opentopomap.org/{z}/{x}/{y}.png"], max: 17, attr: "© OpenTopoMap (CC-BY-SA) · © colaboradores de OpenStreetMap" }
  };
  var DEM_ATTR = "Relieve: Terrain Tiles (Mapzen, AWS Open Data)";
  var opt = { fmt: "h", hd: false, dur: 30, mapa: "pnoa", relieve: 1.4, zoom: 0, color: "#ff7a1a", perfil: true, titulo: "" };

  app.innerHTML =
    '<div class="v3-grid"><aside class="v3-panel">' +
    '<label class="btn btn-primary v3-abrir">Abrir GPX, KML o TCX<input type="file" id="v3-file" accept=".gpx,.kml,.tcx" hidden></label>' +
    '<button type="button" class="btn btn-ghost" id="v3-demo">Probar con un ejemplo</button>' +
    '<p class="v3-nom" id="v3-nom">Ningún track cargado.</p>' +
    '<label class="v3-l">Título del vídeo<input id="v3-tit" maxlength="60" placeholder="Nombre de la ruta"></label>' +
    '<label class="v3-l">Mapa<select id="v3-mapa">' + Object.keys(MAPAS).map(function (k) { return '<option value="' + k + '">' + MAPAS[k].n + "</option>"; }).join("") + "</select></label>" +
    '<label class="v3-l">Formato<select id="v3-fmt">' + Object.keys(FORMATOS).map(function (k) { return '<option value="' + k + '">' + FORMATOS[k].n + "</option>"; }).join("") + "</select></label>" +
    '<div class="v3-f2"><label class="v3-l">Duración<select id="v3-dur"><option value="20">20 s</option><option value="30" selected>30 s</option><option value="45">45 s</option><option value="60">60 s</option></select></label>' +
    '<label class="v3-l">Cámara<select id="v3-zoom"><option value="0.7">Cerca</option><option value="0" selected>Normal</option><option value="-0.7">Lejos</option></select></label></div>' +
    '<div class="v3-f2"><label class="v3-l">Relieve<select id="v3-rel"><option value="1">Real</option><option value="1.4" selected>Algo exagerado</option><option value="2">Muy exagerado</option></select></label>' +
    '<label class="v3-l">Color<input type="color" id="v3-col" value="' + opt.color + '"></label></div>' +
    '<label class="v3-ch"><input type="checkbox" id="v3-perf" checked> Perfil y datos en el vídeo</label>' +
    '<label class="v3-ch"><input type="checkbox" id="v3-hd"> Full HD (más pesado y más lento de crear)</label>' +
    '<div class="v3-acc"><button type="button" class="btn btn-ghost" id="v3-play" disabled>▶ Ver animación</button><button type="button" class="btn btn-primary" id="v3-rec" disabled>Crear vídeo MP4</button></div>' +
    '<div id="v3-estado" class="v3-estado" role="status"></div></aside>' +
    '<div class="v3-der"><div class="v3-marco" id="v3-marco"><div class="v3-esc" id="v3-esc"><div id="v3-map" class="v3-map"></div><canvas id="v3-ov" class="v3-ov"></canvas></div>' +
    '<div class="v3-drop" id="v3-drop"><b>Arrastra aquí tu track</b><span>GPX, KML o TCX</span></div></div>' +
    '<p class="v3-nota">Relieve y satélite se descargan mientras se anima: la primera vez puede tardar un poco en verse nítido. El vídeo se crea fotograma a fotograma y sale siempre bien, aunque tu ordenador sea lento.</p></div></div>';
  var $ = function (id) { return document.getElementById(id); };
  var estado = $("v3-estado"), ov = $("v3-ov"), esc0 = $("v3-esc"), marco = $("v3-marco");

  var T = null, map = null, listo = false;
  function dims() { var f = FORMATOS[opt.fmt]; return opt.hd ? { w: f.hd[0], h: f.hd[1] } : { w: f.w, h: f.h }; }
  function ajustarEscala() {
    var d = dims(), ancho = marco.clientWidth, alto = Math.min(window.innerHeight * 0.78, 760);
    var s = Math.min(ancho / d.w, alto / d.h);
    esc0.style.width = d.w + "px"; esc0.style.height = d.h + "px"; esc0.style.transform = "scale(" + s + ")";
    marco.style.height = (d.h * s) + "px";
  }
  function estilo() {
    var m = MAPAS[opt.mapa];
    return {
      version: 8,
      sources: {
        base: { type: "raster", tiles: m.tiles, tileSize: 256, maxzoom: m.max, attribution: m.attr },
        dem: { type: "raster-dem", tiles: ["https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"], encoding: "terrarium", tileSize: 256, maxzoom: 15, attribution: DEM_ATTR },
        hill: { type: "raster-dem", tiles: ["https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"], encoding: "terrarium", tileSize: 256, maxzoom: 15 },
        todo: { type: "geojson", data: { type: "Feature", geometry: { type: "LineString", coordinates: [] } } },
        hecho: { type: "geojson", data: { type: "Feature", geometry: { type: "LineString", coordinates: [] } } },
        pos: { type: "geojson", data: { type: "Feature", geometry: { type: "Point", coordinates: [0, 0] } } }
      },
      layers: [
        { id: "base", type: "raster", source: "base", paint: { "raster-fade-duration": 0 } },
        { id: "hill", type: "hillshade", source: "hill", paint: { "hillshade-exaggeration": 0.25, "hillshade-shadow-color": "#2a1d12" } },
        { id: "todo", type: "line", source: "todo", layout: { "line-cap": "round", "line-join": "round" }, paint: { "line-color": "#ffffff", "line-width": 3, "line-opacity": 0.55 } },
        { id: "hecho-b", type: "line", source: "hecho", layout: { "line-cap": "round", "line-join": "round" }, paint: { "line-color": "#1b120c", "line-width": 8, "line-opacity": 0.5 } },
        { id: "hecho", type: "line", source: "hecho", layout: { "line-cap": "round", "line-join": "round" }, paint: { "line-color": opt.color, "line-width": 5 } },
        { id: "pos-h", type: "circle", source: "pos", paint: { "circle-radius": 14, "circle-color": opt.color, "circle-opacity": 0.3 } },
        { id: "pos", type: "circle", source: "pos", paint: { "circle-radius": 7, "circle-color": opt.color, "circle-stroke-color": "#fff", "circle-stroke-width": 3 } }
      ],
      terrain: { source: "dem", exaggeration: opt.relieve },
      sky: { "sky-color": "#7fb4dc", "horizon-color": "#e9eef2", "fog-color": "#dfe7ee", "sky-horizon-blend": 0.6, "horizon-fog-blend": 0.6, "fog-ground-blend": 0.25, "atmosphere-blend": 0.8 }
    };
  }
  function crearMapa() {
    if (map) { map.remove(); map = null; }
    listo = false;
    ajustarEscala();
    map = new maplibregl.Map({ container: "v3-map", style: estilo(), interactive: false, attributionControl: false, pixelRatio: 1,
      canvasContextAttributes: { preserveDrawingBuffer: true, antialias: true }, preserveDrawingBuffer: true, fadeDuration: 0, maxPitch: 80,
      center: T ? T.C[0] && [T.C[0].lon, T.C[0].lat] : [-5.2, 40.3], zoom: T ? 11 : 6 });
    map.on("load", function () {
      listo = true;
      if (T) { cargarTrack(); prepararVistas(); camara(0); map.jumpTo(vistaIni); dibujarOverlay(0); }
    });
    map.on("error", function (e) { if (e && e.error && /terrarium|tile/i.test(String(e.error.message || ""))) return; });
  }
  function cargarTrack() {
    var coords = T.pts.map(function (p) { return [p.lon, p.lat]; });
    map.getSource("todo").setData({ type: "Feature", geometry: { type: "LineString", coordinates: coords } });
    map.getSource("hecho").setData({ type: "Feature", geometry: { type: "LineString", coordinates: [coords[0], coords[0]] } });
  }

  /* ---------------------------------------------------------------- animación */
  var TI = 3, TF = 3.5;  // segundos de entrada y de salida
  function zoomBase() { return Math.max(11, Math.min(15.2, 14.1 - 0.72 * Math.log2(Math.max(500, T.total) / 10000))) + opt.zoom + (opt.fmt === "v" ? -0.35 : 0); }
  function camInicio() { return { center: [T.C[0].lon, T.C[0].lat], zoom: zoomBase(), pitch: 62, bearing: T.B[0] }; }
  function camVista(bearing, pitch) {
    var d = dims(), pad = Math.round(Math.min(d.w, d.h) * 0.14);
    var c = map.cameraForBounds(T.bounds, { padding: { top: pad, bottom: pad + (opt.perfil ? d.h * 0.18 : 0), left: pad, right: pad }, bearing: bearing, pitch: pitch, maxZoom: 15 });
    return { center: c ? [c.center.lng, c.center.lat] : [T.C[0].lon, T.C[0].lat], zoom: c ? c.zoom : 12, pitch: pitch, bearing: bearing };
  }
  var vistaIni = null, vistaFin = null;
  function prepararVistas() {
    vistaIni = camVista(0, 0);
    var bf = T.B[T.N - 1];
    vistaFin = camVista(bf - 25, 48);
  }
  function mezcla(a, b, t) {
    return { center: [lerp(a.center[0], b.center[0], t), lerp(a.center[1], b.center[1], t)], zoom: lerp(a.zoom, b.zoom, t), pitch: lerp(a.pitch, b.pitch, t), bearing: angLerp(a.bearing, b.bearing, t) };
  }
  /* coloca la cámara y la línea en el segundo s del vídeo; devuelve el avance 0..1 */
  function camara(s) {
    var D = opt.dur, fase, prog;
    if (s < TI) { fase = "ini"; prog = 0; }
    else if (s > D - TF) { fase = "fin"; prog = 1; }
    else { fase = "ruta"; prog = (s - TI) / (D - TI - TF); }
    var dist = T.total * prog, pos = enDist(T, dist);
    var q = Math.min(T.N - 1, Math.round(prog * (T.N - 1)));
    var ruta = { center: [T.C[q].lon, T.C[q].lat], zoom: zoomBase(), pitch: 62, bearing: T.B[q] };
    var cam;
    if (fase === "ini") cam = mezcla(vistaIni, camInicio(), suave(s / TI));
    else if (fase === "fin") { var tf = suave((s - (D - TF)) / TF); cam = mezcla(ruta, vistaFin, tf); }
    else cam = ruta;
    map.jumpTo(cam);
    var c = T.pts.slice(0, pos.i + 1).map(function (p) { return [p.lon, p.lat]; });
    c.push([pos.lon, pos.lat]);
    if (c.length < 2) c.push(c[0]);
    map.getSource("hecho").setData({ type: "Feature", geometry: { type: "LineString", coordinates: c } });
    map.getSource("pos").setData({ type: "Feature", geometry: { type: "Point", coordinates: [pos.lon, pos.lat] } });
    return { prog: prog, pos: pos, dist: dist };
  }

  /* ---------------------------------------------------------------- capa de datos (perfil, cifras, marca) */
  var logo = new Image(); logo.src = "/img/logo-adastra-pin.png";
  function caja(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
  function dibujarOverlay(s, ctx) {
    var d = dims(), propio = !ctx;
    if (propio) { if (ov.width !== d.w || ov.height !== d.h) { ov.width = d.w; ov.height = d.h; } ctx = ov.getContext("2d"); ctx.clearRect(0, 0, d.w, d.h); }
    if (!T) return;
    var k = Math.min(d.w, d.h) / 720, m = 26 * k, D = opt.dur;
    var prog = s < TI ? 0 : s > D - TF ? 1 : (s - TI) / (D - TI - TF), pos = enDist(T, T.total * prog);
    var ent0 = 1, sal = 1;
    ctx.save(); ctx.globalAlpha = ent0 * sal;
    ctx.shadowColor = "rgba(0,0,0,.55)"; ctx.shadowBlur = 10 * k;
    // título
    var tit = opt.titulo || T.name || "";
    ctx.fillStyle = "#fff"; ctx.textBaseline = "top";
    ctx.font = "800 " + Math.round(34 * k) + "px Inter, system-ui, sans-serif";
    var maxW = d.w - 2 * m;
    while (ctx.measureText(tit).width > maxW && tit.length > 4) tit = tit.slice(0, -2);
    if (tit !== (opt.titulo || T.name || "")) tit += "…";
    ctx.fillText(tit, m, m);
    var sub = km(T.total) + " km" + (T.ele ? " · +" + ent(T.up[T.up.length - 1]) + " m" : "") + (T.tiempo ? " · " + new Date(T.tiempo[0]).toLocaleDateString("es-ES", { day: "numeric", month: "long", year: "numeric" }) : "");
    ctx.font = "600 " + Math.round(19 * k) + "px Inter, system-ui, sans-serif"; ctx.fillStyle = "rgba(255,255,255,.92)";
    ctx.fillText(sub, m, m + 44 * k);
    ctx.restore();
    if (opt.perfil) {
      // cifras en directo
      var datos = [["Distancia", km(pos.dist != null ? pos.dist : T.total * prog) + " km"]];
      if (T.ele) { datos.push(["Altitud", ent(pos.ele) + " m"]); datos.push(["Desnivel +", ent(pos.up) + " m"]); }
      if (T.tiempo && isFinite(pos.t)) datos.push(["Tiempo", dur(pos.t - T.tiempo[0])]);
      var ph = (opt.fmt === "h" ? 0.2 : 0.15) * d.h, py = d.h - ph - m, bw = (d.w - 2 * m - (datos.length - 1) * 10 * k) / datos.length, bh = 58 * k, by = py - bh - 10 * k;
      ctx.save(); ctx.globalAlpha = ent0;
      datos.forEach(function (x, i) {
        var bx = m + i * (bw + 10 * k);
        caja(ctx, bx, by, bw, bh, 10 * k); ctx.fillStyle = "rgba(20,12,8,.62)"; ctx.fill();
        ctx.fillStyle = "rgba(255,255,255,.7)"; ctx.font = "600 " + Math.round(12.5 * k) + "px Inter, system-ui, sans-serif"; ctx.textBaseline = "top";
        ctx.fillText(x[0].toUpperCase(), bx + 12 * k, by + 9 * k);
        ctx.fillStyle = "#fff"; ctx.font = "800 " + Math.round(23 * k) + "px Inter, system-ui, sans-serif";
        ctx.fillText(x[1], bx + 12 * k, by + 26 * k);
      });
      // perfil
      caja(ctx, m, py, d.w - 2 * m, ph, 12 * k); ctx.fillStyle = "rgba(20,12,8,.62)"; ctx.fill();
      if (T.ele) {
        var e0 = T.emin, e1 = Math.max(T.emax, T.emin + 50), px = m + 14 * k, pw = d.w - 2 * m - 28 * k, pt = py + 12 * k, phh = ph - 24 * k;
        var X = function (dd) { return px + pw * dd / T.total; }, Y = function (v) { return pt + phh * (1 - (v - e0) / (e1 - e0)); };
        var paso = Math.max(1, Math.floor(T.pts.length / 600));
        function camino(hasta) {
          ctx.beginPath(); ctx.moveTo(X(0), pt + phh);
          for (var i = 0; i < T.pts.length && T.d[i] <= hasta; i += paso) ctx.lineTo(X(T.d[i]), Y(T.ele[i]));
          var e = enDist(T, hasta); ctx.lineTo(X(hasta), Y(e.ele)); ctx.lineTo(X(hasta), pt + phh); ctx.closePath();
        }
        camino(T.total); ctx.fillStyle = "rgba(255,255,255,.22)"; ctx.fill();
        if (prog > 0) { camino(T.total * prog); ctx.fillStyle = opt.color; ctx.globalAlpha = ent0 * 0.85; ctx.fill(); ctx.globalAlpha = ent0; }
        var cx = X(T.total * prog), cy = Y(pos.ele);
        ctx.beginPath(); ctx.arc(cx, cy, 6 * k, 0, 2 * Math.PI); ctx.fillStyle = "#fff"; ctx.fill(); ctx.lineWidth = 3 * k; ctx.strokeStyle = opt.color; ctx.stroke();
        ctx.fillStyle = "rgba(255,255,255,.75)"; ctx.font = "600 " + Math.round(12 * k) + "px Inter, system-ui, sans-serif"; ctx.textBaseline = "top";
        ctx.fillText(ent(e1) + " m", px, pt); ctx.textBaseline = "bottom"; ctx.fillText(ent(e0) + " m", px, pt + phh);
      } else {
        var bx2 = m + 14 * k, bw2 = d.w - 2 * m - 28 * k;
        caja(ctx, bx2, py + ph / 2 - 5 * k, bw2, 10 * k, 5 * k); ctx.fillStyle = "rgba(255,255,255,.25)"; ctx.fill();
        caja(ctx, bx2, py + ph / 2 - 5 * k, Math.max(10 * k, bw2 * prog), 10 * k, 5 * k); ctx.fillStyle = opt.color; ctx.fill();
      }
      ctx.restore();
    }
    // marca
    ctx.save(); ctx.globalAlpha = 0.92; ctx.shadowColor = "rgba(0,0,0,.6)"; ctx.shadowBlur = 8 * k;
    var lw = 30 * k, lh = lw * 401 / 300, txt = "guiasadastra.com";
    ctx.font = "800 " + Math.round(16 * k) + "px Inter, system-ui, sans-serif"; ctx.textBaseline = "middle";
    var tw = ctx.measureText(txt).width, lx = d.w - m - tw - lw - 8 * k, ly = m;
    if (logo.complete && logo.naturalWidth) ctx.drawImage(logo, lx, ly, lw, lh);
    ctx.fillStyle = "#fff"; ctx.fillText(txt, lx + lw + 8 * k, ly + lh / 2);
    ctx.restore();
    // atribución (obligatoria en las licencias de los datos)
    ctx.save(); ctx.font = "500 " + Math.round(10 * k) + "px Inter, system-ui, sans-serif"; ctx.textBaseline = "bottom"; ctx.textAlign = "right";
    ctx.fillStyle = "rgba(255,255,255,.75)"; ctx.shadowColor = "rgba(0,0,0,.8)"; ctx.shadowBlur = 4 * k;
    ctx.fillText(MAPAS[opt.mapa].attr + " · " + DEM_ATTR, d.w - 8 * k, d.h - 4 * k);
    ctx.restore();
  }

  /* ---------------------------------------------------------------- reproducción en directo */
  var anim = null;
  function reproducir() {
    if (!T || !listo) return;
    if (anim) { cancelAnimationFrame(anim.id); anim = null; $("v3-play").textContent = "▶ Ver animación"; return; }
    prepararVistas();
    var t0 = performance.now();
    $("v3-play").textContent = "■ Parar";
    anim = { id: 0 };
    (function paso() {
      var s = (performance.now() - t0) / 1000;
      if (s > opt.dur) { anim = null; $("v3-play").textContent = "▶ Ver animación"; return; }
      camara(s); dibujarOverlay(s);
      anim.id = requestAnimationFrame(paso);
    })();
  }

  /* ---------------------------------------------------------------- grabación fotograma a fotograma (WebCodecs + MP4) */
  function esperarRender(maxMs) {
    return new Promise(function (res) {
      var t0 = performance.now();
      function mira() {
        if ((map.areTilesLoaded() && map.loaded()) || performance.now() - t0 > maxMs) { res(); return; }
        map.once("render", function () { setTimeout(mira, 0); }); map.triggerRepaint();
      }
      map.once("render", function () { setTimeout(mira, 0); }); map.triggerRepaint();
    });
  }
  function cargarMuxer() {
    if (window.Mp4Muxer) return Promise.resolve();
    return new Promise(function (ok, ko) {
      var s = document.createElement("script"); s.src = "https://cdn.jsdelivr.net/npm/mp4-muxer@5.2.2/build/mp4-muxer.js"; s.onload = ok; s.onerror = function () { ko(new Error("No se ha podido cargar el generador de vídeo.")); }; document.head.appendChild(s);
    });
  }
  async function elegirCodec(w, h) {
    var lista = ["avc1.640034", "avc1.640028", "avc1.4d0028", "avc1.42E028", "avc1.42001f", "vp09.00.40.08", "vp09.00.31.08"];
    for (var i = 0; i < lista.length; i++) {
      var cfg = { codec: lista[i], width: w, height: h, bitrate: w * h * 30 * 0.28, framerate: 30 };
      if (lista[i].indexOf("avc") === 0) cfg.avc = { format: "avc" };
      try { var r = await VideoEncoder.isConfigSupported(cfg); if (r.supported) return cfg; } catch (e) {}
    }
    return null;
  }
  var grabando = false, cancelar = false;
  async function grabar() {
    if (grabando) { cancelar = true; return; }
    if (!T || !listo) return;
    if (!window.VideoEncoder || !window.VideoFrame) { aviso("Tu navegador no permite crear vídeos. Usa Chrome, Edge o Safari actualizados (o Firefox 130 o posterior).", true); return; }
    if (anim) reproducir();
    var d = dims(), cfg = await elegirCodec(d.w, d.h);
    if (!cfg) { aviso("Tu navegador no puede codificar vídeo MP4 a este tamaño. Prueba sin Full HD.", true); return; }
    try { await cargarMuxer(); } catch (e) { aviso(e.message, true); return; }
    grabando = true; cancelar = false;
    $("v3-rec").textContent = "Cancelar"; $("v3-play").disabled = true;
    var fps = 30, total = Math.round(opt.dur * fps), errorCod = null;
    var muxer = new Mp4Muxer.Muxer({ target: new Mp4Muxer.ArrayBufferTarget(), video: { codec: cfg.codec.indexOf("vp09") === 0 ? "vp9" : "avc", width: d.w, height: d.h, frameRate: fps }, fastStart: "in-memory" });
    var enc = new VideoEncoder({ output: function (ch, meta) { muxer.addVideoChunk(ch, meta); }, error: function (e) { errorCod = e; } });
    enc.configure(cfg);
    var cv = document.createElement("canvas"); cv.width = d.w; cv.height = d.h;
    var ctx = cv.getContext("2d");
    prepararVistas();
    var t0 = performance.now();
    try {
      for (var f = 0; f < total; f++) {
        if (cancelar || errorCod) break;
        var s = f / fps;
        camara(s);
        await esperarRender(f === 0 ? 20000 : 6000);
        ctx.drawImage(map.getCanvas(), 0, 0, d.w, d.h);
        dibujarOverlay(s, ctx);
        var vf = new VideoFrame(cv, { timestamp: Math.round(f * 1e6 / fps), duration: Math.round(1e6 / fps) });
        enc.encode(vf, { keyFrame: f % (fps * 2) === 0 });
        vf.close();
        while (enc.encodeQueueSize > 6) await new Promise(function (r) { setTimeout(r, 5); });
        if (f % 5 === 0) {
          dibujarOverlay(s);
          var pc = (f + 1) / total, quedan = (performance.now() - t0) / pc * (1 - pc) / 1000;
          estado.innerHTML = '<div class="v3-bar"><i style="width:' + (pc * 100).toFixed(1) + '%"></i></div>Creando el vídeo: ' + Math.round(pc * 100) + " %" + (f > 30 ? " · quedan unos " + Math.max(1, Math.round(quedan)) + " s" : "");
        }
      }
      if (errorCod) throw errorCod;
      if (cancelar) { estado.textContent = "Cancelado."; enc.close(); return; }
      await enc.flush(); enc.close(); muxer.finalize();
      var blob = new Blob([muxer.target.buffer], { type: "video/mp4" }), url = URL.createObjectURL(blob);
      var nombre = (opt.titulo || T.name || "ruta").replace(/[\\/:*?"<>|]+/g, "-").slice(0, 60) + " - 3D.mp4";
      estado.innerHTML = '<p class="v3-ok">Vídeo listo (' + (blob.size / 1048576).toFixed(1).replace(".", ",") + ' MB).</p><a class="btn btn-primary" href="' + url + '" download="' + esc(nombre) + '">Descargar el vídeo</a><video class="v3-vid" src="' + url + '" controls playsinline></video>';
    } catch (e) {
      console.error(e); aviso("Ha fallado la creación del vídeo: " + (e.message || e) + ". Prueba sin Full HD o con otro navegador.", true);
    } finally {
      grabando = false; $("v3-rec").textContent = "Crear vídeo MP4"; $("v3-play").disabled = !T;
    }
  }

  /* ---------------------------------------------------------------- eventos */
  function aviso(txt, malo) { estado.innerHTML = '<p class="' + (malo ? "v3-err" : "v3-ok") + '">' + esc(txt) + "</p>"; }
  function usar(texto, nombre) {
    try {
      T = preparar(leer(texto, nombre));
      $("v3-nom").innerHTML = "<b>" + esc(T.name) + "</b><br>" + km(T.total) + " km" + (T.ele ? " · +" + ent(T.up[T.up.length - 1]) + " m · " + ent(T.emin) + "–" + ent(T.emax) + " m" : " · sin altitud") + (T.tiempo ? " · " + dur(T.tiempo[1] - T.tiempo[0]) : "");
      $("v3-tit").placeholder = T.name;
      $("v3-play").disabled = false; $("v3-rec").disabled = false; $("v3-drop").style.display = "none";
      estado.innerHTML = "";
      if (listo) { cargarTrack(); prepararVistas(); camara(0); map.jumpTo(vistaIni); dibujarOverlay(0); }
      else crearMapa();
    } catch (e) { aviso(e.message, true); }
  }
  $("v3-file").addEventListener("change", function (e) {
    var f = e.target.files[0]; if (!f) return;
    var rd = new FileReader(); rd.onload = function () { usar(rd.result, f.name); }; rd.readAsText(f); e.target.value = "";
  });
  $("v3-demo").addEventListener("click", function () { fetch("/data/ejemplo-laguna-grande.gpx").then(function (r) { return r.text(); }).then(function (t) { usar(t, "ejemplo.gpx"); }); });
  marco.addEventListener("dragover", function (e) { e.preventDefault(); marco.classList.add("v3-arr"); });
  marco.addEventListener("dragleave", function () { marco.classList.remove("v3-arr"); });
  marco.addEventListener("drop", function (e) {
    e.preventDefault(); marco.classList.remove("v3-arr");
    var f = e.dataTransfer.files[0]; if (!f) return;
    var rd = new FileReader(); rd.onload = function () { usar(rd.result, f.name); }; rd.readAsText(f);
  });
  function cambio(rehacer) {
    if (grabando) return;
    if (anim) reproducir();
    if (rehacer) crearMapa();
    else if (listo && T) { ajustarEscala(); prepararVistas(); camara(0); map.jumpTo(vistaIni); dibujarOverlay(0); }
  }
  $("v3-tit").addEventListener("input", function (e) { opt.titulo = e.target.value.trim(); dibujarOverlay(0); });
  $("v3-mapa").addEventListener("change", function (e) { opt.mapa = e.target.value; cambio(true); });
  $("v3-fmt").addEventListener("change", function (e) { opt.fmt = e.target.value; cambio(true); });
  $("v3-hd").addEventListener("change", function (e) { opt.hd = e.target.checked; cambio(true); });
  $("v3-dur").addEventListener("change", function (e) { opt.dur = +e.target.value; cambio(false); });
  $("v3-zoom").addEventListener("change", function (e) { opt.zoom = +e.target.value; cambio(false); });
  $("v3-rel").addEventListener("change", function (e) { opt.relieve = +e.target.value; if (listo) map.setTerrain({ source: "dem", exaggeration: opt.relieve }); cambio(false); });
  $("v3-col").addEventListener("input", function (e) {
    opt.color = e.target.value;
    if (listo) { ["hecho", "pos"].forEach(function (l) { map.setPaintProperty(l, l === "pos" ? "circle-color" : "line-color", opt.color); }); map.setPaintProperty("pos-h", "circle-color", opt.color); }
    dibujarOverlay(0);
  });
  $("v3-perf").addEventListener("change", function (e) { opt.perfil = e.target.checked; cambio(false); });
  $("v3-play").addEventListener("click", reproducir);
  $("v3-rec").addEventListener("click", grabar);
  window.addEventListener("resize", function () { if (!grabando) ajustarEscala(); });

  crearMapa();
  // track enviado desde el editor GPX
  try {
    var desdeEditor = sessionStorage.getItem("gx-video");
    if (desdeEditor) { sessionStorage.removeItem("gx-video"); usar(desdeEditor, "track.gpx"); }
  } catch (e) {}
  window.__v3 = { opt: opt, map: function () { return map; }, T: function () { return T; } };
})();
