# Migración a Rameli v0.16.0 — registro de ejecución (2026-10-20)

Encargo del dueño la noche del 2026-10-20 («corre las
actualizaciones al cien por ciento», incluido My POD al
confirmar que está en pausa), ejecutado en el chat propio
«🔀 My POD — Migración Rameli v0.16.0 + datos de instancia»
con brief limpio (`~/workspace/migraciones-v0160/brief-my-pod.md`).
Canon que mandó: `rameli/MIGRACIONES.md` (nota 0.15.0 → 0.16.0)
y `rameli/docs/DATOS-INSTANCIA.md`. El delta es aditivo y sin
cambios rompientes: el **estándar de datos de instancia** y el
**chequeo 5** de `rameli validar`, con el ámbito de instancia
del chequeo 4. Como esta app ya versionaba medios, el brief
mandó además la **cirugía de historial** por la ruta de
reescritura con filtro que la nota de migración documenta —
decisión de la app, ejecutada aquí con respaldo íntegro previo.

## Paso 0 — guardas (antes de tocar nada)

- **Agentes:** `subagent.list` sin agentes activos sobre este
  repo al abrir. El worker hermano de My Channels corre su
  propia migración en paralelo sobre SU repo; no toca `my-pod`.
- **Inventario de automatizaciones** (crons que operan sobre
  `~/workspace/my-pod`, verificado en vivo con `cron.list` /
  `cron.view` / `cron.status`):
  - *Escriben datos de la tienda y/o hacen git (add/commit/push)
    — ninguno cae dentro de la ventana nocturna de la cirugía:*
    `equipo-pod-pinterest-diario` (diario 08:50; próxima corrida
    mié 2026-10-21 08:50 — escribe registro de listings, pins y
    commit+push de cierre; es el primero tras la ventana),
    `equipo-pod-propuestas-diarias` (diario 18:00,
    **desactivado** por orden del dueño; escribiría artes,
    registro y checkpoints y commitea el registro),
    `equipo-pod-investigacion-semanal` (lun 08:50; próxima
    lun 2026-10-26), `equipo-pod-estratega-semanal` (lun 10:50;
    próxima lun 2026-10-26), `pod-ritual-lunes-h04` (lun 07:50;
    próxima lun 2026-10-26), `equipo-pod-revision-viernes`
    (vie 17:50; próxima vie 2026-10-23), `pod-ritual-viernes-h12`
    (vie 17:50; próxima vie 2026-10-23), `pod-trend-scan`
    (lun/jue 09:50; próxima jue 2026-10-22).
  - *Solo lectura sobre el repo — corren durante la ventana
    por diseño y ninguno escribe ni hace git:*
    `equipo-pod-watchdog` (cada 30 min; lee
    `estado-propuestas.json` y `registro-listings.json` y cruza
    contra la API de Printify en solo lectura; su cuerpo le
    prohíbe mover estados) y `vigia-migraciones-v0160-apps`
    (cada 30 min; solo lectura en ambos repos, creado para
    vigilar esta misma cirugía). La reescritura se ejecutó
    entre sus corridas.
  - *Sin operaciones sobre el repo:* `etsy-sale-25-to-20-oct31`
    (runonce 2026-10-31, opera en Etsy),
    `cyber-specials-decision-2026-10-26` (runonce 2026-10-26),
    `pod-evaluacion-piloto-nocturno-2026-10-25` (runonce
    2026-10-25), `printify-upload-watch` (próxima 2026-11-03).
  - **No se tocó el contenido ni el horario de ningún job**
    (solo inventario y, al cierre, verificación de
    consistencia contra el repo reescrito).
