# CHANGELOG — publicar-printify-etsy

## v0.11.0 (2026-10-23) — colores sin techo + mockups y videos con estándar (propuesta aprobada por el dueño)
- **Colores sin techo:** el «tope máximo 4 por prenda» de v0.10.0 queda eliminado como techo. 3–4 por prenda es la **guía de producción** (juicio del arte); la extensión a **5–6** está permitida sin bloqueo con la nota operativa ampliada (por qué más colores); el dueño en §M2 agrega/quita colores **sin límite del sistema**. Se borra el techo del §Selección de colores, del procedimiento (paso 4), de §M1, de §M8, del `CHECKLIST-PUBLICACION.md` y de `FLUJO-PIPELINE.md`.
- **Puerta de conteo reescrita** (`scripts/verificar-variantes.py`): detiene SOLO por límite técnico del MPL (>400 variantes totales o >70 opciones del conjunto, exit 2); informa el conteo por item y **avisa sin detener** si un item pasa de 6 colores (exit 0). El caso de regresión viejo «5 colores = AVISO/detener» se elimina.
- **Catálogo canónico de tomas por producto:** nueva sección `tomas_preferidas` + `tomas_a_evitar` en `data/productos/gildan-18000.json` y `data/productos/bella-canvas-3001.json`, sembrada solo con evidencia del historial (etiquetas de cámara y clases documentadas; lo sin evidencia va declarado como provisional). Producto nuevo sin catálogo = M5 se detiene y reporta.
- **§M5 = algoritmo determinista + manifiesto:** la lista fija de 10 espacios se retira del skill, del checklist y del config de tienda; el config pasa a **pesos por composición** (principal 5 espacios visuales / secundario 3 / 1 tabla de tallas por producto / total 10). El worker genera el manifiesto con `scripts/generar-manifiesto-mockups.py` (modo fixture) desde los colores finales post-M2 y lo verifica con la puerta nueva `scripts/verificar-mockups.py`; sin PASS no hay publicación. El dueño **nunca** elige mockups; los defaults de Printify no son una selección válida. La regla «todos los colores representados» (imposible: playera 3 espacios < 4 colores) se reemplaza por garantías mínimas + colores sin representación **declarados** en el manifiesto.
- **§M6 = escenarios A–D:** los videos se arman solo con tomas del manifiesto (A: MPL de 2 productos; B: producto con 1–2 colores cubiertos; C: single; D: composición futura según su peso y su catálogo). El formato técnico de video (1080×1080, 30 fps, 9.5 s, zoom de posición absoluta sin temblor, yuv420p rango limitado obligatorio) pasa a vivir en §M6 y `CRITERIO-VIDEO.md` (raíz) se **elimina** como fuente duplicada que contradecía al esquema (su estructura «Video 2 = flat/folded/zoom del color hero» queda retirada).
- **Consumidores alineados:** `publicador-lote` delega M5/M6 contra el manifiesto + puerta; `puerta-pinterest-pin` consume el manifiesto de mockups como fuente del mapa de assets. Piloto seco con datos reales de p058 en `docs/PILOTO-MOCKUPS-2026-10-23.md`.

## v0.10.0 (2026-10-23) — selección de colores del diseño (corrección del dueño)
- **Sin paleta canónica:** «paleta» como lista fija queda retirada del glosario. La **selección de colores** se elige por diseño al producir (contraste con el arte ya colocado + disponibilidad), **tope 4 por prenda**, y vive solo en el borrador. El trío de playera y el de sudadera bajan de regla fija a **preferencia frecuente / referencia de partida**.
- **§M1/§M4:** dejar solo los colores elegidos al crear cada item es parte de crearlo, con la advertencia de lectura por API (contar solo variantes `is_enabled`; el GET lista también las deshabilitadas — error de la primera pasada de la auditoría del 2026-10-23). **Procedimiento de elección por item** (corrección del dueño, 2026-10-23): mirar los tonos del arte colocado → candidatas por contraste → **verificación visual sobre cada candidata** → elegir 3–4 → nota de producción de una línea (operativa, no canónica). El trío histórico queda nombrado como **hábito prohibido sin juicio** (Fase B: 9/10 con el mismo trío por inercia; el único distinto, p058, lo cambió el dueño a mano; caso de prueba p059: letras crema ilegibles sobre White/Sand, el arte pide oscuros).
- **§M2 = ubicación + colores:** el dueño filtra y puede cambiar los colores en su revisión; su «listos» aprueba ambos, y eso **no se guarda como canónico** — §M3 y §M8 leen los colores del borrador tal como él lo dejó.
- **Puerta mecánica de conteo** nueva: `scripts/verificar-variantes.py` (colores por item y variantes totales ≤400; avisa al dueño y se detiene, sin comparar contra lista alguna).
- Alineados: `CHECKLIST-PUBLICACION.md`, `FLUJO-PIPELINE.md` (etapas 2/3/6) y `paquete-listing-etsy` (colores del paquete leídos del borrador por API).

