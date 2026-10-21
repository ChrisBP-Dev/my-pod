# Migración a Rameli v0.17.0 + separación de registros D1 (2026-10-21)

> Actualización oficial de la app a **Rameli v0.17.0** con
> la **separación de registros (D1)** ejecutada en la misma
> unidad, por encargo del dueño (paquete completo confirmado
> el 2026-10-21 01:09 EDT: D1 registros en repo privado
> propio de datos; D2 ese repo ES el respaldo en GitHub, sin
> servicios pagos ni cuentas nuevas). Brief de la unidad:
> `~/workspace/migraciones-v0170/brief-my-pod-v0170.md`.
> Proceso: `rameli/MIGRACIONES.md` (nota 0.16.x → 0.17.0) y
> canon `rameli/docs/DATOS-INSTANCIA.md` (§6 registros y §8
> staging). Auditoría de adopción (no diferible):
> `docs/AUDITORIA-ADOPCION-V0170.md`.

## Paso 0 — guardas e inventario

- **Sin agentes activos** sobre el repo al abrir
  (`subagent.list`: activos = ninguno). La tienda está en
  pausa operativa acordada para esta ventana nocturna.
- **Respaldo íntegro previo verificado** en
  `~/workspace/respaldos/my-pod-pre-v0170-2026-10-21/`:
  bundle `--all` de la historia completa en `85c75fa`
  (verificado con `git bundle verify`, sha256
  `6cab318c…`), manifiesto sha256 de `data/` e inventario
  de registros trackeados. La media física al abrir:
  **551 archivos, 1,770,117,400 bytes** — idéntica a la
  registrada en la migración a v0.16.0.
- **Línea base (sobre `main` en `85c75fa`):** lint **VERDE**
  total; regresión **VERDE, 53 casos** (13+4+3+18+15), 0
  fallas, 4 avisos preexistentes de skills sin `evals/`;
  `rameli validar` **0 fallos, 0 avisos**. Pin vigente:
  **0.16.0**. Pack del repo: **29.81 MiB**; 164 commits.
- **Inventario de registros (pre-corte):** 143 archivos
  trackeados bajo `data/` — **139 de contenido** (104 json
  + 35 md) **y 4 `.gitkeep`** — y **0 medios** trackeados;
  censo del historial completo: **0 rutas de medios bajo
  `data/`** en los 164 commits (la historia ya venía limpia
  de las cirugías de v0.16.x). El archivo sin trackear de
  otro trabajo (`tmp/paso1-investigacion-personalizacion.md`,
  sha256 `6dc145e9…`) se preserva intacto, verificado antes
  y después.
- **Inventario de crons que escriben registros en este
  repo** (con su próxima corrida al abrir, mié 2026-10-21
  ~01:10 EDT — **ninguno cae en la ventana del corte**):
  - `equipo-pod-pinterest-diario` — diario 08:50 (hoy mié
    08:50: la primera corrida tras el corte). Commitea
    `registro-listings.json`, `data/pins-publicados/` y
    `data/cola-pins/`.
  - `pod-trend-scan` — lun/jue 09:50 (próxima: jue
    2026-10-22). Commitea `investigaciones/<fecha>-tendencias.md`.
  - `equipo-pod-revision-viernes` y `pod-ritual-viernes-h12`
    — vie 17:50 (2026-10-23). Commitean actas en
    `revisiones/`.
  - `equipo-pod-investigacion-semanal` (lun 08:50) y
    `equipo-pod-estratega-semanal` (lun 10:50) — próxima:
    lun 2026-10-26. Commitean investigaciones y
    directriz/config, respectivamente.
  - `equipo-pod-propuestas-diarias` — diario 18:00,
    **deshabilitado** (piloto en pausa). Su cuerpo commitea
    el registro por diseño; se re-apunta igual que los
    demás para que nazca correcto al reactivarse.
  - `etsy-sale-25-to-20-oct31` — runonce 2026-10-31: escribe
    `config.json` (calendario de descuentos) **sin paso de
    commit en su cuerpo** — inconsistencia previa con la
    regla de la app; esta unidad le suma el paso de commit
    de registros (ver «Ciclo de escritura»).
  - **Solo lectura (corren en la ventana, no escriben el
    repo):** `equipo-pod-watchdog` (30 min; lee checkpoints
    y registro, no mueve estados) y
    `vigia-actualizaciones-v0170-apps` (15 min; el vigía de
    esta misma actualización, de solo lectura por diseño).
  - `pod-ritual-lunes-h04` (lun 07:50): **sin mecánica git
    sobre `my-pod`** en su cuerpo; referencia rutas
    `docs/investigacion/…` inexistentes en este repo —
    registrado como observación P2 de la fase de mejora.
  - `printify-upload-watch` (cada 336 h): no toca el repo.

