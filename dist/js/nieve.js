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
    var za = ALUDES && ALUDES.macizos && ALUDES.macizos[m.id], ra = za && ALUDES.regiones[za];
    if (ra) { var va = (ra.dias || {})[ALUDES.fechas[0]]; h += '<p class="nv-oficial">Peligro de aludes oficial hoy (' + esc(ra.nombre) + "): " + (va ? chipAlud(va) : "<b>sin boletín en vigor</b>") + ' · <a href="' + esc(ra.url) + '" target="_blank" rel="noopener">boletín de ' + esc(ra.fuente) + "</a></p>"; }
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
  /* desplegables cordillera -> sierra, como en meteorología; la elección queda en la dirección (#id) */
  function selector(lista, zonaDe, nombreDe, labZ, labS, todasS, onCambio) {
    var zonas = [];
    lista.forEach(function (x) { if (zonas.indexOf(zonaDe(x)) < 0) zonas.push(zonaDe(x)); });
    var html = '<form class="mt-selbar" onsubmit="return false"><label><span>' + labZ + '</span><select class="sel-z"><option value="">Todas</option>' +
      zonas.map(function (z) { return "<option>" + esc(z) + "</option>"; }).join("") + '</select></label><label><span>' + labS + '</span><select class="sel-s"></select></label></form>';
    function rellenar(form, z, sel) {
      form.querySelector(".sel-s").innerHTML = '<option value="">' + todasS + "</option>" + lista.filter(function (x) { return !z || zonaDe(x) === z; }).map(function (x) {
        return '<option value="' + x.id + '"' + (x.id === sel ? " selected" : "") + ">" + esc(nombreDe(x)) + "</option>"; }).join("");
    }
    function montar(form) {
      var sz = form.querySelector(".sel-z"), ss = form.querySelector(".sel-s");
      function aplicar(id, z) {
        var x = lista.filter(function (y) { return y.id === id; })[0];
        if (x) z = zonaDe(x);
        sz.value = z || ""; rellenar(form, z, id);
        onCambio(id || "", z || "");
      }
      sz.addEventListener("change", function () {
        var de = lista.filter(function (y) { return !sz.value || zonaDe(y) === sz.value; });
        aplicar(de.length === 1 ? de[0].id : "", sz.value);
        history.replaceState(null, "", de.length === 1 ? "#" + de[0].id : location.pathname);
      });
      ss.addEventListener("change", function () { aplicar(ss.value, sz.value); history.replaceState(null, "", ss.value ? "#" + ss.value : location.pathname); });
      var ini = location.hash.slice(1);
      aplicar(lista.some(function (y) { return y.id === ini; }) ? ini : "", "");
      return aplicar;
    }
    return { html: html, montar: montar };
  }


  /* mapa: un copo por macizo, más grande cuanta más nieve (manto del modelo; discontinuo si solo hay nevada prevista) */
  function cargarLeaflet(cb) {
    if (window.L) return cb();
    var css = document.createElement("link"); css.rel = "stylesheet"; css.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"; document.head.appendChild(css);
    var js = document.createElement("script"); js.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"; js.onload = cb; document.head.appendChild(js);
  }
  function tam(cm) { return cm >= 80 ? 40 : cm >= 30 ? 36 : 32; }
  /* color por espesor del manto: 5 cm verde, 30 amarillo, 80 naranja, 150 rojo */
  var ESCALA = [[150, "#e8574a", "150 cm o más"], [80, "#f08a24", "80–150 cm"], [30, "#f5d000", "30–80 cm"], [5, "#4caf50", "5–30 cm"]];
  function colNieve(cm) { for (var i = 0; i < ESCALA.length; i++) if (cm >= ESCALA[i][0]) return ESCALA[i][1]; return "#bfe0f7"; }
  var mapa = null, capas = {};
  function pintarMapa(lista, elegido, alPulsar) {
    cargarLeaflet(function () {
      if (!mapa) {
        mapa = L.map("nv-mapa", { scrollWheelZoom: false, attributionControl: true });
        // mapa topográfico libre (OpenTopoMap); si no responde, el de OpenStreetMap
        var topo = L.tileLayer("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", { maxZoom: 13, subdomains: "abc",
          attribution: 'Mapa: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (CC-BY-SA) · datos &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' }).addTo(mapa);
        var fallos = 0;
        topo.on("tileerror", function () {
          if (++fallos === 4) { mapa.removeLayer(topo); L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 13, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' }).addTo(mapa); }
        });
      }
      Object.keys(capas).forEach(function (k) { mapa.removeLayer(capas[k]); }); capas = {};
      var pts = [];
      lista.forEach(function (m) {
        var manto = m.manto || 0, prev = m.nieve_prevista || 0, val = manto >= 3 ? manto : prev, solo = manto < 3 && prev >= 3;
        var col = solo ? "#c9a7e8" : colNieve(val), sz = m.hay_nieve ? tam(val) : 12;
        var html = m.hay_nieve ? '<div class="nv-pin' + (solo ? " nv-pin-p" : "") + (m.id === elegido ? " nv-pin-sel" : "") + '" style="width:' + sz + "px;height:" + sz + "px;--c:" + col + ';font-size:' + Math.round(sz * 0.55) + 'px">❄</div>' : '<div class="nv-pin nv-pin-0" style="width:12px;height:12px"></div>';
        var mk = L.marker([m.cumbre.lat, m.cumbre.lon], { icon: L.divIcon({ html: html, className: "", iconSize: [sz, sz], iconAnchor: [sz / 2, sz / 2] }), zIndexOffset: Math.round(val) });
        mk.bindTooltip("<b>" + esc(m.corto) + "</b><br>" + esc(m.estado) + "<br>Manto: " + n(m.manto, " cm") + " · prevista 3 días: " + n(m.nieve_prevista, " cm"), { direction: "top", offset: [0, -sz / 2] });
        mk.on("click", function () { alPulsar(m.id); });
        mk.addTo(mapa); capas[m.id] = mk; pts.push([m.cumbre.lat, m.cumbre.lon]);
      });
      var sel = lista.filter(function (m) { return m.id === elegido; })[0];
      if (sel) mapa.setView([sel.cumbre.lat, sel.cumbre.lon], 9);
      else if (pts.length > 1) mapa.fitBounds(pts, { padding: [30, 30], maxZoom: 9 });
      else if (pts.length) mapa.setView(pts[0], 9);
      setTimeout(function () { mapa.invalidateSize(); }, 50);
    });
  }
  var leyenda = '<div class="nv-ley"><b>Espesor del manto (cumbre):</b>' + ESCALA.slice().reverse().map(function (x) { return '<span><i class="nv-pin" style="width:24px;height:24px;--c:' + x[1] + ';font-size:13px">❄</i>' + x[2] + "</span>"; }).join("") +
    '<span><i class="nv-pin" style="width:24px;height:24px;--c:#bfe0f7;font-size:13px">❄</i>menos de 5 cm</span><span><i class="nv-pin nv-pin-p" style="width:24px;height:24px;--c:#c9a7e8;font-size:13px">❄</i>solo nevada prevista</span><span><i class="nv-pin nv-pin-0" style="width:12px;height:12px"></i>sin nieve</span></div>';

  /* mapa de peligro de aludes oficial (boletines de AEMET, ICGC, Arán y Andorra vía EAWS) */
  var ALUD = { 1: ["Débil", "#ccff66"], 2: ["Limitado", "#ffff00"], 3: ["Notable", "#ff9900"], 4: ["Fuerte", "#ff0000"], 5: ["Muy fuerte", "#1b120c"] };
  var ALUDES = null, mapaA = null, capaA = null, diaA = 0;
  function chipAlud(v) { var c = ALUD[v]; return c ? '<span class="nv-alud" style="--a:' + c[1] + (v >= 4 ? ";color:#fff" : "") + '">' + v + " · " + c[0] + "</span>" : ""; }
  function pintarAludes() {
    if (!ALUDES) return;
    var f = ALUDES.fechas[diaA];
    cargarLeaflet(function () {
      if (!mapaA) {
        mapaA = L.map("nv-mapa-aludes", { scrollWheelZoom: false });
        L.tileLayer("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", { maxZoom: 13, subdomains: "abc", opacity: .8,
          attribution: 'Peligro: boletines de AEMET, ICGC, Conselh Generau d\'Aran y Andorra (vía <a href="https://www.avalanches.org">EAWS</a>) · Mapa: &copy; OpenTopoMap, &copy; OpenStreetMap' }).addTo(mapaA);
      }
      if (capaA) mapaA.removeLayer(capaA);
      capaA = L.layerGroup();
      var b = [];
      Object.keys(ALUDES.zonas).forEach(function (id) {
        var r = ALUDES.regiones[id] || {}, v = (r.dias || {})[f], c = ALUD[v];
        ALUDES.zonas[id].forEach(function (an) {
          var pol = L.polygon(an, c ? { color: "#1b120c", weight: 1, fillColor: c[1], fillOpacity: .75 } : { color: "#8d847b", weight: 1, dashArray: "4 4", fillColor: "#8d847b", fillOpacity: .15 });
          pol.bindTooltip("<b>" + esc(r.nombre || id) + "</b><br>" + (c ? "Peligro " + v + " (" + c[0] + ")" : "Sin boletín para este día") + "<br><small>" + esc(r.fuente || "") + "</small>", { sticky: true });
          pol.on("click", function () { if (r.url) window.open(r.url, "_blank", "noopener"); });
          capaA.addLayer(pol); an.forEach(function (p) { b.push(p); });
        });
      });
      capaA.addTo(mapaA);
      if (b.length && !mapaA._ajustado) { mapaA.fitBounds(b, { padding: [20, 20] }); mapaA._ajustado = true; }
      setTimeout(function () { mapaA.invalidateSize(); }, 50);
      var hay = Object.keys(ALUDES.regiones).some(function (k) { return (ALUDES.regiones[k].dias || {})[f]; });
      document.getElementById("nv-al-nota").innerHTML = hay ? "" : "Ahora mismo no hay boletines de peligro de aludes en vigor para este día (fuera de temporada o aún no publicados). Las zonas en gris son las que tienen boletín oficial durante la temporada.";
    });
  }
  function bloqueAludes() {
    var fmt = new Intl.DateTimeFormat("es-ES", { timeZone: "UTC", weekday: "long", day: "numeric", month: "long" });
    var fd = function (s) { var p = s.split("-"); return fmt.format(new Date(Date.UTC(+p[0], +p[1] - 1, +p[2], 12))); };
    return '<section class="nv-aludes"><h2>Peligro de aludes oficial</h2><p class="muted small">Nivel máximo de cada zona según los boletines oficiales. Pulsa una zona para abrir su boletín.</p>' +
      '<div class="mt-modo" role="group" aria-label="Día">' + ALUDES.fechas.map(function (f, i) { return '<button type="button" data-ad="' + i + '" class="' + (i === diaA ? "on" : "") + '">' + (i ? "Mañana" : "Hoy") + " · " + fd(f) + "</button>"; }).join("") + "</div>" +
      '<div id="nv-mapa-aludes" class="nv-mapa" role="region" aria-label="Mapa de peligro de aludes"></div><p id="nv-al-nota" class="muted small"></p>' +
      '<div class="nv-ley"><b>Escala europea:</b>' + [1, 2, 3, 4, 5].map(function (v) { return chipAlud(v); }).join("") + '<span><i style="display:inline-block;width:18px;height:12px;border:1px dashed #8d847b;background:rgba(141,132,123,.15);margin-right:6px"></i>sin boletín</span></div></section>';
  }

  var pAludes = fetch("/meteo/datos/aludes.json?t=" + Math.floor(Date.now() / 6e5), { cache: "no-cache" }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
  fetch("/meteo/datos/nieve.json?t=" + Math.floor(Date.now() / 6e5), { cache: "no-cache" }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (d) {
    var aplicar;
    var S = selector(d.macizos, function (m) { return m.region; }, function (m) { return m.nombre; }, "Cordillera", "Sierra o macizo", "Todas las sierras", function (id, z) {
      var de = d.macizos.filter(function (m) { return !z || m.region === z; });
      var vis = id ? d.macizos.filter(function (m) { return m.id === id; }) : de.filter(function (m) { return m.hay_nieve; });
      var sin = id ? [] : de.filter(function (m) { return !m.hay_nieve; });
      cont.innerHTML = (vis.length ? '<div class="nv-cards">' + vis.map(tarjeta).join("") + "</div>" : '<p class="nv-nada">Ahora mismo los modelos no ven nieve significativa en ninguna cumbre de esta zona.</p>') +
        (sin.length ? '<h2 class="nv-sin-t">Sin nieve significativa</h2><p class="nv-sin">' + sin.map(function (m) { return '<a href="#' + m.id + '" data-id="' + m.id + '">' + esc(m.corto) + "</a>"; }).join(" · ") + "</p>" : "");
      cont.querySelectorAll("details.nv-cams").forEach(function (dt) {
        dt.addEventListener("toggle", function () { var f = dt.querySelector("iframe"); if (dt.open && !f.src) f.src = f.getAttribute("data-src"); });
      });
      cont.querySelectorAll("a[data-id]").forEach(function (a) { a.addEventListener("click", function (ev) { ev.preventDefault(); elegir(a.getAttribute("data-id")); }); });
      pintarMapa(de, id, elegir);
    });
    function elegir(id) { history.replaceState(null, "", "#" + id); aplicar(id, ""); window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 90, behavior: "smooth" }); }
    pAludes.then(function (A) {
      if (!A || !A.zonas) return;
      ALUDES = A;
      var box = document.createElement("div"); box.innerHTML = bloqueAludes(); el.insertBefore(box.firstChild, document.getElementById("nv-cont"));
      el.querySelectorAll("[data-ad]").forEach(function (b) { b.addEventListener("click", function () { diaA = +b.getAttribute("data-ad"); el.querySelectorAll("[data-ad]").forEach(function (x) { x.classList.toggle("on", x === b); }); pintarAludes(); }); });
      pintarAludes();
      aplicar(location.hash.slice(1), "");
    });
    el.innerHTML = S.html + '<p class="mt-act">Actualizado el ' + fAct.format(new Date(d.generado.replace("Z", ":00Z"))) + " · 4 veces al día con la previsión de meteorología</p>" +
      '<div id="nv-mapa" class="nv-mapa" role="region" aria-label="Mapa de la nieve por macizo"></div>' + leyenda + '<div id="nv-cont"></div>';
    var cont = document.getElementById("nv-cont");
    aplicar = S.montar(el.querySelector(".mt-selbar"));
  }).catch(function (e) { console.error(e); el.innerHTML = '<p class="mt-err">El estado de la nieve se está calculando. Vuelve a intentarlo en unos minutos.</p>'; });
})();
