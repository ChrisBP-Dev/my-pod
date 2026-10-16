# Contrato: tipo de producto de las propuestas (2026-10-15)

**Versión 1.0.** La estratega decide el TIPO de producto de cada lote de
propuestas; el cron de propuestas lo lee; el skill de publicación lo
ejecuta. Este documento define el formato y el contrato entre las tres
partes. Cambios al formato = bump de `version` + entrada en el CHANGELOG
de cada skill afectado.

## Partes y responsabilidades

| Parte | Escribe | Lee | No hace |
|---|---|---|---|
| `estratega-tienda` (cron semanal) | `data/config-propuestas.json` + `data/direccion-tienda.md` | research, márgenes, actas | No toca listings ni crea drafts |
| `equipo-pod-propuestas-diarias` (cron diario) | drafts en Printify según el config | `data/config-propuestas.json` (primero), `data/direccion-tienda.md` (fallback) | No redefine el tipo de producto; no publica |
| `publicar-printify-etsy` (skill) | listings publicados | `tipo` del registro + config vigente | No cambia la composición sin dale |

## Formato: `data/config-propuestas.json`

JSON (parseable por código, editable a mano). La estratega lo escribe
junto con `data/direccion-tienda.md` en cada corrida semanal.

```json
{
  "version": "1.0",
  "vigencia_desde": "2026-10-15",
  "vigencia_hasta": "2026-10-22",
  "n_propuestas_dia": 10,
  "tipo_lote": "mpl",
  "mpl": {
    "componentes": ["gildan-18000", "bella-canvas-3001"],
    "nombres_variacion": {
      "gildan-18000": "Sweatshirt",
      "bella-canvas-3001": "T-Shirt"
    }
  },
  "single": {
    "producto": "gildan-18000"
  },
  "mixto": {
    "reparto": { "mpl": 5, "single": 5 }
  },
  "flujo_bifurcado": true,
  "temas": [
    { "tema": "thanksgiving", "n": 10,
      "angulos": ["enfermería × thankful/grateful/blessed", "night shift", "ER", "ICU"] }
  ],
  "precios": {
    "gildan-18000":      { "base": 34.99, "2XL": 37.99, "3XL": 39.99 },
    "bella-canvas-3001": { "base": 24.99, "2XL": 27.99, "3XL": 30.99 }
  },
  "notas": "Override del dueño 2026-10-15: 15–18 oct = 10/día 100% Thanksgiving."
}
```

### Campos

- `version`: versión del formato. Lectores ignoran campos desconocidos;
  si falta un campo requerido, usan el default y lo reportan.
- `vigencia_desde` / `vigencia_hasta`: 7 días exactos. Vencido o ausente
  → el cron usa defaults y lo reporta (igual que con la directriz .md).
- `n_propuestas_dia`: N del día (default 10, orden del dueño 2026-10-15).
- `tipo_lote`: `"mpl"` | `"single"` | `"mixto"`. **Dinámico por semana:**
  la estratega puede poner 100% MPL una semana y 5 MPL + 5 single de
  ornamentos la siguiente, sin cambiar código.
- `mpl.componentes`: slugs de `data/productos/<slug>.json`, en orden
  (el primero es el producto base del MPL). Default de tienda:
  `["gildan-18000", "bella-canvas-3001"]`.
- `mpl.nombres_variacion`: nombre corto por componente para el campo
  "Variation name for Etsy listing". Default: Sweatshirt/T-Shirt.
- `single.producto`: slug del producto para lotes single.
- `mixto.reparto`: cuántas propuestas van por cada track (suma = N).
- `flujo_bifurcado`: siempre `true`. Aunque `tipo_lote` sea `"mpl"`,
  un diseño marcado como **personalizable** va por track single
  (el MPL nativo no soporta personalización — orden del dueño).
- `temas`: reparto de foco (tema, n, ángulos). Suma de `n` = N.
- `precios`: tabla por producto (base S–XL + recargos). La publica el
  agente con la fórmula del skill; la estratega solo fija la base.
- `notas`: overrides del dueño, supuestos, lo que invalida el config.

### Defaults (si el JSON falta o está vencido)

```
tipo_lote: "mpl"
mpl.componentes: ["gildan-18000", "bella-canvas-3001"]
n_propuestas_dia: 10
temas: [{tema: "enfermeria", n: 10}]
precios: tablas vigentes del skill publicar-printify-etsy
```
El cron reporta qué default usó.

## Detección de drafts en realidad MPL (tarea E, 2026-10-15)

El concepto "el único draft" ya no aplica. Estados reales:

- **Propuesta MPL** = 1 diseño × K drafts componentes (uno por producto
  de `mpl.componentes`), todos "unpublished", en la pestaña de drafts.
  El contenedor MPL vive en otra pestaña y se crea en la conversión
  (§M4 del skill) — NO antes.
- **Propuesta single** = 1 diseño × 1 draft.
- **Regla:** los componentes de un MPL **nunca** se publican por
  separado. Un draft componente publicado solo = error a corregir
  (revertir o completar el MPL).

El cron de propuestas, antes de crear drafts del día:
1. Lista los drafts "unpublished" en Printify (navegador).
2. Agrupa por diseño (título real del draft).
3. Si un diseño ya tiene sus K componentes como drafts pendientes →
   **no duplicar**; lo salta y lo reporta.
4. Si un diseño tiene componentes parciales (ej. solo sudadera) →
   crea solo los faltantes.
5. Límite de seguridad: si hay ≥ N×2 drafts pendientes sin revisar,
   no crea más y alerta al dueño (la cola está atorada).

## Versionado

- Cambios compatibles (campos nuevos opcionales): bump menor.
- Cambios incompatibles (campos requeridos nuevos, tipos que cambian):
  bump mayor + actualizar los tres lectores el mismo día.
- El CHANGELOG de `estratega-tienda` registra cada cambio de formato.
