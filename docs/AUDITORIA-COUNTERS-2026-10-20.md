# Auditoría counters — 2026-10-20

Pedida por el dueño tras el rescate de p046: si el flujo está
"pulido", ¿por qué un error de esta clase llegó hasta Printify?
¿Fue el skill, las indicaciones, o qué — y dónde más puede estar?

## Qué pasó (línea de tiempo, con evidencia)

- **2026-10-17:** p046 "ICU: I Care U" se genera y entra a drafts
  por el flujo de propuestas de entonces. Nace con el fondo
  horneado dentro de los huecos cerrados de "Care" (C, a, r, e).
- Las puertas vigentes lo dejaron pasar TODO (verificado de nuevo
  el 2026-10-20 con el código de entonces): `sin_blanco_puro`
  0.0%, `sin_blancos_interiores` 0.69%, esquinas limpias. La clase
  "counters" era **gate humano declarado**: el ojo del dueño en su
  revisión de drafts en Printify (paso M2). El dueño la cazó ahí —
  el sistema "funcionó como estaba diseñado", pero el diseño
  dejaba la clase en el paso MÁS CARO (draft ya creado) y con un
  PASS mecánico total que daba falsa tranquilidad.
- **2026-10-18/19:** la auditoría de recortes revisó COMPLETITUD
  de composición, no counters. p046/p047 quedaron "completos sin
  tocar" — cierto en recortes; los counters nunca se midieron.
  El "sin tocar" se leyó después como "sanos": confusión de
  alcance, no un error de esa auditoría en su alcance.

## Causa raíz (tres capas)

1. **Generación:** el quitado de fondo exterior (flood-fill) y el
   key de blanco puro no alcanzan zonas ENCERRADAS por el contorno
   de una letra; el fondo atrapado además no es blanco puro
   (media ~249/245/237), así que ninguna limpieza canónica lo toca.
2. **Medición:** todos los gates de fondo eran de porcentaje
   global o de borde. Ninguno medía COMPONENTES interiores. La
   propiedad real —una mancha localizada, maciza y acromática—
   no la medía ningún proxy: por eso el PASS era total y falso
   para esta clase.
3. **Diseño del flujo:** la clase vivía asignada al gate humano
   en la revisión de Printify, contradiciendo el principio del
   propio skill (rechazar en la puerta de arte, lo más barato).
   Lo que el código no distingue, el sistema lo empujó al paso
   caro en vez de a la entrega de aprobación.

## Validación integral aplicada (2026-10-20)

- `rameli validar .` → **0 fallos, 0 avisos** (9 skills).
- `rameli test` (9 skills) → **regresión verde: 51 casos, 0
  fallas**. AVISO preexistente: 3 skills sin `evals/`
  (conectar-etsy-api, estratega-pinterest, publicador-lote) —
  hueco de cobertura: sin regresión, un cambio ahí no se caza.
- `rameli lint` de puerta-arte-propuesta → verde.
- **Nuevo gate** `sin_counters_rellenos` (puerta-arte-propuesta
  v0.6.0) + `scripts/limpiar-counters.py`, calibrados contra
  buenos conocidos y el malo real.
- **Barrido de los 47 artes vigentes** del registro con el
  detector + adjudicación visual de los marcados. El barrido
  recalibró el propio gate (→ v0.6.1): la densidad por bbox daba
  falsos positivos en líneas finas y brillos; se añadió el
  GROSOR y el piso de sospechosos (detalle en el CHANGELOG del
  skill).

## Resultado del barrido (tras adjudicar con el ojo)

- **Rellenos duros confirmados:** solo p046 (rescatado; v2 en
  drafts desde el 2026-10-20, verificado por API). p047 marcaba
  19 componentes, pero el dueño lo eliminó el 2026-10-20 en su
  limpieza de drafts: fuera de alcance, no se reconstruye.
- **Falsos positivos confirmados (diseño legítimo):** p043
  (líneas decorativas), p045 (brillos metálicos de las letras
  tubo), p062 en su mayoría (elementos finos de invierno).
