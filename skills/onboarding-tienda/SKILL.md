---
name: "onboarding-tienda"
description: "Puesta en marcha de una tienda POD nueva, de cero a operativa: descubrimiento, conexiones (Etsy API, Printify), activaciones de Etsy, calibración de productos y crons operativos con patrones de resiliencia."
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.2.0"
  framework_version: "0.19.0"
---

# Onboarding de tienda POD

**Versión 0.2.0** (2026-10-16: destilado de la puesta en marcha real de
MyNightShiftShop — todo lo aprendido en el camino, convertido en
procedimiento reproducible).

## Principio

Una tienda nueva debe poder recorrer este playbook de inicio a fin y
quedar **operativa sin huecos**: cada flujo que la tienda va a usar
(propuestas, Pinterest, precios, ofertas, Share & Save) queda montado,
calibrado y verificado. Nada de "eso lo configuramos después".

El skill enseña el **mecanismo** (qué preguntar, qué crear, en qué
orden, cómo verificar). Los **valores** (precios, horarios, productos,
nichos) son calibración del dueño y viven en
`data/tiendas/<shop_id>/config.json` — nunca quemados aquí.

Los patrones de resiliencia que aplican los crons están en
`docs/PATRONES-RESILIENCIA.md` (P1 health-check, P2 checkpoints, P3
reintentos acotados).

## Cuándo usarme

- Para poner en marcha una tienda nueva desde cero, o una tienda
  existente que nunca recorrió este playbook completo.
- NO para la operación diaria de una tienda ya operativa: eso vive
  en los crons y skills que este onboarding deja montados.

## Procedimiento

Recorrer las fases en orden, sin saltarse ninguna: Fase 0 (nicho,
identidad y creación de la tienda) → Fase 1 (descubrimiento) →
Fase 2 (conexiones) → Fase 3 (activaciones de Etsy) → Fase 4
(calibración de productos) → Fase 5 (crons operativos con los
patrones P1/P2/P3) → Fase 6 (verificación y cierre). La tienda se
declara operativa solo cuando la Fase 6 verifica el conjunto.

## Pre-requisitos

- Cuentas del dueño: Printify (con tienda creada) y Etsy (con tienda
  creada). Anotar el **Printify shop ID** (numérico)
  — es el `<shop_id>` de `data/tiendas/<shop_id>/`.
- El dueño disponible para: crear la Seller App (1 clic), pegar el
  código OAuth, y responder el cuestionario de descubrimiento.

## Fase 0 — Nicho, identidad y creación de la tienda (2026-10-16)

Todo lo anterior a "la tienda existe". Una pregunta al dueño a la vez.

**0.1 Selección de nicho.** Con el dueño: revisar `docs-migrados/nichos/`
(plantilla `_plantilla.md` + nichos evaluados). Criterios: demanda
evergreen o estacional con calendario claro, competencia atacable,
margen viable con la doctrina de precios de la Fase 1. El nicho elegido
se registra en el config (`nicho`, `subnichos`, `temporadas`).

**0.2 Nombre de la tienda.** Con el dueño: corto, memorable, con la
palabra del nicho si ayuda al SEO de Etsy. Verificar disponibilidad en
Etsy antes de enamorarse del nombre.

**0.3 Identidad visual.** Generar con el dueño: logo (versión clara y
oscura, legible a 64px), banner de tienda (dimensiones vigentes de
Etsy — verificarlas, cambian), foto de perfil. Guardar finales en
`data/tiendas/<shop_id>/branding/`. Nada de versiones previas junto a
la final aprobada.

**0.4 Creación de la tienda en Etsy.** Guiar al dueño en la creación
(Etsy la crea él, no el agente). Luego configurar el perfil: about,
políticas de la tienda (ver `docs-migrados/estandar-politicas-etsy.md`),
banner, foto, idiomas/moneda, ubicación.

**0.5 Conexión Printify ↔ Etsy.** Conectar la tienda Printify como canal
de ventas de la tienda Etsy (desde Printify, con el dueño). Anotar el
Printify shop ID → es el `<shop_id>` de `data/tiendas/<shop_id>/`.

