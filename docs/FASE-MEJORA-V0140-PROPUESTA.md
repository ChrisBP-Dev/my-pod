# Fase de mejora post-migración v0.14.0 — PROPUESTA (2026-10-19)

Abierta automáticamente al cerrar la migración a Rameli
v0.14.0, como manda `rameli/MIGRACIONES.md`, con la **auditoría
de adopción completa** como primer insumo — en esta migración
era **no diferible** (el delta trae capacidades nuevas) y se
corrió: `docs/AUDITORIA-ADOPCION-V0140.md`. **Este documento es
la propuesta: nada de lo siguiente se ejecuta sin el dale del
dueño, y con dale corre como fase propia (rama y puertas
propias), no como apéndice de la migración.** Si se difiere o
se rechaza, queda registrado aquí y reaparece en la siguiente
migración.

Punto de partida verificado en vivo el 2026-10-19: lint en
**cero** fallos, regresión **verde total** (48 casos), pin
0.14.0 vigente en todas las declaraciones vivas, chequeo 4 de
`rameli validar` **sin hallazgos**. Las brechas de esta fase no
son de formato, de pin ni de datos: son **un FALLO de
colocación de calibración (B1)**, **una brecha de declaración
(B2)** y **un matiz menor del mapa en clones fríos (B3)**.

## P1 — Llevar el diseño canónico de la suite de arte dentro del repo (B1, C22/C5)

**El hallazgo:** la suite de `puerta-arte-propuesta` lee
`vitals-stable-print-300dpi.png` desde
`$HOME/workspace/goals/pod-etsy-sistema-operativo-q4-2026/files/disenos/canonicos`
(casos P1 y F6). Es el FALLO vigente del chequeo 3 de
`rameli validar` y la única deuda de frío de la app: la
regresión pasa en esta VM por el entorno, no por el sistema.
**En la migración no se movió ningún archivo de diseño** — la
forma de corregirlo es decisión del dueño entre estas
opciones:

| Opción | Qué cambia | Impacto / costo |
|---|---|---|
| **A — Copiar el canónico usado a fixtures** (recomendada) | El único archivo que la suite usa (11 MB) se copia a `skills/puerta-arte-propuesta/evals/fixtures/` y la variable `K` pasa a apuntar ahí. El original en la carpeta de diseños canónicos del goal **no se mueve ni se borra**: sigue siendo el canónico de producción; la copia es el insumo de calibración, con su origen registrado en el script. | La suite queda fría y portable; `rameli validar` pierde su único FALLO. Costo: +11 MB en el repo (que ya versiona binarios de producción de tamaño comparable). Riesgo: la copia puede divergir del canónico si este se regenera — mitigación: el script registra origen y fecha, y un caso de la suite puede verificar su hash contra el registrado. |
| **B — Generar un fixture sintético equivalente** | Se construye un PNG sintético que dispare exactamente los mismos veredictos (PASS a 300 DPI y FAIL `dpi_sin_margen_zoom` con margen) y los casos dejan de usar el diseño real. | Repo liviano y cero binarios de producción en fixtures. Riesgo: la equivalencia hay que **probarla en ambos sentidos** (mismos veredictos y criterios que con el canónico, calibrado contra él antes de retirarlo) — si el sintético no reproduce la geometría/DPI reales, los casos P1/F6 dejan de medir lo que medían. Más trabajo y más riesgo de calibración que A. |
| **C — Diferir con registro** | Nada cambia; el FALLO queda como deuda aceptada con motivo y fecha de revisión, y reaparece en la siguiente migración. | Mantiene el estado actual: la suite no es fría y cada cierre futuro cargará el mismo FALLO clasificado. Solo tiene sentido si el dueño planea rehacer la suite de arte por otro motivo en breve. |

**Riesgo general: bajo-medio.** Acotado a la suite de una
puerta (2 de sus 13 casos); ningún criterio, umbral ni
comportamiento de `verificar-arte.py` cambia. Verificación al
ejecutar: suite de arte verde con la ruta externa
renombrada/ausente (prueba de frío real), regresión total
verde y `rameli validar` sin el FALLO del chequeo 3.

## P2 — Declarar los 3 scripts sin declarar (B2, C22/C9/C20)

**Qué cambia:** cada script gana su declaración en el
documento que lo gobierna y su mención en la ruta de lectura
de `FLUJO-PIPELINE.md`, sin moverlos de `scripts/` (su casa
correcta) y sin tocar su código:

- `procesar-arte-propuesta.py` → skill `puerta-arte-propuesta`
  (es el paso que produce el print-ready que la puerta juzga,
  con autotrim) y ruta F1/Fase A.
