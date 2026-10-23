# Contrato: tipo de producto de las propuestas (2026-10-15)

**Versión 1.0** (§E alineado el 2026-10-22 a la ruta MPL única y al
flujo vitrina: cambia la semántica de detección, no el formato). La
estratega decide el TIPO de producto de cada lote de
propuestas; el cron de propuestas lo lee; el skill de publicación lo
ejecuta. Este documento define el formato y el contrato entre las tres
partes. Cambios al formato = bump de `version` + entrada en el CHANGELOG
de cada skill afectado.

## Partes y responsabilidades

| Parte | Escribe | Lee | No hace |
|---|---|---|---|
| `estratega-tienda` (cron semanal) | `data/tiendas/29222324/config-propuestas.json` + `data/tiendas/29222324/direccion-tienda.md` | research, márgenes, actas | No toca listings ni crea drafts |
| `equipo-pod-propuestas-diarias` (cron diario) | drafts en Printify según el config | `data/tiendas/29222324/config-propuestas.json` (primero), `data/tiendas/29222324/direccion-tienda.md` (fallback) | No redefine el tipo de producto; no publica |
| `publicar-printify-etsy` (skill) | listings publicados | `tipo` del registro + config vigente | No cambia la composición sin dale |

## Formato: `data/tiendas/29222324/config-propuestas.json`

JSON (parseable por código, editable a mano). La estratega lo escribe
junto con `data/tiendas/29222324/direccion-tienda.md` en cada corrida semanal.

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
- El **esquema de mockups/videos** de cada composición vive en
  `data/tiendas/<id>/config.json` (`mpl.esquema_mockups`,
  `mpl.esquema_videos`) — no en este contrato ni quemado en el skill.
  Si la estratega propone una composición nueva, propone su esquema
  junto con ella (PROPUESTA hasta el dale del dueño).
- `single.producto`: slug del producto para lotes single.
- `mixto.reparto`: cuántas propuestas van por cada track (suma = N).
- `flujo_bifurcado`: siempre `true`. Aunque `tipo_lote` sea `"mpl"`,
  un diseño marcado como **personalizable** va por track single
  (el MPL nativo no soporta personalización — orden del dueño).
- `personalizados` (opcional, 2026-10-20): bloque de la tienda para el
  flujo de personalizados — `estado` (piloto/en flujo/pausado),
  `cupo_en_flujo_diario` (cuántas de las N propuestas del día pueden
  ser personalizadas; cuentan dentro del reparto single) y, durante
  un piloto, su tabla de listings con precios verificados y regla de
  retiro. Los diseños personalizables son siempre **nuevos y únicos**
  (nunca un diseño que vive en un MPL) y se producen por la ruta
  automatizada (`publicar-printify-etsy` §Track Single-P) con los
  criterios de `puerta-arte-propuesta`. Sin este bloque: no se
  proponen personalizados.
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

## Detección de borradores en realidad MPL (tarea E, 2026-10-15; alineada 2026-10-22)

Estados reales (la aprobación creativa vive en la vitrina, etapa 1
del pipeline; **nada de lo que hay en Printify es una propuesta** —
todo borrador en Printify es PRODUCCIÓN de un diseño ya aprobado):

- **Producción MPL** = 1 diseño × **1 borrador MPL** "unpublished":
  el borrador del producto base (el primero de `mpl.componentes`)
  convertido a MPL, con los demás productos CREADOS dentro del MPL
  desde el catálogo con el mismo diseño (ruta única, skill
  `publicar-printify-etsy` §M1 → §M4; Printify no crea un MPL vacío
  desde cero). El borrador MPL vive en la pestaña de
  Multi-Product Listings, pendiente de la revisión de UBICACIÓN.
- **Producción single** = 1 diseño × 1 borrador.
- **Producción single personalizable** = 1 diseño NUEVO único × 1
  borrador con los campos de personalización montados en Printify
  (producto nuevo; nombres/instrucciones/límites según §Track
  Single-P). No se detecta como MPL ni como single común: el
  borrador declara su personalización en el detalle del producto
  (conteo de campos).
- **Componente suelto de un diseño MPL** = remanente de la ruta
  vieja (anterior a la alineación del 2026-10-22) o error: nunca es
  el estado normal. Se rescata UNA vez (se agrega al MPL del diseño
  y se anota en su registro) o se elimina con reporte al dueño.
- **Regla:** los componentes de un MPL **nunca** se publican por
  separado. Un componente publicado solo = error a corregir
  (revertir o completar el MPL).

La Fase B, antes de producir los aprobados del día:
1. Lista los borradores "unpublished" en Printify y los MPL drafts
   (navegador + sync del registro).
2. Agrupa por diseño (título real del borrador).
3. Si un diseño ya tiene su borrador MPL producido y pendiente →
   **no duplicar**; lo salta y lo reporta.
4. Si un diseño tiene SOLO el borrador base sin convertir → se
   convierte y se crean los items dentro (§M4), en su unidad.
5. Si un diseño tiene componentes sueltos sin MPL (remanente) →
   rescate anotado en el registro (§M4, excepción), nunca crear
   duplicados.
6. Límite de seguridad: si hay ≥ N×2 borradores MPL/single
   pendientes de revisión de ubicación, no produce más y alerta
   al dueño (la cola está atorada).

## Versionado

- Cambios compatibles (campos nuevos opcionales): bump menor.
- Cambios incompatibles (campos requeridos nuevos, tipos que cambian):
  bump mayor + actualizar los tres lectores el mismo día.
- El CHANGELOG de `estratega-tienda` registra cada cambio de formato.
