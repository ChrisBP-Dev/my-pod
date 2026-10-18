# Changelog — puerta-arte-propuesta
Skill de app. Pineado a Rameli v0.9.0.

## v0.4.0 — 2026-10-17 (corrección del dueño revisando el lote de ayer)
- `recorte_ajustado` REPARADO: medía el margen MENOR de los 4 lados
  (min) — aire enorme en 3 lados pasaba si un lado estaba pegado. El
  canónico vitals trae máx 50px/lado (el "22px" citado era el mínimo).
  Ahora: bbox de contenido real (alfa≥128) y tope POR LADO
  máx(48px, 4% del lado). `--autotrim` usa el mismo bbox real.
- Nuevo gate `dpi_al_zoom` (flag `--exigir-margen-zoom`): el ancho del
  CONTENIDO debe rendir ≥300 DPI al ancho nominal ×1.20 — el dueño
  agranda la colocación al revisar y los artes de 3200px caían a
  250-260 DPI ("ya no lo puedo jugar").
- Procedimiento: paso 2b RECORTAR obligatorio (--autotrim) antes de la
  puerta final; antes el cron corría la puerta sin recortar nunca.
- Suite 5→8 casos: F5 aire asimétrico (caza el bug min), P2 zoom con
  margen, F6 vitals sin margen de zoom. Calibración verificada:
  conocido-bueno PASS / conocido-malo FAIL en cada criterio nuevo.
## v0.1.0 — 2026-10-13
- Creado desde la plantilla.

## v0.1.1 (2026-10-13)
- G2 dividido en `fondo_limpio` (esquinas alfa=0) y `recorte_ajustado`
  (margen ≤32px): el criterio del dueño es recorte exacto al arte, sin
  bordes vacíos — el gate anterior pedía margen mínimo, al revés.
- Nuevo `--autotrim`: recorta al bbox + 4px y re-verifica (verifier-repair).
- Suite 4/4: P1 + F1/F2/F3 (fondo, dpi, recorte).
