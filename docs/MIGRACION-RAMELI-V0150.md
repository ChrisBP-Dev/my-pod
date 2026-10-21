# Migración a Rameli v0.15.0 — registro de ejecución (2026-10-20)

Encargo del dueño vía la sesión «Resume My Channels after
update»: primero la contribución al framework, aplicada;
después, actualizar las dos aplicaciones — para My POD con
dos condiciones expresas: **verificar primero que no haya
trabajo en vuelo que la migración pueda pisar** (había un
lote de publicación gestionado desde otro chat) y **auditar
dónde aplica el deber nuevo en vez de asumirlo**. La
contribución que origina el delta subió por la vía de
`rameli/docs/CONTRIBUCIONES.md`: **PR #8 de Rameli,
fusionado (merge `6c7bf39`), publicado como v0.15.0 (commit
`3576a02`, tag anotado `v0.15.0`, Release de GitHub)**.

La migración se ejecutó en worktree aislado sobre la rama
`migracion-rameli-v0150`, desde `main` en `9ba2776`. La
fusión a `main` quedó autorizada por el dueño en la orden
de la sesión, condicionada a las puertas comparadas y al
registro, como manda el sistema.

## Verificación previa — trabajo en vuelo (condición de la orden)

- **El lote de publicación Thanksgiving está CERRADO, no en
  vuelo.** Su checkpoint (`data/tiendas/29222324/
  estado-publicacion.json`) registra el cierre completo
  (11/11 `publicado_completo`, Fase C PASS, registro
  commiteado) sin fases en curso, y su última corrección
  (video2 de p046) se commiteó a las 20:23 EDT en
  `9ba2776` — el HEAD de `main` al abrir esta migración,
  minutos antes del inicio de la misión (20:45 EDT). El
  detalle y la evidencia viven en
  `docs/AUDITORIA-ADOPCION-V0150.md` §2.
- `main` limpia y sincronizada (`main == origin/main` en
  `9ba2776`), una sola rama, un solo worktree al abrir.
  Único rastro de otro trabajo: `tmp/
  paso1-investigacion-personalizacion.md` sin trackear —
  **no se toca** en esta migración (ni se commitea, ni se
  mueve, ni se borra).
- Crons vivos (Pinterest, dirección semanal, watchdog) no
  escriben código ni pines; el de propuestas sigue pausado
  por orden del dueño. La migración corre en worktree y la
  fusión re-verifica que `main` no se haya movido.
- Rameli: `main` en `3576a02`, `VERSION` = **0.15.0**, tag
  anotado remoto `v0.15.0` verificado con `ls-remote`.
- Delta confirmado con `rameli migrate --to 0.15.0`:
  **v0.15.0 solamente**, sin cambios rompientes (nota en
  `rameli/MIGRACIONES.md`). Capacidad nueva → la auditoría
  de adopción **no es diferible** y la nota exige la fila
  del corte (qué flujos cortan, dónde quedó el chequeo, qué
  no-aplica y por qué): corrida como
  `docs/AUDITORIA-ADOPCION-V0150.md`.

## Alcance aplicado

- `rameli.json`: pin 0.14.0 → 0.15.0 + nota de migración
  fechada. La clave `datos` queda **intacta**.
- Los **9 skills**: `framework_version: "0.15.0"` en su
  frontmatter.
- Tres CHANGELOG de skill cuya línea viva declara el pin
  («Pineado a Rameli v0.14.0») actualizados a v0.15.0
  (estratega-pinterest, puerta-arte-propuesta,
  puerta-pinterest-pin). Las entradas fechadas de los demás
  CHANGELOG son historia y no se tocaron.
- `README.md`: pin y sección de esta migración.
- Este registro, la auditoría de adopción
  (`docs/AUDITORIA-ADOPCION-V0150.md`) y la propuesta de la
  fase de mejora (`docs/FASE-MEJORA-V0150-PROPUESTA.md`).
- **Ningún dato se tocó: el diff de la rama contiene 0
  archivos bajo `data/` y 0 cambios al mapa `datos`.** La
  ficha de la tienda (`config.json`) solo se LEYÓ, para la
  auditoría. Nada se tocó fuera del repo (ni Etsy, ni
  Printify, ni Pinterest), y el archivo sin trackear de
  `tmp/` quedó como estaba.

## Registro de adopción — delta v0.15.0

**El corte en las puertas que la ficha declara (C24) —
auditado por flujo; su implementación donde aplica es la
fase de mejora encadenada (P1), con el dale del dueño dado
en la orden de esta sesión.** Resumen de la auditoría
(evidencia completa en su documento, §3):

