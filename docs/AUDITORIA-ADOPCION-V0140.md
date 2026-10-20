# Auditoría de adopción — My POD × Rameli v0.14.0 (2026-10-19)

> Primer insumo de la fase de mejora abierta al cerrar la
> migración a Rameli v0.14.0 (`docs/MIGRACION-RAMELI-V0140.md`),
> como manda `rameli/MIGRACIONES.md`. En esta migración la
> auditoría **no era diferible** (el delta v0.13.0/v0.14.0 trae
> capacidades nuevas) y las notas de migración exigen que la
> matriz sume expresamente la **validación de colocación**
> (primera corrida de `rameli validar` con registro) y la fila
> de **datos multi-unidad** (¿mapa declarado?, ¿hogares
> completos?, ¿mecanismo fuera de los datos?). Método: matriz
> completa de capacidades vigentes del framework × flujos de
> la aplicación, con veredicto y evidencia en el repositorio
> por celda — nada de memoria. Donde la evidencia no alcanza,
> la celda dice **sin evidencia**. **Nada de lo propuesto
> aquí se ejecuta sin el dale del dueño**; la propuesta vive
> en `docs/FASE-MEJORA-V0140-PROPUESTA.md`.

## Método y bases verificadas

- **Framework de referencia:** repo `rameli`, `main` en
  `6c478f3` = `origin/main`, `VERSION` = **0.14.0**; tags
  anotados remotos `v0.13.0`/`v0.14.0` verificados con
  `ls-remote`. Capacidades tomadas SOLO de documentos
  vigentes en ese repo.
- **Aplicación auditada:** repo `my-pod`, `main` en
  `1e73e16` (base de la migración v0.14.0), pin **0.12.1**
  al abrir la auditoría y **0.14.0** en la rama de
  migración, en `rameli.json`, README y frontmatter de los
  **9 skills**.
- **Verificaciones corridas en vivo para esta auditoría**
  (2026-10-19): `rameli lint` sobre los 9 skills → **verde
  total**, idéntico antes/después; `rameli test` → **verde
  total (48 casos)**, idéntico antes/después y sin fuga de
  temporales; `rameli validar` → **1 FALLO (chequeo 3) y
  3 AVISOS (chequeo 1)**, clasificados en el registro de la
  migración, y **chequeo 4 sin hallazgos**; verificación
  directa del mapa de datos (hogar, globales e historial
  existen; ningún código bajo `data/`); estado de crons
  consultado en vivo (propuestas **pausado**, Pinterest
  **activo**, estratega/investigación/rituales/trend-scan
  **activos**, watchdog **activo**, y el cron del 31-oct
  para bajar la oferta a 20% **activo**).
- **Precedente:** `docs/AUDITORIA-ADOPCION-V0121.md` (matriz
  contra v0.12.1, 2 brechas, ambas propuestas ejecutadas y
  cerradas en su fase). Esta auditoría **confirma** los
  veredictos cuyas evidencias siguen en pie, **actualiza**
  los que las ejecuciones de aquella fase y el reorden de
  datos por tienda cambiaron, y **agrega** las capacidades
  nuevas del delta. La numeración C1–C21 se conserva por
  comparabilidad; el delta suma **C22** y **C23**.

## Leyenda de veredictos

| Código | Significado |
|---|---|
| **P** | Adoptado y probado — evidencia de uso real (corrida, suite verde, cierre verificado) |
| **A** | Adoptado sin estrenar — escrito/instanciado, sin corrida real que lo pruebe |
| **NA** | No aplica — con motivo declarado |
| **B** | Brecha real — remite a la propuesta de la fase de mejora |
| **SE** | Sin evidencia — el repo no permite verificarlo |

---

## 1. Inventario de capacidades vigentes de Rameli v0.14.0

C1–C21 como en la auditoría anterior (formato de skills y
revelado progresivo; constructor y su ciclo de vida;
plantillas operativas; puertas mecánicas en código; evals
deterministas; evals de juicio + A/B del constructor;
calibraciones mecanismo vs aplicación; reglas con motivo;
helpers antes que prosa; orquestación determinista — Pieza 4
con su delimitación; criterio y auditoría de colocación;
terminología canónica; versionado, pin y herramienta
`rameli`; lint de formato; contribuciones por PR; ejecución
por workers fríos + brief limpio + watchdog; registro de
flujo y relevo; checkpoints con resume; fase de mejora
encadenada; ruta de lectura por tarea; auditoría de adopción
obligada). **Cambios del delta 0.12.1 → 0.14.0 sobre ese
inventario:**

- **C11 — se endurece con herramienta (v0.13.0):** el
  criterio de colocación deja de ser solo doctrina con
  checklist: gana su puerta mecánica en C22. El veredicto de
  C11 ya no puede declararse sin correrla.
