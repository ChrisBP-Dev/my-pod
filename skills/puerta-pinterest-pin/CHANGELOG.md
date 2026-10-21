# Changelog — puerta-pinterest-pin

## v0.4.1 (2026-10-19)
- El registro se lee desde `data/tiendas/<tienda-id>/registro-listings.json`; `verificar-pin.py` resuelve la tienda por glob `data/tiendas/*/registro-listings.json` (reorden 2026-10-19). Copias del script byte-idénticas.
Skill de app. Pineado a Rameli v0.18.0.
## v0.4.0 — 2026-10-18
- **Causa (mandato del dueño):** 3 pins publicados con imagen que no coincidía con tipo/título (p028-3 y p030-3 "Close-Up" con modelo de playera; p032-5 "Folded" con tabla de tallas). La puerta vieja solo verificaba registro del asset, nunca su clase; la clase se infería por posición — inválido: el orden no es uniforme entre listings (p032: folded=-5, tabla=-10 · p034: folded=-10, tablas=-8/-9).
- **Mapa de assets:** nuevo campo `mapa_assets` (verificado visualmente, con fuente) en `data/registro-listings.json`; sin mapa, FAIL para pins de imagen. Mapas construidos el 2026-10-18 para p028–p034 desde hojas de contacto revisadas.
- **Checks nuevos en el gate:** `mapa_assets`, `clase_tipo` (declarada == mapa, compatible con tipo; `tabla-tallas` prohibida para todo tipo) y `claims` ("close-up"/"folded" deben ser verdad de la imagen).
- **Convergencia:** las dos copias de `verificar-pin.py` (app `scripts/` y skill) quedaron byte-idénticas — deuda de v0.3.1 cerrada; el script resuelve APP_ROOT buscando el registro, así el mismo archivo sirve en ambas rutas.
- **Calibración:** suite `evals/` reescrita: 15 casos — los 3 defectos reales como conocidos-malos (FAIL) y sus correcciones + el par contraejemplo p034 como conocidos-buenos (PASS). 15/15 verde.
- **Corrección en la misma corrida:** un pin publicado que no coincida con su clase se borra y republica en la misma corrida (criterio del dueño, precedente 2026-10-12), no queda como decisión pendiente.
- Tipo 3 sin close-up disponible: se usa front-flat como detalle del frente SIN afirmar "close-up" (los MPL de Thanksgiving no traen close-up).
- **Ejecución de la corrección (mismo día):** auditoría completa de pins de MPL — defectuosos reales: p028-3 (17-oct), p030-3 y p032-5 (18-oct); p034-5 CORRECTO (contraejemplo confirmado). Los 3 defectuosos fueron borrados y republicados por subida de archivo con asset correcto, título honesto y link rastreable, verificados en su página (p028 → pin 1142858842976635594 · p030 → 1142858842976635787 · p032 → 1142858842976635399). Lección adicional escrita en el skill: PROHIBIDO publicar vía "Save from URL" (link no editable, sin rastreable).
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
