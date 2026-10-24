# Inventario de valores de ficha — qué consume el mecanismo y en qué estado está

**Fecha:** 2026-10-23 · **Programa Estándar My POD, frente F5.**
**Qué es:** la lista completa de valores que viven en la ficha
(config de tienda + fichas de producto + artefactos de la tienda)
y que algún skill/script del sistema CONSUME para operar. Cada
valor declara: dónde vive, quién lo consume, su **estado hoy en
la tienda 29222324** (verificado contra el config y las fichas
el 2026-10-23, no supuesto) y **qué paso de
`onboarding-tienda` lo produce** — o **SIN PASO** si ningún paso
lo produce (esos son huecos a la vista: el valor existe, pero
ningún flujo lo crea con el dueño).

Estados: `configurado` = decidido por el dueño en su flujo ·
`provisional` = sembrado sin su pase, usable solo como piloto
declarado · `sin configurar` = no decidido / pendiente.

> Nota de disciplina: el registro formal `estado/fecha/
> decidido_por` por valor hoy solo está completo para la
> estrategia visual (F3, onboarding v0.2.0). El resto de los
> valores trae la trazabilidad parcial (fechas de calibración,
> notas) o no la trae. Este inventario es la foto honesta; la
> extensión del registro de estado a todos los valores queda
> como trabajo posterior declarado aquí, no como silencio.

---

## 1. Identidad y conexiones

| Valor | Dónde vive | Lo consume | Estado hoy | Paso que lo produce |
|---|---|---|---|---|
| Nicho + subnicho | config → `nicho` | estratega, puerta-arte, propuestas | **configurado** (declarado 2026-10-23 desde la evidencia de la propia tienda) | Fase 0.1 |
| Referencia de formato profesional del nicho | config → `nicho.referencia_formato_profesional` → `investigaciones/formato-profesional-enfermeria.md` | `puerta-arte-propuesta` (personalizables) | **configurado** (movida a datos en F4; su contenido nació de la investigación de personalización 2026-10-20) | **SIN PASO** en onboarding (nace de la investigación del nicho; el onboarding solo declara el puntero desde F4) |
| Conexión Etsy API (shop, scopes) | config → `etsy_api` (secretos fuera del repo) | conectar-etsy-api, publicar, estratega | **configurado** (conectada 2026-10-16) | Fase 2 |
| Printify shop id | config → `printify_store_id` / `tienda_id` | todas las puertas y flujos | **configurado** | Fase 0.5 / Pre-requisitos |
| Instancia de la vitrina | config → `vitrina.artefacto` | puerta-arte-propuesta (recogida) | **configurado** | **SIN PASO** explícito en onboarding (la vitrina se canonizó después; su alta no está en las fases) — hueco menor |
| Mensajería (nombre, firma, tono, idioma) | config → `mensajeria` | mensajería con compradores | **configurado** | **SIN PASO** explícito en onboarding — hueco menor |

## 2. Precios y ofertas

| Valor | Dónde vive | Lo consume | Estado hoy | Paso que lo produce |
|---|---|---|---|---|
| Doctrina de precios (colchón, piso, D máx, apilado, modo) | config → `estrategia_precios` | publicar (fórmula), estratega | **configurado** (última calibración registrada en el propio bloque) | Fase 1.1 |
| Precio base S–XL por producto + tabla de variaciones | config → `estrategia_precios.precio_base_s_xl` / `tabla_variaciones`; costos en fichas de producto | publicar, paquete | **configurado** | Fase 4 |
| Calendario de descuentos | config → `calendario_descuentos` | estratega, ofertas | **configurado** (las entradas vigentes son de corridas pasadas: el calendario se renueva por corrida de ofertas, no es hueco de ficha) | Fase 1.4 + Fase 3 |
| Cupones (% junto a precios) | config → `estrategia_precios` (presupuesto de descuento) | estratega | **configurado** como doctrina; el % concreto por cupón se decide por corrida | Fase 1.4 + Fase 3 |
| Share & Save (inscripción, % devolución, links) | config → `share_save` | puerta-pinterest-pin (links rastreables), publicar | **configurado** (inscrito) | Fase 3 |

## 3. Propuestas y contenido

