# Auditoría de adopción — My POD × Rameli (2026-10-19)

> Encargo del dueño (dale 2026-10-19, chat de migración v0.11.0):
> recorrer **todas** las capacidades vigentes del framework contra
> **todos** los flujos de la aplicación, con veredicto por celda y
> evidencia en el repo — nada de memoria. Este documento ES el
> entregable del piso 1. **Nada de lo propuesto aquí se ejecuta sin
> su dale aparte, en este chat; la fusión de esta rama a `main`
> también espera su dale.**

## Método y bases verificadas

- **Framework de referencia:** repo `rameli`, `main` en `2425c2f`,
  `VERSION` = **0.11.1** (fuente de verdad). Capacidades tomadas
  SOLO de documentos vigentes en ese repo (ver inventario §1).
  Lo que no está integrado en `main` de Rameli **no** es capacidad
  vigente: el PR #3 (`contribucion-ruta-de-lectura`) está en
  revisión en otro chat y aquí solo se cita como pendiente, nunca
  como doctrina.
- **Aplicación auditada:** repo `my-pod`, `main` en `3345df7`
  (árbol limpio y sincronizado al abrir la auditoría), pin
  declarado **0.11.0** (`rameli.json`, frontmatter de los 9 skills,
  README). **La app tiene 9 skills** (no 10: `puerta-publicacion-pod`
  se eliminó al cerrar la fase de mejora).
- **Verificaciones corridas en vivo para esta auditoría**
  (2026-10-19): `rameli lint` sobre los 9 skills → **verde total**;
  suite de `puerta-arte-propuesta` → **13/13**; suite de
  `puerta-pinterest-pin` → **15/15**; estado de crons consultado
  (propuestas **pausado**, Pinterest **activo**, estratega e
  investigación **activos**); cuerpos de cron leídos y comparados
  contra los skills que invocan.
