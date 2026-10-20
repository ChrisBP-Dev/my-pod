---
name: "puerta-arte-propuesta"
description: "Puerta del arte-propuesta: valida el PNG del diseño ANTES de generar ningún mockup — fondo transparente, 300 DPI y dimensiones de impresión. Lo más barato de rechazar."
plantilla: false
license: "Apache-2.0"
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.6.1"
  framework_version: "0.14.0"
  regression_suite: "evals/"
---

# Puerta de Arte-Propuesta

**Versión: v0.6.1** · Primera puerta del flujo POD: la propuesta se valida
antes de generar ningún mockup. Un arte con fondo se rechaza aquí, no
después de 12 mockups.

## Cuándo usarme

- Al recibir la propuesta del diseño (PNG), antes de aprobar el arte.
- Si FAIL, el diseño vuelve a corrección. No se genera flat-lay.

## Procedimiento estándar (2026-10-15, endurecido 2026-10-18)

1. **Generar** el PNG con el brief (fondo transparente, sin backdrop).
1b. **Composición sobre el CRUDO** SIEMPRE, antes de tocarlo:
    `scripts/verificar-arte.py --archivo CRUDO.png --es-original`.
    Si el contenido toca el borde del lienzo de generación
    (`composicion_toca_borde`), el diseño nació cortado o un paso
    previo lo desbordó: NO se procesa — se regenera o se adjudica
    visualmente (un trazo que llega al borde ACABADO, p. ej. una línea
    EKG que cruza el diseño, es motivo, no truncamiento; lo decide el
    ojo, no la puerta — corrección del dueño 2026-10-18 tras el lote
    de drafts mutilados p038-p057).
2. **Limpiar** SIEMPRE: `scripts/limpiar-fondo.py --archivo ARTE.png`
   (elimina blanco puro global — método canónico; no es opcional).
2b. **Recortar** SIEMPRE: `scripts/verificar-arte.py --archivo ARTE.png
   --autotrim --salida ARTE.png` (recorta al bbox SEGURO +4px — ver
   Puertas mecánicas; sin este paso el PNG conserva el aire del lienzo
   de generación y el diseño entra chico a Printify — corrección del
   dueño 2026-10-17).
2c. **Counters rellenos** (2026-10-20): si la verificación marca
   `sin_counters_rellenos`, limpiar con
   `scripts/limpiar-counters.py --archivo ARTE.png --salida ARTE-v2.png`
   y re-verificar. El fondo encerrado en huecos de letras NO es blanco
   puro ni llega con flood-fill desde el exterior (el contorno lo
   encierra): el detector es por COMPONENTES (ver Puertas mecánicas)
   y la limpieza crece solo dentro del contorno oscuro, sin tocar el
   diseño (verificable por diff: 0 cambios fuera de las zonas).
3. **Correr** `scripts/verificar-arte.py` (`--archivo`, `--ancho-pulgadas`,
   `--exigir-margen-zoom` en el flujo de propuestas) y, cuando exista
   el crudo, **`--original CRUDO.png`** para la fidelidad de recorte.
4. **PASS** → el arte pasa a aprobación humana (ojo: counters).
   **FAIL** → se devuelve con el criterio violado. Si falla
   `sin_blanco_puro`, repetir paso 2 y re-verificar.
5. **Draft en Printify** → el dueño revisa ubicación en gris.
6. **Mockups** salen de Printify. Nada propio.

## Herramientas de procesamiento (scripts compartidos de la app)

Declaradas en la fase de mejora v0.14.0 (P2 — eran AVISO del
chequeo 1 de `rameli validar`: existían en `scripts/` sin que
ningún documento vivo los nombrara). Viven en los `scripts/`
compartidos de la app (una sola implementación), no en este
skill:

- `scripts/procesar-arte-propuesta.py` — procesa un crudo con
  fondo blanco generado (flood-fill desde las esquinas → alfa,
  limpieza de alfa, upscale FSRCNN ×2 + Lanczos al tamaño
  objetivo) y entrega el PNG print-ready corriendo esta puerta
  con `--autotrim`. Es la vía de entrada cuando el crudo NO
  nace con fondo transparente (pasos 1b–2b de arriba sobre ese
  tipo de crudo).
- `scripts/reparar-fondo-casi-blanco.py` — repara artes ya
  limpiados cuyo fondo quedó casi-blanco no puro (244–249, que
  el key canónico de blanco puro no atrapa): flood-fill desde
  el borde solo sobre píxeles neutros casi-blancos, preservando
  los blancos de diseño encerrados. Se usa cuando la puerta
  marca fondo no limpio en un arte que ya pasó la limpieza
  estándar (caso origen: lote 2026-10-16).

## Puertas mecánicas