## La migración a v0.17.0 (delta y adopción)

- **Delta 0.16.x → 0.17.0** (del `CHANGELOG.md` de Rameli y
  su nota de migración): aditivo, sin cambios rompientes —
  el **ciclo de vida del staging** en
  `docs/DATOS-INSTANCIA.md` §8 (declarar la zona, no
  trackearla, cierre = purga, supervivencia solo con
  consumidor vivo declarado) y el **aviso de
  `zonas_staging`** en el chequeo 5. Incluye el parche
  v0.16.1 (lista de medios del chequeo 5 extendida a
  webp/avif/heic/heif/gif/bmp/tif/tiff; sin re-migración
  por sí solo — esta migración ordinaria lo trae).
- **Adopción:** pin **0.17.0** en `rameli.json` (con la nota
  de la migración y de D1), en el frontmatter de los **9
  skills** y en las **3 líneas vivas** «Pineado a Rameli»
  de los CHANGELOG (estratega-pinterest,
  puerta-arte-propuesta, puerta-pinterest-pin). La adopción
  del ciclo de vida del staging ya estaba **ejecutada de
  hecho** por esta app — es su caso origen —:
  `datos.zonas_staging: []` declarado, la regla escrita en
  `FLUJO-PIPELINE.md` §5.1 y la purga de
  `tmp/videos-pendientes/` ejecutada el 2026-10-21 como P2
  de la fase anterior. Esta migración la **registra y
  verifica**: `rameli validar` 0 fallos, 0 avisos, sin
  aviso de staging. Auditoría completa:
  `docs/AUDITORIA-ADOPCION-V0170.md` (capacidad nueva C26).

## La separación de registros (D1)

### El mapa final — qué vive en cada repo

| | **Sistema** — `my-pod` | **Datos** — `my-pod-datos` (privado) |
|---|---|---|
| Contiene | skills, docs, scripts + **esqueleto** de datos (`.gitkeep` de los hogares declarados) | **registros de la instancia**: todo el texto bajo `data/` (ficha/config/registro/ledger/directriz de la tienda `29222324`, sus investigaciones y revisiones; banco de keywords, índices de productos, paquetes, registros de pins, manifiestos de video, manifiestos de generación de arte) |
| Historia | reescrita **sin registros** (ni árbol ni historial) | la historia real de los registros, separada por rutas |
| Respaldo | remoto GitHub (el que se comparte/forkea) | remoto GitHub privado — **es** el respaldo de los registros (D2) |
| Nunca contiene | registros ni medios | sistema ni medios |

Fuera de ambos repos, como manda el estándar: los **medios**
(551 archivos físicos bajo `data/`, locales en su hogar —
no se movieron ni se borraron) y los **checkpoints**
`estado-*.json` (locales, jamás versionados).

### Ejecución

1. **Repo de datos creado en GitHub por el navegador**
   (cuenta ChrisBP-Dev, privado, vacío — el conector no crea
   repos, 403; es la vía operativa conocida del dueño):
   `github.com/ChrisBP-Dev/my-pod-datos`.
2. **Split por rutas:** clon local del repo del sistema y
   `git-filter-repo --path data/` (venv persistente
   `~/workspace/.venvs/filter-repo`, el mismo de las
   cirugías de v0.16.x): de los 164 commits quedan **88 que
   tocan registros**, con su historia, autores y mensajes;
   el árbol de registros resultante es **idéntico blob a
   blob** al del sistema pre-corte (**143/143**). Sobre esa
   punta, un commit propio del repo de datos suma su
   `README.md` (qué es y qué nunca contiene) y su
   `.gitignore` (medios — las 18 extensiones —, checkpoints,
   CSV crudos y cola transitoria: lo que no se versiona ni
   siquiera ahí). Push por SSH verificado sin ahead.
3. **Esqueleto en el sistema:** `.gitkeep` en cada hogar
   declarado del mapa `datos` (las 10 zonas globales) y en
   `investigaciones/` y `revisiones/` de la tienda
   (estructura declarada por el playbook de onboarding).
   Decisión registrada: el esqueleto **no** crea archivos
   de contenido de la tienda; un clon solo-sistema no es una
   instancia operable hasta restaurar sus registros
   (hallazgo B1-17 de la auditoría, propuesta P1 al
   framework). La raíz `data/tiendas/` no lleva `.gitkeep`
   (el chequeo 4 lo marcaría como dato suelto fuera de
   hogar).
