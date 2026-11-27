# -*- coding: utf-8 -*-
"""Peligro de aludes oficial por zona (página /nieve/ y previsión por macizo).

Fuentes:
- EAWS (avalanches.org): niveles máximos de cada zona para hoy y mañana. Incluye el Pirineo navarro y aragonés
  (AEMET), Cataluña (ICGC), Arán (Conselh Generau d'Aran) y Andorra.
- AEMET (PDF): Guadarrama, Picos de Europa y Cordel–Peña Labra, que no publica en EAWS. Se lee el nivel solo si el
  texto lo da sin ambigüedad (número y nombre del nivel juntos); si no, la zona queda sin nivel y con el enlace.
Las zonas (meteo/zonas-aludes.json) salen de regions.avalanches.org, simplificadas.
No se inventa nada: si una fuente no responde, esa zona queda sin nivel.
"""
import datetime as dt, json, os, re, urllib.request
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Madrid")
UA = {"User-Agent": "guiasadastra.com (prevision de montana)"}
EAWS = "https://static.avalanche.report/eaws_bulletins/{d}/{d}.ratings.json"
AEMET_BPA = "https://www.aemet.es/es/eltiempo/prediccion/montana/boletin_peligro_aludes"
AEMET_PDF = {
    "ES-GU": "https://www.aemet.es/documentos/es/eltiempo/prediccion/montana/boletin_peligro_aludes/BPA_PN_Guadarrama.pdf",
    "ES-PE": "https://www.aemet.es/documentos/es/eltiempo/prediccion/montana/boletin_peligro_aludes/BPA_PN_Picos_Europa.pdf",
    "ES-CL": "https://www.aemet.es/documentos/es/eltiempo/prediccion/montana/boletin_peligro_aludes/BPA_sierra_Cordel_PLabra.pdf",
}
NOMBRES_NIVEL = {1: "Débil", 2: "Limitado", 3: "Notable", 4: "Fuerte", 5: "Muy fuerte"}


def fuente(rid):
    if rid.startswith("ES-CT-L"):
        return "Conselh Generau d'Aran", "https://lauegi.report/"
    if rid.startswith("ES-CT"):
        return "ICGC", "https://bpa.icgc.cat/"
    if rid.startswith("AD"):
        return "Servei Meteorològic d'Andorra", "https://www.meteo.ad/"
    return "AEMET", AEMET_PDF.get(rid, AEMET_BPA)


def _get(url, timeout=40):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def _eaws(fecha, log):
    try:
        r = json.loads(_get(EAWS.format(d=fecha)).decode("utf-8")).get("maxDangerRatings", {})
        return {k: v for k, v in r.items() if ":" not in k and isinstance(v, int) and 1 <= v <= 5}
    except Exception as ex:
        log("Aludes: sin EAWS para %s (%s)" % (fecha, ex))
        return None


def _nivel_pdf(texto):
    """Nivel solo si aparece el número junto a su nombre (p. ej. «3 - Notable» o «Notable (3)»)."""
    t = " ".join(texto.split())
    if re.search(r"finaliza(da|do)? la campaña|no se emite", t, re.I):
        return None
    hall = []
    for n, nom in NOMBRES_NIVEL.items():
        pat = r"(?<!\d)%d\s*[-–(:.]?\s*%s\b|\b%s\s*\(?\s*%d(?!\d)" % (n, nom, nom, n)
        if re.search(pat, t, re.I):
            hall.append(n)
    return max(hall) if hall else None


def _texto_pdf(b):
    try:
        import io, pypdf
        return "\n".join((p.extract_text() or "") for p in pypdf.PdfReader(io.BytesIO(b)).pages)
    except Exception:
        return ""


def _dentro(lon, lat, anillo):
    dentro = False
    for (a1, o1), (a2, o2) in zip(anillo, anillo[1:] + anillo[:1]):
        if (a1 > lat) != (a2 > lat) and lon < (o2 - o1) * (lat - a1) / (a2 - a1) + o1:
            dentro = not dentro
    return dentro


FIJAS = {"pirineo-navarro": "ES-NA"}  # cumbres en el límite entre dos zonas


def zona_de(lat, lon, zonas):
    """Zona que contiene el punto; si ninguna, la que tenga el borde a menos de ~5 km."""
    mejor, dmin = None, 0.05
    for rid, z in zonas.items():
        for an in z["anillos"]:
            if _dentro(lon, lat, an):
                return rid
            for a, o in an:
                d = ((a - lat) ** 2 + ((o - lon) * 0.78) ** 2) ** 0.5
                if d < dmin:
                    mejor, dmin = rid, d
    return mejor


def generar(out, macizos, log=print):
    zonas = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "zonas-aludes.json"), encoding="utf-8"))
    hoy = dt.datetime.now(TZ).date()
    fechas = [hoy.isoformat(), (hoy + dt.timedelta(days=1)).isoformat()]
    niveles = {f: (_eaws(f, log) or {}) for f in fechas}
    regiones = {}
    for rid, z in zonas.items():
        f, url = fuente(rid)
        regiones[rid] = {"nombre": z["nombre"], "fuente": f, "url": url, "dias": {d: niveles[d].get(rid) for d in fechas}}
    for rid, url in AEMET_PDF.items():
        try:
            n = _nivel_pdf(_texto_pdf(_get(url)))
            if n:
                regiones[rid]["dias"][fechas[0]] = n
            log("Aludes: %s (PDF de AEMET) -> %s" % (rid, n))
        except Exception as ex:
            log("Aludes: sin PDF de %s (%s)" % (rid, ex))
    por_macizo = {}
    for m in macizos:
        rid = FIJAS.get(m["id"]) or zona_de(m["cumbre"]["lat"], m["cumbre"]["lon"], zonas)
        if rid:
            r = regiones[rid]
            por_macizo[m["id"]] = {"zona": rid, "nombre": r["nombre"], "fuente": r["fuente"], "url": r["url"], "dias": r["dias"]}
    json.dump({"generado": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "fechas": fechas, "regiones": regiones,
               "macizos": {k: v["zona"] for k, v in por_macizo.items()},
               "zonas": {k: z["anillos"] for k, z in zonas.items()}},
              open(os.path.join(out, "aludes.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    con = [k for k, r in regiones.items() if any(r["dias"].values())]
    log("Aludes: %d zonas con nivel (%s); macizos con zona: %s" % (len(con), ", ".join("%s=%s" % (k, regiones[k]["dias"]) for k in con), ", ".join(por_macizo)))
    return por_macizo
