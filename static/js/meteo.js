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

  /* ---------------------------------------------------------------- sol (algoritmo de la NOAA, precisión ~1 min) */
  function solDia(iso, lat, lon) {
    var p = iso.split("-"), rad = Math.PI / 180;
    var jd = Date.UTC(+p[0], +p[1] - 1, +p[2], 12) / 864e5 + 2440587.5;
    var n = Math.round(jd - 2451545 + 0.0008), js = n - lon / 360;
    var M = (357.5291 + 0.98560028 * js) % 360;
    var C = 1.9148 * Math.sin(M * rad) + 0.02 * Math.sin(2 * M * rad) + 0.0003 * Math.sin(3 * M * rad);
    var lam = (M + C + 180 + 102.9372) % 360;
    var jt = 2451545 + js + 0.0053 * Math.sin(M * rad) - 0.0069 * Math.sin(2 * lam * rad);
    var dec = Math.asin(Math.sin(lam * rad) * Math.sin(23.44 * rad));
    var cw = (Math.sin(-0.833 * rad) - Math.sin(lat * rad) * Math.sin(dec)) / (Math.cos(lat * rad) * Math.cos(dec));
    if (cw < -1 || cw > 1) return null;
    var w = Math.acos(cw) / rad / 360, aJ = function (j) { return new Date((j - 2440587.5) * 864e5); };
    return { sale: aJ(jt - w), pone: aJ(jt + w) };
  }

  /* ---------------------------------------------------------------- avisos de AEMET */
  var fAviso = new Intl.DateTimeFormat("es-ES", { timeZone: TZ, weekday: "short", day: "numeric", hour: "2-digit", minute: "2-digit", hour12: false });
  function avisoEnDia(a, iso) {
    var p = iso.split("-"), d0 = Date.UTC(+p[0], +p[1] - 1, +p[2]) - 2 * 36e5, d1 = d0 + 864e5 + 2 * 36e5;
    var i = Date.parse(a.inicio), f = Date.parse(a.fin);
    return (isNaN(i) || i < d1) && (isNaN(f) || f > d0);
  }
  function fenomeno(a) { return (a.evento || a.titulo || "Aviso").replace(/^Aviso (amarillo|naranja|rojo) (de|por)\s*/i, ""); }
  function chipAemet(a, largo) {
    return '<span class="mt-aemet mt-' + a.nivel + '" title="' + esc(a.titulo || a.evento) + '">Aviso ' + a.nivel + " AEMET" + (largo ? ": " + esc(fenomeno(a)) : "") + "</span>";
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
  function iconoTramo(c, i, horas, prSum) {
    horas = horas || 3;
    var pr = prSum != null ? prSum : c.pr[i], tc = c.tc[i], cp = c.cp[i], cc = c.cc[i];
    if (pr != null) pr = pr * 3 / horas;  // umbrales pensados para 3 h
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
  var HORAS_ACT = [3, 9, 15, 21];  // ejecuciones programadas (UTC, minuto 40; tardan unos 15 min)
  function proxima(g) {  // primera ejecución programada después de la que generó estos datos
    var lim = g.getTime() + 36e5, d0 = Date.UTC(g.getUTCFullYear(), g.getUTCMonth(), g.getUTCDate());
    for (var k = 0; k < 3; k++) for (var j = 0; j < HORAS_ACT.length; j++) {
      var c = d0 + k * 864e5 + HORAS_ACT[j] * 36e5 + 55 * 6e4;
      if (c > lim) return new Date(c);
    }
    return null;
  }
  function actualizado(doc) {
    var g = new Date(doc.generado.replace("Z", ":00Z"));
    var mods = Object.keys(doc.modelos).map(function (k) {
      var m = doc.modelos[k], r = new Date(m.pasada.replace("Z", ":00Z"));
      return esc(m.nombre) + " (" + String(r.getUTCHours()).padStart(2, "0") + " UTC del " + r.getUTCDate() + ")";
    });
    var p = proxima(g), txt;
    if (!p) txt = "";
    else if (p.getTime() < Date.now()) txt = "en curso, en unos minutos";
    else txt = (fYmd.format(p) === fYmd.format(new Date()) ? "hoy" : cap(diaCorto(fYmd.format(p)).toLowerCase())) + " hacia las " + fHora.format(p);
    return '<span class="mt-upd"><b>Última actualización:</b> ' + fAct.format(g) + (txt ? ' · <b>Próxima:</b> ' + txt : "") + '</span><span class="mt-mods">Modelos: ' + mods.join(", ") + "</span>";
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
          h += '<a class="mt-card" data-mac="' + m.id + '" href="/meteo/' + m.id + '/"><div class="mt-card-h"><h3>' + esc(m.nombre) + '</h3><p class="muted small">' + esc(m.cumbre.nombre) + " " + m.cumbre.alt.toLocaleString("es-ES") + " m · " + esc(m.base.nombre) + " " + m.base.alt.toLocaleString("es-ES") + ' m</p></div><div class="mt-mini">';
          dias.forEach(function (d) {
            h += '<div><b>' + diaCorto(d.fecha) + "</b>" + icono(d.icono) + '<span class="mt-t"><i>' + n(d.tc_max, "°") + "</i> " + n(d.tc_min, "°") + '</span><span class="mt-s">' + (d.pr ? dec(d.pr) + " mm" : "&nbsp;") + '</span><span class="mt-s">' + n(d.wc_max) + " km/h</span></div>";
          });
          var ae = (m.aemet || []).filter(function (a) { return Date.parse(a.inicio) < Date.now() + 3 * 864e5; });
          h += "</div>" + (ae.length ? '<div class="mt-avisos">' + chipAemet(ae[0], true) + (ae.length > 1 ? '<span class="mt-s">+' + (ae.length - 1) + "</span>" : "") + "</div>" : "") + (av.length ? '<div class="mt-avisos">' + av.map(function (a) { return '<span class="mt-aviso">' + esc(a) + "</span>"; }).join("") + "</div>" : "") + "</a>";
        });
        h += "</div>";
      });
      h += '<p class="mt-nota muted small">Temperaturas y viento en la cumbre de referencia de cada macizo. Mediana de los modelos ECMWF, GFS e ICON-EU.</p>';
      el.innerHTML = h;
      el.querySelectorAll("[data-mac]").forEach(function (a) {
        a.addEventListener("click", function (ev) {
          if (ev.ctrlKey || ev.metaKey || ev.shiftKey || ev.button) return;
          ev.preventDefault(); elegir(a.getAttribute("data-mac"), true);
        });
      });
    }).catch(function () { el.innerHTML = '<p class="mt-err">La previsión se está generando. Vuelve a intentarlo en unos minutos.</p>'; });
  }

  /* ---------------------------------------------------------------- selector cordillera -> sierra (todo en la misma página) */
  var LISTA = [], H1 = null, TIT0 = document.title, H10 = "";
  function rellenarSierras(reg, sel) {
    var s = document.getElementById("mt-sel");
    s.innerHTML = '<option value="">Todas las sierras</option>' + LISTA.filter(function (m) { return !reg || m.region === reg; }).map(function (m) {
      return '<option value="' + m.id + '"' + (m.id === sel ? " selected" : "") + ">" + esc(m.nombre) + "</option>";
    }).join("");
  }
  function elegir(id, push) {
    var idx = document.getElementById("mt-index"), mac = document.getElementById("mt-mac");
    var m = LISTA.filter(function (x) { return x.id === id; })[0];
    if (!m) {  // todas
      if (!idx) { location.href = "/meteo/"; return; }
      mac.hidden = true; mac.removeAttribute("data-id"); idx.hidden = false;
      document.getElementById("mt-sel").value = "";
      if (H1) H1.textContent = H10;
      document.title = TIT0;
      if (push) history.pushState({ id: "" }, "", "/meteo/");
      return;
    }
    document.getElementById("mt-reg").value = m.region;
    rellenarSierras(m.region, m.id);
    if (idx) idx.hidden = true;
    mac.hidden = false;
    mac.innerHTML = '<p class="mt-cargando">Cargando previsión de ' + esc(m.nombre) + "…</p>";
    if (H1) H1.textContent = "Tiempo en " + m.nombre;
    document.title = "Tiempo en " + m.nombre + ": previsión de montaña | Ad Astra";
    if (push) history.pushState({ id: id }, "", "/meteo/" + id + "/");
    ficha(mac, id).catch(function () {});
    var bar = document.getElementById("mt-selbar");
    if (bar && bar.getBoundingClientRect().top < 0) bar.scrollIntoView({ block: "start" });
  }
  function selector() {
    var l = document.getElementById("mt-lista");
    if (!l) return;
    try { LISTA = JSON.parse(l.textContent); } catch (e) { return; }
    H1 = document.querySelector(".hero h1"); H10 = H1 ? H1.textContent : "";
    var reg = document.getElementById("mt-reg"), sel = document.getElementById("mt-sel");
    reg.addEventListener("change", function () {
      rellenarSierras(reg.value, "");
      var del = LISTA.filter(function (m) { return m.region === reg.value; });
      if (del.length === 1) elegir(del[0].id, true);  // una sola sierra: se carga directamente
      else if (!reg.value) elegir("", true);
    });
    sel.addEventListener("change", function () { elegir(sel.value, true); });
    window.addEventListener("popstate", function () {
      var mm = location.pathname.match(/^\/meteo\/([^\/]+)\/?$/);
      elegir(mm ? mm[1] : "", false);
      if (!mm) { reg.value = ""; rellenarSierras("", ""); }
    });
    var mac = document.getElementById("mt-mac");
    if (mac && mac.getAttribute("data-id")) { history.replaceState({ id: mac.getAttribute("data-id") }, ""); H10 = "Meteorología de montaña"; TIT0 = "Meteorología de montaña: previsión en cumbre a 7 días | Ad Astra"; }
  }

  /* ---------------------------------------------------------------- gráficas */
  function grafica(o) {
    // o: {t:[Date], series:[{v:[], c, w, dash, label}], barras:{v:[], c}, min, max, unidad, sel:[i0,i1], dias:[idx], alto}
    var W = 1000, Hh = o.alto || 190, L = 44, R = 12, T = 16, B = 26, N = o.t.length;
    var H = o.h || o.t.map(function (_, i) { return i; }), h0 = H[0], hN = H[N - 1];
    var x = function (i) { return L + (W - L - R) * ((H[i] - h0) / (hN - h0)); };
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
      o.barras.v.forEach(function (v, i) {
        if (!v) return;
        var bw = Math.max(1.5, (x(i) - x(i ? i - 1 : 0)) * 0.8) || 2;
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
    return s + "</svg>";
  }
  function leyenda(items) {
    return '<div class="mt-ley">' + items.map(function (it) { return '<span><i style="background:' + it.c + (it.dash ? ";height:2px;border-top:2px dashed " + it.c + ";background:none" : "") + '"></i>' + esc(it.l) + "</span>"; }).join("") + "</div>";
  }

  function duracion(a, b) { var m = Math.round((b - a) / 6e4); return Math.floor(m / 60) + " h " + String(m % 60).padStart(2, "0") + " min"; }
  function sens(t, st) { return st == null || t == null || Math.round(st) === Math.round(t) ? "" : ' <span class="mt-st" title="Sensación térmica">' + n(st, "°") + "</span>"; }
  var NUB = [500, 1000, 2000, 3000];
  function celdaNube(v) {
    if (v == null) return '<td class="mt-nb">–</td>';
    var a = Math.min(1, Math.max(0, v / 100)) * 0.75;
    return '<td class="mt-nb" style="background:rgba(200,192,182,' + a.toFixed(2) + ")" + (v >= 60 ? ";color:#1b120c" : "") + '">' + n(v, "%") + "</td>";
  }

  function C0(N, P) { var a = []; for (var i = 0; i < N; i++) a.push(i * P); return a; }

  /* ---------------------------------------------------------------- ficha de macizo */
  function ficha(el, id) {
    id = id || el.getAttribute("data-id");
    el.setAttribute("data-id", id);
    return json(DATOS + id + ".json").then(function (doc) {
      if (el.getAttribute("data-id") !== id) return;  // se eligió otro macizo mientras cargaba
      var t0 = new Date(doc.t0.replace("Z", ":00Z")), N = doc.consenso.tc.length, P = doc.paso;
      var HH = doc.h || C0(N, P);
      var T = HH.map(function (h) { return new Date(t0.getTime() + h * 36e5); });
      var DUR = HH.map(function (h, i) { return i ? h - HH[i - 1] : 1; });
      var modo = "1h";
      var C = doc.consenso, mods = Object.keys(doc.series);
      // índices de cada día local
      var dias = doc.dias, idxDia = {};
      T.forEach(function (t, i) { var k = fYmd.format(new Date(t.getTime() - DUR[i] * 18e5)); (idxDia[k] = idxDia[k] || []).push(i); });
      var marcas = [];
      dias.forEach(function (d) { var ix = idxDia[d.fecha]; if (ix) marcas.push({ i: ix[0], l: diaCorto(d.fecha) + " " + fechaLocal(d.fecha).getUTCDate() }); });
      var sel = 0;

      function tira() {
        return '<div class="mt-dias" role="tablist">' + dias.map(function (d, k) {
          return '<button type="button" role="tab" class="mt-dia' + (k === sel ? " on" : "") + '" data-k="' + k + '" aria-selected="' + (k === sel) + '"><b>' + diaCorto(d.fecha) + "</b><small>" + fFecha.format(fechaLocal(d.fecha)) + "</small>" + icono(d.icono) +
            '<span class="mt-t" title="Cumbre: máxima / mínima"><i>' + n(d.tc_max, "°") + "</i> " + n(d.tc_min, "°") + '</span><span class="mt-s">' + (d.pr ? dec(d.pr) + " mm" : "Sin precip.") + '</span><span class="mt-s">' + flecha(d.wc_dir) + n(d.wc_max) + " km/h</span>" + (d.avisos && d.avisos.length ? '<span class="mt-pt" title="' + esc(d.avisos.join(" · ")) + '">!</span>' : "") + aemetPunto(d.fecha) + "</button>";
        }).join("") + "</div>";
      }

      function aemetPunto(iso) {
        var a = (doc.aemet || []).filter(function (x) { return avisoEnDia(x, iso); });
        return a.length ? '<span class="mt-pa mt-' + a[0].nivel + '" title="Aviso ' + a[0].nivel + ' de AEMET"></span>' : "";
      }
      function detalleDia() {
        var d = dias[sel], ix = idxDia[d.fecha] || [];
        var sl = solDia(d.fecha, doc.base.lat, doc.base.lon);
        var aeDia = (doc.aemet || []).filter(function (x) { return avisoEnDia(x, d.fecha); });
        var h = '<div class="mt-res"><div><h3>' + cap(fLargo.format(fechaLocal(d.fecha))) + "</h3>" +
          (sl ? '<p class="mt-sol">Amanece ' + fHora.format(sl.sale) + " · Anochece " + fHora.format(sl.pone) + '<br>Horas de luz: ' + duracion(sl.sale, sl.pone) + "</p>" : "") +
          (d.horas < 24 ? '<p class="muted small">Desde ahora hasta medianoche.</p>' : "") +
          (aeDia.length ? '<div class="mt-avisos">' + aeDia.map(function (a) { return chipAemet(a, true); }).join("") + "</div>" : "") + avisos(d) + "</div>";
        h += '<dl class="mt-kv">' +
          "<div><dt>Cumbre (" + esc(doc.cumbre.nombre) + ")</dt><dd>" + n(d.tc_min, "°") + " / " + n(d.tc_max, "°C") + (d.st_min != null ? ' <small class="mt-st">sensación ' + n(d.st_min, "°") + "</small>" : "") + "</dd></div>" +
          "<div><dt>Base (" + esc(doc.base.nombre) + ")</dt><dd>" + n(d.tv_min, "°") + " / " + n(d.tv_max, "°C") + (d.sv_min != null ? ' <small class="mt-st">sensación ' + n(d.sv_min, "°") + (d.sv_max != null && d.tv_max != null && d.sv_max > d.tv_max ? " / " + n(d.sv_max, "°") : "") + "</small>" : "") + "</dd></div>" +
          "<div><dt>Viento en cumbre</dt><dd>" + flecha(d.wc_dir) + n(d.wc_max) + " km/h " + dir(d.wc_dir) + "</dd></div>" +
          "<div><dt>Rachas en la base</dt><dd>" + n(d.gv_max) + " km/h</dd></div>" +
          "<div><dt>Precipitación</dt><dd>" + (d.pr ? dec(d.pr) + " mm" : "No") + (d.nieve_c ? " · " + d.nieve_c + " cm de nieve en cumbre" : "") + "</dd></div>" +
          "<div><dt>Isocero</dt><dd>" + (d.i0_min == null ? "–" : (d.i0_min === d.i0_max ? d.i0_min.toLocaleString("es-ES") : d.i0_min.toLocaleString("es-ES") + "–" + d.i0_max.toLocaleString("es-ES")) + " m") + "</dd></div>" +
          "<div><dt>Tormentas</dt><dd>" + (d.tormenta >= 2 ? "Probables" : d.tormenta === 1 ? "Posibles" : "No") + "</dd></div>" +
          "<div><dt>Acuerdo entre modelos</dt><dd>" + (d.acuerdo ? cap(d.acuerdo) : "–") + "</dd></div></dl></div>";
        var hayHoras = ix.some(function (i) { return DUR[i] === 1; });
        var hayNub = C.n3000 !== undefined;
        var filas = ix, m3 = !hayHoras || modo === "3h";
        if (m3) filas = ix.filter(function (i) { return T[i].getUTCHours() % 3 === 0; });
        if (hayHoras) h += '<div class="mt-modo" role="group" aria-label="Detalle de la tabla"><button type="button" data-modo="1h" class="' + (modo === "1h" ? "on" : "") + '">Cada hora</button><button type="button" data-modo="3h" class="' + (modo === "3h" ? "on" : "") + '">Cada 3 horas</button></div>';
        h += '<div class="mt-scroll"><table class="mt-tab"><thead><tr><th>Hora</th><th>Cielo</th><th>Cumbre</th><th>Base</th><th>Precip.</th><th>Viento cumbre</th><th>Racha base</th>' + (hayNub ? NUB.map(function (a) { return '<th class="mt-nb">Nubes<br>' + a.toLocaleString("es-ES") + " m</th>"; }).join("") : "<th>Nubes</th>") + "<th>Isocero</th><th>Cota nieve</th></tr></thead><tbody>";
        filas.forEach(function (i) {
          var noche = +fH.format(T[i]) < 8 || +fH.format(T[i]) >= 20;
          var horas = DUR[i], pr = C.pr[i];
          if (m3 && DUR[i] === 1) {  // suma de las 3 horas anteriores
            pr = null; horas = 0;
            for (var j = i; j >= 0 && horas < 3; j--) { if (C.pr[j] != null) pr = (pr || 0) + C.pr[j]; horas += DUR[j]; }
          }
          h += "<tr><td>" + fHora.format(T[i]) + "</td><td>" + icono(iconoTramo(C, i, horas, pr), noche) + "</td><td><b>" + n(C.tc[i], "°") + "</b>" + sens(C.tc[i], C.st && C.st[i]) + "</td><td>" + n(C.tv[i], "°") + sens(C.tv[i], C.sv && C.sv[i]) + "</td><td>" + (pr ? dec(pr) + " mm" : "–") + "</td><td>" + flecha(C.dc[i]) + n(C.wc[i]) + " km/h " + dir(C.dc[i]) + "</td><td>" + n(C.gv[i]) + " km/h</td>" + (hayNub ? NUB.map(function (a) { return celdaNube(C["n" + a][i]); }).join("") : "<td>" + n(C.cc[i], "%") + "</td>") + "<td>" + (C.i0[i] == null ? "–" : C.i0[i].toLocaleString("es-ES") + " m") + "</td><td>" + (C.sl[i] == null || !pr ? "–" : C.sl[i].toLocaleString("es-ES") + " m") + "</td></tr>";
        });
        h += "</tbody></table></div><p class=\"muted small\">La precipitación de cada fila es la caída desde la fila anterior (" + (m3 ? "3 horas" : "1 hora") + "); el resto, el valor a esa hora. Mediana de los modelos. En azul, junto a la temperatura, la sensación térmica (frío por viento o calor por humedad). Nubes a cada altitud: estimadas con la humedad del aire a esa altura; «–» si esa altitud queda bajo el terreno de la zona. Las primeras 72 horas van hora a hora (ECMWF solo da datos cada 3 horas: entre medias se interpola).</p>";
        return h;
      }

      function graficas() {
        var d = dias[sel], ix = idxDia[d.fecha] || [0], rg = [ix[0], ix[ix.length - 1]];
        var fino = function (k, v) { return { v: v, c: MOD[k].c, w: 1.2, op: 0.55, dash: "3 3" }; };
        var gT = grafica({ titulo: "Temperatura", t: T, h: HH, unidad: "°C", cero: true, sel: rg, dias: marcas,
          series: mods.map(function (k) { return fino(k, doc.series[k].tc); }).concat([{ v: C.tv, c: "#b9a593", w: 2 }, { v: C.tc, c: "#f3e9df", w: 2.6 }]) });
        var gP = grafica({ titulo: "Precipitación", t: T, h: HH, unidad: "mm", min: 0, max: 2, sel: rg, dias: marcas, barras: { v: C.pr, c: "#3f84b8" },
          series: mods.map(function (k) { return { v: doc.series[k].pr, c: MOD[k].c, w: 1.3, op: 0.7 }; }), alto: 150 });
        var gW = grafica({ titulo: "Viento en cumbre", t: T, h: HH, unidad: "km/h", min: 0, sel: rg, dias: marcas,
          series: mods.map(function (k) { return fino(k, doc.series[k].wc); }).concat([{ v: C.wc, c: "#f3e9df", w: 2.6 }]), alto: 160 });
        var gI = grafica({ titulo: "Isocero", t: T, h: HH, unidad: "m", min: 0, sel: rg, dias: marcas,
          series: mods.map(function (k) { return fino(k, doc.series[k].i0); }).concat([{ v: C.i0, c: "#6fb3e0", w: 2.4 }]), alto: 150 });
        var ley = leyenda(mods.map(function (k) { return { c: MOD[k].c, l: MOD[k].n }; }));
        return '<div class="mt-g"><h3>Temperatura <small>°C</small></h3>' + leyenda([{ c: "#f3e9df", l: "Cumbre " + doc.cumbre.alt.toLocaleString("es-ES") + " m" }, { c: "#b9a593", l: "Base " + doc.base.alt.toLocaleString("es-ES") + " m" }]) + '<div class="mt-scroll">' + gT + "</div></div>" +
          '<div class="mt-g"><h3>Precipitación <small>mm por hora (cada 3 h desde el 4.º día)</small></h3><div class="mt-scroll">' + gP + "</div></div>" +
          '<div class="mt-g"><h3>Viento en cumbre <small>km/h</small></h3><div class="mt-scroll">' + gW + "</div></div>" +
          '<div class="mt-g"><h3>Isocero <small>metros</small></h3><div class="mt-scroll">' + gI + "</div></div>" + '<p class="muted small">Líneas de colores: cada modelo por separado. ' + ley + "</p>";
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
        var ae = doc.aemet || [];
        var bloque = ae.length ? '<div class="mt-aemet-box"><h3>Avisos de AEMET</h3><ul>' + ae.map(function (a) {
          return "<li>" + chipAemet(a, false) + " <b>" + esc(fenomeno(a)) + "</b> · " + esc(a.zona) + ' <span class="muted">(' + (a.inicio ? fAviso.format(new Date(a.inicio)) : "") + " – " + (a.fin ? fAviso.format(new Date(a.fin)) : "") + ")</span></li>";
        }).join("") + '</ul><p class="muted small">Avisos oficiales de la Agencia Estatal de Meteorología para la zona del pueblo base o de la cumbre. Consulta el detalle en <a href="https://www.aemet.es/es/eltiempo/prediccion/avisos" target="_blank" rel="noopener">aemet.es</a>.</p></div>' : "";
        el.innerHTML = '<div class="mt-cab"><h2>Tiempo en ' + esc(doc.nombre) + '</h2><p class="muted small">Cumbre: ' + esc(doc.cumbre.nombre) + " " + doc.cumbre.alt.toLocaleString("es-ES") + " m · Base: " + esc(doc.base.nombre) + " " + doc.base.alt.toLocaleString("es-ES") + ' m</p></div><p class="mt-act">' + actualizado(doc) + "</p>" + bloque + tira() +
          '<div class="mt-sec">' + detalleDia() + "</div>" +
          '<div class="mt-sec"><h2>Evolución a 7 días</h2>' + graficas() + "</div>" +
          '<div class="mt-sec"><h2>Comparación de modelos</h2>' + comparativa() + "</div>";
        el.querySelectorAll("[data-modo]").forEach(function (b) {
          b.addEventListener("click", function () { modo = b.getAttribute("data-modo"); var y = window.scrollY; pintar(); window.scrollTo(0, y); });
        });
        el.querySelectorAll(".mt-dia").forEach(function (b) {
          b.addEventListener("click", function () { sel = +b.getAttribute("data-k"); var y = window.scrollY; pintar(); window.scrollTo(0, y); });
        });
      }
      pintar();
    }).catch(function () { el.innerHTML = '<p class="mt-err">La previsión se está generando. Vuelve a intentarlo en unos minutos.</p>'; });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var a = document.getElementById("mt-index"); if (a) indice(a);
    var b = document.getElementById("mt-mac"); if (b && b.getAttribute("data-id")) ficha(b).catch(function () {});
    selector();
  });
})();
