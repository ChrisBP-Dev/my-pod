# Fase de mejora post-migración v0.16.0 — PROPUESTA (2026-10-20)

Abierta automáticamente al cerrar la migración a Rameli
v0.16.0, como manda `rameli/MIGRACIONES.md`, con la
**auditoría de adopción completa** como primer insumo — en
esta migración era **no diferible** (el delta trae capacidad
nueva) y se corrió: `docs/AUDITORIA-ADOPCION-V0160.md`.
Tres brechas (B1–B3) y una micro-decisión (P4).

**Estado: PROPUESTA — nada se ejecuta sin el dale del
dueño.** A diferencia de la fase v0.15.0, la orden de esta
sesión no incluye dale de ejecución para estas propuestas:
son decisiones de alcance mayor (B1), de material cuyo dueño
de flujo debe confirmar (B2) o de gasto/servicio (B3), y
quedan registradas aquí con impacto, riesgo y orden.

**Actualización de estado (2026-10-21, cierre):** **P1
EJECUTADA** (decisión D1 del dueño, confirmada el
2026-10-21 01:09 EDT; evidencia en su sección y en
`docs/MIGRACION-RAMELI-V0170.md`), **P2 EJECUTADA**
(decisión del dueño de 2026-10-21 00:39 EDT; evidencia en
su sección), **P3 RESUELTA por la decisión D2 del dueño**
(el respaldo de los registros ES el repo de datos de D1;
los medios quedan sin respaldo externo por decisión
explícita; nota en su sección) y **P4 ABSORBIDA** (Rameli
v0.16.1 extendió la lista canónica y la mini-purga eliminó
el único `.webp`; nota en su sección). **La fase de mejora
v0.16.0 queda CERRADA: sus cuatro propuestas resueltas.**

## P1 — Separar los registros de la instancia del repo del sistema (B1)

- **Qué:** crear el respaldo versionado de la instancia
  (repo privado propio de datos, p. ej. `my-pod-datos`) y
  mover a él el tracking de los registros de texto de la
  tienda (`data/tiendas/29222324/` y los registros globales
  de texto bajo `data/`), dejando en el repo del sistema el
  esqueleto de datos vacío. Incluye reescribir la regla
  «escribir = commitear en la misma corrida» de los skills y
  crons de la tienda para que commiteen en el repo de datos,
  y decidir si también se purga su historial del repo del
  sistema (segunda cirugía, menor: son texto, ~pocos MB).
- **Impacto:** completa la adopción del estándar en su
  clase «registros»: el repo del sistema queda distribuible
  tal cual (sistema + esqueleto), y la historia comercial de
  la tienda gana respaldo propio sin viajar con el sistema.
- **Riesgo:** medio-alto — toca el ciclo de escritura de
  todos los crons vivos de la tienda (Pinterest, estratega,
  rituales) y cada ruta que hoy asume «el registro vive en
  este repo». Exige su propio brief, su ventana con la
  tienda en pausa y migración de los flujos por fases.
- **Orden:** 3 — después de P2/P3, y solo con brief propio.

- **EJECUTADA el 2026-10-21 — decisión D1 del dueño**
  (paquete completo confirmado el 2026-10-21 01:09 EDT),
  como alcance de la unidad «actualización oficial a Rameli
  v0.17.0 + separación de registros», con su brief propio
  (`~/workspace/migraciones-v0170/brief-my-pod-v0170.md`).
  **Evidencia:** repo privado `my-pod-datos` creado en
  GitHub (cuenta ChrisBP-Dev, por el navegador); la historia
  de los registros se separó por rutas `data/` desde los 164
  commits del sistema (88 commits tocan registros; árbol de
  registros idéntico blob a blob, 143/143); el repo del
  sistema se reescribió sin registros en árbol ni en
  historial, conservando el esqueleto (`.gitkeep` de los
  hogares declarados); la regla «escribir = commitear» se
  re-apuntó en `ARQUITECTURA-DATOS.md`, en los skills
  estratega-tienda v0.6.1, estratega-pinterest v0.1.4 y
  onboarding-tienda v0.1.4 y en los cuerpos de los crons
  vivos de la tienda — registros al repo de datos vía
  `scripts/registros-datos.py`, sistema a este repo — y la
  media física quedó intacta (manifiesto sha256 551/551).
  Registro completo: `docs/MIGRACION-RAMELI-V0170.md`.

