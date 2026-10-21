---
name: "publicador-lote"
description: "Publica un lote de diseños APROBADOS por el dueño: un side chat por lote, manifiesto explícito, pipeline por listing sobre publicar-printify-etsy (M3→M9), checkpoints con resume por listing y rollback."
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.1.6"
  framework_version: "0.16.0"
---

# Publicador de lote POD

**Versión 0.1.6** (2026-10-20: chequeo previo al corte en
## Invocación paso 0 — antes de resolver el manifiesto, el
agente principal lee la ficha de la tienda y su registro y
corta el manifiesto EN la puerta de aprobación del dueño:
solo MPLs unpublished revisados y aprobados; el remanente
nunca entra y se reporta aparte; el manifiesto declara su
corte — mecanismo de Rameli v0.15.0, cierra la brecha B1 de
la auditoría de adopción) · 0.1.5 (2026-10-20: la regla «no regenerar» protege
videos VÁLIDOS — un video que reprueba la puerta se regenera en
la fuente; manipularlo para pasar = trampa, ver M6 de
`publicar-printify-etsy` v0.8.2, incidente p046) · 0.1.4
(2026-10-20: checkpoint en dos tiempos por
listing — al INICIAR cada fase (con timestamp) y al completarla,
nunca en bloque al final de una fase larga; ver P2) · 0.1.3
(2026-10-19: watchdog obligatorio al lanzar el
lote — fase de mejora P4; 0.1.1: el flujo post-aprobación existía y
funcionaba, pero sin vehículo diseñado — corría donde el dueño
respondiera, sin checkpoints. Este skill lo formaliza: un side chat por
lote, manifiesto explícito, resume por listing).

## Principio

Publicar es la acción más delicada del sistema (dinero, listings
públicos). Por eso: **un lote = un side chat = un worker = un reporte**.
El chat arranca limpio (solo el manifiesto), el contexto del chat
principal no se toca, y el lote sobrevive a caídas a mitad de camino.

## Cuándo usarme

- Cuando el dueño aprobó un lote de diseños y hay que publicarlo:
  un lote aprobado = una invocación de este skill.
- NO para propuestas o drafts sin aprobación del dueño, ni para
  corregir un listing suelto ya publicado (eso va por vía directa
  sobre `publicar-printify-etsy`).

## Procedimiento

Resumen (el detalle está en ## Invocación y ## Pipeline por
listing): 1) el agente principal resuelve el manifiesto explícito
de aprobados; 2) crea el side chat del lote y pasa el manifiesto
al worker; 3) el worker ejecuta el pipeline por listing
(M3 → M9 de `publicar-printify-etsy`) con checkpoint por listing;
4) cierra con un solo reporte del lote en ese mismo chat.

## Invocación (la ejecuta el agente principal, no el worker)

