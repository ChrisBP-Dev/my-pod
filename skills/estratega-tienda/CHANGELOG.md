# CHANGELOG — estratega-tienda

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
