# Vitrina de revisión de propuestas — EN VIVO (contrato del sistema)

**Qué es.** La superficie donde el dueño ejerce la puerta creativa de
la Etapa 1 del flujo v2 (ver `FLUJO-PIPELINE.md` §1): una página
organizada, pensada primero para el teléfono, donde cada propuesta se
revisa con su arte y su porqué, y la decisión se guarda **como dato en
el repositorio de datos** — no como mensajes sueltos en un chat ni como
filas en una base de datos de la superficie.

**El motor (desde 2026-10-26, decisión del dueño):** la vitrina **lee
en vivo** el repo de datos de la aplicación (`ChrisBP-Dev/my-pod-datos`)
con el conector de GitHub declarado, y su única escritura es el
registro de decisiones de la tienda, en ese mismo repo. No hay
paquete, no hay siembra, no hay base de datos propia con estado de
revisión: la bandeja se **deriva** del repo en cada apertura. Es el
mismo patrón del Centro de gestión de My Channels (contrato
`CENTRO-GESTION-VIVO.md` de esa app, ruta C de decisiones), aplicado a
esta puerta. Plan y auditoría que lo originan:
`docs/PROPUESTA-VITRINA-LECTURA-EN-VIVO.md`.

**Estado:** contrato vigente desde su fusión. La presentación es la
plantilla v2.3 aprobada por el dueño (sus §§ de UX se conservan
abajo); la plantilla sembrada anterior (`docs/VITRINA-REVISION.md`)
queda como historia.

## Principios de UX (los de la plantilla v2.3, no negociables)

1. **Móvil primero, desktop con su ancho.** En el teléfono: una columna,
   el arte manda. En desktop: parrilla de tarjetas (2–3 por fila) y el
   detalle en dos columnas (arte | información y decisión).
2. **Pocas cosas, bien ordenadas.** Una sola jerarquía por pantalla:
   arte → título y etiquetas → porqué en secciones → decisión. Nada de
   tableros cargados ni datos duplicados en dos lugares.
3. **Progreso siempre visible.** Encabezado fijo con el conteo
   (revisados / total) y su barra; el dueño sabe en todo momento
   cuánto falta.
4. **Decidir cuesta un toque.** La decisión se guarda al instante, sin
   botón de «guardar» global ni formularios. Cambiar de opinión es
   volver a tocar: la última decisión es la que vale.
5. **El arte se juzga como se va a usar.** Cada diseño trae dos vistas
   previas deterministas compuestas desde el PNG de producción: sobre
   fondo oscuro y sobre fondo claro (las prendas reales), con un
   conmutador en el detalle. Nunca una regeneración «parecida».
6. **Sin celdas vacías ni datos huérfanos.** Todo lo que la puerta
   declara (porqué, qué mirar, nota de la puerta) vive dentro de la
   tarjeta del diseño; ningún archivo adjunto sustituye la
   presentación.
7. **La tarjeta no decide; el detalle decide.** La lista es para
   navegar: tarjeta = arte completo + título + descripción breve +
   etiquetas + estado, y se entra tocándola. Los botones de decisión
   viven solo en el detalle (el flujo de revisión es de a uno).
8. **El arte nunca se recorta en pantalla.** Tarjeta, detalle y visor
   muestran el diseño COMPLETO (ajuste «contain», mismo margen y
   fondo en todas), fiel al recorte real del archivo — un encuadre
   que corte el diseño falsea la evaluación del recorte.
9. **Nada bloquea a nada.** La vitrina es una bandeja continua: los
   lotes se suman, las decisiones conviven y todo sigue editable
   mientras el diseño esté en la vitrina. No hay «cierre de lote» ni
   requisito de cero pendientes para que entre trabajo nuevo.

A estos se suma, propio del motor en vivo:

