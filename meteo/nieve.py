# -*- coding: utf-8 -*-
"""Estado de la nieve por macizo (página /nieve/).

Lo llama procesar.py al terminar. Usa:
- el histórico de los últimos 15 días (historial.json): en cada ejecución se guardan las primeras 6 horas de la
  previsión de consenso, que es lo más parecido a lo que ha pasado de verdad;
- la previsión de los próximos 3 días.
Con eso estima nieve nueva, viento tras las nevadas, ciclos de deshielo y rehielo, lluvia sobre nieve y fusión,
y escribe nieve.json. Es una estimación orientativa, no un boletín de peligro de aludes.
"""
import datetime as dt, json, os, urllib.request
from zoneinfo import ZoneInfo

UTC = dt.timezone.utc
TZ = ZoneInfo("Europe/Madrid")
WEB = "https://www.guiasadastra.com"
DIAS_HIST = 15
CLAVES = ("tc", "tv", "pr", "wc", "dc", "i0", "sl", "sn", "snb")
DIRS = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
BOLETINES = {
    "Pirineos": [("Boletín de peligro de aludes de AEMET (Pirineo navarro y aragonés)", "https://www.aemet.es/es/eltiempo/prediccion/montana/boletin_peligro_aludes"),
                 ("Butlletí de perill d'allaus (ICGC, Pirineo catalán)", "https://bpa.icgc.cat/")],
}
PRED_MONTANA = ("Predicción de montaña de AEMET", "https://www.aemet.es/es/eltiempo/prediccion/montana")


