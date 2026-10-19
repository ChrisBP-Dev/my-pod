---
name: "onboarding-tienda"
description: "Playbook de puesta en marcha de una tienda POD nueva, de cero a operativa: descubrimiento con el dueño, conexiones (Etsy API, Printify), config de tienda, activaciones de Etsy (Share & Save, calendario de descuentos, cupones), calibración de productos y creación de los crons operativos con patrones de resiliencia. El mecanismo es portable; los valores son calibración por tienda."
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.1.2"
  framework_version: "0.11.0"
---

# Onboarding de tienda POD

**Versión 0.1.2** (2026-10-16: destilado de la puesta en marcha real de
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

## Pre-requisitos

- Cuentas del dueño: Printify (con tienda creada) y Etsy (con tienda
  creada). Anotar el **Printify shop ID** (numérico, p. ej. 29222324)
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

## Fase 5 — Crons operativos

Crear el set estándar de crons (ajustar horarios/N por tienda):

| Cron | Ritmo | Hace |
|---|---|---|
| propuestas diarias | diario, hora de revisión −X | P1→P2→P3; genera N propuestas según `tipo_lote`; ensambla MPL si aplica; reporte en chat nuevo |
| pinterest diario | diario | pins según mix; gate `puerta-pinterest-pin`; URLs rastreables Share & Save |
| estratega semanal | semanal | `estratega-tienda`: `data/direccion-tienda.md` (vigencia 7 días) |
| revisión viernes | semanal | paquetes SEO vs ledger |
| trends | semanal | señales de nicho para la estratega |
| watchdog | según criticidad | vigila trabajos largos delegados |

Cada cron lleva en su body: **P1** (health-check antes de trabajar),
**P2** (checkpoints con resume en `data/estado-<cron>.json`,
gitignoreado), **P3** (reintentos acotados: 1 reintento en ~2h, tope
3/día, luego escala al dueño). El body del cron ES el procedimiento;
el reintento lo relee, no lo duplica.

## Fase 6 — Verificación y cierre

1. Correr cada gate/eval afectado en verde (`evals/`).
2. Primera corrida de propuestas supervisada: el dueño revisa los
   drafts en Printify.
3. Commit + push de todo lo portable (skills, docs, scripts, config
   **sin secretos**). Verificar `git status` limpio y `origin/main`
   idéntico.
4. Estado de ejecución (checkpoints, tokens, colas) → gitignoreado,
   nunca commiteado.

## Anti-patrones de onboarding

- Dejar activaciones "para después" (Share & Save, ofertas dirigidas).
- Quemar valores de la tienda en skills o scripts.
- Crons sin P1/P2/P3: el primer fallo externo los deja tirados.
- Asumir endpoints o costos sin verificarlos en vivo.
