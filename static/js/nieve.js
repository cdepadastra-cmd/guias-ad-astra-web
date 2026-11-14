/* Estado de la nieve: lee /meteo/datos/nieve.json (calculado con los modelos y el histórico) y pinta una tarjeta por macizo. */
(function () {
  "use strict";
  var TZ = "Europe/Madrid";
  var fAct = new Intl.DateTimeFormat("es-ES", { timeZone: TZ, weekday: "long", day: "numeric", month: "long", hour: "2-digit", minute: "2-digit", hour12: false });
  var fDia = new Intl.DateTimeFormat("es-ES", { timeZone: "UTC", weekday: "short", day: "numeric" });
  var COL = { "Placas de viento probables": "#e8574a", "Nieve reciente": "#f08a3e", "Nieve húmeda": "#e9c46a", "Nieve húmeda / fusión": "#e9c46a",
    "Costra de rehielo": "#6fb3e0", "Nevadas previstas": "#c9a7e8", "Nieve fría / polvo": "#bfe0f7", "Nieve asentada": "#7cc47f", "Sin nieve significativa": "#8d847b" };
  var NIV = { alto: "#e8574a", medio: "#e9c46a", info: "#8d847b" };
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function n(v, s) { return v == null ? "–" : Math.round(v) + (s || ""); }
  function dia(f) { var p = f.split("-"); return fDia.format(new Date(Date.UTC(+p[0], +p[1] - 1, +p[2], 12))); }
  var CAMS = {};
  try { CAMS = JSON.parse(document.getElementById("nv-cams").textContent); } catch (e) {}

  function tabla(m) {
    var d = m.dias.slice(-10);
    return '<div class="nv-tw"><table class="nv-t"><thead><tr><th></th>' + d.map(function (x) { return '<th class="nv-' + x.tipo + '">' + esc(dia(x.fecha)) + "</th>"; }).join("") + "</tr></thead><tbody>" +
      "<tr><th>Cumbre</th>" + d.map(function (x) { return "<td>" + n(x.tc_min, "°") + " / " + n(x.tc_max, "°") + "</td>"; }).join("") + "</tr>" +
      "<tr><th>Nieve nueva</th>" + d.map(function (x) { return "<td>" + (x.nieve ? "<b>" + x.nieve + " cm</b>" : "–") + "</td>"; }).join("") + "</tr>" +
      "<tr><th>Lluvia</th>" + d.map(function (x) { return "<td>" + (x.lluvia >= 0.5 ? x.lluvia.toLocaleString("es-ES") + " mm" : "–") + "</td>"; }).join("") + "</tr>" +
      "<tr><th>Viento máx.</th>" + d.map(function (x) { return "<td>" + n(x.wc_max) + (x.wc_dir ? " " + x.wc_dir : "") + "</td>"; }).join("") + "</tr>" +
      "<tr><th>Isocero</th>" + d.map(function (x) { return "<td>" + (x.i0_max == null ? "–" : x.i0_max.toLocaleString("es-ES") + " m") + "</td>"; }).join("") + "</tr>" +
      "</tbody></table></div>";
  }

  function tarjeta(m) {
    var col = COL[m.estado] || "#8d847b", c = CAMS[m.id] || {};
    var h = '<article class="nv-card" id="' + m.id + '" style="--nv:' + col + '"><header><div><h2>' + esc(m.nombre) + '</h2><p class="muted small">' + esc(m.cumbre.nombre) + " " + m.cumbre.alt.toLocaleString("es-ES") + " m · " + esc(m.region) + '</p></div><span class="nv-estado">' + esc(m.estado) + "</span></header>";
    h += '<div class="nv-kv"><div><b>' + n(m.manto, " cm") + "</b><span>Manto (modelo, cumbre)</span></div><div><b>" + n(m.nieve_72h, " cm") + "</b><span>Nieve nueva 3 días</span></div><div><b>" + n(m.nieve_prevista, " cm") + "</b><span>Prevista 3 días</span></div><div><b>" + n(m.manto_base, " cm") + "</b><span>Manto en " + esc(m.base.nombre) + "</span></div></div>";
    h += '<ul class="nv-s">' + m.senales.map(function (s) { return '<li style="--c:' + NIV[s.nivel] + '">' + esc(s.txt) + "</li>"; }).join("") + "</ul>";
    h += tabla(m);
    if (c.windy && c.windy.length) h += '<details class="nv-cams"><summary>Ver webcam (' + esc(c.windy[0][1]) + ")</summary>" + '<div class="mt-cam-v"><iframe data-src="https://webcams.windy.com/webcams/public/embed/player/' + esc(c.windy[0][0]) + '/day" title="Webcam ' + esc(c.windy[0][1]) + '" loading="lazy" allowfullscreen></iframe></div></details>';
    else if (c.enlaces && c.enlaces.length) h += '<p class="small">Webcam: <a href="' + esc(c.enlaces[0][0]) + '" target="_blank" rel="noopener">' + esc(c.enlaces[0][1]) + "</a></p>";
    h += '<p class="nv-links small"><a href="/meteo/' + m.id + '/">Previsión completa</a>' + (m.boletines || []).map(function (b) { return ' · <a href="' + esc(b[1]) + '" target="_blank" rel="noopener">' + esc(b[0]) + "</a>"; }).join("") + "</p>";
    if (m.historico_horas < 48) h += '<p class="muted small">El histórico de días pasados se está acumulando: la estimación mejora con los días.</p>';
    return h + "</article>";
  }

  var el = document.getElementById("nv-lista");
  if (!el) return;
  fetch("/meteo/datos/nieve.json?t=" + Math.floor(Date.now() / 6e5), { cache: "no-cache" }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (d) {
    var con = d.macizos.filter(function (m) { return m.hay_nieve; }), sin = d.macizos.filter(function (m) { return !m.hay_nieve; });
    el.innerHTML = '<p class="mt-act">Actualizado el ' + fAct.format(new Date(d.generado.replace("Z", ":00Z"))) + " · 4 veces al día con la previsión de meteorología</p>" +
      (con.length ? '<div class="nv-cards">' + con.map(tarjeta).join("") + "</div>" : '<p class="nv-nada">Ahora mismo los modelos no ven nieve significativa en ninguna cumbre.</p>') +
      (sin.length ? '<h2 class="nv-sin-t">Sin nieve significativa</h2><p class="nv-sin">' + sin.map(function (m) { return '<a href="/meteo/' + m.id + '/">' + esc(m.corto) + "</a>"; }).join(" · ") + "</p>" : "");
    el.querySelectorAll("details.nv-cams").forEach(function (dt) {
      dt.addEventListener("toggle", function () { var f = dt.querySelector("iframe"); if (dt.open && !f.src) f.src = f.getAttribute("data-src"); });
    });
  }).catch(function () { el.innerHTML = '<p class="mt-err">El estado de la nieve se está calculando. Vuelve a intentarlo en unos minutos.</p>'; });
})();