Sin la Fase 0 completa no se avanza: una tienda sin nicho ni identidad
es la que después hay que re-marcar.

## Fase 1 — Descubrimiento

No se avanza a la Fase 2 sin estas respuestas. Una pregunta a la vez;
el dueño no responde dos cosas al mismo tiempo.

1. **Doctrina de precios:** ¿precio con colchón? (fijar precio base
   para que con −D% el margen ≥ piso) ¿piso de ganancia en $? ¿descuento
   máximo D%? ¿modo "siempre en descuento" o precio pleno con eventos?
2. **Propuestas:** ¿N diseños/día? ¿hora de revisión matutina?
   ¿tipo de lote: `mpl` (multi-producto), `single` o `mixto`?
   ¿productos por defecto? ¿temas/nichos y reparto?
3. **Pinterest:** ¿cuenta conectada? ¿tableros? ¿pins/día y mix por
   listing (hero/alternativo/detalle/video)?
4. **Ofertas:** ¿calendario de descuentos en rampa? (piso/rotación/
   eventos). ¿cupones? (decidir % junto con precios — presupuesto total
   de descuento ≤ D%).
5. **Metas:** ¿Star Seller como meta? ¿horizonte?
6. **Descubrimiento visual (inicio de la Calibración visual de la
   tienda, §Fase 4):** ¿cuántas fotos por tipo de listing?
   (presupuesto, con techo de plataforma 20 en Etsy) ¿las tablas
   de tallas ocupan foto, van combinadas en una, o no van?
   ¿reparto de espacios por composición y producto principal de
   cada composición que la tienda opere? ¿qué se muestra primero
   cuando colores × productos no alcanzan en el presupuesto?
   ¿cuántos videos por listing y con qué lógica (techo Etsy: 2)?
   La estratega aporta la evidencia (qué convierte, qué hace la
   competencia del nicho); el dueño decide. Estas respuestas se
   completan con la calibración por producto de la Fase 4 y
   juntas forman la **Calibración visual de la tienda**.

Registrar todo en `data/tiendas/<shop_id>/config.json`
(`estrategia_precios`, `calendario_descuentos`, `pinterest`, etc.).

## Fase 2 — Conexiones

1. **Etsy API:** ejecutar el skill `conectar-etsy-api` (v0.1.1):
   Seller App → OAuth PKCE (el dueño pega el code) → canje → gate →
   registro en `config.json → etsy_api`. Scopes: lectura + `listings_w`
   (necesario para precios por API).
2. **Printify:** verificar acceso a la tienda (shop ID) por navegador o
   CLI. Calibrar y anotar el **endpoint sano** para el health-check de
   los crons (P1): debe devolver el código esperado *verificado*, nunca
   supuesto.

Credenciales: `~/.config/my-pod/` (0600), nunca en el repo ni en el
chat.

**Estándar API-first** (canon: `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md`):
todo lo que el API de Etsy cubre se hace por API; el navegador solo
para lo que el API no expone. Los skills lo referencian; este playbook
no duplica sus reglas.

## Fase 3 — Activaciones de Etsy (lo aprendido en el camino)

Todo esto es parte estándar de lo que una tienda debe gestionar; no es
"extra":

1. **Share & Save:** inscribir en Shop Manager → Marketing → Share &
   Save. Anotar `%` de devolución y vigencia en
   `config.json → share_save`; generar los links rastreables por
   listing (`https://<subdominio>.etsy.com/listing/<id>`) y
   registrarlos (los pines futuros los exigen por gate).
2. **Calendario de descuentos:** crear las ofertas en rampa según la
   Fase 1 (reglas Etsy: ≤30 días por oferta, no solapar eventos, un
   descuento por compra — cupones no apilan con ofertas).
3. **Cupones:** solo si el dueño dio el %; viven en ventanas a precio
   pleno.
4. **Ofertas dirigidas:** activar emails automáticos (carrito
   abandonado, favoritos, post-compra) — gratis, una sola configuración.
5. **Star Seller:** registrar la meta y el dashboard de seguimiento.

## Fase 4 — Calibración de productos