def _t(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%MZ").replace(tzinfo=UTC)


def _f(t):
    return t.strftime("%Y-%m-%dT%H:%MZ")


def _dir_opuesta(d):
    if d is None:
        return None
    return DIRS[int(((d + 180) % 360) / 45 + 0.5) % 8]


def _dir(d):
    return None if d is None else DIRS[int((d % 360) / 45 + 0.5) % 8]


def es_nieve(p, alt):
    """¿La precipitación de este punto cae como nieve en la cumbre?"""
    if p.get("sl") is not None:
        return p["sl"] <= alt
    return p.get("tc") is not None and p["tc"] <= 0.5


def analizar(mac, pasado, futuro, ahora):
    alt = mac["cumbre"]["alt"]
    todos = sorted(pasado + futuro, key=lambda p: p["t"])
    # agrupar por día local
    dias = {}
    for p in todos:
        d = _t(p["t"]).astimezone(TZ).strftime("%Y-%m-%d")
        x = dias.setdefault(d, {"fecha": d, "tc": [], "pr_n": 0.0, "pr_l": 0.0, "wc": [], "i0": [], "tipo": set(), "dc": []})
        if p.get("tc") is not None:
            x["tc"].append(p["tc"])
        pr = p.get("pr") or 0.0
        if pr:
            if es_nieve(p, alt):
                x["pr_n"] += pr
            else:
                x["pr_l"] += pr
        if p.get("wc") is not None:
            x["wc"].append(p["wc"])
            x["dc"].append((p["wc"], p.get("dc")))
        if p.get("i0") is not None:
            x["i0"].append(p["i0"])
        x["tipo"].add("previsto" if _t(p["t"]) > ahora else "pasado")
    tabla = []
    for d in sorted(dias):
        x = dias[d]
        vmax = max(x["dc"], key=lambda y: y[0]) if x["dc"] else (None, None)
        tabla.append({"fecha": d, "tipo": "previsto" if x["tipo"] == {"previsto"} else ("pasado" if x["tipo"] == {"pasado"} else "hoy"),
                      "tc_min": round(min(x["tc"])) if x["tc"] else None, "tc_max": round(max(x["tc"])) if x["tc"] else None,
                      "nieve": round(x["pr_n"]), "lluvia": round(x["pr_l"], 1), "wc_max": round(vmax[0]) if vmax[0] is not None else None,
                      "wc_dir": _dir(vmax[1]), "wc_dir_g": vmax[1], "i0_max": max(x["i0"]) if x["i0"] else None})
    # manto actual (modelo) y nieve nueva
    actual = [p for p in todos if _t(p["t"]) <= ahora + dt.timedelta(hours=1)]
    ult = actual[-1] if actual else (futuro[0] if futuro else {})
    manto, manto_b = ult.get("sn"), ult.get("snb")

    def suma_nieve(desde, hasta):
        return sum((p.get("pr") or 0) for p in todos if desde < _t(p["t"]) <= hasta and es_nieve(p, alt))
    n72 = suma_nieve(ahora - dt.timedelta(hours=72), ahora)
    n7d = suma_nieve(ahora - dt.timedelta(days=7), ahora)
    nfut = suma_nieve(ahora, ahora + dt.timedelta(hours=72))
    lluvia_sobre = sum((p.get("pr") or 0) for p in todos if ahora - dt.timedelta(hours=72) < _t(p["t"]) <= ahora + dt.timedelta(hours=48) and not es_nieve(p, alt))
    hay_nieve = (manto or 0) >= 3 or n7d >= 3 or nfut >= 3
    señales = []
    estado = "Sin nieve significativa"
    if not hay_nieve:
        señales.append(("info", "Sin nieve significativa en cumbre según los modelos."))
    else:
        if n72 >= 10:
            señales.append(("alto", "Nevada reciente: unos %d cm en los últimos 3 días. Nieve todavía sin asentar." % round(n72)))
            estado = "Nieve reciente"
        if nfut >= 5:
            señales.append(("medio", "Nieve nueva prevista: unos %d cm en los próximos 3 días." % round(nfut)))
        # viento con nieve reciente o prevista
        ventanas = [p for p in todos if ahora - dt.timedelta(hours=72) < _t(p["t"]) <= ahora + dt.timedelta(hours=48)]
        fuerte = [p for p in ventanas if (p.get("wc") or 0) >= 40]
        if fuerte and (n72 + nfut) >= 5:
            pmax = max(fuerte, key=lambda p: p["wc"])
            señales.append(("alto", "Viento fuerte (hasta %d km/h del %s) con nieve reciente o prevista: placas de viento probables en laderas orientadas al %s y en collados." % (
                round(pmax["wc"]), _dir(pmax.get("dc")) or "–", _dir_opuesta(pmax.get("dc")) or "–")))
            estado = "Placas de viento probables"
        # ciclos de deshielo y rehielo
        ciclos = 0
        for a, b in zip(tabla, tabla[1:]):
            if a["tc_max"] is not None and b["tc_min"] is not None and a["tc_max"] >= 1 and b["tc_min"] <= -2:
                ciclos += 1
        if ciclos:
            señales.append(("medio", "Ciclos de deshielo y rehielo (%d en el periodo): costra dura y helada a primera hora, conviene crampones y piolet; transforma a partir del mediodía en solanas." % ciclos))
            if estado == "Sin nieve significativa":
                estado = "Costra de rehielo"
        if lluvia_sobre >= 2 and (manto or 0) >= 3:
            señales.append(("alto", "Lluvia sobre la nieve (%s mm): nieve húmeda y pesada; al volver a helar, hielo y costra muy dura." % round(lluvia_sobre, 1)))
            if estado in ("Sin nieve significativa", "Costra de rehielo"):
                estado = "Nieve húmeda"
        dias_calor = sum(1 for d in tabla if d["i0_max"] is not None and d["i0_max"] >= alt + 500)
        if dias_calor >= 2 and (manto or 0) >= 3:
            señales.append(("alto", "Isocero muy por encima de la cumbre %d días: nieve húmeda, posibles purgas y aludes de fusión en las horas centrales. Madrugar." % dias_calor))
            if estado in ("Sin nieve significativa", "Costra de rehielo"):
                estado = "Nieve húmeda / fusión"
        racha = mx = 0
        for d in tabla:
            racha = racha + 1 if d["tc_max"] is not None and d["tc_max"] <= -3 else 0
            mx = max(mx, racha)
        if mx >= 3:
            señales.append(("medio", "Frío persistente (%d días seguidos sin pasar de −3 °C en cumbre): nieve fría y polvo, poco transformada; las placas se estabilizan despacio." % mx))
            if estado == "Sin nieve significativa":
                estado = "Nieve fría / polvo"
        if estado == "Sin nieve significativa":
            estado = "Nieve asentada"
            señales.append(("info", "Sin cambios importantes: nieve asentada según los modelos."))
    return {"id": mac["id"], "nombre": mac["nombre"], "corto": mac["corto"], "region": mac["region"],
            "cumbre": mac["cumbre"], "base": mac["base"], "estado": estado, "hay_nieve": hay_nieve,
            "manto": manto, "manto_base": manto_b, "nieve_72h": round(n72), "nieve_7d": round(n7d), "nieve_prevista": round(nfut),
            "senales": [{"nivel": n, "txt": t} for n, t in señales], "dias": tabla,
            "boletines": BOLETINES.get(mac["region"], []) + [PRED_MONTANA],
            "historico_horas": len(pasado)}


def generar(out, macizos, log=print):
    ahora = dt.datetime.now(UTC)
    hist = {}
    try:
        req = urllib.request.Request("%s/meteo/datos/historial.json?n=%d" % (WEB, ahora.timestamp()), headers={"User-Agent": "guiasadastra.com"})
        hist = json.loads(urllib.request.urlopen(req, timeout=30).read().decode("utf-8")).get("macizos", {})
        log("Nieve: histórico recuperado (%d macizos)" % len(hist))
    except Exception as ex:
        log("Nieve: sin histórico previo (%s)" % ex)
    res = []
    for mac in macizos:
        try:
            doc = json.load(open(os.path.join(out, mac["id"] + ".json"), encoding="utf-8"))
        except Exception:
            continue
        t0 = _t(doc["t0"])
        C = doc["consenso"]
        hs = doc.get("h") or [i * doc["paso"] for i in range(len(C["tc"]))]
        puntos = [dict({"t": _f(t0 + dt.timedelta(hours=h))}, **{k: C.get(k, [None] * len(hs))[i] for k in CLAVES}) for i, h in enumerate(hs)]
        # al histórico: lo de las primeras 6 horas de esta ejecución
        h_mac = {p["t"]: p for p in hist.get(mac["id"], [])}
        for p in puntos:
            if _t(p["t"]) < t0 + dt.timedelta(hours=6):
                h_mac[p["t"]] = p
        limite = ahora - dt.timedelta(days=DIAS_HIST)
        hist[mac["id"]] = [h_mac[k] for k in sorted(h_mac) if _t(k) >= limite]
        pasado = [p for p in hist[mac["id"]] if _t(p["t"]) <= ahora]
        futuro = [p for p in puntos if ahora < _t(p["t"]) <= ahora + dt.timedelta(hours=72)]
        res.append(analizar(mac, pasado, futuro, ahora))
    json.dump({"generado": _f(ahora), "macizos": hist}, open(os.path.join(out, "historial.json"), "w", encoding="utf-8"), separators=(",", ":"))
    json.dump({"generado": _f(ahora), "macizos": res}, open(os.path.join(out, "nieve.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    log("Nieve: %s" % ", ".join("%s=%s (%s cm)" % (r["id"], r["estado"], r["manto"]) for r in res if r["hay_nieve"]) or "Nieve: sin nieve en ningún macizo")
