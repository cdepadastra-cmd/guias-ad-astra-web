/* Guías Ad Astra · Calculadora de rutas (tiempo estimado y análisis de tracks GPX/KML/TCX) */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var nf1 = new Intl.NumberFormat("es-ES", { maximumFractionDigits: 1, minimumFractionDigits: 1 });
  var nf0 = new Intl.NumberFormat("es-ES", { maximumFractionDigits: 0 });

  /* ---------- método de cálculo ----------
     Horizontal: distancia / velocidad en llano (4–5 km/h).
     Vertical:   desnivel positivo / 300 m/h + desnivel negativo / bajada (m/h).
     Total (criterio MIDE): el mayor de los dos + la mitad del menor. */
  function estimate(km, up, down, kmh, upRate, downRate) {
    var h = km / kmh;
    var v = up / upRate + (downRate > 0 ? down / downRate : 0);
    var total = Math.max(h, v) + Math.min(h, v) / 2;
    return { h: h, v: v, total: total };
  }
  function hm(hours) {
    if (!isFinite(hours) || hours <= 0) return "0 min";
    var m = Math.round(hours * 60 / 5) * 5; // redondeo a 5 minutos
    var hh = Math.floor(m / 60), mm = m % 60;
    return (hh ? hh + " h" : "") + (hh && mm ? " " : "") + (mm || !hh ? mm + " min" : "");
  }
  function difficulty(km, up, total) {
    var score = total + up / 600;
    if (score < 3) return ["Fácil", "Ruta corta y asequible para casi todo el mundo."];
    if (score < 5.5) return ["Moderada", "Media jornada. Hace falta algo de costumbre de caminar."];
    if (score < 8.5) return ["Exigente", "Jornada completa. Buena forma física y salir temprano."];
    return ["Muy exigente", "Ruta larga y dura. Solo con experiencia y buena planificación."];
  }
  function params(scope) {
    return {
      kmh: parseFloat($("[name=ritmo]:checked", scope).value),
      up: parseFloat($("#c-subida").value) || 300,
      down: parseFloat($("#c-bajada").value) || 0,
      stops: $("#c-paradas").checked
    };
  }

  /* ---------- calculadora manual ---------- */
  var form = $("#calc");
  function renderResult(box, km, up, down, p) {
    var r = estimate(km, up, down, p.kmh, p.up, p.down);
    var total = p.stops ? r.total * 1.15 : r.total;
    var d = difficulty(km, up, r.total);
    var start = new Date(); start.setHours(9, 0, 0, 0);
    var end = new Date(start.getTime() + total * 3600e3);
    box.innerHTML =
      '<div class="calc-big"><span class="label">Duración aproximada</span><strong>' + hm(total) + "</strong>" +
      '<span class="muted">' + (p.stops ? "Incluye un 15 % para paradas, fotos y comer." : "Tiempo en movimiento, sin paradas.") + "</span></div>" +
      '<dl class="calc-parts">' +
      "<div><dt>Por distancia</dt><dd>" + hm(r.h) + "<small>" + nf1.format(km) + " km a " + nf1.format(p.kmh) + " km/h</small></dd></div>" +
      "<div><dt>Por desnivel</dt><dd>" + hm(r.v) + "<small>+" + nf0.format(up) + " m a " + nf0.format(p.up) + " m/h" + (p.down && down ? " · −" + nf0.format(down) + " m a " + nf0.format(p.down) + " m/h" : "") + "</small></dd></div>" +
      "<div><dt>Dificultad física</dt><dd>" + d[0] + "<small>" + d[1] + "</small></dd></div>" +
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
      renderResult(out, km, up, down, params(document));
      if (lastTrack) showTrack(lastTrack);
    };
    $$("input", form).forEach(function (i) { i.addEventListener("input", run); i.addEventListener("change", run); });
    $$("#ajustes input").forEach(function (i) { i.addEventListener("input", run); i.addEventListener("change", run); });
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
    if (!window.L) { el.hidden = true; return; }
    el.hidden = false;
    if (!map) {
      map = L.map(el, { scrollWheelZoom: false });
      L.tileLayer("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", { maxZoom: 17, attribution: "© OpenStreetMap · © OpenTopoMap" }).addTo(map);
    }
    if (layer) layer.remove(); if (marker) marker.remove();
    var ll = A.pts.map(function (p) { return [p.lat, p.lon]; });
    layer = L.layerGroup([
      L.polyline(ll, { color: "#160d09", weight: 7, opacity: .6 }),
      L.polyline(ll, { color: "#f0b445", weight: 4 }),
      L.circleMarker(ll[0], { radius: 7, color: "#160d09", weight: 2, fillColor: "#5cb87a", fillOpacity: 1 }).bindTooltip("Salida"),
      L.circleMarker(ll[ll.length - 1], { radius: 7, color: "#160d09", weight: 2, fillColor: "#c9533b", fillOpacity: 1 }).bindTooltip("Llegada")
    ]).addTo(map);
    marker = L.circleMarker(ll[0], { radius: 6, color: "#fff", weight: 2, fillColor: "#e9a53b", opacity: 0, fillOpacity: 0 }).addTo(map);
    map.fitBounds(L.latLngBounds(ll), { padding: [24, 24] });
    setTimeout(function () { map.invalidateSize(); }, 50);
  }

  /* ---------- mostrar análisis ---------- */
  var lastTrack = null;
  function showTrack(A) {
    lastTrack = A;
    var p = params(document);
    var r = estimate(A.km, A.up, A.down, p.kmh, p.up, p.down), total = p.stops ? r.total * 1.15 : r.total;
    var d = difficulty(A.km, A.up, r.total);
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
      ["Dificultad física", d[0]],
      ["Tipo", A.loop ? "Circular" : "Lineal (ida)"]
    ];
    if (A.real) stats.push(["Tiempo real del track", hm(A.real)]);
    var n = stats.length; $("#trk-stats").style.setProperty("--cols", n % 5 === 0 ? 5 : n % 4 === 0 ? 4 : 3);
    $("#trk-stats").innerHTML = stats.map(function (s) { return "<div><dt>" + s[0] + "</dt><dd>" + s[1] + "</dd></div>"; }).join("");
    $("#trk-note").textContent = "Duración calculada con " + nf1.format(p.kmh) + " km/h en llano y " + nf0.format(p.up) + " m/h de subida" + (p.down ? " y " + nf0.format(p.down) + " m/h de bajada" : "") + (p.stops ? ", más un 15 % de paradas." : ", sin paradas.") + " " + d[1];
    drawProfile(A, $("#trk-prof"), function (i) {
      if (!marker) return;
      if (i < 0) { marker.setStyle({ opacity: 0, fillOpacity: 0 }); return; }
      marker.setLatLng([A.pts[i].lat, A.pts[i].lon]); marker.setStyle({ opacity: 1, fillOpacity: 1 });
    });
    drawMap(A);
  }
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
      fetch(((window.ADASTRA_CONFIG || {}).base || "") + demo.dataset.src).then(function (r) { return r.text(); }).then(function (t) { showTrack(analyse(parseTrack(t, "ejemplo.gpx"))); $("#trk-res").scrollIntoView({ behavior: "smooth", block: "start" }); })
        .catch(function () { $("#trk-err").textContent = "No se pudo cargar el ejemplo."; });
    });
  }
})();