- **C13 — la herramienta `rameli` suma dos superficies:**
  `rameli validar` (v0.13.0) y el esqueleto `datos` que
  `rameli init` crea para apps nuevas (v0.14.0; para esta
  app, NA — ver C23).
- **C22 — Validación de colocación (NUEVA, v0.13.0, PR #7).**
  Comando `rameli validar <dir-app>` (capa mecánica en el
  constructor, fabrica-skills v0.6.0, regresión permanente
  del validador): chequeo 1 correspondencia
  declarado↔físico, chequeo 2 declaraciones muertas,
  chequeo 3 calibración dentro del repo — y encima el
  **protocolo de cierre con registro** (inventario de
  herramientas de la fase + prueba de frío por escrito +
  artefactos que calibran archivados en el repo el mismo
  día), al cerrar una fase o migración y a pedido
  («valídalo»). (`rameli/docs/VALIDACION-COLOCACION.md`)
- **C23 — Datos multi-unidad (NUEVA, v0.14.0).** Estándar
  del framework para la data operativa multi-unidad:
  hogar por unidad, mecanismo nunca en datos, lo compartido
  declarado como global, el registro referencia y no copia,
  ciclo de vida de activos, historia ejecutada congelada y
  declarada. Cada aplicación declara su **mapa** en
  `rameli.json` (clave `datos`) y el **chequeo 4** de
  `rameli validar` lo verifica. (`rameli/docs/
  DATOS-MULTIUNIDAD.md`)

## 2. Inventario de flujos de My POD (estado verificado hoy)

- **F1 — Propuestas (flujo v2).** Sin cambios de forma desde
  la auditoría anterior (Fase A: arte + puerta completa +
  aprobación del dueño por diseño; Fase B: drafts/MPL solo
  de aprobados). Tras aquella auditoría corrió el reorden de
  datos por tienda: la operación de la tienda vive hoy en
  `data/tiendas/29222324/` (directriz, config, registro,
  ledger, checkpoints, investigaciones y revisiones). Cron
  `equipo-pod-propuestas-diarias` **pausado** (verificado en
  vivo); su reactivación sigue la secuencia fijada por el
  dueño (primero pulir la personalización; la reactivación
  servirá de prueba integral).
- **F2 — Publicación por lote.** Sin cambios; sin lote nuevo
  en el período — sin evidencia nueva.
- **F3 — Pinterest diario.** Cron **activo** (08:50,
  verificado en vivo); parrilla de `estratega-pinterest`,
  puerta `puerta-pinterest-pin`, links rastreables.
- **F4 — Dirección semanal.** Crons **activos** (verificado
  en vivo): investigación y estratega de lunes, trend-scan
  lun/jue, rituales de lunes y viernes. La directriz de la
  semana 19–26 oct está commiteada en el hogar de la tienda
  (la regla «escribir = commitear en la misma corrida» ya
  opera).
- **F5 — Onboarding de tienda.** Sin corrida nueva; sigue
  sin estrenar para una segunda tienda.
- **F6 — Conexión Etsy API por tienda.** Sin corrida nueva;
  probado con una tienda (2026-10-16).
- **F7 — Operación comercial por API/scripts.** Declarado
  con dueño y ruta en `docs/DELIMITACIONES-ADOPCION.md` §1.
  Cron de un solo uso **activo** para el 31-oct (bajar la
  oferta de 25% a 20% al cerrar la intro de Share & Save),
  según el calendario de descuentos registrado.
- **F8 — Puertas transversales.** Suites verdes verificadas
  hoy: arte 13/13, pin 15/15, paquete 4/4, publicar 3/3,
  contrato de la estratega 13/13 (**48 casos, 0 fallas**).
- **F9 — Mantenimiento del sistema.** Probado hoy de punta
  a punta: migración a v0.14.0 (rama aislada, regresión
  comparada idéntica, primera corrida de `rameli validar`
  con registro) y esta auditoría como apertura de su fase
  de mejora.

---

## 3. Matriz capacidad × flujo

Solo se listan las celdas cuyo veredicto **cambia** respecto
de la auditoría v0.12.1, las capacidades **nuevas** y las
que el delta toca; el resto se **confirma** con la evidencia
de aquella matriz, que sigue en pie (lint y regresión de
hoy la revalidan, y la ruta de lectura adoptada en su fase
de mejora se verificó vigente en `FLUJO-PIPELINE.md`).

| Cap. | Veredicto hoy | Evidencia / nota |
|---|---|---|
| C5 Regresión determinista | **P** en F8/F1 (48 casos verdes hoy, idénticos antes/después) — **con la salvedad de B1** | La fuga de temporales (brecha B2 de la auditoría anterior) está cerrada y verificada hoy: corridas con `TMPDIR` propio, 0 crecimiento. Pero la suite de arte **no es portable**: pasa en esta VM porque su insumo canónico existe fuera del repo (ver B1). Un verde que depende del entorno es un verde a medias. |
| C9 Helpers antes que prosa | **P** en las puertas — **con la salvedad de B2** | Los helpers de las puertas viven en sus skills y están declarados. Pero 3 herramientas reales de `scripts/` no están declaradas en ningún documento vivo: existen sin que el sistema las presente (ver B2). |
| C11 Criterio de colocación | **P** (F9) | Por primera vez verificado con herramienta y no por barrido manual: `rameli validar` corrido y registrado en esta migración (registro de cierre con inventario + prueba de frío en `docs/MIGRACION-RAMELI-V0140.md`). El veredicto «P» convive con los hallazgos B1/B2: la capacidad está adoptada; los hallazgos son de la app, no de adopción. |
| C13 Pin + herramienta | **P** (F9) | Pin **0.14.0** hoy, con `rameli migrate` para el delta, `rameli lint`/`test` como puertas comparadas y `rameli validar` estrenado. La superficie `rameli init` (esqueleto `datos`) es **NA** para una app existente con su mapa ya declarado. |
| C19 Fase de mejora | **P** | Demostrada por tercera vez consecutiva: la migración cerró con alcance del delta y esta fase se abrió sola, con esta auditoría como primer insumo. |
| C20 Ruta de lectura | **P** | Adoptada en la fase post-v0.12.1 (12 rutas en `FLUJO-PIPELINE.md`, cobertura 9/9) y **actualizada por el reorden de datos**: sus punteros F1/F2/F4 ya resuelven a las rutas del hogar de la tienda (verificado hoy en el documento). Sigue siendo el índice de lo vivo — y es donde B2 deja su hueco: los 3 scripts no aparecen en ninguna ruta. |
| C21 Auditoría obligada | **P** (F9) | Su segunda aplicación es este documento: no diferida, corrida en la primera migración donde el delta la hacía obligada. |
| **C22 Validación de colocación** | **P** (F9) | Estrenada en este cierre: corrida antes/después, resultado clasificado hallazgo por hallazgo y protocolo cumplido con registro (inventario de herramientas + prueba de frío) en el documento de la migración. **Respuesta expresa a la nota v0.13.0: la primera corrida de `rameli validar` con registro está hecha; su FALLO vigente (chequeo 3) entra a esta fase como B1, sin moverse en la migración.** |
| **C23 Datos multi-unidad** | **P** (F1/F4/F7/F9) | **Fila expresa de la nota v0.14.0:** ¿mapa declarado? **Sí** — `rameli.json → datos`, declarado en `1e73e16` y registrado como adopción en esta migración (no re-decidido). ¿Hogares completos? **Sí** — la única tienda cumple 4/4 del hogar requerido y concentra su operación (config, registro, ledger, directriz, checkpoints, investigaciones, revisiones, registro de flujo). ¿Mecanismo fuera de los datos? **El chequeo 4 no halló código en `data/`** ni entradas sin declarar; el mecanismo vive en `skills/` y `scripts/`. El ciclo de vida de activos ya operaba como doctrina de la app (`ARQUITECTURA-DATOS.md`) — es el criterio que el framework promovió en esta versión. Único matiz: B3. |

**Confirmadas sin cambio** (evidencia de la matriz anterior,
revalidada por las corridas de hoy): C1 (P; lint verde
total), C2 (A en flujos operativos, P en F9), C3 (A;
`registro-flujo.md` instanciado por tienda, hoy dentro de su
hogar), C4 (P en las puertas), C6 (NA declarado como
práctica continua + A acotado, `docs/DELIMITACIONES-
ADOPCION.md` §3), C7 (P/A; sin disparadores de revalidación
vencidos detectados en esta pasada), C8 (P/A), C10 (A
declarado; ningún registro vivo presenta la Pieza 4 como
camino rival), C12 (P; barrido de la migración limpio en
vivos), C14 (P; lint en cero), C15 (P; el ciclo de
contribución que trajo C22 — PR #7 — se integró en Rameli
v0.13.0 con su auditoría en el PR), C16 (P; esta migración
se ejecutó como unidad en chat dedicado con brief, worktree
aislado y cierre verificado contra el repo), C17 (A/P;
registro por tienda dentro de su hogar + umbral de relevo
calibrado), C18 (P; checkpoints `estado-*.json` en el hogar
de la tienda).

## 4. Brechas reales

### B1 (C22 chequeo 3 / C5) — La suite de arte lee su diseño canónico desde fuera del repo

`skills/puerta-arte-propuesta/evals/test-regression.sh`
declara `K="$HOME/workspace/goals/pod-etsy-sistema-operativo-
q4-2026/files/disenos/canonicos"` y dos casos (P1 y F6) corren
contra `$K/vitals-stable-print-300dpi.png` (11 MB). Es el
**FALLO único** de la primera corrida de `rameli validar` y
el hallazgo que el framework ya tenía registrado al integrar
v0.13.0. Impacto: la regresión de la puerta de arte — la
puerta que más pesa en F1 — **no es reproducible con solo el
repo**: en un clon frío esos dos casos fallan por insumo
ausente, y en esta VM pasan por el entorno, no por el
sistema. Es la clase exacta de deuda «funciona porque el
entorno lo sostiene» que el chequeo 3 existe para cazar.
**En esta migración no se movió ningún archivo de diseño**
(decisión vigente del dueño, registrada en el encargo).
→ **P1**, con opciones para que el dueño elija la forma.

### B2 (C22 chequeo 1 / C9 / C20) — Tres scripts de `scripts/` sin declarar en ningún documento vivo

`rameli validar` reporta como AVISO a
`scripts/procesar-arte-propuesta.py` (procesa el arte crudo
a print-ready y corre la puerta con autotrim),
`scripts/reparar-fondo-casi-blanco.py` (repara fondos
casi-blancos, 2026-10-16) y `scripts/reporte-seo.py`
(cruza banco de keywords × ledger, «M4»). Clasificación
verificada: **no son entradas de cron** (ningún cron los
nombra), **no son huérfanos** (los tres tienen uso real
registrado en git, 2026-10-16/17) y **viven en su casa
correcta** (los `scripts/` compartidos de la app). La brecha
es de **declaración**: ningún `SKILL.md`, doc vivo ni ruta
de lectura los nombra, así que un chat frío no sabe que
existen, cuándo usarlos ni qué puerta los gobierna — el
inverso de B1: ahí un insumo declarado vive fuera; aquí
herramientas colocadas viven sin declarar. → **P2.**
*Nota post-fusión (cierre de la migración): en `main`
fusionado, `rameli validar` ya no reproduce estos 3 avisos,
porque los documentos de la migración/auditoría nombran a
los scripts y el corpus «vivo» del validador incluye todo
`docs/*.md`. La brecha sustantiva sigue abierta: la
declaración que falta es en el skill gobernante y en la
ruta de lectura, no en un registro fechado.*

### B3 (C23 chequeo 4, menor) — `data/cola-pins` declarado en el mapa no existe en un clon frío

El mapa declara `data/cola-pins` como global, y el
directorio existe en el disco del árbol principal — pero
está cubierto por `.gitignore` y vacío, así que **no existe
en git**: un worktree o clon nuevo nace sin él y
`rameli validar` levanta el aviso «declarado en el mapa pero
no existe». Impacto bajo (es AVISO, no FALLO, y el flujo lo
crea al operar), pero es una declaración que el repo por sí
solo no puede satisfacer: la misma clase de matiz que B1 en
miniatura. El mapa **no se re-decide en esta migración**;
las opciones quedan para el dueño. → **P3.**

## 5. Inventario arrastrado (no son brechas de adopción; reaparecen por la regla C19)

- **Reactivación del cron de propuestas (F1):** pausado,
  verificado en vivo hoy. La secuencia fijada por el dueño
  sigue vigente: primero pulir la personalización en su
  chat, después reactivar el cron — su reactivación servirá
  de prueba integral de que todo funciona. Es un **dale del
  dueño** pendiente, no una mejora de esta fase.
- **Re-revisión del dueño de la ubicación** de la playera
  p055 y la sudadera p056 recreadas (incidencia neck ya
  resuelta y cerrada el 2026-10-19): la hará él en otro
  chat; nada de esta fase depende de ella.
- De la fase de mejora post-v0.12.1 **no queda nada
  abierto**: P2 (fuga de `verificar-video.py`) y P1 (ruta de
  lectura) se ejecutaron y cerraron el 2026-10-19, y la
  segunda se revalidó hoy (rutas actualizadas por el
  reorden de datos, cobertura intacta).

## 6. Capacidades de la app sin contraparte en el framework (observación, sin cambio)

Patrones de resiliencia (`docs/PATRONES-RESILIENCIA.md`):
doctrina de la app, vigente, sin contraparte declarada en
Rameli v0.14.0. El criterio de ciclo de vida de activos
**dejó de ser** capacidad sin contraparte: hoy es parte de
C23 del framework (promovido desde esta app, reescrito sin
dominio, según el CHANGELOG de v0.14.0).
