# Seguimiento SEO

- `palabras-clave.txt`: búsquedas que se siguen cada mes.
- `historico/AAAA-MM-DD.csv`: foto de cada mes (búsquedas al mes en Google España, posición de www.guiasadastra.com y página que sale).
- `informe.py`: genera el CSV del mes y el resumen comparando con el mes anterior, a partir de dos respuestas de DataForSEO:
  `ranked_keywords/live` (target guiasadastra.com, location_code 2724, language_code es) y `google_ads/search_volume/live` con las palabras de la lista.
- Lo lanza una tarea programada cada mes (día 4) desde Claude, que además actualiza el documento «Competencia y estudio de mercado» y avisa.
- Coste aproximado por mes en DataForSEO: 0,10–0,15 $.