- **formato**: PNG con canal alfa.
- **fondo_limpio**: las 4 esquinas alfa = 0 (atrapa el PNG con fondo
  de un color aplanado).
- **recorte_ajustado**: el bbox del contenido REAL (alfa≥128) deja, **en
  cada lado por separado**, ≤ máx(48px, 4% del lado) transparentes
  (criterio del dueño: recortado exacto al arte, sin bordes vacíos —
  los bordes vacíos distorsionan el área de impresión). **Corrección
  2026-10-17:** la puerta medía el margen MENOR de los 4 lados — un arte
  con aire enorme en 3 lados pasaba si un lado estaba pegado, y el
  canónico de calibración trae 50px de margen máximo (el "22px" citado
  era su mínimo). El dueño lo cazó revisando: PNG con mucho aire en
  todos lados y colocación pequeña. Ahora se mide lado por lado sobre
  el contenido visible (alfa≥128), no sobre píxeles fantasma.
- **dpi_al_zoom** (con `--exigir-margen-zoom`, obligatorio en el flujo
  de propuestas): el ANCHO DEL CONTENIDO debe rendir ≥300 DPI al ancho
  máximo de colocación (nominal ×1.20). **Motivo (dueño, 2026-10-17):**
  él agranda la colocación en su revisión; un arte que apenas pasa
  300 DPI al nominal cae a 250-260 DPI al agrandarlo y "ya no lo puede
  jugar". Si falla → escalar (`scripts/upscale-arte-fsrcnn.py`) y
  re-verificar ANTES de crear el draft. Nunca entregar al dueño un
  arte sin margen de zoom.
- **composicion_completa** (con `--es-original`, sobre el crudo, ANTES
  de cualquier recorte): el contenido no puede tocar el borde del
  lienzo de generación. Se mide con el **bbox seguro** (unión de
  componentes reales: área ≥150px y min(ancho,alto) ≥8px — filtra
  slivers y specks de borde que no son diseño) por lado: margen ≥
  máx(6px, 0.4% del lado) en los cuatro lados. Contenido en el borde =
  truncamiento de generación o desborde de un paso posterior.
  Calibración 2026-10-18: 16 crudos completos del lote ≥0.86% por
  lado → PASS; los 16 prints mutilados tocan el borde (0px) → FAIL.
- **contenido_intacto** (finales): el bbox seguro del archivo final no
  puede tocar el borde del lienzo (≥2px por lado). Este flujo es
  recorte-al-contenido + pad: si el contenido toca el borde del
  archivo, algo fue rebanado en el camino. Calibración: mutilados 0px
  en los 4 lados (16/16); buenos conocidos ≥12px.
- **fidelidad_recorte** (con `--original CRUDO`): el final debe
  contener TODO el crudo — desviación de aspecto del contenido
  ≤1.5% y pérdida en la banda externa (3%, rejilla 200×200) ≤2% por
  lado. Calibración: pares fieles 16/16 PASS (pérdida 0.0, aspecto
  ≤0.5%); pares mutilados 10/16 FAIL aquí y 16/16 FAIL en
  contenido_intacto. Cobertura honesta: las amputaciones finas y
  simétricas de pocos px no las separa ninguna métrica de píxeles a
  esa magnitud (medido) — se previenen en el mecanismo (autotrim
  seguro) y se hacen visibles con contenido_intacto.
- **Reparación** `--autotrim`: recorta al **bbox seguro** + 4px y
  re-verifica (la salida declara `"autotrim_bbox": "seguro"`).
  **Corrección raíz 2026-10-18:** antes recortaba al bbox por MASA
  (0.05% acumulado), que amputa los extremos de baja masa — puntas de
  guirnaldas, hojas finas, iconos pequeños, la base de un círculo —
  y así llegaron 8 diseños cortados a los drafts sin que ninguna
  puerta lo viera (el contenido que quedaba no tocaba el borde del
  crudo; el recorte mismo era el corte). Si el bbox seguro no se
  puede calcular (sin cv2/scipy), cae al de masa y lo declara
  (`"masa_fallback"`).
