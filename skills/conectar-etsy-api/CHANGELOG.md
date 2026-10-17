# CHANGELOG — conectar-etsy-api

## v0.1.1 (2026-10-16)
- Refresh de tokens concretado: `scripts/etsy_auth.py` (`get_headers()` / `load_secrets()`) renueva el access token (~1h) automáticamente; todo script nuevo debe usarlo.

## v0.1.0 (2026-10-16)
- Skill nuevo: flujo portable de conexión Etsy API por tienda (Seller App → OAuth PKCE con clic del dueño → canje → gate → registro en config).