- `reparar-fondo-casi-blanco.py` → skill
  `puerta-arte-propuesta` (utilidad de reparación previa a la
  puerta, con el caso que la originó) y ruta F1/Fase A.
- `reporte-seo.py` → el doc/skill que el dueño prefiera entre
  `estratega-tienda` (cruza banco × ledger, insumos de la
  dirección) o `paquete-listing-etsy` (mide la cobertura SEO
  de los paquetes) — la propuesta recomienda
  **estratega-tienda**, porque su salida alimenta decisiones
  de dirección, no la producción de un paquete; queda como
  micro-decisión del dueño al dar el dale.

**Impacto:** junto con P1, `rameli validar` puede llegar a
verde total *por las razones correctas* (hoy los avisos del
chequeo 1 ya no se reproducen, pero enmascarados por los
registros de la migración — ver la nota de riesgo); un chat
frío descubre las tres herramientas desde el sistema, con
su cuándo y su puerta, en vez de heredarlas por memoria del
operador.

**Riesgo: bajo.** Solo documentación y punteros. Ojo con la
verificación: `rameli validar` ya no reproduce los avisos en
`main`, porque los registros de la migración/auditoría
nombran a los scripts y cuentan como corpus vivo — la
verificación de P2 es **declaración presente en el skill
gobernante y en la ruta de lectura, con sus punteros
resolviendo**, no la ausencia del aviso. Si al documentar
alguno el
dueño juzga que ya no tiene uso, la alternativa por script es
**retirarlo** (borrado con huella en el registro, según el
ciclo de vida de activos) en vez de declararlo — también con
su dale, caso por caso.

## P3 — Resolver el matiz de `data/cola-pins` en el mapa (B3, C23)

**El matiz:** el mapa declara `data/cola-pins` como global,
pero el directorio es vacío y está en `.gitignore`: en un
clon frío no existe y `rameli validar` levanta el aviso
«declarado pero no existe». **El mapa no se re-decidió en la
migración**; las opciones:

| Opción | Qué cambia | Nota |
|---|---|---|
| **A — Versionar el directorio** (recomendada) | Se fuerza un `.gitkeep` dentro de `data/cola-pins/` (excepción puntual al `.gitignore`) para que el directorio exista en todo clon. | La declaración del mapa se vuelve satisfacible desde el repo. La cola sigue siendo local (sus contenidos siguen ignorados). Cambio mínimo. |
| **B — Sacarlo del mapa** | `datos.globales` deja de listar `data/cola-pins`, declarándolo de hecho una zona local transitoria fuera del estándar. | El aviso desaparece, pero una entrada real de la raíz queda sin declarar — el chequeo 4 la marcaría como «entrada no declarada» cuando el directorio exista, cambiando un aviso por otro según el árbol. Peor que A. |
| **C — Aceptar el aviso** | Nada cambia; el aviso se clasifica en cada cierre como conocido. | Válido si el dueño prefiere no versionar directorios vacíos; el costo es ruido permanente en cada corrida sobre clones. |

**Impacto:** cosmético-operativo; no toca datos ni precios.
**Riesgo: mínimo.**

## Orden sugerido

| Orden | Propuesta | Por qué ahí |
|---|---|---|
| 1 | **P1** — canónico de la suite dentro del repo | Es el único FALLO de `rameli validar` y la única deuda de frío: mientras viva, ningún cierre puede declarar la colocación verificada. |
| 2 | **P2** — declarar los 3 scripts | Con P1 hecha, P2 deja `rameli validar` en verde total por primera vez; es documental y rápida. |
| 3 | **P3** — matiz `cola-pins` | Menor y opcional en la práctica (opción A es un cambio de un archivo); puede viajar con P2 en la misma rama de la fase. |

## Inventario arrastrado (decisiones del dueño, fuera de esta propuesta)

Reaparecen por la regla de la fase (registrados en
`docs/AUDITORIA-ADOPCION-V0140.md` §5), **no** forman parte de
las propuestas de ejecución de arriba:

- **Reactivación del cron `equipo-pod-propuestas-diarias`**
  (pausado, verificado hoy): con la secuencia fijada por el
  dueño — primero pulir la personalización en su chat, recién
  entonces reactivarlo como prueba integral del sistema.
- **Corrección del dueño (2026-10-19):** este inventario
  traía una «re-revisión de p055/p056» como pendiente del
  dueño; **nunca fue decisión suya** — era un remanente del
  resumen del asistente al cerrar la incidencia neck, que
  está cerrada. Se retira de los pendientes: esos drafts
  siguen el flujo normal (revisión en Printify, etapa 3),
  como cualquier draft. **El único pendiente que queda del
  lado del dueño es la personalización** (su chat ya creado),
  del que depende la reactivación del cron de arriba.

