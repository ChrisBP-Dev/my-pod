# CHANGELOG — estratega-tienda

## v0.6.1 (2026-10-21)
- Separación de registros D1 (migración a Rameli v0.17.0): el commit de cierre de la directriz y el config-propuestas se re-apunta al repo privado de datos (`my-pod-datos`) vía `scripts/registros-datos.py commit`; la regla «escribir = commitear» ahora nombra el repo que toca (registros → datos, sistema → este repo).

## v0.6.0 (2026-10-20)
- **Doctrina de personalizados por la RAZÓN** (estudio de criterios del 2026-10-20 + corrección del dueño): sección nueva — las 5 razones (identidad/relación/ocasión/conmemoración/pertenencia), los patrones que venden y encajan en la ruta automatizada (badge pecho/manga, credencial con dropdown, club+año, roster en un campo, foto en marco), lo que no se propone como automatizable (retrato, romanos, personaje abierto, texto libre sin razón), geometría por lógica de objeto y la ocasión mandando el calendario. Cada propuesta personalizada de la directriz nace con su ficha de razón; el detalle de puerta vive en puerta-arte-propuesta v0.7.0.

## v0.5.3 (2026-10-19)
- Fase de mejora v0.14.0, P2: declarada la herramienta compartida `scripts/reporte-seo.py` (cruce banco de keywords × ledger) como entrada de la dirección semanal.

## v0.5.2 (2026-10-19)
- La directriz y el config viven ahora en `data/tiendas/<tienda-id>/` (reorden de datos por tienda, decisión del dueño 2026-10-19) y la salida declara la regla de commit en la misma corrida.

## v0.5.1 (2026-10-16)
- **Share & Save:** la estratega ahora conoce el programa (4% devolución de comisión por link rastreable, 6.5% en intro; no entra en el presupuesto de descuento D; margen por canal usa 2.5% de transaction fee en órdenes atribuidas).
## v0.5.0 (2026-10-16)
- **Mecánica Etsy verificada:** los cupones NO se apilan con ofertas (un solo descuento por compra; Etsy aplica el mejor). Los cupones son herramienta de ventanas a precio pleno; el acoplamiento cupones↔precios pasa a planificarse como CALENDARIO secuencial, no como suma.
- **Flujo dueño (2026-10-16):** la estratega PROPONE el calendario de descuentos/cupones con números y márgenes por ventana; el dueño da el dale; Jarvis ejecuta y verifica.

## v0.4.0 (2026-10-16)
- **Portabilidad de la estrategia de precios** (corrección del dueño):
  el skill define el MECANISMO ("precio con colchón":
  P ≥ (C + 0.25 + M) / ((1−D)×0.905)) y el método de calibración
  (preguntas al dueño + recalibración semanal), NUNCA los valores.
  La estrategia de cada tienda vive en
  `data/tiendas/<id>/config.json → estrategia_precios`; la estratega
  la lee, y si no existe la calibra con el dueño antes de la primera
  directriz. Los números de la tienda 29222324 quedan como EJEMPLO
  marcado, no como regla.

## v0.3.0 (2026-10-16)
- Entrada #7: ledger de ventas como feedback loop (M2) — la estratega
  lee `data/ledger-ventas.json` en cada corrida.

## v0.2.0 (2026-10-15)
- **Config máquina de tipo de producto** (pedido del dueño): la estratega
  ahora también escribe `data/config-propuestas.json` (contrato
  `docs/CONTRATO-TIPO-PRODUCTO.md` v1.0) con `tipo_lote` (`mpl`/`single`/
  `mixto`), componentes del MPL o producto single, reparto mixto, temas,
  precios y vigencia. El cron de propuestas lee el JSON primero.
- **Decisión de tipo de lote** en el método (paso 2): dinámico por semana
  (ej. 100% MPL una semana, 5 MPL + 5 single la siguiente). Flujo
  bifurcado siempre: diseños personalizables → track single aunque el
  lote sea MPL. Cambiar la composición del MPL o agregar producto nuevo
  = PROPUESTA hasta el dale del dueño.

## v0.1.0 (2026-10-15)
- Versión inicial. Rol de estratega/administrador de la tienda POD, pedido
  del dueño: las propuestas diarias corrían por defecto (siempre sudadera,
  sin foco estacional) porque nadie convertía la investigación en
  dirección. La estratega lee research, trends, márgenes y estacionalidad,
  y emite `data/direccion-tienda.md` (vigencia 7 días) que el cron diario
  consume como orden de trabajo. Cambios de estrategia = PROPUESTA hasta
  el dale del dueño; lo operativo se aplica directo.