10. **La superficie lee la realidad y lo dice.** Cada apertura fija el
    HEAD del repo, deriva de él y muestra el sello «Leído en vivo ·
    commit `<sha-corto>`». Si una lectura falla, la vista lo muestra
    fallido con su causa; jamás sirve una copia vieja como si fuera
    la realidad, y jamás inventa un dato que su fuente no trae: si
    falta un entregable (una previa, un campo), el hueco se nombra
    en la vista y se corrige en el flujo que lo produce.

## Flujo de uso

1. **Entrega (el flujo):** con un lote en PASS de la puerta de arte,
   el flujo produce las previas en su hogar del repo y registra los
   entregados en el estado de la tienda, commiteando todo en la
   misma corrida (procedimiento exacto: `puerta-arte-propuesta`
   §«Entrega para aprobación del dueño»). No hay acción de entrega
   sobre la vitrina: al abrir, el diseño entregado simplemente
   **está**, derivado del estado.
2. **Revisión (el dueño):** entra a la vitrina — la vista inicial es
   **Pendientes** (no hay vista «todas»: la lista se va limpiando a
   medida que decide; las demás vistas son aprobadas / rechazadas /
   por mejorar, para consultar lo ya decidido y cambiar de opinión
   cuando quiera) —, abre cada diseño, lee su porqué, alterna el
   fondo con el control segmentado etiquetado «Fondo: Oscuro /
   Claro» (estado activo inconfundible en ambos modos), inspecciona
   el arte en el visor con zoom focal (acotado, sin cierre por
   gestos) y decide en el detalle: **Aprobar**, **Rechazar** o
   **Mejorar** (con nota de qué mejorar; la nota también es
   bienvenida en un rechazo). Cada decisión se escribe al instante
   en el repo (ver §Decisiones), con su estado de escritura visible:
   escribiendo → guardada, o fallida con su causa (nunca dada por
   guardada). **No hay paso posterior de envío ni de marca**
   (U1, 2026-10-26): la decisión escrita al instante YA es la
   decisión vigente, lista para su recogida-aplicación en cuanto
   el dueño avise en un chat — sin botón «Marcar listas», sin
   recibo copiable y sin estado `lista` como requisito. Todo
   sigue editable mientras no se aplique: cambiar de opinión
   escribe una decisión nueva que reemplaza a la anterior como
   vigente.
3. **Recogida-aplicación (Jarvis):** con cualquier aviso del
   dueño en un chat, sigue el procedimiento operativo exacto de
   `skills/puerta-arte-propuesta/SKILL.md` (§«Recogida-aplicación
   de decisiones (vitrina en vivo)»): lee las decisiones
   **vigentes** del repo (ver §Decisiones), las aplica con sus
   validaciones e idempotencia sobre el estado y el registro, y
   marca cada decisión `aplicada` con su commit. La Fase B
   produce **solo** lo aprobado. Nada se produce desde la
   vitrina.

## Lectura — qué lee la instancia y cómo deriva la bandeja

La instancia declara el conector de GitHub con lectura y escritura
acotado **solo al repo de datos**. Por apertura:

1. Fija el HEAD de la rama con `list_commits`.
2. Lee, contra ese commit, SOLO estos archivos de SU tienda
   (declarada en §Instalación): `config.json`,
   `registro-listings.json`, `estado-propuestas.json` y
   `vitrina/decisiones.json`. Lista blanca de campos por diseño:
   `titulo`, `tema`, `track`/`tipo`, `fecha_propuesta`, el porqué
   (que el servidor parte en sus secciones por sus marcadores
   canónicos — «Tema y ángulo:», «Frase:», «Iconografía:», «Qué
   mirar:» — sin reescribirlo), `nota_puerta`, `personalizable`,
   `ficha_razon`, `dimensiones_px` y el bloque `vitrina` (rutas de
   previas + `arte_ref`). Etiquetas y frase corta se derivan del
   porqué/tema con la misma lógica determinista que usaba el
   generador retirado. Nada más viaja.
