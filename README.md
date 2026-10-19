# my-pod — aplicación POD (cuarto limpio)

App construida con Rameli **v0.12.1** (pineado en `rameli.json`).
Valida el framework en el camino más corto antes de construir My Channels.

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
| `estratega-tienda` | v0.5.2 | Dirección semanal de tienda: reparto de foco, mix, guía de precios, NO-hacer |
| `estratega-pinterest` | v0.1.2 | Parrilla de Pinterest: 5 pins/día, mix por listing |
| `onboarding-tienda` | v0.1.3 | Playbook de puesta en marcha: de cero a tienda operativa |
| `paquete-listing-etsy` | v0.2.0 | Paquete comercial del listing: título, descripción, tags, keywords |
| `publicar-printify-etsy` | v0.7.3 | Drafts en Printify → ensamblaje MPL → publicación en Etsy |
| `publicador-lote` | v0.1.3 | Lote aprobado → side chat: manifiesto explícito, checkpoints por listing, reporte |
| `puerta-arte-propuesta` | v0.5.2 | Arte listo: PNG 300 DPI, fondo transparente, sin blanco puro |
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

- `data/tiendas/29222324/registro-listings.json` — registro de diseños y listings con sus assets finales aprobados (45 claves, 21 publicados completos al 2026-10-19).
- `data/banco-keywords/` — bancos de keywords por nicho.
- `data/cola-pins/` — pins que pasaron la puerta, en espera de publicación.

## Criterios canónicos

- `FLUJO-PIPELINE.md` — el flujo end-to-end Printify-first + MPL vigente.
- `CRITERIO-VIDEO.md` — criterio de los videos de listing (1080×1080, 9.5 s, zoom sin temblor).
- `ARQUITECTURA-DATOS.md` — qué dato vive dónde (global vs por tienda) y el ciclo de vida de los activos.
- `docs/PATRONES-RESILIENCIA.md` — health-check, checkpoints con resume y reintentos acotados.
- `docs/CONTRATO-TIPO-PRODUCTO.md` — contrato estratega → propuestas → publicación (tipo de lote).
- `docs/DELIMITACIONES-ADOPCION.md` — estatus declarado de lo no adoptado (capa de juicio, orquestación del runtime) y dueño del flujo comercial F7.
