# Regla: delivery de procesos automatizados a chats (2026-10-15)

**Problema:** procesos automatizados (crons, reportes de investigación,
notificaciones de propuestas) reabrían chats archivados en vez de crear
uno nuevo o ir al destino correcto.

**Causa raíz (investigación 2026-10-15):**
1. Los workers de cron NO tienen la herramienta `chat`: no pueden crear
   chats ni verificar si uno está archivado. Su único canal de entrega
   es el mensaje final, que el runtime lleva al `delivery` configurado.
2. El patrón viejo ("chat del día") delegaba al agente conversacional
   crear un chat nuevo por handoff. Si en vez de `chat.create` (fresh)
   se usaba `chat.send_message` al ID de un chat de un día anterior que
   el dueño ya había archivado, el runtime lo desarchivaba para entregar
   → el chat "reabría" en su lista.
3. Los cuerpos de cron decían "reporta en el chat" / "mensaje en este
   chat" sin nombrar el destino por rol ni prohibir explícitamente
   escribir en chats archivados.

## La regla

1. **Cada reporte automático tiene UN destino vivo:** el chat de
   `delivery` configurado en el cron (hub "📌 POD — Equipo y fábrica"
   para los crons del equipo POD; el chat de trabajo correspondiente
   para los demás). El destino se nombra por ROL en el cuerpo del cron,
   no solo por ID.
2. **NUNCA se escribe en un chat archivado.** Un chat archivado es una
   decisión del dueño (quitarlo de su vista). Ningún proceso automático
   la revierte.
3. **Si el destino configurado está archivado o no existe**, el reporte
   se entrega en un chat NUEVO (fresh) titulado
   `"<Nombre del reporte> · <fecha>"` — nunca reabriendo el archivado.
4. **El worker no nombra chats en su salida.** El cuerpo del cron prohíbe
   al worker mencionar IDs de chats viejos como destino ("en vez de crear
   uno nuevo" aplica al agente conversacional que procesa el handoff).
5. **Los chats de trabajo del dueño no se archivan** (regla vigente);
   los workers/background sí. Si un destino deja de ser el correcto, se
   cambia el `delivery` del cron con `cron.update`, no se improvisa en
   el cuerpo.

## Dónde vive

- Esta regla: `docs/REGLA-DELIVERY-CHATS.md` (este archivo).
- Cláusula operativa: cada cron POD la lleva en su cuerpo como
  "REGLA ANTI-REAPERTURA (2026-10-15)".
