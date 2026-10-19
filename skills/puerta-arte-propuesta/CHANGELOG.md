# Changelog — puerta-arte-propuesta
Skill de app. Pineado a Rameli v0.11.0.

## v0.5.0 — 2026-10-18 (lote de drafts mutilados p038-p057, cazado por el dueño)
Contexto: 16 diseños llegaron CORTADOS a los drafts de Printify (palabras
rebanadas en los extremos, hojas y elementos incompletos) y ninguna
puerta lo vio — la puerta medía que no sobrara aire tras el recorte,
pero un diseño ya cortado "pasa" ese criterio. Causas medidas, no
supuestas (auditoría completa en data/estado-correccion-recortes.json):
(a) lote A (p038-p045): el autotrim por bbox de MASA (0.05%) amputó los
extremos de baja masa de originales completos (7-53px por lado a escala
de generación); (b) lote B (p048-p057): un desbordamiento tipo fill
rebanó 0.4-3.7% por lado.
- Nuevo gate `composicion_completa` (`--es-original`, sobre el CRUDO
  antes de procesar): margen del bbox SEGURO por lado ≥ máx(6px, 0.4%).
  El bbox seguro = unión de componentes reales (área ≥150px,
  min(ancho,alto) ≥8px; filtra slivers/specks de borde).
- Nuevo gate `contenido_intacto` (finales): el bbox seguro no toca el
  borde del archivo (≥2px/lado).
- Nuevo gate `fidelidad_recorte` (`--original <crudo>`): desviación de
  aspecto del contenido ≤1.5% y pérdida en banda externa ≤2%/lado
  (rejilla 200×200 normalizada a bbox seguro). Si no se puede
  verificar, no pasa.
- FIX RAÍZ: `--autotrim` recorta al bbox SEGURO (antes: masa). La
  salida declara qué bbox usó (`autotrim_bbox`).
- Calibración con casos reales (no fixtures inventados): crudos del
  lote 16/16 PASS composición (mín. 0.86%/lado); prints mutilados
  16/16 FAIL composición (0px en los 4 lados) y 16/16 FAIL
  contenido_intacto; finales corregidos 16/16 PASS en todo, incluida
  fidelidad (pérdida 0.0, aspecto ≤0.5%). Fidelidad sola caza 10/16
  mutilados: las amputaciones finas/simétricas restantes no las
  separa ninguna métrica de píxeles a esa magnitud (el registro por
  template tiene piso de ruido ~0.5%/lado; medido y descartado como
  gate) — quedan cubiertas por contenido_intacto + el fix del
  mecanismo. La puerta nueva cazó además un defecto real en la
  primera reconstrucción corregida (p049 v1: pad inferior clampeado
  a 0) antes de subirla.
- Suite 8→13 casos: P3/F7 composición, P4/F8 fidelidad, F9 autotrim
  seguro (la barra fina de baja masa sobrevive: salida 1409px vs
  1384px con masa). 13/13 verde.

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
