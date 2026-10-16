# Estándar: API de Etsy vs navegador (canon 2026-10-16)

Documento canónico del enrutamiento operativo entre la API de Etsy v3 y
el navegador automatizado. Los skills consumidores
(`publicar-printify-etsy`, `estratega-tienda`, `conectar-etsy-api`)
**apuntan aquí**; no duplican estas reglas.

## Principio

**API-first.** Todo lo que el API cubre se hace por API (determinista,
rápido, verificable por máquina). El navegador es solo para lo que el
API no expone. Nunca se usa el navegador como atajo para algo que el
API cubre con los scopes otorgados; si falta un scope, se pide al dueño
(re-autorización OAuth) antes de recurrir al navegador.

## Tabla de enrutamiento

| Operación | Vía | Notas |
|---|---|---|
| Leer listings, inventario y precios por variación | API | `listings_r` |
| Actualizar precios / inventario por variación | API | `listings_w` → `updateListingInventory`. NUNCA edición manual en navegador |
| Editar título, descripción, tags, materiales | API | `listings_w` → `updateListing` |
| Subir / ordenar imágenes | API | `listings_w` |
| Crear borradores de listing | API | `listings_w` |
| Leer órdenes / recibos / transacciones | API | `transactions_r` (base del ledger de ventas) |
| Leer reviews y favoritos | API | `listings_r` / `shops_r` |
| Leer datos de la tienda | API | `shops_r` |
| Sales events / Sales and discounts | NAVEGADOR | El API no lo expone |
| Cupones y Targeted Offers | NAVEGADOR | El API no lo expone |
| Estadísticas de visitas / views / fuentes | NAVEGADOR | El API no lo expone (hueco documentado) |
| Mensajes con compradores | NAVEGADOR | El API no lo expone |

## Conexión por tienda

Ver skill `conectar-etsy-api` (flujo portable). Resumen:

- Cada tienda tiene su Seller App, sus tokens y su `shop_id`.
- Registro: `data/tiendas/<id>/config.json → etsy_api`
  (`shop_id`, `scopes`, `secrets_file`, `conectada_el`).
- Credenciales en `~/.config/my-pod/etsy-api-<shop>.json` (0600);
  nunca en repo, chat ni logs. Los scripts resuelven la ruta desde el
  config de la tienda.
- **Por qué no es un conector formal:** el API exige en cada llamada
  `x-api-key: keystring:shared_secret` ADEMÁS del bearer OAuth — doble
  secreto que el sistema de conectores no modela. Si lo soporta en el
  futuro, migrar.

## Reglas de uso

1. Antes de una operación de escritura por API, verificar el scope en
   el config de la tienda. Sin scope → pedir re-autorización al dueño,
   no improvisar por navegador.
2. Después de una escritura incierta, leer el estado actual antes de
   reintentar (la primera llamada pudo haber aplicado).
3. Los tokens rotan solos (`refresh_if_needed` en los scripts); si el
   refresh falla con 401, re-grant del dueño (skill `conectar-etsy-api`
   §2).
4. Este documento es el canon; los skills lo referencian, no lo copian.
