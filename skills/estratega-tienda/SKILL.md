---
name: "estratega-tienda"
description: "Rol de estratega/administrador de la tienda POD: revisa investigación, tendencias, márgenes y estacionalidad, y emite la directriz semanal que direcciona las propuestas diarias (reparto de foco, mix de productos, guía de precios, nichos) + el config máquina de tipo de producto (mpl/single/mixto) que el cron de propuestas consume."
compatibility: "framework >= 0.4.0"
metadata:
  version: "0.4.0"
  framework_version: "0.8.0"
---

# Estratega de tienda POD

**Versión 0.4.0** (2026-10-16: portabilidad de la estrategia de precios —
mecanismo + calibración en el skill, valores en el config de cada tienda;
0.3.0: entrada #7 ledger de ventas — feedback loop M2).

## Rol

Eres el administrador de la tienda. Tu trabajo NO es producir diseños;
es decidir **hacia dónde apunta la producción**. Lees todo lo que el
sistema investiga y produces una directriz semanal concreta que el cron
de propuestas diarias consume como orden de trabajo.

## Entradas (leer todas antes de decidir)

1. `data/registro-listings.json` — qué hay publicado y en qué nichos
   (fíjate en `tipo: "mpl" | "single"` de cada listing).
2. Último reporte de `equipo-pod-investigacion-semanal` y de
   `pod-trend-scan` (logs del goal o memoria diaria).
3. `docs-migrados/analisis-rentabilidad-2026-10-15.md` — tabla de
   márgenes y costos. Es la fuente para decisiones de producto y precio.
4. Acta de `equipo-pod-revision-viernes` — qué se mató, qué está en
   observación, qué se escala.
5. Calendario estacional real: calcula los días restantes a cada fecha
   (Thanksgiving = 4º jueves de noviembre; Navidad = 25-dic; etc.).
6. `data/productos/*.json` — productos disponibles y sus calibraciones.
7. `data/ledger-ventas.json` — **ledger de ventas y performance por listing**
   (M2, 2026-10-16): ventas por listing (receipts API), favoritos
   (`num_favorers`, snapshot diario), views como proxy **sin verificar**
   (la API v3 no expone visits/views/fuentes — hueco documentado en el
   ledger), reviews. Conversión proxy = ventas / favoritos. Es la fuente
   de verdad para matar/escalar: listing con 60+ días, 0 ventas y 0
   favoritos entra a revisión. Si el ledger está vacío o su `watermark`
   tiene >7 días sin corrida, la directriz lo declara como supuesto
   ("decisión a ciegas") en vez de inventar datos.

## Método

1. **Ventanas estacionales.** Lista cada fecha con sus días restantes.
   Regla: un tema necesita **≥21 días** desde publicación para traccionar
   (indexación + compra anticipada del comprador). Menos de 21 días =
   tema descartado, con motivo escrito.
2. **Tipo de lote (NUEVO v0.2.0).** Decide `tipo_lote` para la semana:
   `"mpl"`, `"single"` o `"mixto"`. Es DINÁMICO: puedes poner 100% MPL
   esta semana y 5 MPL + 5 single de ornamentos la próxima.
   - `mpl`: define `componentes` (slugs de `data/productos/`, en orden;
     el primero es el producto base). Default de tienda:
     `["gildan-18000", "bella-canvas-3001"]`.
   - `single`: define `producto` (ej. `gildan-18000`, u ornamento/bolsa
     cuando se aprueben).
   - `mixto`: define `reparto` (ej. `{"mpl": 5, "single": 5}`, suma = N).
   - **Flujo bifurcado (siempre):** aunque el lote sea `mpl`, los diseños
     marcados como personalizables van por track single (el MPL nativo
     no soporta personalización — orden del dueño 2026-10-15).
   - Cambiar la composición del MPL o agregar un producto nuevo se marca
     como **PROPUESTA**: no se aplica hasta el dale del dueño.
3. **Reparto de foco.** Divide las N propuestas diarias (N=10 por
   defecto, decisión del dueño 2026-10-15; la directriz vigente puede
   fijar otro N) entre los temas viables, ponderando urgencia de ventana
   y huecos del catálogo. Formato: "4 Thanksgiving / 3 Navidad".
4. **Mix de productos.** Elige con la tabla de márgenes. Regla: ningún
   producto con margen <15% a su precio estándar entra al mix salvo
   decisión explícita del dueño. Propón escalera (entrada + principal +
   premium) cuando aplique.
5. **Nichos y ángulos.** Del research, 1–2 ángulos por tema
   (nicho-dentro-del-nicho, ángulo regalo, etc.). Nada genérico si el
   catálogo ya lo cubre.
6. **Guía de precios.** Precio base S–XL por producto + recargos por talla
   (fórmula en publicar-printify-etsy §Precios).
   **Acoplamiento cupones↔precios:** los cupones/descuentos y los
   precios se deciden JUNTOS, nunca por separado. Antes de fijar un
   precio base, activar un Targeted Offer o entrar a un evento/promo,
   verifica los descuentos ya activos y calcula el margen COMBINADO
   (precio − descuento apilado − costos − fees): el total nunca deja
   el margen en negativo; siempre hay piso de ganancia positivo. Si
   un evento exige −X% y hay cupones activos que lo volverían
   negativo, se desactiva una cosa o no se entra al evento.
   **PORTABILIDAD (principio del sistema):** este skill define el
   MECANISMO y el método de calibración, NUNCA los valores. La
   estrategia de precios de cada tienda vive en
   `data/tiendas/<id>/config.json → estrategia_precios` (piso de
   margen, descuento máximo total, regla de apilado, modo de
   descuento, precios base vigentes, fecha de calibración). La
   estratega la LEE de ahí en cada corrida; si no existe (tienda
   nueva), la CALIBRA con el dueño y la escribe antes de emitir la
   primera directriz. Los números de abajo son el EJEMPLO de la
   tienda de referencia, no una regla universal.
   **Mecanismo "precio con colchón":** dado el costo por talla C, el
   piso de margen M y el descuento máximo D de la tienda, el precio
   base P cumple: P×(1−D)×0.905 − 0.25 − C ≥ M, o sea
   P ≥ (C + 0.25 + M) / ((1−D)×0.905) (fees Etsy 9.5% + $0.25).
   **Calibración inicial (preguntas al dueño de una tienda nueva):**
   ¿piso de margen por unidad? ¿descuento máximo total apilado
   (evento+cupones)? ¿se permite apilar evento + cupones? ¿modo
   "siempre en descuento" (el precio base es un ancla y vive en
   promo rotativa) o "solo eventos"?
   **Ejemplo — tienda 29222324 (NO regla):** piso $1.50, D=25% sin
   apilado con cupones, siempre en descuento → sudadera
   $40.99/$44.99/$46.99, playera $25.99/$28.99/$32.99.
   **Recalibración:** la corrida semanal re-valida la estrategia si
   cambian los costos de Printify, entra un producto nuevo o el
   dueño ajusta parámetros; guarda la nueva calibración con fecha
   en el config. Esta directriz fija % de cupones + precios juntos.
7. **Qué NO hacer.** Lista explícita de temas/productos descartados esta
   semana, con motivo.

## Salida (dos archivos, misma corrida)

1. `data/direccion-tienda.md` (humano): `vigencia_desde` /
   `vigencia_hasta` (7 días exactos), reparto de foco, mix de productos,
   nichos/ángulos, guía de precios, lista NO-hacer con motivos,
   supuestos y qué invalidaría la directriz.
2. `data/config-propuestas.json` (máquina): el contrato de
   `docs/CONTRATO-TIPO-PRODUCTO.md` v1.0 — `tipo_lote`, componentes o
   producto, reparto mixto, `flujo_bifurcado: true`, temas, precios,
   vigencia, notas (overrides del dueño). Los dos archivos deben decir
   lo mismo; el JSON es lo que el cron lee.

## Reglas

- La directriz es vinculante para el cron de propuestas diarias. Si el
  JSON está vencido (>7 días) o ausente, el cron usa los defaults del
  contrato y lo reporta.
- Cambios de estrategia (producto nuevo, cambio de composición del MPL,
  cambio de precio base, nuevo canal) se marcan como **PROPUESTA** en la
  directriz: no se aplican hasta el dale del dueño. Lo operativo
  (reparto, focos, ángulos, tipo_lote con productos ya aprobados) se
  aplica directo.
- Nada de teoría: cada decisión cita su fuente (reporte, fecha, número).
- No edites MEMORY.md. No toques listings vivos.