- **sin_blanco_puro**: blanco puro ≤0.3% (método canónico 2026-10-15).
- **sin_counters_rellenos** (2026-10-20, recalibrado el mismo día):
  ningún componente de la semilla acromática clara (alfa>128, media
  ≥200, spread ≤18) puede ser una mancha maciza en AMBAS dimensiones:
  área ≥1500px, densidad (área/bbox) ≥0.25 Y grosor (radio inscrito
  máximo) ≥13px. Mide COMPONENTES, no % global — los rellenos de
  p046 pesaban 0.69% del bbox y 0.0% de blanco puro y pasaban todo.
  Calibración: buenos conocidos ≤0.108 de densidad en todo
  componente ≥1500px; rellenos de p046: densidad 0.42–0.68, radio
  14.0–99.5. La densidad sola daba falsos positivos (líneas
  decorativas de p043, radio ≤2.8; brillos finos de p045/p062,
  ≤12.8): sin grosor, el componente se reporta como
  `counters_sospechosos` en mediciones y NO bloquea — zona gris
  medida que adjudica el ojo (ahí conviven rellenos chicos reales,
  p. ej. p052, con brillos de diseño). Limpieza:
  `scripts/limpiar-counters.py` (solo rellenos duros; sospechosos
  solo con `--incluir-sospechosos` tras adjudicar). Cobertura
  honesta: rellenos <1500px, tenues o cálidos no los caza — siguen
  en el gate humano.
- **dpi**: ≥300 al ancho de impresión del producto.
- **dimensiones**: lado menor ≥3000px (archivo de impresión).
- **sin_blancos_interiores**: blanco/casi-blanco opaco dentro del bbox ≤8%
  (atrapa el fondo sin limpiar: p022 mancha crema entre los elfos, p024
  disco blanco, 2026-10-15). Entre 2% y 8% → adjudicación visual (puede
  ser blanco de diseño: papel, copos — no se destruye con key global).
- **cabe_en_area_impresion**: INFORMATIVO, no bloquea (corrección suya
  2026-10-15): los diseños altos están permitidos; el criterio va en la
  COLOCACIÓN (scale-to-fit en publicar-printify-etsy) — el diseño debe
  verse COMPLETO en el mockup, nada cortado.
- **Método de limpieza canónico (2026-10-15, aprendido del rescate p021-p026):**
  en estos artes el diseño usa CREMA/blanco roto para sus elementos claros
  (rellenos de letras, luna, taza, cofia — nunca blanco puro) mientras que
  los restos de fondo son BLANCO PURO (min RGB ≥250, dispersión ≤18).
  Limpiar blanco puro globalmente elimina TODO el fondo —incluidos counters
  y espacios encerrados entre letras— sin tocar el diseño. Verificado en los
  6 artes: blanco puro 0% tras limpiar, diseño intacto.
- **Brief de generación (2026-10-15, pedido suyo):** fondo 100% transparente
  sin halo ni resplandor, sin backdrop/papel/viñeta detrás del diseño.
  El diseño debe mostrarse completo visualmente.