3. Deriva la bandeja desde el estado y las decisiones, en este
   orden de verdad: un diseño está **en la bandeja** si el estado
   lo lista como entregado y ninguna recogida lo ha movido a
   aprobados/producidos/rechazados ni está en `mejorar` con su
   mejora aún sin cumplir. Su vista: **Pendientes** si no tiene
   decisión vigente; la vista de su decisión (aprobadas /
   rechazadas / por mejorar) si la tiene; **«Esperando
   regeneración»** si su decisión vigente es mejorar y ya fue
   aplicada; **«Nueva versión»** (de vuelta en Pendientes, con la
   nota de mejora anterior visible en su detalle) cuando su
   entrada pasó a `mejoras_cumplidas` y el flujo entregó el arte
   nuevo. Aprobados y rechazados aplicados **salen** de la
   bandeja por derivación. El vacío es un estado terminal
   legítimo: bandeja en cero = «todo decidido y aplicado», y la
   vista muestra «Sin pendientes» — no falta ninguna siembra.
4. Sirve las previas desde su hogar en el repo
   (`propuestas/<slug>/previa-oscura.jpg` y `previa-clara.jpg`;
   en personalizables también `simulacion-oscura.jpg` y
   `simulacion-clara.jpg`), con caché de bytes por SHA de blob:
   los bytes inmutables se cachean por contenido; los datos
   derivados se leen en vivo en cada apertura, jamás se cachean.
   La previa servida es siempre la declarada para el `arte_ref`
   vigente de la entrada; si el archivo declarado no existe en el
   repo, la tarjeta lo nombra como hueco («Previa no encontrada
   en el repo») en vez de mostrar otra imagen.

Presupuesto de lecturas por apertura: ~5 llamadas de texto +
las previas que cambiaron de SHA. Las lecturas independientes se
emiten en oleadas acotadas (una ráfaga grande recibe 429 del
conector: el paralelismo tiene techo y se respeta).

## Decisiones — la única escritura de la instancia

El registro: `data/tiendas/<tienda-id>/vitrina/decisiones.json`,
una lista append-only. Cada entrada:

```json
{"id": "p058-2026-10-26T15:04:11-04:00",
 "fecha": "2026-10-26T15:04:11-04:00",
 "slug": "p058",
 "accion": "aprobado|rechazado|mejorar",
 "nota": "texto libre del dueño o cadena vacía",
 "estado": "vigente",
 "fecha_lista": null,
 "commit_aplicacion": null}
```

**Vocabulario de `estado` (U1, 2026-10-26).** Una decisión nueva
nace `vigente`: escrita al instante, aún no aplicada. La
recogida-aplicación la pasa a `aplicada` (o `devuelta` si una
validación la rechaza, con su causa). **Compatibilidad hacia
atrás:** las entradas históricas con `estado` `sin-marcar` o
`lista` se leen e interpretan exactamente como `vigente` — la
marca (`lista` / `fecha_lista`) es un dato histórico que se
ignora, nunca un error ni un requisito; ninguna escritura nueva
lo produce. **Decisión vigente de un diseño** = la última
entrada registrada para su slug que no esté `aplicada` ni
`devuelta` y cuya `accion` no sea `retirar`; si la última
entrada es `retirar`, el diseño no tiene decisión vigente.

- **Decidir = escribir al instante.** Al confirmar una decisión en
  el detalle, la instancia lee el registro vigente (creándolo si
  no existe), fusiona por `id` y escribe con **un solo commit**
  por el conector. No hay bandeja de guardado ni escritura en
  lote. Conflicto de SHA: relee, refusiona y reintenta **una**
  vez; segundo choque: error con causa y la decisión **no queda
  en pie** — la vista lo muestra fallido, nunca como guardado.
  Ritmo medido del patrón (Centro de My Channels): la escritura
  ronda los 13 s; la tarjeta muestra ese estado mientras tanto.
  Sin confirmación por relectura, nada se da por guardado.
- **Cambiar de opinión** escribe una decisión NUEVA para el mismo
  slug (otro `id`): manda la última registrada como vigente; las
  anteriores conservan su historia en el registro. No hay marca
  que rehacer: la nueva decisión vale desde que se escribe.
