# Changelog — puerta-pinterest-pin
Skill de app. Pineado a Rameli v0.8.0.
## v0.3.1 — 2026-10-16
- **Share & Save (orden del dueño):** `url_listing` ahora exige el link rastreable (`<tienda>.etsy.com/...`) cuando la tienda está inscrita; el formato clásico sigue aceptado como fallback. El gate de producción valida contra la `url` del registro, así que basta con actualizar el registro. Caso de regresión P2 agregado.
- Deuda visible: la copia del gate en `skills/.../scripts/` y `scripts/verificar-pin.py` (el que usa el cron, con más checks) deben converger a una sola implementación.
## v0.3.0 — 2026-10-16
- Gate real `scripts/verificar-pin.py` (antes solo papel); videos 1:1 sin recortar (decisión del dueño).
## v0.2.0 — 2026-10-14
- Procedimiento de publicación por navegador documentado.
- Criterio validado con el dueño: 3 pins por listing (hero lifestyle + lifestyle alternativo + detalle folded).
- Boards temáticos por nicho/ocasión, no por producto.
- Prioridad de imágenes: lifestyle > folded decorado > flat (flat blanco excluido).
- Estrategia respaldada por investigación (múltiples pins por producto, link directo para POD).

## v0.1.0 — 2026-10-13
- Creado desde la plantilla.
- Puertas en código (`scripts/verificar-pin.py`): asset_final (trazabilidad
  por registro — caso 2026-10-12), url_listing, keywords_banco con fuente,
  tablero. Suite `evals/test-regression.sh`: 6/6 verde.