- **Precedente parcial:** el registro de adopción de workers por
  flujo en `docs/MIGRACION-RAMELI-V0110.md` (§"Registro de
  adopción") y su cierre en `docs/FASE-MEJORA-V0110-PROPUESTA.md`
  (P4). Esta auditoría lo generaliza; donde el precedente ya
  declaró un veredicto y la evidencia sigue en pie, se confirma —
  no se re-decide.
- Donde la evidencia en el repo no alcanza, la celda dice
  **sin evidencia** y no se sustituye por memoria.

## Leyenda de veredictos

| Código | Significado |
|---|---|
| **P** | Adoptado y probado — hay evidencia de uso real (corrida, suite verde, cierre verificado) |
| **A** | Adoptado sin estrenar — está escrito/instanciado, sin corrida real que lo pruebe todavía |
| **NA** | No aplica — con motivo declarado |
| **B** | Brecha real — remite a la propuesta `P-n` de §4 |
| **SE** | Sin evidencia — el repo no permite verificarlo |

---

## 1. Inventario de capacidades vigentes de Rameli v0.11.1

Fuente entre paréntesis (ruta en el repo `rameli`):

- **C1 — Formato estándar de skills + revelado progresivo.**
  `SKILL.md` + `scripts/` + `references/`; metadata → cuerpo →
  referencias. (`docs/formato-skills.md`, `docs/arquitectura.md`
  Pieza 1, `skills/_plantilla/SKILL.md`)
- **C2 — Constructor de skills y su ciclo de vida.**
  Descubrir (INTAKE con dale por fase) → diseñar → construir →
  probar → versionar. Un skill = un trabajo. (`skills/fabrica-skills/
  SKILL.md` v0.5.0, `INTAKE.md`)
- **C3 — Plantillas operativas.** Del constructor (CUERPO,
  ESTADO-DE-CORRIDA, EVALUACION, GRAFO, RECETA, SESION) y de la
  raíz (`templates/brief-unidad.md`, `templates/registro-flujo.md`):
  la doctrina no vive solo en prosa. (`skills/fabrica-skills/
  templates/`, `templates/`)
- **C4 — Puertas mecánicas en código.** La puerta verifica
  contenido con código (schema-gate, verifier-repair, comandos,
  comparación contra dorado, `blocked`); existir ≠ verificado;
  toda corrección nombra el criterio violado.
  (`skills/fabrica-skills/references/gates.md`,
  `docs/formato-skills.md` extensión 2)
- **C5 — Evals y regresión, capa determinista.** Cada fallo real →
  caso de regresión permanente; la suite (`evals/`, declarada en
  `regression_suite`) es la suite de aceptación del skill; sin
  evals el skill no se acepta. (`docs/evals.md`,
  `skills/fabrica-skills/references/regresion.md`)
- **C6 — Evals, capa de juicio + evaluación del constructor.**
  Juicio con modelo (promptfoo/deepeval) para lo no medible por
  código; A/B contra genérico, huella, deriva y contradicción como
  aceptación de skills nuevos. (`docs/evals.md`,
  `skills/fabrica-skills/templates/EVALUACION.md`)
- **C7 — Calibraciones (mecanismo vs aplicación).** Sección
  obligatoria desde v0.8.0: todo umbral declara MECANISMO o
  CALIBRACIÓN con instancia, fecha y disparador de revalidación.
  (`skills/_plantilla/SKILL.md`, CHANGELOG v0.8.0)
- **C8 — Reglas con motivo.** Toda regla lleva fecha, caso que la
  originó y qué se rompe si se ignora. (`docs/formato-skills.md`
  extensión 3)
- **C9 — Helpers antes que prosa.** Lo mecánico vive en `scripts/`
  y se ejecuta; no se duplica en el prompt. (`docs/formato-skills.md`
  extensión 4)
- **C10 — Orquestación determinista.** Grafo fijo y versionado;
  ningún modelo decide el flujo; en el runtime: `agent()` con
  `schema`, `parallel()` barrera, `pipeline()`, `blocked`,
  workflows guardados + snapshots. (`docs/arquitectura.md` Pieza 4,
  `skills/fabrica-skills/references/workflow-patterns.md`)
- **C11 — Criterio de colocación + auditoría de colocación.**
  Prueba de quitar el dominio; checklist al cerrar una fase o
  tocar un skill. (`skills/fabrica-skills/references/
  criterio-colocacion.md`)
- **C12 — Terminología canónica.** Framework / aplicación / ficha;
  términos retirados fuera de documentos vivos. (CHANGELOG v0.9.0,
  `MIGRACIONES.md` guía v0.9.0)
- **C13 — Versionado y herramienta.** SemVer; la app pinea y migra
  deliberadamente, sin propagación automática; `bin/rameli`
  (`init`, `new-skill`, `lint`, `test`, `migrate`) se usa, no solo
  se lee. (README, `MIGRACIONES.md`, `docs/INICIO-RAPIDO-IAS.md`)
- **C14 — Lint / higiene de formato.** Gates mecánicos del formato
  (frontmatter, descripción ≤220, "Cuando usarme", puertas o
  procedimiento, CHANGELOG, scripts ejecutables, placeholders).
  (`bin/rameli lint`, `skills/fabrica-skills/scripts/
  verificar-skill.sh`)
- **C15 — Contribuciones por PR.** Checklist operativo de 8 pasos:
  rama → auditoría de colocación → push verificado → PR → revisión
  en el PR → merge + bump + CHANGELOG + **actualizar el estado
  declarado de lo integrado** → borrar rama → cierre verificable.
  Preparar ≠ abrir ≠ integrar. (`docs/CONTRIBUCIONES.md`)
- **C16 — Ejecución por workers fríos + brief limpio.** El chat
  principal decide; la unidad la ejecuta un worker sin herencia,
  con brief (objetivo, línea base, alcance, puertas citadas,
  entregable — nunca el cómo) + el repo; cierre por verificación
  contra el repo con **watchdog** montado al lanzar; no aplica a
  tareas de 1–2 pasos. (`docs/EJECUCION-POR-WORKERS.md` — doctrina
  vigente desde v0.10.0, encabezado corregido en v0.11.1)
- **C17 — Registro de flujo versionado + relevo del orquestador.**
  Registro por flujo en el repo (unidades, decisiones, veredictos,
  siguiente paso), distinto del checkpoint fino; el orquestador
  rota entre unidades, el entrante lee ficha → registro → briefs →
  sistema y verifica el estado antes de operar. (mismo doc +
  `templates/registro-flujo.md`)
- **C18 — Checkpoints de ejecución con resume.** Estado de corrida
  por unidad: una corrida que muere se retoma sin repetir trabajo;
  `blocked` pausa limpio. (`templates/ESTADO-DE-CORRIDA.md`, doc
  de workers §dos capas) — *Nota de colocación:* los patrones
  P1 (health-check) y P3 (reintentos acotados) con los que esta app
  lo opera viven en `docs/PATRONES-RESILIENCIA.md` **de la app**;
  el framework vigente no los declara con ese detalle.
- **C19 — Fase de mejora encadenada post-migración.** La migración
  cierra con alcance del delta y abre sola la fase de mejora:
  inventario de brechas → propuesta (qué cambia, impacto, riesgo,
  orden) → ejecución solo con dale, como fase propia; si se
  difiere, queda registrada y reaparece en la siguiente migración.
  (`MIGRACIONES.md`, v0.11.0)

*Capacidades de la app sin contraparte en el framework vigente*
(no son filas de la matriz; se evalúan en §5): patrones de
resiliencia P1/P3, criterio de ciclo de vida de activos
(`ARQUITECTURA-DATOS.md`, 2026-10-19) y la ruta de lectura por
tarea (hoy solo existe como propuesta en el PR #3, no vigente).

## 2. Inventario de flujos de My POD

Estado operativo verificado el 2026-10-19 (crons + repo):

- **F1 — Propuestas diarias.** Cron `equipo-pod-propuestas-diarias`
  (18:00): arte con puerta → drafts en Printify → ensamblaje MPL →
  registro. **Pausado por el dueño** desde 2026-10-18 (tras el fallo
  de recortes); la puerta nueva quedó verde el 2026-10-19 y la
  reactivación espera su dale. Checkpoint:
  `data/estado-propuestas.json`.
- **F2 — Publicación por lote.** `publicador-lote` (un worker por
  lote, manifiesto del dueño) sobre `publicar-printify-etsy`
  (M3→M9) + `paquete-listing-etsy` + videos. Bajo demanda; sin lote
  desde que el watchdog se hizo obligatorio (P4, 2026-10-19).
  Checkpoint: `data/estado-publicacion.json`.
- **F3 — Pinterest diario.** Cron `equipo-pod-pinterest-diario`
  (08:50, **activo**): `estratega-pinterest` decide la parrilla,
  `puerta-pinterest-pin` valida, se publica con links rastreables.
  Checkpoint: `data/estado-pinterest.json`. Corrida de hoy
  registrada en `main` (`3345df7`).
- **F4 — Dirección semanal.** Crons de investigación y estratega
  (lunes), trend-scan (lun/jue) y rituales de lunes/viernes,
  **activos**: producen `data/direccion-tienda.md` +
  `data/config-propuestas.json` (vigencia 7 días).
- **F5 — Onboarding de tienda.** `onboarding-tienda`: de cero a
  tienda operativa, por fases con dale. Probado con la tienda
  29222324; **sin estrenar para una segunda tienda**.
- **F6 — Conexión Etsy API por tienda.** `conectar-etsy-api`:
  Seller App → OAuth PKCE → tokens → registro en el config.
  Probado con una tienda (2026-10-16, primera escritura real por
  API el mismo día); flujo interactivo con el dueño presente.
- **F7 — Operación comercial por API/scripts.** Precios por
  variación (`scripts/precios-variacion-api.py` +
  `verificar-precios.py`), ledger de ventas M2
  (`scripts/import-ventas-etsy.py`), sincronización del registro
  con Printify (`scripts/sincronizar-registro-printify.py`),
  ofertas y calendario en el config de la tienda. **Sin skill
  dueño único**: lo consumen F2/F4 y crons puntuales.
- **F8 — Puertas transversales.** `puerta-arte-propuesta`,
  `puerta-pinterest-pin`, y las puertas de paquete y de
  listos-para-publicar dentro de sus skills: gates mecánicos que
  corren DENTRO de otros flujos, por vía directa (declarado así en
  el registro de adopción de la migración).
- **F9 — Mantenimiento del sistema.** Migraciones de framework,
  fase de mejora, contribuciones, lint/test, ciclo de vida de
  activos. Probado el 2026-10-19 de punta a punta (migración
  v0.11.0 + fase de mejora P1–P4 cerradas + rama de ciclo de vida
  fusionada).

---

## 3. Matriz capacidad × flujo

| Cap. | F1 Prop. | F2 Lote | F3 Pins | F4 Direc. | F5 Onb. | F6 API | F7 Comerc. | F8 Puertas | F9 Sist. |
|---|---|---|---|---|---|---|---|---|---|
| C1 Formato + revelado | P | P | P | P | P | P | A¹ | P | P |
| C2 Constructor / ciclo de vida | A² | A² | A² | A² | A² | A² | SE | A² | P |
| C3 Plantillas operativas | A³ | A³ | A³ | A³ | NA⁴ | NA⁴ | SE | NA⁴ | P |
| C4 Puertas mecánicas | P | P | P | NA⁵ | A | A | P⁶ | **P** | P |
| C5 Regresión determinista | P⁷ | **B** | P | **B** | **B** | **B** | SE | **P**⁷ | P |
| C6 Juicio / A-B del constructor | SE | SE | SE | SE | SE | SE | SE | SE | **B** |
| C7 Calibraciones declaradas | P | **B** | P | **B** | **B** | **B** | A | P | P |
| C8 Reglas con motivo | P | P | P | A | A | A | A | P | P |
| C9 Helpers antes que prosa | P | P | P | A | A | P | P | P | P |
| C10 Orquestación determinista | A⁸ | A⁸ | A⁸ | A⁸ | NA⁹ | NA⁹ | A⁸ | NA¹⁰ | SE |
| C11 Criterio de colocación | SE | SE | SE | SE | SE | SE | SE | SE | P |
| C12 Terminología canónica | P | P | P | P | P | P | P | P | P |
| C13 Pin + herramienta `rameli` | — | — | — | — | — | — | — | — | **B**¹¹ |
| C14 Lint de formato | P | P | P | P | P | P | — | P | P |
| C15 Contribuciones por PR | NA¹² | NA¹² | NA¹² | NA¹² | NA¹² | NA¹² | NA¹² | NA¹² | **P** |
| C16 Workers fríos + brief + watchdog | P¹³ | P/A¹⁴ | P | P | NA¹⁵ | NA¹⁵ | A | NA¹⁶ | P |
| C17 Registro de flujo + relevo | A | A | A | A | A | A | SE | NA¹⁶ | P/A¹⁷ |
| C18 Checkpoints + resume | P | P | P | A | A | NA¹⁸ | A | NA¹⁰ | P |
| C19 Fase de mejora encadenada | — | — | — | — | — | — | — | — | **P** |

Notas de celda (el motivo manda sobre el código):

1. **C1×F7 = A:** F7 no tiene skill propio; el formato aplica a los
   scripts y docs que lo sostienen, sin `SKILL.md` que lo declare
   (ver brecha B6).
2. **C2 = A en los flujos operativos:** los 9 skills existen en el
   formato y con su CHANGELOG, pero en el repo de la app **no hay
   evidencia** de que cada uno haya pasado el ciclo completo del
   constructor (intake con dale, A/B, optimización) — nacieron en
   sesiones de trabajo y se endurecieron por fallos reales. El
   ciclo sí se ejerció en F9 al crear/eliminar skills con puertas
   (p. ej. la eliminación de la puerta legacy, 2026-10-19).
3. **C3 = A:** la única plantilla instanciada en la app es
   `registro-flujo.md` (por tienda, P4). No hay instancias de
   `brief-unidad.md` en el repo: los briefs de lote viven como
   manifiesto del `publicador-lote` y los de cron como cuerpo del
   cron — formas equivalentes declaradas en el registro de
   adopción, pero la plantilla del framework como tal está sin
   estrenar.
4. **C3×F5/F6/F8 = NA:** flujos guiados o gates internos; no
   producen briefs de unidad ni registros propios — su estado vive
   en el registro de flujo de la tienda.
5. **C4×F4 = NA con matiz:** la estratega es un flujo de decisión
   (juicio), no de verificación: su "puerta" es el veredicto del
   dueño sobre la directriz. El framework exime lo que no se puede
   medir con código pasándolo a la capa de juicio (C6) — que está
   sin evidencia (ver B5).
6. **C4×F7 = P acotado:** `verificar-precios.py` y el sync con
   códigos de salida (0/2 CONFLICTO) son puertas reales y usadas;
   el resto de F7 verifica por lectura del operador.
7. **C5×F1/F8 = P por las puertas:** las suites que corren en F1 y
   F8 son las de las puertas (arte **13/13** y pin **15/15**,
   verificadas en vivo hoy). La brecha de C5 está en los skills
   sin suite (F2/F4/F5/F6): ver B2.
8. **C10 = A en los flujos de cron/lote:** el grafo es fijo y está
   versionado **como texto** (cuerpos de cron + `FLUJO-PIPELINE.md`
   + procedimiento del skill), con puertas en scripts — pero las
   primitivas del runtime que la Pieza 4 declara (`agent()` con
   schema como gate en código, workflows guardados con snapshot)
   **no se usan** en ningún flujo de la app, y no hay declaración
   de no-adopción con motivo. Ver B7.
9. **C10×F5/F6 = NA:** flujos interactivos guiados con el dueño;
   no hay grafo repetible que fijar todavía (una sola corrida real
   cada uno).
10. **C10/C18×F8 = NA:** las puertas son funciones puras sin estado
    ni flujo propio; el estado lo lleva el flujo que las invoca.
11. **C13×F9 = B no por el pin, por el registro:** pinear 0.11.0
    con el framework en 0.11.1 es legal (migración deliberada),
    pero **la app no registra en ningún documento que 0.11.1
    existe** ni la decisión de adoptarlo o diferirlo; además quedan
    declaraciones vivas desactualizadas (ver B1).
12. **C15 = NA fuera de F9:** las contribuciones son un flujo del
    mantenimiento del sistema, no de la operación de la tienda.
13. **C16×F1 = P con la salvedad de B3:** el cron opera como worker
    con checkpoint y watchdog del sistema (vigía de 30 min), pero
    su cuerpo **no invoca la puerta de arte vigente completa**
    (v0.5.0) — la adopción del modelo es real, la del contenido
    quedó atrás.
14. **C16×F2 = P/A:** el modelo (worker por lote + manifiesto-brief)
    está probado en lotes reales; el **watchdog obligatorio**
    (P4, 2026-10-19) está adoptado en el skill v0.1.2 y **sin
    estrenar**: ningún lote ha corrido desde entonces.
15. **C16×F5/F6 = NA declarado:** onboarding y conexión API son
    guiados con el dueño (decisiones por fase / clic OAuth) —
    motivo ya registrado en `docs/MIGRACION-RAMELI-V0110.md`.
16. **C16/C17×F8 = NA declarado:** las puertas corren dentro de
    cualquier flujo por vía directa; no son unidades de producción
    ni flujos con registro propio.
17. **C17×F9 = P/A:** cada fase de sistema deja su registro
    versionado (migración, fase de mejora, esta auditoría) — eso
    es P; el **relevo formal del orquestador** (con verificación
    del entrante anotada en el registro) está calibrado en
    `docs/EJECUCION-Y-RELEVO.md` y **sin estrenar**: el registro de
    la tienda dice textualmente que el primer relevo se anotará
    cuando ocurra. Los relevos de hecho (este encargo nació en otro
    chat) no se han anotado.
18. **C18×F6 = NA:** la conexión es una corrida interactiva corta;
    su "resume" es el refresh de tokens, documentado en el skill.

### Lectura de conjunto (lo que la matriz dice en una frase)

La app está **probada** en lo que usa a diario (formato, lint,
puertas de arte y de pin con sus suites, checkpoints, workers de
cron, terminología, contribuciones y la cadena
migración→fase-de-mejora) y **declarada pero sin estrenar** en la
segunda capa del modelo de workers (watchdog de lote, relevo
formal, plantilla de brief). Las **brechas reales son ocho** y se
concentran en cuatro temas: declaraciones que el repo no sostiene
(suites vacías, calibraciones ausentes, pin y textos desfasados,
remanentes sin estado), una puerta endurecida que su flujo
principal no invoca completa, la capa de evaluación por juicio —
que no existe ni como exención declarada — y dos delimitaciones
sin declarar (el flujo comercial F7 y la orquestación del
runtime).

---

## 4. Brechas reales → propuestas

Cada propuesta: qué cambia, impacto, riesgo y orden. Ninguna se
ejecuta sin dale del dueño; con dale, cada una corre como trabajo
propio (rama y puertas propias), no mezclada con las demás.

### B1 → Propuesta 3 — Pin sin registro del delta y declaraciones vivas desfasadas

**Evidencia:** el framework vigente es **0.11.1** y la app pinea
**0.11.0** sin que ningún documento de la app registre que 0.11.1
existe ni la decisión de adoptarlo o diferirlo. El desfase en sí
es legal (migración deliberada); el hueco es la ausencia de
registro. En la misma condición: el README dice "los 10 skills"
en sus dos secciones de migración (hoy son 9); el cuerpo del cron
de propuestas dice "Rameli v0.9.0"; el README describe
`data/registro-listings.json` como "4 listings, 44 assets" (el
registro real tiene decenas de claves); y tres skills traen la
línea de versión del cuerpo distinta a la del frontmatter
(`conectar-etsy-api` 0.1.0 vs 0.1.1, `estratega-tienda` 0.4.0 vs
0.5.1, `publicar-printify-etsy` 0.7.0 vs 0.7.2 — el lint solo
verifica que la línea exista, no que coincida).

**Qué cambia:** decidir el pin (subir a 0.11.1 — delta de parche:
encabezado de doctrina, `bin/rameli` ejecutable y un paso del
checklist de contribuciones; cero cambios de comportamiento — con
su mini-registro, o registrar el diferimiento con motivo y fecha
de revisión) y corregir en la misma pasada todas las
declaraciones vivas listadas arriba.
**Impacto:** un lector frío deja de encontrar tres versiones del
estado del sistema. **Riesgo:** bajo. **Orden: 3.**

### B2 → Propuesta 2 — Suites de regresión declaradas pero vacías, y skills sin suite

**Evidencia:** `paquete-listing-etsy` y `publicar-printify-etsy`
declaran `regression_suite: "evals/"` en su frontmatter, pero sus
`evals/` están **vacíos y sin un solo archivo versionado** (un
directorio vacío ni siquiera existe para git): la declaración no
la sostiene el repo. Otros cinco skills (`conectar-etsy-api`,
`estratega-pinterest`, `estratega-tienda`, `onboarding-tienda`,
`publicador-lote`) no tienen `evals/` ni declaran suite. El
framework es explícito: sin evals, el skill no se acepta, y cada
fallo real se convierte en caso permanente. Hoy `rameli test`
solo ejercita de verdad 2 de 9 skills (las dos puertas, 13/13 y
15/15).

**Qué cambia:** (a) crear las suites reales de los dos skills que
la declaran, sobre sus scripts de puerta ya existentes
(`verificar-paquete.py`, `verificar-listos-publicar.py`), con
fixtures conocido-bueno/conocido-malo versionados; (b) para los
cinco restantes, suite de contrato mínima o declaración explícita
en el skill de "sin suite — motivo", retirando cualquier
declaración que no se sostenga.
**Impacto:** la regresión pasa a ser veraz en 9/9 y los fallos
futuros de paquete/publicación tienen dónde volverse prueba.
**Riesgo:** bajo (aditivo; las puertas ya se usan a mano).
**Orden: 2.**

### B3 → Propuesta 1 — El cron de propuestas no invoca la puerta de arte vigente completa

**Evidencia:** `puerta-arte-propuesta` v0.5.0 (endurecida el
2026-10-18 tras los drafts cortados p038–p057) manda en su
procedimiento: paso **1b** — composición sobre el CRUDO con
`--es-original` **antes** de procesar — y paso **3** con
`--original CRUDO.png` para la fidelidad de recorte. El cuerpo del
cron `equipo-pod-propuestas-diarias` (leído íntegro en esta
auditoría) ejecuta solo limpieza → autotrim → puerta con
`--exigir-margen-zoom`: **nunca corre 1b ni pasa `--original`**, y
describe el autotrim con el criterio anterior ("alfa>=128 +4px",
no el bbox seguro). Es decir: la puerta que nació del desastre de
recortes **no correría completa en su flujo principal** cuando el
cron se reactive. El skill está bien; el consumidor quedó atrás.

**Qué cambia:** actualizar el cuerpo del cron (vive en el sistema
de crons, no en este repo) para seguir el procedimiento del skill
paso a paso: conservar el crudo como artefacto del lote (ruta en
el registro/checkpoint), correr 1b antes de tocar el arte, y el
paso 3 con `--original`; corregir la descripción del autotrim y
el pin citado. Nada cambia en el skill.
**Impacto:** alto — cierra la única vía por la que el fallo de
recortes puede volver con la puerta "existiendo".
**Riesgo:** bajo-medio (el cron está pausado: ventana segura;
mitigación: diff paso a paso contra el skill y una corrida de
prueba con un diseño antes de reactivar en serio).
**Orden: 1 — condición previa recomendada para reactivar F1.**

### B4 → Propuesta 4 — Calibraciones sin la sección obligatoria en 4 skills

**Evidencia:** `conectar-etsy-api`, `estratega-tienda`,
`onboarding-tienda` y `publicador-lote` no tienen sección
"Calibraciones (mecanismo vs aplicación)" (obligatoria en la
plantilla desde v0.8.0). Varios de sus umbrales sí existen, pero
dispersos en el cuerpo, sin declarar naturaleza ni disparador de
revalidación (p. ej. la estratega discute mecanismo/calibración
de precios en prosa y en su historial, sin la sección).

**Qué cambia:** agregar la sección a los 4 skills extrayendo los
umbrales que ya usan y declarándolos MECANISMO/CALIBRACIÓN con su
disparador. Sin cambiar ningún valor ni comportamiento.
**Impacto:** la próxima calibración parte del escenario correcto
en vez de fosilizar el anterior. **Riesgo:** bajo (documental).
**Orden: 4.**

### B5 → Propuesta 7 — Capa de juicio y A/B del constructor: ni adoptados ni exentos

**Evidencia:** no hay en el repo rastro de promptfoo/deepeval, ni
de una sola evaluación A/B contra genérico, ni de análisis de
varianza para ningún skill de la app (**sin evidencia** en las 9
columnas de C6). Tampoco hay una declaración de no-adopción con
motivo: el hueco no es que falte la capa — es que nadie decidió
su estatus, y cada auditoría futura lo volverá a "descubrir".

**Qué cambia:** declarar el estatus en la app: la capa de juicio
no se adopta como práctica continua (motivo: su costo y que el
juicio real ya lo ejercen las puertas humanas del dueño — arte,
directriz, paquete), y el A/B se adopta solo al crear un skill
nuevo o subir uno de versión mayor, registrado en su CHANGELOG.
**Impacto:** convierte un hueco recurrente en decisión revisable.
**Riesgo:** bajo. **Orden: 7.**

### B6 → Propuesta 6a — F7 (operación comercial) sin dueño declarado

**Evidencia:** los scripts de precios, ledger y sincronización
viven en `scripts/` de la raíz y los invocan crons y otros skills,
pero **ningún skill ni doc declara el flujo completo** (qué lo
dispara, qué puerta lo cierra, qué config manda). Es el único
flujo operativo sin ficha de flujo: su procedimiento vive
repartido entre cabeceras de scripts y cuerpos de cron.

**Qué cambia:** declarar dueño y ruta del flujo en un doc de la
app (disparadores, puertas — `verificar-precios.py`, el sync con
código 2 —, configs que mandan, y qué skill lo consume). Skill
propio solo si abre la segunda tienda o el flujo crece.
**Impacto:** F7 pasa de "sin evidencia" a flujo auditable sin
construir nada. **Riesgo:** bajo. **Orden: 6 (junto a B7).**

### B7 → Propuesta 6b — Orquestación determinista del runtime: sin usar y sin declarar

**Evidencia:** ningún flujo de la app usa las primitivas de la
Pieza 4 (workflows guardados con snapshot, gates en código sobre
`agent()` con schema, verifier-repair programado). Lo que sí hay
es el equivalente a esta escala: grafo fijo como texto versionado
(cuerpos de cron, `FLUJO-PIPELINE.md`, procedimientos) + puertas
en scripts. Pero a diferencia del modelo de workers — que sí
tiene registro de adopción por flujo — **esta no-adopción no está
declarada en ninguna parte**.

**Qué cambia:** registrar la no-adopción deliberada por flujo con
su motivo y el disparador que la reabriría (p. ej. un flujo donde
un gate deba decidir en código sobre salidas de varios agentes en
paralelo). Sin construir orquestación nueva.
**Impacto:** la matriz deja de marcar SE en C10 y la decisión
queda para quien migre después. **Riesgo:** bajo. **Orden: 6.**

### B8 → Propuesta 5 — El criterio de ciclo de vida de activos, sin aplicar a sus propios remanentes

**Evidencia:** el criterio (adoptado el 2026-10-19 en
`ARQUITECTURA-DATOS.md`) manda que el checkpoint muera con su
flujo y que todo activo tenga hogar y estado; sin embargo:
`data/estado-correccion-recortes.json` — checkpoint de un flujo
**cerrado** — sigue versionado en la raíz de `data/`;
`artwork-recuperado/` y `data/candidatos-p037/` están versionados
sin estado declarado en ningún doc; `data/auditoria-2026-10-15/`
sobrevive sin que el repo declare si es historia que se queda; y
existe un `evals/` vacío en la raíz (solo en disco). La pasada de
ciclo de vida ya fusionada (`0142f2c`) resolvió los canónicos en
riesgo y dejó estos ítems **esperando la palabra del dueño** —
esta propuesta es esa palabra, ítem por ítem.

**Qué cambia:** resolver cada ítem con su dale: borrar el
checkpoint cerrado dejando su huella en el registro de flujo
(ya está resumido ahí), declarar o retirar `artwork-recuperado/`
y `candidatos-p037/`, declarar la auditoría de 2026-10-15 como
registro histórico que se queda, y eliminar el `evals/` vacío.
Borrados por papelera recuperable, verificando referencias antes,
como en la pasada anterior.
**Impacto:** el criterio deja de tener excepciones visibles al
lado de su propio texto. **Riesgo:** medio-bajo (hay binarios;
mitigado por papelera y verificación ítem por ítem).
**Orden: 5.**

### Ruta de lectura por flujo — fuera de esta fase, con un arreglo previo

El framework vigente **no** declara una ruta de lectura por tarea
(solo el revelado progresivo general de C1): esa capacidad es
exactamente la del **PR #3, en revisión en otro chat** — no se
cuenta como vigente ni como brecha del framework. Del lado de la
app sí hay un daño ya presente y reparable sin esperar al PR: el
README (§"Criterios canónicos") apunta a tres archivos que **no
existen** (`CRITERIO-COLOCACION.md`,
`VISION-BIBLIOTECA-MOCKUPS-BORRADOR.md`,
`CAMINO-OPTIMIZADO-BORRADOR.md`). Si el PR #3 se integra, la
adopción en My POD será agregar la ruta por flujo a
`FLUJO-PIPELINE.md` y reparar esos punteros en la misma pasada;
si no se integra, los punteros se reparan igual dentro de la
Propuesta 3.

### Orden sugerido de ejecución (si hay dale)

| Orden | Propuesta | Por qué ahí |
|---|---|---|
| 1 | **P1** — cron de propuestas × puerta v0.5.0 completa (B3) | Bloquea la reactivación segura de F1 |
| 2 | **P2** — suites veraces en 9/9 (B2) | Sin regresión real, todo lo demás se verifica a mano |
| 3 | **P3** — pin 0.11.1 + declaraciones vivas (B1) | Ventana única de higiene del sistema |
| 4 | **P4** — calibraciones en 4 skills (B4) | Documental, sin riesgo, cierra C7 |
| 5 | **P5** — remanentes del ciclo de vida (B8) | Requiere su palabra ítem por ítem |
| 6 | **P6** — declarar F7 y C10 (B6+B7) | Dos SE convertidos en decisión |
| 7 | **P7** — estatus de la capa de juicio (B5) | Cierra el último SE estructural |

## 5. Capacidades de la app sin contraparte en el framework (observación)

- **Patrones de resiliencia P1/P3** (`docs/PATRONES-RESILIENCIA.md`):
  health-check previo y reintentos acotados con escalado, probados
  en los crons desde 2026-10-16. El framework vigente solo declara
  checkpoints/resume en general (C18). Pasan la prueba de quitar
  el dominio; si algún día suben, sería por contribución — **no**
  es el tema del piso 2 propuesto abajo.
- **Criterio de ciclo de vida de activos** (`ARQUITECTURA-DATOS.md`):
  doctrina de la app, aplicada a medias (ver B8). Tampoco tiene
  contraparte en el framework.
- **Ruta de lectura por tarea:** ver la nota tras B8 — vive hoy
  solo como PR #3 pendiente.

## 6. Recomendación sobre el piso 2 (contribución a Rameli)

**Recomendación: SÍ, abrir el piso 2 si el dueño aprueba esta
auditoría** — con el alcance acotado siguiente:

- **Qué se contribuye:** que `MIGRACIONES.md` incluya la auditoría
  de adopción (matriz capacidad × flujo con evidencia) como pieza
  de la fase de mejora, **obligada cuando el delta trae doctrinas
  o mecanismos nuevos** (como v0.10.0 trajo workers) y **diferible
  con motivo registrado cuando el delta es solo de parche** (como
  v0.11.1) — para que la obligación no se vuelva ceremonia en
  migraciones triviales.
- **Por qué la evidencia lo sostiene:** el registro parcial de
  workers (el precedente) no cazó B3 — una puerta endurecida cuyo
  flujo principal no la invoca completa — porque miraba solo el
  delta. La matriz completa lo cazó en una pasada. Ese es el caso
  real que la contribución debe citar.
- **Compatibilidad:** no rompe nada para las aplicaciones
  existentes: como todo en Rameli, adoptan al migrar; las que ya
  migraron a 0.11.x sin auditoría la incorporan en su siguiente
  fase de mejora, no retroactivamente.
- **Vía:** `rameli/docs/CONTRIBUCIONES.md`, checklist completo —
  rama `contribucion-auditoria-adopcion`, auditoría de colocación
  (la regla sobrevive sin el vocabulario POD: es mecanismo de
  migración, no de una app), push verificado con `git status -sb`,
  PR abierto (rama subida ≠ PR). **Sin tocar el PR #3**, que sigue
  su propia revisión.

## Estado de este documento

- Piso 1 **ejecutado**: auditoría completa en esta rama
  (`auditoria-adopcion-v0110`), sin tocar `main` ni ningún skill,
  script, dato o cron. La única escritura fuera de este repo fue
  ninguna — el cuerpo del cron de propuestas se leyó, no se editó
  (su corrección es la Propuesta 1, con dale).
- **Fusión a `main`: hecha el 2026-10-19** con el dale del dueño en
  este chat (merge `9ab05eb`, push verificado, rama eliminada).
- Piso 2: **abierto por el mismo dale** — ver el cierre abajo.

## Ejecución de las propuestas (2026-10-19, dale total del dueño)

El dueño dio dale a ejecutar TODAS las propuestas ("encárgate de
todo, sin dejar nada a medias") y a abrir el piso 2. Ejecución en
la rama `mejora-adopcion-v0111`, un commit por propuesta,
verificación total antes de fusionar (lint verde en los 9 skills;
`rameli test` verde: arte 13/13, pin 15/15, paquete 4/4, publicar
2/2, contrato de la estratega 13/13).

| Propuesta | Estado | Evidencia |
|---|---|---|
| P1 (B3) — cron de propuestas invoca la puerta de arte completa | **Ejecutada** | Cuerpo del cron actualizado paso a paso contra puerta-arte-propuesta v0.5.0: paso 1b `--es-original` sobre el crudo (que se conserva como artefacto del lote), autotrim descrito como bbox seguro, paso 3 con `--original` y manejo de `fidelidad_recorte`; línea "Rameli v0.9.0" corregida a v0.11.1. Verificado releyendo el job. **El cron sigue pausado**: su reactivación es un dale separado que el dueño no ha dado. |
| P2 (B2) — suites donde se declaraban | **Ejecutada** | Suites reales nuevas: paquete-listing-etsy (4/4, sobre `verificar-paquete.py` con fixtures versionados), publicar-printify-etsy (2/2, sobre `verificar-listos-publicar.py`), estratega-tienda (13/13, contrato del config de propuestas). Los 4 skills sin suite determinista posible (conectar-etsy-api, estratega-pinterest, onboarding-tienda, publicador-lote) llevan ahora la declaración explícita "sin suite — motivo" en su SKILL.md. Ningún skill declara ya una suite vacía. |
| P3 (B1) — pin y declaraciones vivas | **Ejecutada** | Pin a Rameli **0.11.1** en `rameli.json`, README y los 9 frontmatter; mini-registro del delta del parche en el README. Corregidas las declaraciones vivas: "los 10 skills" (hoy son 9), la descripción del registro de listings (conteo real) y las líneas de versión de cuerpo desalineadas (conectar, estratega-tienda, publicar). Los punteros rotos de "Criterios canónicos" del README se repararon en la misma pasada, apuntando a los cánones que sí existen (el PR #3 de Rameli sigue pendiente en su propio chat; si se integra, la ruta de lectura por flujo se adopta entonces). |
| P4 (B4) — secciones de Calibraciones | **Ejecutada** | Sección "Calibraciones (mecanismo vs aplicación)" agregada en conectar-etsy-api, estratega-tienda, onboarding-tienda y publicador-lote, extrayendo los umbrales que ya usaban, sin cambiar ningún valor. |
| P5 (B8) — ciclo de vida de remanentes | **Ejecutada** | El checkpoint de la corrección cerrada se renombró a `data/registro-correccion-recortes-2026-10-19.json` (registro fechado declarado en ARQUITECTURA-DATOS; referencias actualizadas). `artwork-recuperado/`: el arte final de quiet-night-shift se promovió a `data/artes-print/quiet-night-shift-print-300dpi.png` con nota honesta en el registro (bajo la puerta vigente da dpi insuficiente: es un legado aprobado, no un arte nuevo; el asset de producción vive en Printify); los sobrantes de generación y `data/candidatos-p037/` (el ganador ya vive en artes-print) fueron a la papelera recuperable, restaurables hasta el 2026-11-18. `data/auditoria-2026-10-15/` queda declarado como registro histórico. El `evals/` vacío de la raíz se eliminó. |
| P6 (B6+B7) — delimitaciones declaradas | **Ejecutada** | `docs/DELIMITACIONES-ADOPCION.md`: F7 (operación comercial por scripts) con dueño y ruta declarados (skill propio solo si abre una segunda tienda o el flujo crece), y no-adopción deliberada de las primitivas de orquestación de la Pieza 4, por flujo, con motivo y disparador de revisión. |
| P7 (B5) — capa de juicio | **Ejecutada** | Declarado en `docs/DELIMITACIONES-ADOPCION.md`: la capa de juicio con modelo no se adopta como práctica continua (las puertas humanas del dueño son el juicio real a esta escala); la evaluación A/B del constructor se adopta acotada — al crear un skill nuevo o subir versión mayor, registrada en su CHANGELOG. |
| Piso 2 — contribución a Rameli | **Ejecutada (PR abierto)** | Rama `contribucion-auditoria-adopcion` en el repo de Rameli: la auditoría de adopción como pieza obligada de la fase de mejora en `MIGRACIONES.md`, obligada cuando el delta trae doctrinas o mecanismos nuevos y diferible con motivo registrado en deltas de solo parche. Push verificado con `git status -sb` y **PR #4 abierto, pendiente de revisión**: https://github.com/ChrisBP-Dev/rameli/pull/4. Sin tocar el PR #3. La integración, el bump y el tag esperan su revisión en el PR, como manda CONTRIBUCIONES.md. |

**Lo que NO cambió:** ningún comportamiento de producción. El
cron de propuestas sigue pausado; ningún lote corrió; ninguna
puerta cambió de criterio (solo ganaron suites); los valores de
calibración son los mismos, ahora declarados.
