---
name: "investigacion-tienda"
description: "Investigación semanal de una tienda POD: lee la ficha (nicho, líneas vigentes), el registro y el ledger, y produce el reporte que la estratega consume, con propuestas que citan la línea que tocan."
compatibility: "framework >= 0.4.0"
metadata:
  version: "1.0.0"
  framework_version: "0.19.0"
  regression_suite: "evals/"
---

# Investigación de tienda POD

**Versión 1.0.0** (2026-10-27, recalibración de alineación a
Rameli): nace porque la investigación semanal vivía como cuerpo
de una agenda fuera del repo de la app — sin entradas, salidas ni
puerta declaradas, con la tienda y el nicho escritos en duro en
su texto. Este skill es su hogar; la agenda solo lo invoca.

## Rol

Investigar PARA la tienda que la ficha declara: qué se mueve en
su nicho, qué dice su propia operación (registro, ledger) y qué
debería mirar la estratega. NO decides la directriz (eso es
`estratega-tienda`), NO modificas skills, puertas ni flujos:
propones, con el formato de abajo.

## Cuándo usarme

- En la corrida semanal de investigación de una tienda (la
  agenda `equipo-pod-investigacion-semanal` me invoca), o cuando
  el dueño pide una investigación puntual de una tienda.
- NO para el rastreo de tendencias de producto (eso es el
  trend-scan, agenda propia declarada en el inventario de
  `FLUJO-PIPELINE.md`) ni para decidir la directriz semanal.

## Entradas (leer todas antes de investigar)

**Camino de lectura canónica:** primero
`python3 scripts/registros-datos.py pull` desde la raíz de la
app; la copia física de los registros es caché, la realidad es
el repo de datos.

1. **La ficha de la tienda** (`data/tiendas/<tienda-id>/config.json`):
   su `nicho` (nombre, subnicho) manda el tema de la investigación
   — nunca un nicho escrito en el cuerpo de una agenda — y sus
   **`lineas_vigentes`**: los focos/métodos que el dueño ya tiene
   abiertos, con su estado. Lo ya decidido NO se investiga como
   novedad ni se re-propone: se evalúa su avance o se pide su
   cambio con motivo.
2. `data/tiendas/<tienda-id>/registro-listings.json` — qué hay
   publicado, en qué temas, qué murió.
3. `data/tiendas/<tienda-id>/ledger-ventas.json` — ventas,
   favoritos, reviews. Si su watermark tiene >7 días, el reporte
   lo declara en la primera línea («decisión a ciegas» es también
   el titular de la estratega) y la prioridad 1 es su refresco.
4. La investigación y el trend-scan más recientes de la tienda
   (`investigaciones/`): no repetir hallazgos sin evidencia nueva.
5. `data/banco-keywords/<nicho>.md` — el banco del nicho de la
   ficha.

## Método

1. **Operación primero:** qué vendió/murió/fue favorito según
   registro y ledger (con números y fechas, no impresiones).
2. **Mercado del nicho de la ficha:** tendencias, keywords
   emergentes, estrategias SEO y movimientos de competidores del
   nicho declarado. Cada hallazgo cita su fuente (qué superficie,
   qué fecha).
3. **Cruce con las líneas vigentes:** por cada línea abierta de
   la ficha, qué encontró la investigación que la alimenta,
   la frena o pide recalibrarla (ocasiones, formatos, precios
   del mercado para ESA línea). Una línea sin una sola mención
   en dos corridas seguidas es un hallazgo en sí mismo y se
   declara.
4. **Propuestas (PROP-INV):** cada propuesta declara si toca una
   línea vigente (citando su `id` de ficha: la propuesta es sobre
   la línea, no la línea de nuevo) o si pide el **alta de una
   línea nueva** (y entonces lo dice así, para que el dale del
   dueño la abra en la ficha). Propuesta sin esa declaración no
   entra al reporte.

## Salida

Un solo artefacto: `data/tiendas/<tienda-id>/investigaciones/
<YYYY-MM-DD>-investigacion.md`, con:

- Primera línea: titular con la fecha y, si aplica, la
  declaración de ceguera de datos (ledger viejo).
- `## Fuentes` — qué se leyó de la ficha (nicho y líneas citadas
  por su `id`), del registro y del ledger, con su frescura.
- Hallazgos (operación, mercado, líneas) con su evidencia.
- **Top 5 prioridades** para la estratega, en orden.
- PROP-INV con la declaración del Método §4.

**Escribir = commitear** en la misma corrida, en el repo de
datos: `python3 scripts/registros-datos.py commit -m
"Investigación semanal <fecha>"` desde la raíz de la app.

## Puertas mecánicas

Antes de dar la corrida por cerrada:
`python3 scripts/verificar-investigacion.py --reporte
data/tiendas/<tienda-id>/investigaciones/<fecha>-investigacion.md
--shop <tienda-id>` debe dar **PASS** (fuentes declaradas,
prioridades presentes, líneas vigentes citadas o ausencia
declarada, ninguna PROP re-proponiendo una línea vigente). Sin
PASS no hay entrega: el reporte no existe para la estratega.

## Reglas

- Esta investigación OPTIMIZA el sistema, nunca lo rompe: no
  modifica skills, gates ni flujos; las mejoras a ellos van como
  PROPUESTA en el reporte (regla heredada de la agenda que este
  skill reemplaza, 2026-10-15).
- Ningún valor de una tienda concreta (su id, su nicho, sus
  precios) vive en este skill: todo eso se lee de la ficha en
  cada corrida.
- No edites MEMORY.md.

## Calibraciones (mecanismo vs aplicación)

- `MECANISMO:` las entradas, la estructura de salida, la puerta
  `scripts/verificar-investigacion.py` y la regla «lo decidido
  no se re-propone» — universales para una tienda POD.
- `CALIBRACIÓN:` el nicho, las líneas y los bancos de cada
  tienda viven en su ficha y en `data/banco-keywords/`; este
  skill no trae ninguno.