## P2 — Resolver `tmp/videos-pendientes/` (B2)

- **Qué:** decidir el destino de los 30 `.jpg` trackeados
  (50 archivos físicos, 37 MB) que ningún consumidor
  declarado referencia: si es material vivo, moverlo a su
  hogar canónico bajo `data/` (donde la política ya lo
  cubre) y des-trackearlo; si es remanente de la producción
  de videos ya publicados (sus salidas viven en
  `data/videos/` y en Etsy), eliminarlo del tracking y del
  disco con su mini-purga de historial (~37 MB).
- **Impacto:** cierra el último rincón del repo donde un
  medio de producción sigue versionado; `tmp/` vuelve a ser
  scratch, que es su nombre.
- **Riesgo:** bajo — ningún consumidor lo referencia
  (verificado por barrido); el único cuidado es la
  confirmación de que no es material en espera de uso.
- **Orden:** 1 — rápido y de bajo riesgo cuando el dueño
  confirme si el material es vivo o remanente.

- **EJECUTADA el 2026-10-21 — decisión del dueño
  (2026-10-21 00:39 EDT): ELIMINAR por completo**
  (tracking, historial y disco), por encima de la opción
  conservadora de conservar los `.mp4`. Su criterio: el
  flujo de videos cerró y se publicó el 2026-10-16
  (registro con `videos_pendientes=false` en las 21
  entradas), las salidas viven en Etsy y el set canónico
  local está en `data/videos/`, y el flujo de Pinterest
  consume solo `data/videos/` (puerta-pinterest-pin: el
  asset del pin de video es el MP4 final del listing en
  `data/videos/`, «nada generado ad-hoc») — ningún
  consumidor vivo necesita la carpeta.
  **Evidencia:** respaldo previo verificado (bundle
  `--all`, historia completa en `cec7aac`, sha256
  `8b3573f1…`) en
  `~/workspace/respaldos/my-pod-pre-purga-p2-2026-10-21/`;
  purga de la ruta en todo el historial con
  `git-filter-repo` y borrado de la carpeta del disco
  (50 archivos, 38,343,335 B; los 10 `.mp4` nunca
  trackeados se eliminaron del disco con la carpeta, como
  manda la decisión de eliminar «por completo» — su
  contenido vive publicado en Etsy); force-push con lease
  (`cec7aac → 9379608`, sin actividad ajena). Censo de la
  ruta: **0 en disco y 0 en los 163 commits** (por
  `ls-tree` y por `rev-list --objects`); el censo extendido
  (18 extensiones) del historial completo queda solo con
  los 15 fixtures vivos de `puerta-arte-propuesta`. Pack:
  42.99 MiB → **29.81 MiB**. `data/` físico intacto
  (sha256 551/551, 1,770,117,400 B) y el archivo vivo de
  `tmp/` (investigación de personalización, de otro
  trabajo) intacto. Puertas post-purga en verde (lint,
  regresión 53 casos, `rameli validar` 0/0) en el commit
  de cierre de esta ejecución.
  **Criterio destilado a canon por orden suya:** la regla
  de ciclo de vida del staging vive ahora en
  `FLUJO-PIPELINE.md` §5.1 (con puntero en
  `CRITERIO-VIDEO.md`) y `rameli.json` declara
  `datos.zonas_staging: []` — ninguna zona viva; toda zona
  futura nace declarada y se purga en el cierre de su
  flujo.

## P3 — Decisión de respaldo externo de medios (B3)

