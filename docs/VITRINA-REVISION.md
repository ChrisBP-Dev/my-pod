# Vitrina de revisión de propuestas — plantilla del sistema

**Qué es.** La superficie donde el dueño ejerce la puerta creativa de la
Etapa 1 del flujo v2 (ver `FLUJO-PIPELINE.md` §1): una página organizada,
pensada primero para el teléfono, donde cada propuesta se revisa con su
arte y su porqué, y la decisión se guarda **como dato** — no como mensajes
sueltos en un chat. Idea del dueño (2026-10-20): revisar así ahorra
créditos (cada reacción en un chat largo re-lee el contexto completo) y
deja las decisiones estructuradas para que Jarvis las procese de una vez.

**Estado:** plantilla v2.0 (modelo de bandeja continua, corrección
del dueño 2026-10-22 que reemplaza la regla de cola/anti-cruce de la
v1.2 — ver §Operación) + piloto con el lote 2026-10-19 (p058–p067).
La canonización en `puerta-arte-propuesta` (como canal de entrega) se
decide cuando el piloto esté validado por el uso real del dueño.

## Principios de UX (no negociables de la plantilla)

1. **Móvil primero, desktop con su ancho.** En el teléfono: una columna,
   el arte manda. En desktop: parrilla de tarjetas (2–3 por fila) y el
   detalle en dos columnas (arte | información y decisión).
2. **Pocas cosas, bien ordenadas.** Una sola jerarquía por pantalla:
   arte → título y etiquetas → porqué en secciones → decisión. Nada de
   tableros cargados ni datos duplicados en dos lugares.
3. **Progreso siempre visible.** Encabezado fijo con el conteo del lote
   (revisados / total) y su barra; el dueño sabe en todo momento cuánto
   falta.
4. **Decidir cuesta un toque.** La decisión se guarda al instante, sin
   botón de «guardar» global ni formularios. Cambiar de opinión es
   volver a tocar: la última decisión es la que vale.
5. **El arte se juzga como se va a usar.** Cada diseño trae dos vistas
   previas deterministas compuestas desde el PNG de producción: sobre
   fondo oscuro y sobre fondo claro (las prendas reales), con un
   conmutador en el detalle. Nunca una regeneración «parecida».
6. **Sin celdas vacías ni datos huérfanos.** Todo lo que la puerta
   declara (porqué, qué mirar, nota de la puerta) vive dentro de la
   tarjeta del diseño; ningún archivo adjunto sustituye la presentación.
7. **La tarjeta no decide; el detalle decide.** La lista es para
   navegar: tarjeta = arte completo + título + descripción breve +
   etiquetas + estado, y se entra tocándola. Los botones de decisión
   viven solo en el detalle (el flujo de revisión es de a uno).
8. **El arte nunca se recorta en pantalla.** Tarjeta, detalle y visor
   muestran el diseño COMPLETO (ajuste «contain», mismo margen y fondo
   en todas), fiel al recorte real del archivo — un encuadre que corte
   el diseño falsea la evaluación del recorte.
9. **Nada bloquea a nada.** La vitrina es una bandeja continua: los
   lotes se suman, las decisiones conviven y todo sigue editable
   mientras el diseño esté en la vitrina. No hay «cierre de lote» ni
   requisito de cero pendientes para que entre trabajo nuevo
   (corrección del dueño 2026-10-22 que reemplaza el cierre de la
   v1.1/v1.2: la fecha es un indicador, no una puerta).

## Flujo de uso

1. **Siembra (el flujo):** con un lote en PASS de la puerta de arte,
   se genera el paquete de datos (§Contrato de entrada) con
   `scripts/generar-datos-vitrina.py` y se **siembra** en la vitrina
   de la tienda (§Operación: la siembra es aditiva y nunca bloquea).
