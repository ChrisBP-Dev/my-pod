# CHANGELOG — onboarding-tienda

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