De la fase post-v0.12.1 no queda nada abierto: sus dos
propuestas (P1 ruta de lectura, P2 fuga de
`verificar-video.py`) se ejecutaron y cerraron el 2026-10-19,
y ambas se revalidaron en esta auditoría.

---

## Estado de ejecución (2026-10-19, dale del dueño en este chat)

El dueño ordenó ejecutar la fase completa en este chat
— «aplicar todo» y sin dejar remanentes: lo único que queda
pendiente de su lado es la personalización — y fijó las
opciones recomendadas (P1-A, P2 con `reporte-seo.py` en
estratega-tienda, P3-A). Ejecutada en la rama
`mejora-v0140`:

| Propuesta | Estado | Evidencia |
|---|---|---|
| P1 (B1) — canónico dentro del repo | **Ejecutada** | `vitals-stable-print-300dpi.png` copiado a `skills/puerta-arte-propuesta/evals/fixtures/` (sha256 idéntico al origen: `6549b13b…27a135`; el original NO se movió de su hogar canónico); `K` en la suite apunta ahora a `evals/fixtures`, con origen y hash registrados en el propio script. Suite de arte **13/13** y **prueba de frío real**: la suite corre 13/13 con `HOME` apuntando a un directorio vacío — ya no lee nada fuera del repo. `rameli validar`: el FALLO del chequeo 3 desapareció. |
| P2 (B2) — declarar los 3 scripts | **Ejecutada** | `procesar-arte-propuesta.py` y `reparar-fondo-casi-blanco.py` declarados en `puerta-arte-propuesta` (nueva sección «Herramientas de procesamiento», v0.5.3) y en la ruta F1 de `FLUJO-PIPELINE.md`; `reporte-seo.py` declarado en `estratega-tienda` (entrada 9, v0.5.3) y en la ruta F4. Verificación por declaración en skill + ruta (no por la salida de `validar`, que ya venía enmascarada). |
| P3 (B3) — matiz `cola-pins` | **Ejecutada** | Opción A: `data/cola-pins/.gitkeep` versionado; `.gitignore` pasa de ignorar el directorio a ignorar su contenido con excepción del `.gitkeep` (probado: un archivo de prueba dentro sigue ignorado, el `.gitkeep` es versionable). En el worktree de la fase el directorio existe desde el clon y el aviso del chequeo 4 no se reproduce. |

**Puertas de la fase:** lint VERDE e idéntico al antes;
regresión VERDE total (48 casos, 0 fugas de temporales);
**`rameli validar` VERDE total por primera vez: 0 fallos,
0 avisos** (antes de la fase: 1 fallo / 3 avisos en el árbol
principal). Ningún criterio de ninguna puerta cambió,
ningún dato de producción se tocó (el único archivo nuevo
bajo `data/` es el `.gitkeep` vacío de P3), y el cron de
propuestas **sigue pausado** en su secuencia.

**Corrección incorporada en esta ejecución:** la
«re-revisión de p055/p056» se retiró de los pendientes de
esta fase y de la auditoría (ver §Inventario): nunca fue
decisión del dueño.

**Cierre (2026-10-19):** rama `mejora-v0140` (commit
`01e931a`) fusionada a `main` en fast-forward
(`9100c95 → 01e931a`) tras re-verificar que `main` no se
había movido; rama borrada (local y remota) y worktree
retirado. **Verificación post-fusión sobre `main`: lint
VERDE idéntico, regresión VERDE total idéntica a la de la
rama (48 casos) y `rameli validar` VERDE total — 0 fallos,
0 avisos — también en el árbol principal.** De esta fase no
queda nada abierto: el único pendiente del sistema es la
personalización, en su chat, y la reactivación del cron que
de ella depende.

## Pendientes del dueño al abrir esta fase

1. **Dale (o diferimiento con motivo) para P1, P2 y P3** —
   cada una con su opción donde la hay: P1 opción A/B/C;
   P2 con la micro-decisión de dónde se declara
   `reporte-seo.py` (recomendado: estratega-tienda) y la
   posibilidad de retirar algún script en vez de declararlo;
   P3 opción A/B/C.
2. Del inventario arrastrado, solo queda la secuencia ya
   fijada por él: pulir la personalización en su chat y,
   recién entonces, reactivar el cron de propuestas como
   prueba integral. (La «re-revisión de p055/p056» que un
   borrador listaba aquí fue retirada por su corrección del
   2026-10-19: nunca fue decisión suya.)