0. **Corte en la puerta que la ficha declara (Rameli v0.15.0).**
   Antes de resolver el manifiesto, el agente principal lee la
   ficha de la tienda (`data/tiendas/<id>/config.json`) y su
   `registro-flujo.md`, y **corta el manifiesto EN la puerta de
   aprobación del dueño**: solo entra lo que el dueño revisó y
   aprobó como MPL unpublished — el criterio del dueño
   (2026-10-20): un producto suelto que nunca se volvió MPL NO
   fue revisado por él, NO está aprobado y ni siquiera lo
   conoce; es un remanente de un ensamblaje mal hecho, no
   parte de ninguna aprobación. Un remanente NUNCA entra en un
   lote aprobado: se reporta aparte, al cerrar, para que el
   dueño decida si se ensambla/corrige para su revisión. El
   manifiesto **declara su corte**: qué puerta lo corta (la
   aprobación registrada del dueño), qué quedó dentro y qué
   remanentes quedaron fuera.
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
- **P2 — Checkpoints:** `data/tiendas/<tienda-id>/estado-publicacion.json`
  (gitignoreado):
  `{"lote_actual": {"fecha": "YYYY-MM-DD", "manifiesto": [slugs],
  "fases_ok": {"slug": ["seo","mockups","video","publicado",
  "verificado"]}}, "videos": {"slug": "/ruta/video.mp4"}}`.
  Actualizar INMEDIATAMENTE tras cada fase. Si el worker muere, el
  siguiente retoma donde quedó — nunca repite fases hechas.
  **Checkpoint en dos tiempos (2026-10-20, incidente del lote
  Thanksgiving):** el checkpoint se escribe POR LISTING y en dos
  momentos — (1) al INICIAR una fase para un listing, registrando
  la fase en curso con su timestamp de inicio junto a `fases_ok`
  (p. ej. `"en_curso": {"slug": {"fase": "mockups", "desde":
  "<ISO>"}}`), y (2) al COMPLETARLA ese listing, sin esperar a
  que termine la fase para todo el lote. Una fase larga ejecutada
  en bloque (p. ej. navegador sobre 11 listings, ~75 min) sin
  ningún asiento intermedio es indistinguible de un freno: el
  watchdog disparó FRENO en falso el 2026-10-20 con el lote
  avanzando sano. Con el asiento de inicio, el watchdog calibra:
  fase en curso dentro de su ventana esperada = trabajo, no
  freno; freno = sin completadas nuevas Y sin fase en curso
  vigente (o en curso vencida).
- **P3 —** no aplica como reintento programado (el lote es a demanda);
  el escalado es el reporte al principal.
- **Watchdog (obligatorio desde 2026-10-19, fase de mejora P4):**
  al lanzar el lote, el agente principal monta una vigilancia
  programada que verifica el avance contra
  `data/tiendas/<tienda-id>/estado-publicacion.json` y le despierta si el lote se
  frena o falla en silencio (la notificación del worker no es
  confiable — doctrina en `docs/EJECUCION-Y-RELEVO.md`). El
  watchdog se retira al cerrar el lote. Un lote sin watchdog es
  un lote mal lanzado.

## Videos: paralelo y nunca regenerados

- Generar los videos del lote **en paralelo** (hasta 6 por tanda,
  regla del sistema).
- **REGLA DURA:** si `videos.<slug>` existe en disco y el archivo es
  válido → NO regenerar. El video es el paso caro del pipeline.
  **Alcance exacto:** «válido» = pasó la puerta. Un video que
  REPRUEBA `verificar-video.py` no está protegido por esta regla:
  se regenera en la fuente hasta pasar por mérito propio, y está
  PROHIBIDO reencuadrarlo/recortarlo para inflar la métrica
  (incidente p046, 2026-10-20; regla completa en M6 de
  `publicar-printify-etsy` v0.8.2).

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

## Calibraciones (mecanismo vs aplicación)

(Sección agregada 2026-10-19, Propuesta 4 de la auditoría de
adopción `docs/AUDITORIA-ADOPCION-V0110.md`.)

- `MECANISMO:` un lote = un worker = un manifiesto explícito del
  dueño; checkpoint por listing con resume; fallos aislados por
  listing (nunca bloquean el lote); watchdog obligatorio al
  lanzar y retirado al cerrar (calibración de la app en
  `docs/EJECUCION-Y-RELEVO.md`). Revalidar el watchdog si cambia
  el runtime de vigilancia.
- `CALIBRACIÓN:` el tamaño del lote y su composición los fija el
  manifiesto de cada lote (decisión del dueño por lote), no este
  skill; el pipeline por listing (M3→M9) y sus puertas son los
  de `publicar-printify-etsy` vigentes al lanzarse el lote.

## Regresión

Sin suite determinista propia — **declarado** (2026-10-19,
Propuesta 2 de la auditoría de adopción): el lote corre contra
sistemas externos vivos (Printify, Etsy, navegador) y su
verificación es el pipeline por listing con las puertas de
`publicar-printify-etsy` (que sí tienen suite) + el checkpoint
con resume + el watchdog. Un fallo real de un lote se convierte
en caso en la suite del skill cuya puerta debió atraparlo, no
en un fixture de este orquestador.
