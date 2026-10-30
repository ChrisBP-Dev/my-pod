---
name: "puerta-arte-propuesta"
description: "Puerta del arte-propuesta: valida el PNG del diseño ANTES de generar ningún mockup — fondo transparente, 300 DPI y dimensiones de impresión. Lo más barato de rechazar."
plantilla: false
license: "Apache-2.0"
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.14.0"
  framework_version: "0.19.0"
  regression_suite: "evals/"
---

# Puerta de Arte-Propuesta

**Versión: v0.14.0** · Primera puerta del flujo POD: la propuesta se valida
antes de generar ningún mockup. Un arte con fondo se rechaza aquí, no
después de 12 mockups.

## Cuándo usarme

- Al recibir la propuesta del diseño (PNG), antes de aprobar el arte.
- Si FAIL, el diseño vuelve a corrección. No se genera flat-lay.

## Procedimiento estándar (2026-10-15, endurecido 2026-10-18)

1. **Generar** el PNG con el brief (fondo transparente, sin backdrop).
1c. **Ruta de proceso del crudo opaco (OBLIGATORIA, 2026-10-30):**
    si el crudo nace opaco sobre fondo blanco (el caso normal de
    esta app), la ÚNICA vía de entrada es
    `scripts/procesar-arte-propuesta.py` (flood-fill con tolerancia
    desde las esquinas + borde suave + upscale FSRCNN), seguida de
    los pasos 2–3 de abajo. Quedan PROHIBIDAS las cadenas
    improvisadas (p. ej. «upscale premultiplicado → limpiar-fondo
    global», o limpiezas manuales hueco a hueco como ruta): escalar
    ANTES de quitar el fondo hornea la franja casi-blanca en
    counters y bordes, y la llave estricta de blanco puro ya no la
    alcanza después. Toda desviación de esta ruta se declara en la
    `nota_puerta` del diseño con su causa; una nota que declare una
    cadena distinta sin causa es defecto de la entrega. (Regresión
    2026-10-28/29: los lotes p082–p101 se procesaron con cadenas
    improvisadas y llegaron con la franja que el dueño cazó en
    p087–p091; los lotes de la era buena — p058–p067 — pasaron
    uniformes por `procesar-arte-propuesta.py`.)
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
2c. **Counters rellenos** (2026-10-20, adjudicación primero —
   corrección del mismo día tras el barrido completo): si la
   verificación marca `sin_counters_rellenos`, NO se limpia a
   ciegas: un componente macizo claro puede ser RELLENO (fondo
   horneado, caso p046) o DISEÑO (dientes, blanco del ojo, luz de
   lámpara, bisel 3D de las letras — en el barrido del registro,
   6 de 7 diseños marcados eran diseño; limpiarlos habría borrado
   partes del arte). Procedimiento: (1) generar el zoom de cada
   zona reportada sobre fondo negro y adjudicar con el ojo;
   (2) si es diseño, registrar el veredicto en el registro del
   diseño (`adjudicacion_counters`) y seguir; (3) si es relleno,
   limpiar con `scripts/limpiar-counters.py --archivo ARTE.png
   --salida ARTE-v2.png --adjudicado` (el flag es obligatorio: sin
   él el script no escribe) y re-verificar. El fondo encerrado en
   huecos de letras NO es blanco puro ni llega con flood-fill
   desde el exterior (el contorno lo encierra): el detector es por
   COMPONENTES (ver Puertas mecánicas) y la limpieza crece solo
   dentro del contorno oscuro, sin tocar el diseño (verificable
   por diff: 0 cambios fuera de las zonas).
   **Los SOSPECHOSOS se adjudican igual que los duros (2026-10-30):**
   cada componente de `counters_sospechosos` recibe su zoom sobre
   fondo oscuro y su veredicto registrado en el registro del diseño
   (`adjudicacion_counters` cubre duros Y sospechosos, zona por
   zona). La frase «sospechosos no bloqueantes» NO cierra un arte
   ni aparece como conclusión en una nota de puerta: describe una
   cola de adjudicación, no un resultado. Un arte con zonas sin
   veredicto registrado no se entrega.
2d. **Zoom de franja sobre fondo oscuro (SIEMPRE, cada arte,
   2026-10-30):** componer el arte final sobre fondo NEGRO y mirar
   con zoom (a) los counters de las letras del titular y (b) los
   bordes del diseño, buscando la FRANJA: el anillo casi-blanco
   teñido (media ~208–230, spread ~20–40) que queda pegado a un
   counter o a un borde cuando la limpieza no lo alcanzó. Ningún
   gate la mide (medido el 2026-10-30 sobre 19 artes: el bueno
   conocido p058 puntúa igual o peor que el malo p091 en blanco
   puro, blanco interior, componentes y franja fina — la clase es
   visual, como el damero de 2026-10-17). El veredicto se registra
   en la entrada del diseño: `revision_franja` = `limpia` |
   `corregida` (qué se limpió y con qué) | `diseno` (qué se ve y
   por qué es diseño). Sin `revision_franja` registrada, la
   entrega está incompleta aunque la puerta mecánica dé PASS.
   Si hay franja de fondo: se limpia por la ruta canónica (paso
   1c + paso 2; si el residuo es un bolsillo encerrado, paso 2c
   con `limpiar-counters.py`) y se REPITE el zoom hasta `limpia`.
3. **Correr** `scripts/verificar-arte.py` (`--archivo`, `--ancho-pulgadas`,
   `--exigir-margen-zoom` en el flujo de propuestas) y, cuando exista
   el crudo, **`--original CRUDO.png`** para la fidelidad de recorte.
