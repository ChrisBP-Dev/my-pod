# Ejecución por workers y relevo del orquestador — adopción de la app

Adoptado en la fase de mejora post-v0.11.0 (P4, 2026-10-19), sobre
el registro de adopción por flujo de
`docs/MIGRACION-RAMELI-V0110.md`. La doctrina es del framework:
`rameli/docs/EJECUCION-POR-WORKERS.md`. Aquí viven solo las
calibraciones de ESTA aplicación.

## Registro de flujo (calibración)

- Cada tienda lleva su registro de flujo versionado junto a su
  ficha: `data/tiendas/<id>/registro-flujo.md` (plantilla:
  `rameli/templates/registro-flujo.md`).
- Los checkpoints `data/tiendas/<tienda-id>/estado-*.json` siguen siendo la capa fina
  local (gitignoreada): NO se duplican en el registro; el registro
  resume por unidad y apunta al checkpoint.
- El registro se actualiza al cerrar cada unidad, no en tiempo
  real.

## Watchdog de lote (calibración)

- Todo lote de publicación lanzado con `publicador-lote` lleva
  watchdog: una vigilancia programada que verifica el avance
  contra `data/tiendas/29222324/estado-publicacion.json` y despierta al
  orquestador si el lote se frena o falla en silencio.
- El watchdog se monta AL LANZAR el lote y se retira AL CERRARLO.
  Un lote sin watchdog es un lote mal lanzado.

## Relevo del orquestador (umbral, calibración v1)

El hub (chat central de la app) rota:

- **Entre fases**: al cerrar una fase mayor (una migración, un
  lote de producción completo, una fase de mejora) el siguiente
  trabajo abre en chat nuevo con el estado en el repo.
- **Por tiempo**: como máximo tras 7 días de operación continua
  del mismo hub.
- **Por degradación** (inmediato): dos o más errores de memoria o
  verificaciones omitidas detectados en una misma sesión.

El entrante verifica el estado contra el registro de flujo de la
tienda y los registros de fase vigentes ANTES de operar; si algo
no coincide, se corrige el registro, no se rellena de memoria.
Esta calibración se revisa con la primera rotación real.
