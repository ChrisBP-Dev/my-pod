# Auditoría de adopción — My POD × Rameli v0.12.1 (2026-10-19)

> Primer insumo de la fase de mejora abierta al cerrar la
> migración a Rameli v0.12.1 (`docs/MIGRACION-RAMELI-V0121.md`),
> como manda `rameli/MIGRACIONES.md`. En esta migración la
> auditoría **no era diferible** (el delta v0.12.0 trae
> capacidades nuevas) y la nota de migración exige que la matriz
> incluya expresamente la **ruta de lectura** y la **delimitación
> de orquestación**. Método: matriz completa de capacidades
> vigentes del framework × flujos de la aplicación, con veredicto
> y evidencia en el repositorio por celda — nada de memoria.
> Donde la evidencia no alcanza, la celda dice **sin evidencia**.
> **Nada de lo propuesto aquí se ejecuta sin el dale del dueño**;
> la propuesta vive en `docs/FASE-MEJORA-V0121-PROPUESTA.md`.

## Método y bases verificadas

- **Framework de referencia:** repo `rameli`, `main` en `e4d76f8`
  = `origin/main`, `VERSION` = **0.12.1**; tags anotados remotos
  `v0.12.0`/`v0.12.1` verificados con `ls-remote`. Capacidades
  tomadas SOLO de documentos vigentes en ese repo.
- **Aplicación auditada:** repo `my-pod`, `main` en `2dec8f7`
  (migración v0.12.1 fusionada y verificada), pin **0.12.1** en
  `rameli.json`, README y frontmatter de los **9 skills**.
- **Verificaciones corridas en vivo para esta auditoría**
  (2026-10-19): `rameli lint` sobre los 9 skills → **verde
  total**; `rameli test` → **verde total** (47 casos: arte 13,
  estratega-tienda 13, pin 15, paquete 4, publicar 2); estado de
  crons consultado en vivo (propuestas **pausado**, Pinterest
  **activo**, estratega/investigación/rituales/trend-scan
  **activos**, watchdog **activo**); barridos de pin, de ruta de
  lectura y de delimitación sobre los documentos vivos.
- **Precedente:** `docs/AUDITORIA-ADOPCION-V0110.md` (matriz
  contra v0.11.1, 8 brechas, las 7 propuestas ejecutadas con dale
  total del dueño + piso 2). Esta auditoría **confirma** los
  veredictos cuyas evidencias siguen en pie, **actualiza** los
  que las ejecuciones de aquella fase cambiaron y **agrega** las
  capacidades nuevas del delta. La numeración C1–C19 se conserva
  por comparabilidad; el delta suma **C20** y **C21**.

## Leyenda de veredictos

| Código | Significado |
|---|---|
| **P** | Adoptado y probado — evidencia de uso real (corrida, suite verde, cierre verificado) |
| **A** | Adoptado sin estrenar — escrito/instanciado, sin corrida real que lo pruebe |
| **NA** | No aplica — con motivo declarado |
| **B** | Brecha real — remite a la propuesta de la fase de mejora |
| **SE** | Sin evidencia — el repo no permite verificarlo |

---

## 1. Inventario de capacidades vigentes de Rameli v0.12.1

C1–C19 como en la auditoría anterior (formato de skills y
revelado progresivo; constructor y su ciclo de vida; plantillas
operativas; puertas mecánicas en código; evals deterministas;
evals de juicio + A/B del constructor; calibraciones mecanismo vs
aplicación; reglas con motivo; helpers antes que prosa;
orquestación determinista — Pieza 4; criterio y auditoría de
colocación; terminología canónica; versionado, pin y herramienta
`rameli`; lint de formato; contribuciones por PR; ejecución por
workers fríos + brief limpio + watchdog; registro de flujo y
relevo; checkpoints con resume; fase de mejora encadenada).
**Cambios del delta 0.11.1 → 0.12.1 sobre ese inventario:**