2. **Revisión (el dueño):** entra a la vitrina — la vista inicial es
   **Pendientes** (no hay vista «todas»: la lista se va limpiando a
   medida que decide; las demás vistas son aprobadas / rechazadas /
   mejoradas, para consultar lo ya decidido y cambiar de opinión
   cuando quiera) —, abre cada diseño, lee su porqué, alterna el
   fondo con el control segmentado etiquetado «Fondo: Oscuro /
   Claro» (estado activo inconfundible en ambos modos), inspecciona
   el arte en el visor con zoom natural (focal, acotado, sin cierre
   por gestos) y decide en el detalle: **Aprobar**, **Rechazar** o
   **Mejorar** (con nota de qué mejorar; la nota también es
   bienvenida en un rechazo). Cuando quiere, pulsa **«Marcar listas
   para Jarvis»** (visible solo si hay decisiones sin marcar, con su
   conteo): las marca como listas — una bandera, no un candado; todo
   sigue editable y cambiar una decisión le quita la marca. Al
   marcar, la vitrina muestra un recibo compacto («Listas para
   recoger — todavía no fueron procesadas») con el mensaje exacto
   para avisar en un chat y su botón **Copiar mensaje**; el recibo
   reaparece, discreto, mientras haya decisiones listas sin recoger.
3. **Lectura de vuelta (Jarvis):** lee las decisiones enviadas
   (§Contrato de salida), las vuelca al checkpoint del sistema
   (`data/tiendas/<tienda-id>/estado-propuestas.json`: aprobados con
   `{slug, fecha_aprobacion}`; rechazados fuera con su motivo si lo
   dio; mejorar señalados para regenerar solo lo pedido) y confirma
   la recogida en la vitrina: aprobados y rechazados **salen** de la
   vitrina (ya viven en el registro del sistema; los rechazados se
   purgan, como manda el flujo) y los de mejorar quedan como
   «Esperando regeneración» hasta que su nueva versión se siembra
   (vuelve a Pendientes con distintivo «Nueva versión» y la nota
   anterior visible en su detalle). La Fase B produce **solo** lo
   aprobado, como manda el flujo v2. Nada se produce desde la
   vitrina.

## Contrato de entrada — `datos-vitrina.json`

Generado por `scripts/generar-datos-vitrina.py` desde el registro de la
tienda y el checkpoint; es la única fuente que la instancia consume.

```json
{
  "version_contrato": 1,
  "tienda": {"id": "29222324", "nombre": "MyNightShiftShop"},
  "lote": {"fecha": "2026-10-19", "slugs": ["p058", "..."]},
  "disenos": [{
    "slug": "p058",
    "titulo": "Quiet ER Christmas Wish",
    "tema": "navidad",
    "etiquetas": ["Navidad", "ER", "MPL"],
    "frase": "All I Want for Christmas Is a Quiet ER",
    "tema_angulo": "…", "frase_texto": "…",
    "iconografia": "…", "que_mirar": "…",
    "puerta": "puerta-arte-propuesta v0.5.1 PASS completo …",
    "producto_destino": "MPL — sudadera + playera (un solo listing)",
    "personalizable": false,
    "simulacion": null,
    "arte_ref": "data/artes-print/p058-print-300dpi.png",
    "dimensiones_px": {"ancho_px": 6458, "alto_px": 3842},
    "previa_oscura": "previas/p058-oscura.jpg",
    "previa_clara": "previas/p058-clara.jpg"
  }]
}
```

- El porqué llega ya partido en sus secciones de entrega (tema y
  ángulo / frase / iconografía / qué mirar), partidas del texto
  canónico del registro; la vitrina no reescribe el porqué.
- **Personalizables:** `personalizable: true` y `simulacion` con la
  ruta de la previa de la simulación (compuesta sobre el arte real,
  según la variante de entrega de `puerta-arte-propuesta`); el detalle
  muestra arte real y simulación, etiquetadas como tales.

## Contrato de salida — decisiones (v2, bandeja continua)

Una decisión por diseño, guardada en la instancia al momento de tocar:

```json
{"slug": "p058", "lote_fecha": "2026-10-19",
 "decision": "aprobado|rechazado|mejorar",
 "nota": "texto libre del dueño o cadena vacía",
 "fecha": "2026-10-22T21:05:00-04:00",
 "enviada": true, "fecha_envio": "2026-10-22T21:20:00-04:00",
 "nueva_version": false}
```

No hay registro de «revisión terminada»: el flujo de recogida es
continuo. Jarvis procesa las decisiones marcadas `enviada` (o las que
el dueño avise en el chat) y confirma la recogida por slug (§Flujo
de uso, paso 3). Una decisión no enviada es un borrador del dueño,
no una orden; una enviada sigue siendo editable, y editarla le
quita la marca hasta que vuelva a enviarla.

## Qué hace «Marcar listas para Jarvis» (funcionamiento, sin magia)

Pone la bandera `enviada` con su fecha a las decisiones que aún no la
tienen — es una **señal**, no una acción sobre la tienda ni un envío:
la vitrina no produce, no publica, no toca Printify y **no notifica
a nadie por sí sola**. La señal dice «estas decisiones ya pueden
recogerse»; la recogida ocurre cuando el dueño avisa en un chat (el
recibo de la vitrina trae el mensaje exacto, copiable: «Jarvis,
recoge las decisiones de la vitrina de My POD (<tienda>)»). Jarvis
lee las decisiones (contrato de salida), las vuelca al checkpoint de
la tienda, confirma la recogida y el flujo v2 sigue su curso (la
Fase B produce solo lo aprobado, con la palabra que el flujo exija).
Un diseño ya recogido en «Esperando regeneración» no cuenta como
«sin enviar» ni vuelve a ofrecer la acción de marcar.

## Pulido v1.1 — correcciones del dueño (2026-10-22, sobre el piloto)

Sobre la v1, probada por el dueño en su teléfono: (1) fuera los
botones rápidos de decisión de las tarjetas — no tenían sentido en un
flujo de revisión de a uno; (2) fuera la vista «todas» — la vista de
trabajo es Pendientes y se va limpiando; (3) el conmutador de fondo
eran «chips raros» sin función evidente ni estado activo legible en
modo oscuro — pasa a control segmentado etiquetado con estado
inconfundible; (4) el arte quedaba recortado por el encuadre de la
tarjeta — pasa a mostrarse completo siempre; (5) faltaba inspección
fina — visor a pantalla completa con zoom; (6) «Terminé mi revisión»
y «resumen» estaban en todos lados y sin validación visible — el
cierre pasa al panel que solo existe con cero pendientes (principios
7–9 y §anterior). La variante para personalizados se pule cuando
lleguen propuestas personalizadas (decisión del dueño).

## Operación: UNA instancia por tienda, bandeja continua

La vitrina **no se crea por lote ni por día**: existe **una sola
instancia por tienda**, que vive en la aplicación, y lo que cambia
es su contenido. Crear instancias nuevas por corrida quemaría trabajo
de creación y multiplicaría superficies que el dueño tendría que
buscar; sembrar datos es una llamada, no una construcción.

- **Siembra ADITIVA:** al cerrar la Fase A de un lote, el flujo
  genera el paquete (`scripts/generar-datos-vitrina.py`) y lo siembra
  en la instancia de la tienda. Sembrar **suma**: los diseños nuevos
  entran como pendientes (arriba, más recientes primero; su fecha de
  lote es solo un indicador en la tarjeta) y los ya presentes
  conservan su decisión y su nota. Un slug sembrado con arte nuevo
  es una **regeneración**: se actualiza, vuelve a pendiente con
  distintivo «Nueva versión» y conserva la nota de mejora anterior
  visible en su detalle.
