# Fase de mejora post-migración v0.17.0 — PROPUESTA (2026-10-21)

Abierta automáticamente al cerrar la migración a Rameli
v0.17.0, como manda `rameli/MIGRACIONES.md`, con la
**auditoría de adopción completa** como primer insumo —
en esta migración era **no diferible** (el delta trae
capacidad nueva) y se corrió:
`docs/AUDITORIA-ADOPCION-V0170.md`. Una brecha (B1-17) y
una observación (el ritual de los lunes).

**Estado: PROPUESTA — nada se ejecuta sin el dale del
dueño.** La migración misma y la separación de registros
D1 se ejecutaron con el dale del paquete completo
(2026-10-21 01:09 EDT); estas dos propuestas nacen DE la
auditoría de esta unidad y esperan su palabra, cada una
en su ámbito (framework y flujo, respectivamente).

## P1 — Declarar el repo de registros en el framework (B1-17)

- **Qué:** proponer a Rameli, por la vía de contribución
  (`rameli/docs/CONTRIBUCIONES.md`), dos piezas que la
  separación D1 dejó al descubierto: (1) un campo de
  declaración en `rameli.json → datos` para el respaldo de
  registros de la instancia (p. ej. el repo de datos que la
  instancia usa), de modo que el sistema declare dónde
  viven sus registros en vez de saberlo solo su operador;
  y (2) que el chequeo 4 trate el hogar de unidad presente
  pero sin registros — en una app que declara separación —
  con **ámbito de instancia** (AVISO: «registros sin
  restaurar en esta copia»), como ya hace con
  `historial_instancia`, en vez de FALLO de hogar
  incompleto. Hoy la instancia restaurada (sistema + datos
  + `registros-datos.py pull`) valida 0/0 y el clon
  solo-sistema marca FALLO: la señal es honesta pero ciega
  a la causa.
- **Impacto:** cualquier app que adopte D1 (My Channels
  está ejecutando la misma separación en su unidad)
  valida con la semántica correcta en los dos estados
  (con y sin registros restaurados), y la declaración del
  repo de datos viaja con el sistema: un clon frío sabe
  dónde buscar los registros de su instancia.
- **Riesgo:** bajo-medio — toca el validador del framework
  (chequeo 4) y el esquema de `rameli.json`; exige sus
  fixtures en la regresión del framework y versión nueva
  de Rameli. No toca datos ni operación de la tienda.
- **Orden:** 1 — cuando el dueño lo apruebe; nace como
  contribución desde esta app, no como parche local.

## P2 — Revisar las rutas del ritual de los lunes (H04)

- **Qué:** el cron `pod-ritual-lunes-h04` referencia
  bancos y fichas en `docs/investigacion/keywords/` y
  `docs/investigacion/nichos/` — rutas que no existen en
  este repo desde el reorden de datos (2026-10-19); su
  insumo real hoy vive en `data/tiendas/29222324/
  investigaciones/` y `data/banco-keywords/`. Revisar su
  cuerpo contra el layout vigente y corregir las rutas
  (o declarar el ritual retirado, si el flujo ya lo
  absorbió la investigación semanal). No commitea
  registros en `my-pod`, por lo que quedó fuera del
  inventario D1 de esta unidad; se detectó en su
  inventario de Paso 0.
- **Impacto:** el ritual vuelve a leer insumos reales (o
  deja de correr en vacío cada lunes).
- **Riesgo:** bajo — es un cuerpo de cron; el cuidado es
  no duplicar el trabajo de `equipo-pod-investigacion-
  semanal`, que corre el mismo lunes.
- **Orden:** 2 — con la palabra del dueño sobre si el
  ritual sigue vivo como flujo propio.

## Lo que esta fase NO propone

- Tocar la operación comercial (listings, ofertas,
  precios): esta fase es de sistema, como la migración
  que la abrió.
- Mover el esqueleto de datos: su forma actual
  (`.gitkeep` de hogares declarados, sin contenido) es la
  verificada en la prueba de frío de esta unidad; cambiarla
  es consecuencia de P1, no una propuesta separada.
- Reabrir D2: la decisión de respaldo quedó cerrada por
  el dueño el 2026-10-21 (registros → repo de datos;
  medios sin respaldo externo, por decisión explícita).