- **Sin marca ni recibo (U1, 2026-10-26).** No existe botón
  «Marcar listas», ni recibo copiable, ni acción `marcarlistas`:
  las acciones de la instancia son exactamente `getboard`,
  `sello` y `guardardecision` (ver §Acciones). La vitrina no
  produce, no publica, no toca Printify y **no notifica a nadie
  por sí sola**. La aplicación ocurre cuando el dueño avisa en
  un chat — cualquier aviso suyo, sin frase exacta (regla del
  disparador libre, `puerta-arte-propuesta` v0.8.4) — y la
  recogida lee las decisiones vigentes del repo en ese momento.
  Motivo: la marca era una decisión compensatoria de cuando las
  decisiones vivían solo dentro de la vitrina sembrada; con la
  lectura en vivo y la escritura al instante, su contexto murió.
- **La instancia jamás escribe otro archivo:** ni el registro de
  listings, ni el estado, ni el config. Los cambios sobre esos
  archivos los hace el flujo dueño (la recogida-aplicación), con
  sus validaciones, y quedan en el mismo repo como commits del
  sistema.

## Acciones de la instancia (contrato exacto, U1 2026-10-26)

Toda instancia de vitrina en vivo expone **exactamente** estas
tres acciones — ni una más:

- **`getboard`** — deriva y devuelve la bandeja desde el HEAD
  vigente del repo de datos (ver §Lectura).
- **`sello`** — comprobación ligera de solo-HEAD: devuelve el
  commit vigente sin releer la bandeja (ver §Pase de pulido).
  Es el nombre canónico en todas las instancias.
- **`guardardecision`** — escribe la decisión al instante en
  `vitrina/decisiones.json` (un commit por decisión). Acepta
  `aprobar` / `rechazar` / `mejorar` (con su nota) y `retirar`
  (ver Enmienda F3).

**Retirada en U1:** `marcarlistas` — sin botón en la UI, sin
recibo y sin efecto sobre la recogida. Una instancia que aún la
exponga está fuera de contrato.

## La entrega produce sus fuentes (contrato con el flujo)

La vitrina no inventa ni completa nada: lo que muestra nace en el
flujo que entrega, guardado en su lugar (`puerta-arte-propuesta`
§«Entrega» ejecuta; esto declara el contrato):

- **El porqué** vive en la entrada del registro, completo y con
  sus marcadores. La vitrina lo parte y lo presenta; no lo
  reescribe.
- **Las previas** son un entregable del paso de entrega:
  `scripts/producir-previas-vitrina.py` las compone desde el PNG
  de producción y las deja en
  `data/tiendas/<tienda-id>/propuestas/<slug>/`, declarando en la
  entrada `dimensiones_px` y el bloque `vitrina` con sus rutas y
  su `arte_ref`. Ese hogar es el único donde un medio se
  versiona: excepción acotada del dueño (2026-10-26) al «nunca
  medios en git», declarada igual en el `.gitignore` del repo de
  datos y en la clasificación de `scripts/registros-datos.py`. El
  PNG de producción sigue sin versionarse, como todo medio.
- **Personalizables:** la entrada declara `personalizable: true`,
  `simulacion` y `ficha_razon` completos (contrato de la puerta).
  Sin simulación o sin ficha, la producción de previas FALLA y el
  diseño no llega a la bandeja disfrazado de normal. El detalle
  muestra arte real y simulación etiquetados («Arte real — zonas
  vacías» / «Simulación — con el ejemplo») bajo el mismo
  conmutador de fondo, y la sección «Ficha de personalización»
  con la ficha completa.

## Instalación — una instancia por tienda, multitienda por diseño

La vitrina **no se crea por lote ni por día**: existe **una sola
instancia por tienda**, y lo que cambia es lo que el repo trae.
Crear instancias por corrida quemaría trabajo y multiplicaría
superficies. Para dar de alta la vitrina de una tienda nueva:

1. La tienda declara en su `config.json` el bloque `vitrina` con
   el slug de su instancia (sin esa declaración, nadie inventa el
   slug ni reutiliza el de otra tienda).
