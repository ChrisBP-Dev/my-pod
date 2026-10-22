# Vitrina de revisión de propuestas — plantilla del sistema

**Qué es.** La superficie donde el dueño ejerce la puerta creativa de la
Etapa 1 del flujo v2 (ver `FLUJO-PIPELINE.md` §1): una página organizada,
pensada primero para el teléfono, donde cada propuesta se revisa con su
arte y su porqué, y la decisión se guarda **como dato** — no como mensajes
sueltos en un chat. Idea del dueño (2026-10-20): revisar así ahorra
créditos (cada reacción en un chat largo re-lee el contexto completo) y
deja las decisiones estructuradas para que Jarvis las procese de una vez.

**Estado:** plantilla v1 + piloto con el lote 2026-10-19 (p058–p067).
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

## Flujo de uso

1. **Preparación (Jarvis):** con el lote en PASS de la puerta de arte,
   se genera el paquete de datos (§Contrato de entrada) con
   `scripts/generar-datos-vitrina.py` y se crea (o se actualiza) la
   instancia de la vitrina de la tienda sembrada con ese paquete.
2. **Revisión (el dueño):** entra a la vitrina, filtra si quiere
   (todas / pendientes / aprobadas / rechazadas / a mejorar), abre cada
   diseño, lee su porqué, mira las dos vistas y decide:
   **Aprobar**, **Rechazar** o **Mejorar** (con nota de qué mejorar;
   la nota también es bienvenida en un rechazo). Al terminar, marca
   **«Terminé mi revisión»**.
3. **Lectura de vuelta (Jarvis):** lee las decisiones guardadas
   (§Contrato de salida) y las vuelca al checkpoint del sistema
   (`data/tiendas/<tienda-id>/estado-propuestas.json`): los aprobados
   entran en `aprobados`
   con `{slug, fecha_aprobacion}`; los rechazados salen del lote con su
   motivo si lo dio; los marcados «mejorar» quedan señalados para
   regenerar solo lo pedido. La Fase B produce **solo** lo aprobado,
   como manda el flujo v2. Nada se produce desde la vitrina.

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

## Contrato de salida — decisiones

Una decisión por diseño, guardada en la instancia al momento de tocar:

```json
{"slug": "p058", "decision": "aprobado|rechazado|mejorar",
 "nota": "texto libre del dueño o cadena vacía",
 "fecha": "2026-10-22T21:05:00-04:00"}
```

Y un registro de revisión por lote: `{estado: "en_curso|terminada",
fecha_terminada}`. Jarvis procesa las decisiones cuando la revisión
está **terminada** (o cuando el dueño avise en el chat que ya revisó);
una decisión sin terminar es un borrador del dueño, no una orden.

## Replicación (otra tienda u otro usuario de la aplicación)

1. La tienda declara sus propuestas en su registro, como siempre
   (el contrato de entrada no pide nada que el flujo v2 no produzca ya).
2. Se corre el generador con el id de esa tienda y su lote.
3. Se crea la instancia de la vitrina (aplicación web con guardado
   propio) sembrada con el paquete generado, siguiendo los principios
   de UX y los contratos de este doc — la instancia es desechable por
   lote; lo durable es esta plantilla.
4. El dueño revisa; Jarvis lee de vuelta y vuelca al checkpoint de
   esa tienda. Ningún paso depende de la memoria de un chat.