4. **PASS** → el arte pasa a aprobación humana (ojo: counters).
   **FAIL** → se devuelve con el criterio violado. Si falla
   `sin_blanco_puro`, repetir paso 2 y re-verificar.
5. **Entrega en la vitrina** → el dueño decide ahí (aprobar /
   rechazar / mejorar); solo lo aprobado y registrado en el
   checkpoint pasa a producción. Nada se crea en Printify antes
   de esa aprobación (ver «Entrega para aprobación del dueño»).
6. **Producción en Printify** (Fase B, skill `publicar-printify-etsy`)
   → el dueño revisa UBICACIÓN en los borradores producidos.
   **Mockups** salen de Printify. Nada propio.

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
  que adjudica el ojo. **Calibración honesta (barrido completo
  del registro, adjudicado con zooms el 2026-10-20):** ni con
  grosor se separa la clase en arte ilustrado — los componentes
  DUROS de p052 (válvula), p054 (dientes), p063 (fondo sticker),
  p002 (estetoscopio), p022 (luz de lámpara) y p032 (ojo) son
  TODOS diseño; el único relleno real del registro era p046.
  Por eso el FAIL de este gate significa «adjudica con el ojo»
  (paso 2c), nunca «limpia directo»: su valor es que el caso
  p046 ya no llega a Printify sin que nadie lo mire. Limpieza:
  `scripts/limpiar-counters.py` (solo rellenos duros; sospechosos
  solo con `--incluir-sospechosos` tras adjudicar; escribir
  exige `--adjudicado`). Cobertura honesta: rellenos <1500px,
  tenues o cálidos no los caza — siguen en el gate humano.
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
  tenues o de tono cálido, y adjudica cualquier mancha dudosa. Desde
  v0.14.0 ese ojo es un paso numerado e ineludible (pasos 2c–2d):
  duros y sospechosos con veredicto registrado zona por zona, y zoom
  de franja sobre fondo oscuro en CADA arte con su `revision_franja`
  en el registro. Un PASS mecánico sin esos registros no es un arte
  verificado y no se entrega.

## Diseños personalizables — criterios (2026-10-20; razón primero, técnica después)

Un arte personalizable pasa TODAS las puertas de arriba **más** estas.
El procedimiento de campos/publicación vive en `publicar-printify-etsy`
(§Track Single-P); aquí vive el criterio de diseño. La base de evidencia
es el **estudio de criterios de personalización** (2026-10-20: tipología
de razones, patrones P1–P9 con su encaje, formatos reales); su doctrina
de patrones vive en `estratega-tienda`.

### La ficha de razón (sin ficha completa, no hay entrega)

Toda propuesta personalizada se entrega con su ficha:

- **Razón** en una frase verificable — identidad / relación / ocasión /
  conmemoración / pertenencia — nombrando el dato, su dueño y el vínculo
  ("el nombre de SU mascota junto al de la dueña: la pieza dice
  'nosotras'"). Si la frase vale igual para un diseño sin personalizar,
  la propuesta se rechaza: el mercado paga el vínculo, no el hueco.
- **Prueba de borrado:** sin el dato del comprador, el diseño debe verse
  INCOMPLETO (un club sin nombre, un badge sin titular, una manga sin
  los nombres); con el dato, es la pieza terminada. La simulación se
  entrega en los dos estados.
- **Campos:** máximo 3 del comprador, cada uno con tipo (texto /
  dropdown / imagen), límite y opciones. **Nombre ≤15 caracteres;
  credencial, título y club SOLO desde dropdown** con el vocabulario
  cerrado de la referencia de nicho de la tienda (ver «Formato
  profesional real» abajo) — jamás texto libre para un dato con vocabulario
  cerrado; año de 4 dígitos.
- **Comprador / destinatario / ocasión** nombrados; sin ocasión
  plausible en el calendario de la tienda, la propuesta espera.
- **Clase de encaje** del patrón (ver § de encaje): (a) automatizable es
  la norma; (b)/(c) exigen justificación escrita y aprobación expresa
  como excepción manual — nunca entran disfrazados de automatizables.
- **Ejemplo de simulación derivado del concepto** (NO un comodín único
  de tienda): el que un comprador real pondría en ESE concepto, con su
  formato real; y el **peor caso renderizado** (nombre de 15, roster
  completo) además del ejemplo bonito.

### Formato profesional real (referencia de nicho de la tienda)

El formato profesional real (firma de credenciales, vocabulario
cerrado de la profesión, instrucción al comprador) es **calibración
del nicho de la tienda**, no mecanismo de esta puerta: vive en la
referencia de nicho que la ficha de la tienda declara
(`config.json → nicho.referencia_formato_profesional`, en los datos
de la tienda). **Si la ficha declara un nicho con formato
profesional documentado, la puerta carga esa referencia ANTES de
juzgar propuestas personalizables** y juzga credenciales, títulos
y vocabulario contra ella (un formato inventado mata la
credibilidad ante un comprador que ES de esa profesión). Si la
ficha no declara referencia de nicho, la puerta juzga solo con
los criterios generales de esta sección y declara la ausencia en
su reporte — nunca aplica el formato de otro nicho.
(Movido el 2026-10-23, Programa Estándar My POD F4: la sección de
enfermería que vivía aquí era el nicho de una tienda concreta
viviendo en el skill; ahora vive como referencia de nicho en los
datos de esa tienda.)

### Encaje (regla de oro)

Si el patrón necesita que un humano TOQUE el dato o la imagen antes de
imprimir (convertir fecha→romanos, ilustrar un retrato, componer un
personaje), es **manual (b)**. La ruta automatizada **(a)** solo imprime
tal cual, a escala de caja, lo que el comprador escribió o subió:
badge pecho/manga, nombre+credencial con dropdown, club+nombre+año,
roster en UN campo con zona diseñada para lista, foto tal cual en marco
(con su pérdida declarada). Texto libre genérico sin razón ("tu texto
aquí") = **(c) no encaja por criterio**, aunque sea imprimible.

### Técnica de zona (la caja de herramientas — manda la razón, no la forma)

- **Nace con su zona integrada.** El arte se genera ya con la zona del
  dato integrada; nada de pegar capas sobre un diseño terminado (error
  de la prueba p005: capas chicas, pegadas al borde, 2ª línea tapada).
  La referencia visual del resultado se deriva del arte real, nunca se
  genera en paralelo.
- **La forma sigue al objeto real que imita** (corrección del dueño
  2026-10-19, afinada por el estudio): pecho = identidad (título /
  credencial), manga/muñeca = persona (nombre, roster, iniciales),
  espalda = nombre grande tipo jersey. Franjas genéricas sin lógica de
  objeto = la fórmula rechazada el 2026-10-20.
- **Geometría medida, no a ojo:** toda zona se mide desde los píxeles
  del arte final (bbox de la cara/zona) antes de montar capas, y se
  dimensiona para el PEOR caso del campo.
  - Nombre: caja ≈60–65% del ancho de la cara de su zona, ENTERA dentro
    con margen en los 4 lados, UNA línea. Capa de texto 2.5–3× más
    grande que el intento p005 (capa chica = nombre ilegible).
  - Dato bajo el diseño: pegado visualmente al bloque (separación
    ≈0.15–0.3"), nunca flotando; el arte deja el hueco con su ratio
    (zona + dato completos dentro del área de impresión).
  - **Contraste fuerte obligatorio** sobre la prenda más clara del
    listing: dorado tenue sobre blanco = FAIL.
- **Foto del comprador (verificado en vivo 2026-10-20):** la foto entra
  ENTERA con su proporción (FIT) y su propio fondo — la caja es cota
  máxima, no molde, y el comprador no puede ajustarla. El marco del
  arte se diseña **tipo passe-partout**: fondo y borde que absorban
  fotos verticales u horizontales (la foto tocará solo 2 lados de la
  caja si su ratio difiere). Formas no rectangulares NO disponibles:
  la forma la aporta el marco dibujado, no la foto. El listing lleva
  instrucciones de foto (clara, iluminada, sujeto centrado).
- **Bordado (pecho 4×4"):** texto corto y bold, sin degradados ni
  detalle fino; solo fuentes pre-digitalizadas. Sin Live Preview:
  el arte y las fotos del listing cargan la confianza.
- **Bordado — la FUENTE es plana, el look bordado es el RESULTADO**
  (recalibración 2026-10-26, duda del dueño resuelta contra la guía
  oficial de Printify): el archivo que entra a Printify para bordar
  es un dibujo PLANO — colores sólidos contrastantes (máx. 6 colores
  de hilo por diseño), formas gruesas (línea ≥0.05", texto ≥0.25" de
  alto), fondo transparente, SIN degradados, sombras, brillos ni
  textura de puntadas dentro del arte. La textura de hilo nace al
  digitalizar (el proveedor convierte el dibujo en recorridos de
  aguja) y al coser: un arte que ya «se ve bordado» obliga a la
  digitalización a simplificar o alterar sus partes finas y el
  resultado real difiere de la previa. La propuesta de un bordado
  lleva UN solo arte — la fuente plana — y la simulación se compone
  sobre esa misma fuente, como en todo método: el dueño juzga el
  diseño tal cual es y dónde va su personalización. **No existe
  vista de «resultado esperado» con textura** (el campo
  `resultado_esperado` quedó retirado por corrección del dueño el
  2026-10-26: fingir el acabado bordado en una previa confunde el
  juicio; que el cosido real nace de digitalizar la fuente se
  declara en la ficha, no se renderiza). El diseño declara su
  `metodo` (ver «Dónde vive en el sistema»). Un arte bordado cuya
  fuente lleve textura, degradados o más de 6 colores sólidos es
  FAIL de esta puerta, no un estilo. **Puerta mecánica (desde
  v0.13.0, 2026-10-27):** `scripts/verificar-arte.py --metodo
  bordado` mide los colores dominantes del contenido (gate
  `fuente_plana_bordado`: >6 dominantes al 99.5% de cobertura =
  FAIL). Calibración: las fuentes planas reales p070/p071 miden
  5 y 4 dominantes; un arte DTG a todo color mide cientos. La
  verificación de todo arte bordado corre con `--metodo bordado`
  además de los gates de siempre.
  **Contornos LISOS, tipo vector (corrección del dueño 2026-10-26):**
  plano no alcanza — la silueta debe ser la de un dibujo normal,
  con bordes limpios y suaves. **Aplanar/posterizar un arte
  texturizado NO produce una fuente válida:** conserva el contorno
  tembloroso del hilo en versión sutil y el diseño «se ve raro»,
  ni plano ni bordado. Si el concepto nació texturizado, la fuente
  se **regenera como ilustración plana de contornos lisos** (misma
  composición) y se cuantiza a los colores exactos (≤6). Una
  fuente con silueta temblorosa o bordes de hilo es FAIL de esta
  puerta, adjudicable a ojo sobre el PNG final.
- **Estilo declarado, independiente del método (corrección del
  dueño 2026-10-26):** cada diseño declara su `estilo` en la ficha
  y el método NO lo dicta. Un diseño de impresión (dtg) nace como
  gráfico de impresión — ilustración impresa, tipografía de
  póster, vintage impreso — y **nunca con look bordado, puntadas
  ni parche cosido**, salvo que su concepto declare «parche» como
  estilo buscado y la ficha lo justifique: el sesgo de un lote (el
  tema o el método de los diseños vecinos) no contagia la estética
  de un diseño. Un bordado nace plano y liso por su regla, no por
  «verse bordado».
- **Brief de generación:** el prompt pide la zona explícita con el
  resto de la composición completa y cerrada; el gate de composición
  sigue aplicando igual. Y si el diseño trae elementos que se leen
  blancos (pelaje, nieve), el prompt los exige **sombreados en crema o
  gris, nunca blanco puro**: `limpiar-fondo` se come el blanco puro
  también cuando es diseño (PIL-02 v1 perdió el gorro así; v2 con el
  pelaje sombreado pasó limpia).
- **Orden de proceso (verificado 2026-10-20):** cualquier resize va
  ANTES de `limpiar-fondo`/`limpiar-counters` y con **alfa
  premultiplicado** — el Lanczos directo sangra el blanco de los
  píxeles transparentes y recrea la película en los counters después
  de limpios.
- **El motivo, íntegro:** los elementos del oficio (estetoscopio y
  demás) se dibujan completos y conectados con la composición — nunca
  fragmentos sueltos ni piezas partidas (corrección del dueño
  2026-10-20: un estetoscopio roto delata generación sin criterio ante
  quien lo usa a diario). Se verifica por inspección visual del arte
  final antes de la entrega.
- **Diseño personalizable = diseño NUEVO y único.** Nunca se convierte
  ni se copia un diseño que vive en un MPL (duplicado penalizado por
  Etsy aunque uno sea personalizable — regla 2026-10-16/19).
- **Puerta visual de personalización:** ningún draft personalizable se
  reporta "listo" sin inspección visual de las capturas del editor con
  el ejemplo del concepto puesto (y su peor caso): nombre centrado en
  su zona con márgenes, dato pegado sin solapar, tamaños proporcionales.
  Los números de un worker no bastan (puerta aprendida 2026-10-18).

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

- (2026-10-30, decisiones de mejora del dueño sobre p087–p091:
  «dentro del hueco de la R se nota mal quitado el fondo blanco»,
  «fondo de algunas letras queda blanco») **Regresión de limpieza
  de fondo con la puerta en PASS.** Causa medida, en tres patas:
  (1) **Ruta:** los lotes recientes (p082–p101, 2026-10-28/29) se
  procesaron con cadenas improvisadas («upscale premultiplicado →
  limpiar-fondo global», limpiezas dirigidas hueco a hueco)
  en vez de la vía canónica `procesar-arte-propuesta.py` de la
  era buena (p058–p067, notas uniformes «PASS completo»); el
  procedimiento numerado no nombraba esa vía como obligatoria
  (vivía en una sección lateral) y la reescritura F1 de la
  vitrina en vivo (v0.9.0) rehízo la entrega sin tocar el
  proceso — la técnica no se borró de ningún archivo (limpiar-
  fondo intacto desde 2026-10-15, gates de limpieza desde
  2026-10-20, procesar desde 2026-10-17), se dejó de INVOCAR.
  (2) **Adjudicación encogida:** el paso 2c se aplicó a los
  componentes DUROS (veredictos registrados: diafragma de p098,
  counters de p100), pero los SOSPECHOSOS de cada arte (2–11 por
  arte) se cerraron en las notas como «no bloqueantes», sin zoom
  ni veredicto — y ningún paso exigía el zoom de counters sobre
  fondo oscuro por arte. (3) **La clase cambió de forma:** la
  franja actual es teñida y fina (anillo media ~208/227/230 en
  el counter de la R de p091, verificado en zoom contra el
  counter limpio de p058): no es blanco puro (gate 8 no la ve),
  su densidad de anillo es ~0.1 (gate 13 exige ≥0.25) y su
  grosor <13 (sospechoso a lo sumo). Medición de descarte: sobre
  19 artes reales, blanco puro / blanco interior / componentes
  encerrados / franja fina puntúan al bueno p058 igual o peor
  que a los malos — ninguna métrica de píxeles separa esta
  clase en arte ilustrado (misma conclusión del barrido de
  2026-10-20 para componentes). Corrección en v0.14.0: paso 1c
  (ruta obligatoria), 2c extendido a sospechosos, 2d nuevo
  (zoom de franja siempre, con `revision_franja` registrada) y
  `zonas_adjudicacion` + `gate_humano_pendiente` endurecidos en
  la salida de la puerta. Los artes ya entregados con la franja
  (p082–p101 pendientes y los `mejorar` p087–p091) se corrigen
  REGENERANDO/REPROCESANDO por la ruta canónica en su unidad de
  recogida/regeneración — no se parchan en la vitrina.

## Entrega para aprobación del dueño (flujo v2, 2026-10-19; superficie ÚNICA: la vitrina, corrección del dueño 2026-10-22)

Un PASS de esta puerta NO va directo a producción: va primero
al dueño, **por diseño**, por UNA SOLA superficie: **la vitrina
de revisión de la tienda**. El chat ya NO es superficie de
aprobación en esta fase (era el flujo anterior a la vitrina;
el dueño lo retiró el 2026-10-22: las propuestas por chat
dispersaban la revisión y llenaban el chat de artes). Sin
aprobación del dueño registrada en el checkpoint
(`data/tiendas/<tienda-id>/estado-propuestas.json`, vía la
recogida), el diseño no entra a producción (flujo v2 en
`FLUJO-PIPELINE.md`).

**La entrega, paso a paso** (flujo en vivo desde 2026-10-26,
decisión del dueño: la vitrina lee el repo — no hay paquete ni
siembra; contratos en `docs/VITRINA-VIVA.md`):

1. **El porqué completo vive en el registro.** La entrada del
   diseño en el registro de la tienda ya trae, al entregar, el
   arte y su **porqué completo**: tema y ángulo según la
   directriz vigente, la frase y su sentido, la iconografía y
   por qué esos elementos (qué significan en el tema; p. ej.
   qué es propio de la temporada y qué sería de otra), y
   **qué mirar**: los puntos que la puerta declara pendientes
   del ojo humano (counters/agujeros de las letras, trazos que
   llegan al borde adjudicados como motivo) y cualquier duda
   honesta del generador. Si el porqué no está completo en el
   registro, la entrega se detiene: se completa en la fuente,
   no al mostrar.
2. **Producir las previas como entregable en el repo** con
   `scripts/producir-previas-vitrina.py --tienda <id>
   --slugs <lote>`: compone las previas deterministas desde el
   PNG de producción, las deja en su hogar declarado
   (`data/tiendas/<tienda-id>/propuestas/<slug>/`) y declara en
   la entrada del registro sus `dimensiones_px` y su bloque
   `vitrina` (rutas de previas + `arte_ref`). En
   personalizables es además la puerta mecánica: sin
   simulación o sin ficha completa, **falla** y no produce
   nada. Una regeneración vuelve a correrlo con el arte nuevo:
   la previa servida es siempre la del `arte_ref` vigente.
3. **Registrar la entrega en el estado y commitear todo en la
   misma corrida:** los slugs del lote quedan en
   `entregados` (y en `lote_actual`) de
   `data/tiendas/<tienda-id>/estado-propuestas.json`, y el
   ciclo escribir = commitear
   (`scripts/registros-datos.py commit`) sube al repo de datos,
   en un solo commit, registro + estado + previas. **Puerta de
   forma (2026-10-28, incidente «vitrina en cero»):** ANTES de
   commitear se corre
   `python3 scripts/verificar-estado-entrega.py --shop <id>` —
   comprueba que `lote_actual.entregados` nombre exactamente el
   lote y que cada entregado traiga su bloque `vitrina`
   completo; en FAIL la entrega NO cierra (la corrida que
   entregó p072–p081 omitió `entregados` y la vitrina derivó
   cero con el lote íntegro en el repo). Con ese
   commit el diseño **ya está en la vitrina**: la instancia
   (una por tienda, declarada en `vitrina` del `config.json`)
   lo deriva al abrir, sin siembra ni edición de la instancia.
   **Verificación sobre la superficie viva:** tras el commit,
   la entrega se verifica contra la bandeja que la instancia
   deriva de verdad (su lectura/tab­lero), no solo contra el
   repo; si esa lectura no está disponible para la corrida, la
   verificación se declara PARCIAL en la entrega — nunca «OK»
   (corrección del mismo incidente: verificar el dato no es
   verificar la superficie).
   Si tras el commit la vitrina mostrara diseños que esta
   entrega no produjo — en particular diseños ya aplicados que
   reaparecieran como pendientes — sería un defecto de
   derivación de la superficie (la bandeja se deriva del
   estado, no se administra): se reporta y se corrige la
   derivación primero; no se avisa al dueño a decidir sobre
   ellos ni se recogen como decisiones nuevas.
4. **Avisar al dueño en el chat de entrega** (según
   `docs/REGLA-DELIVERY-CHATS.md`): un aviso breve — qué lote
   es, cuántos diseños trae y **el acceso a la vitrina** (su
   tarjeta) — **SIN adjuntar artes ni porqués en el chat**:
   todo eso vive dentro de la vitrina y ahí se revisa.
5. **El dueño decide en la vitrina** (sus decisiones se
   escriben al instante en el registro de decisiones de la
   tienda, en el repo — esa escritura ES la decisión vigente;
   desde U1 2026-10-26 no hay marca posterior) y avisa en un
   chat cuando quiere; la recogida-aplicación al checkpoint
   sigue la sección «Recogida-aplicación de decisiones
   (vitrina en vivo)» de este skill.

El porqué se escribe al generar (sale de la directriz y del
brief del diseño, no se inventa al entregar) y se guarda en el
registro del diseño (`porque` en `data/tiendas/<tienda-id>/registro-listings.json`)
para que lo hereden la producción y el paquete comercial.

### Variante personalizable (2026-10-20, pedido del dueño)

El arte personalizable llega con las zonas VACÍAS: solo con eso el
dueño no puede juzgar el resultado. La entrega trae **dos imágenes**:

- **El arte real** — el PNG de producción, con las zonas vacías tal
  cual entrará a Printify.
- **La SIMULACIÓN** — el resultado esperado: un compuesto
  determinista **sobre el arte real** (nunca una generación paralela:
  la referencia se deriva del arte verdadero) con el **ejemplo derivado
  del concepto** colocado en cada zona según su geometría medida — el
  dato que un comprador real pondría en ESE diseño, con su formato
  real (ver "Formato profesional real" en los criterios: la
  referencia de nicho declarada en la ficha de la tienda), y una foto
  de muestra en el marco si el diseño lleva imagen. Se entrega
  declarada como simulación: aproxima la tipografía y el color de la
  capa prevista; el render definitivo es el mockup del draft en la
  revisión de Printify. (El comodín único "Maria / RN - ICU" de la
  primera prueba quedó RETIRADO el 2026-10-20: era un ejemplo casual
  del dueño aplicado sin criterio — cada concepto trae el suyo.)

Y el porqué de un personalizable trae su **ficha de razón completa**
(ver "Diseños personalizables — criterios"): razón en una frase,
prueba de borrado en dos estados (vacío / con el ejemplo), campos con
tipo y límites, comprador/destinatario/ocasión, clase de encaje y el
peor caso renderizado. Y declara además, explícito:

**Dónde vive en el sistema (cierre de vitrina, 2026-10-22):** la
entrada del diseño en el registro de la tienda declara
`personalizable: true`, `simulacion` (ruta repo-relativa del PNG de
la simulación, compuesto sobre el arte real — la FUENTE misma, en
todo método), `metodo`
(`"dtg"` o `"bordado"` — declarado en TODA propuesta, personalizable
o no, desde la recalibración 2026-10-26) y `ficha_razon` (objeto
estructurado: `razon`, `estilo` — la dirección de arte declarada
del diseño, independiente de su método —, `prueba_borrado`, `campos` — cada uno con
`nombre`, `tipo` y, según el tipo, `limite` u `opciones`, más su
`ejemplo`, su `fuente` y su `color` (la tipografía declarada de
ese texto, ver «Canon de fuentes») —, `comprador_destinatario_ocasion`, `clase_encaje`,
`ejemplo_simulacion`, `peor_caso`, `producto_destino`,
`plan_zonas`). El script de entrega
(`scripts/producir-previas-vitrina.py`) es la puerta mecánica de esta
entrega: sin simulación válida o sin ficha completa, la producción
de previas FALLA — el diseño nunca llega a la bandeja disfrazado de
normal, y la vitrina lo muestra con sus dos imágenes etiquetadas y
su sección «Ficha de personalización» (contrato:
`docs/VITRINA-VIVA.md`, variante personalizable).

### Canon de fuentes de personalización (2026-10-26, corrección del dueño)

El texto personalizable NO se compone con «una fuente cualquiera»:
cada campo de la ficha declara su `fuente` y su `color`, el dueño
aprueba esa tipografía con la propuesta, y la composición — la
simulación primero y el pedido real después — usa exactamente lo
declarado. El dueño no coloca textos pedido a pedido: aprueba la
ficha una vez y el sistema compone desde ella de forma
determinista. Fuentes canónicas (archivos en
`assets/fuentes/` de este skill, licencias abiertas):

- **Dancing Script** — manuscrita cálida: nombres y frases con
  carácter (la firma personal del diseño).
- **Oswald** — titular condensada en mayúsculas: credenciales,
  unidades, años (lo institucional, legible de lejos).
- **Montserrat** — sans limpia: textos neutros o secundarios.

Un diseño puede declarar una fuente propia fuera del canon si su
concepto la pide; entonces el archivo se suma a `assets/fuentes/`
con su licencia y la ficha la nombra. La simulación renderiza los
ejemplos con la fuente y el color DECLARADOS de cada campo (no
con una genérica), y el ejemplo tiene el carácter del concepto —
un nombre con su credencial se lee como una credencial real, no
como un texto de relleno: un ejemplo básico desinfla la propuesta
y es defecto de la entrega, no un detalle.

- **Producto destino** (el que la estratega fijó en el config de
  propuestas — al aprobar el arte, el dueño aprueba diseño +
  producto + plan de zonas junto).
- **Plan de zonas:** qué dato va en cada zona, con sus límites de
  caracteres y, si una decisión es cerrada, su dropdown.
- Qué mirar: cómo se lee cada zona vacía vs. llena en la simulación,
  contraste del dato sobre la prenda más clara, y si la composición
  sigue cerrando con el dato puesto.

## Recogida-aplicación de decisiones (vitrina en vivo) — 2026-10-26, sin marca desde U1 (2026-10-26)

**Dónde vive y por qué.** Esta recogida es el cierre de ESTA
puerta — la misma que entrega —, no un flujo nuevo: consume el
mismo checkpoint que la Fase B y la decide el mismo dueño. Por
eso vive como sección de este skill y no como skill aparte: un
skill separado fragmentaría la puerta entre dos dueños, y la
Fase B seguiría apuntando aquí. Los contratos de la vitrina en
vivo (lectura, decisiones, UX) viven en `docs/VITRINA-VIVA.md`;
**este es el procedimiento operativo de recogida-aplicación**
y manda sobre cualquier descripción resumida de aquel doc.

**La fuente ya no es la instancia: es el repo.** Las decisiones
del dueño viven en el registro de decisiones de la tienda,
`data/tiendas/<tienda-id>/vitrina/decisiones.json` (append-only;
la vitrina lo escribe al instante con el conector, un commit
por decisión — ruta C del Centro de My Channels). Cada
decisión trae `{id, fecha, slug, accion
(aprobado|rechazado|mejorar|retirar), nota, estado
(vigente|aplicada|devuelta), fecha_lista,
commit_aplicacion}`. **Decisión vigente** = la última entrada
registrada para un slug que no esté `aplicada` ni `devuelta`
y cuya `accion` no sea `retirar` (si la última es `retirar`,
no hay decisión vigente para ese slug). **Compatibilidad hacia
atrás (U1):** las entradas históricas con `estado` `sin-marcar`
o `lista` se leen e interpretan exactamente como `vigente`;
`fecha_lista` es un dato histórico ignorado, no un error ni un
requisito, y ninguna escritura nueva lo produce. Recoger =
**aplicar**: leer las decisiones **vigentes**, mover el estado
y el registro con las validaciones de esta sección, y marcar
cada decisión `aplicada` (o `devuelta` si una validación la
rechaza, con su causa en la nota de aplicación) con el
`commit_aplicacion` del commit que la aplicó. No existe
confirmación hacia la superficie: la bandeja se deriva del
repo, así que lo aplicado deja de verse pendiente por
derivación, no por purga.

**Disparador.** El dueño avisa en un chat — cualquier aviso
suyo basta (p. ej. «recoge las decisiones de la vitrina de
<tienda>»). **No se exige la frase exacta:** cualquier mensaje
suyo, en cualquier forma (texto o audio), que indique que ya
decidió en la vitrina ES el aviso y dispara la recogida (regla
del disparador libre, vigente desde v0.8.4; caso fundacional
2026-10-22: avisó por audio y la recogida corrió). Sin aviso
NO hay aplicación: una decisión vigente por sí sola no dispara
nada y la vitrina no notifica a nadie. No existe botón de
marca ni recibo copiable (retirados en U1, 2026-10-26: la
marca era compensatoria de la vitrina sembrada; con la
escritura al instante en el repo, su contexto murió).

**Cruce obligatorio antes de reportar estados.** El checkpoint
NO conoce las decisiones vigentes del dueño que aún no se
aplicaron. Antes de reportarle conteos de aprobados / mejorar
/ rechazados de un lote, cruza con el registro de decisiones
de la tienda (tras el `pull` del paso 1): lo decidido se
reporta como «decidido en la vitrina, pendiente de
aplicación» — nunca se le repiten los conteos viejos como si
su decisión no existiera (mismo caso fundacional: el sistema
le siguió diciendo «uno en mejorar» horas después de que él
ya había aprobado la nueva versión en la vitrina).

**Instancia.** Una sola vitrina por tienda, declarada en el
bloque `vitrina` del `config.json` de la tienda
(`data/tiendas/<tienda-id>/config.json`, campo `artefacto`).
Si la tienda no declara su instancia, la recogida se detiene y
reporta el hueco — nunca se adivina un slug ni se reutiliza la
instancia de otra tienda. (Cada tienda declara la suya en su
propio config; ninguna instancia se comparte entre tiendas.)

**Procedimiento.**

1. **Traer el repo y leer** el registro de decisiones de la
   tienda: primero `scripts/registros-datos.py pull` (la
   vitrina commitea directo en el repo de datos; el pull baja
   sus commits y los sincroniza al árbol físico), después
   leer `data/tiendas/<tienda-id>/vitrina/decisiones.json`.
   De cada decisión interesa: `slug`, `accion`
   (`aprobado|rechazado|mejorar|retirar`), `nota`, `estado` y
   `fecha`. (`fecha_lista`, si una entrada histórica la trae,
   se ignora.) Un veredicto nuevo sobre el mismo diseño
   **reemplaza** al anterior — manda el último: el registro
   conserva todos (es append-only) y se aplica solo el
   vigente, el último no aplicado para ese slug.
2. **Filtrar:** solo se aplican las decisiones **vigentes**
   (definición arriba): la última entrada por slug, no
   `aplicada` ni `devuelta`, con `accion` en
   `aprobado|rechazado|mejorar`. Las entradas históricas con
   `estado` `sin-marcar` o `lista` cuentan como vigentes en
   igualdad de condiciones — ninguna decisión vigente se
   descarta por no llevar marca. Una entrada `retirar` como
   última de su slug significa «sin decisión vigente»: no se
   aplica nada para ese slug.
3. **Validar ANTES de escribir** — si algo falla, se detiene
   todo y se reporta; nunca se escribe a medias:
   - Cada slug filtrado existe en el registro de la tienda
     (`data/tiendas/<tienda-id>/registro-listings.json`) y en
     el checkpoint (`data/tiendas/<tienda-id>/estado-propuestas.json`).
   - Los conteos cuadran: total de filtradas = aprobadas +
     rechazadas + mejorar de esta recogida.
   - **Idempotencia:** una decisión ya `aplicada` o `devuelta`
     no se reaplica jamás; y un slug que ya está en
     `aprobados`, `mejorar` o `rechazados` del checkpoint por
     una recogida anterior se excluye y se reporta como ya
     recogido. Jamás se duplica su entrada ni se reescribe
     (una entrada de `mejorar` puede llevar trabajo posterior
     — p. ej. su bloque de regeneración — que no es de esta
     recogida). Si tras excluir no queda nada nuevo, la
     recogida termina aquí: se reporta «nada nuevo por
     recoger» y no se escribe nada.
     **Excepción — decisión sobre una nueva versión:** si la
     mejora ya se cumplió (su entrada se movió a
     `mejoras_cumplidas` al entregarse la regeneración, ver
     §«Retorno de una mejora») y existe una decisión vigente
     posterior sobre ese slug, esa decisión es NUEVA: se
     procesa con normalidad y su entrada se escribe en el
     array que corresponda, sin que la historia en
     `mejoras_cumplidas` la bloquee.
4. **Escribir** en el checkpoint
   `data/tiendas/<tienda-id>/estado-propuestas.json`
   (desde 2026-10-26 es un registro versionado de la tienda,
   no un checkpoint local: se commitea con
   `scripts/registros-datos.py commit`):
   - `aprobado` → array `aprobados`, agregando
     `{slug, fecha_aprobacion}` — `fecha_aprobacion` = la
     fecha en que el dueño decidió (`fecha` de la decisión,
     en formato `YYYY-MM-DD`; la decisión se escribe al
     instante, así que esa es su fecha real — no hay fecha de
     marca).
   - `rechazado` → array `rechazados`, agregando
     `{slug, fecha_decision, motivo}` — `fecha_decision` con
     la misma regla de `fecha`; `motivo` = la nota del dueño
     si la dio, si no `null`. Un rechazado no entra jamás a
     `aprobados`, `mejorar` ni `producidos`.
   - `mejorar` → array `mejorar`, agregando
     `{slug, nota, fecha_decision, estado: "esperando_regeneracion"}`
     — `fecha_decision` con la misma regla de `fecha`.
   - Bloque `recogida_vitrina` (reemplaza al anterior; es el
     registro de la ÚLTIMA recogida): `{fecha_recogida,
     fecha_envio_dueno, lote_fecha, tienda_id, total,
     aprobados, mejorar, rechazados, fuente}` — conteos de
     ESTA recogida; `fecha_envio_dueno` (nombre histórico del
     campo) = la mayor `fecha` de las decisiones aplicadas;
     `fuente` = `vitrina/decisiones.json (repo de datos)`.
   - **Y en el mismo acto, el `estado` de cada diseño
     recogido en el registro** (`registro-listings.json` de
     la tienda) — aprobado / mejorar / rechazado, con la
     fecha de la decisión — y la marca de cada decisión en
     `vitrina/decisiones.json` (`aplicada` +
     `commit_aplicacion` = el commit del propio
     `registros-datos.py commit` que cierra este paso; si el
     hash se conoce recién al commitear, se escribe en un
     segundo commit inmediato del mismo acto, solo sobre
     `decisiones.json`). Registro, checkpoint y decisiones
     NUNCA quedan discrepando: el watchdog cruza los tres, y
     una aprobación que solo vive en uno se lee como trabajo
     perdido (hueco fundacional: la recogida del 2026-10-22
     solo escribió el checkpoint y el watchdog alertó esa
     noche; los estados se alinearon a mano y esta regla lo
     cierra).
5. **Verificar por relectura:** con el commit pusheado,
   releer el `decisiones.json` del repo de datos (o el árbol
   físico sincronizado) y confirmar que cada decisión
   aplicada quedó marcada y que la bandeja derivada ya no la
   ofrece como pendiente. Sin esta relectura no se reporta
   éxito: un guardado no verificado no es un guardado.
6. **Reportar al dueño en el chat donde avisó:** conteos por
   resultado, qué quedó registrado y qué sigue (la Fase B
   produce solo los `aprobados` registrados, con la palabra
   que el flujo exija; los `mejorar` se regeneran solo en lo
   que pide su nota). La recogida NO produce drafts, NO
   publica y NO entrega nada nuevo a la vitrina.

**Modo lectura (dry-run).** Si el dueño pide revisar sin
recoger — o ante cualquier duda sobre el estado — se ejecutan
solo los pasos 1–3 y se reporta qué se aplicaría (o que no hay
nada nuevo), sin escribir nada.


## Retorno de una mejora (regeneración → nueva versión en la vitrina) — 2026-10-22

El ciclo de un `mejorar` se cierra cuando su nueva versión está
**visible de verdad** en la vitrina, no cuando el arte nuevo
existe en disco. Procedimiento (caso fundacional: p063 v2,
cerrado el 2026-10-22):

1. **Regenerar solo lo pedido** por la nota del dueño, por la
   misma ruta calibrada del lote original. Sin su palabra no
   se regenera nada.
2. **Verificar el arte nuevo** antes de mostrarlo: puerta
   mecánica completa y adjudicación con el ojo. Si la puerta
   marca `sin_counters_rellenos` porque el cambio MISMO es un
   fondo de diseño (el caso p063: el disco crema del medallón),
   el veredicto se registra en el registro del diseño
   (`adjudicacion_counters…`: es diseño, no limpiar) y se sigue.
3. **Actualizar el registro del diseño:** su `arte` apunta a
   la nueva versión y el bloque de regeneración guarda motivo,
   cambio y verificación (diff acotado a la zona pedida).
4. **Producir las previas de la nueva versión (requisito
   duro):** correr `scripts/producir-previas-vitrina.py` con
   el arte NUEVO ya apuntado en el registro (paso 3): las
   previas del hogar del diseño se recomponen desde ese arte
   y el bloque `vitrina` de la entrada declara el `arte_ref`
   nuevo. La vitrina sirve siempre la previa del `arte_ref`
   vigente, así que mostrar el arte viejo como «Nueva
   versión» es imposible por construcción — no por cuidado
   del operador. (Hueco fundacional del flujo de siembra: las
   previas eran estáticas por slug dentro de la instancia y
   la siembra habría mostrado el arte viejo; la resolución
   por `arte_ref` se publicó el 2026-10-22 y este paso la
   vuelve estructural.)
5. **Commitear y verificar por relectura:**
   `scripts/registros-datos.py commit` (registro + previas +
   checkpoint del paso 6 en un solo commit), y recién con el
   commit en el repo, verificar que la bandeja derivada
   muestra el diseño pendiente, marcado «Nueva versión», con
   la previa del arte nuevo y la nota anterior presente.
   Nunca se avisa al dueño sin esa verificación: el retorno
   no está completo hasta que la imagen nueva es la que la
   vitrina sirve de verdad.
6. **Checkpoint:** la entrada del diseño se mueve de `mejorar`
   a `mejoras_cumplidas` (conservando nota, fechas y bloque de
   regeneración, más el cumplimiento: fecha de entrega, arte
   nuevo y verificación). Así, la decisión que el dueño tome
   sobre la nueva versión es una decisión nueva para la
   recogida (ver la excepción de idempotencia en
   §«Recogida-aplicación de decisiones (vitrina en vivo)»
   paso 3).
8. **Avisar al dueño en el chat de entrega** con el acceso a
   la vitrina (sin artes en el chat, como manda la entrega).
