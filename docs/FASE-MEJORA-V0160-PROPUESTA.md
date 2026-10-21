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

## Lo que esta fase NO propone

- Tocar los 15 `.png` de `skills/puerta-arte-propuesta/
  evals/fixtures/`: son calibración **del sistema** (viven
  en el repo a propósito desde la fase de mejora v0.14.0);
  el estándar los ubica ahí, no bajo la raíz de datos.
- Reabrir la reclasificación de `data/auditoria-2026-10-15`:
  declarada y verificada en esta migración.
- Ningún cambio en listings, ofertas ni operación comercial:
  esta fase es de sistema, como la migración que la abrió.
