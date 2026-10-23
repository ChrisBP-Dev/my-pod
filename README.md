# my-pod — aplicación POD (cuarto limpio)

App construida con Rameli **v0.19.0** (pineado en `rameli.json`).
Valida el framework en el camino más corto antes de construir My Channels.

## Migración a Rameli v0.19.0 — actualización completa (2026-10-23)

Adoptada como **actualización completa** por mandato del dueño
(2026-10-23), siguiendo `rameli/MIGRACIONES.md`: pin en
`rameli.json`, en el frontmatter de los **9 skills** y en las
declaraciones vivas de sus CHANGELOG. El delta 0.18.0 → 0.19.0
trae **solo** la doctrina de **versionado de aplicaciones**
(`rameli/docs/VERSIONADO-APLICACIONES.md`, PR #10): sin cambios
rompientes, sin mecanismo nuevo y sin cambios de comportamiento.
La adopción se verificó contra el canon en
`docs/AUDITORIA-ADOPCION-V0190.md` — veredicto: **conforme, sin
brechas** — sobre la v1.0.0 que esta app ya había abierto el
mismo día (semver propio, `CHANGELOG.md`, tag anotado y Release
verificado como Latest; el repo de registros no se versiona).
Esta migración se libera como **My POD v1.1.0** (migración sin
rompientes = MENOR según el canon). Registro completo:
`docs/MIGRACION-RAMELI-V0190.md`.

## Migración a Rameli v0.18.0 — cierre de alineación completo (2026-10-21)

Adoptada como **actualización completa** por mandato del dueño
(2026-10-21 08:50 EDT), siguiendo `rameli/MIGRACIONES.md` (nota
0.17.0 → 0.18.0 y la doctrina de actualización completa): pin en
`rameli.json`, en el frontmatter de los **9 skills** y en las
declaraciones vivas de sus CHANGELOG. El delta es aditivo y sin
cambios rompientes: la **declaración del repo de registros**
(`datos.repo_datos`, `rameli/docs/DATOS-INSTANCIA.md` §4), el
**ámbito de instancia por separación** en el chequeo 4 de
`rameli validar` y la doctrina de actualización completa.
Adopción: la separación D1 ejecutada en v0.17.0 gana su
declaración canónica — `datos.repo_datos` apunta al repo
privado **`my-pod-datos`** — y la validación se probó en los
dos estados: instancia restaurada **0 fallos, 0 avisos** y clon
de solo sistema **sin FALLO de hogar** (AVISO «registros sin
restaurar en esta copia»). En la misma operación se ejecutó la
**fase de mejora v0.17.0 completa**: P1 vía el framework
(Rameli v0.18.0, PR #9) y P2 en esta app (rutas del ritual de
los lunes corregidas al layout vigente, con evidencia de
función propia frente a la investigación semanal), más el
barrido de referencias muertas en crons vivos, skills, scripts
y docs operativos. Registro completo:
`docs/MIGRACION-RAMELI-V0180.md`; auditoría de adopción del
delta: `docs/AUDITORIA-ADOPCION-V0180.md`.

## Migración a Rameli v0.17.0 + separación de registros D1 (2026-10-21)

Adoptada por encargo del dueño (paquete completo confirmado por
él: D1 + D2), siguiendo `rameli/MIGRACIONES.md`: pin en
`rameli.json`, en el frontmatter de los **9 skills** y en las
declaraciones vivas de sus CHANGELOG. El delta 0.16.x → 0.17.0
es aditivo y sin cambios rompientes: el **ciclo de vida del
staging** (`rameli/docs/DATOS-INSTANCIA.md` §8) y el aviso de
`zonas_staging` en el chequeo 5 — adopción ya ejecutada de
hecho por esta app (`datos.zonas_staging: []` declarado, regla
en `FLUJO-PIPELINE.md` §5.1 y la purga de `tmp/videos-pendientes/`
como ejecución de P2), aquí registrada y verificada. En la
misma unidad se ejecutó la **separación de registros (D1)**,
la P1 de la fase de mejora v0.16.0: los registros de la
instancia (todo el texto bajo `data/`) se versionan desde hoy
en el repo privado **`my-pod-datos`** — creado en GitHub, con
la historia de los registros separada por rutas (88 commits) —
y este repo del sistema queda **sin registros en el árbol ni
en el historial**, conservando el esqueleto de datos
(`.gitkeep`). Los archivos físicos no se movieron; el ciclo
«escribir = commitear» commitea en el repo que toca vía
`scripts/registros-datos.py`. **D2** quedó resuelta por
decisión del dueño: el respaldo de los registros ES el repo
de datos en GitHub; los medios quedan sin respaldo externo
por decisión explícita. Registro completo:
`docs/MIGRACION-RAMELI-V0170.md`.

## Migración a Rameli v0.16.0 (2026-10-20)

Adoptada por encargo del dueño (My POD en pausa, confirmado por
él), siguiendo `rameli/MIGRACIONES.md`: pin en `rameli.json`, en
el frontmatter de los **9 skills** y en las declaraciones vivas
de sus CHANGELOG. El delta 0.15.0 → 0.16.0 es aditivo y sin
cambios rompientes: el **estándar de datos de instancia**
(`rameli/docs/DATOS-INSTANCIA.md`) y el **chequeo 5** de
`rameli validar`, con el ámbito de instancia del chequeo 4.
Adopción ejecutada: política
`datos.politica_instancia.medios_en_git: false` declarada,
`.gitignore` con el bloque de medios bajo `data/` (el que genera
`rameli init`) y la zona `data/auditoria-2026-10-15` reclasificada
de `historial` a `historial_instancia`. Como la app ya versionaba
medios, la migración incluyó la **cirugía de historial** (ruta de
reescritura con filtro de la nota de migración): respaldo íntegro
verificado antes (bundle `--all` + copia del árbol de datos),
purga de los blobs de medios bajo `data/` de los 161 commits
(407 rutas: 355 en HEAD + 52 solo históricas, más 1 `.webp`
histórico) y restauración de la media física a su hogar,
verificada byte a byte (manifiesto sha256: 551/551 archivos,
1,770,117,400 bytes, idénticos antes y después). `.git` pasó de
1.82 GiB de objetos sueltos a un pack de 65.21 MiB y un clon
limpio del repo pesa 111 MB (el árbol en disco de la instancia,
con su media física local, 1.8 GB). Ningún listing se tocó; el
archivo sin trackear de `tmp/` quedó intacto. Registro completo:
`docs/MIGRACION-RAMELI-V0160.md`.

## Migración a Rameli v0.15.0 (2026-10-20)

Adoptada por encargo del dueño, siguiendo `rameli/MIGRACIONES.md`:
pin en `rameli.json`, en el frontmatter de los **9 skills** y en
las declaraciones vivas de sus CHANGELOG. El delta 0.14.0 →
0.15.0 es un solo mecanismo, aditivo y sin cambios rompientes:
el deber del orquestador de leer la ficha y cortar la unidad en
las puertas que la ficha declara (contribución PR #8 de Rameli).
Antes de migrar se verificó el trabajo en vuelo: el lote de
publicación Thanksgiving gestionado desde otro chat quedó
**cerrado y commiteado** (11/11, `9ba2776`) minutos antes de
abrir la migración — nada en curso que pisar; el archivo sin
trackear de `tmp/` (investigación de otro trabajo) no se tocó.
La auditoría de adopción (no diferible) auditó flujo por flujo
dónde aplica el deber: aplica en la publicación por lote y en
los briefs ad-hoc (brecha B1: el corte no estaba escrito donde
la app corta), con puerta equivalente dentro del flujo de
propuestas y no-aplica motivado en el resto; su implementación
es la fase de mejora de esta migración, ejecutada con el dale
del dueño dado en la orden de la sesión. Ningún dato se tocó.
Registro completo: `docs/MIGRACION-RAMELI-V0150.md`.

## Migración a Rameli v0.14.0 (2026-10-19)

Adoptada por encargo del dueño, siguiendo `rameli/MIGRACIONES.md`:
pin en `rameli.json`, en el frontmatter de los **9 skills** y en
las declaraciones vivas de sus CHANGELOG. El delta 0.12.1 →
0.14.0 es aditivo y sin cambios rompientes: v0.13.0 suma la
validación de colocación (el comando `rameli validar` y su
protocolo de cierre con registro); v0.14.0 suma el estándar de
datos multi-unidad y el chequeo 4 de `rameli validar`, que lo
verifica contra el mapa que cada aplicación declara en su
`rameli.json` (clave `datos`). El mapa de esta app ya estaba
declarado (commit `1e73e16`): esta migración lo registra como
adopción, no lo re-decide. La primera corrida de `rameli validar`
queda registrada y clasificada en el registro de la migración;
su hallazgo vigente del chequeo 3 (la suite de arte lee diseños
canónicos desde fuera del repo) es insumo de la fase de mejora
que esta migración abre — no se mueve ningún archivo de diseño
en esta migración —, cuya auditoría de adopción NO es diferible
(el delta trae capacidades nuevas). Ningún dato se tocó.
Registro completo: `docs/MIGRACION-RAMELI-V0140.md`.

## Migración a Rameli v0.12.1 (2026-10-19)

Adoptada por encargo del dueño, siguiendo `rameli/MIGRACIONES.md`:
pin en `rameli.json`, en el frontmatter de los **9 skills** y en
las declaraciones vivas de sus CHANGELOG. El delta 0.11.1 →
0.12.1 es aditivo y sin cambios rompientes: v0.12.0 suma la ruta
de lectura por tarea (canon del constructor), la auditoría de
adopción como pieza obligada de la fase de mejora y la
delimitación de orquestación (la Pieza 4 como capacidades
disponibles dentro de la doctrina única de workers, no como
camino rival — esta app ya lo declara así en
`docs/DELIMITACIONES-ADOPCION.md` §2); v0.12.1 es un parche del
cierre de versiones del framework (exige Release de GitHub
publicado), sin efecto en el comportamiento de la app. La ruta
de lectura se adopta en la fase de mejora que esta migración
abre, cuya auditoría de adopción NO es diferible (el delta trae
capacidades nuevas). Ningún dato se tocó. Registro completo:
`docs/MIGRACION-RAMELI-V0121.md`.

## Migración a Rameli v0.11.1 (2026-10-19)

Parche del framework (encabezado de la doctrina de workers
declarado vigente, `bin/rameli` ejecutable, paso de estado en el
checklist de contribuciones): cero cambios de comportamiento.
Adoptada como Propuesta 3 de la auditoría de adopción
(`docs/AUDITORIA-ADOPCION-V0110.md`, con el dale del dueño a
ejecutar todas sus propuestas): pin en `rameli.json` y en el
frontmatter de los **9 skills actuales** (la puerta legacy
`puerta-publicacion-pod` se eliminó en la fase de mejora
post-v0.11.0; en la migración anterior la app tenía 10 skills).

## Migración a Rameli v0.11.0 (2026-10-19)

Adoptada por dale del dueño, siguiendo `rameli/MIGRACIONES.md`:
pin en `rameli.json` y en el frontmatter de los skills. El delta
0.9.0 → 0.11.0 es aditivo y sin cambios rompientes: v0.10.0 suma el
modelo de ejecución por workers (adoptado **por flujo**, con el
registro en `docs/MIGRACION-RAMELI-V0110.md`) y v0.11.0 suma la
fase de mejora post-migración. Ningún dato se tocó.

## Migración a Rameli v0.9.0 (2026-10-18)

Adoptada por dale del dueño, siguiendo `rameli/MIGRACIONES.md`:
pin en `rameli.json` y en el frontmatter de los skills, secciones
"Calibraciones (mecanismo vs aplicación)" renombradas, terminología
canónica (framework / aplicación / ficha) en los documentos vivos.
El gemelo máquina de la ficha de la tienda (`config.json`) no cambió
de nombre ni de formato: ningún dato se tocó. Los documentos
históricos conservan la terminología de su época.

## Skills

| Skill | Versión | Qué puerta |
|---|---|---|
| `conectar-etsy-api` | v0.1.1 | Conexión API Etsy por tienda: Seller App → OAuth PKCE → tokens → registro |
| `estratega-tienda` | v0.6.1 | Dirección semanal de tienda: reparto de foco, mix, guía de precios, NO-hacer |
| `estratega-pinterest` | v0.1.4 | Parrilla de Pinterest: 5 pins/día, mix por listing |
| `onboarding-tienda` | v0.1.5 | Playbook de puesta en marcha: de cero a tienda operativa |
| `paquete-listing-etsy` | v0.2.0 | Paquete comercial del listing: título, descripción, tags, keywords |
| `publicar-printify-etsy` | v0.9.0 | Producción en Printify (MPL: base → conversión → items creados dentro) → publicación en Etsy |
| `publicador-lote` | v0.1.3 | Lote aprobado → side chat: manifiesto explícito, checkpoints por listing, reporte |
| `puerta-arte-propuesta` | v0.8.7 | Arte listo: PNG 300 DPI, fondo transparente, sin blanco puro; entrega en la vitrina |
| `puerta-pinterest-pin` | v0.4.1 | Pin listo: asset FINAL del listing, keywords con fuente, URL rastreable |

## Principios operativos (para quien opere esta app)

Esta app es portable: quien la clone recibe skills + docs + scripts.
Estos principios rigen cómo se opera, sin depender del manual del
operador original:

- **Patrones de resiliencia** (`docs/PATRONES-RESILIENCIA.md`): todo
  trabajo largo con dependencia externa lleva health-check antes de
  trabajar, checkpoints con resume, y reintentos acotados (tope 3/día).
- **Ejecución por workers** (Rameli v0.10.0, adoptado por flujo —
  registro completo en `docs/MIGRACION-RAMELI-V0110.md` y
  calibraciones en `docs/EJECUCION-Y-RELEVO.md`): el
  publicador de lote ya opera con un worker por lote y los crons
  diarios operan como workers con checkpoint local
  (`data/tiendas/<tienda-id>/estado-*.json`); las puertas y las tareas de 1–2 pasos van
  por vía directa. Cada tienda lleva su registro de flujo en
  `data/tiendas/<id>/registro-flujo.md`.
- **Puesta en marcha** (`skills/onboarding-tienda`): playbook de cero
  a tienda operativa; es el que aplica los patrones al crear crons.
- **Capas**: sistema portable y versionado (skills/docs/scripts) vs
  tienda (config en `data/tiendas/<id>/`). Nada de la tienda quemado
  en código.
- **API-first**: lo que cubre la API de Etsy va por API; navegador
  solo para lo no expuesto (`docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md`).

## Docs operativos

- `docs/PATRONES-RESILIENCIA.md` — patrones portables para workers con dependencias externas (health-check, checkpoints, reintentos acotados).
- `docs/CONTRATO-TIPO-PRODUCTO.md` — contrato de tipo de lote (mpl/single/mixto).
- `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` — API-first; navegador solo para lo no expuesto.
- `docs/REGLA-DELIVERY-CHATS.md` — reportes automáticos en chat nuevo, nunca en archivados.

## Datos

Los archivos viven físicamente bajo `data/`, como siempre;
desde la separación D1 (2026-10-21) su **versionado** vive en
el repo privado `my-pod-datos` (este repo conserva solo el
esqueleto). Ver el mapa en `ARQUITECTURA-DATOS.md`.

- `data/tiendas/29222324/registro-listings.json` — registro de diseños y listings con sus assets finales aprobados (45 claves, 21 publicados completos al 2026-10-19).
- `data/banco-keywords/` — bancos de keywords por nicho.
- `data/cola-pins/` — pins que pasaron la puerta, en espera de publicación.

## Criterios canónicos

- `FLUJO-PIPELINE.md` — el flujo end-to-end Printify-first + MPL vigente.
- El criterio de los videos de listing (formato técnico 1080×1080, 9.5 s, zoom sin temblor, yuv420p rango limitado + escenarios A–D desde el manifiesto de mockups) vive en `skills/publicar-printify-etsy/SKILL.md` §M6 — única fuente desde v0.11.0; el antiguo `CRITERIO-VIDEO.md` de la raíz se retiró por duplicarla y contradecirla.
- `ARQUITECTURA-DATOS.md` — qué dato vive dónde (global vs por tienda) y el ciclo de vida de los activos.
- `docs/PATRONES-RESILIENCIA.md` — health-check, checkpoints con resume y reintentos acotados.
- `docs/CONTRATO-TIPO-PRODUCTO.md` — contrato estratega → propuestas → publicación (tipo de lote).
- `docs/DELIMITACIONES-ADOPCION.md` — estatus declarado de lo no adoptado (capa de juicio, orquestación del runtime) y dueño del flujo comercial F7.