- **F2 Publicación por lote — APLICA, brecha B1:** el agente
  principal corta la unidad (el manifiesto) contra la puerta
  de aprobación del dueño, pero `publicador-lote` no manda
  leer la ficha ni declarar el corte. → P1 lo escribe en su
  paso de invocación (v0.1.6).
- **F9 Flujos ad-hoc multi-paso con brief — APLICA, brecha
  B1 (misma raíz):** la adopción local de la doctrina
  (`docs/EJECUCION-Y-RELEVO.md`) no declara el corte. → P1
  le suma la sección del deber con la tabla por flujo.
- **F1 Propuestas — NO APLICA como corte de brief, con
  puerta equivalente operando:** lo despierta el reloj con
  alcance prefijado por el sistema, y su puerta (aprobación
  del dueño entre Fase A y Fase B) vive dentro del flujo y
  exige aprobados registrados.
- **F3 Pinterest, F4 Dirección semanal — NO APLICA:** crons
  con unidad prefijada por su skill; el reloj no orquesta y
  nadie empaqueta alcance por corrida.
- **F5 Onboarding, F6 Conexión Etsy API — NO APLICA:** vía
  directa guiada con el dueño en vivo (adopción registrada
  desde v0.11.0); no hay worker ni brief que cortar.
- **F7 Operación comercial — NO APLICA:** órdenes directas
  del dueño, caso por caso; la orden es la autorización.
- **F8 Puertas transversales — NO APLICA:** ejecutan dentro
  de las unidades; son las puertas, no quien corta.

## Validación de colocación — registro del protocolo (v0.13.0)

- `rameli validar .` corrido sobre esta app **antes y
  después** del cambio de pin: **0 fallos, 0 avisos en
  ambas corridas** (su hallazgo histórico del chequeo 3
  quedó cerrado en la fase de mejora v0.14.0 y la puerta lo
  re-verificó hoy).
- **Inventario de herramientas de la fase:** `bin/rameli`
  (lint / test / validar / migrate) desde el repo del
  framework; git con worktree aislado. Nada usado como
  puerta o mecanismo vive fuera de los repos.
- **Prueba de frío:** otra IA con solo este repo y el del
  framework reconstruye la migración y la adopción: delta
  en el CHANGELOG de Rameli, proceso en su
  `MIGRACIONES.md`, alcance aquí, veredictos por flujo en
  la auditoría y la implementación propuesta en la fase de
  mejora.
- **Mapa de datos:** sin cambios (la unidad no tocó datos).

## Verificación

- **Lint** (`rameli lint` sobre los 9 skills): VERDE total,
  0 fallos, antes (sobre `main` en `9ba2776`) y después (en
  el worktree con el pin nuevo).
- **Regresión** (`rameli test` sobre los 9 skills): **VERDE
  total en ambas corridas, con conteos idénticos** — base
  (worktree en el commit `9ba2776`, pin 0.14.0) y después
  (worktree de la migración, pin 0.15.0): 5 suites con
  casos — 13 + 4 + 3 + 18 + 15 = **53 casos, 0 fallas** — y
  los mismos 4 avisos de skills sin `evals/` (conectar-etsy-api,
  estratega-pinterest, onboarding-tienda, publicador-lote),
  preexistentes e idénticos en ambas.
- **`rameli validar`**: 0 fallos, 0 avisos, antes y después.
- Consistencia del pin: `rameli.json` = 0.15.0, los 9
  frontmatter en 0.15.0 y las 3 líneas vivas de CHANGELOG en
  0.15.0 (barrido: los `0.14.0` restantes son historia
  fechada o referencias al delta de la migración anterior).

## Fusión y cierre

- Rama `migracion-rameli-v0150` (commit `688debc`),
  fusionada a `main` por fast-forward y empujada:
  `origin/main = 688debc`, verificado con
  `git status -sb` (sin ahead; único rastro en el árbol: el
  `tmp/paso1-investigacion-personalizacion.md` sin trackear
  de otro trabajo, intacto).
- Rama `migracion-rameli-v0150` borrada (local; nunca se
  empujó) y worktrees de la migración y de la base retirados.
- **La fase de mejora (P1: cerrar B1) se ejecuta a
  continuación en su rama `mejora-v0150`**, con la
  autorización de la orden de trabajo de esta sesión; su
  resultado queda en `docs/FASE-MEJORA-V0150-PROPUESTA.md`.