- **Inventario del repo (antes):** `main` en `65c2721`
  (= `origin/main`), árbol limpio salvo
  `tmp/paso1-investigacion-personalizacion.md` sin trackear
  (16,686 bytes, de otro trabajo — se preserva tal cual), una
  sola rama, un solo worktree, sin tags. Repo total **3.6 GB**;
  `.git` con **1.82 GiB** en 2,175 objetos sueltos (sin packs);
  `data/` físico: **551 archivos, 1,770,117,400 bytes**.
  Medios trackeados bajo `data/` en HEAD: **355 archivos**
  (256 `.jpg` + 99 `.png`), **1,651,115,025 bytes** —
  `data/artes-print` 99 archivos / ~1,557.5 MB,
  `data/mockups` 250 / ~92.8 MB, `data/auditoria-2026-10-15`
  6 / ~0.8 MB. Medios físicos bajo `data/` (trackeados o no):
  405 archivos, 1,769,740,835 bytes (incluye 50 `.mp4` ya
  ignorados en `data/videos/`).
  Censo de historial hecho por `ls-tree` de los **161 commits**
  (`rev-list --objects` demostró omitir blobs reales — los
  `-9/-10.jpg` — y no sirve de censo): **407 rutas de medios
  distintas bajo `data/`** (las 355 de HEAD + 52 solo
  históricas) **más 1 `.webp` solo histórico**
  (`data/candidatos-p037/…webp`, 326,048 bytes; el `.webp` no
  está en la lista del chequeo 5 — el brief manda purgar «las
  extensiones del chequeo 5 y cualquier otra presente»).
  Fuera de `data/` quedan trackeados, fuera del alcance de
  esta cirugía: 15 `.png` de fixtures del sistema en
  `skills/puerta-arte-propuesta/evals/fixtures/` (canónicos de
  la suite desde la fase de mejora v0.14.0) y 30 `.jpg` en
  `tmp/videos-pendientes/` (ver propuesta P2 de la fase de
  mejora).
- **Línea base (sobre `main` en `65c2721`):** lint **VERDE**
  total; regresión **VERDE, 53 casos** (13+4+3+18+15), 0
  fallas, con los mismos 4 avisos de skills sin `evals/`
  (conectar-etsy-api, estratega-pinterest, onboarding-tienda,
  publicador-lote); `rameli validar` **0 fallos, 1 aviso** —
  el aviso es la adopción pendiente de la política de
  instancia, justo lo que esta migración cierra.
- Rameli: `main` en `cf421e3`, `VERSION` = **0.16.0**, tag
  anotado `v0.16.0` y Release de GitHub publicados y
  verificados la misma noche.

## Respaldo íntegro (antes de cualquier reescritura)

En `~/workspace/respaldos/my-pod-pre-v0160-2026-10-20/`:

- `my-pod-pre-v0160.bundle` — `git bundle --all`,
  1,855,053,061 bytes, sha256
  `6b94caf4a58baecc97a60f18c1f5c04949935cd92463388a45ea671d45eec1d1`
  (en `bundle.sha256`). `git bundle verify`: «The bundle
  records a complete history», cabezas `main` / `origin/main`
  / `HEAD` = `65c2721`.
- `data/` — copia completa del árbol de datos (551 archivos),
  verificada contra el manifiesto con `sha256sum -c`:
  **551/551 OK** (salida en `verificacion-copia-data.txt`;
  manifiesto en `manifiesto-data-pre.txt`).
- `tmp-sin-trackear/paso1-investigacion-personalizacion.md` —
  copia del archivo sin trackear, sha256
  `6dc145e908260d1d6606230639d8d87810a59d1a499b107081e1597916b5e480`,
  idéntico al original.
- Post-cirugía se sumaron a la misma carpeta el mapa de
  hashes de `git-filter-repo` (`.git/filter-repo/commit-map`
  y `ref-map`, copia como `mapa-hashes-cirugia/`) y el paquete
  de evidencia de la corrida.

## Cirugía de historial (reescritura con filtro)

- Herramienta: `git-filter-repo`, instalada para esta unidad
  en el venv `~/workspace/.venvs/filter-repo`
  (`pip install git-filter-repo`; versión `a40bce548d2c`) —
  **colocación documentada aquí**, como manda el brief para
  herramientas que no viven en un repo del sistema; el venv
  persiste bajo `~/workspace/.venvs/` junto a los demás
  entornos de herramientas de la casa.