4. **Purga del sistema:** `git-filter-repo
   --invert-paths --path data/` sobre la historia fusionada
   (la migración primero, la purga después, como en
   v0.16.0), restaurando el esqueleto en un commit posterior
   y force-push con lease explícito contra el hash esperado.
   Censo de cierre: **0 rutas de registros** de las 139 de
   contenido en árbol y en historial (por `ls-tree` commit
   a commit); el detalle de hashes va en «Fusión y cierre».

### El ciclo de escritura sigue funcionando

- **Puente:** `scripts/registros-datos.py` (nuevo, en el
  repo del sistema; declarado en `ARQUITECTURA-DATOS.md`,
  en la ruta de lectura de `FLUJO-PIPELINE.md` y en los
  skills que commitean registros). Los archivos físicos no
  se movieron — los flujos leen y escriben en
  `~/workspace/my-pod/data/…` como siempre — y el script
  versiona: `commit -m "<mensaje>"` trae el repo de datos
  (`pull --ff-only`), sincroniza los registros físicos al
  clon `~/workspace/my-pod-datos` (altas, cambios y bajas;
  nunca medios, checkpoints, CSV crudos ni la cola
  transitoria), commitea solo si hay cambios, pushea y
  verifica que no quede «ahead»; `pull` restaura el árbol
  físico desde el repo de datos.
- **Regla re-apuntada:** «escribir = commitear en la misma
  corrida, **en el repo que toca**» — texto actualizado en
  `ARQUITECTURA-DATOS.md` (con el mapa de repos), en
  `skills/estratega-tienda` **v0.6.1**,
  `skills/estratega-pinterest` **v0.1.4** y
  `skills/onboarding-tienda` **v0.1.4**, cada uno con su
  entrada de CHANGELOG.
- **Crons:** los cuerpos de los 7 crons que commitean
  registros se actualizaron **solo en su mecánica de
  commit** (`cron.update` preservando todo lo demás y
  verificación con `cron.view`): pinterest-diario,
  estratega-semanal, investigacion-semanal,
  revision-viernes, ritual-viernes-h12, trend-scan y
  propuestas-diarias (deshabilitado). Al runonce
  `etsy-sale-25-to-20-oct31` se le sumó el paso de commit
  de registros que le faltaba (escribe `config.json`). Los
  de solo lectura (watchdog, vigía) no necesitaron cambios:
  leen los archivos físicos, que no se movieron. El detalle
  cron por cron va en «Fusión y cierre».

## Cierre de la fase de mejora v0.16.0

Con esta unidad, la fase de mejora post-v0.16.0 queda
**cerrada** (registro en su propio documento,
`docs/FASE-MEJORA-V0160-PROPUESTA.md`): **P1 EJECUTADA**
(esta separación), **P2 EJECUTADA** (purga del staging,
2026-10-21), **P3 RESUELTA por la decisión D2** (el
respaldo de los registros ES el repo de datos; medios sin
respaldo externo por decisión explícita) y **P4
ABSORBIDA** (la lista extendida de Rameli v0.16.1 y la
mini-purga `.webp`). La fase de mejora de **esta**
migración se abre con su propuesta
(`docs/FASE-MEJORA-V0170-PROPUESTA.md`: P1 declaración del
repo de registros en el framework, P2 rutas del ritual de
los lunes) — **sin ejecutar**: espera el dale del dueño.

## Colocación (barrido de cierre)

- Toda herramienta usada como puerta o mecanismo en esta
  unidad vive donde el sistema dice: las puertas son las
  del framework (`bin/rameli` en v0.17.0); el mecanismo
  nuevo (`scripts/registros-datos.py`) vive en el repo del
  sistema y está declarado en `ARQUITECTURA-DATOS.md`, en
  la ruta de lectura y en los skills que lo invocan; la
  herramienta de cirugía (`git-filter-repo`) vive en su
  venv persistente declarado (`~/workspace/.venvs/
  filter-repo`), como en las cirugías anteriores.
- La evidencia de la unidad (respaldo íntegro, manifiestos
  sha256 antes/después, salidas de las puertas) vive con el
  respaldo en `~/workspace/respaldos/my-pod-pre-v0170-
  2026-10-21/` — es evidencia de la instancia, no del
  sistema.
- **Prueba de frío:** clon limpio del repo del sistema
  (árbol e historial sin registros, esqueleto presente) y
  clon limpio del repo de datos (registros íntegros contra
  el inventario previo); y la **instancia restaurada**
  combinando ambos (`registros-datos.py pull` sobre un
  clon del sistema) valida `rameli validar` sin fallos —
  el detalle va en «Fusión y cierre».

<!-- La sección «Fusión y cierre» se completa tras la purga
     y los pushes, con los hashes finales de ambos repos. -->
