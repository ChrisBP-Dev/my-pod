# Regla: delivery de procesos automatizados a chats (2026-10-15, act. 22:30)

**Preferencia del dueño (2026-10-15, verbal):** cada investigación,
cada reporte, cada notificación automática va en un **chat NUEVO**
(fresh), nunca en el hub ni en un chat archivado.

**Problema original:** procesos automatizados (crons, reportes de
investigación, notificaciones de propuestas) reabrían chats archivados
en vez de crear uno nuevo.

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

## La regla (vigente)

1. **Cada reporte automático vive en un chat NUEVO** (fresh), titulado
   según su tipo: `📌 POD — Propuestas · <fecha>`,
   `🔍 POD — Investigación · <fecha>`, `📊 POD — Estratega · <fecha>`,
   `📋 POD — Revisión viernes · <fecha>`, `📈 POD — Trends · <fecha>`,
   `📌 POD — Pinterest · <fecha>`, `⚠️ POD — Alerta watchdog · <fecha>`.
2. **Mecánica:** el worker termina con su mensaje final = SOLO el
   reporte, primera línea `TÍTULO: <título del chat nuevo>`. El agente
   conversacional (al procesar el handoff en el hub) crea el chat con
   `chat.create` (fresh) y publica el reporte ahí con `chat.send_message`.
   En el hub solo queda una línea indicando dónde quedó el reporte.
3. **NUNCA se escribe en un chat archivado.** Un chat archivado es una
   decisión del dueño (quitarlo de su vista). Ningún proceso automático
   la revierte. El worker no menciona IDs de chats viejos como destino.
4. **Excepción:** el watchdog en silencio (sin alertas) no crea ningún
   chat.
5. **Los chats de trabajo del dueño no se archivan** (regla vigente);
   los workers/background sí. Si un destino deja de ser el correcto, se
   cambia el `delivery` del cron con `cron.update`, no se improvisa en
   el cuerpo.

## Dónde vive

- Esta regla: `docs/REGLA-DELIVERY-CHATS.md` (este archivo).
- Cláusula operativa: cada cron POD la lleva en su cuerpo como
  "ENTREGA (2026-10-15, preferencia del dueño)".
- Preferencia durable: `~/MEMORY.md` (delivery de reportes POD).

## Actualización 2026-10-16: nomenclatura My POD + multi-tienda

Por decisión del dueño:
- El hub se llama **🏭 My POD — Central** (antes "📌 POD — Equipo y fábrica").
- Los chats de reporte incluyen la tienda: `📌 My POD · <tienda> — <Tipo> · <fecha>`
  Ejemplo: `📌 My POD · MyNightShiftShop — Propuestas · 2026-10-16`
- Motivo: si más adelante hay más tiendas, cada reporte se distingue por tienda.
