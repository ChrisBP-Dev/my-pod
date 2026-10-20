# Changelog — puerta-arte-propuesta

## v0.6.1 (2026-10-20) — recalibración por grosor (barrido del registro)
La validación integral que pidió el dueño tras el rescate de p046
barrió los 47 artes vigentes del registro con el detector v0.6.0 y
lo adjudicó visualmente: la densidad (área/bbox) sola NO es la
propiedad — líneas decorativas finas (p043, densidad hasta 0.55)
y brillos metálicos/ojos (p045/p054/p062) la cruzan igual que un
relleno. Medido el GROSOR (radio del mayor círculo inscrito):
rellenos verdaderos de p046 = 14.0–99.5px; líneas = ≤2.8px;
brillos finos = ≤12.8px.
- Gate de dos pisos: RELLENO (FAIL) exige ahora también radio
  >=13px. Sin grosor suficiente el componente se reporta en
  mediciones como `counters_sospechosos` y no bloquea: zona gris
  honesta donde conviven rellenos chicos reales (p052: counters
  de D/R de titular, radio 7.6–14.8) y diseño legítimo.
- `limpiar-counters.py` limpia por defecto SOLO rellenos duros
  (con v0.6.0 habría podido comerse las líneas de un diseño bueno);
  los sospechosos exigen `--incluir-sospechosos` tras adjudicar.
- Fixture nuevo `arte-lineas-finas.png` (caso P6 de la suite).
- Hallazgos del barrido (detalle en
  `docs/AUDITORIA-COUNTERS-2026-10-20.md`): vivos con sospechosos
  por adjudicar: p043/p045 (falsos positivos confirmados), p052/
  p054/p055/p056/p058/p062/p063/p067 y publicados p002/p021/p022/
  p031/p032/p034 (manchas chicas, 1.5–10k px c/u). p047 —que
  marcaba 19 componentes— fue eliminado por el dueño el mismo
  2026-10-20 revisando drafts: fuera de alcance.

## v0.6.0 (2026-10-20) — gate de counters rellenos (caso p046)
Contexto: p046 "ICU: I Care U" (draft MPL en Printify) traía los
huecos cerrados de las letras de "Care" (C, a, r, e) con el fondo
crema-blanco horneado como píxeles opacos. El PNG pasaba TODAS las
puertas (blanco_puro 0.0%, blancos interiores 0.69%): el fondo
encerrado no es blanco puro (media ~249/245/237), no toca el borde
y pesa poco contra el bbox completo. Lo cazó el dueño revisando en
Printify — la clase vivía solo en el gate humano.
- Nuevo gate `sin_counters_rellenos`: componentes de la semilla
  acromática clara (alfa>128, media>=200, spread<=18) con área
  >=1500px y densidad (área/bbox) >=0.25 = relleno. Calibración
  2026-10-20: buenos conocidos (vitals canónico, p036 v3, p037 v2,
  p028/p033 publicados) — densidad <=0.108 en todo componente
  >=1500px; p046 malo — 4 rellenos, densidad 0.42-0.68. Fixtures
  nuevos `arte-counters-rellenos.png` (FAIL) y
  `arte-counters-limpios.png` (PASS); suite 16/16.
- Nuevo `scripts/limpiar-counters.py`: quita los rellenos
  detectados creciendo sobre la franja clara contigua (el contorno
  oscuro y saturado actúa de pared; no cruza al diseño) + residuo
  encerrado. Rescate de p046 verificado por diff: 129,558px, solo
  alfa->0, 0 cambios de RGB, 0 cambios fuera de las 4 zonas;
  resultado `p046-print-300dpi-v2.png` con PASS completo
  (incl. dpi_al_zoom). El reemplazo en los drafts de Printify lo
  hace el dueño (él reacomoda y aprueba).
- Cobertura honesta: rellenos <1500px, tenues o de tono cálido
  siguen fuera del gate mecánico (gate humano, declarado).
- Hallazgo de la calibración: p047 (mismo lote, "sin tocar" en la
  corrección de recortes) marca la misma clase en varios
  componentes (densidad 0.26-0.68) — reportado al dueño, sin tocar:
  su revisión de ese draft sigue pendiente y el alcance pedido
  fue p046.

## v0.5.3 (2026-10-19)
- Fase de mejora v0.14.0: P1 — el diseño canónico de calibración de la suite vive ahora en `evals/fixtures/` (copia con origen y sha256 registrados en la suite; `K` ya no apunta fuera del repo). P2 — declaradas en el skill las herramientas compartidas `scripts/procesar-arte-propuesta.py` y `scripts/reparar-fondo-casi-blanco.py`.

## v0.5.2 (2026-10-19)
- El registro del diseño (`porque`) vive en `data/tiendas/<tienda-id>/registro-listings.json` (reorden de datos por tienda, 2026-10-19).
Skill de app. Pineado a Rameli v0.14.0.

## v0.5.1 — 2026-10-19 (flujo de propuestas v2, idea del dueño)
- Nueva sección "Entrega para aprobación del dueño": el PASS de
  la puerta se entrega por diseño en un chat nuevo, con el arte
  final y su porqué (tema/ángulo/frase/iconografía) + qué mirar
  (los pendientes del ojo humano que la puerta ya declaraba).
  Sin esa aprobación, el diseño no entra a producción: el dale
  creativo se mueve al punto más barato (antes se revisaba el
  arte recién en Printify, con los drafts ya creados). El porqué
  se guarda en el registro (`porque`) y lo hereda el paquete
  comercial. Sin cambios en los gates.

## v0.5.0 — 2026-10-18 (lote de drafts mutilados p038-p057, cazado por el dueño)
Contexto: 16 diseños llegaron CORTADOS a los drafts de Printify (palabras
rebanadas en los extremos, hojas y elementos incompletos) y ninguna
puerta lo vio — la puerta medía que no sobrara aire tras el recorte,
pero un diseño ya cortado "pasa" ese criterio. Causas medidas, no
supuestas (auditoría completa en data/registro-correccion-recortes-2026-10-19.json):
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