- Comando (en `~/workspace/my-pod`, historial completo):
  `git-filter-repo --force --invert-paths` con
  `--path-glob 'data/*.<ext>'` para las 11 extensiones
  (mp4, mov, mkv, webm, mp3, wav, flac, png, jpg, jpeg del
  chequeo 5 + webp presente en el historial). Los globs de
  filter-repo usan `fnmatch` (el `*` cruza `/`): cada patrón
  cubre cualquier profundidad bajo `data/`.
- Resultado: 161 commits reescritos en 7.38 s; `main` pasó de
  `65c2721` a `4a3e2d0` (todos los hashes cambian — costo
  documentado de esta ruta en la nota de migración). La
  herramienta retiró el remoto `origin` (su salvaguarda
  estándar); se re-agregó a mano
  (`git@github.com:ChrisBP-Dev/my-pod.git`, con el
  `core.sshCommand` del repo intacto).
- **Verificación post-cirugía:** censo por `ls-tree` de los
  161 commits = **0 rutas de medios bajo `data/`**;
  `git count-objects`: 1 pack, 1,672 objetos, **65.21 MiB**
  (desde 1.82 GiB sueltos); repo total **~247 MB** con el
  árbol de trabajo ya reducido.
- **La media física no se borró del disco como pérdida:**
  el reset de la herramienta dejó en el árbol los 196
  archivos no-medios de `data/` (551 − 355) y los 50 `.mp4`
  ignorados intactos; el archivo sin trackear de `tmp/`
  sobrevivió intacto (mismo hash al cierre, ver abajo).

## Restauración de la media física

- `rsync -rt --ignore-existing` desde la copia del respaldo
  a `data/`: **551 archivos** de vuelta en su hogar canónico.
- Verificación contra el manifiesto pre-cirugía
  (`sha256sum -c`): **551/551 OK**; `data/` =
  **1,770,117,400 bytes, idénticos a antes de la cirugía**.
  Las rutas que los skills y scripts de la tienda leen
  resuelven igual (la regresión post-migración corre contra
  esos archivos físicos — entre ella la suite de
  `publicar-printify-etsy`, que verifica diseños y videos
  reales de `data/`).
- Barrido de consumidores: ningún script, skill ni doc vivo
  de la app usa `git ls-files` para localizar medios — la
  verificación es por **existencia física**, como manda el
  estándar; des-trackear no rompe ningún flujo.

## Alcance aplicado (rama `migracion-rameli-v0160`)

- `rameli.json`: pin 0.15.0 → **0.16.0** + nota de migración
  fechada; en `datos`: **`politica_instancia:
  { "medios_en_git": false }`** declarada y la zona
  `data/auditoria-2026-10-15` reclasificada de `historial` a
  **`historial_instancia`** (es el historial de auditoría de
  ESTA tienda, no del sistema: en un clon fresco su ausencia
  es aviso de ámbito de instancia, no declaración podrida;
  su ubicación física no cambia y ningún código la lee desde
  el mapa — solo `ARQUITECTURA-DATOS.md` la menciona, por su
  ruta).
- Los **9 skills**: `framework_version: "0.16.0"` en su
  frontmatter. Tres CHANGELOG de skill cuya línea viva
  declara el pin actualizados a v0.16.0 (estratega-pinterest,
  puerta-arte-propuesta, puerta-pinterest-pin). Las
  referencias a «Rameli v0.15.0» que quedan en
  `publicador-lote` son atribución histórica del mecanismo
  del corte, no pin — no se tocan.
- `.gitignore`: gana el bloque de medios bajo `data/`
  **verbatim** del que genera `rameli init` en v0.16.0 (las
  10 extensiones del estándar con su comentario canónico).
  Verificado con `git check-ignore -v` sobre artes, mockups
  y videos. La media restaurada queda ignorada: `git status`
  limpio sin des-trackeos pendientes.
