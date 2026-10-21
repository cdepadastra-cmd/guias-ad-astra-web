/* Guías Ad Astra · interacción de la web (sin dependencias) */
(function () {
  "use strict";
  var CFG = window.ADASTRA_CONFIG || {};
  var WA = CFG.whatsapp || "34621075048";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var eur = function (n) { return (Math.round(n * 100) / 100).toLocaleString("es-ES") + " €"; };
  var DIAS = ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"];
  var MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
  function parseDate(s) { var p = String(s).slice(0, 10).split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function iso(d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
  function fmtLong(s) { var d = parseDate(s); return DIAS[d.getDay()] + " " + d.getDate() + " de " + MESES[d.getMonth()] + " de " + d.getFullYear(); }
  function fmtShort(s) { var d = parseDate(s); return d.getDate() + "/" + (d.getMonth() + 1) + "/" + d.getFullYear(); }
  function todayISO() { return iso(new Date()); }
  function waURL(text) { return "https://wa.me/" + WA + "?text=" + encodeURIComponent(text); }
  function openWA(text) {
    var url = waURL(text);
    var w = window.open(url, "_blank", "noopener");
    if (!w) location.href = url;
    return url;
  }
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function telOK(t) { return t.replace(/\D/g, "").length >= 9; }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  /* ---------------- menú */
  var tog = $(".menu-toggle"), nav = $(".nav");
  if (tog && nav) tog.addEventListener("click", function () { var o = nav.classList.toggle("open"); tog.setAttribute("aria-expanded", o); });
  $$(".dd > button").forEach(function (b) {
    b.addEventListener("click", function () { var dd = b.parentNode; var o = dd.classList.toggle("open"); b.setAttribute("aria-expanded", o); });
  });

  /* ---------------- steppers */
  function bindStepper(st, onChange) {
    var inp = $("input", st), min = +inp.min || 0, max = +inp.max || 99;
    function set(v) { v = Math.max(min, Math.min(max, v | 0)); inp.value = v; onChange && onChange(v); }
    $$("button", st).forEach(function (b) { b.addEventListener("click", function () { set((+inp.value || 0) + (+b.dataset.step)); }); });
    inp.addEventListener("input", function () { set(+inp.value); });
    return set;
  }

  /* ---------------- filtros de listados */
  $$("[data-filter]").forEach(function (bar) {
    var target = $(bar.dataset.filter), key = bar.dataset.key || "cat";
    function apply(val) {
      $$(".chip", bar).forEach(function (c) { c.setAttribute("aria-pressed", c.dataset.val === val); });
      $$("[data-" + key + "]", target).forEach(function (el) {
        var vals = (el.getAttribute("data-" + key) || "").split("|");
        el.hidden = !(val === "" || vals.indexOf(val) > -1);
      });
      $$(".cat-section", target).forEach(function (sec) { sec.hidden = !$$(".card:not([hidden])", sec).length; });
    }
    $$(".chip", bar).forEach(function (c) { c.addEventListener("click", function () { apply(c.dataset.val); }); });
    var q = new URLSearchParams(location.search).get(bar.dataset.param || "categoria");
    if (q) {
      var m = $$(".chip", bar).filter(function (c) { return c.dataset.val.toLowerCase() === q.toLowerCase(); })[0];
      apply(m ? m.dataset.val : "");
    }
  });

  /* ---------------- reserva de actividad / curso por WhatsApp */
  $$("form[data-book]").forEach(function (f) {
    var title = f.dataset.title, base = +f.dataset.price || 0;
    var sel = $("select[name=opcion]", f), date = $("input[name=fecha]", f), out = $("[data-total]", f);
    var pers = 2;
    if (date) date.min = todayISO();
    var st = $(".stepper", f); if (st) bindStepper(st, function (v) { pers = v; calc(); });
    function price() { if (sel && sel.selectedOptions[0] && sel.selectedOptions[0].dataset.price) return +sel.selectedOptions[0].dataset.price; return base; }
    function calc() { if (out) out.textContent = price() ? eur(price() * pers) : "A consultar"; }
    if (sel) sel.addEventListener("change", calc);
    $$("[data-pick]").forEach(function (b) {
      b.addEventListener("click", function () { if (sel) { sel.value = b.dataset.pick; calc(); } f.scrollIntoView({ behavior: "smooth", block: "start" }); setTimeout(function () { date && date.focus({ preventScroll: true }); }, 450); });
    });
    calc();
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var err = $(".err", f); if (err) err.textContent = "";
      var val = function (n) { var i = $("[name=" + n + "]", f); return i ? i.value.trim() : ""; };
      var fail = function (n, m) { if (err) err.textContent = m; var i = $("[name=" + n + "]", f); if (i) i.focus(); };
      var nombre = val("nombre"), full = f.hasAttribute("data-full");
      if (date && !date.value) { if (err) err.textContent = "Elige el día que quieres hacer la actividad."; date.focus(); return; }
      if (!nombre) return fail("nombre", "Escribe tu nombre.");
      if (full) {
        if (!val("apellidos")) return fail("apellidos", "Escribe tus apellidos.");
        if (!EMAIL.test(val("email"))) return fail("email", "Revisa el correo electrónico (ejemplo: nombre@gmail.com).");
        if (!telOK(val("telefono"))) return fail("telefono", "Revisa el número de teléfono (9 cifras).");
      }
      var quote = f.hasAttribute("data-presupuesto");
      var lines = quote ? ["Hola, quiero pedir información / presupuesto a Guías Ad Astra:", "", "• Servicio: " + title] : ["Hola, quiero reservar en Guías Ad Astra:", "", (f.hasAttribute("data-curso") ? "• Curso: " : "• Actividad: ") + title];
      if (sel) lines.push("• Opción: " + sel.value);
      if (date) lines.push("• Fecha: " + fmtLong(date.value));
      var alt = $("input[name=fecha2]", f); if (alt && alt.value) lines.push("• Fecha alternativa: " + fmtLong(alt.value));
      if (!quote) lines.push("• Personas: " + pers);
      if (val("entidad")) lines.push("• Entidad: " + val("entidad"));
      if (price()) lines.push("• Total estimado: " + eur(price() * pers) + " (" + eur(price()) + "/persona)");
      lines.push("• Nombre: " + nombre + (full ? " " + val("apellidos") : ""));
      if (full) { lines.push("• Email: " + val("email")); lines.push("• Teléfono: " + val("telefono")); }
      var com = $("textarea", f); if (com && com.value.trim()) lines.push("• Comentarios: " + com.value.trim());
      lines.push("", quote ? "Gracias." : "¿Tenéis disponibilidad?");
      openWA(lines.join("\n"));
    });
  });

  /* ---------------- inscripciones (Gredos Limpio) → Google Sheets */
  $$("form[data-inscripcion]").forEach(function (f) {
    var pers = 1, st = $(".stepper", f); if (st) bindStepper(st, function (v) { pers = v; });
    var err = $(".err", f), ok = $("[data-ok]", f), btn = $("button[type=submit]", f);
    f.addEventListener("submit", function (e) {
      e.preventDefault(); err.textContent = "";
      var v = function (n) { var i = $("[name=" + n + "]", f); return i ? i.value.trim() : ""; };
      var fail = function (n, m) { err.textContent = m; var i = $("[name=" + n + "]", f); if (i) i.focus(); };
      if (!v("nombre")) return fail("nombre", "Escribe tu nombre.");
      if (!v("apellidos")) return fail("apellidos", "Escribe tus apellidos.");
      if (!EMAIL.test(v("email"))) return fail("email", "Revisa el correo electrónico (ejemplo: nombre@gmail.com).");
      if (!telOK(v("telefono"))) return fail("telefono", "Revisa el número de teléfono (9 cifras).");
      if (!$("[name=privacidad]", f).checked) return fail("privacidad", "Marca la casilla de protección de datos para poder inscribirte.");
      var url = CFG.appsScriptURL || CFG.calendarioURL;
      if (!url) { err.textContent = "Las inscripciones online todavía no están activas. Inténtalo de nuevo más tarde."; return; }
      btn.disabled = true; btn.textContent = "Enviando…";
      var data = { action: "inscripcion", evento: f.dataset.evento, edicion: f.dataset.edicion, nombre: v("nombre"), apellidos: v("apellidos"), email: v("email"), telefono: v("telefono"), localidad: v("localidad"), personas: pers, comentarios: v("comentarios") };
      fetch(url, { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify(data) })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j.ok) throw new Error(j.error || "No se pudo guardar la inscripción.");
          $$(".field, .row2, .check, button[type=submit]", f).forEach(function (x) { x.hidden = true; });
          ok.hidden = false;
          ok.innerHTML = "<b>¡Inscripción recibida, " + esc(data.nombre) + "!</b><br>Te hemos apuntado " + (pers > 1 ? "con " + pers + " personas " : "") + "a " + esc(data.edicion) + ". Recibirás un correo de confirmación en " + esc(data.email) + ".";
        })
        .catch(function (x) { err.textContent = (x && x.message && x.message.indexOf("JSON") < 0 ? x.message : "No hemos podido enviar la inscripción. Revisa tu conexión e inténtalo de nuevo."); btn.disabled = false; btn.textContent = "Enviar inscripción"; });
    });
  });

  /* ---------------- alquiler */
  var rent = $("#alquiler-app");
  if (rent) (function () {
    var d1 = $("#r-desde"), d2 = $("#r-hasta"), daysOut = $("#r-dias"), bar = $(".mbar"), dlg = $("#r-dlg");
    var qty = {}, items = {};
    $$(".rent-card").forEach(function (c) {
      var id = c.dataset.id; items[id] = { name: c.dataset.name, price: +c.dataset.price };
      bindStepper($(".stepper", c), function (v) { qty[id] = v; c.classList.toggle("on", v > 0); update(); });
    });
    var t = todayISO(); d1.min = t; d2.min = t;
    function days() {
      if (!d1.value) return 0;
      var a = parseDate(d1.value), b = d2.value ? parseDate(d2.value) : a;
      var n = Math.round((b - a) / 864e5) + 1; return n > 0 ? n : 0;
    }
    function sel() { return Object.keys(qty).filter(function (k) { return qty[k] > 0; }); }
    function update() {
      if (d1.value) { d2.min = d1.value; if (d2.value && d2.value < d1.value) d2.value = d1.value; }
      var n = days(); daysOut.textContent = n ? n + (n === 1 ? " día" : " días") : "—";
      var ids = sel(), units = 0, perDay = 0;
      ids.forEach(function (k) { units += qty[k]; perDay += qty[k] * items[k].price; });
      bar.hidden = !ids.length; document.body.classList.toggle("has-mbar", ids.length > 0);
      $("#m-total").textContent = n ? eur(perDay * n) : eur(perDay) + "/día";
      $("#m-info").textContent = units + (units === 1 ? " unidad" : " unidades") + (n ? " · " + n + (n === 1 ? " día" : " días") : " · elige fechas");
      var ul = $("#r-list"); ul.innerHTML = "";
      ids.forEach(function (k) {
        var li = document.createElement("li");
        li.innerHTML = "<span>" + qty[k] + " × " + esc(items[k].name) + "</span><span>" + eur(qty[k] * items[k].price * (n || 1)) + "</span>";
        ul.appendChild(li);
      });
      $("#r-sum").textContent = n ? eur(perDay * n) : "Elige las fechas";
      $("#r-when").textContent = d1.value ? (n > 1 ? "Del " + fmtShort(d1.value) + " al " + fmtShort(d2.value || d1.value) : fmtLong(d1.value)) : "Sin fechas";
    }
    [d1, d2].forEach(function (i) { i.addEventListener("change", update); });
    $("#m-open").addEventListener("click", function () { update(); dlg.showModal(); });
    $$("[data-close]", dlg).forEach(function (b) { b.addEventListener("click", function () { dlg.close(); }); });
    $("#r-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var err = $("#r-err"); err.textContent = "";
      var n = days(), ids = sel(), nombre = $("#r-nombre").value.trim();
      if (!n) { err.textContent = "Elige el día de recogida (y el de devolución si es más de un día)."; dlg.close(); d1.focus(); d1.scrollIntoView({ block: "center" }); return; }
      if (!ids.length) { err.textContent = "Añade al menos un artículo."; return; }
      if (!nombre) { err.textContent = "Escribe tu nombre."; $("#r-nombre").focus(); return; }
      var perDay = 0, lines = ["Hola, quiero alquilar material:", ""];
      lines.push("• Fechas: " + (n > 1 ? "del " + fmtLong(d1.value) + " al " + fmtLong(d2.value) : fmtLong(d1.value)) + " (" + n + (n === 1 ? " día" : " días") + ")", "");
      ids.forEach(function (k) { perDay += qty[k] * items[k].price; lines.push("• " + qty[k] + " × " + items[k].name + " — " + eur(qty[k] * items[k].price * n)); });
      lines.push("", "Total estimado: " + eur(perDay * n) + " (IVA incluido)");
      var pts = $("#r-punto").value; if (pts) lines.push("Recogida: " + pts);
      var tall = $("#r-notas").value.trim(); if (tall) lines.push("Tallas / notas: " + tall);
      lines.push("Nombre: " + nombre, "", "¿Está disponible?");
      openWA(lines.join("\n"));
    });
    update();
  })();

  /* ---------------- calendario de actividades y cursos */
  var calRoots = $$("[data-calendar], [data-upcoming]");
  if (!calRoots.length) return;
  var EVENTS = [], LIVE = !!CFG.calendarioURL;

  function norm(e) {
    var max = +e.plazas_max || 0, res = +e.plazas_reservadas || 0;
    return {
      id: String(e.id), fecha: String(e.fecha).slice(0, 10), fecha_fin: e.fecha_fin ? String(e.fecha_fin).slice(0, 10) : "",
      hora: e.hora || "", titulo: e.titulo || "", tipo: (e.tipo || "Actividad").toLowerCase().indexOf("curso") > -1 ? "curso" : "actividad",
      slug: e.slug || "", precio: +e.precio || 0, max: max, libres: Math.max(0, e.plazas_libres != null && e.plazas_libres !== "" ? +e.plazas_libres : max - res),
      lugar: e.lugar || "", notas: e.notas || ""
    };
  }
  function load() {
    var url = LIVE ? CFG.calendarioURL + (CFG.calendarioURL.indexOf("?") > -1 ? "&" : "?") + "action=list&t=" + Date.now() : (CFG.base || "") + "/data/calendario.json";
    return fetch(url).then(function (r) { return r.json(); }).then(function (j) {
      var arr = Array.isArray(j) ? j : (j.events || []);
      EVENTS = arr.map(norm).filter(function (e) { return e.fecha && (e.fecha_fin || e.fecha) >= todayISO(); }).sort(function (a, b) { return a.fecha < b.fecha ? -1 : 1; });
      return EVENTS;
    }).catch(function () { EVENTS = []; return EVENTS; });
  }
  function seatsHTML(e) {
    var pct = e.max ? Math.round(e.libres / e.max * 100) : 0;
    var cls = e.libres === 0 ? "zero" : (e.libres <= Math.max(2, Math.ceil(e.max * 0.25)) ? "low" : "");
    var txt = e.libres === 0 ? "Completo" : e.libres + " de " + e.max + " plazas libres";
    return '<div class="seats ' + cls + '"><div class="bar"><i style="width:' + pct + '%"></i></div><small>' + txt + "</small></div>";
  }
  function dateRange(e) { return e.fecha_fin && e.fecha_fin !== e.fecha ? fmtShort(e.fecha) + " – " + fmtShort(e.fecha_fin) : fmtLong(e.fecha); }

  /* modal de reserva con plazas */
  var dlg = document.createElement("dialog");
  dlg.innerHTML = '<form class="dlg" method="dialog" id="ev-form" novalidate><div class="dlg-head"><div><p class="eyebrow" id="ev-type"></p><h2 id="ev-title"></h2></div><button type="button" class="icon-btn" data-x aria-label="Cerrar">×</button></div>' +
    '<p class="muted" id="ev-when"></p><div id="ev-seats"></div>' +
    '<div class="field"><label for="ev-pers">Plazas que quieres reservar</label><div class="stepper"><button type="button" data-step="-1" aria-label="Menos">−</button><input id="ev-pers" type="number" min="1" max="10" value="1" inputmode="numeric"><button type="button" data-step="1" aria-label="Más">+</button></div></div>' +
    '<div class="row2"><div class="field"><label for="ev-nombre">Nombre</label><input id="ev-nombre" autocomplete="given-name" required></div><div class="field" data-curso><label for="ev-ape">Apellidos</label><input id="ev-ape" autocomplete="family-name"></div></div>' +
    '<div class="row2"><div class="field" data-curso><label for="ev-email">Correo electrónico</label><input id="ev-email" type="email" autocomplete="email" inputmode="email"></div><div class="field"><label for="ev-tel">Teléfono</label><input id="ev-tel" type="tel" autocomplete="tel" inputmode="tel" required></div></div>' +
    '<div class="total"><span class="label">Total</span><strong id="ev-total"></strong></div>' +
    '<p class="err" id="ev-err"></p><div id="ev-done" hidden></div>' +
    '<button class="btn btn-wa btn-block" id="ev-send" type="submit">' + waIcon() + " Reservar y enviar por WhatsApp</button>" +
    '<p class="hint">Tu plaza queda apartada y te escribimos por WhatsApp para confirmar y gestionar el pago.</p></form>';
  document.body.appendChild(dlg);
  var cur = null, pers = 1;
  var setPers = bindStepper($(".stepper", dlg), function (v) { pers = v; if (cur) $("#ev-total").textContent = cur.precio ? eur(cur.precio * v) : "Gratis"; });
  $("[data-x]", dlg).addEventListener("click", function () { dlg.close(); });
  function openReserve(id) {
    cur = EVENTS.filter(function (e) { return e.id === id; })[0]; if (!cur) return;
    $("#ev-type").textContent = cur.tipo === "curso" ? "Curso" : "Actividad";
    $("#ev-title").textContent = cur.titulo;
    $("#ev-when").textContent = dateRange(cur) + (cur.hora ? " · " + cur.hora : "") + (cur.lugar ? " · " + cur.lugar : "");
    $("#ev-seats").innerHTML = seatsHTML(cur);
    $("#ev-pers").max = Math.max(1, cur.libres); setPers(1);
    $("#ev-err").textContent = ""; $("#ev-done").hidden = true; $("#ev-send").hidden = false; $("#ev-send").disabled = cur.libres === 0;
    dlg.showModal();
  }
  $("#ev-form", dlg).addEventListener("submit", function (e) {
    e.preventDefault();
    var nombre = $("#ev-nombre").value.trim(), ape = $("#ev-ape").value.trim(), email = $("#ev-email").value.trim(), tel = $("#ev-tel").value.trim(), err = $("#ev-err");
    err.textContent = "";
    var fail = function (id, m) { err.textContent = m; $(id).focus(); };
    if (!nombre) return fail("#ev-nombre", "Escribe tu nombre.");
    if (!ape) return fail("#ev-ape", "Escribe tus apellidos.");
    if (!EMAIL.test(email)) return fail("#ev-email", "Revisa el correo electrónico (ejemplo: nombre@gmail.com).");
    if (!telOK(tel)) return fail("#ev-tel", "Revisa el número de teléfono (9 cifras).");
    if (pers > cur.libres) { err.textContent = "Solo quedan " + cur.libres + " plazas."; return; }
    var msg = ["Hola, acabo de reservar desde el calendario de la web:", "", "• " + (cur.tipo === "curso" ? "Curso" : "Actividad") + ": " + cur.titulo, "• Fecha: " + dateRange(cur) + (cur.hora ? " a las " + cur.hora : ""), cur.lugar ? "• Lugar: " + cur.lugar : null, "• Plazas: " + pers, cur.precio ? "• Total: " + eur(cur.precio * pers) : null, "• Nombre: " + nombre + (ape ? " " + ape : ""), email ? "• Email: " + email : null, "• Teléfono: " + tel, "", "¿Me confirmáis la reserva?"].filter(Boolean).join("\n");
    var btn = $("#ev-send"); btn.disabled = true;
    var done = function (left) {
      if (left != null) { cur.libres = left; }
      $("#ev-seats").innerHTML = seatsHTML(cur);
      var url = waURL(msg);
      $("#ev-done").innerHTML = '<div class="notice ok">Plaza apartada. Pulsa el botón para enviarnos el mensaje y confirmar.</div><a class="btn btn-wa btn-block" target="_blank" rel="noopener" href="' + url + '">' + waIcon() + " Abrir WhatsApp</a>";
      $("#ev-done").hidden = false; btn.hidden = true; renderAll(); window.open(url, "_blank", "noopener");
    };
    if (!LIVE) { done(null); return; }
    fetch(CFG.calendarioURL, { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify({ action: "reservar", id: cur.id, plazas: pers, nombre: nombre, apellidos: ape, email: email, telefono: tel }) })
      .then(function (r) { return r.json(); })
      .then(function (j) { if (j.ok) done(j.libres); else { err.textContent = j.error || "No se pudo reservar."; if (j.libres != null) { cur.libres = j.libres; $("#ev-seats").innerHTML = seatsHTML(cur); renderAll(); } btn.disabled = false; } })
      .catch(function () { err.textContent = "No hemos podido conectar. Puedes reservar igualmente por WhatsApp."; btn.disabled = false; done(null); });
  });

  function evRow(e) {
    var d = parseDate(e.fecha);
    return '<article class="evrow" data-tipo="' + e.tipo + '"><div class="evdate"><b>' + d.getDate() + "</b><span>" + MESES[d.getMonth()].slice(0, 3) + " " + String(d.getFullYear()).slice(2) + '</span></div>' +
      '<div class="evinfo"><span class="tag">' + (e.tipo === "curso" ? "Curso" : "Actividad") + "</span><h3>" + (e.slug ? '<a href="' + (CFG.base || "") + '/actividades/' + esc(e.slug) + '/" style="color:inherit">' + esc(e.titulo) + "</a>" : esc(e.titulo)) + "</h3>" +
      '<p class="meta">' + esc(dateRange(e)) + (e.hora ? " · " + esc(e.hora) : "") + (e.lugar ? " · " + esc(e.lugar) : "") + (e.notas ? "<br>" + esc(e.notas) : "") + "</p>" + seatsHTML(e) + "</div>" +
      '<div class="evact"><span class="price">' + (e.precio ? eur(e.precio) : "Gratis") + '</span><button class="btn ' + (e.libres ? "btn-primary" : "btn-ghost") + '" data-res="' + esc(e.id) + '"' + (e.libres ? "" : " disabled") + ">" + (e.libres ? "Reservar plaza" : "Completo") + "</button></div></article>";
  }
  var view = new Date(); view.setDate(1); var tipo = "";
  function renderCalendar(root) {
    var list = $("[data-evlist]", root), grid = $("[data-month]", root), title = $("[data-mtitle]", root);
    var evs = EVENTS.filter(function (e) { return !tipo || e.tipo === tipo; });
    title.textContent = MESES[view.getMonth()] + " " + view.getFullYear();
    var first = new Date(view), start = (first.getDay() + 6) % 7, d = new Date(first); d.setDate(1 - start);
    var html = ["L", "M", "X", "J", "V", "S", "D"].map(function (x, i) { return '<div class="dow">' + ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"][i] + "</div>"; }).join("");
    for (var i = 0; i < 42; i++) {
      var s = iso(d), out = d.getMonth() !== view.getMonth();
      var today = s === todayISO();
      var dayEv = evs.filter(function (e) { return s >= e.fecha && s <= (e.fecha_fin || e.fecha); });
      html += '<div class="day' + (out ? " out" : "") + (today ? " today" : "") + '"><span class="n">' + d.getDate() + "</span>" +
        dayEv.map(function (e) { return '<button class="ev ' + e.tipo + (e.libres ? "" : " full") + '" data-res="' + esc(e.id) + '" title="' + esc(e.titulo + " · " + (e.libres ? e.libres + " plazas libres" : "completo")) + '">' + esc(e.titulo) + "</button>"; }).join("") + "</div>";
      d.setDate(d.getDate() + 1);
      if (i === 34 && d.getMonth() !== view.getMonth()) break;
    }
    grid.innerHTML = html;
    list.innerHTML = evs.length ? evs.map(evRow).join("") : '<div class="empty">No hay fechas publicadas ' + (tipo ? "de este tipo " : "") + "ahora mismo. Escríbenos por WhatsApp y te avisamos de las próximas salidas.</div>";
  }
  function renderUpcoming(root) {
    var slug = root.dataset.upcoming, evs = EVENTS.filter(function (e) { return e.slug === slug; }).slice(0, 4);
    var box = $("[data-uplist]", root);
    root.hidden = !evs.length;
    box.innerHTML = evs.map(function (e) { return '<div class="upc"><span class="d">' + parseDate(e.fecha).getDate() + " " + MESES[parseDate(e.fecha).getMonth()].slice(0, 3) + '</span><span class="t">' + esc(dateRange(e)) + (e.lugar ? " · " + esc(e.lugar) : "") + "</span>" + seatsHTML(e) + '<button class="btn ' + (e.libres ? "btn-primary" : "btn-ghost") + '" data-res="' + esc(e.id) + '"' + (e.libres ? "" : " disabled") + ">" + (e.libres ? "Reservar plaza" : "Completo") + "</button></div>"; }).join("");
  }
  function renderAll() {
    $$("[data-calendar]").forEach(renderCalendar); $$("[data-upcoming]").forEach(renderUpcoming);
  }
  function injectLD() {
    var ld = EVENTS.slice(0, 30).map(function (e) {
      return { "@context": "https://schema.org", "@type": e.tipo === "curso" ? "EducationEvent" : "SportsEvent", name: e.titulo, startDate: e.fecha + (e.hora ? "T" + e.hora : ""), endDate: e.fecha_fin || e.fecha, eventStatus: "https://schema.org/EventScheduled", eventAttendanceMode: "https://schema.org/OfflineEventAttendanceMode", location: { "@type": "Place", name: e.lugar || "Castilla y León", address: { "@type": "PostalAddress", addressLocality: e.lugar || "Castilla y León", addressCountry: "ES" } }, organizer: { "@type": "Organization", name: "Guías Ad Astra", url: location.origin }, offers: { "@type": "Offer", price: e.precio, priceCurrency: "EUR", availability: e.libres ? "https://schema.org/InStock" : "https://schema.org/SoldOut", url: location.href, validFrom: todayISO() }, maximumAttendeeCapacity: e.max, remainingAttendeeCapacity: e.libres };
    });
    if (!ld.length) return;
    var s = document.createElement("script"); s.type = "application/ld+json"; s.textContent = JSON.stringify(ld); document.head.appendChild(s);
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-res]"); if (b && !b.disabled) { e.preventDefault(); openReserve(b.dataset.res); }
  });
  $$("[data-calendar]").forEach(function (root) {
    $("[data-prev]", root).addEventListener("click", function () { view.setMonth(view.getMonth() - 1); renderCalendar(root); });
    $("[data-next]", root).addEventListener("click", function () { view.setMonth(view.getMonth() + 1); renderCalendar(root); });
    $$("[data-tipo-btn]", root).forEach(function (c) { c.addEventListener("click", function () { tipo = c.dataset.tipoBtn; $$("[data-tipo-btn]", root).forEach(function (x) { x.setAttribute("aria-pressed", x === c); }); renderCalendar(root); }); });
  });
  load().then(function () {
    if (EVENTS.length && $("[data-calendar]")) { var f = parseDate(EVENTS[0].fecha); if (f > new Date()) { view = new Date(f.getFullYear(), f.getMonth(), 1); } }
    renderAll(); if ($("[data-calendar]")) injectLD();
  });

  function waIcon() { return '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.4-2.3-1.4-.8-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.3 2.4 1 2.9.8 3.4.7.5-.1 1.7-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4C2.7 15.6 2.2 13.8 2.2 12 2.2 6.6 6.6 2.2 12 2.2S21.8 6.6 21.8 12 17.4 21.8 12 21.8zM12 0C5.4 0 0 5.4 0 12c0 2.1.6 4.2 1.6 6L0 24l6.2-1.6c1.7 1 3.7 1.5 5.8 1.5 6.6 0 12-5.4 12-12S18.6 0 12 0z"/></svg>'; }
})();
