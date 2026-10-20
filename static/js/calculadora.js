/* Guías Ad Astra · Calculadora de rutas (tiempo estimado y análisis de tracks GPX/KML/TCX) */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var nf1 = new Intl.NumberFormat("es-ES", { maximumFractionDigits: 1, minimumFractionDigits: 1 });
  var nf0 = new Intl.NumberFormat("es-ES", { maximumFractionDigits: 0 });

  /* ---------- método de cálculo (MIDE, FEDME) ----------
     Horizontal: distancia / velocidad en llano.
     Vertical:   metros de subida / ritmo de subida + metros de bajada / ritmo de bajada.
     Total:      el mayor de los dos + la mitad del menor.
     MIDE oficial: 4 km/h, 400 m/h de subida y 600 m/h de bajada (sin paradas).
     En un track se calcula por tramos y se suman, como indica el método. */
  var METHODS = {
    mide: { kmh: 4, up: 400, down: 600, name: "MIDE oficial" },
    guia: { kmh: 4.5, up: 300, down: 500, name: "ritmo de guía" },
    naismith: { kmh: 5, up: 600, down: 0, name: "regla de Naismith", sum: true }
  };
  function estimate(km, up, down, kmh, upRate, downRate, sum) {
    var h = km / kmh;
    var v = (upRate > 0 ? up / upRate : 0) + (downRate > 0 ? down / downRate : 0);
    var total = sum ? h + v : Math.max(h, v) + Math.min(h, v) / 2; // Naismith suma; MIDE: mayor + mitad del menor
    return { h: h, v: v, total: total };
  }
  function hm(hours) {
    if (!isFinite(hours) || hours <= 0) return "0 min";
    var m = Math.round(hours * 60 / 5) * 5; // redondeo a 5 minutos
    var hh = Math.floor(m / 60), mm = m % 60;
    return (hh ? hh + " h" : "") + (hh && mm ? " " : "") + (mm || !hh ? mm + " min" : "");
  }
  /* Esfuerzo necesario según MIDE (horas de marcha efectiva, sin paradas) */
  function esfuerzo(t) {
    if (t <= 1) return [1, "Hasta 1 h de marcha efectiva."];
    if (t <= 3) return [2, "De 1 a 3 h de marcha efectiva."];
    if (t <= 6) return [3, "De 3 a 6 h de marcha efectiva."];
    if (t <= 10) return [4, "De 6 a 10 h de marcha efectiva."];
    return [5, "Más de 10 h de marcha efectiva."];
  }
  function params() {
    var m = ($("[name=metodo]:checked") || {}).value || "mide";
    return {
      method: m,
      kmh: parseFloat(String($("#c-llano").value).replace(",", ".")) || METHODS[m].kmh,
      up: parseFloat($("#c-subida").value) || METHODS[m].up,
      down: parseFloat($("#c-bajada").value) || 0,
      sum: !!METHODS[m].sum,
      stops: parseFloat($("#c-paradas").value) || 0
    };
  }
  function methodText(p) {
    var n = { mide: "Método MIDE", guia: "Ritmo de guía", naismith: "Regla de Naismith" }[p.method];
    return n + ": " + nf1.format(p.kmh) + " km/h en llano, " + nf0.format(p.up) + " m/h de subida" + (p.down ? " y " + nf0.format(p.down) + " m/h de bajada" : "") + (p.sum ? " (tiempos sumados)" : "");
  }
  function stopsText(p, short) {
    return p.stops ? (short ? ", con " + Math.round(p.stops * 100) + " % de paradas" : "Incluye un " + Math.round(p.stops * 100) + " % de margen para descansos, comer e imprevistos.") : (short ? ", sin paradas" : "Tiempo en movimiento, sin paradas.");
  }

  /* ---------- calculadora manual ---------- */
  var form = $("#calc");
  function renderResult(box, km, up, down, p) {
    var r = estimate(km, up, down, p.kmh, p.up, p.down, p.sum);
    var total = r.total * (1 + p.stops);
    var d = esfuerzo(r.total);
    var start = new Date(); start.setHours(9, 0, 0, 0);
    var end = new Date(start.getTime() + total * 3600e3);
    box.innerHTML =
      '<div class="calc-big"><span class="label">Duración aproximada</span><strong>' + hm(total) + "</strong>" +
      '<span class="muted">' + stopsText(p) + " " + methodText(p) + ".</span></div>" +
      '<dl class="calc-parts">' +
      "<div><dt>Por distancia</dt><dd>" + hm(r.h) + "<small>" + nf1.format(km) + " km a " + nf1.format(p.kmh) + " km/h</small></dd></div>" +
      "<div><dt>Por desnivel</dt><dd>" + hm(r.v) + "<small>+" + nf0.format(up) + " m a " + nf0.format(p.up) + " m/h" + (p.down && down ? " · −" + nf0.format(down) + " m a " + nf0.format(p.down) + " m/h" : "") + "</small></dd></div>" +
      "<div><dt>Esfuerzo MIDE</dt><dd>" + d[0] + " de 5<small>" + d[1] + "</small></dd></div>" +
      "<div><dt>Si sales a las 9:00</dt><dd>" + end.getHours() + ":" + String(end.getMinutes()).padStart(2, "0") + "<small>Hora aproximada de llegada.</small></dd></div>" +
      "</dl>";
    return total;
  }
  if (form) {
    var out = $("#calc-out");
    var run = function () {
      var km = parseFloat(String($("#c-km").value).replace(",", ".")) || 0;
      var up = parseFloat($("#c-up").value) || 0;
      var down = $("#c-down").value === "" ? up : (parseFloat($("#c-down").value) || 0);
      $("#c-down").placeholder = up ? String(up) : "igual que la subida";
      if (!km && !up) { out.innerHTML = '<p class="muted">Escribe la distancia y el desnivel para ver la duración.</p>'; return; }
      renderResult(out, km, up, down, params());
      if (lastTrack) showTrack(lastTrack);
    };
    $$("input", form).forEach(function (i) { i.addEventListener("input", run); i.addEventListener("change", run); });
    var applyMethod = function () {
      var m = ($("[name=metodo]:checked") || {}).value || "mide", d = METHODS[m];
      $("#ritmo-wrap").hidden = m !== "guia";
      var r = $("[name=ritmo]:checked");
      $("#c-llano").value = m === "guia" && r ? r.value : d.kmh;
      $("#c-subida").value = d.up; $("#c-bajada").value = d.down;
    };
    $$("[name=metodo]").forEach(function (i) { i.addEventListener("change", function () { applyMethod(); run(); }); });
    $$("[name=ritmo]").forEach(function (i) { i.addEventListener("change", function () { $("#c-llano").value = i.value; run(); }); });
    $$("#ajustes input:not([name=metodo]):not([name=ritmo])").forEach(function (i) { i.addEventListener("input", run); i.addEventListener("change", run); });
    $("#c-paradas").addEventListener("change", run);
    applyMethod();
    form.addEventListener("submit", function (e) { e.preventDefault(); run(); });
    run();
  }

  /* ---------- lectura de tracks ---------- */
  function parseTrack(text, name) {
    var doc = new DOMParser().parseFromString(text, "application/xml");
    if (doc.getElementsByTagName("parsererror").length) throw new Error("El archivo no es un GPX, KML o TCX válido.");
    var pts = [];
    var nodes = doc.getElementsByTagName("trkpt");
    if (!nodes.length) nodes = doc.getElementsByTagName("rtept");
    if (nodes.length) {
      for (var i = 0; i < nodes.length; i++) {
        var n = nodes[i], e = n.getElementsByTagName("ele")[0], t = n.getElementsByTagName("time")[0];
        pts.push({ lat: +n.getAttribute("lat"), lon: +n.getAttribute("lon"), ele: e ? parseFloat(e.textContent) : NaN, t: t ? Date.parse(t.textContent) : NaN });
      }
    } else if (doc.getElementsByTagName("Trackpoint").length) { // TCX
      var tp = doc.getElementsByTagName("Trackpoint");
      for (var j = 0; j < tp.length; j++) {
        var la = tp[j].getElementsByTagName("LatitudeDegrees")[0], lo = tp[j].getElementsByTagName("LongitudeDegrees")[0];
        if (!la || !lo) continue;
        var al = tp[j].getElementsByTagName("AltitudeMeters")[0], ti = tp[j].getElementsByTagName("Time")[0];
        pts.push({ lat: +la.textContent, lon: +lo.textContent, ele: al ? parseFloat(al.textContent) : NaN, t: ti ? Date.parse(ti.textContent) : NaN });
      }
    } else { // KML: LineString o gx:Track
      var coords = doc.getElementsByTagName("coordinates");
      for (var k = 0; k < coords.length; k++) {
        coords[k].textContent.trim().split(/\s+/).forEach(function (c) {
          var v = c.split(","); if (v.length >= 2) pts.push({ lat: +v[1], lon: +v[0], ele: v[2] != null ? parseFloat(v[2]) : NaN, t: NaN });
        });
      }
      var gx = doc.getElementsByTagNameNS("*", "coord");
      for (var g = 0; g < gx.length; g++) { var w = gx[g].textContent.trim().split(/\s+/); pts.push({ lat: +w[1], lon: +w[0], ele: parseFloat(w[2]), t: NaN }); }
    }
    pts = pts.filter(function (p) { return isFinite(p.lat) && isFinite(p.lon); });
    if (pts.length < 2) throw new Error("No hemos encontrado puntos de recorrido en el archivo.");
    var nm = (doc.getElementsByTagName("name")[0] || {}).textContent || name.replace(/\.[^.]+$/, "");
    return { name: nm.trim(), pts: pts };
  }
  function hav(a, b) {
    var R = 6371000, r = Math.PI / 180, dLat = (b.lat - a.lat) * r, dLon = (b.lon - a.lon) * r;
    var x = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(a.lat * r) * Math.cos(b.lat * r) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    return 2 * R * Math.asin(Math.sqrt(x));
  }
  function analyse(tr) {
    var p = tr.pts, dist = [0], hasEle = p.some(function (x) { return isFinite(x.ele); });
    for (var i = 1; i < p.length; i++) dist.push(dist[i - 1] + hav(p[i - 1], p[i]));
    // altitudes: rellenar huecos y suavizar (media móvil por distancia ~60 m) para no inflar el desnivel
    var ele = p.map(function (x) { return x.ele; });
    if (hasEle) {
      var last = ele.find(function (v) { return isFinite(v); });
      for (var a = 0; a < ele.length; a++) { if (isFinite(ele[a])) last = ele[a]; else ele[a] = last; }
    }
    var sm = ele.slice();
    if (hasEle) {
      for (var b = 0, lo = 0, hi = 0, sum = 0; b < ele.length; b++) {
        while (hi < ele.length && dist[hi] - dist[b] <= 30) { sum += ele[hi]; hi++; }
        while (dist[b] - dist[lo] > 30) { sum -= ele[lo]; lo++; }
        sm[b] = sum / (hi - lo);
      }
    }
    var up = 0, down = 0, ref = sm[0], th = 3;
    if (hasEle) for (var c = 1; c < sm.length; c++) {
      var dz = sm[c] - ref;
      if (dz >= th) { up += dz; ref = sm[c]; } else if (dz <= -th) { down -= dz; ref = sm[c]; }
    }
    var maxE = -Infinity, minE = Infinity, maxI = 0, minI = 0;
    if (hasEle) sm.forEach(function (v, i) { if (v > maxE) { maxE = v; maxI = i; } if (v < minE) { minE = v; minI = i; } });
    // pendiente máxima sostenida en tramos de ~200 m
    var maxSlope = 0, j = 0;
    if (hasEle) for (var s = 0; s < sm.length; s++) {
      while (j < sm.length - 1 && dist[j] - dist[s] < 200) j++;
      if (dist[j] - dist[s] >= 150) maxSlope = Math.max(maxSlope, Math.abs(sm[j] - sm[s]) / (dist[j] - dist[s]) * 100);
    }
    var t0 = p[0].t, t1 = p[p.length - 1].t, real = isFinite(t0) && isFinite(t1) && t1 > t0 ? (t1 - t0) / 3600e3 : 0;
    var loop = hav(p[0], p[p.length - 1]) < 250;
    return { name: tr.name, pts: p, dist: dist, ele: sm, hasEle: hasEle, km: dist[dist.length - 1] / 1000, up: up, down: down, maxE: maxE, minE: minE, maxI: maxI, minI: minI, maxSlope: maxSlope, real: real, loop: loop, startT: t0 };
  }

  /* tiempo MIDE por tramos de ~250 m (más preciso que con los totales) */
  function trackTime(A, p) {
    var tot = 0, th = 0, tv = 0, i = 0, n = A.pts.length;
    while (i < n - 1) {
      var j = i + 1; while (j < n - 1 && A.dist[j] - A.dist[i] < 250) j++;
      var km = (A.dist[j] - A.dist[i]) / 1000, dz = A.hasEle ? A.ele[j] - A.ele[i] : 0;
      var r = estimate(km, Math.max(dz, 0), Math.max(-dz, 0), p.kmh, p.up, p.down, p.sum);
      tot += r.total; th += r.h; tv += r.v; i = j;
    }
    return { total: tot, h: th, v: tv };
  }

  /* ---------- perfil (SVG) ---------- */
  function niceStep(range, n) {
    var raw = range / n, pow = Math.pow(10, Math.floor(Math.log10(raw))), f = raw / pow;
    return (f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10) * pow;
  }
  function drawProfile(A, box, onHover) {
    if (!A.hasEle) { box.innerHTML = '<p class="muted">Este track no tiene altitudes, así que no podemos dibujar el perfil. Puedes usar el desnivel de la ficha de la ruta en la calculadora de arriba.</p>'; return; }
    var W = 1000, H = 300, L = 54, R = 16, T = 16, B = 34;
    var kmMax = A.km, eMin = A.minE, eMax = A.maxE, pad = Math.max(20, (eMax - eMin) * 0.08);
    var yStep = niceStep(eMax - eMin + 2 * pad, 4); var y0 = Math.floor((eMin - pad) / yStep) * yStep, y1 = Math.ceil((eMax + pad) / yStep) * yStep;
    var xStep = niceStep(kmMax, 6);
    var X = function (km) { return L + (km / kmMax) * (W - L - R); }, Y = function (e) { return T + (1 - (e - y0) / (y1 - y0)) * (H - T - B); };
    var n = A.pts.length, stride = Math.max(1, Math.floor(n / 1500)), line = "";
    for (var i = 0; i < n; i += stride) line += (i ? "L" : "M") + X(A.dist[i] / 1000).toFixed(1) + " " + Y(A.ele[i]).toFixed(1);
    line += "L" + X(kmMax).toFixed(1) + " " + Y(A.ele[n - 1]).toFixed(1);
    var area = line + "L" + X(kmMax).toFixed(1) + " " + Y(y0) + "L" + L + " " + Y(y0) + "Z";
    var grid = "", lab = "";
    for (var y = y0; y <= y1 + 0.01; y += yStep) { grid += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + Y(y) + '" y2="' + Y(y) + '"/>'; lab += '<text x="' + (L - 8) + '" y="' + (Y(y) + 4) + '" text-anchor="end">' + nf0.format(y) + "</text>"; }
    for (var x = 0; x <= kmMax + 1e-6; x += xStep) lab += '<text x="' + X(x) + '" y="' + (H - 10) + '" text-anchor="middle">' + (Math.round(x * 10) / 10).toString().replace(".", ",") + "</text>";
    var mx = X(A.dist[A.maxI] / 1000), my = Y(A.ele[A.maxI]);
    box.innerHTML = '<svg viewBox="0 0 ' + W + " " + H + '" class="prof-svg" role="img" aria-label="Perfil de altitud: de ' + nf0.format(eMin) + " a " + nf0.format(eMax) + ' metros">' +
      '<defs><linearGradient id="pg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#e9a53b" stop-opacity=".55"/><stop offset="1" stop-color="#d9661f" stop-opacity=".05"/></linearGradient></defs>' +
      '<g class="grid">' + grid + "</g>" + '<path d="' + area + '" fill="url(#pg)"/><path d="' + line + '" fill="none" stroke="#f0b445" stroke-width="2.2" stroke-linejoin="round"/>' +
      '<circle cx="' + mx + '" cy="' + my + '" r="5" fill="#f3e9df" stroke="#160d09" stroke-width="2"/><text class="peak" x="' + Math.min(Math.max(mx, L + 40), W - R - 40) + '" y="' + Math.max(my - 12, 12) + '" text-anchor="middle">' + nf0.format(eMax) + " m</text>" +
      '<g class="axis">' + lab + '<text x="' + (W - R) + '" y="' + (H - 10) + '" text-anchor="end" class="unit"> km</text></g>' +
      '<g class="hover" visibility="hidden"><line y1="' + T + '" y2="' + (H - B) + '"/><circle r="5"/></g>' +
      '<rect class="hit" x="' + L + '" y="' + T + '" width="' + (W - L - R) + '" height="' + (H - T - B) + '" fill="transparent"/></svg>' +
      '<div class="prof-tip" hidden></div>';
    var svg = $("svg", box), hv = $(".hover", svg), tip = $(".prof-tip", box), hit = $(".hit", svg);
    function move(ev) {
      var rc = svg.getBoundingClientRect(), cx = ((ev.touches ? ev.touches[0].clientX : ev.clientX) - rc.left) / rc.width * W;
      var km = Math.max(0, Math.min(kmMax, (cx - L) / (W - L - R) * kmMax)), m = km * 1000;
      var lo = 0, hi = n - 1; while (hi - lo > 1) { var mid = (lo + hi) >> 1; if (A.dist[mid] < m) lo = mid; else hi = mid; }
      var e = A.ele[hi], px = X(A.dist[hi] / 1000), py = Y(e);
      hv.setAttribute("visibility", "visible"); $("line", hv).setAttribute("x1", px); $("line", hv).setAttribute("x2", px); $("circle", hv).setAttribute("cx", px); $("circle", hv).setAttribute("cy", py);
      var back = Math.max(0, hi - 1); while (back > 0 && A.dist[hi] - A.dist[back] < 100) back--;
      var sl = A.dist[hi] - A.dist[back] > 20 ? (A.ele[hi] - A.ele[back]) / (A.dist[hi] - A.dist[back]) * 100 : 0;
      tip.hidden = false; tip.style.left = (px / W * 100) + "%";
      tip.innerHTML = "<b>km " + nf1.format(A.dist[hi] / 1000) + "</b> · " + nf0.format(e) + " m · " + (sl >= 0 ? "+" : "") + nf0.format(sl) + " %";
      onHover && onHover(hi);
    }
    hit.addEventListener("mousemove", move); hit.addEventListener("touchmove", function (e) { move(e); }, { passive: true });
    hit.addEventListener("mouseleave", function () { hv.setAttribute("visibility", "hidden"); tip.hidden = true; onHover && onHover(-1); });
  }

  /* ---------- mapa (Leaflet si está disponible) ---------- */
  var map, layer, marker;
  function drawMap(A) {
    var el = $("#trk-map");
    var mb = $("[data-dl=mapa]");
    if (!window.L) { el.hidden = true; if (mb) mb.hidden = true; return; }
    if (mb) mb.hidden = false;
    el.hidden = false;
    if (!map) {
      map = L.map(el, { scrollWheelZoom: false });
      L.tileLayer("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", { maxZoom: 17, crossOrigin: "anonymous", attribution: "© OpenStreetMap · © OpenTopoMap" }).addTo(map);
    }
    if (layer) layer.remove(); if (marker) marker.remove();
    var ll = A.pts.map(function (p) { return [p.lat, p.lon]; });
    map.invalidateSize();
    map.fitBounds(L.latLngBounds(ll), { padding: [24, 24], animate: false });
    layer = L.layerGroup([
      L.polyline(ll, { color: "#160d09", weight: 7, opacity: .6 }),
      L.polyline(ll, { color: "#f0b445", weight: 4 }),
      L.circleMarker(ll[0], { radius: 7, color: "#160d09", weight: 2, fillColor: "#5cb87a", fillOpacity: 1 }).bindTooltip("Salida"),
      L.circleMarker(ll[ll.length - 1], { radius: 7, color: "#160d09", weight: 2, fillColor: "#c9533b", fillOpacity: 1 }).bindTooltip("Llegada")
    ]).addTo(map);
    marker = L.circleMarker(ll[0], { radius: 6, color: "#fff", weight: 2, fillColor: "#e9a53b", opacity: 0, fillOpacity: 0 }).addTo(map);
    setTimeout(function () { map.invalidateSize(); map.fitBounds(L.latLngBounds(ll), { padding: [24, 24], animate: false }); }, 60);
  }

  /* ---------- mostrar análisis ---------- */
  var lastTrack = null;
  function showTrack(A) {
    lastTrack = A;
    var p = params();
    var r = trackTime(A, p), total = r.total * (1 + p.stops);
    var d = esfuerzo(r.total);
    A.calc = { total: total, esfuerzo: d[0], p: p };
    var res = $("#trk-res"); res.hidden = false;
    $("#trk-name").textContent = A.name || "Tu ruta";
    var stats = [
      ["Distancia", nf1.format(A.km) + " km"],
      ["Desnivel +", A.hasEle ? nf0.format(A.up) + " m" : "—"],
      ["Desnivel −", A.hasEle ? nf0.format(A.down) + " m" : "—"],
      ["Altitud máx.", A.hasEle ? nf0.format(A.maxE) + " m" : "—"],
      ["Altitud mín.", A.hasEle ? nf0.format(A.minE) + " m" : "—"],
      ["Pendiente máx.", A.hasEle ? nf0.format(A.maxSlope) + " %" : "—"],
      ["Duración estimada", hm(total)],
      ["Esfuerzo MIDE", d[0] + " de 5"],
      ["Tipo", A.loop ? "Circular" : "Lineal (ida)"]
    ];
    if (A.real) stats.push(["Tiempo real del track", hm(A.real)]);
    var n = stats.length; $("#trk-stats").style.setProperty("--cols", n % 5 === 0 ? 5 : n % 4 === 0 ? 4 : 3);
    $("#trk-stats").innerHTML = stats.map(function (s) { return "<div><dt>" + s[0] + "</dt><dd>" + s[1] + "</dd></div>"; }).join("");
    $("#trk-note").textContent = "Duración calculada por tramos de 250 m. " + methodText(p) + stopsText(p, true) + ". Esfuerzo MIDE " + d[0] + ": " + d[1].toLowerCase();
    drawProfile(A, $("#trk-prof"), function (i) {
      if (!marker) return;
      if (i < 0) { marker.setStyle({ opacity: 0, fillOpacity: 0 }); return; }
      marker.setLatLng([A.pts[i].lat, A.pts[i].lon]); marker.setStyle({ opacity: 1, fillOpacity: 1 });
    });
    drawMap(A);
  }
  /* ---------- descargas (PNG) ---------- */
  var C = { bg: "#160d09", card: "#25170f", line: "#3a271b", fg: "#f3e9df", muted: "#b9a593", dim: "#8a7564", gold: "#e9a53b", orange: "#d9661f" };
  var DISP = '"Bebas Neue","Oswald","Arial Narrow",Impact,sans-serif', BODY = '"Barlow",system-ui,sans-serif', LAB = '"Barlow Condensed","Arial Narrow",sans-serif';
  function slug(s) { return (s || "ruta").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60) || "ruta"; }
  function save(canvas, name) {
    try {
      canvas.toBlob(function (b) {
        if (!b) return alertErr();
        var a = document.createElement("a"); a.href = URL.createObjectURL(b); a.download = name; document.body.appendChild(a); a.click();
        setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 2000);
      }, "image/png");
    } catch (e) { alertErr(); }
  }
  function alertErr() { $("#trk-err").textContent = "No se pudo generar la imagen. Prueba de nuevo cuando el mapa termine de cargar."; }
  function profileTo(ctx, A, x, y, w, h, k) {
    ctx.save(); ctx.fillStyle = C.card; ctx.fillRect(x, y, w, h);
    if (!A.hasEle) { ctx.fillStyle = C.muted; ctx.font = 16 * k + "px " + BODY; ctx.fillText("Este track no tiene altitudes.", x + 20 * k, y + h / 2); ctx.restore(); return; }
    var L = x + 64 * k, R = x + w - 20 * k, T = y + 30 * k, B = y + h - 40 * k;
    var pad = Math.max(20, (A.maxE - A.minE) * 0.08), st = niceStep(A.maxE - A.minE + 2 * pad, 4);
    var y0 = Math.floor((A.minE - pad) / st) * st, y1 = Math.ceil((A.maxE + pad) / st) * st, xs = niceStep(A.km, 6);
    var X = function (km) { return L + km / A.km * (R - L); }, Y = function (e) { return T + (1 - (e - y0) / (y1 - y0)) * (B - T); };
    ctx.font = 600 * 0 + 14 * k + "px " + LAB; ctx.textBaseline = "middle";
    ctx.strokeStyle = C.line; ctx.lineWidth = 1 * k; ctx.setLineDash([3 * k, 5 * k]); ctx.fillStyle = C.dim; ctx.textAlign = "right";
    for (var v = y0; v <= y1 + 0.01; v += st) { ctx.beginPath(); ctx.moveTo(L, Y(v)); ctx.lineTo(R, Y(v)); ctx.stroke(); ctx.fillText(nf0.format(v) + " m", L - 10 * k, Y(v)); }
    ctx.setLineDash([]); ctx.textAlign = "center";
    for (var q = 0; q <= A.km + 1e-6; q += xs) ctx.fillText(String(Math.round(q * 10) / 10).replace(".", ",") + " km", X(q), B + 22 * k);
    var n = A.pts.length, stride = Math.max(1, Math.floor(n / 2000));
    ctx.beginPath(); ctx.moveTo(X(0), Y(A.ele[0]));
    for (var i = 0; i < n; i += stride) ctx.lineTo(X(A.dist[i] / 1000), Y(A.ele[i]));
    ctx.lineTo(X(A.km), Y(A.ele[n - 1]));
    var line = new Path2D(); line.moveTo(X(0), Y(A.ele[0])); for (var j = 0; j < n; j += stride) line.lineTo(X(A.dist[j] / 1000), Y(A.ele[j])); line.lineTo(X(A.km), Y(A.ele[n - 1]));
    ctx.lineTo(X(A.km), B); ctx.lineTo(X(0), B); ctx.closePath();
    var g = ctx.createLinearGradient(0, T, 0, B); g.addColorStop(0, "rgba(233,165,59,.55)"); g.addColorStop(1, "rgba(217,102,31,.05)"); ctx.fillStyle = g; ctx.fill();
    ctx.strokeStyle = "#f0b445"; ctx.lineWidth = 2.5 * k; ctx.lineJoin = "round"; ctx.stroke(line);
    var mx = X(A.dist[A.maxI] / 1000), my = Y(A.ele[A.maxI]);
    ctx.beginPath(); ctx.arc(mx, my, 5 * k, 0, 7); ctx.fillStyle = C.fg; ctx.fill(); ctx.lineWidth = 2 * k; ctx.strokeStyle = C.bg; ctx.stroke();
    ctx.fillStyle = C.fg; ctx.font = "600 " + 15 * k + "px " + LAB; ctx.fillText(nf0.format(A.maxE) + " m", Math.min(Math.max(mx, L + 40 * k), R - 40 * k), Math.max(my - 16 * k, y + 12 * k));
    ctx.restore();
  }
  function mapTo(ctx, x, y, w, h, A, withTiles, k) {
    var el = $("#trk-map"), rc = el.getBoundingClientRect(), sx = w / rc.width, sy = h / rc.height, u = k || 2;
    ctx.save(); ctx.beginPath(); ctx.rect(x, y, w, h); ctx.clip(); ctx.fillStyle = "#e8e2d4"; ctx.fillRect(x, y, w, h);
    if (withTiles) $$(".leaflet-tile-loaded", el).forEach(function (t) {
      var r = t.getBoundingClientRect(); ctx.drawImage(t, x + (r.left - rc.left) * sx, y + (r.top - rc.top) * sy, r.width * sx, r.height * sy);
    });
    var pt = function (p) { var c = map.latLngToContainerPoint([p.lat, p.lon]); return [x + c.x * sx, y + c.y * sy]; };
    ctx.lineJoin = "round"; ctx.lineCap = "round";
    [[C.bg, 7, .6], ["#f0b445", 4, 1]].forEach(function (s) {
      ctx.beginPath(); A.pts.forEach(function (p, i) { var c = pt(p); i ? ctx.lineTo(c[0], c[1]) : ctx.moveTo(c[0], c[1]); });
      ctx.strokeStyle = s[0]; ctx.globalAlpha = s[2]; ctx.lineWidth = s[1] * u; ctx.stroke(); ctx.globalAlpha = 1;
    });
    [[A.pts[0], "#5cb87a"], [A.pts[A.pts.length - 1], "#c9533b"]].forEach(function (m) { var c = pt(m[0]); ctx.beginPath(); ctx.arc(c[0], c[1], 7 * u, 0, 7); ctx.fillStyle = m[1]; ctx.fill(); ctx.lineWidth = 2 * u; ctx.strokeStyle = C.bg; ctx.stroke(); });
    var at = "© OpenStreetMap · © OpenTopoMap"; ctx.font = 12 * u + "px " + BODY; var tw = ctx.measureText(at).width;
    ctx.fillStyle = "rgba(255,255,255,.8)"; ctx.fillRect(x + w - tw - 14 * u, y + h - 20 * u, tw + 14 * u, 20 * u); ctx.fillStyle = "#333"; ctx.textBaseline = "middle"; ctx.textAlign = "left"; ctx.fillText(at, x + w - tw - 7 * u, y + h - 10 * u);
    ctx.restore();
  }
  function fit(ctx, text, maxW, size, minSize, family) {
    var sz = size; ctx.font = sz + "px " + family;
    while (ctx.measureText(text).width > maxW && sz > minSize) { sz -= 2; ctx.font = sz + "px " + family; }
    if (ctx.measureText(text).width > maxW) { while (text.length > 3 && ctx.measureText(text + "…").width > maxW) text = text.slice(0, -1); text += "…"; }
    return text;
  }
  function tryCanvas(build) { // si los mosaicos del mapa no permiten exportar, se repite sin ellos
    var c = build(true);
    try { c.getContext("2d").getImageData(0, 0, 1, 1); return c; } catch (e) { return build(false); }
  }
  function fonts() { return document.fonts && document.fonts.load ? Promise.all([document.fonts.load("40px 'Bebas Neue'"), document.fonts.load("16px Barlow"), document.fonts.load("600 14px 'Barlow Condensed'")]).catch(function () {}) : Promise.resolve(); }
  function dlProfile() {
    var A = lastTrack; if (!A) return;
    fonts().then(function () {
      var k = 2, W = 1200 * k, H = 420 * k, c = document.createElement("canvas"); c.width = W; c.height = H; var x = c.getContext("2d");
      x.fillStyle = C.bg; x.fillRect(0, 0, W, H);
      x.fillStyle = C.fg; x.textBaseline = "alphabetic"; x.fillText(fit(x, (A.name || "Perfil de la ruta").toUpperCase(), W - 56 * k - 200 * k, 34 * k, 22 * k, DISP), 28 * k, 48 * k);
      x.fillStyle = C.muted; x.font = 15 * k + "px " + BODY; x.fillText(nf1.format(A.km) + " km  ·  +" + nf0.format(A.up) + " m  /  −" + nf0.format(A.down) + " m  ·  " + hm(A.calc.total) + "  ·  Esfuerzo MIDE " + A.calc.esfuerzo, 28 * k, 76 * k);
      x.fillStyle = C.gold; x.font = 30 * k + "px " + DISP; x.textAlign = "right"; x.fillText("AD ASTRA", W - 28 * k, 48 * k); x.textAlign = "left";
      profileTo(x, A, 16 * k, 96 * k, W - 32 * k, H - 112 * k, k);
      save(c, slug(A.name) + "-perfil.png");
    });
  }
  function dlMap() {
    var A = lastTrack; if (!A || !map) return;
    var rc = $("#trk-map").getBoundingClientRect(), k = 2;
    save(tryCanvas(function (tiles) { var c = document.createElement("canvas"); c.width = rc.width * k; c.height = rc.height * k; mapTo(c.getContext("2d"), 0, 0, c.width, c.height, A, tiles, k); return c; }), slug(A.name) + "-mapa.png");
  }
  function dlFicha() {
    var A = lastTrack; if (!A) return;
    fonts().then(function () {
      var k = 2, W = 1200 * k, hasMap = map && !$("#trk-map").hidden, mrc = $("#trk-map").getBoundingClientRect();
      var mapW = hasMap ? Math.min(W - 64 * k, mrc.width * 3) : 0, mapH = hasMap ? Math.round(mapW * mrc.height / mrc.width) : 0, H = (300 + 400) * k + mapH + (hasMap ? 24 * k : 0) + 70 * k;
      save(tryCanvas(function (tiles) {
        var c = document.createElement("canvas"); c.width = W; c.height = H; var x = c.getContext("2d");
        x.fillStyle = C.bg; x.fillRect(0, 0, W, H);
        var gr = x.createLinearGradient(0, 0, W, 0); gr.addColorStop(0, "#f0b445"); gr.addColorStop(1, "#d9661f"); x.fillStyle = gr; x.fillRect(0, 0, W, 8 * k);
        x.fillStyle = C.gold; x.font = "600 " + 14 * k + "px " + LAB; x.fillText("FICHA DE LA RUTA", 32 * k, 52 * k);
        x.fillStyle = C.fg; x.fillText(fit(x, (A.name || "Tu ruta").toUpperCase(), W - 64 * k - 260 * k, 52 * k, 30 * k, DISP), 32 * k, 104 * k);
        x.fillStyle = C.gold; x.font = 34 * k + "px " + DISP; x.textAlign = "right"; x.fillText("AD ASTRA", W - 32 * k, 56 * k);
        x.fillStyle = C.muted; x.font = "600 " + 12 * k + "px " + LAB; x.fillText("MONTAÑA Y AVENTURA", W - 32 * k, 76 * k); x.textAlign = "left";
        var st = [["DISTANCIA", nf1.format(A.km) + " km"], ["DESNIVEL +", A.hasEle ? nf0.format(A.up) + " m" : "—"], ["DESNIVEL −", A.hasEle ? nf0.format(A.down) + " m" : "—"], ["ALTITUD MÁX.", A.hasEle ? nf0.format(A.maxE) + " m" : "—"], ["ALTITUD MÍN.", A.hasEle ? nf0.format(A.minE) + " m" : "—"],
                  ["DURACIÓN", hm(A.calc.total)], ["ESFUERZO MIDE", A.calc.esfuerzo + " de 5"], ["PENDIENTE MÁX.", A.hasEle ? nf0.format(A.maxSlope) + " %" : "—"], ["TIPO", A.loop ? "Circular" : "Lineal"], [A.real ? "TIEMPO REAL" : "MÉTODO", A.real ? hm(A.real) : ({ mide: "MIDE", guia: "Guía", naismith: "Naismith" })[A.calc.p.method]]];
        var cw = (W - 64 * k) / 5, ch = 82 * k, y0 = 130 * k;
        st.forEach(function (s, i) {
          var cx = 32 * k + (i % 5) * cw, cy = y0 + Math.floor(i / 5) * ch;
          x.fillStyle = C.card; x.fillRect(cx, cy, cw - 6 * k, ch - 6 * k);
          x.fillStyle = C.gold; x.font = "600 " + 12 * k + "px " + LAB; x.fillText(s[0], cx + 16 * k, cy + 26 * k);
          x.fillStyle = C.fg; x.font = 32 * k + "px " + DISP; x.fillText(s[1], cx + 16 * k, cy + 62 * k);
        });
        var py = y0 + 2 * ch + 18 * k;
        profileTo(x, A, 32 * k, py, W - 64 * k, 380 * k, k);
        var my = py + 380 * k + 24 * k;
        if (hasMap) mapTo(x, (W - mapW) / 2, my, mapW, mapH, A, tiles, k);
        x.textBaseline = "alphabetic"; x.fillStyle = C.gold; x.font = "600 " + 16 * k + "px " + LAB; x.textAlign = "right"; x.fillText("GUIASADASTRA.COM", W - 32 * k, H - 30 * k);
        var uw = x.measureText("GUIASADASTRA.COM").width; x.textAlign = "left"; x.fillStyle = C.dim;
        x.fillText(fit(x, "Duración estimada. " + methodText(A.calc.p) + stopsText(A.calc.p, true) + ". Orientativo: depende del terreno, la meteo y el grupo.", W - 64 * k - uw - 30 * k, 14 * k, 10 * k, BODY), 32 * k, H - 30 * k);
        return c;
      }), slug(A.name) + "-ficha.png");
    });
  }
  $$("[data-dl]").forEach(function (b) { b.addEventListener("click", function () { $("#trk-err").textContent = ""; ({ perfil: dlProfile, mapa: dlMap, ficha: dlFicha })[b.dataset.dl](); }); });

  function loadFile(file) {
    var err = $("#trk-err"); err.textContent = "";
    if (!file) return;
    if (file.size > 25 * 1024 * 1024) { err.textContent = "El archivo es demasiado grande (máximo 25 MB)."; return; }
    var rd = new FileReader();
    rd.onload = function () {
      try { showTrack(analyse(parseTrack(String(rd.result), file.name))); $("#trk-res").scrollIntoView({ behavior: "smooth", block: "start" }); }
      catch (e) { err.textContent = e.message + " Prueba a exportarlo de nuevo en formato GPX desde Wikiloc, Strava, Garmin o tu app."; }
    };
    rd.onerror = function () { err.textContent = "No hemos podido leer el archivo."; };
    rd.readAsText(file);
  }
  var drop = $("#trk-drop"), inp = $("#trk-file");
  if (drop && inp) {
    inp.addEventListener("change", function () { loadFile(inp.files[0]); });
    ["dragenter", "dragover"].forEach(function (t) { drop.addEventListener(t, function (e) { e.preventDefault(); drop.classList.add("over"); }); });
    ["dragleave", "drop"].forEach(function (t) { drop.addEventListener(t, function (e) { e.preventDefault(); drop.classList.remove("over"); }); });
    drop.addEventListener("drop", function (e) { loadFile(e.dataTransfer.files[0]); });
    var demo = $("#trk-demo");
    if (demo) demo.addEventListener("click", function () {
      fetch(demo.dataset.src).then(function (r) { return r.text(); }).then(function (t) { showTrack(analyse(parseTrack(t, "ejemplo.gpx"))); $("#trk-res").scrollIntoView({ behavior: "smooth", block: "start" }); })
        .catch(function () { $("#trk-err").textContent = "No se pudo cargar el ejemplo."; });
    });
  }
})();
