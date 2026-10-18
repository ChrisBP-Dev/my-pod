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
- **Tandas con red de seguridad, no fragmentación.** La tanda (máx. 3
  diseños por tarea de navegador) limita el tamaño del bloque delegado;
  el registro se cierra por diseño dentro de la misma corrida, como en
  las corridas que funcionaron. Solo si la corrida lleva ≥150 min y
  quedan diseños, cierra limpio (sync + commit del registro — el
  checkpoint es local, no se versiona; se reconstruye con el sync) y
  programa su continuación en +15 min. Nunca trabajo sin registrar,
  nunca silencio. (Umbral corregido en la auditoría del mismo día: el
  umbral original de 50 min fragmentaba cada lote en 3–4 corridas —
  más recargas de contexto y más créditos sin beneficio.)
- **Congelamiento de pasos.** No se agregan pasos, puertas ni chequeos
  nuevos a este flujo sin orden expresa del dueño. Proteger el avance no
  puede volver a costar lo que ya funcionaba.

## Calibración del script de sync (2026-10-18, en seco contra Printify real)

p048/p049 = ok (conocidos buenos) · p050–p053 = completos detectados
(p053 posterior al último chequeo del watchdog) · p054 = parcial
(sudadera creada, playera en curso en ese momento) · p055–p057 = sin
drafts · 0 conflictos. El PASS del script significa que el registro
refleja Printify, no una promesa del agente.

## Auditoría de la propia corrección (2026-10-18, pedido del dueño)

Huecos cazados en la v1 y cerrados en la v2 del script / cuerpo del cron:

1. El script reescribía el registro con indent=1 (el archivo usa 2):
   cada sync habría generado un diff gigante y riesgo de conflicto.
   v2 conserva el formato de cada archivo y escribe atómico (tmp+rename).
2. Match por título sin fecha: un draft huérfano viejo con el mismo
   título podía capturarse como el de hoy. v2 prefiere creados en/después
   de `fecha_propuesta`; si solo hay match anterior → SOSPECHOSO, no se
   registra.
3. "Sin drafts" era una afirmación falsa posible: el listado cubre la
   página 1 (50 de 82). v2 reporta NO_ENCONTRADO y suma `--verificar-ids`
   (confirma IDs registrados uno a uno, cualquier página; probado:
   p048/p049 verificados).
4. Track single quedaba marcado incompleto para siempre (exigía ambos
   componentes). v2 juzga completitud según el track/componentes.
5. El cuerpo del cron ordenaba commitear el checkpoint, pero
   `estado-propuestas.json` está en .gitignore (no se versiona): la
   orden era imposible. Corregido a "commit solo del registro".
6. Referencia muerta: el texto de reintento citaba "secciones A–E" y el
   cuerpo nuevo tiene A–D. Corregido.
7. Sin regla de parada ante CONFLICTO del sync (exit 2). Agregada:
   ante conflicto se detiene la tanda y se reporta; no se crea sobre un
   registro en conflicto.

Residuales honestos (no cerrados, con mitigación):

- `mpl_draft_id` se sigue registrando a mano al ensamblar (el MPL no
  sale del listado de productos de Printify). Mitigación: se registra en
  la unidad del diseño, no al final del lote, y la entrega exige el sync
  final + verificación del dueño en su revisión nocturna.
- Dos corridas simultáneas (continuación + diaria) podrían pisarse el
  registro. Mitigación parcial: escritura atómica del script y
  catchup=latest del scheduler; el riesgo baja porque la continuación
  solo nace cuando la corrida madre ya cerró.
- El watchdog (cada 30 min, orden del dueño del 2026-10-18) ahora es en
  parte redundante: el sync dentro del flujo ya reconcilia registro vs
  Printify. Su valor restante es detectar frenadas. Costo: ~48 corridas
  diarias de agente. Decisión de bajarlo a cada 2 h: del dueño.