- `README.md`: pin y sección de esta migración.
- Este registro, la auditoría de adopción
  (`docs/AUDITORIA-ADOPCION-V0160.md`) y la propuesta de la
  fase de mejora (`docs/FASE-MEJORA-V0160-PROPUESTA.md`).
- **Ningún dato de producción se modificó de contenido:**
  el único cambio sobre `data/` es de tracking e historial,
  con la media física verificada byte a byte. Nada se tocó
  fuera del repo (ni Printify, ni Etsy, ni Pinterest, ni
  ningún cron), y el archivo sin trackear de `tmp/` quedó
  como estaba (hash `6dc145e9…` antes y después).

## Registro de adopción — delta v0.16.0

- **Política de instancia declarada:** sí,
  `datos.politica_instancia.medios_en_git: false`.
- **Medios fuera del repo del sistema:** sí — purga de
  historial verificada por censo (0 rutas en 161 commits) y
  `.gitignore` que sostiene la política desde hoy.
- **Zonas de historial de instancia declaradas:**
  `data/auditoria-2026-10-15` en `historial_instancia`.
- **Chequeo 5:** en verde (`rameli validar` 0 fallos,
  0 avisos tras la adopción; antes: 0 fallos, 1 aviso).
- La auditoría completa (matriz de capacidades × flujos con
  la fila nueva C25 de datos de instancia) vive en
  `docs/AUDITORIA-ADOPCION-V0160.md`; no es diferible en este
  delta y se corrió.

## Validación de colocación — registro del protocolo (v0.13.0)

- `rameli validar .` corrido antes (0 fallos, 1 aviso — la
  adopción pendiente) y después (ver «Verificación»): la
  puerta re-verifica el cierre.
- **Inventario de herramientas de la fase:** `bin/rameli`
  (lint / test / validar / migrate) desde el repo del
  framework; git del sistema; `git-filter-repo` en el venv
  documentado arriba (`~/workspace/.venvs/filter-repo`),
  creado para esta unidad porque la herramienta no estaba
  instalada — es el único artefacto de la fase que vive
  fuera de un repo, y queda declarado en este registro con
  su ruta y versión. El paquete de evidencia (manifiestos
  sha256 de `data/` antes/después, salidas de las puertas,
  log de la cirugía) vive con el respaldo en
  `~/workspace/respaldos/my-pod-pre-v0160-2026-10-20/` —
  es evidencia de la instancia, no del sistema.
- **Prueba de frío:** clon limpio del repo reescrito en
  `/tmp` + `rameli validar` sin FALLO (detalle en
  «Verificación»): otra IA con solo este repo y el del
  framework reconstruye la migración, la adopción y la
  cirugía (delta en el CHANGELOG de Rameli, proceso en su
  `MIGRACIONES.md`, estándar en `DATOS-INSTANCIA.md`,
  alcance y evidencia aquí).
- **Barrido de colocación:** todo script o medición usado
  como puerta en esta unidad vive donde el sistema dice:
  las puertas son las del framework (`bin/rameli`); la
  herramienta de cirugía queda en su venv persistente y
  declarada arriba; ningún artefacto de calibración quedó
  solo en `/tmp` (los manifiestos y salidas se archivaron
  con el respaldo el mismo día). Los scripts de la app
  nombrados por skills se re-verificaron presentes vía
  `rameli validar` (chequeos 1–3 sin hallazgos).

## Verificación

- **Lint** (`rameli lint` sobre los 9 skills): VERDE total
  antes y después.
- **Regresión** (`rameli test` sobre los 9 skills): VERDE
  total en ambas corridas con conteos idénticos — **53
  casos, 0 fallas** (13+4+3+18+15) y los mismos 4 avisos de
  skills sin `evals/`, preexistentes. La corrida posterior es
  además la prueba de que los flujos leen la media física
  restaurada (las suites verifican diseños y videos reales).
