/* Qué llevar en la mochila: listas por actividad que se van tachando. Lo marcado se guarda en este navegador. */
(function () {
  "use strict";
  var SIEMPRE = {
    "Seguridad y orientación": ["Móvil cargado y batería externa", "Frontal con pilas de repuesto", "Botiquín básico (tiritas, vendas, antiinflamatorio, tus medicinas)", "Manta térmica", "Silbato", "Mapa o track descargado en el móvil", "Teléfono de emergencias: 112"],
    "Comida, agua y otros": ["Agua (1,5–2 l o más si hace calor)", "Comida y algo energético (frutos secos, barritas)", "Crema solar y protector de labios", "Gafas de sol", "DNI, tarjeta sanitaria y licencia federativa", "Algo de dinero", "Bolsa para la basura"],
  };
  var ACT = [
    { id: "barrancos", n: "Barrancos", g: {
      "Equipo técnico": ["Casco", "Arnés de barranco con culera", "Descensor (ocho, pirana…)", "2–3 mosquetones de seguridad", "Cabo de anclaje doble", "Cuerda: el doble del rápel más largo + margen", "Cuerda de reserva", "Autobloqueante o cordino para prusik", "Navaja de barranco", "Kit de instalación (cordino, maillones)", "Topografía del barranco"],
      "Ropa y calzado": ["Neopreno (completo, de 5 mm en aguas frías)", "Escarpines o calcetines de neopreno", "Calzado de barranco o con buena suela", "Escarpín/capucha o chaleco extra si el agua está muy fría"],
      "Mochila y estanqueidad": ["Saca de barranco con drenaje", "Bidón estanco para comida, móvil y botiquín", "Funda estanca para el móvil"],
      "Al terminar (en el coche)": ["Ropa seca y toalla", "Bolsa para el neopreno mojado", "Calzado seco"] } },
    { id: "deportiva", n: "Escalada deportiva", g: {
      "Equipo técnico": ["Pies de gato", "Arnés", "Casco", "Cuerda de 60–80 m", "12–16 cintas exprés", "Aparato de aseguramiento (mejor con bloqueo asistido)", "Mosquetón HMS de seguridad", "Cabo de anclaje y 2 mosquetones de seguridad", "Material para montar el descuelgue", "Magnesera y magnesio", "Cepillo para las presas", "Croquis o reseña de la escuela"],
      "Ropa y otros": ["Ropa cómoda que deje mover", "Chaqueta para asegurar a la sombra", "Lona o saco para la cuerda", "Esparadrapo para los dedos", "Calzado de aproximación"] } },
    { id: "clasica", n: "Escalada clásica", g: {
      "Equipo técnico": ["Pies de gato cómodos para muchas horas", "Arnés con portamaterial", "Casco", "Cuerdas dobles o gemelas", "Juego de friends", "Juego de empotradores", "Extractor de fisureros", "Cintas exprés y cintas largas", "Anillos de cinta y cordinos", "Mosquetones de seguridad para las reuniones", "Aparato tipo reverso (aseguramiento desde reunión)", "Autobloqueantes / cordinos de prusik", "Navaja", "Croquis impreso de la vía y del descenso"],
      "Ropa y otros": ["Calzado de aproximación (para bajar)", "Cortavientos ligero", "Capa de abrigo ligera", "Mochila pequeña de pared", "Frontal (las vías largas se alargan)", "Agua y comida para la pared"] } },
    { id: "alpinismo", n: "Alpinismo", g: {
      "Equipo técnico": ["Botas rígidas o semirrígidas", "Crampones ajustados a las botas", "Piolet (o dos piolets técnicos)", "Casco", "Arnés", "Cuerda (simple o doble según la ruta)", "Tornillos de hielo y estaca o muerto", "Cintas y mosquetones de seguridad", "Aparato de aseguramiento", "Cordinos y prusik", "ARVA, pala y sonda", "Polainas"],
      "Ropa (sistema de capas)": ["Camiseta térmica", "Forro polar o chaqueta de fibra", "Chaqueta y pantalón con membrana", "Plumífero para paradas", "Guantes finos y guantes gordos (dos pares)", "Gorro y buff", "Gafas de ventisca (categoría 3–4)", "Calcetines de recambio"],
      "Navegación y otros": ["GPS o app con el track y brújula", "Termo con bebida caliente", "Comida energética fácil de comer con guantes", "Consulta del boletín de aludes y la previsión"] } },
    { id: "senderismo", n: "Senderismo", g: {
      "Ropa y calzado": ["Botas o zapatillas de montaña", "Calcetines técnicos", "Camiseta transpirable (nada de algodón)", "Forro polar ligero", "Chubasquero o cortavientos", "Gorra o gorro según la época"],
      "Otros": ["Bastones", "Mochila de 20–30 l", "Papel higiénico y bolsa para recogerlo"] } },
    { id: "montanismo", n: "Montañismo", g: {
      "Ropa y calzado": ["Botas de montaña", "Calcetines técnicos y de recambio", "Camiseta térmica", "Forro polar o chaqueta de fibra", "Chaqueta con membrana", "Plumífero ligero para la cima", "Pantalón de montaña (y cubrepantalón si hay mal tiempo)", "Guantes y gorro", "Gafas de sol de categoría 3–4"],
      "Equipo": ["Bastones", "Crampones o microcrampones si hay nieve o hielo", "Piolet si hay nieve", "Casco si hay trepadas o caída de piedras", "GPS o app con el track y brújula", "Termo"] } },
    { id: "vivac", n: "Vivac", g: {
      "Para dormir": ["Saco de dormir (mira la temperatura de confort)", "Esterilla aislante", "Funda de vivac o tienda ligera", "Almohada hinchable o la ropa en una bolsa", "Ropa seca para dormir", "Gorro y calcetines secos", "Tapones para los oídos"],
      "Cocina y agua": ["Hornillo, cartucho de gas y mechero", "Cazo y cubiertos", "Cena y desayuno", "Agua de sobra o filtro / pastillas potabilizadoras", "Taza o vaso"],
      "Otros": ["Plumífero", "Frontal con pilas de repuesto", "Papel higiénico y pala", "Bolsas para bajar toda la basura", "Normativa del espacio natural (dónde y desde qué altura se permite vivaquear)"] } },
  ];

  var el = document.getElementById("mo-app");
  if (!el) return;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function leer(k, def) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : def; } catch (e) { return def; } }
  function guardar(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  var act = leer("mochila-act", "senderismo");
  if (location.hash && ACT.some(function (a) { return "#" + a.id === location.hash; })) act = location.hash.slice(1);

  function grupos(a) {
    var g = {}, extra = leer("mochila-extra-" + a.id, []);
    Object.keys(a.g).forEach(function (k) { g[k] = a.g[k]; });
    Object.keys(SIEMPRE).forEach(function (k) { g[k] = SIEMPRE[k]; });
    if (extra.length) g["Añadido por ti"] = extra;
    return g;
  }

  function pintar() {
    var a = ACT.filter(function (x) { return x.id === act; })[0] || ACT[0];
    var marcados = leer("mochila-" + a.id, {}), g = grupos(a), total = 0, hechos = 0;
    Object.keys(g).forEach(function (k) { g[k].forEach(function (it) { total++; if (marcados[it]) hechos++; }); });
    var h = '<div class="mo-btns" role="tablist">' + ACT.map(function (x) {
      return '<button type="button" role="tab" aria-selected="' + (x.id === a.id) + '" class="mo-btn' + (x.id === a.id ? " on" : "") + '" data-a="' + x.id + '">' + esc(x.n) + "</button>";
    }).join("") + "</div>";
    h += '<div class="mo-prog"><div class="mo-bar"><i style="width:' + (total ? Math.round(100 * hechos / total) : 0) + '%"></i></div><b>' + hechos + " de " + total + "</b>" +
      (hechos === total && total ? ' <span class="mo-ok">¡Mochila lista!</span>' : "") + "</div>";
    h += '<div class="mo-grid">' + Object.keys(g).map(function (k) {
      return '<fieldset class="mo-g"><legend>' + esc(k) + "</legend>" + g[k].map(function (it) {
        var on = !!marcados[it];
        return '<label class="mo-it' + (on ? " hecho" : "") + '"><input type="checkbox" data-it="' + esc(it) + '"' + (on ? " checked" : "") + "><span>" + esc(it) + "</span>" +
          (k === "Añadido por ti" ? '<button type="button" class="mo-del" data-del="' + esc(it) + '" aria-label="Quitar">×</button>' : "") + "</label>";
      }).join("") + "</fieldset>";
    }).join("") + "</div>";
    h += '<form class="mo-add" onsubmit="return false"><input id="mo-nuevo" placeholder="Añadir algo a la lista…" maxlength="80"><button type="submit" class="btn btn-ghost">Añadir</button></form>';
    h += '<div class="mo-acc"><button type="button" class="btn btn-ghost" id="mo-reset">Desmarcar todo</button><button type="button" class="btn btn-ghost" onclick="window.print()">Imprimir la lista</button></div>';
    el.innerHTML = h;
    el.querySelectorAll(".mo-btn").forEach(function (b) { b.addEventListener("click", function () { act = b.getAttribute("data-a"); guardar("mochila-act", act); history.replaceState(null, "", "#" + act); pintar(); }); });
    el.querySelectorAll("input[data-it]").forEach(function (c) {
      c.addEventListener("change", function () { var m = leer("mochila-" + a.id, {}); if (c.checked) m[c.getAttribute("data-it")] = 1; else delete m[c.getAttribute("data-it")]; guardar("mochila-" + a.id, m); pintar(); });
    });
    el.querySelectorAll("[data-del]").forEach(function (b) {
      b.addEventListener("click", function (ev) { ev.preventDefault(); var x = leer("mochila-extra-" + a.id, []).filter(function (y) { return y !== b.getAttribute("data-del"); }); guardar("mochila-extra-" + a.id, x); pintar(); });
    });
    el.querySelector(".mo-add").addEventListener("submit", function () {
      var v = document.getElementById("mo-nuevo").value.trim(); if (!v) return;
      var x = leer("mochila-extra-" + a.id, []); if (x.indexOf(v) < 0) x.push(v); guardar("mochila-extra-" + a.id, x); pintar();
      document.getElementById("mo-nuevo").focus();
    });
    document.getElementById("mo-reset").addEventListener("click", function () { guardar("mochila-" + a.id, {}); pintar(); });
  }
  pintar();
})();