- **Criterios de generación (2026-10-15, de lo aprendido en el rescate):**
  el generador debe apuntar bien desde el inicio, no depender de la limpieza:
  1. **Fondo**: transparente real en TODAS partes —incluidos counters de
     letras (a, e, o, P, R) y espacios encerrados entre letras. Sin blanco
     ni crema en zonas que no sean elemento del diseño.
  2. **Disciplina de color**: los elementos claros del diseño usan CREMA /
     blanco roto cálido (nunca blanco puro #FFFFFF). Así el blanco puro,
     si aparece, es inconfundiblemente fondo y se elimina sin riesgo.
  3. **Resolución**: 300 DPI al tamaño de impresión (p. ej. 10" de ancho
     → ≥3000 px de ancho).
  4. **Composición completa**: el diseño entero visible, nada cortado en
     los bordes del PNG. Los diseños altos están permitidos.
  5. **Texto**: ortografía exacta, letras legibles, sin artefactos.
  6. **Sin halo**: bordes del diseño limpios, sin resplandor blanco
     alrededor de los elementos.
  **Fragmento para el prompt de imagen** (copiar tal cual al generar):
  > "isolated on a fully transparent background, no backdrop, no paper,
  > no vignette, no glow or halo around the design; light-colored areas
  > in warm cream/off-white tones (never pure white); transparent inside
  > letter counters and enclosed gaps; complete composition, nothing
  > cropped at the edges"
- **Gate humano**: counters — los rellenos grandes acromáticos los caza
  el gate mecánico `sin_counters_rellenos` (2026-10-20); el ojo sigue
  revisando los agujeros de letras (a, e, o, P...) por rellenos chicos,
  tenues o de tono cálido, y adjudica cualquier mancha dudosa.

## Calibraciones (mecanismo vs aplicación)

- `MECANISMO:` validar el arte antes del primer mockup (costo de rechazo
  mínimo) — universal.
- `MECANISMO:` fondo transparente medido por bbox alfa — universal.
- `CALIBRACIÓN:` MARGEN_MAX 48px o 4% por lado (el mayor), LADO_MIN
  3000px, DPI_MIN 300, ZOOM_HEADROOM 1.20 — recalibrado 2026-10-17
  contra vitals-stable-print-300dpi.png (márgenes por masa 0.05%:
  69/50/66/84px, máx 2.7% → PASS), arte-margen-amplio.png (≥185px/lado → FAIL),
  arte-aire-asimetrico.png (aire solo en 2 lados → FAIL; la versión
  anterior con min() lo pasaba) y arte-zoom-ok.png (contenido 3980px →
  PASS con margen de zoom; vitals sin margen → FAIL dpi_al_zoom).
  Revalidar si cambia el producto (otro ancho de impresión).
- `MECANISMO:` verifier-repair — el recorte es determinista y seguro,
  la puerta lo repara y re-verifica en vez de solo bloquear.
- `CALIBRACIÓN:` bbox seguro COMP_AREA_MIN 150px / COMP_DIM_MIN 8px;
  composición COMP_MARGEN_MIN máx(6px, 0.4%); toque de borde del
  final TOQUE_BORDE_MIN 2px; fidelidad FID_ASPECTO_MAX 1.5% /
  FID_BANDA_MAX 2% — calibrado 2026-10-18 contra el lote real
  p038-p057 (16 crudos completos, 16 prints mutilados, 16 finales
  corregidos verificados) + canónico vitals (margen seguro 24-50px).
  Detalle y cobertura honesta en CHANGELOG v0.5.0. Revalidar si un
  diseño legítimo trae elementos reales menores que el filtro de
  componentes (motas, estrellas sueltas <150px).

## Reglas con motivo

- (2026-10-13, errores recurrentes suyos) Los errores típicos: PNG con
  fondo de un color, fondo metido dentro de las letras. El primero lo
  atrapa `fondo_limpio`; el segundo lo revisa el ojo (gate humano
  declarado, no promesa falsa del código).
- (2026-10-20, caso p046 "ICU: I Care U", cazado por el dueño en
  Printify) **Counters con el fondo HORNEADO:** el PNG nació
  "transparente" y pasaba todas las puertas, pero los huecos cerrados
  de C-a-r-e traían el fondo crema-blanco como píxeles opacos (media
  ~249/245/237: ni blanco puro, ni conectado al borde, ni pesado
  contra el bbox). Lección medida: un % global nunca caza una mancha
  localizada — la propiedad real es el COMPONENTE (tamaño ×
  densidad × color acromático). Gate `sin_counters_rellenos` +
  `scripts/limpiar-counters.py` calibrados el mismo día; el gate
  humano de counters queda para lo chico/tenue/cálido, declarado.
- (2026-10-17, caso p036 ICU Thankful Heart, cazado por el dueño en el
  mockup) **Damero de "transparencia falsa" horneado en el arte:** el
  generador dibuja los cuadros grises del damero como píxeles reales y
  la limpieza por flood-fill/blanco puro NO los quita: son gris neutro
  ~237 (bajo el umbral de blanco puro ≥250 de `limpiar-fondo.py`) y
  quedan atrapados en huecos interiores entre elementos. Los gates
  actuales lo pasan todo (el damero es contenido opaco: `fondo_limpio`
  y `sin_blanco_puro` dan PASS). Detección: componer el arte sobre
  fondo NEGRO y mirar — los fragmentos aparecen como cuadros
  gris/blanco entre elementos; conteo de píxeles opacos acromáticos
  (dispersión RGB ≤18) con media ≥200 fuera de elementos de diseño.
  Limpieza determinista verificada: alfa→0 en píxeles acromáticos
  (dispersión ≤18, media ≥200, cualquier alfa) — el diseño de estos
  artes no usa gris neutro (sus claros son crema cálido), remanente 0
  y diseño intacto. Candidato a gate automático cuando se calibre
  contra artes con gris de diseño legítimo (no bloquear por defecto).

## Entrega para aprobación del dueño (flujo v2, 2026-10-19)

Un PASS de esta puerta NO va directo a producción: va primero
al dueño, en un chat nuevo, **por diseño**, con este bloque:

- **El arte final** (el PNG que pasó la puerta, adjunto).
- **El porqué:** tema y ángulo según la directriz vigente, la
  frase y su sentido, la iconografía y por qué esos elementos
  (qué significan en el tema; p. ej. qué es propio de la
  temporada y qué sería de otra).
- **Qué mirar:** los puntos que la puerta declara pendientes
  del ojo humano (counters/agujeros de las letras, trazos que
  llegan al borde adjudicados como motivo) y cualquier duda
  honesta del generador.

El porqué se escribe al generar (sale de la directriz y del
brief del diseño, no se inventa al entregar) y se guarda en el
registro del diseño (`porque` en `data/tiendas/<tienda-id>/registro-listings.json`)
para que lo hereden la producción y el paquete comercial. Sin
aprobación del dueño en esta entrega, el diseño no entra a
producción (flujo v2 en `FLUJO-PIPELINE.md`).
