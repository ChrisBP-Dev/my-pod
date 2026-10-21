# Changelog — puerta-arte-propuesta

## v0.7.0 (2026-10-20) — criterios de personalización con RAZÓN (estudio + corrección del dueño)
- **La sección de personalizables se reescribe con la razón gobernando:** ficha de razón obligatoria en la entrega (razón en una frase — identidad/relación/ocasión/conmemoración/pertenencia —, prueba de borrado en dos estados, campos ≤3 cerrados, comprador/destinatario/ocasión, clase de encaje, peor caso renderizado). Base: el estudio de criterios de personalización del 2026-10-20 y la corrección del dueño del mismo día (los 4 diseños del piloto, "diseño + franja con texto", quedaron parqueados como prueba de flujo por no tener razón).
- **Formato profesional real:** firma ANCC (grado → licencia → designación → certificación, con comas), vocabulario cerrado de títulos/unidades para los dropdowns, patrón de instrucción al comprador de los listings top.
- **Encaje con regla de oro:** si un humano debe tocar el dato o la imagen antes de imprimir, es manual (b); la ruta automatizada solo imprime tal cual lo del comprador. Texto libre sin razón = (c) no encaja por criterio.
- **RETIRADO el comodín "Maria / RN - ICU"** como ejemplo estándar de tienda (era un ejemplo casual del dueño, aplicado sin criterio): la simulación usa el ejemplo derivado del concepto con su formato real. La geometría de zonas se reordena por lógica de objeto (pecho = identidad, manga = persona, espalda = jersey) en vez de franjas genéricas.
- **Técnica sumada de la producción del piloto:** prompt con blancos sombreados (el blanco puro de diseño se lo come limpiar-fondo: gorro de PIL-02 v1) y orden de proceso (resize con alfa premultiplicado ANTES de las limpiezas; el Lanczos directo recrea la película). Regla del motivo íntegro (estetoscopio completo y conectado — corrección del dueño).

