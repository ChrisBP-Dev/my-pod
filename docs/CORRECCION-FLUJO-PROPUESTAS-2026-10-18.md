# Corrección del flujo de propuestas — 2026-10-18 (orden del dueño)

## Qué pasó

En la era My POD el flujo cerró 2/2 lotes completos (2026-10-16: 67 min +
MPL en segunda pasada; 2026-10-17: 144 min en una corrida). El lote del
2026-10-18 es la primera falla: arrancó 07:00 y a las 18:00 seguía abierto.

Causa verificada, no teórica:

1. La corrida de la mañana quedó huérfana: el cron se editó (piloto
   nocturno: horario 18:00 + desactivado) con la corrida en vuelo; en el
   scheduler figura "queued, started_at=null" aunque hubo trabajo real
   07:43–08:28 que se detuvo sin registrar el diseño p049.
2. La creación de drafts se delegaba como UN bloque (una tarea de navegador
   para todos los diseños) y el registro quedaba en manos de otro agente,
   al final. División por FUNCIÓN: si el bloque se corta, nada quedó
   registrado aunque Printify sí avanzó (p050–p052 creados sin registro).
3. La recuperación repitió el patrón: su brief ordenaba "registrar en el
   acto", pero era texto sobre el mismo método. Ritmo medido: ~22 min por
   diseño por navegador (la subida directa a Printify vía CLI sigue rota
   desde 2026-10-06); 8 diseños + MPL no cabían en su presupuesto de 2 h.
4. Cada "mejora" de los días previos agregó pasos a la MISMA corrida
   monolítica (MPL obligatorio dentro de la corrida, checkpoints, puerta
   nueva) sin dividir el trabajo. El watchdog detecta; no ejecuta mejor.

## Corrección (vigente desde el lote 2026-10-19)

- **División por diseño, no por función.** Cada diseño es una unidad
  cerrada: crear componentes → sincronizar → ensamblar MPL → registrar →
  verificar, antes de tocar el siguiente. Una tarea de navegador lleva
  COMO MÁXIMO una tanda de 3 diseños, y entre diseño y diseño se
  sincroniza.
- **El registro lo escribe un script, no el agente.**
  `scripts/sincronizar-registro-printify.py --fecha <hoy> --aplicar`
  lee Printify real (solo lectura) y rellena los IDs del registro y el
  checkpoint. El agente no transcribe IDs a mano. Única excepción:
  `mpl_draft_id` (vive fuera del listado de Printify), que se registra
  inmediatamente tras ensamblar ese diseño.
- **Presupuesto por tanda, con continuación programada.** Tanda = 3
  diseños (~66 min al ritmo medido). Si el tiempo de la corrida no
  alcanza para otra tanda completa, la corrida cierra limpio (sync +
  commit + push) y programa su continuación en +15 min. Nunca trabajo
  sin registrar, nunca silencio.
- **Congelamiento de pasos.** No se agregan pasos, puertas ni chequeos
  nuevos a este flujo sin orden expresa del dueño. Proteger el avance no
  puede volver a costar lo que ya funcionaba.

## Calibración del script de sync (2026-10-18, en seco contra Printify real)

p048/p049 = ok (conocidos buenos) · p050–p053 = completos detectados
(p053 posterior al último chequeo del watchdog) · p054 = parcial
(sudadera creada, playera en curso en ese momento) · p055–p057 = sin
drafts · 0 conflictos. El PASS del script significa que el registro
refleja Printify, no una promesa del agente.