Por cada producto del mix: crear el draft, leer el **costo base real**
por variante (la API en solo-lectura no lo expone — se lee del draft),
verificar envío, y fijar la tabla de precios por talla en
`config.json → estrategia_precios.tabla_variaciones` con la fórmula del
skill `estratega-tienda` (v0.5.1). Sin costos reales no hay precios
definitivos. Guardar ficha en `data/productos/<slug>.json`.

### Calibración visual de la tienda (v0.2.0, 2026-10-23 — Programa
Estándar My POD, F3)

La tienda no solo calibra costos: calibra **cómo se ve** lo que
vende. Este bloque produce, con el dueño decidiendo y la
estratega aportando evidencia, TODOS los valores visuales que el
flujo de publicación consume — para que ningún mecanismo tenga
que sembrarlos desde el historial ni asumirlos en silencio.
**Una decisión a la vez**, en este orden:

1. **Presupuesto de fotos por listing** (descubrimiento visual,
   Fase 1): cuántas fotos usa esta tienda por tipo de listing,
   con techo de plataforma **20** (Etsy, desde ago-2025), y si
   las tablas de tallas ocupan foto, van combinadas en una o
   no van. → `config.json → mpl.esquema_mockups`
   (`total_imagenes`, `tabla_tallas_por_producto`).
2. **Reparto por composición:** por cada composición que la
   tienda opere, los espacios visuales por producto y cuál es
   el producto principal. → `mpl.esquema_mockups.pesos`.
3. **Catálogo por producto:** por cada producto del mix, el
   dueño elige sus tomas preferidas **desde las opciones
   reales que Printify ofrece para ese producto**, presentadas
   con muestras visuales reales (no una lista de nombres):
   orden de preferencia para principal, secundarias, planas y
   detalle; las descartadas quedan en `tomas_a_evitar` con su
   motivo. → `data/productos/<slug>.json → tomas_preferidas`
   (+ `tomas_a_evitar`).
4. **Prioridad de cobertura:** qué se muestra primero cuando
   colores × productos no alcanzan en el presupuesto (la regla
   general la pone el mecanismo de `publicar-printify-etsy`
   §M5; el orden fino lo declara la tienda). →
   `mpl.esquema_mockups` (reglas de la composición).
5. **Escenarios de video de la tienda:** cuántos videos por
   listing y con qué lógica, dentro de los 2 que permite
   Etsy. → `mpl.esquema_videos`.

**Registro de estado (obligatorio):** cada valor visual queda
en su ficha con `estado`, `fecha` y `decidido_por`:
- `configurado` — decidido por el dueño en este flujo.
- `provisional` — sembrado con otra procedencia (historial,
  propuesta) SIN pase del dueño: usable SOLO como piloto
  declarado (ver la puerta de completitud de
  `publicar-printify-etsy` §M5), nunca como operación normal.
- `sin_configurar` — aún no se decidió: el flujo que lo
  consume se detiene y lo reporta (no lo inventa).

Sin pase del dueño no hay `configurado`: lo que una tienda
decide no se hereda a otra — cada tienda recorre su propia
calibración visual (multitienda de verdad). Producto o
composición nueva = recorrer este bloque para lo nuevo antes
de producirlo.

## Fase 5 — Crons operativos

Crear el set estándar de crons (ajustar horarios/N por tienda):

| Cron | Ritmo | Hace |
|---|---|---|
| propuestas diarias | diario, hora de revisión −X | P1→P2→P3; dos fases en orden: **Fase B** produce SOLO los diseños ya aprobados en la vitrina (track MPL: borrador base → conversión → items creados dentro del MPL, ruta única de `publicar-printify-etsy` §M1/§M4); **Fase A** genera las N artes nuevas según `tipo_lote`, les corre la puerta y **las entrega a la vitrina en vivo de la tienda (previas a su hogar en el repo de datos + entregados en el estado + commit del puente, según `puerta-arte-propuesta` §«Entrega»; la vitrina lee el repo, no se siembra) + aviso breve en chat nuevo (sin artes: la aprobación creativa es en la vitrina, ANTES de producir — nada llega a Printify como propuesta)** |
| pinterest diario | diario | pins según mix; gate `puerta-pinterest-pin`; URLs rastreables Share & Save |
| estratega semanal | semanal | `estratega-tienda`: `data/tiendas/<tienda-id>/direccion-tienda.md` (vigencia 7 días) |
| revisión viernes | semanal | paquetes SEO vs ledger |
| trends | semanal | señales de nicho para la estratega |
| watchdog | según criticidad | vigila trabajos largos delegados |

