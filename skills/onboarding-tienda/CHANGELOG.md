# CHANGELOG — onboarding-tienda

## v0.2.0 (2026-10-23) — Calibración visual de la tienda (Programa Estándar My POD, F3)
- **Nuevo bloque «Calibración visual de la tienda»:** la Fase 1 suma el descubrimiento visual (presupuesto de fotos ≤20, tablas de tallas, reparto, prioridad de cobertura, videos ≤2) y la Fase 4 suma la calibración por producto (catálogo de tomas elegido por el dueño DESDE las opciones reales de Printify, con muestras visuales; `tomas_a_evitar` con motivo). Son las 5 decisiones que el flujo de publicación consume: antes este paso NO existía y los valores se sembraban desde el historial sin pase del dueño (hueco detectado por el dueño el 2026-10-23).
- **Registro de estado obligatorio:** cada valor visual vive en la ficha (config + fichas de producto) con `estado`/`fecha`/`decidido_por` — `configurado` solo con el pase del dueño; `provisional` = solo piloto declarado; `sin_configurar` = el flujo consumidor se detiene y lo reporta.
- **Fase 6:** la tienda no se declara operativa con la calibración visual sin hacer — queda como hueco declarado con su paso y su dueño de cobro, nunca como silencio. Anti-patrón nuevo: sembrar la estrategia visual sin pase del dueño.

## v0.1.5 (2026-10-22)
- Fila del cron de propuestas diarias alineada al flujo vigente: la fila mezclaba en una frase «ensambla MPL» y «siembra en la vitrina», legible como propuestas → Printify → vitrina. Ahora declara las dos fases en orden (Fase B: solo aprobados de la vitrina, ruta MPL única base→conversión→items dentro; Fase A: artes nuevas a la vitrina, aprobación antes de producir).

## v0.1.4 (2026-10-21)
- Separación de registros D1 (migración a Rameli v0.17.0): el cierre de la Fase 6 commitea en el repo que toca — sistema en este repo y registros de la tienda nueva en el repo privado de datos (`my-pod-datos`) vía `scripts/registros-datos.py commit` — verificando ambos sin "ahead".

## v0.1.3 (2026-10-19)
- La estructura de tienda nueva nace con su operación dentro de `data/tiendas/<tienda-id>/` (dirección, config, registro, ledger, checkpoints, investigaciones/, revisiones/) — reorden 2026-10-19.

## v0.1.2 (2026-10-16)
- Referencia explícita al canon `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md`
  (API-first) en la fase de conexiones.

## v0.1.1 (2026-10-16)
- Fase 0 agregada: nicho → nombre → identidad visual (logo/banner) →
  creación de la tienda en Etsy → perfil y políticas → conexión
  Printify↔Etsy. El playbook ahora cubre de cero absoluto a tienda
  operativa (antes arrancaba con la tienda ya creada).

## v0.1.0 (2026-10-16)
- Skill nuevo: playbook portable de puesta en marcha de tienda POD de
  cero a operativa (descubrimiento → conexiones → activaciones Etsy →
  calibración de productos → crons con patrones de resiliencia →
  verificación). Destilado de la puesta en marcha real de
  MyNightShiftShop; incluye todo lo aprendido en el camino (Share &
  Save, calendario de descuentos en rampa, ofertas dirigidas, Star
  Seller) como activaciones estándar, no extras.