## v0.9.1 (2026-10-23) — lecciones de producción de la Fase B del lote 2026-10-19
- §M4 suma las lecciones verificadas al producir los 10 MPLs aprobados: prohibición de producción en paralelo en la misma cuenta (cruce p059/p062); el item de catálogo nace con Printful y "Replace print provider" regenera el ID y rompe la referencia del MPL (cierre fiable: re-agregar vía "Your products", patrón de rescate anotado); la validación del MPL exige nombres de producto distintos (playera = título + " - T-Shirt", solo interno); el diálogo "Your products" puede no listar productos recién creados (esperar y reintentar, no duplicar); un componente puede aparecer "Published" sin clic de publicación (p064: Hide on Etsy inmediato + verificación por API de Etsy + incidente en el registro, decisión de fondo del dueño).

## v0.9.0 (2026-10-22) — alineación de producción MPL (orden del dueño)
- **Ruta MPL ÚNICA:** §M1 crea SOLO el borrador base (primer producto de la composición); §M4 lo convierte y los demás items se CREAN dentro del MPL desde el catálogo con el mismo diseño. Printify no crea MPL vacíos desde cero: la conversión del base es la entrada. La ruta vieja (crear todos los componentes como borradores y ensamblar los existentes) queda degradada a **excepción de rescate** para componentes ya creados por lotes anteriores, con anotación en el registro.
- **Orden de ejecución declarado:** M1 → M4 → M2 → M3 → M5… (la conversión ocurre en la producción/Fase B, no en la publicación).
- **Aprobación creativa fuera de Printify:** §M1/§M2 reescritos — nada llega a Printify como propuesta; la aprobación creativa vive en la vitrina (Fase A) y la revisión del dueño en Printify es solo de UBICACIÓN, por item dentro del editor del MPL. Eliminada la variante de revisión por borrador componente suelto y todo el lenguaje «draft = propuesta» (también en el track single).
- Alineados en la misma pasada: `FLUJO-PIPELINE.md` (etapas 2/3/7 + colocación recalibrada), `docs/CONTRATO-TIPO-PRODUCTO.md` §E, `CHECKLIST-PUBLICACION.md` y el cuerpo del cron de propuestas (B3).

## v0.8.2 (2026-10-20)
- M7 idempotencia de publicación — verificar antes de reintentar; el clic de Publish es acción con costo. M6 corrección en la fuente — prohibido manipular un video reprobado para pasar la puerta. Incidentes p052 y p046. (Entrada registrada retroactivamente en v0.9.0: la versión vivía en el encabezado del skill sin entrada en este changelog.)

## v0.8.1 (2026-10-20)
- §Track Single-P: puntero al vocabulario cerrado y al formato profesional (firma ANCC) que ahora viven en puerta-arte-propuesta v0.7.0; el diseño personalizado llega con su ficha de razón y sus campos definidos (≤3 del comprador por criterio; 5 sigue siendo el tope técnico).

## v0.8.0 (2026-10-20)
- **Ruta AUTOMATIZADA de personalización (§Track Single-P)** — cierra el hueco señalado por el dueño el 2026-10-17 (el skill solo contemplaba caja nativa de Etsy + fulfillment manual; la personalización nativa de Printify nunca entró). Procedimiento P1–P7 verificado en vivo en el sandbox de la tienda: campos montados en Printify (producto y diseño NUEVOS; duplicar un diseño del MPL = duplicado penalizado), congelados con la aprobación, jamás editados desde Etsy; la API no expone la configuración de personalización (corrección = editor). Comportamiento verificado: texto escala a la caja; imagen FIT entera con su ratio (sin ajuste del comprador; HEIC = excepción manual); Live Preview en DTG sí, en bordado NO; máx. 5 campos. Órdenes: llegan aplicadas con "Review needed" y se aprueban (la aprobación automática de respaldo queda registrada como NO verificada). Bordado: fuentes pre-digitalizadas, digitalización gratis ≤36 h, handling ~10 días. La ruta manual queda como excepción consciente para el esquema multi-producto manual (P7). Protocolo sandbox para pruebas con Etsy (precio disuasorio, ventana de minutos, desactivar y verificar).

## v0.7.3 (2026-10-19)
- El registro de listings y la directriz viven ahora en `data/tiendas/29222324/` (reorden de datos por tienda, 2026-10-19); punteros actualizados en el skill y el checklist.

## v0.7.1 (2026-10-16)
- **Propuestas como MPL drafts (orden del dueño, causa raíz 2026-10-16):** M2 calibrado — las propuestas diarias llegan ensambladas como MPL draft (un draft por diseño); la revisión del dueño verifica placement por item dentro del editor del MPL. El cron de propuestas ahora incluye el ensamblaje (M1+M4 antes de la revisión).
## v0.7.0 (2026-10-16)
- **Estándar API de Etsy vs navegador** (punto del dueño): sección nueva que apunta al canon `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` (API-first; navegador solo para ofertas/cupones, stats de visitas, mensajes).
- **Tablas de precios**: ya no hardcodeadas; se leen de `estrategia_precios` del config de tienda (ejemplo 29222324 actualizado a doctrina precio con colchón).
- Paso de checklist: listings nuevos se agregan a eventos de ofertas vigentes (`eventos_ofertas` del config).

