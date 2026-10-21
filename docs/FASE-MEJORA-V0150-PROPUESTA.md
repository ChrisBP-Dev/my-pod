# Fase de mejora post-migración v0.15.0 — PROPUESTA (2026-10-20)

Abierta automáticamente al cerrar la migración a Rameli
v0.15.0, como manda `rameli/MIGRACIONES.md`, con la
**auditoría de adopción completa** como primer insumo — en
esta migración era **no diferible** (el delta trae capacidad
nueva) y se corrió: `docs/AUDITORIA-ADOPCION-V0150.md`. Una
sola brecha: **B1 (C24 × F2/F9)**.

**Dale de ejecución: dado por el dueño en la orden de esta
sesión (2026-10-20)** — la misión aprobada manda auditar
dónde aplica el deber en esta app e implementar la adopción
donde aplique. La fase corre como fase propia (rama
`mejora-v0150`, puertas propias), nunca mezclada con la
migración; su estado de ejecución queda al final de este
documento.

## P1 — Escribir el corte donde esta app corta (B1)

- **Qué, en dos piezas:**
  1. `docs/EJECUCION-Y-RELEVO.md` gana la sección «Corte en
     las puertas que la ficha declara (Rameli v0.15.0)»: la
     regla local del deber — todo brief o manifiesto que
     esta app corte para una tienda se corta en la
     siguiente puerta que su ficha y su registro de flujo
     declaran (la primera: la aprobación del dueño antes de
     publicar), declara su corte, y la ausencia de puerta
     declarada se registra — más la tabla de aplicación por
     flujo que la auditoría verificó (F2 y F9 aplican; F1
     puerta equivalente dentro del flujo; F3–F8 no aplica,
     con su motivo).
  2. `publicador-lote` (v0.1.5 → v0.1.6): su paso de
     invocación gana el chequeo previo al corte — leer la
     ficha de la tienda (`config.json`) y su registro de
     flujo, y cortar el manifiesto EN la puerta de
     aprobación: solo entra un slug con aprobación
     registrada del dueño (revisado por él como MPL
     unpublished en Printify, según su criterio del
     2026-10-20); un producto suelto nunca vuelto MPL no
     fue revisado, no está aprobado y **no entra** — queda
     fuera y se reporta aparte, nunca mezclado en el lote.
     El manifiesto declara su corte (la puerta en la que se
     cortó y dónde vive la declaración).
- **Impacto:** el criterio de aprobación que hoy vive en la
  memoria del sistema pasa al paso exacto que corta el
  lote; el incidente del 2026-10-20 (remanentes mezclados
  en un lote aprobado) deja de depender de que el agente
  principal lo recuerde.
- **Riesgo:** bajo — procedimiento y documentación; no
  cambia el pipeline por listing, datos ni fichas. Se
  verifica con lint y regresión comparados y `rameli
  validar`.
- **Orden:** 1 (única propuesta de esta fase).

## Estado de ejecución

*(Se completa al ejecutar la fase en su rama propia; la
migración no la ejecuta.)*