- **Qué:** el dueño elige el respaldo de los medios fuera
  de esta máquina (nube, almacenamiento de objetos o disco
  externo) para los ~1.77 GB de `data/` físico, que crecen
  con cada lote. Mientras tanto, la copia íntegra verificada
  de esta migración
  (`~/workspace/respaldos/my-pod-pre-v0160-2026-10-20/`)
  queda como respaldo local de referencia, y las piezas
  finales conservan su copia en Printify/Etsy.
- **Impacto:** la clase «medios» del estándar queda con su
  responsabilidad de respaldo cerrada por decisión, no por
  accidente: perder esta máquina ya no significaría perder
  artes y mockups irrecuperables (los intermedios se
  regeneran desde su registro; los artes «crudo» no).
- **Riesgo:** el de no hacerlo — punto único de falla local.
  La decisión puede ser «sin respaldo externo, aceptado»:
  lo que el estándar exige es que sea explícita.
- **Orden:** 2 — decisión suya; la ejecución, si la elige,
  es mecánica.

- **RESUELTA el 2026-10-21 por la decisión D2 del dueño**
  (conversación de la actualización a v0.17.0, confirmada
  con el paquete el 2026-10-21 01:09 EDT): **sin servicios
  pagos, sin cuentas nuevas y sin flujos extra de respaldo**
  — el respaldo versionado de los registros ES el repo
  privado de datos de P1 (`my-pod-datos` en GitHub, gratis;
  el sistema commitea solo, el respaldo es el flujo), y los
  **medios quedan sin respaldo externo por decisión
  explícita**: son temporales por diseño, los finales viven
  en las plataformas (Etsy/Printify) y el staging se purga
  al cierre de su flujo; el riesgo de perder crudos no
  publicados si la máquina cayera queda aceptado. La copia
  local verificada de la migración a v0.16.0
  (`~/workspace/respaldos/my-pod-pre-v0160-2026-10-20/`)
  sigue como referencia local. No queda decisión: la
  responsabilidad de respaldo de cada clase quedó cerrada
  por decisión, como exige el estándar.

## P4 — Micro-decisión: `.webp` en el bloque local de `.gitignore`

- **Qué:** sumar `data/**/*.webp` al bloque de medios del
  `.gitignore` de esta app (el bloque canónico de
  `rameli init` no lo trae, y el chequeo 5 tampoco lo
  cubre). Solo aplica si algún flujo vuelve a producir
  `.webp` bajo `data/`; hoy no hay ninguno físico.
- **Impacto/riesgo:** mínimo; es una línea local que no se
  propone subir al framework desde aquí (si el patrón se
  repite en otra app, nacería como contribución a Rameli).
- **Orden:** 4 — junto con cualquier toque futuro del
  `.gitignore`, o nunca si el formato no reaparece.
- **ABSORBIDA el 2026-10-21 (sin ejecutar como estaba
  planteada):** Rameli **v0.16.1** extendió la lista
  canónica del framework (webp/avif/heic/heif/gif/bmp/
  tif/tiff) en los tres lugares — ya no es una línea local
  pendiente — y la mini-purga del 2026-10-21 eliminó el
  único `.webp` del historial de esta app. No queda
  decisión: si un flujo produce `.webp` bajo `data/`, el
  chequeo extendido ya lo detecta (el framework corre en
  v0.16.1 sin que la app cambie su pin) y el bloque de
  `.gitignore` extendido entrará con la próxima migración
  que lo adopte.

## Lo que esta fase NO propone

- Tocar los 15 `.png` de `skills/puerta-arte-propuesta/
  evals/fixtures/`: son calibración **del sistema** (viven
  en el repo a propósito desde la fase de mejora v0.14.0);
  el estándar los ubica ahí, no bajo la raíz de datos.
- Reabrir la reclasificación de `data/auditoria-2026-10-15`:
  declarada y verificada en esta migración.
- Ningún cambio en listings, ofertas ni operación comercial:
  esta fase es de sistema, como la migración que la abrió.