## v0.6.3 (2026-10-20) — personalización (llega sobre la v0.6.2 del barrido counters; numerada 0.6.3 para no colisionar)
- **Criterios de arte para diseños personalizables** (fase de personalización, Pasos 2+3): el diseño nace con su zona integrada y la forma sigue al diseño/mercado (caja de herramientas, no plantilla — corrección del dueño 2026-10-19); geometría medida desde los píxeles del arte final (caja del nombre ≈60–65% de la cara, una línea, margen en 4 lados; dato pegado 0.15–0.3"; contraste fuerte sobre la prenda más clara); marco de foto tipo passe-partout (relleno FIT verificado en vivo: la foto entra entera con su ratio y su fondo); bordado = texto corto bold con fuentes pre-digitalizadas; diseño personalizable siempre NUEVO y único (nunca copia de un MPL — duplicado penalizado); puerta visual con el ejemplo estándar Maria / RN - ICU antes de reportar un draft listo. La guía v1 de la prueba quedó clasificada contra estos criterios (donde conflictó, mandó el sistema; su "aprobación automática de respaldo" queda como NO verificada).
- **Entrega para aprobación con SIMULACIÓN** (pedido del dueño 2026-10-20, alineación del flujo v2): la entrega de un personalizable trae dos imágenes — el arte real (zonas vacías, el de producción) y la simulación del resultado esperado, compuesta determinísticamente sobre el arte real con el ejemplo estándar en las zonas medidas (nunca una generación paralela) — y su porqué declara producto destino + plan de zonas (dato, límites, dropdowns). Sin la simulación el dueño no puede juzgar un diseño cuyas zonas nacen vacías.

## v0.5.3 (2026-10-19)
- Fase de mejora v0.14.0: P1 — el diseño canónico de calibración de la suite vive ahora en `evals/fixtures/` (copia con origen y sha256 registrados en la suite; `K` ya no apunta fuera del repo). P2 — declaradas en el skill las herramientas compartidas `scripts/procesar-arte-propuesta.py` y `scripts/reparar-fondo-casi-blanco.py`.

## v0.5.2 (2026-10-19)
- El registro del diseño (`porque`) vive en `data/tiendas/<tienda-id>/registro-listings.json` (reorden de datos por tienda, 2026-10-19).
Skill de app. Pineado a Rameli v0.18.0.

## v0.5.1 — 2026-10-19 (flujo de propuestas v2, idea del dueño)
- Nueva sección "Entrega para aprobación del dueño": el PASS de
  la puerta se entrega por diseño en un chat nuevo, con el arte
  final y su porqué (tema/ángulo/frase/iconografía) + qué mirar
  (los pendientes del ojo humano que la puerta ya declaraba).
  Sin esa aprobación, el diseño no entra a producción: el dale
  creativo se mueve al punto más barato (antes se revisaba el
  arte recién en Printify, con los drafts ya creados). El porqué
  se guarda en el registro (`porque`) y lo hereda el paquete
  comercial. Sin cambios en los gates.

## v0.5.0 — 2026-10-18 (lote de drafts mutilados p038-p057, cazado por el dueño)
Contexto: 16 diseños llegaron CORTADOS a los drafts de Printify (palabras
rebanadas en los extremos, hojas y elementos incompletos) y ninguna
puerta lo vio — la puerta medía que no sobrara aire tras el recorte,
pero un diseño ya cortado "pasa" ese criterio. Causas medidas, no
supuestas (auditoría completa en data/registro-correccion-recortes-2026-10-19.json):
(a) lote A (p038-p045): el autotrim por bbox de MASA (0.05%) amputó los
extremos de baja masa de originales completos (7-53px por lado a escala
de generación); (b) lote B (p048-p057): un desbordamiento tipo fill
rebanó 0.4-3.7% por lado.
- Nuevo gate `composicion_completa` (`--es-original`, sobre el CRUDO
  antes de procesar): margen del bbox SEGURO por lado ≥ máx(6px, 0.4%).
  El bbox seguro = unión de componentes reales (área ≥150px,
  min(ancho,alto) ≥8px; filtra slivers/specks de borde).
- Nuevo gate `contenido_intacto` (finales): el bbox seguro no toca el
  borde del archivo (≥2px/lado).
- Nuevo gate `fidelidad_recorte` (`--original <crudo>`): desviación de
  aspecto del contenido ≤1.5% y pérdida en banda externa ≤2%/lado
  (rejilla 200×200 normalizada a bbox seguro). Si no se puede
  verificar, no pasa.
- FIX RAÍZ: `--autotrim` recorta al bbox SEGURO (antes: masa). La
  salida declara qué bbox usó (`autotrim_bbox`).
- Calibración con casos reales (no fixtures inventados): crudos del
  lote 16/16 PASS composición (mín. 0.86%/lado); prints mutilados
  16/16 FAIL composición (0px en los 4 lados) y 16/16 FAIL
  contenido_intacto; finales corregidos 16/16 PASS en todo, incluida
  fidelidad (pérdida 0.0, aspecto ≤0.5%). Fidelidad sola caza 10/16
  mutilados: las amputaciones finas/simétricas restantes no las
  separa ninguna métrica de píxeles a esa magnitud (el registro por
  template tiene piso de ruido ~0.5%/lado; medido y descartado como
  gate) — quedan cubiertas por contenido_intacto + el fix del
  mecanismo. La puerta nueva cazó además un defecto real en la
  primera reconstrucción corregida (p049 v1: pad inferior clampeado
  a 0) antes de subirla.
- Suite 8→13 casos: P3/F7 composición, P4/F8 fidelidad, F9 autotrim
  seguro (la barra fina de baja masa sobrevive: salida 1409px vs
  1384px con masa). 13/13 verde.

## v0.4.0 — 2026-10-17 (corrección del dueño revisando el lote de ayer)
- `recorte_ajustado` REPARADO: medía el margen MENOR de los 4 lados
  (min) — aire enorme en 3 lados pasaba si un lado estaba pegado. El
  canónico vitals trae máx 50px/lado (el "22px" citado era el mínimo).
  Ahora: bbox de contenido real (alfa≥128) y tope POR LADO
  máx(48px, 4% del lado). `--autotrim` usa el mismo bbox real.
- Nuevo gate `dpi_al_zoom` (flag `--exigir-margen-zoom`): el ancho del
  CONTENIDO debe rendir ≥300 DPI al ancho nominal ×1.20 — el dueño
  agranda la colocación al revisar y los artes de 3200px caían a
  250-260 DPI ("ya no lo puedo jugar").
- Procedimiento: paso 2b RECORTAR obligatorio (--autotrim) antes de la
  puerta final; antes el cron corría la puerta sin recortar nunca.
- Suite 5→8 casos: F5 aire asimétrico (caza el bug min), P2 zoom con
  margen, F6 vitals sin margen de zoom. Calibración verificada:
  conocido-bueno PASS / conocido-malo FAIL en cada criterio nuevo.
## v0.1.0 — 2026-10-13
- Creado desde la plantilla.

## v0.1.1 (2026-10-13)
- G2 dividido en `fondo_limpio` (esquinas alfa=0) y `recorte_ajustado`
  (margen ≤32px): el criterio del dueño es recorte exacto al arte, sin
  bordes vacíos — el gate anterior pedía margen mínimo, al revés.
- Nuevo `--autotrim`: recorta al bbox + 4px y re-verifica (verifier-repair).
- Suite 4/4: P1 + F1/F2/F3 (fondo, dpi, recorte).