- **`rameli validar`**: antes 0 fallos / 1 aviso; después
  **0 fallos, 0 avisos** — chequeo 5 en verde (cero medios
  trackeados bajo `data/` con la política declarada).
- **Tamaños antes/después:** `.git` 1.82 GiB de objetos
  sueltos → pack de **65.21 MiB**; clon limpio del repo
  (lo que viaja y se comparte): **111 MB** en total; el
  árbol en disco de esta instancia pasa de 3.6 GB a 1.8 GB
  — el resto es la media física local (1.77 GB), que por
  diseño ya no vive en git. `data/` físico idéntico:
  551 archivos / 1,770,117,400 bytes antes y después
  (sha256 551/551).
- **Prueba de frío:** `git clone` limpio del remoto en
  `/tmp/clon-frio-v0160` (**111 MB**, 300 archivos
  trackeados, 143 bajo `data/` — todos de texto — y **0
  medios**) y `rameli validar` sobre el clon: **0 fallos**
  (chequeo 5 en verde: el clon no contiene ni trackea medio
  alguno bajo `data/`), con exactamente 2 avisos, ambos el
  comportamiento de ámbito de instancia que el estándar
  v0.16.0 define para un clon fresco o de otro dueño:
  `data/mockups` declarado en el mapa pero ausente (zona de
  medios puros: 250 archivos físicos solo existen en esta
  instancia) y `data/auditoria-2026-10-15` declarado en
  `historial_instancia` pero ausente (aviso de instancia,
  no declaración podrida).
- **Consistencia de jobs post-cirugía:** los jobs del Paso 0
  operan sobre este mismo árbol de trabajo (no hay otras
  copias vivas del repo: un solo worktree), ya reescrito y
  empujado; `git fetch` + `git status -sb` sin divergencia
  al cierre deja a cada job que hace git operando sobre la
  historia nueva. Cualquier clon externo futuro debe hacerse
  de nuevo (costo documentado de la reescritura); no existe
  ninguno registrado en el sistema.

## Fusión y cierre

- Rama `migracion-rameli-v0160` (commit `8e3a06a` sobre la
  historia reescrita), fusionada a `main` por fast-forward.
- **Force-push de la historia reescrita** con lease
  explícito contra el hash esperado
  (`--force-with-lease=main:65c2721…`): el remoto seguía en
  `65c2721` — sin actividad ajena durante la operación — y
  quedó en `8e3a06a`
  (`+ 65c2721...8e3a06a main -> main (forced update)`).
  Era la única rama reescrita (la app vive en una sola rama
  y un solo worktree); la rama de migración nunca se empujó
  y se borró local al fusionar.
- Verificación post-push: `git status -sb` =
  `## main...origin/main` **sin ahead ni behind** (único
  rastro en el árbol: el `tmp/paso1-investigacion-
  personalizacion.md` sin trackear de otro trabajo,
  intacto, con su hash `6dc145e9…` verificado antes y
  después); `git ls-remote origin main` = `8e3a06a` =
  `main` local. Guardia durante el proceso: un `git fetch`
  intermedio se detuvo a tiempo al detectarse que
  descargaba la historia vieja completa (el repo local ya
  no la contiene); su pack temporal parcial se eliminó y
  `.git` quedó en sus 65.21 MiB.
- **Consistencia de jobs:** los jobs del Paso 0 que hacen
  git operan sobre este mismo árbol, ya sobre la historia
  nueva y sincronizado con el remoto — su próximo
  `add/commit/push` (Pinterest, mié 2026-10-21 08:50) parte
  de `main = origin/main` verificado. Ningún job requirió
  cambios de contenido ni de horario.
- **La fase de mejora queda abierta con su propuesta**
  (`docs/FASE-MEJORA-V0160-PROPUESTA.md`: P1 registros de la
  instancia, P2 `tmp/videos-pendientes/`, P3 respaldo
  externo de medios, P4 micro-decisión `.webp`), **sin
  ejecutar** — espera el dale del dueño, como manda el
  framework cuando la orden no lo incluye.
