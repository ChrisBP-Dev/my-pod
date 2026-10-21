# Changelog — estratega-pinterest

## v0.1.3 (2026-10-20)
- Regla de cierre con commit: la corrida que registra pins
  commitea en la misma corrida (la del 2026-10-20 dejó el
  registro y 5 pin.json sin commitear; ni el skill ni el cron
  lo exigían). Convención escrita de `pin_ultimo` (URL del pin
  más reciente).

## v0.1.2 (2026-10-19)
- Insumos reubicados a la carpeta de la tienda: `data/tiendas/<tienda-id>/registro-listings.json`, `direccion-tienda.md` y `ledger-ventas.json` (reorden 2026-10-19).
Skill de app. Pineado a Rameli v0.15.0.

## v0.1.1 — 2026-10-18
- Elegibilidad por CLASE de asset del `mapa_assets` verificado del
  listing (nunca por posición del archivo) al armar la parrilla.

## v0.1.0 — 2026-10-16
- Versión inicial: parrilla de Pinterest de la tienda — 5 pins/día,
  videos 1:1 sin recortar, 3–5 pins por listing (hero, alternativo,
  detalle, video), keywords del banco de Pinterest.
