# Evaluación de catálogo Printify — 2026-10-16

**Tienda:** MyNightShiftShop (Printify 29222324) · **Nichos:** enfermería, Thanksgiving, Navidad
**Método:** solo lectura vía API Printify (personal access token verificado OK).
**Fuente:** `printify blueprints` / `print-providers` / `variants` / `shipping` en vivo.

## ⚠️ Hallazgo de datos (importante)

**El costo base por variante NO está expuesto por la API en modo solo-lectura.**
El endpoint de catálogo `variants` devuelve opciones, placeholders (área de impresión) y
métodos de decoración, pero no el `cost`. El costo solo aparece en productos ya creados
(`products`). El escape hatch `printify request` está roto (404, ya documentado en TOOLS.md).
Crear un draft para ver costos está prohibido por la restricción de esta tarea.

**Lo que SÍ se obtuvo (dato duro API):** provider, variantes (colores/tallas), envío US,
área de impresión, handling time. La fórmula de precio se deja aplicada en forma de
**umbral de viabilidad** (ver § Fórmula).

## Fórmula (doctrina tienda 29222324 — solo mecanismo)

- `C = costo_base + costo_envío`
- `P = (C + 0.25 + 1.50) / (0.75 × 0.905)`, redondeado a .99
- `margen(D) = P×(1−D)×0.905 − 0.25 − C`
- Propiedad útil: con P fijado por la fórmula, **M25 = $1.50 siempre** (por construcción);
  `M20 = 0.0667×C + 1.62`, `M15 = 0.1333×C + 1.73`.
- **Umbral de viabilidad:** dado un precio de referencia de mercado `P_ref`,
  el costo base máximo admisible es `base_max = P_ref×0.67875 − 1.75 − envío`.
  Si el costo base real (a verificar con draft) ≤ base_max, el producto es viable
  con piso $1.50 al 25%.

## Tabla comparativa

| Producto | Blueprint / Provider | Envío US | Variantes | Área impresión (front) | base_max @ P_ref | Encaje estacional | Recomendación |
|---|---|---|---|---|---|---|---|
| Hoodie Gildan 18500 | bp 77 / Choice 99 | $7.39 | 36 colores × 8 tallas (S–5XL) | 2919×1944 px DTG | **$21.40** @ $44.99 | Alto (otoño/invierno, los 3 nichos) | **APROBAR p/ verificación de costo** → MPL existente o single |
| Manga larga Bella+Canvas 3501 | bp 41 / Choice 99 | $3.99 | 13 colores × 6 tallas (XS–2XL) | 3185×3636 px DTG | **$14.62** @ $29.99 | Alto (capas otoño/invierno) | **APROBAR p/ verificación de costo** → MPL existente o single |
| Tote canvas 5-Color Straps | bp 507 / Choice 99 | $6.09 | 5 colores × 3 tamaños | 2102×4051 px dye-sub | **$7.09** @ $21.99 | Alto (nurse diario, regalo) | **APROBAR p/ verificación de costo** → single (no es apparel, no entra al MPL) |
| Mug cerámica 11/15oz | bp 478 / Choice 99 | $5.79 / $7.09 | 2 tamaños | 2475×1155 px dye-sub | **$3.99** @ $16.99 · **$6.08** @ $19.99 | Medio (regalo Navidad/nurse) | **CONDICIONAL** → single; margen estrecho, verificar costo |
| Ornamento cerámica 4 formas | bp 531 / Choice 99 | $5.89 | 4 formas (Star/Circle/Heart/Snowflake) | ~954–1043 px dye-sub | **$2.53** @ $14.99 · **$5.93** @ $19.99 | Solo Navidad (ventana corta) | **CONDICIONAL/RIESGOSO** → single; margen muy estrecho + handling 10 días vs reloj navideño |

Notas:
- `P_ref` = banda de referencia típica de Etsy (estimación, NO dato API). El umbral se
  recalcula con el precio que fije la estratega.
- Handling time: **10 días en los 5** (Printify Choice). Para Navidad (ornamento/mug),
  10 días de producción + tránsito = riesgo real de no llegar; el ornamento solo tiene
  sentido si se lanza esta misma semana.
- Tote 507: envío $6.09 supera el umbral de $6 que Etsy prioriza en visibilidad
  (página Search Visibility). A considerar en precio (absorber envío) o aceptar.
- Hoodie: tallas 4XL/5XL existen pero la tabla de precios de la tienda solo llega a 3XL;
  habría que extender la tabla (regla de escalonado) o no habilitarlas.
- Tote/mug/ornamento NO son apparel → no entran al MPL de sudadera+playera; van como
  listings single-product.

## Descartados (con motivo)

- **Tote 609 (Organic Canvas)**: solo 3 colores × 1 tamaño vs 5×3 del 507. Menos juego.
- **Ornamento 537**: único provider Duplium (sin Printify Choice). Se prefiere Choice.
- **Hoodie 458 (B&C)**: único provider Textildruck Europa (UE) — envío US inviable.
- **Hoodie 175 (Bella+Canvas 3719)**: tiene Choice, pero Gildan 18500 gana por
  consistencia de marca con el 18000 (misma línea Heavy Blend, historia de fit/calidad
  ya validada en la tienda).
- **Kids/Toddler hoodies, Wine Tote, Pewter Snowflake**: fuera de nicho o sin Choice.

## Márgenes en el umbral de viabilidad (C = C_max, por construcción M25 = $1.50)

| Producto | C (= base_max+envío) | M15 | M20 | M25 |
|---|---|---|---|---|
| Hoodie @ $44.99 | $28.79 | $5.57 | $3.54 | $1.50 |
| Manga larga @ $29.99 | $18.61 | $4.21 | $2.86 | $1.50 |
| Tote @ $21.99 | $13.18 | $3.49 | $2.50 | $1.50 |
| Mug @ $19.99 | $11.87 | $3.31 | $2.41 | $1.50 |
| Ornamento @ $19.99 | $11.82 | $3.31 | $2.41 | $1.50 |

(Si el costo base real resulta MENOR que base_max, los márgenes suben en la misma
proporción; la fórmula se recalcula con el costo real.)

## Siguiente paso requerido

Obtener **costos base reales** de los 5 candidatos. Vía honesta: crear 1 draft por
producto (requiere dale del dueño — esta tarea lo tenía prohibido) o revisar el
catálogo web de Printify con la sesión del dueño. Con el costo real se aplica la
fórmula tal cual y se fija el P definitivo.
