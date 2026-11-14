/* Caudal de barrancos: lee /meteo/rios/rios.json (aforos SAIH Tajo y Duero) y pinta una tarjeta por barranco. */
(function () {
  "use strict";
  var TZ = "Europe/Madrid";
  var fHora = new Intl.DateTimeFormat("es-ES", { timeZone: TZ, weekday: "short", day: "numeric", hour: "2-digit", minute: "2-digit", hour12: false });
  var fDia = new Intl.DateTimeFormat("es-ES", { timeZone: TZ, weekday: "short", day: "numeric" });
  var COL = { poco: "#e9c46a", bueno: "#7cc47f", alto: "#f08a3e", no: "#e8574a" };
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function dec(v, n) { return v == null ? "–" : v.toLocaleString("es-ES", { maximumFractionDigits: n == null ? 1 : n, minimumFractionDigits: n == null ? 1 : n }); }
  function fecha(s) { return new Date(s.replace("Z", ":00Z")); }

  function grafica(b) {
    var S = (b.serie || []).map(function (x) { return [fecha(x[0]).getTime(), x[1]]; });
    if (S.length < 2) return '<p class="muted small">La gráfica aparecerá cuando haya varias horas de datos.</p>';
    var W = 640, Hh = 220, L = 44, R = 12, T = 12, B = 26;
    var t0 = S[0][0], t1 = S[S.length - 1][0];
    var qs = S.map(function (x) { return x[1]; }), mx = Math.max.apply(null, qs), mn = 0;
    (b.umbrales || []).forEach(function (u) { if (u.hasta && u.hasta < mx * 1.6) mx = Math.max(mx, u.hasta * 1.1); });
    mx = mx <= 0 ? 1 : mx * 1.1;
    var X = function (t) { return L + (W - L - R) * (t - t0) / Math.max(1, t1 - t0); };
    var Y = function (q) { return T + (Hh - T - B) * (1 - (q - mn) / (mx - mn)); };
    var g = '<svg class="rio-g" viewBox="0 0 ' + W + " " + Hh + '" role="img" aria-label="Caudal de las últimas horas">';
    // bandas de los umbrales
    var desde = 0;
    (b.umbrales || []).forEach(function (u) {
      var hasta = u.hasta == null ? mx : Math.min(u.hasta, mx);
      if (hasta > desde) g += '<rect x="' + L + '" y="' + Y(hasta).toFixed(1) + '" width="' + (W - L - R) + '" height="' + (Y(desde) - Y(hasta)).toFixed(1) + '" fill="' + COL[u.estado] + '" opacity=".13"/>';
      desde = hasta;
    });
    var paso = [0.5, 1, 2, 5, 10, 20, 50, 100].filter(function (p) { return mx / p <= 6; })[0] || 200;
    for (var v = 0; v <= mx; v += paso) g += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + Y(v).toFixed(1) + '" y2="' + Y(v).toFixed(1) + '" stroke="rgba(255,255,255,.08)"/><text x="' + (L - 6) + '" y="' + (Y(v) + 4).toFixed(1) + '" class="rio-y">' + v + "</text>";
    for (var t = Math.ceil(t0 / 36e5) * 36e5; t <= t1; t += 36e5) {
      var h = +new Intl.DateTimeFormat("en-GB", { timeZone: TZ, hour: "2-digit", hour12: false }).format(new Date(t)) % 24;
      if (h % 6) continue;
      g += '<text x="' + X(t).toFixed(1) + '" y="' + (Hh - 7) + '" class="rio-x">' + (h === 0 ? fDia.format(new Date(t)) : String(h).padStart(2, "0") + "h") + "</text>";
    }
    var d = S.map(function (x, i) { return (i ? "L" : "M") + X(x[0]).toFixed(1) + " " + Y(x[1]).toFixed(1); }).join("");
    g += '<path d="' + d + "L" + X(t1).toFixed(1) + " " + Y(0) + "L" + X(t0).toFixed(1) + " " + Y(0) + 'Z" fill="rgba(111,179,224,.15)"/>';
    g += '<path d="' + d + '" fill="none" stroke="#6fb3e0" stroke-width="2.6" stroke-linejoin="round"/>';
    g += '<circle cx="' + X(t1).toFixed(1) + '" cy="' + Y(S[S.length - 1][1]).toFixed(1) + '" r="4.5" fill="#6fb3e0"/>';
    return g + "</svg>";
  }

  function tarjeta(b) {
    var col = b.estado ? COL[b.estado] : "#8d847b";
    var flecha = { sube: "↗ Subiendo", baja: "↘ Bajando", estable: "→ Estable" }[b.tendencia] || "";
    var h = '<article class="rio-card" style="--rio:' + col + '"><header><div><h2>' + esc(b.nombre) + '</h2><p class="muted">' + esc(b.lugar) + "</p></div>" +
      '<div class="rio-estado">' + (b.estado ? esc(b.estado_txt) : "Sin umbral todavía") + "</div></header>";
    h += '<div class="rio-dato"><span class="rio-q">' + dec(b.q, b.q != null && b.q < 10 ? 2 : 1) + ' <small>m³/s</small></span><span class="rio-t">' + flecha + "</span></div>";
    h += '<p class="muted small">Aforo ' + esc(b.aforo.nombre) + " (" + esc(b.aforo.fuente) + ", " + esc(b.aforo.codigo) + ")" + (b.hora ? " · dato de " + fHora.format(fecha(b.hora)) : "") +
      (b.dato_antiguo ? ' · <b style="color:#f08a3e">dato con más de 6 horas: el aforo puede estar sin conexión</b>' : "") + (b.max24 != null ? " · máximo 24 h: " + dec(b.max24) + " m³/s" : "") + "</p>";
    if (b.umbrales) h += '<p class="rio-umb">' + b.umbrales.map(function (u, i) {
      var de = i ? b.umbrales[i - 1].hasta : 0;
      var f = function (x) { return x < 10 && x % 1 ? dec(x, 1) : dec(x, 0); };
      return '<span><i style="background:' + COL[u.estado] + '"></i>' + (u.hasta == null ? "más de " + f(de) : f(de) + "–" + f(u.hasta)) + " m³/s: " + esc(u.txt) + "</span>";
    }).join("") + "</p>";
    if (b.provisional) h += '<p class="muted small">Umbrales provisionales, estimados con el caudal del aforo en las épocas en que hacemos el barranco. Se irán ajustando con cada salida.</p>';
    h += grafica(b);
    var ll = b.lluvia_ahora, pv = b.prevision;
    h += '<div class="rio-ll">';
    if (ll && ll.p1h != null) h += "<div><b>Lluvia ahora</b><span>" + dec(ll.p1h) + " l/m² en la última hora en " + esc(ll.nombre) + (ll.t ? " · " + esc(ll.t) : "") + "</span></div>";
    if (pv) {
      h += "<div><b>Lluvia prevista</b><span>Próximas 24 h: " + dec(pv.p24) + " mm · de 24 a 48 h: " + dec(pv.p48) + " mm</span></div>";
      if (pv.p24 >= 10 || pv.p48 >= 15) h += '<div class="rio-av">Lluvia importante prevista: el caudal puede subir con rapidez.</div>';
    }
    h += "</div>";
    h += '<p class="rio-links"><a href="' + esc(b.actividad) + '">Ver la actividad</a></p></article>';
    return h;
  }

  var el = document.getElementById("rio-lista");
  if (!el) return;
  fetch("/meteo/rios/rios.json?t=" + Math.floor(Date.now() / 6e5), { cache: "no-cache" }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (d) {
    el.innerHTML = '<p class="mt-act">Actualizado: ' + fHora.format(fecha(d.generado)) + " · los aforos se leen cada hora</p>" +
      '<div class="rio-cards">' + d.barrancos.map(tarjeta).join("") + "</div>" +
      (d.errores && d.errores.length ? '<p class="muted small">Sin respuesta ahora mismo: ' + esc(d.errores.join(" · ")) + "</p>" : "");
  }).catch(function () { el.innerHTML = '<p class="mt-err">Los caudales se están cargando. Vuelve a intentarlo en unos minutos.</p>'; });
})();