- **C10 — nota de delimitación (v0.12.0, PR #5):** la Pieza 4
  describe primitivas DISPONIBLES dentro de la doctrina única de
  workers, no un camino rival (`rameli/docs/arquitectura.md`,
  `rameli/docs/EJECUCION-POR-WORKERS.md`).
- **C15 — paso 6 endurecido (v0.12.1, PR #6):** integrar una
  versión exige tag anotado empujado **y Release de GitHub
  publicado y verificado como Latest**
  (`rameli/docs/CONTRIBUCIONES.md`).
- **C20 — Ruta de lectura por tarea (NUEVA, v0.12.0, PR #3).**
  Cada aplicación declara en su propio doc de flujo, por tipo de
  tarea o flujo vivo, las lecturas mínimas gobernantes como
  punteros puros (ruta + cuándo): piso, nunca techo; cobertura
  verificable (todo skill vivo en alguna ruta, todo puntero
  resuelve); retirar un flujo = retirar su ruta.
  (`rameli/skills/fabrica-skills/references/ruta-de-lectura.md`)
- **C21 — Auditoría de adopción obligada en la fase de mejora
  (NUEVA como pieza, v0.12.0, PR #4).** La fase de mejora no se
  alimenta del registro por delta: su primer insumo es esta
  matriz completa con evidencia por celda. Obligada cuando el
  delta trae capacidad nueva; diferible solo en parches, con
  motivo y fecha registrados. (`rameli/MIGRACIONES.md`)

## 2. Inventario de flujos de My POD (estado verificado hoy)

- **F1 — Propuestas (flujo v2).** `FLUJO-PIPELINE.md` §§1–2:
  Fase A = arte + puerta + **aprobación del dueño por diseño en
  el chat** (con su porqué); Fase B = drafts/MPL **solo de
  aprobados**. Piloto Fase A corrido el 2026-10-19: lote
  p058–p067 con puerta completa PASS (commit `56d8325`). Cron
  `equipo-pod-propuestas-diarias` **pausado** (verificado en
  vivo: deshabilitado desde 2026-10-18); su reactivación espera
  el dale del dueño. Checkpoint: `data/estado-propuestas.json`.
- **F2 — Publicación por lote.** Sin cambios desde la auditoría
  anterior (`publicador-lote`, un worker por lote); sin lote
  nuevo en el período — sin evidencia nueva.
- **F3 — Pinterest diario.** Cron **activo** (08:50, verificado
  en vivo); parrilla de `estratega-pinterest`, puerta
  `puerta-pinterest-pin`, links rastreables.
- **F4 — Dirección semanal.** Crons **activos** (verificado en
  vivo): investigación y estratega de lunes, trend-scan lun/jue,
  rituales de lunes y viernes.
- **F5 — Onboarding de tienda.** Sin corrida nueva; sigue sin
  estrenar para una segunda tienda.
- **F6 — Conexión Etsy API por tienda.** Sin corrida nueva;
  probado con una tienda (2026-10-16).
- **F7 — Operación comercial por API/scripts.** Declarado con
  dueño y ruta en `docs/DELIMITACIONES-ADOPCION.md` §1 (sin
  skill propio por decisión, con disparador de revisión).
- **F8 — Puertas transversales.** Suites verdes verificadas hoy:
  arte 13/13, pin 15/15, paquete 4/4, publicar 2/2, contrato de
  la estratega 13/13 (47 casos, 0 fallas).
- **F9 — Mantenimiento del sistema.** Probado hoy de punta a
  punta: migración a v0.12.1 (rama aislada, regresión comparada
  idéntica, fusión con dale, cierre verificado) y esta auditoría
  como apertura de su fase de mejora.

---

## 3. Matriz capacidad × flujo

Solo se listan las celdas cuyo veredicto **cambia** respecto de
la auditoría v0.11.1, las capacidades **nuevas** y las que el
delta toca; el resto se **confirma** con la evidencia de aquella
matriz, que sigue en pie (lint y regresión de hoy la revalidan).

| Cap. | Veredicto hoy | Evidencia / nota |
|---|---|---|
| C5 Regresión determinista | **P** en F8/F1 (suites de puertas y del contrato); **A declarado** en F2/F4/F5/F6 | La brecha anterior (skills sin suite sin declarar) se cerró en la fase post-v0.11.0: 5 suites reales (47 casos verdes hoy) y los 4 skills sin suite determinista posible llevan la declaración explícita "Sin suite determinista — declarado (2026-10-19…)" en su `SKILL.md` (conectar-etsy-api, estratega-pinterest, onboarding-tienda, publicador-lote — verificado por barrido). `rameli test` sigue imprimiendo AVISO por esos 4: es el aviso de la herramienta, no una declaración faltante de la app. **Pero ver B2:** la ejecución de las suites tiene una fuga ambiental nueva. |
| C6 Juicio / A-B | **NA declarado** (práctica continua) + **A acotado** | `docs/DELIMITACIONES-ADOPCION.md` §3: no se adopta como práctica continua con motivo (las puertas humanas del dueño son el juicio a esta escala); sí se adopta acotada — comparación contra genérico al crear un skill o subirlo de versión mayor, registrada en su CHANGELOG. La brecha anterior (estatus sin declarar) está cerrada. |
| C7 Calibraciones | **P/A** — sin disparadores vencidos detectados | Las secciones "Calibraciones (mecanismo vs aplicación)" se agregaron a los 4 skills que faltaban (fase post-v0.11.0, P4); el umbral de relevo quedó calibrado en `docs/EJECUCION-Y-RELEVO.md`. En esta pasada no se detectó ningún disparador de revalidación vencido en los documentos revisados. |
| C10 Orquestación (delimitación) | **A declarado** | `docs/DELIMITACIONES-ADOPCION.md` §2 (reescrito el 2026-10-19 por corrección del dueño): doctrina única de workers fríos; la Pieza 4 como capacidades disponibles, "no una doctrina rival". **Respuesta expresa a la nota v0.12.0: ningún registro vivo de adopción presenta la Pieza 4 como camino rival** (barrido verificado en la migración). La tabla de cierre de la auditoría anterior conserva la redacción de su época — historia fechada, no registro vivo. |
| C13 Pin + herramienta | **P** (F9) | La brecha anterior (0.11.1 existente y no registrado) se cerró dos veces: pin 0.11.1 en su fase y **0.12.1 hoy**, con `rameli migrate` usado para el delta y registro en `docs/MIGRACION-RAMELI-V0121.md`. |
| C15 Contribuciones por PR | **P** (F9) | El piso 2 de la auditoría anterior (PR #3 ruta de lectura, PR #4 esta auditoría, PR #5 delimitación) se integró en Rameli **v0.12.0** y el endurecimiento del paso 6 (Release) en **v0.12.1** — ciclo de contribución completo: rama → PR → revisión → integración con bump, CHANGELOG y estado actualizado (consta en el CHANGELOG del framework y en los merges de `main` de Rameli, verificados hoy). |
| C16 Workers fríos | **P** | Evidencia fresca de hoy: la migración v0.12.1 se ejecutó como unidad en chat dedicado con encargo-brief, worktree aislado y cierre verificado contra el repo; F1 corre ya su Fase A del flujo v2 (dale creativo por diseño en el chat) con piloto PASS. |
| C19 Fase de mejora | **P** | Demostrada por segunda vez consecutiva: la migración cerró con alcance del delta y esta fase se abrió sola, con esta auditoría como primer insumo. |
| **C20 Ruta de lectura** | **B** (todos los flujos) | Ver B1. |
| **C21 Auditoría obligada** | **P** (F9) | Su primera aplicación es este documento: no diferida, corrida en la primera migración donde el delta la hacía obligada. |

**Confirmadas sin cambio** (evidencia de la matriz anterior,
revalidada por las corridas de hoy): C1 (P; lint verde total),
C2 (A en flujos operativos, P en F9), C3 (A; `registro-flujo.md`
instanciado por tienda en `data/tiendas/29222324/`, plantilla de
brief sin instanciar como tal — los briefs viven como manifiesto,
cuerpo de cron o encargo de chat, declarado), C4 (P en las
puertas), C8 (P/A), C9 (P — con la salvedad de B2), C11 (P en
F9), C12 (P; barrido de la migración limpio en vivos), C14 (P;
lint en cero), C17 (A/P; registro por tienda + umbral de relevo
calibrado), C18 (P; checkpoints `data/estado-*.json` vivos).

## 4. Brechas reales

### B1 (C20) — La ruta de lectura no está declarada, y el inventario que la roza está incompleto

La app no declara en ningún doc vivo una ruta de lectura por
tarea (verificado: ninguna sección de ruta en `FLUJO-PIPELINE.md`
ni en otro doc; sus encabezados cubren etapas, no lecturas). Lo
más cercano, la sección "Skills activos" de `FLUJO-PIPELINE.md`,
lista **4 de los 9 skills vivos** (faltan conectar-etsy-api,
estratega-pinterest, estratega-tienda, onboarding-tienda y
publicador-lote) y no declara qué leer por tipo de tarea: es un
inventario parcial, exactamente el modo de fallo que el canon
C20 existe para prevenir (el caso origen del propio canon nació
en esta app). La auditoría anterior ya fijó el destino de
adopción: la ruta por flujo en `FLUJO-PIPELINE.md`. → **P1.**

### B2 (C5/C9) — Fuga de temporales de `verificar-video.py` que corrompe las corridas de regresión

`scripts/verificar-video.py::extract_frames` crea el directorio
de frames con `tempfile.mkdtemp()` y **nunca lo borra** (los
frames se cargan en memoria y el directorio queda abandonado;
contraste: `scripts/generar-video-listing.py` usa
`TemporaryDirectory()` correctamente). Medido hoy: una corrida
completa de `rameli test` fuga **4 directorios, ~143 MB** de
PNGs. Con `/tmp` en tmpfs de 512 MB, ~3 corridas lo llenan y la
siguiente corrida falla de forma engañosa: en la verificación
post-fusión de hoy, la suite de Pinterest dio 4 FAIL espurios
(sus JSON temporales salían vacíos por disco lleno) que
desaparecieron al limpiar y re-correr — la regresión quedó
idéntica y verde. Es un fallo de higiene de un helper (C9) con
impacto directo en la confiabilidad de la capa de regresión
(C5): una puerta que falla por el ambiente entrena a ignorarla.
→ **P2.**

## 5. Inventario arrastrado (no son brechas de adopción; reaparecen por la regla C19)

- **Reactivación del cron de propuestas (F1):** pausado desde
  2026-10-18; la puerta completa ya está invocada (fase
  post-v0.11.0), el flujo v2 está vigente y su piloto Fase A
  corrió hoy con PASS. La reactivación es un **dale del dueño**
  pendiente, no una mejora de esta fase.
- **Incidencia neck (4 componentes):** p055 playera, p056
  sudadera, p057 ambos quedaron sin el placeholder de la
  etiqueta de cuidados tras la corrección de recortes
  (`data/registro-correccion-recortes-2026-10-19.json`, estado
  CERRADO con este único pendiente). Decisión del dueño
  pendiente (recomendación registrada: recrear los 4 drafts
  duplicando un hermano sano, con dale nuevo).
- De la fase de mejora post-v0.11.0 **no queda nada abierto**:
  P1/P3/P4 cerradas, P2 cerrada por eliminación de la puerta
  legacy (decisión del dueño), P5 excluida por el dueño porque
  la contribución la ejecutó él — y su resultado es hoy parte
  del framework vigente (v0.12.0/v0.12.1), así que el ítem
  cierra por los hechos, no por olvido.

## 6. Capacidades de la app sin contraparte en el framework (observación, sin cambio)

Patrones de resiliencia P1/P3 (`docs/PATRONES-RESILIENCIA.md`) y
criterio de ciclo de vida de activos (`ARQUITECTURA-DATOS.md`):
doctrina de la app, vigentes, sin contraparte declarada en
Rameli v0.12.1. La ruta de lectura **dejó de ser** capacidad sin
contraparte: hoy es C20 del framework y brecha B1 de la app.