Cada cron lleva en su body: **P1** (health-check antes de trabajar),
**P2** (checkpoints con resume en `data/tiendas/<tienda-id>/estado-<cron>.json`,
gitignoreado), **P3** (reintentos acotados: 1 reintento en ~2h, tope
3/día, luego escala al dueño). El body del cron ES el procedimiento;
el reintento lo relee, no lo duplica.

## Fase 6 — Verificación y cierre

0. **Calibración visual verificada:** correr la puerta de
   completitud (`publicar-printify-etsy/scripts/verificar-ficha-visual.py`)
   sobre el config y las fichas de producto del mix. Una tienda
   **no se declara operativa con la calibración visual sin
   hacer**: si queda pendiente, queda registrada como **hueco
   declarado** — qué decisión falta, en qué paso de este
   onboarding se llena (Fase 1 descubrimiento visual / Fase 4
   calibración por producto) y quién la cobra — nunca como
   silencio. Con valores `provisional`, la tienda opera solo
   en modo piloto declarado hasta el pase del dueño.
1. Correr cada gate/eval afectado en verde (`evals/`).
2. Primera corrida de propuestas supervisada: el dueño revisa los
   drafts en Printify.
3. Commit + push en el repo que toca (separación D1, 2026-10-21):
   lo portable (skills, docs, scripts) en el repo del sistema, y
   los registros de la tienda nueva (config **sin secretos**,
   directriz, registro, ledger) en el repo privado de datos de la
   instancia (`my-pod-datos`), con
   `python3 scripts/registros-datos.py commit -m "<mensaje>"`.
   Verificar **ambos** repos sin "ahead" y `origin/main` idéntico
   en cada uno.
4. Estado de ejecución (checkpoints, tokens, colas) → gitignoreado,
   nunca commiteado.

## Anti-patrones de onboarding

- Dejar activaciones "para después" (Share & Save, ofertas dirigidas).
- Quemar valores de la tienda en skills o scripts.
- Sembrar la estrategia visual desde el historial o desde otra
  tienda sin el pase del dueño: queda `provisional` y solo sirve
  como piloto declarado (Fase 4, Calibración visual).
- Crons sin P1/P2/P3: el primer fallo externo los deja tirados.
- Asumir endpoints o costos sin verificarlos en vivo.

## Calibraciones (mecanismo vs aplicación)

(Sección agregada 2026-10-19, Propuesta 4 de la auditoría de
adopción `docs/AUDITORIA-ADOPCION-V0110.md`.)

- `MECANISMO:` el recorrido por fases (0→6) con dale del dueño
  entre fases, las conexiones por API-first, las activaciones de
  Etsy con sus reglas (ofertas ≤30 días, sin solapar eventos) y
  dejar los crons naciendo con los patrones de resiliencia
  (health-check, checkpoint, reintentos acotados) — igual para
  cualquier tienda nueva.
- `CALIBRACIÓN:` horarios, N diario de propuestas, pins/día y mix
  son valores de CADA tienda: se fijan en su onboarding y viven en
  su config y en los cuerpos de sus crons (la tabla de la Fase 5
  trae valores de una tienda de ejemplo, no defaults
  universales). Revalidar al abrir la segunda tienda: lo que solo
  se ha probado con una tienda es calibración, no mecanismo.

## Regresión

Sin suite determinista en `evals/` — **declarado** (2026-10-19,
Propuesta 2 de la auditoría de adopción): es un playbook guiado
por fases con el dueño; su "suite" es la Fase 6 (verificación y
cierre contra la tienda real) y el hecho de que cada artefacto
que deja montado (crons con patrones, conexión API, config)
hereda las suites y puertas de su propio skill. Al abrir la
segunda tienda, los fallos que aparezcan se convierten en casos
aquí o en el skill que corresponda, en la misma sesión.
