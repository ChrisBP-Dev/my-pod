---
name: "publicador-lote"
description: "Publica un lote de diseños APROBADOS por el dueño: un side chat por lote, manifiesto explícito de aprobados, pipeline por listing sobre publicar-printify-etsy (M3→M9), checkpoints con resume por listing, videos en paralelo y nunca regenerados, fallos aislados sin bloquear el lote, y protocolo de rollback. Formaliza lo que antes ocurría por accidente."
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.1.1"
  framework_version: "0.9.0"
---

# Publicador de lote POD

**Versión 0.1.1** (2026-10-16: el flujo post-aprobación existía y
funcionaba, pero sin vehículo diseñado — corría donde el dueño
respondiera, sin checkpoints. Este skill lo formaliza: un side chat por
lote, manifiesto explícito, resume por listing).

## Principio

Publicar es la acción más delicada del sistema (dinero, listings
públicos). Por eso: **un lote = un side chat = un worker = un reporte**.
El chat arranca limpio (solo el manifiesto), el contexto del chat
principal no se toca, y el lote sobrevive a caídas a mitad de camino.

## Invocación (la ejecuta el agente principal, no el worker)

1. El dueño aprueba: responde "publica todos" o dicta la lista en el
   chat de reporte (o en el principal).
2. El agente principal **resuelve el manifiesto**: lista explícita de
   `{slug, id_etsy, mpl_id}`. "Todos" = los slugs del reporte de ESE
   chat, nunca una suposición. Lo que el dueño borró o no nombró NO
   entra.
3. Crea un side chat nuevo (`chat.create`), título
   `📦 POD — Publicación · <fecha>`.
4. Pasa al worker el manifiesto + la orden de leer este skill. El
   worker no decide QUÉ publicar, solo ejecuta el manifiesto.

## Pipeline por listing

Por cada slug del manifiesto, en orden, delegando en
`publicar-printify-etsy` (v0.7.1): **M3** paquete SEO → **M5** mockups
(desde Printify, sin generar propios) → **M6** videos →
**M7** publicar → **M8** verificación Fase C → **M9** registrar.
M2 (revisión del dueño) ya ocurrió: es la aprobación que originó el
lote. M10 (Pinterest) lo cubre el cron de Pinterest con la parrilla.

## Enrutamiento API vs navegador (2026-10-16)

**API-first.** Canon: `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` — tabla
de enrutamiento (qué va por API con qué scope, qué va por navegador).
Todo lo que el API de Etsy cubre se hace por API (determinista, rápido,
verificable por máquina); el navegador es solo para lo que el API no
expone. El pipeline M3→M9 heredado de `publicar-printify-etsy` ya trae
este enrutamiento; este skill lo **exige**, no lo relaja: si un paso
tiene vía API disponible, se usa la vía API. La conexión es por tienda
(skill `conectar-etsy-api`, `config.json → etsy_api`).

## Patrones de resiliencia (docs/PATRONES-RESILIENCIA.md)

- **P1 — Salud:** antes de empezar, health-check de Printify
  (`https://printify.com/app/` → 200) y de la API de Etsy. Si un
  servicio está caído: no se empieza, se reporta, y el agente principal
  re-dispara cuando vuelva (a demanda: sin reintentos programados).
- **P2 — Checkpoints:** `data/estado-publicacion.json`
  (gitignoreado):
  `{"lote_actual": {"fecha": "YYYY-MM-DD", "manifiesto": [slugs],
  "fases_ok": {"slug": ["seo","mockups","video","publicado",
  "verificado"]}}, "videos": {"slug": "/ruta/video.mp4"}}`.
  Actualizar INMEDIATAMENTE tras cada fase. Si el worker muere, el
  siguiente retoma donde quedó — nunca repite fases hechas.
- **P3 —** no aplica como reintento programado (el lote es a demanda);
  el escalado es el reporte al principal.

## Videos: paralelo y nunca regenerados

- Generar los videos del lote **en paralelo** (hasta 6 por tanda,
  regla del sistema).
- **REGLA DURA:** si `videos.<slug>` existe en disco y el archivo es
  válido → NO regenerar. El video es el paso caro del pipeline.

## Fallos: aislados, nunca bloquean el lote

- Un listing falla (gate, API, navegador) → se registra la causa, se
  continúa con el resto, y el fallo va al reporte con su causa.
- Al final: reintento único de los fallidos solo si la causa fue
  externa y ya se resolvió. Si la causa es del asset/datos, queda para
  el dueño.

## Rollback

Si un listing se publica con error (mockup o arte equivocado,
precio mal):
1. Despublicar o poner en draft según el caso (API o navegador).
2. Corregir la fase afectada y re-ejecutar desde ahí.
3. Re-verificar Fase C completa antes de republicar.
4. Reportar qué pasó y qué se corrigió. Nunca "arreglar en silencio".

## Reporte

En el mismo side chat del lote. Primera línea
`TÍTULO: 📦 POD — Publicación · <fecha de hoy>` y luego por listing:
slug → estado (publicado/verificado/fallido con causa) + URL de Etsy.
El agente principal lo resume al dueño en el chat donde aprobó.

## Anti-patrones

- Publicar sin manifiesto explícito ("publica todo lo pendiente").
- Regenerar videos existentes.
- Correr el lote en el chat principal.
- Un worker por listing (diez briefs, diez reportes, diez sesiones de
  navegador contra la misma cuenta).
