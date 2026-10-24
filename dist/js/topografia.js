/* Guías Ad Astra · Topografía de barrancos
   El usuario añade tramos (rápel, destrepe, pasamanos o tramo andando) y se dibuja el perfil del barranco
   con la simbología habitual de las topografías: R (rápel), d/D (destrepe), Pc (pasamanos), lados I/C/D,
   anclajes X (parabolt) con anilla, maillón o eslabón, uniones por cadena o cordino, rápel destrepable,
   pozas, remolinos, peligros, puntos sin retorno, escapes y parking. Todo se calcula en el navegador. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var root = $("#topo");
  if (!root) return;

  var TIPOS = { r: "Rápel", d: "Destrepe", p: "Pasamanos", a: "Andando" };
  // anclajes: código, nombre en el desplegable, texto corto, símbolo (letra pequeña bajo la X)
  var ANC = [
    ["", "—", "", ""], ["x", "Parabolt (X)", "parabolt", ""], ["xo", "Parabolt + anilla (Xo)", "parabolt + anilla", "o"],
    ["xm", "Parabolt + maillón (Xm)", "parabolt + maillón", "m"], ["xu", "Parabolt + eslabón en U (XU)", "parabolt + eslabón", "U"],
    ["quimico", "Químicos", "químicos", "q"], ["cadena", "Reunión de cadena", "cadena", "c"], ["natural", "Anclaje natural", "natural", ""], ["arbol", "Árbol", "árbol", ""]
  ];
  var ANC_OLD = { "químicos": "quimico", parabolts: "x", spits: "x", "árbol": "arbol" };
  var UNION = [["1", "1 anclaje"], ["2", "2 anclajes sin unir"], ["2c", "2 unidos por cadena"], ["2k", "2 unidos por cordino"]];
  var LADOS = [["", "—"], ["I", "Izquierda (I)"], ["C", "Centro (C)"], ["D", "Derecha (D)"]];
  var LADO_TXT = { I: "izq", C: "centro", D: "dcha" };
  var ESC = [["", "—"], ["I", "Escape por la izquierda"], ["D", "Escape por la derecha"], ["N", "Sin escapes"]];
  var KEY = "adastra-topo-v1";
  var EJEMPLO = {
    nombre: "Barranco de ejemplo", zona: "Sierra de Gredos (Ávila)", etiqueta: "metros", anclajes: true, leyenda: true, parkIni: true, parkFin: false,
    tramos: [
      { t: "a", m: 40 }, { t: "r", m: 9, inst: "quimico", union: "2c", lado: "C", destrepable: true }, { t: "a", m: 60, esc: "N" },
      { t: "r", m: 9, inst: "xm", union: "2c", lado: "I" }, { t: "a", m: 220, ver: true }, { t: "d", m: 3 }, { t: "p", m: 6, lado: "D" },
      { t: "r", m: 11, inst: "xo", union: "2k", lado: "D", sinretorno: true }, { t: "a", m: 360, ver: true, esc: "I" },
      { t: "r", m: 5, inst: "arbol", union: "1", poza: true, remolino: true, peligro: true, aviso: "rebufo" }, { t: "a", m: 30 }
    ]
  };
  var S;

  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function num(v) { v = parseFloat(String(v).replace(",", ".")); return isFinite(v) && v > 0 ? Math.round(v * 10) / 10 : 0; }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function fmt(n) { return String(n).replace(".", ","); }
  function anc(code) { for (var i = 0; i < ANC.length; i++) if (ANC[i][0] === code) return ANC[i]; return ANC[0]; }

  /* ---------- guardar / cargar ---------- */
  function fromHash() {
    var h = location.hash.slice(1);
    if (h.indexOf("t=") !== 0) return null;
    try { return JSON.parse(decodeURIComponent(escape(atob(h.slice(2))))); } catch (e) { return null; }
  }
  function migrate(s) {                                              // datos guardados con la versión anterior
    (s.tramos || []).forEach(function (t) {
      if (t.inst && ANC_OLD[t.inst]) t.inst = ANC_OLD[t.inst];
      if (t.lado && t.lado.length > 1) t.lado = { izq: "I", centro: "C", dcha: "D" }[t.lado] || "";
    });
    if (s.leyenda == null) s.leyenda = true;
    return s;
  }
  function load() {
    var s = fromHash();
    if (!s) { try { s = JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { s = null; } }
    S = (s && s.tramos) ? migrate(s) : clone(EJEMPLO);
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }

  /* ---------- editor ---------- */
  var list = $("#topo-list", root);
  function opt(pairs, val) { return pairs.map(function (p) { return '<option value="' + esc(p[0]) + '"' + (p[0] === (val || "") ? " selected" : "") + ">" + esc(p[1]) + "</option>"; }).join(""); }
  function chk(k, on, txt) { return '<label class="tp-chk"><input type="checkbox" data-k="' + k + '"' + (on ? " checked" : "") + "> " + txt + "</label>"; }
  function sel(k, title, pairs, val) { return '<label class="tp-f"><span>' + title + '</span><select data-k="' + k + '">' + opt(pairs, val) + "</select></label>"; }
  function verDist(t) { return t.ver != null ? !!t.ver : (t.m || 0) >= 100; }

  function rowHTML(t, i) {
    var x = "";
    if (t.t === "r" || t.t === "p") {
      x += sel("inst", "Anclaje", ANC.map(function (a) { return [a[0], a[1]]; }), t.inst);
      x += sel("union", "Nº de anclajes", UNION, t.union || "2c");
    }
    if (t.t !== "a") x += sel("lado", "Lado (aguas abajo)", LADOS, t.lado);
    if (t.t === "r") x += chk("destrepable", t.destrepable, 'Destrepable <span class="tp-sym tp-dest" aria-hidden="true"></span>');
    if (t.t === "r" || t.t === "d") {
      x += chk("poza", t.poza, "Poza abajo");
      if (t.poza) x += chk("remolino", t.remolino, 'Remolino en la poza <span class="tp-ico" aria-hidden="true">🌀</span>');
    }
    if (t.t === "a") {
      x += chk("ver", verDist(t), "Poner la distancia (A" + fmt(t.m || 0) + ")");
      x += sel("esc", "Escapes", ESC, t.esc);
    }
    x += chk("peligro", t.peligro, 'Peligro / incidencia <span class="tp-warn" aria-hidden="true">!</span>');
    x += chk("sinretorno", t.sinretorno, 'Punto sin retorno <span class="tp-sym tp-nr" aria-hidden="true"></span>');
    if (t.peligro) x += '<label class="tp-f tp-aviso"><span>¿Qué pasa? (opcional)</span><input type="text" maxlength="40" data-k="aviso" placeholder="Rebufo, sifón, tronco atascado…" value="' + esc(t.aviso || "") + '"></label>';
    var unit = t.t === "a" ? "Metros de cauce" : t.t === "p" ? "Metros de pasamanos" : "Metros de altura";
    return '<li class="tp-row tp-' + t.t + '" data-i="' + i + '">' +
      '<span class="tp-n">' + (i + 1) + "</span>" +
      '<label class="tp-f"><span>Tipo</span><select data-k="t">' + opt([["r", TIPOS.r], ["d", TIPOS.d], ["p", TIPOS.p], ["a", TIPOS.a]], t.t) + "</select></label>" +
      '<label class="tp-f tp-m"><span>' + unit + '</span><input type="number" inputmode="decimal" min="0" step="0.5" data-k="m" value="' + (t.m || "") + '"></label>' +
      '<div class="tp-extra">' + x + "</div>" +
      '<div class="tp-act"><button type="button" data-a="up" aria-label="Subir tramo" title="Subir">↑</button><button type="button" data-a="down" aria-label="Bajar tramo" title="Bajar">↓</button>' +
      '<button type="button" data-a="dup" aria-label="Duplicar tramo" title="Duplicar">⧉</button><button type="button" data-a="del" aria-label="Borrar tramo" title="Borrar">✕</button></div></li>';
  }

  function renderList() {
    list.innerHTML = S.tramos.length ? S.tramos.map(rowHTML).join("") : '<li class="tp-empty">Añade el primer tramo con los botones de abajo.</li>';
    $("#topo-nombre", root).value = S.nombre || "";
    $("#topo-zona", root).value = S.zona || "";
    $("#topo-etq", root).value = S.etiqueta || "metros";
    $("#topo-anc", root).checked = S.anclajes !== false;
    $("#topo-ley", root).checked = S.leyenda !== false;
    $("#topo-pi", root).checked = !!S.parkIni;
    $("#topo-pf", root).checked = !!S.parkFin;
  }

  var REDRAW = { t: 1, poza: 1, peligro: 1 };
  list.addEventListener("input", function (e) {
    var el = e.target, li = el.closest(".tp-row"); if (!li) return;
    var t = S.tramos[+li.dataset.i], k = el.dataset.k;
    if (k === "m") t.m = num(el.value);
    else if (el.type === "checkbox") { t[k] = el.checked; if (k === "poza" && !t.poza) delete t.remolino; }
    else if (k === "t") {
      t.t = el.value;
      if (t.t === "a") ["inst", "union", "lado", "poza", "remolino", "destrepable"].forEach(function (p) { delete t[p]; });
      if (t.t !== "a") { delete t.ver; delete t.esc; }
      if (t.t !== "r") delete t.destrepable;
    } else t[k] = el.value;
    if (REDRAW[k]) renderList();
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
    var t = b.dataset.add, def = { r: 10, d: 3, p: 6, a: 50 }[t], nt = { t: t, m: def };
    if (t === "r" || t === "p") nt.union = "2c";
    S.tramos.push(nt);
    renderList(); update();
    var last = list.lastElementChild; if (last) { var inp = $('[data-k="m"]', last); if (inp) { inp.focus(); inp.select(); } }
  });
  ["nombre", "zona"].forEach(function (k) { $("#topo-" + k, root).addEventListener("input", function (e) { S[k] = e.target.value; update(); }); });
  $("#topo-etq", root).addEventListener("change", function (e) { S.etiqueta = e.target.value; update(); });
  [["anc", "anclajes"], ["ley", "leyenda"], ["pi", "parkIni"], ["pf", "parkFin"]].forEach(function (p) {
    $("#topo-" + p[0], root).addEventListener("change", function (e) { S[p[1]] = e.target.checked; update(); });
  });
  $("#topo-nuevo", root).addEventListener("click", function () {
    if (S.tramos.length && !window.confirm("¿Empezar una topografía nueva? Se borrarán los tramos actuales.")) return;
    S = { nombre: "", zona: "", etiqueta: S.etiqueta || "metros", anclajes: S.anclajes !== false, leyenda: S.leyenda !== false, tramos: [] }; renderList(); update();
  });
  $("#topo-ejemplo", root).addEventListener("click", function () { S = clone(EJEMPLO); renderList(); update(); });

  /* ---------- dibujo ---------- */
  var seed = 1;
  function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
  function jit(a) { return (rnd() - 0.5) * 2 * a; }

  function label(t, n) {                                            // n = número de orden dentro de su tipo
    var m = fmt(t.m || 0), L = t.lado || "";
    var P = { r: "R", d: S.etiqueta === "federativo" ? "d" : "D", p: "Pc", a: "A" }[t.t];
    if (t.t === "a") return "A" + m;
    if (S.etiqueta === "federativo") return P + n + "-" + m + "m" + (L ? "-" + L : "");
    if (S.etiqueta === "numero") return P + n + " · " + m + " m";
    return P + m;
  }
  function subtext(t) {                                              // texto pequeño junto a la etiqueta (formato «R13 - químicos, centro»)
    if (S.etiqueta === "federativo") return "";
    var a = anc(t.inst)[2], l = LADO_TXT[t.lado] || "";
    return [a, l].filter(Boolean).join(", ");
  }

  function build() {
    var T = S.tramos.filter(function (t) { return t.m > 0; });
    var sumV = 0; T.forEach(function (t) { if (t.t === "r" || t.t === "d") sumV += t.m; });
    var kv = Math.max(4, Math.min(14, sumV ? 560 / sumV : 10));     // píxeles por metro de altura
    seed = 7;
    var x = 40, y = 92, P = [[x, y]], ann = [], pools = [], cnt = { r: 0, d: 0, p: 0 };
    function walk(len) {                                             // tramo andando: poca pendiente y ondulado
      var dx = Math.max(36, Math.min(260, 26 + Math.sqrt(len) * 9)), dy = Math.min(40, dx * 0.16), steps = Math.max(3, Math.round(dx / 22));
      for (var i = 1; i <= steps; i++) P.push([x + dx * i / steps + jit(2), y + dy * i / steps + (i < steps ? jit(3.2) : 0)]);
      x += dx; y += dy; return dx;
    }
    walk(30);
    if (S.parkIni) ann.push({ k: "park", x: 34, y: 66 });
    T.forEach(function (t) {
      var x0 = x, y0 = y;
      if (t.sinretorno) ann.push({ k: "nr", x: x0 - 8, y: y0 + 26 });
      if (t.t === "a") {
        var w = walk(t.m);
        if (verDist(t)) ann.push({ k: "a", x: x0 + w / 2, y: (y0 + y) / 2 + 28, txt: label(t) });
        if (t.m >= 300) ann.push({ k: "cut", x: x0 + w / 2, y: (y0 + y) / 2 });
        if (t.esc) ann.push({ k: "esc", x: x0 + w / 2, y: (y0 + y) / 2 + (verDist(t) ? 46 : 28), v: t.esc });
        if (t.peligro) ann.push({ k: "p", x: x0 + w / 2, y: (y0 + y) / 2 - 30, txt: t.aviso || "" });
        return;
      }
      cnt[t.t]++;
      if (t.t === "p") {                                             // pasamanos: tramo casi llano con cuerda fija por encima
        var wp = Math.max(60, Math.min(220, 40 + t.m * 9));
        var stp = Math.max(3, Math.round(wp / 22));
        for (var q = 1; q <= stp; q++) P.push([x + wp * q / stp + jit(2), y + 6 * q / stp + jit(2.5)]);
        ann.push({ k: "pc", x0: x + 6, x1: x + wp - 6, y: y - 22, txt: label(t, cnt.p), sub: subtext(t), inst: t.inst, union: t.union });
        x += wp; y += 6;
        if (t.peligro) ann.push({ k: "p", x: x0 + wp / 2, y: y0 - 56, txt: t.aviso || "" });
        return;
      }
      var h = Math.max(t.t === "r" ? 30 : 16, t.m * kv);
      if (t.t === "r") {
        var dx = Math.max(6, h * 0.1), top = [x, y];
        P.push([x + 3, y - 3]);                                      // pequeño borde antes de la caída
        var n = Math.max(3, Math.round(h / 26));
        for (var i = 1; i <= n; i++) P.push([x + 3 + dx * i / n + jit(2.5), y + h * i / n]);
        x += 3 + dx; y += h;
        ann.push({ k: "r", x0: top[0] + 14, y0: top[1] - 16, x1: x + 18, y1: y - 4, txt: label(t, cnt.r), sub: subtext(t), inst: t.inst, union: t.union || "2c", dest: t.destrepable });
      } else {
        var w2 = Math.max(16, h * 0.75), st = Math.max(2, Math.round(h / 14));
        for (var j = 1; j <= st; j++) {                               // escalones del destrepe
          P.push([x + w2 * (j - 0.55) / st, y + h * (j - 0.15) / st + jit(1.5)]);
          P.push([x + w2 * j / st + jit(1.2), y + h * j / st]);
        }
        ann.push({ k: "d", x: x + w2 / 2 - 14, y: y + h / 2 + 6, txt: label(t, cnt.d) });
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
    if (S.parkFin) ann.push({ k: "park", x: x + 22, y: y - 4 });
    return { P: P, ann: ann, pools: pools, w: x, h: y, cnt: cnt };
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
    var T = S.tramos.filter(function (t) { return t.m > 0; });
    var r = T.filter(function (t) { return t.t === "r"; }), maxR = r.reduce(function (a, t) { return Math.max(a, t.m); }, 0);
    return {
      nR: r.length, nD: T.filter(function (t) { return t.t === "d"; }).length, nP: T.filter(function (t) { return t.t === "p"; }).length,
      maxR: maxR, cuerda: Math.ceil(maxR * 2 + 2),
      vert: T.reduce(function (a, t) { return a + (t.t === "r" || t.t === "d" ? t.m : 0); }, 0),
      walk: T.reduce(function (a, t) { return a + (t.t === "a" ? t.m : 0); }, 0)
    };
  }

  /* ---------- símbolos ---------- */
  var BLUE = "#24408e", INK = "#1b1a19", RED = "#c62828";
  function f1(n) { return n.toFixed(1); }
  function spiral(cx, cy, r) {
    var d = "", turns = 2.6, n = 46;
    for (var i = 0; i <= n; i++) { var a = i / n * turns * 2 * Math.PI, rr = r * i / n; d += (i ? " L" : "M") + f1(cx + rr * Math.cos(a)) + " " + f1(cy + rr * Math.sin(a) * 0.62); }
    return '<path d="' + d + '" fill="none" stroke="#1f4fa3" stroke-width="2.4" stroke-linecap="round"/>';
  }
  function warn(cx, cy) {
    var s = 13;
    return '<path d="M' + f1(cx) + " " + f1(cy - s) + " L" + f1(cx + s) + " " + f1(cy + s * 0.75) + " L" + f1(cx - s) + " " + f1(cy + s * 0.75) + ' Z" fill="#ffd21f" stroke="' + RED + '" stroke-width="2.6" stroke-linejoin="round"/>' +
      '<text x="' + f1(cx) + '" y="' + f1(cy + s * 0.55) + '" font-size="15" font-weight="900" fill="' + INK + '" text-anchor="middle">!</text>';
  }
  function noReturn(cx, cy) {                                          // punto sin retorno: señal de prohibido
    return '<circle cx="' + f1(cx) + '" cy="' + f1(cy) + '" r="11" fill="#fff" stroke="' + RED + '" stroke-width="3"/><rect x="' + f1(cx - 7) + '" y="' + f1(cy - 2.2) + '" width="14" height="4.4" fill="' + RED + '"/>';
  }
  function destrepable(cx, cy) {                                       // rápel destrepable: insignia morada
    return '<circle cx="' + f1(cx) + '" cy="' + f1(cy) + '" r="10" fill="#7b3fa0"/><path d="M' + f1(cx - 5) + " " + f1(cy - 3) + " l3 0 l0 3 l3 0 l0 3 l3 0" + '" stroke="#fff" stroke-width="2" fill="none"/>';
  }
  function parking(cx, cy) {
    return '<circle cx="' + f1(cx) + '" cy="' + f1(cy) + '" r="12" fill="#1f5fae"/><text x="' + f1(cx) + '" y="' + f1(cy + 5.5) + '" font-size="16" font-weight="900" fill="#fff" text-anchor="middle">P</text>';
  }
  function tree(cx, cy) {
    return '<rect x="' + f1(cx - 1.5) + '" y="' + f1(cy - 4) + '" width="3" height="8" fill="#6b4a2b"/><circle cx="' + f1(cx) + '" cy="' + f1(cy - 9) + '" r="7" fill="#3f8f3a"/>';
  }
  function anchors(x, y, code, union) {                                // X con su letra pequeña y la unión entre anclajes
    if (!code) return "";
    if (code === "natural" || code === "arbol") return code === "arbol" ? tree(x + 6, y) : '<circle cx="' + f1(x + 5) + '" cy="' + f1(y - 4) + '" r="6" fill="none" stroke="' + INK + '" stroke-width="2"/>';
    var two = union && union !== "1", out = "", sub = anc(code)[3];
    var xs = two ? [x, x + 18] : [x];
    xs.forEach(function (ax) {
      out += '<text x="' + f1(ax) + '" y="' + f1(y) + '" font-size="15" font-weight="700" fill="' + INK + '">X</text>';
      if (sub) out += '<text x="' + f1(ax + 10) + '" y="' + f1(y + 5) + '" font-size="9.5" font-weight="700" fill="' + INK + '">' + sub + "</text>";
    });
    if (union === "2c") out += '<path d="M' + f1(x + 4) + " " + f1(y + 4) + " l3 7 l9 0 l3 -7" + '" fill="none" stroke="' + INK + '" stroke-width="1.6"/>';
    if (union === "2k") out += '<path d="M' + f1(x + 4) + " " + f1(y + 4) + " Q" + f1(x + 13) + " " + f1(y + 13) + " " + f1(x + 22) + " " + f1(y + 4) + '" fill="none" stroke="' + INK + '" stroke-width="1.6"/>';
    return out;
  }

  function svg() {
    var G = build(), st = stats();
    var used = {};
    var W = Math.max(680, G.w + 280), drawH = G.h + 70;
    var o = [];
    var title = S.nombre || "Topografía del barranco";
    o.push('<text x="24" y="34" font-size="22" font-weight="700" fill="' + INK + '">' + esc(title) + "</text>");
    if (S.zona) o.push('<text x="24" y="54" font-size="13" fill="#555">' + esc(S.zona) + "</text>");
    G.pools.forEach(function (p) {
      used.poza = 1;
      o.push('<path d="M' + (p.x + 2) + " " + (p.y + 1) + " Q" + (p.x + p.w * 0.35) + " " + (p.y + p.d + 2) + " " + (p.x + p.w * 0.7) + " " + (p.y + p.d * 0.85) + " L" + (p.x + p.w - 2) + " " + (p.y + 1) + ' Z" fill="#9fd8ea" stroke="none"/>');
      if (p.rem) { used.rem = 1; o.push(spiral(p.x + p.w * 0.42, p.y + p.d * 0.45, 12)); }
    });
    o.push('<path d="' + smooth(G.P) + '" fill="none" stroke="' + INK + '" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>');
    G.ann.forEach(function (a) {
      if (a.k === "r") {
        used.r = 1;
        if (S.anclajes !== false) {
          var ang = Math.atan2(a.y1 - a.y0, a.x1 - a.x0), ah = 11;
          o.push('<circle cx="' + f1(a.x0) + '" cy="' + f1(a.y0) + '" r="5" fill="#fff" stroke="' + BLUE + '" stroke-width="2.4"/>');
          o.push('<line x1="' + f1(a.x0) + '" y1="' + f1(a.y0 + 5) + '" x2="' + f1(a.x1) + '" y2="' + f1(a.y1) + '" stroke="' + BLUE + '" stroke-width="2.2"/>');
          o.push('<path d="M' + f1(a.x1) + " " + f1(a.y1) + " L" + f1(a.x1 - ah * Math.cos(ang - 0.4)) + " " + f1(a.y1 - ah * Math.sin(ang - 0.4)) + " M" + f1(a.x1) + " " + f1(a.y1) + " L" + f1(a.x1 - ah * Math.cos(ang + 0.4)) + " " + f1(a.y1 - ah * Math.sin(ang + 0.4)) + '" stroke="' + BLUE + '" stroke-width="2.2" fill="none" stroke-linecap="round"/>');
        }
        var lx = Math.max(a.x0, a.x1) + 14, ly = a.y0 + Math.min(40, (a.y1 - a.y0) * 0.35) + 10;
        o.push('<text x="' + f1(lx) + '" y="' + f1(ly) + '" font-size="21" font-weight="700" fill="' + INK + '">' + esc(a.txt) +
          (a.sub ? '<tspan font-size="14" font-weight="600" fill="#333"> - ' + esc(a.sub) + "</tspan>" : "") + "</text>");
        if (a.inst) { used["a_" + a.inst] = 1; if (a.union === "2c" || a.union === "2k") used["u_" + a.union] = 1; o.push(anchors(lx + 2, ly + 22, a.inst, a.union)); }
        if (a.dest) { used.dest = 1; o.push(destrepable(a.x0, a.y0 - 22)); }
      } else if (a.k === "pc") {
        used.pc = 1;
        o.push('<line x1="' + f1(a.x0) + '" y1="' + f1(a.y) + '" x2="' + f1(a.x1) + '" y2="' + f1(a.y + 4) + '" stroke="' + BLUE + '" stroke-width="2.4" stroke-dasharray="7 4"/>');
        o.push('<circle cx="' + f1(a.x0) + '" cy="' + f1(a.y) + '" r="4" fill="' + BLUE + '"/><circle cx="' + f1(a.x1) + '" cy="' + f1(a.y + 4) + '" r="4" fill="' + BLUE + '"/>');
        o.push('<text x="' + f1(a.x0) + '" y="' + f1(a.y - 14) + '" font-size="19" font-weight="700" fill="' + INK + '">' + esc(a.txt) + (a.sub ? '<tspan font-size="13" font-weight="600" fill="#333"> - ' + esc(a.sub) + "</tspan>" : "") + "</text>");
        if (a.inst) { used["a_" + a.inst] = 1; if (a.union === "2c" || a.union === "2k") used["u_" + a.union] = 1; o.push(anchors(a.x1 + 12, a.y + 2, a.inst, a.union)); }
      } else if (a.k === "p") {
        used.peligro = 1; o.push(warn(a.x, a.y));
        if (a.txt) o.push('<text x="' + f1(a.x + 16) + '" y="' + f1(a.y + 5) + '" font-size="13" font-weight="700" fill="' + RED + '">' + esc(a.txt) + "</text>");
      } else if (a.k === "nr") { used.nr = 1; o.push(noReturn(a.x, a.y)); }
      else if (a.k === "park") { used.park = 1; o.push(parking(a.x, a.y)); }
      else if (a.k === "cut") {
        used.cut = 1;
        o.push('<path d="M' + f1(a.x - 9) + " " + f1(a.y + 10) + " l8 -20 M" + f1(a.x + 1) + " " + f1(a.y + 10) + ' l8 -20" stroke="#fff" stroke-width="7"/><path d="M' + f1(a.x - 9) + " " + f1(a.y + 10) + " l8 -20 M" + f1(a.x + 1) + " " + f1(a.y + 10) + ' l8 -20" stroke="' + INK + '" stroke-width="2"/>');
      } else if (a.k === "esc") {
        var tx = a.v === "N" ? "(No hay escapes)" : (a.v === "I" ? "Escape I ↖" : "Escape D ↗");
        o.push('<text x="' + f1(a.x) + '" y="' + f1(a.y) + '" font-size="12.5" font-weight="700" fill="#6b4a2b" text-anchor="middle">' + tx + "</text>");
      } else if (a.k === "d") {
        used.d = 1; o.push('<text x="' + f1(a.x) + '" y="' + f1(a.y) + '" font-size="18" font-weight="700" fill="' + INK + '" text-anchor="end">' + esc(a.txt) + "</text>");
      } else {
        o.push('<text x="' + f1(a.x) + '" y="' + f1(a.y) + '" font-size="15" font-weight="700" fill="#555" text-anchor="middle">' + esc(a.txt) + "</text>");
      }
    });

    /* leyenda: solo los símbolos que aparecen en esta topografía */
    var L = [];
    var fed = S.etiqueta === "federativo";
    if (used.r) L.push(["txt", "R", fed ? "Rápel: nº-metros-lado" : "Rápel y metros"]);
    if (used.d) L.push(["txt", fed ? "d" : "D", fed ? "Destrepe: nº-metros-lado" : "Destrepe y metros"]);
    if (used.pc) L.push(["txt", "Pc", "Pasamanos con cuerda fija"]);
    if (fed) L.push(["txt", "I · C · D", "Lado izquierdo, centro, derecho"]);
    ANC.forEach(function (a) { if (used["a_" + a[0]]) L.push(["anc", a[0], a[1].replace(/ \(.*\)$/, "")]); });
    if (used.u_2c) L.push(["uni", "2c", "Anclajes unidos por cadena"]);
    if (used.u_2k) L.push(["uni", "2k", "Anclajes unidos por cordino"]);
    if (used.dest) L.push(["dest", "", "Rápel destrepable"]);
    if (used.poza) L.push(["poza", "", "Poza"]);
    if (used.rem) L.push(["rem", "", "Remolino"]);
    if (used.peligro) L.push(["warn", "", "Peligro"]);
    if (used.nr) L.push(["nr", "", "Punto sin retorno"]);
    if (used.cut) L.push(["cut", "", "Tramo largo (acortado)"]);
    if (used.park) L.push(["park", "", "Parking"]);
    var showL = S.leyenda !== false && L.length;
    var cols = Math.max(1, Math.min(3, Math.floor((W - 48) / 250))), rows = showL ? Math.ceil(L.length / cols) : 0;
    var legY = drawH + 10, legH = showL ? 44 + rows * 28 : 0;
    var H = Math.max(320, drawH + legH + 46);
    if (showL) {
      o.push('<rect x="24" y="' + legY + '" width="' + (W - 48) + '" height="' + legH + '" fill="#fff" stroke="#c9d3e6" rx="6"/>');
      o.push('<rect x="24" y="' + legY + '" width="' + (W - 48) + '" height="26" fill="#1f5fae" rx="6"/><rect x="24" y="' + (legY + 14) + '" width="' + (W - 48) + '" height="12" fill="#1f5fae"/>');
      o.push('<text x="' + (W / 2) + '" y="' + (legY + 18) + '" font-size="13" font-weight="800" fill="#fff" text-anchor="middle" letter-spacing="2">LEYENDA</text>');
      var cw = (W - 48) / cols;
      L.forEach(function (it, i) {
        var cx = 24 + (i % cols) * cw + 14, cy = legY + 44 + Math.floor(i / cols) * 28, sx = cx + 22, g = "";
        if (it[0] === "txt") g = '<text x="' + sx + '" y="' + (cy + 5) + '" font-size="14" font-weight="800" fill="' + INK + '" text-anchor="middle">' + esc(it[1]) + "</text>";
        if (it[0] === "anc") g = anchors(sx - 8, cy + 5, it[1], "1");
        if (it[0] === "uni") g = anchors(sx - 14, cy + 1, "x", it[1]);
        if (it[0] === "dest") g = destrepable(sx, cy);
        if (it[0] === "poza") g = '<path d="M' + (sx - 14) + " " + (cy - 3) + " Q" + sx + " " + (cy + 14) + " " + (sx + 14) + " " + (cy - 3) + ' Z" fill="#9fd8ea"/>';
        if (it[0] === "rem") g = spiral(sx, cy, 9);
        if (it[0] === "warn") g = warn(sx, cy + 2);
        if (it[0] === "nr") g = noReturn(sx, cy);
        if (it[0] === "park") g = parking(sx, cy);
        if (it[0] === "cut") g = '<line x1="' + (sx - 16) + '" y1="' + cy + '" x2="' + (sx + 16) + '" y2="' + cy + '" stroke="' + INK + '" stroke-width="5"/><path d="M' + (sx - 8) + " " + (cy + 9) + " l6 -18 M" + (sx + 2) + " " + (cy + 9) + ' l6 -18" stroke="#fff" stroke-width="6"/><path d="M' + (sx - 8) + " " + (cy + 9) + " l6 -18 M" + (sx + 2) + " " + (cy + 9) + ' l6 -18" stroke="' + INK + '" stroke-width="1.8"/>';
        o.push(g + '<text x="' + (sx + 30) + '" y="' + (cy + 5) + '" font-size="12.5" fill="#333">' + esc(it[2]) + "</text>");
      });
    }

    var info = [st.nR + (st.nR === 1 ? " rápel" : " rápeles")];
    if (st.maxR) info.push("más largo " + fmt(st.maxR) + " m", "cuerda mínima " + st.cuerda + " m");
    if (st.nD) info.push(st.nD + (st.nD === 1 ? " destrepe" : " destrepes"));
    if (st.nP) info.push(st.nP + (st.nP === 1 ? " pasamanos" : " pasamanos"));
    if (st.vert) info.push("desnivel vertical " + fmt(Math.round(st.vert)) + " m");
    if (st.walk) info.push(fmt(Math.round(st.walk)) + " m de cauce");
    o.push('<text x="24" y="' + (H - 18) + '" font-size="12.5" fill="#444">' + esc(info.join(" · ")) + "</text>");
    o.push('<text x="' + (W - 20) + '" y="' + (H - 18) + '" font-size="12" fill="#888" text-anchor="end">Hecho con la topografía de barrancos de guiasadastra.com</text>');
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + Math.round(W) + " " + Math.round(H) + '" width="' + Math.round(W) + '" height="' + Math.round(H) + '" font-family="Arial,Helvetica,sans-serif"><rect width="100%" height="100%" fill="#fff"/>' + o.join("") + "</svg>";
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