- **Sospechosos por adjudicar** (manchas chicas, radio <13; la
  métrica no separa relleno chico de brillo de diseño):
  drafts vivos p052 (counters de D/R del titular: probablemente
  rellenos chicos reales), p054, p055, p056, p053 (1 componente
  en el borde exacto del umbral, 1500px); propuestas v2 p058,
  p063, p067; publicados p002, p021, p022, p031, p032, p034
  (1.5–10k px por diseño ≈ manchas de ~2–5 mm a escala de
  impresión).
- **Limpios:** el resto, incluidos los canónicos de calibración.

## Recomendaciones (esperan palabra del dueño)

1. Limpiar los sospechosos de drafts/propuestas AL APROBAR cada
   diseño (la limpieza de sospechosos exige adjudicación visual
   caso por caso: `limpiar-counters.py --incluir-sospechosos`).
   Costo bajo mientras sigan en draft.
2. Publicados: NO tocar listings vivos por manchas de 2–5 mm sin
   evidencia de que se vean en el mockup/producto; el riesgo de
   tocar un listing sano supera el beneficio.
3. Crear `evals/` mínimos para los 3 skills sin regresión.
4. Higiene observada el 2026-10-20 ~09:25: la corrida de
   Pinterest dejó `registro-listings.json` con cambios sin
   commitear en el árbol principal — contra la regla "escribir =
   commitear en la misma corrida". Revisar esa corrida/cron.

## Estado de esta auditoría

Rescate de p046 y corrección del sistema en la rama
`correccion-p046-counters`; la fusión a main se registra en el
commit de cierre de esta unidad.

## 7. Addendum del mismo día — adjudicación completa y correcciones aplicadas

Con el dale del dueño («aprovecha que los encontraste y
corrígelos y mejóralos»), se adjudicó con zooms a resolución
completa CADA componente marcado en los 15 diseños del barrido
y se aplicaron las correcciones. Resultado que CORRIGE la
sección 5 de esta auditoría:

- **El único relleno real del registro era p046.** Los
  componentes duros de p052 (válvula del tensiómetro), p054
  (dientes de la enfermera), p063 (fondo crema del bloque
  tipográfico), p002 (disco del estetoscopio), p022 (luz de la
  lámpara) y p032 (blanco del ojo del pavo) son DISEÑO. Los
  sospechosos de p052/p062/p021/p034 son el bisel 3D crema de
  las letras; los de p043/p045/p053/p055/p056/p058/p067/p031,
  brillos, líneas y detalles finos. La frase de la sección 5
  «p052: rellenos chicos probablemente reales» era INCORRECTA:
  era el bisel. Ningún arte vivo se limpió: limpiar a ciegas
  habría destruido diseño bueno.
- **Veredictos registrados** en el registro
  (`adjudicacion_counters_2026_10_20` en las 15 entradas) para
  que un barrido futuro no re-marque lo ya juzgado.
- **Corrección de sistema (puerta-arte-propuesta v0.6.2):** el
  FAIL de `sin_counters_rellenos` queda definido como
  «adjudica con el ojo» (paso 2c: zoom por zona → veredicto →
  recién entonces limpieza), y `limpiar-counters.py` exige el
  flag `--adjudicado` para escribir (suite 18 casos, F10c
  nuevo). La lección de calibración: en arte ilustrado de este
  nicho, geometría y color NO separan relleno de diseño; el
  gate correcto es el que obliga a mirar barato, en la etapa de
  propuesta del flujo v2, no el que decide solo.
- **Los 3 skills sin suite NO son un hueco:** conectar-etsy-api,
  estratega-pinterest y publicador-lote declaran la ausencia
  como DECISIÓN (auditoría de adopción 2026-10-19, Propuesta 2,
  aprobada por el dueño) con su justificación en cada SKILL.md.
  La recomendación de la sección 6 («crear evals mínimos»)
  queda RETIRADA: no se repropone trabajo ya decidido.
- **Pinterest:** el hueco real era de CIERRE, no de contenido:
  la corrida publica y registra pero ningún documento le decía
  que commiteara. Corregido en estratega-pinterest v0.1.3
  (regla de cierre con commit) y en el cron
  `equipo-pod-pinterest-diario` (paso 6: commit + push +
  verificación). La corrida del 2026-10-20 quedó saneada a mano
  en el commit de este cierre. `pin_ultimo`: la convención de
  facto (URL del pin más reciente) quedó escrita en el skill y
  en el cron.