- **Sin cola bloqueante (corrección del dueño 2026-10-22, reemplaza
  la «regla anti-cruce» de la v1.2):** un lote nuevo nunca espera a
  que el dueño termine de revisar otro. Todos los pendientes son
  simplemente pendientes del dueño, vengan del día que vengan; los
  decididos viven en sus vistas (aprobadas / rechazadas / mejoradas)
  hasta que Jarvis los recoge, y tras la recogida aprobados y
  rechazados salen de la vitrina (los rechazados se purgan, como
  manda el flujo) y los de mejorar quedan «Esperando regeneración».
- **Quién la usa en el flujo:** cuando esta plantilla se canonice,
  el paso de entrega de la Fase A en `puerta-arte-propuesta` dirá:
  generar el paquete → sembrar la vitrina de la tienda (aditivo) →
  avisar al dueño que revise ahí. Hasta esa canonización, la
  siembra la hace Jarvis.
- **Costo:** la creación de la instancia ocurre **una vez por
  tienda**. Cada lote cuesta solo la generación del paquete (script
  local determinista) y la llamada de siembra.
- **Cómo funciona por dentro (para que nadie tenga que imaginarlo):**
  los diseños y las decisiones son registros en la base de datos
  propia de la instancia; la interfaz los lee y los modifica ahí
  (decidir = actualizar el registro del diseño, con su nota). Jarvis
  los lee y confirma recogidas mediante las acciones de la propia
  instancia (§Contrato de salida). Nada de esto vive en un chat ni
  depende de su memoria.

## Pulido v2.0 — visor en iPhone y modelo continuo (2026-10-22)

Tercera pasada del dueño, ya sobre su iPhone: (1) el zoom del visor
ampliaba siempre desde el centro y al arrastrar hacia un lado la
vista **se cerraba** (el gesto llegaba a la hoja de debajo) — el
visor pasa a zoom focal (sigue al gesto), arrastre acotado a los
límites de la imagen y **ningún gesto cierra el visor** (solo el
botón Cerrar). (2) El interruptor «Límites» y su damero se retiran:
con el marco y el borde de la v1.2 los límites ya se leen y el
interruptor sobraba. (3) El modelo por lote con cola bloqueante se
reemplaza por la bandeja continua (§Operación y principio 9):
la preocupación del dueño era perder lo ya decidido al cambiar de
lote y no poder cambiar de opinión ni gestionar mejoras en paralelo;
con la bandeja, todo convive y todo sigue editable hasta la recogida.

## Pulido v1.2 — límites del arte y área segura (2026-10-22)

Segunda pasada del dueño sobre el piloto: (1) con el fondo uniforme
expandido no se veía **dónde termina el arte ni cuánto aire lleva el
recorte** — solución de pura presentación: la imagen va siempre dentro
de un marco visible (fondo del contenedor distinto + borde + franja
uniforme) en tarjeta, detalle y visor; el visor suma el interruptor
«Límites» (contorno de contraste pegado al borde exacto del arte y
damero sutil fuera del arte) y el detalle muestra las dimensiones
reales del PNG (`dimensiones_px` en el contrato de entrada, medido
por el generador — nunca estimado). (2) Los controles del visor
invadían los extremos de la pantalla — pasan a una barra agrupada
con márgenes de área segura reales (`env(safe-area-inset-*)` + un
mínimo en píxeles) en los cuatro lados.

## Replicación (otra tienda u otro usuario de la aplicación)

1. La tienda declara sus propuestas en su registro, como siempre
   (el contrato de entrada no pide nada que el flujo v2 no produzca ya).
2. Se corre el generador con el id de esa tienda y su lote.
3. Se crea la instancia de la vitrina de esa tienda (aplicación web
   con guardado propio) — **una sola, durable** — y se siembra con el
   paquete generado, siguiendo los principios de UX y los contratos
   de este doc; los lotes siguientes solo se siembran.
4. El dueño revisa; Jarvis lee de vuelta y vuelca al checkpoint de
   esa tienda. Ningún paso depende de la memoria de un chat.