## v0.6.1 (2026-10-15)
- **Organización a nivel tienda** (punto del dueño): el esquema de
  mockups (`mpl.esquema_mockups`) y de videos (`mpl.esquema_videos`) se
  movió a `data/tiendas/29222324/config.json`. El skill lee el esquema
  vigente; si la estratega define otra composición, define su esquema
  en el config sin reescribir el skill. Nueva sección "Calibraciones
  (mecanismo vs instancia vs tienda)".

## v0.6.0 (2026-10-15)
- **Flujo MPL nativo** (decisión del dueño): track MPL para diseños NO
  personalizables — composición estándar Gildan 18000 + Bella+Canvas 3001
  (Printify Choice), conversión "Convert to Multi-Product Listing" en
  Printify, nombres de variación "Sweatshirt"/"T-Shirt".
- **Flujo bifurcado por personalización** (orden del dueño): diseño
  personalizable → track single-product SIEMPRE (el MPL nativo no soporta
  personalización, verificado en help.printify.com). Cambiar de track
  exige re-optimización SEO completa + mockups/videos nuevos.
- **Esquema de mockups MPL: 10 imágenes** (APROBADO por el dueño):
  2 lifestyles sudadera + 2 flat sudadera + 1 folded decorado + 2 on-model
  playera + 1 flat playera + 2 tablas de tallas. Reglas: nunca repetir
  pose/modelo, todos los colores vendidos representados, hero = lifestyle.
- **Esquema de videos MPL:** Video 1 = 3 lifestyles sudadera, Video 2 =
  3 tomas playera (1080×1080, 9.5s, sin audio).
- **SEO MPL:** título con ambos productos, descripción con sección
  "CHOOSE YOUR STYLE", 13 tags ≤20 car.
- **Precios playera:** S–XL $24.99, 2XL $27.99, 3XL $30.99 (fórmula ×1.15).
- **Placement en CADA producto del MPL** + revisión del dueño (lección
  p005: el placement heredado no pasó puerta numérica).
- **Criterio color-diseño** (regla suya): colores validados contra el
  diseño, sin abarcar sin verificación visual.
- **Regla:** componentes de un MPL no se publican single por separado.
- **Fase C:** verificación exhaustiva en Etsy tras publicar el MPL
  (variaciones, precios, SKUs, orden de imágenes, videos intactos,
  materiales, atributos, políticas, envío, personalización ausente,
  cantidades, visibilidad de variantes).
- Notas MPL verificadas 2026-10-15: título/desc/tags/mockups se gestionan
  en el MPL (pricing en cada single), un shipping profile compartido,
  límites 20 productos/400 variantes/70 opciones, push selectivo por
  categorías, revert a single disponible.

## v0.5.0 (2026-10-15)
- **Estándar de precios escalonados por talla** (orden del dueño): el precio
  nunca es plano; recargo = redondeo((costo_talla − costo_SXL) × 1.15).
  Calibración Gildan 18000: S–XL $34.99, 2XL $37.99 (+$3), 3XL $39.99 (+$5).
  Aplica en Printify antes de publicar y se verifica por variación en Etsy.
  El precio base S–XL lo define la directriz de la estratega
  (`data/direccion-tienda.md`).
- Checklist: "Precio final verificado" ahora exige cada variación con su
  precio correcto en el listing vivo.

## v0.4.0 (2026-10-14)
- **Endurecimiento:** checklist completa de publicación (CHECKLIST-PUBLICACION.md).
  Ningún listing se declara publicado hasta verificar título, descripción,
  13 tags, hero correcto, videos en Etsy, categoría, atributos, production
  partner, envío y políticas. Lección: p002 se publicó incompleto (sin tags,
  sin videos, hero incorrecto) por no tener esta validación.
- Puerta `verificar-listos-publicar.py` actualizada a Printify-first
  (ya no busca mockups propios eliminados; exige 2 videos Printify-first).

## v0.3.0 (2026-10-14)
- **Probado en producción:** p002 publicado exitosamente con este flujo.
- Selección estándar de mockups documentada: Flat + Folded 2 decorado + Lifestyle 1/2/3 (1 por color, sin repetir modelo). Hero = lifestyle (preferencia 2/3, luego 1 o Folded decorado).
- El color del hero depende del diseño (no siempre blanco).
- Eliminados remanentes del flujo anterior (scripts de mockups propios, bases, flatlays, zooms generados).

## v0.2.0 (2026-10-14)
- **Cambio mayor:** flujo Printify-first. Ya no se generan mockups propios
  ni se traduce colocación. El draft se crea en Printify, el dueño revisa
  ahí, los mockups salen de Printify.
- Procedimiento simplificado de 7 a 8 pasos (agrega Pinterest).
- La puerta de colocación ahora es revisión del dueño en Printify,
  no comparación contra mockups propios.

## v0.1.0 (2026-10-14)
- Versión inicial: flujo con mockups propios y validación de colocación
  por comparación. Reemplazado por v0.2.0.