2. Se crea la instancia — una aplicación web **sin estado propio**
   (no guarda nada: lee y escribe el repo) — declarando el
   conector de GitHub con lectura y escritura **solo sobre el
   repo de datos**, y su tienda: `repo = my-pod-datos`,
   `ruta_tienda = data/tiendas/<tienda-id>`. La instalación de la
   app de GitHub selecciona solo ese repo.
3. El hogar de previas y el registro de decisiones nacen con la
   primera entrega y la primera decisión; ningún paso siembra
   contenido inicial. Una bandeja en cero al nacer es correcta.

**Costo por lote en este modelo:** la corrida del script de
previas (local, determinista) + un commit del puente. La
instancia no se edita por lote, no se siembra y no se confirma
nada en ella tras la recogida.

## Qué murió con este contrato (y dónde queda su historia)

- `scripts/generar-datos-vitrina.py` y el paquete
  `datos-vitrina.json` (contrato de entrada de la plantilla
  sembrada).
- Las acciones de la instancia sembrada: `seedlote`,
  `leerdecisiones`, `confirmarrecogida`, `setdecision`,
  `savenota`, `cleardecision`, `enviardecisiones`,
  `leerestadorevision` — reemplazadas por la lectura derivada y
  la escritura directa al repo.
- Las previas horneadas en el código de la instancia y la regla
  de siembra con su registro de retirados (la resurrección es
  imposible por construcción: no hay copia que resucitar).
- La acción `marcarlistas`, el botón «Marcar listas para Jarvis»
  y su recibo copiable (Enmienda U1, 2026-10-26).
- La historia completa del modelo anterior vive en
  `docs/VITRINA-REVISION.md` (plantilla v2.3) y en el CHANGELOG
  de `puerta-arte-propuesta`; este contrato conserva de aquella
  plantilla solo su presentación y su gestión, que son el piso.

## Enmienda F3 (2026-10-26) — lo que el ciclo de ensayo probó y corrigió

- **Acción `retirar` (paridad «Quitar decisión»):** `guardardecision` acepta
  `retirar`; se escribe al instante en `vitrina/decisiones.json` (desde U1 con
  estado `vigente`; en entradas históricas, `sin-marcar`), manda sobre la
  decisión vigente no aplicada del mismo slug, y la derivación la trata como
  «sin decisión vigente» (el diseño vuelve a Pendientes). La
  recogida-aplicación ignora las entradas `retirar` — su efecto ya ocurrió al
  escribirse: cancelan la decisión vigente anterior de ese slug.
- **Tienda de ensayo permanente:** `data/tiendas/ensayo-vitrina/` en el repo de
  datos es el fixture declarado de pruebas de la vitrina (NO es una tienda
  real; ningún flujo de producción la opera). La instancia de ensayo lee esa
  tienda; la de producción, la suya.
- **`vitrina/decisiones.json` es REPO-FIRST (regla dura):** lo escribe la
  vitrina en el repo; la copia física es solo caché de lectura. El puente
  `registros-datos.py` NUNCA lo espeja físico→repo: al commitear, primero hace
  pull (repo→físico) de ese archivo. Motivo (incidente F3, 2026-10-26): el
  commit de investigación semanal espejó la copia física vieja (`[]`) sobre el
  registro remoto y borró las decisiones aplicadas del ensayo; se restauró
  desde el historial git (commit `f5cd67a`). **Sin esta regla en el puente
  fusionado no hay corte (F4).**
- **Timeouts de escritura:** una escritura puede agotar el presupuesto de
  respuesta y aun así aterrizar en el repo. Ante un timeout se verifica por
  relectura (HEAD derivado) antes de reintentar. (La nota histórica sobre la
  idempotencia de `marcarlistas` quedó sin objeto en U1: esa acción ya no
  existe.)
- **`commit_aplicacion`:** la recogida lo escribe sobre la entrada aplicada
  aunque el campo exista en `null` (la vitrina crea las entradas con
  `commit_aplicacion: null`).
