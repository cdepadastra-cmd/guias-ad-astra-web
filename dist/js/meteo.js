/* Meteorología de montaña — Guías Ad Astra
   Lee /meteo/datos/resumen.json (índice) o /meteo/datos/<macizo>.json (ficha) generados cada 6 h
   a partir de ECMWF IFS, NOAA GFS y DWD ICON-EU (ver meteo/procesar.py). */
(function () {
  "use strict";
  var DATOS = "/meteo/datos/";
  var TZ = "Europe/Madrid";
  var MOD = { ecmwf: { n: "ECMWF", c: "#e9a53b" }, gfs: { n: "GFS", c: "#6fb3e0" }, icon: { n: "ICON", c: "#9ccf7a" } };
  var DIRS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSO", "SO", "OSO", "O", "ONO", "NO", "NNO"];
  var fDia = new Intl.DateTimeFormat("es-ES", { timeZone: TZ, weekday: "short" });
  var fFecha = new Intl.DateTimeFormat("es-ES", { timeZone: TZ, day: "numeric", month: "short" });
  var fHora = new Intl.DateTimeFormat("es-ES", { timeZone: TZ, hour: "2-digit", minute: "2-digit", hour12: false });
  var fLargo = new Intl.DateTimeFormat("es-ES", { timeZone: TZ, weekday: "long", day: "numeric", month: "long" });
  var fAct = new Intl.DateTimeFormat("es-ES", { timeZone: TZ, weekday: "long", day: "numeric", month: "long", hour: "2-digit", minute: "2-digit", hour12: false });
  var fYmd = new Intl.DateTimeFormat("en-CA", { timeZone: TZ, year: "numeric", month: "2-digit", day: "2-digit" });
  var fH = new Intl.DateTimeFormat("en-GB", { timeZone: TZ, hour: "2-digit", hour12: false });

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function n(v, s) { return v == null ? "–" : Math.round(v) + (s || ""); }
  function dec(v) { return v == null ? "–" : (Math.round(v * 10) / 10).toLocaleString("es-ES"); }
  function dir(d) { return d == null ? "" : DIRS[Math.round(d / 22.5) % 16]; }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function fechaLocal(iso) { var p = iso.split("-"); return new Date(Date.UTC(+p[0], +p[1] - 1, +p[2], 12)); }
  function diaCorto(iso, i) {
    var d = fechaLocal(iso), hoy = fYmd.format(new Date());
    if (iso === hoy) return "Hoy";
    var man = fYmd.format(new Date(Date.now() + 864e5));
    if (iso === man) return "Mañana";
    return cap(fDia.format(d).replace(".", ""));
  }
  function json(url) {
    return fetch(url + "?t=" + Math.floor(Date.now() / 6e5), { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    });
  }

  /* ---------------------------------------------------------------- iconos */
  var SOL = '<circle cx="24" cy="24" r="8" fill="#f2c14e"/><g stroke="#f2c14e" stroke-width="2.6" stroke-linecap="round"><path d="M24 6v5M24 37v5M6 24h5M37 24h5M11.3 11.3l3.5 3.5M33.2 33.2l3.5 3.5M11.3 36.7l3.5-3.5M33.2 14.8l3.5-3.5"/></g>';
  var LUNA = '<path d="M30 9a14 14 0 1 0 9 22A12 12 0 0 1 30 9z" fill="#e8dcc0"/>';
  var NUBE = function (x, y, s, c) { return '<path transform="translate(' + x + ' ' + y + ') scale(' + s + ')" d="M12 30h22a8 8 0 0 0 0-16 11 11 0 0 0-21-2A8 8 0 0 0 12 30z" fill="' + c + '"/>'; };
  var GOTAS = '<g stroke="#6fb3e0" stroke-width="2.6" stroke-linecap="round"><path d="M17 36l-2 6M25 36l-2 6M33 36l-2 6"/></g>';
  var GOTA = '<g stroke="#6fb3e0" stroke-width="2.6" stroke-linecap="round"><path d="M21 37l-2 5M30 37l-2 5"/></g>';
  var COPOS = '<g fill="#fff"><circle cx="17" cy="39" r="2.3"/><circle cx="25" cy="42" r="2.3"/><circle cx="33" cy="39" r="2.3"/></g>';
  var COPO = '<g fill="#fff"><circle cx="20" cy="40" r="2.3"/><circle cx="30" cy="40" r="2.3"/></g>';
  var RAYO = '<path d="M26 31l-6 9h5l-3 7 9-11h-5l3-5z" fill="#f2c14e"/>';
  function icono(k, noche) {
    var a = noche ? '<g transform="translate(-4 -4) scale(.75)">' + LUNA + "</g>" : '<g transform="translate(-4 -4) scale(.8)">' + SOL + "</g>";
    var g = { sol: noche ? '<g transform="translate(4 4) scale(.85)">' + LUNA + "</g>" : SOL,
      "poco-nuboso": a + NUBE(6, 8, 0.85, "#d9d2c8"),
      nuboso: NUBE(-4, 2, 0.8, "#a59b91") + NUBE(4, 8, 0.9, "#d9d2c8"),
      cubierto: NUBE(-4, 0, 0.85, "#8d847b") + NUBE(4, 6, 0.95, "#b8afa5"),
      chubascos: a + NUBE(6, 4, 0.85, "#c8c0b6") + GOTA,
      lluvia: NUBE(2, 0, 0.95, "#9d958c") + GOTAS,
      "nieve-debil": a + NUBE(6, 4, 0.85, "#c8c0b6") + COPO,
      nieve: NUBE(2, 0, 0.95, "#b8b0a6") + COPOS,
      tormenta: NUBE(2, -2, 0.95, "#857d75") + RAYO };
    var t = { sol: noche ? "Despejado" : "Soleado", "poco-nuboso": "Poco nuboso", nuboso: "Nuboso", cubierto: "Cubierto", chubascos: "Chubascos", lluvia: "Lluvia", "nieve-debil": "Nieve débil", nieve: "Nieve", tormenta: "Tormenta" };
    return '<svg class="mt-ico" viewBox="0 0 48 48" role="img" aria-label="' + (t[k] || k) + '"><title>' + (t[k] || k) + "</title>" + (g[k] || g.nuboso) + "</svg>";
  }
  function iconoTramo(c, i) {
    var pr = c.pr[i], tc = c.tc[i], cp = c.cp[i], cc = c.cc[i];
    if (cp != null && cp >= 500 && pr != null && pr >= 0.3) return "tormenta";
    var nieve = tc != null && tc <= 0.5;
    if (pr != null && pr >= 1) return nieve ? "nieve" : "lluvia";
    if (pr != null && pr >= 0.2) return nieve ? "nieve-debil" : "chubascos";
    if (cc == null || cc < 25) return "sol";
    return cc < 60 ? "poco-nuboso" : cc < 85 ? "nuboso" : "cubierto";
  }
  function flecha(d) {
    if (d == null) return "";
    return '<svg class="mt-dir" viewBox="0 0 20 20" aria-hidden="true"><path transform="rotate(' + Math.round(d + 180) + ' 10 10)" d="M10 2l5 13-5-3-5 3z" fill="currentColor"/></svg>';
  }
  function avisos(d) {
    return (d.avisos || []).map(function (a) { return '<span class="mt-aviso">' + esc(a) + "</span>"; }).join("");
  }
  function actualizado(doc) {
    var g = new Date(doc.generado.replace("Z", ":00Z").replace(/:(\d\d):00Z$/, ":$1:00Z"));
    var mods = Object.keys(doc.modelos).map(function (k) {
      var m = doc.modelos[k], r = new Date(m.pasada.replace("Z", ":00Z"));
      return esc(m.nombre) + " (" + String(r.getUTCHours()).padStart(2, "0") + " UTC del " + r.getUTCDate() + ")";
    });
    return "Actualizado el " + fAct.format(g) + " · Modelos: " + mods.join(", ");
  }

  /* ---------------------------------------------------------------- índice */
  function indice(el) {
    json(DATOS + "resumen.json").then(function (doc) {
      var porReg = {};
      doc.macizos.forEach(function (m) { (porReg[m.region] = porReg[m.region] || []).push(m); });
      var h = '<p class="mt-act">' + actualizado(doc) + "</p>";
      doc.regiones.forEach(function (reg) {
        if (!porReg[reg]) return;
        h += '<h2 class="mt-reg">' + esc(reg) + '</h2><div class="mt-grid">';
        porReg[reg].forEach(function (m) {
          var dias = (m.dias || []).slice(0, 4), av = [];
          (m.dias || []).slice(0, 3).forEach(function (d) { (d.avisos || []).forEach(function (a) { if (av.indexOf(a) < 0) av.push(a); }); });
          h += '<a class="mt-card" href="/meteo/' + m.id + '/"><div class="mt-card-h"><h3>' + esc(m.nombre) + '</h3><p class="muted small">' + esc(m.cumbre.nombre) + " " + m.cumbre.alt.toLocaleString("es-ES") + " m · " + esc(m.base.nombre) + " " + m.base.alt.toLocaleString("es-ES") + ' m</p></div><div class="mt-mini">';
          dias.forEach(function (d) {
            h += '<div><b>' + diaCorto(d.fecha) + "</b>" + icono(d.icono) + '<span class="mt-t"><i>' + n(d.tc_max, "°") + "</i> " + n(d.tc_min, "°") + '</span><span class="mt-s">' + (d.pr ? dec(d.pr) + " mm" : "&nbsp;") + '</span><span class="mt-s">' + n(d.wc_max) + " km/h</span></div>";
          });
          h += "</div>" + (av.length ? '<div class="mt-avisos">' + av.map(function (a) { return '<span class="mt-aviso">' + esc(a) + "</span>"; }).join("") + "</div>" : "") + "</a>";
        });
        h += "</div>";
      });
      h += '<p class="mt-nota muted small">Temperaturas y viento en la cumbre de referencia de cada macizo. Mediana de los modelos ECMWF, GFS e ICON-EU.</p>';
      el.innerHTML = h;
    }).catch(function () { el.innerHTML = '<p class="mt-err">La previsión se está generando. Vuelve a intentarlo en unos minutos.</p>'; });
  }

  /* ---------------------------------------------------------------- gráficas */
  function grafica(o) {
    // o: {t:[Date], series:[{v:[], c, w, dash, label}], barras:{v:[], c}, min, max, unidad, sel:[i0,i1], dias:[idx], alto}
    var W = 1000, Hh = o.alto || 190, L = 44, R = 12, T = 12, B = 26, N = o.t.length;
    var x = function (i) { return L + (W - L - R) * (i / (N - 1)); };
    var vals = [];
    o.series.forEach(function (s) { s.v.forEach(function (v) { if (v != null) vals.push(v); }); });
    if (o.barras) o.barras.v.forEach(function (v) { if (v != null) vals.push(v); });
    var mn = o.min != null ? Math.min(o.min, Math.min.apply(null, vals.concat([o.min]))) : Math.min.apply(null, vals);
    var mx = o.max != null ? Math.max(o.max, Math.max.apply(null, vals.concat([o.max]))) : Math.max.apply(null, vals);
    if (!isFinite(mn) || !isFinite(mx)) { mn = 0; mx = 1; }
    var dmin = Math.min.apply(null, vals.length ? vals : [0]);
    if (mx - mn < 4) { mx += 2; mn -= 2; }
    if (o.min != null && dmin >= o.min) mn = Math.max(mn, o.min);
    var paso = Math.pow(10, Math.floor(Math.log10((mx - mn) / 4)));
    [1, 2, 2.5, 5, 10].some(function (k) { if ((mx - mn) / (paso * k) <= 5) { paso *= k; return true; } });
    mn = Math.floor(mn / paso) * paso; mx = Math.ceil(mx / paso) * paso;
    var y = function (v) { return T + (Hh - T - B) * (1 - (v - mn) / (mx - mn)); };
    var s = '<svg viewBox="0 0 ' + W + " " + Hh + '" class="mt-chart" role="img" aria-label="' + esc(o.titulo) + '">';
    if (o.sel) s += '<rect x="' + x(o.sel[0]) + '" y="' + T + '" width="' + Math.max(2, x(o.sel[1]) - x(o.sel[0])) + '" height="' + (Hh - T - B) + '" fill="rgba(233,165,59,.08)"/>';
    for (var g = mn; g <= mx + 1e-9; g += paso) {
      s += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + y(g) + '" y2="' + y(g) + '" stroke="' + (Math.abs(g) < 1e-9 && o.cero ? "#6fb3e0" : "#3a271b") + '" stroke-width="1"' + (Math.abs(g) < 1e-9 && o.cero ? ' stroke-dasharray="4 4"' : "") + "/>";
      s += '<text x="' + (L - 6) + '" y="' + (y(g) + 4) + '" text-anchor="end" class="mt-ax">' + (Math.round(g * 10) / 10).toLocaleString("es-ES") + "</text>";
    }
    (o.dias || []).forEach(function (d) {
      s += '<line x1="' + x(d.i) + '" x2="' + x(d.i) + '" y1="' + T + '" y2="' + (Hh - B) + '" stroke="#4d3424"/>';
      s += '<text x="' + (x(d.i) + 4) + '" y="' + (Hh - 8) + '" class="mt-ax">' + esc(d.l) + "</text>";
    });
    if (o.barras) {
      var bw = (W - L - R) / (N - 1) * 0.7;
      o.barras.v.forEach(function (v, i) {
        if (!v) return;
        s += '<rect x="' + (x(i) - bw) + '" y="' + y(v) + '" width="' + bw + '" height="' + Math.max(0, y(mn) - y(v)) + '" fill="' + o.barras.c + '" rx="1"/>';
      });
    }
    o.series.forEach(function (se) {
      var d = "", pen = false;
      se.v.forEach(function (v, i) {
        if (v == null) { pen = false; return; }
        d += (pen ? "L" : "M") + x(i).toFixed(1) + " " + y(v).toFixed(1);
        pen = true;
      });
      if (d) s += '<path d="' + d + '" fill="none" stroke="' + se.c + '" stroke-width="' + (se.w || 2) + '"' + (se.dash ? ' stroke-dasharray="' + se.dash + '"' : "") + ' stroke-linejoin="round" stroke-linecap="round"' + (se.op ? ' opacity="' + se.op + '"' : "") + "/>";
    });
    s += '<text x="' + (L - 6) + '" y="' + (T - 2) + '" text-anchor="end" class="mt-ax">' + esc(o.unidad || "") + "</text>";
    return s + "</svg>";
  }
  function leyenda(items) {
    return '<div class="mt-ley">' + items.map(function (it) { return '<span><i style="background:' + it.c + (it.dash ? ";height:2px;border-top:2px dashed " + it.c + ";background:none" : "") + '"></i>' + esc(it.l) + "</span>"; }).join("") + "</div>";
  }

  /* ---------------------------------------------------------------- ficha de macizo */
  function ficha(el) {
    var id = el.getAttribute("data-id");
    json(DATOS + id + ".json").then(function (doc) {
      var t0 = new Date(doc.t0.replace("Z", ":00Z")), N = doc.consenso.tc.length, P = doc.paso;
      var T = []; for (var i = 0; i < N; i++) T.push(new Date(t0.getTime() + i * P * 36e5));
      var C = doc.consenso, mods = Object.keys(doc.series);
      // índices de cada día local
      var dias = doc.dias, idxDia = {};
      T.forEach(function (t, i) { var k = fYmd.format(new Date(t.getTime() - 90 * 6e4)); (idxDia[k] = idxDia[k] || []).push(i); });
      var marcas = [];
      dias.forEach(function (d) { var ix = idxDia[d.fecha]; if (ix) marcas.push({ i: ix[0], l: diaCorto(d.fecha) + " " + fechaLocal(d.fecha).getUTCDate() }); });
      var sel = 0;

      function tira() {
        return '<div class="mt-dias" role="tablist">' + dias.map(function (d, k) {
          return '<button type="button" role="tab" class="mt-dia' + (k === sel ? " on" : "") + '" data-k="' + k + '" aria-selected="' + (k === sel) + '"><b>' + diaCorto(d.fecha) + "</b><small>" + fFecha.format(fechaLocal(d.fecha)) + "</small>" + icono(d.icono) +
            '<span class="mt-t" title="Cumbre: máxima / mínima"><i>' + n(d.tc_max, "°") + "</i> " + n(d.tc_min, "°") + '</span><span class="mt-s">' + (d.pr ? dec(d.pr) + " mm" : "Sin precip.") + '</span><span class="mt-s">' + flecha(d.wc_dir) + n(d.wc_max) + " km/h</span>" + (d.avisos && d.avisos.length ? '<span class="mt-pt" title="' + esc(d.avisos.join(" · ")) + '">!</span>' : "") + "</button>";
        }).join("") + "</div>";
      }

      function detalleDia() {
        var d = dias[sel], ix = idxDia[d.fecha] || [];
        var h = '<div class="mt-res"><div><h3>' + cap(fLargo.format(fechaLocal(d.fecha))) + "</h3>" + (d.horas < 24 ? '<p class="muted small">Desde ahora hasta medianoche.</p>' : "") + avisos(d) + "</div>";
        h += '<dl class="mt-kv">' +
          "<div><dt>Cumbre (" + esc(doc.cumbre.nombre) + ")</dt><dd>" + n(d.tc_min, "°") + " / " + n(d.tc_max, "°C") + "</dd></div>" +
          "<div><dt>Base (" + esc(doc.base.nombre) + ")</dt><dd>" + n(d.tv_min, "°") + " / " + n(d.tv_max, "°C") + "</dd></div>" +
          "<div><dt>Viento en cumbre</dt><dd>" + flecha(d.wc_dir) + n(d.wc_max) + " km/h " + dir(d.wc_dir) + "</dd></div>" +
          "<div><dt>Rachas en la base</dt><dd>" + n(d.gv_max) + " km/h</dd></div>" +
          "<div><dt>Precipitación</dt><dd>" + (d.pr ? dec(d.pr) + " mm" : "No") + (d.nieve_c ? " · " + d.nieve_c + " cm de nieve en cumbre" : "") + "</dd></div>" +
          "<div><dt>Isocero</dt><dd>" + (d.i0_min == null ? "–" : (d.i0_min === d.i0_max ? d.i0_min.toLocaleString("es-ES") : d.i0_min.toLocaleString("es-ES") + "–" + d.i0_max.toLocaleString("es-ES")) + " m") + "</dd></div>" +
          "<div><dt>Tormentas</dt><dd>" + (d.tormenta >= 2 ? "Probables" : d.tormenta === 1 ? "Posibles" : "No") + "</dd></div>" +
          "<div><dt>Acuerdo entre modelos</dt><dd>" + (d.acuerdo ? cap(d.acuerdo) : "–") + "</dd></div></dl></div>";
        h += '<div class="mt-scroll"><table class="mt-tab"><thead><tr><th>Hora</th><th>Cielo</th><th>Cumbre</th><th>Base</th><th>Viento cumbre</th><th>Racha base</th><th>Precip.</th><th>Nubes</th><th>Isocero</th><th>Cota nieve</th></tr></thead><tbody>';
        ix.forEach(function (i) {
          var noche = +fH.format(T[i]) < 8 || +fH.format(T[i]) >= 20;
          h += "<tr><td>" + fHora.format(T[i]) + "</td><td>" + icono(iconoTramo(C, i), noche) + "</td><td><b>" + n(C.tc[i], "°") + "</b></td><td>" + n(C.tv[i], "°") + "</td><td>" + flecha(C.dc[i]) + n(C.wc[i]) + " km/h " + dir(C.dc[i]) + "</td><td>" + n(C.gv[i]) + " km/h</td><td>" + (C.pr[i] ? dec(C.pr[i]) + " mm" : "–") + "</td><td>" + n(C.cc[i], "%") + "</td><td>" + (C.i0[i] == null ? "–" : C.i0[i].toLocaleString("es-ES") + " m") + "</td><td>" + (C.sl[i] == null || !C.pr[i] ? "–" : C.sl[i].toLocaleString("es-ES") + " m") + "</td></tr>";
        });
        h += "</tbody></table></div><p class=\"muted small\">Cada fila resume las 3 horas anteriores en la precipitación y es el valor a esa hora en el resto. Mediana de los modelos.</p>";
        return h;
      }

      function graficas() {
        var d = dias[sel], ix = idxDia[d.fecha] || [0], rg = [ix[0], ix[ix.length - 1]];
        var fino = function (k, v) { return { v: v, c: MOD[k].c, w: 1.2, op: 0.55, dash: "3 3" }; };
        var gT = grafica({ titulo: "Temperatura", t: T, unidad: "°C", cero: true, sel: rg, dias: marcas,
          series: mods.map(function (k) { return fino(k, doc.series[k].tc); }).concat([{ v: C.tv, c: "#b9a593", w: 2 }, { v: C.tc, c: "#f3e9df", w: 2.6 }]) });
        var gP = grafica({ titulo: "Precipitación", t: T, unidad: "mm/3h", min: 0, max: 2, sel: rg, dias: marcas, barras: { v: C.pr, c: "#3f84b8" },
          series: mods.map(function (k) { return { v: doc.series[k].pr, c: MOD[k].c, w: 1.3, op: 0.7 }; }), alto: 150 });
        var gW = grafica({ titulo: "Viento en cumbre", t: T, unidad: "km/h", min: 0, sel: rg, dias: marcas,
          series: mods.map(function (k) { return fino(k, doc.series[k].wc); }).concat([{ v: C.wc, c: "#f3e9df", w: 2.6 }]), alto: 160 });
        var gI = grafica({ titulo: "Isocero", t: T, unidad: "m", min: 0, sel: rg, dias: marcas,
          series: mods.map(function (k) { return fino(k, doc.series[k].i0); }).concat([{ v: C.i0, c: "#6fb3e0", w: 2.4 }]), alto: 150 });
        var ley = leyenda(mods.map(function (k) { return { c: MOD[k].c, l: MOD[k].n }; }));
        return '<div class="mt-g"><h3>Temperatura</h3>' + leyenda([{ c: "#f3e9df", l: "Cumbre " + doc.cumbre.alt.toLocaleString("es-ES") + " m" }, { c: "#b9a593", l: "Base " + doc.base.alt.toLocaleString("es-ES") + " m" }]) + '<div class="mt-scroll">' + gT + "</div></div>" +
          '<div class="mt-g"><h3>Precipitación</h3><div class="mt-scroll">' + gP + "</div></div>" +
          '<div class="mt-g"><h3>Viento en cumbre</h3><div class="mt-scroll">' + gW + "</div></div>" +
          '<div class="mt-g"><h3>Isocero</h3><div class="mt-scroll">' + gI + "</div></div>" + '<p class="muted small">Líneas de colores: cada modelo por separado. ' + ley + "</p>";
      }

      function comparativa() {
        var h = '<div class="mt-scroll"><table class="mt-tab mt-cmp"><thead><tr><th rowspan="2">Día</th>' + mods.map(function (k) { return '<th colspan="3" style="color:' + MOD[k].c + '">' + MOD[k].n + "</th>"; }).join("") + "</tr><tr>" +
          mods.map(function () { return "<th>Precip.</th><th>Máx. cumbre</th><th>Viento</th>"; }).join("") + "</tr></thead><tbody>";
        dias.forEach(function (d) {
          var ix = idxDia[d.fecha] || [];
          h += "<tr><td>" + diaCorto(d.fecha) + " " + fechaLocal(d.fecha).getUTCDate() + "</td>";
          mods.forEach(function (k) {
            var s = doc.series[k], p = 0, cnt = 0, tm = null, wm = null;
            ix.forEach(function (i) { if (s.pr[i] != null) { p += s.pr[i]; cnt++; } if (s.tc[i] != null) tm = tm == null ? s.tc[i] : Math.max(tm, s.tc[i]); if (s.wc[i] != null) wm = wm == null ? s.wc[i] : Math.max(wm, s.wc[i]); });
            h += "<td>" + (cnt ? dec(p) + " mm" : "–") + "</td><td>" + n(tm, "°") + "</td><td>" + n(wm) + "</td>";
          });
          h += "</tr>";
        });
        return h + '</tbody></table></div><p class="muted small">ICON-EU llega a 5 días; ECMWF y GFS, a 7. Si los modelos no coinciden, la previsión es menos fiable.</p>';
      }

      function pintar() {
        el.innerHTML = '<p class="mt-act">' + actualizado(doc) + "</p>" + tira() +
          '<div class="mt-sec">' + detalleDia() + "</div>" +
          '<div class="mt-sec"><h2>Evolución a 7 días</h2>' + graficas() + "</div>" +
          '<div class="mt-sec"><h2>Comparación de modelos</h2>' + comparativa() + "</div>";
        el.querySelectorAll(".mt-dia").forEach(function (b) {
          b.addEventListener("click", function () { sel = +b.getAttribute("data-k"); var y = window.scrollY; pintar(); window.scrollTo(0, y); });
        });
      }
      pintar();
    }).catch(function () { el.innerHTML = '<p class="mt-err">La previsión se está generando. Vuelve a intentarlo en unos minutos.</p>'; });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var a = document.getElementById("mt-index"); if (a) indice(a);
    var b = document.getElementById("mt-mac"); if (b) ficha(b);
  });
})();
