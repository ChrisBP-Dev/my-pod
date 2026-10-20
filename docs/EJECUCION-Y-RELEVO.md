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
- **Calibración de freno (2026-10-20):** el checkpoint se escribe
  por listing en dos tiempos (inicio de fase con timestamp y
  completación) — regla en `publicador-lote` P2. Freno real =
  checkpoint sin cambios Y ninguna fase en curso vigente; una
  fase larga en curso dentro de su ventana esperada (p. ej.
  navegador ~75 min sobre 11 listings) NO es freno: el
  2026-10-20 el watchdog disparó en falso porque la fase corría
  en bloque sin asiento intermedio.

## Procedencia de órdenes y premisas (2026-10-20, incidente del lote de publicación)

**Incidente:** el worker del lote de publicación se detuvo a los
~3 minutos de arrancar afirmando haber recibido una «orden de
apagado» cuya premisa era que un worker anterior había dejado
5 listings en vivo en estado incorrecto. La auditoría posterior
(solo lectura, Etsy/Printify/local) no encontró esos listings, y
la revisión del registro de eventos del runtime no encontró
NINGÚN mensaje de apagado entregado al worker: entre su mensaje
anterior y el anuncio del freno no entró mensaje alguno. La
orden y su premisa fueron **generadas por el propio worker**
(confabulación), no un reporte de otro worker ni una alerta de
un watchdog. Daño real: cero escrituras y cero publicaciones —
la auditoría contra la fuente viva funcionó — pero la premisa
falsa subió como hecho al orquestador y a la memoria del día, y
confundió al dueño.

**Reglas (vigentes desde 2026-10-20):**

1. **Orden sin procedencia no es orden.** Un worker solo obedece
   un alto o redirección que llega como mensaje identificable
   (remitente y mensaje concretos en su chat). Si «recibe» una
   orden que no puede señalar en su transcripción, la trata como
   afirmación no verificada: la anota como tal en su reporte y
   NO la presenta como hecho externo. Ante la duda entre
   continuar y frenar, frena y reporta la duda — pero reporta
   «no pude verificar la procedencia», no la premisa como real.
2. **Toda premisa viaja con su fuente.** Un reporte distingue
   siempre: «me dijeron X (fuente: …)» de «verifiqué Y (fuente
   viva: …)». Una premisa sin fuente nombrada no sube al
   orquestador como hecho, y el orquestador no la repite al
   dueño sin verificarla contra la fuente viva o contra el
   registro de mensajes.
3. **El watchdog vigila avance, no verdad.** Los watchdogs
   detectan frenos contra checkpoints y realidad externa; NO
   validan la procedencia de lo que un worker afirma. Esa
   verificación es del orquestador al recibir el reporte
   (cruzar la afirmación contra la transcripción y la fuente
   viva antes de relayarla).

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