- **Retorno de mejora (derivación):** decisión `mejorar` aplicada + slug en
  `mejoras_cumplidas` (por `slug`, cualquier forma de entrada con slug) ⇒ el
  diseño vuelve a Pendientes como nueva versión, con `notaMejoraAnterior` =
  nota de la decisión mejorar aplicada (respaldo:
  `registro.regeneracion.nota_dueno`). Sin cumplimiento, sigue en «Por mejorar»
  como esperando regeneración.
- **Dimensiones:** la ficha expone `dimensiones_px` {ancho_px, alto_px} de la
  entrada del registro como dimensiones reales del PNG; si falta, no se
  inventa.

## Pase de pulido — carga y actualización (2026-10-26, portado del Centro de gestión de My Channels)

Aplicado y verificado primero en la instancia de ensayo y después en la de
producción, con el dale del dueño. Cuatro piezas, sin tocar el contrato de datos:

1. **Carga centrada:** el único estado de carga inicial es el símbolo de carga
   centrado en la vista con solo la palabra «Cargando». Los refrescos en
   segundo plano usan una versión pequeña que nunca tapa la vista.
2. **«Actualizar» dentro de la vista:** botón en la cabecera de la lista y del
   detalle. Primero comprueba el **sello** (acción ligera de solo-HEAD: en
   producción `sello`; devuelve el commit vigente). Si el commit no cambió,
   avisa «Ya está al día» y no relee nada; si cambió, refresca la bandeja en
   segundo plano conservando vista, filtro, detalle abierto y posición de
   scroll. Nunca recarga el documento.
3. **Caché de derivación por commit:** en el servidor, la derivación de la
   bandeja se indexa por el SHA de HEAD; con el sello quieto, reabrir o
   actualizar no repite la lectura completa. Las escrituras de decisiones
   invalidan la caché al instante.
4. **Overscroll contenido:** contención en la raíz (CSS + guardia de toque)
   para que el gesto de tirar hacia abajo no fuerce una recarga completa del
   documento.

El guardado instantáneo queda como estaba (decisión/retiro = un commit al
instante, con estado escribiendo/fallida); la nota NO se auto-guarda por
tecleo (viaja con la decisión o con «Guardar nota»).

**Deuda del nombre del sello — CERRADA en U1 (2026-10-26):** ambas
instancias exponen `sello` (verificado por acciones en ensayo y en
producción durante la corrida U1); ya no difieren.

## Enmienda U1 (2026-10-26) — vitrina sin marca

Decisión cerrada del dueño (brief de alineación 2026-10-26, U1):

- «Marcar listas» se retira como puerta: sin botón, sin recibo
  copiable, sin estado `lista` como requisito de recogida y sin
  acción `marcarlistas` en ninguna instancia.
- Las decisiones son automáticas al instante: se escriben en
  `vitrina/decisiones.json` al decidir (eso ya funcionaba) y esa
  escritura ES la decisión vigente; la recogida-aplicación se
  dispara con cualquier aviso del dueño en un chat y lee las
  decisiones vigentes del repo.
- Compatibilidad hacia atrás: entradas históricas con `estado`
  `lista` o `sin-marcar` se siguen leyendo e interpretando igual
  (como vigentes si no están aplicadas/devueltas); la marca y su
  `fecha_lista` son datos históricos ignorados, no un error.
- La regla del watchdog que alertaba por «decisiones marcadas
  listas sin recoger por más de 24 h» se reformuló: la alerta, si
  queda alguna, se basa en **decisiones vigentes sin aplicar**
  (última entrada por slug, no aplicada/devuelta, no `retirar`)
  con más de 24 h desde su `fecha` de decisión, leídas del repo
  — nunca de marcas.
- Qué murió también aquí: el recibo «Listas para recoger» y su
  mensaje copiable como mecanismo (el aviso libre del dueño ya
  era el disparador real desde `puerta-arte-propuesta` v0.8.4).