| Valor | Dónde vive | Lo consume | Estado hoy | Paso que lo produce |
|---|---|---|---|---|
| Tipo de lote, N propuestas/día, temas y reparto | `config-propuestas.json` (salida de la estratega, vigencia 7 días) | cron de propuestas, puerta-arte | **configurado** (vigencia 2026-10-19 → 2026-10-26; el cron de propuestas está pausado por decisión del dueño — estado operativo, no de ficha) | Fase 1.2 (preguntas) + estratega semanal (emisión) |
| Banco de keywords del nicho | `data/banco-keywords/<nicho>.md` | paquete-listing-etsy, estratega (reporte SEO) | **configurado** (de operación) | **SIN PASO** en onboarding (nace de la investigación del nicho) |
| Productos aprobados del mix | config → `productos_aprobados` | publicar, onboarding | **configurado** | Fase 0/Fase 4 |
| Fichas de producto (costos, precios, placement, `detalle_listing`) | `data/productos/<slug>.json` | publicar, paquete (`--producto`), puertas | **configurado** (`detalle_listing` agregado en F4 para los 2 productos del mix) | Fase 4 |
| Personalización (si la tienda la opera) | config → `personalizacion.estado` | publicar (track Single-P), puerta-arte | **sin configurar** — `pendiente_investigacion`, declarado (decisión diferida a la vista, no silencio) | La investigación de tienda (no es paso de onboarding) |

## 4. Estrategia visual (el frente F3)

| Valor | Dónde vive | Lo consume | Estado hoy | Paso que lo produce |
|---|---|---|---|---|
| Presupuesto de fotos (`total_imagenes`) + tablas por producto | config → `mpl.esquema_mockups` | generar-manifiesto (§M5) | **provisional** (`estado: provisional_sin_pase_del_dueno`; valor vigente 10 hasta el pase del dueño) | **Calibración visual, Fase 1** (nuevo en onboarding v0.2.0; antes: SIN PASO — la causa raíz de F3) |
| Pesos por composición + producto principal | config → `mpl.esquema_mockups.pesos` | generar-manifiesto | **provisional** (5/3, derivados del esquema viejo) | **Calibración visual, Fase 1/4** (nuevo) |
| Catálogo de tomas por producto + a evitar | fichas → `tomas_preferidas` / `tomas_a_evitar` | generar-manifiesto, verificar-mockups, puerta-pinterest | **provisional** (`estado: provisional_sin_pase_del_dueno` en ambas fichas; sembrado desde el historial, solo 1 etiqueta de cámara con evidencia real) | **Calibración visual, Fase 4** (nuevo: el dueño elige desde las opciones reales de Printify con muestras) |
| Prioridad de cobertura fina | config → `mpl.esquema_mockups` (reglas) | generar-manifiesto | **provisional/parcial**: la regla general vive en el mecanismo (§M5); el orden fino de ESTA tienda no está declarado por separado | **Calibración visual, Fase 1** (nuevo) |
| Escenarios de video de la tienda | config → `mpl.esquema_videos` | publicar §M6, publicador-lote | **provisional de hecho**: el bloque trae los escenarios A–D del mecanismo pero **no trae campo `estado` propio** — hueco menor de registro (su estado efectivo es el de la estrategia visual: provisional) | **Calibración visual, Fase 1** (nuevo) |

## 5. Operación

| Valor | Dónde vive | Lo consume | Estado hoy | Paso que lo produce |
|---|---|---|---|---|
| Crons operativos (horarios, N, cuerpos) | definiciones de cron de la instancia (workspace del goal) | el scheduler | **configurado** | Fase 5 |
| Reglas de track (bifurcación personalizable/no) | config → `flujo_bifurcado` | publicar §0, propuestas | **configurado** | Fase 1.2 |

## 6. Remanente detectado al inventariar (no es un valor vivo)

- **`config → mockups` (bloque top-level):** selección fija vieja
  (`flat`, `folded_2_decorado`, `lifestyle_1..3`, `hero_preferencia`,
  nota «Esquema MPL = 10 imágenes»). **Ningún skill ni script del
  sistema lo lee** (verificado por grep el 2026-10-23): el mecanismo
  vivo es `mpl.esquema_mockups` + manifiesto. Es un remanente del
  esquema anterior viviendo en la ficha — candidato a retiro con
  la palabra del dueño (doctrina: los remanentes de flujos
  descartados se eliminan, no se conservan). Queda registrado
  aquí como hallazgo de F5; este inventario no lo borra.

## 7. Resumen de huecos (SIN PASO o estado pendiente)

1. **Estrategia visual completa** — provisional/sin configurar;
   su paso YA existe (Calibración visual, onboarding v0.2.0) y
   se cobra con el pase del dueño (frente F3/F8).
2. **Referencia de formato profesional, banco de keywords,
   instancia de la vitrina, mensajería** — valores configurados
   cuyo **paso productor no está documentado en onboarding**:
   nacieron de la operación. Al abrir la segunda tienda, el
   onboarding debe nombrarlos (la prueba de frío F7 los trata
   como checklist de detección, no como supuestos).
3. **`esquema_videos` sin campo `estado`** — hueco menor de
   registro dentro de la estrategia visual.
4. **Personalización `pendiente_investigacion`** — diferida y
   declarada; no es silencio.
5. **Bloque legacy `config → mockups`** — remanente sin
   consumidores, pendiente de retiro con palabra del dueño.
