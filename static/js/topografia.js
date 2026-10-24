/* Guías Ad Astra · Topografía de barrancos
   El usuario añade tramos (rápel, destrepe o tramo andando) y se dibuja el perfil del barranco
   con el estilo de los croquis a mano: R + metros en los rápeles, D + metros en los destrepes
   y A + metros en los tramos largos andando. Todo se calcula en el navegador. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var root = $("#topo");
  if (!root) return;

  var TIPOS = { r: "Rápel", d: "Destrepe", a: "Andando" };
  var INST = ["", "químicos", "parabolts", "spits", "cadena", "natural", "árbol"];
  var LADOS = ["", "izq", "centro", "dcha"];
  var KEY = "adastra-topo-v1";
  var EJEMPLO = {
    nombre: "Barranco de ejemplo", zona: "Sierra de Gredos (Ávila)", etiqueta: "metros", anclajes: true,
    tramos: [
      { t: "a", m: 40 }, { t: "r", m: 9, inst: "químicos", lado: "centro" }, { t: "a", m: 60 },
      { t: "r", m: 9, inst: "químicos", lado: "izq" }, { t: "a", m: 220, ver: true }, { t: "d", m: 3 },
      { t: "r", m: 11, inst: "químicos", lado: "dcha" }, { t: "a", m: 260, ver: true }, { t: "r", m: 5, inst: "natural", poza: true, remolino: true, peligro: true, aviso: "rebufo" }, { t: "a", m: 30 }
    ]
  };
  var S;

  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function num(v) { v = parseFloat(String(v).replace(",", ".")); return isFinite(v) && v > 0 ? Math.round(v * 10) / 10 : 0; }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function fmt(n) { return String(n).replace(".", ","); }

  /* ---------- guardar / cargar ---------- */
  function fromHash() {
    var h = location.hash.slice(1);
    if (h.indexOf("t=") !== 0) return null;
    try { return JSON.parse(decodeURIComponent(escape(atob(h.slice(2))))); } catch (e) { return null; }
  }
  function load() {
    var s = fromHash();
    if (!s) { try { s = JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { s = null; } }
    S = (s && s.tramos) ? s : clone(EJEMPLO);
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }

  /* ---------- editor ---------- */
  var list = $("#topo-list", root);

  function opt(arr, val, labels) { return arr.map(function (v, i) { return '<option value="' + esc(v) + '"' + (v === (val || "") ? " selected" : "") + ">" + esc(labels ? labels[i] : v) + "</option>"; }).join(""); }

  function rowHTML(t, i) {
    var extras = "";
    if (t.t === "r") {
      extras = '<label class="tp-f"><span>Instalación</span><select data-k="inst">' + opt(INST, t.inst, ["—", "Químicos", "Parabolts", "Spits", "Cadena", "Natural", "Árbol"]) + "</select></label>" +
        '<label class="tp-f"><span>Lado</span><select data-k="lado">' + opt(LADOS, t.lado, ["—", "Izquierda", "Centro", "Derecha"]) + "</select></label>";
    }
    if (t.t !== "a") {
      extras += '<label class="tp-chk"><input type="checkbox" data-k="poza"' + (t.poza ? " checked" : "") + "> Poza abajo</label>";
      if (t.poza) extras += '<label class="tp-chk"><input type="checkbox" data-k="remolino"' + (t.remolino ? " checked" : "") + '> Remolino en la poza <span class="tp-ico" aria-hidden="true">🌀</span></label>';
    }
    if (t.t === "a") extras += '<label class="tp-chk"><input type="checkbox" data-k="ver"' + (verDist(t) ? " checked" : "") + "> Poner la distancia (A" + fmt(t.m || 0) + ")</label>";
    extras += '<label class="tp-chk"><input type="checkbox" data-k="peligro"' + (t.peligro ? " checked" : "") + '> Peligro / incidencia <span class="tp-warn" aria-hidden="true">!</span></label>';
    if (t.peligro) extras += '<label class="tp-f tp-aviso"><span>¿Qué pasa? (opcional)</span><input type="text" maxlength="40" data-k="aviso" placeholder="Rebufo, sifón, tronco atascado…" value="' + esc(t.aviso || "") + '"></label>';
    var unit = t.t === "a" ? "Metros de cauce" : "Metros de altura";
    return '<li class="tp-row tp-' + t.t + '" data-i="' + i + '">' +
      '<span class="tp-n">' + (i + 1) + "</span>" +
      '<label class="tp-f"><span>Tipo</span><select data-k="t">' + opt(["r", "d", "a"], t.t, [TIPOS.r, TIPOS.d, TIPOS.a]) + "</select></label>" +
      '<label class="tp-f tp-m"><span>' + unit + '</span><input type="number" inputmode="decimal" min="0" step="0.5" data-k="m" value="' + (t.m || "") + '"></label>' +
      '<div class="tp-extra">' + extras + "</div>" +
      '<div class="tp-act"><button type="button" data-a="up" aria-label="Subir tramo" title="Subir">↑</button><button type="button" data-a="down" aria-label="Bajar tramo" title="Bajar">↓</button>' +
      '<button type="button" data-a="dup" aria-label="Duplicar tramo" title="Duplicar">⧉</button><button type="button" data-a="del" aria-label="Borrar tramo" title="Borrar">✕</button></div></li>';
  }
  function verDist(t) { return t.ver != null ? !!t.ver : (t.m || 0) >= 100; }

  function renderList() {
    list.innerHTML = S.tramos.length ? S.tramos.map(rowHTML).join("") : '<li class="tp-empty">Añade el primer tramo con los botones de abajo.</li>';
    $("#topo-nombre", root).value = S.nombre || "";
    $("#topo-zona", root).value = S.zona || "";
    $("#topo-etq", root).value = S.etiqueta || "metros";
    $("#topo-anc", root).checked = S.anclajes !== false;
  }

  list.addEventListener("input", function (e) {
    var el = e.target, li = el.closest(".tp-row"); if (!li) return;
    var t = S.tramos[+li.dataset.i], k = el.dataset.k;
    if (k === "m") t.m = num(el.value);
    else if (k === "ver" || k === "remolino") t[k] = el.checked;
    else if (k === "poza" || k === "peligro") { t[k] = el.checked; if (k === "poza" && !t.poza) delete t.remolino; renderList(); }
    else if (k === "t") { t.t = el.value; if (t.t === "a") { delete t.inst; delete t.lado; delete t.poza; delete t.remolino; } renderList(); }
    else t[k] = el.value;
    if (k === "m" && t.t === "a") { var c = $('[data-k="ver"]', li); if (c && t.ver == null) c.checked = verDist(t); if (c) c.parentNode.lastChild.textContent = " Poner la distancia (A" + fmt(t.m || 0) + ")"; }
    update();
  });
  list.addEventListener("click", function (e) {
    var b = e.target.closest("[data-a]"); if (!b) return;
    var i = +b.closest(".tp-row").dataset.i, a = b.dataset.a, T = S.tramos;
    if (a === "up" && i > 0) T.splice(i - 1, 0, T.splice(i, 1)[0]);
    if (a === "down" && i < T.length - 1) T.splice(i + 1, 0, T.splice(i, 1)[0]);
    if (a === "dup") T.splice(i + 1, 0, clone(T[i]));
    if (a === "del") T.splice(i, 1);
    renderList(); update();
  });
  root.addEventListener("click", function (e) {
    var b = e.target.closest("[data-add]"); if (!b) return;
    var t = b.dataset.add, def = { r: 10, d: 3, a: 50 }[t];
    S.tramos.push({ t: t, m: def });
    renderList(); update();
    var last = list.lastElementChild; if (last) { var inp = $('[data-k="m"]', last); if (inp) { inp.focus(); inp.select(); } }
  });
  ["nombre", "zona"].forEach(function (k) { $("#topo-" + k, root).addEventListener("input", function (e) { S[k] = e.target.value; update(); }); });
  $("#topo-etq", root).addEventListener("change", function (e) { S.etiqueta = e.target.value; update(); });
  $("#topo-anc", root).addEventListener("change", function (e) { S.anclajes = e.target.checked; update(); });
  $("#topo-nuevo", root).addEventListener("click", function () {
    if (S.tramos.length && !window.confirm("¿Empezar una topografía nueva? Se borrarán los tramos actuales.")) return;
    S = { nombre: "", zona: "", etiqueta: S.etiqueta || "metros", anclajes: S.anclajes !== false, tramos: [] }; renderList(); update();
  });
  $("#topo-ejemplo", root).addEventListener("click", function () { S = clone(EJEMPLO); renderList(); update(); });

  /* ---------- dibujo ---------- */
  var seed = 1;
  function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
  function jit(a) { return (rnd() - 0.5) * 2 * a; }

  function label(t, nR) {
    var m = fmt(t.m || 0);
    if (t.t === "r") return S.etiqueta === "numero" ? "R" + nR + " · " + m + " m" : "R" + m;
    if (t.t === "d") return "D" + m;
    return "A" + m;
  }

  function build() {
    var T = S.tramos.filter(function (t) { return t.m > 0; });
    var sumV = 0; T.forEach(function (t) { if (t.t !== "a") sumV += t.m; });
    var kv = Math.max(4, Math.min(14, sumV ? 560 / sumV : 10));     // píxeles por metro de altura
    seed = 7;
    var x = 40, y = 70, P = [[x, y]], ann = [], pools = [], nR = 0;
    function walk(len) {                                             // tramo andando: poca pendiente y ondulado
      var dx = Math.max(36, Math.min(260, 26 + Math.sqrt(len) * 9)), dy = Math.min(40, dx * 0.16), steps = Math.max(3, Math.round(dx / 22));
      for (var i = 1; i <= steps; i++) P.push([x + dx * i / steps + jit(2), y + dy * i / steps + (i < steps ? jit(3.2) : 0)]);
      x += dx; y += dy; return dx;
    }
    walk(30);
    T.forEach(function (t, idx) {
      if (t.t === "a") {
        var x0 = x, y0 = y, w = walk(t.m);
        if (verDist(t)) ann.push({ k: "a", x: x0 + w / 2, y: (y0 + y) / 2 + 26, txt: label(t) });
        if (t.peligro) ann.push({ k: "p", x: x0 + w / 2, y: (y0 + y) / 2 - 30, txt: t.aviso || "" });
        return;
      }
      var h = Math.max(t.t === "r" ? 30 : 16, t.m * kv);
      if (t.t === "r") {
        nR++;
        var dx = Math.max(6, h * 0.1), top = [x, y];
        P.push([x + 3, y - 3]);                                      // pequeño borde antes de la caída
        var n = Math.max(3, Math.round(h / 26));
        for (var i = 1; i <= n; i++) P.push([x + 3 + dx * i / n + jit(2.5), y + h * i / n]);
        x += 3 + dx; y += h;
        ann.push({ k: "r", x0: top[0] + 14, y0: top[1] - 16, x1: x + 18, y1: y - 4, txt: label(t, nR), sub: [t.inst, t.lado].filter(Boolean).join(", "), lado: t.lado });
      } else {
        var w2 = Math.max(16, h * 0.75), st = Math.max(2, Math.round(h / 14));
        for (var j = 1; j <= st; j++) {                               // escalones del destrepe
          P.push([x + w2 * (j - 0.55) / st, y + h * (j - 0.15) / st + jit(1.5)]);
          P.push([x + w2 * j / st + jit(1.2), y + h * j / st]);
        }
        ann.push({ k: "d", x: x + w2 / 2 - 14, y: y + h / 2 + 6, txt: label(t) });
        x += w2; y += h;
      }
      if (t.poza) {                                                  // poza al pie: el cauce baja y vuelve a subir
        var pw = 78, pd = 26, px = x;
        P.push([x + 6, y + pd * 0.6], [x + pw * 0.35, y + pd], [x + pw * 0.7, y + pd * 0.85], [x + pw, y - 2]);
        pools.push({ x: px, y: y, w: pw, d: pd, rem: !!t.remolino });
        if (t.peligro) ann.push({ k: "p", x: px + pw * 0.9, y: y - 26, txt: t.aviso || "" });
        x += pw; y -= 2;
      } else if (t.peligro) ann.push({ k: "p", x: x + 22, y: y - 34, txt: t.aviso || "" });
    });
    walk(40);
    return { P: P, ann: ann, pools: pools, nR: nR, w: x, h: y };
  }

  function smooth(P) {                                               // curva suave por los puntos (trazo a mano)
    var d = "M" + P[0][0].toFixed(1) + " " + P[0][1].toFixed(1);
    for (var i = 1; i < P.length - 1; i++) {
      var mx = (P[i][0] + P[i + 1][0]) / 2, my = (P[i][1] + P[i + 1][1]) / 2;
      d += " Q" + P[i][0].toFixed(1) + " " + P[i][1].toFixed(1) + " " + mx.toFixed(1) + " " + my.toFixed(1);
    }
    var L = P[P.length - 1]; return d + " L" + L[0].toFixed(1) + " " + L[1].toFixed(1);
  }

  function stats() {
    var r = S.tramos.filter(function (t) { return t.t === "r" && t.m > 0; }), d = S.tramos.filter(function (t) { return t.t === "d" && t.m > 0; });
    var maxR = r.reduce(function (a, t) { return Math.max(a, t.m); }, 0);
    var vert = S.tramos.reduce(function (a, t) { return a + (t.t !== "a" ? (t.m || 0) : 0); }, 0);
    var walk = S.tramos.reduce(function (a, t) { return a + (t.t === "a" ? (t.m || 0) : 0); }, 0);
    return { nR: r.length, nD: d.length, maxR: maxR, cuerda: Math.ceil(maxR * 2 + 2), vert: vert, walk: walk };
  }

  function spiral(cx, cy, r) {                                         // remolino: espiral azul dentro de la poza
    var d = "", turns = 2.6, n = 46;
    for (var i = 0; i <= n; i++) {
      var a = i / n * turns * 2 * Math.PI, rr = r * i / n;
      d += (i ? " L" : "M") + (cx + rr * Math.cos(a)).toFixed(1) + " " + (cy + rr * Math.sin(a) * 0.62).toFixed(1);
    }
    return '<path d="' + d + '" fill="none" stroke="#1f4fa3" stroke-width="2.4" stroke-linecap="round"/>';
  }
  function warn(cx, cy) {                                              // incidencia: señal triangular con exclamación
    var s = 13;
    return '<path d="M' + cx.toFixed(1) + " " + (cy - s).toFixed(1) + " L" + (cx + s).toFixed(1) + " " + (cy + s * 0.75).toFixed(1) + " L" + (cx - s).toFixed(1) + " " + (cy + s * 0.75).toFixed(1) + ' Z" fill="#ffd21f" stroke="#c62828" stroke-width="2.6" stroke-linejoin="round"/>' +
      '<text x="' + cx.toFixed(1) + '" y="' + (cy + s * 0.55).toFixed(1) + '" font-size="15" font-weight="900" fill="#1b1a19" text-anchor="middle">!</text>';
  }

  function svg(forExport) {
    var G = build(), st = stats();
    var W = Math.max(640, G.w + 260), H = Math.max(320, G.h + 80);
    var blue = "#24408e", ink = "#1b1a19", font = "Arial,Helvetica,sans-serif";
    var o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + Math.round(W) + " " + Math.round(H) + '" width="' + Math.round(W) + '" height="' + Math.round(H) + '" font-family="' + font + '">',
      '<rect width="100%" height="100%" fill="#fff"/>'];
    var title = S.nombre || "Topografía del barranco";
    o.push('<text x="24" y="34" font-size="22" font-weight="700" fill="' + ink + '">' + esc(title) + "</text>");
    if (S.zona) o.push('<text x="24" y="54" font-size="13" fill="#555">' + esc(S.zona) + "</text>");
    G.pools.forEach(function (p) {
      o.push('<path d="M' + (p.x + 2) + " " + (p.y + 1) + " Q" + (p.x + p.w * 0.35) + " " + (p.y + p.d + 2) + " " + (p.x + p.w * 0.7) + " " + (p.y + p.d * 0.85) + " L" + (p.x + p.w - 2) + " " + (p.y + 1) + ' Z" fill="#9fd8ea" stroke="none"/>');
      if (p.rem) o.push(spiral(p.x + p.w * 0.42, p.y + p.d * 0.45, 12));
    });
    o.push('<path d="' + smooth(G.P) + '" fill="none" stroke="' + ink + '" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>');
    G.ann.forEach(function (a) {
      if (a.k === "r") {
        if (S.anclajes !== false) {
          var ang = Math.atan2(a.y1 - a.y0, a.x1 - a.x0), ah = 11;
          o.push('<circle cx="' + a.x0.toFixed(1) + '" cy="' + a.y0.toFixed(1) + '" r="5" fill="#fff" stroke="' + blue + '" stroke-width="2.4"/>');
          o.push('<line x1="' + a.x0.toFixed(1) + '" y1="' + (a.y0 + 5).toFixed(1) + '" x2="' + a.x1.toFixed(1) + '" y2="' + a.y1.toFixed(1) + '" stroke="' + blue + '" stroke-width="2.2"/>');
          o.push('<path d="M' + a.x1.toFixed(1) + " " + a.y1.toFixed(1) + " L" + (a.x1 - ah * Math.cos(ang - 0.4)).toFixed(1) + " " + (a.y1 - ah * Math.sin(ang - 0.4)).toFixed(1) + " M" + a.x1.toFixed(1) + " " + a.y1.toFixed(1) + " L" + (a.x1 - ah * Math.cos(ang + 0.4)).toFixed(1) + " " + (a.y1 - ah * Math.sin(ang + 0.4)).toFixed(1) + '" stroke="' + blue + '" stroke-width="2.2" fill="none" stroke-linecap="round"/>');
        }
        var lx = Math.max(a.x0, a.x1) + 14, ly = a.y0 + Math.min(40, (a.y1 - a.y0) * 0.35) + 10;
        o.push('<text x="' + lx.toFixed(1) + '" y="' + ly.toFixed(1) + '" font-size="21" font-weight="700" fill="' + ink + '">' + esc(a.txt) +
          (a.sub ? '<tspan font-size="14" font-weight="600" fill="#333"> - ' + esc(a.sub) + "</tspan>" : "") + "</text>");
      } else if (a.k === "p") {
        o.push(warn(a.x, a.y));
        if (a.txt) o.push('<text x="' + (a.x + 16).toFixed(1) + '" y="' + (a.y + 5).toFixed(1) + '" font-size="13" font-weight="700" fill="#c62828">' + esc(a.txt) + "</text>");
      } else if (a.k === "d") {
        o.push('<text x="' + a.x.toFixed(1) + '" y="' + a.y.toFixed(1) + '" font-size="18" font-weight="700" fill="' + ink + '" text-anchor="end">' + esc(a.txt) + "</text>");
      } else {
        o.push('<text x="' + a.x.toFixed(1) + '" y="' + a.y.toFixed(1) + '" font-size="15" font-weight="700" fill="#555" text-anchor="middle">' + esc(a.txt) + "</text>");
      }
    });
    var info = [st.nR + (st.nR === 1 ? " rápel" : " rápeles")];
    if (st.maxR) info.push("más largo " + fmt(st.maxR) + " m", "cuerda mínima " + st.cuerda + " m");
    if (st.nD) info.push(st.nD + (st.nD === 1 ? " destrepe" : " destrepes"));
    if (st.vert) info.push("desnivel vertical " + fmt(Math.round(st.vert)) + " m");
    if (st.walk) info.push(fmt(Math.round(st.walk)) + " m de cauce");
    var nP = S.tramos.filter(function (t) { return t.peligro && t.m > 0; }).length, nW = S.tramos.filter(function (t) { return t.remolino && t.poza && t.m > 0; }).length;
    if (nW) info.push(nW + (nW === 1 ? " remolino" : " remolinos"));
    if (nP) info.push(nP + (nP === 1 ? " punto de peligro" : " puntos de peligro"));
    o.push('<text x="24" y="' + (H - 22) + '" font-size="12.5" fill="#444">' + esc(info.join(" · ")) + "</text>");
    o.push('<text x="' + (W - 20) + '" y="' + (H - 22) + '" font-size="12" fill="#888" text-anchor="end">Hecho con la topografía de barrancos de guiasadastra.com</text>');
    o.push("</svg>");
    return o.join("");
  }

  var view = $("#topo-svg", root), out = $("#topo-stats", root);
  var raf = 0;
  function update() {
    save();
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(function () {
      view.innerHTML = S.tramos.some(function (t) { return t.m > 0; }) ? svg() : '<p class="muted" style="padding:40px;text-align:center">Añade tramos para ver la topografía.</p>';
      var st = stats();
      out.innerHTML = [["Rápeles", st.nR], ["Rápel más largo", st.maxR ? fmt(st.maxR) + " m" : "—"], ["Cuerda mínima", st.maxR ? st.cuerda + " m" : "—"],
        ["Destrepes", st.nD], ["Desnivel vertical", fmt(Math.round(st.vert)) + " m"], ["Cauce andando", fmt(Math.round(st.walk)) + " m"]]
        .map(function (s) { return "<div><dt>" + s[0] + "</dt><dd>" + s[1] + "</dd></div>"; }).join("");
    });
  }

  /* ---------- descargas y compartir ---------- */
  function fileName(ext) { return (S.nombre || "topografia-barranco").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") + "." + ext; }
  function dl(blob, name) { var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 800); }
  $("#topo-svgdl", root).addEventListener("click", function () { dl(new Blob([svg()], { type: "image/svg+xml" }), fileName("svg")); });
  $("#topo-png", root).addEventListener("click", function () {
    var s = svg(), img = new Image(), m = s.match(/viewBox="0 0 (\d+) (\d+)"/), w = +m[1], h = +m[2], k = 2;
    img.onload = function () {
      var c = document.createElement("canvas"); c.width = w * k; c.height = h * k;
      var g = c.getContext("2d"); g.fillStyle = "#fff"; g.fillRect(0, 0, c.width, c.height); g.drawImage(img, 0, 0, c.width, c.height);
      c.toBlob(function (b) { dl(b, fileName("png")); }, "image/png");
    };
    img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(s);
  });
  $("#topo-link", root).addEventListener("click", function () {
    var u = location.origin + location.pathname + "#t=" + btoa(unescape(encodeURIComponent(JSON.stringify(S))));
    var msg = $("#topo-msg", root);
    var ok = function () { msg.textContent = "Enlace copiado. Quien lo abra verá esta misma topografía."; };
    if (navigator.clipboard) navigator.clipboard.writeText(u).then(ok, function () { window.prompt("Copia este enlace:", u); });
    else window.prompt("Copia este enlace:", u);
  });

  load(); renderList(); update();
})();
