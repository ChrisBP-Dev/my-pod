# Delimitaciones de adopción — lo no adoptado, declarado

> Adoptado el 2026-10-19 como Propuestas 6 y 7 de la auditoría de
> adopción (`docs/AUDITORIA-ADOPCION-V0110.md`, brechas B5, B6 y
> B7). Regla madre: lo que la app decide NO adoptar del framework
> se declara aquí con su motivo y su disparador de revisión — una
> no-adopción declarada es una decisión; una no declarada es un
> hueco que cada auditoría vuelve a "descubrir".

## 1. Flujo comercial por API/scripts (F7) — dueño y ruta

**Dueño del flujo:** la operación comercial continua es un flujo
de la aplicación sostenido por scripts de la raíz (`scripts/`),
consumido por la estratega (F4) y por la publicación (F2). No
tiene skill propio **por decisión**: su procedimiento es
determinista y vive en los scripts; crear un skill que lo
re-narre sería prosa duplicada. Su ruta, completa:

| Pieza | Qué hace | Puerta / verificación |
|---|---|---|
| `scripts/precios_comunes.py` + `scripts/precios-variacion-api.py` | Aplica la tabla de precios por variación vía API de Etsy (GET → cambia solo precios → PUT) | `--no-op` como prueba de seguridad antes de `--aplicar` |
| `scripts/verificar-precios.py` | Verifica que los precios vivos coincidan con la tabla esperada | PASS/FAIL por listing |
| `scripts/import-ventas-etsy.py` | Ledger de ventas M2: receipts, favoritos, reviews → `data/ledger-ventas.json` | Watermark incremental; conciliación CSV opcional |
| `scripts/sincronizar-registro-printify.py` | Reconcilia `data/registro-listings.json` contra Printify (IDs reales) | Sale con código 2 ante CONFLICTO: el consumidor debe detenerse |
| Ofertas y calendario de descuentos | Viven en `data/tiendas/<id>/config.json` (`calendario_descuentos`) y se operan por navegador (la API no las expone) | Revisión del dueño; ver `docs/ESTANDAR-ETSY-API-VS-NAVEGADOR.md` |

**Qué manda:** el config de la tienda (precios, calendario) y la
directriz vigente de la estratega. **Disparador para crear el
skill propio:** la apertura de una segunda tienda (el flujo
pasaría a operar por tienda, no global) o que F7 gane pasos con
juicio que hoy no tiene.

## 2. Orquestación determinista del runtime (Pieza 4 de Rameli) — no adoptada, con motivo

El framework declara como patrón las primitivas del runtime
(workflows guardados con snapshot, `agent()` con `schema` como
gate en código, verifier-repair programado, `parallel()` /
`pipeline()`). **Esta app no las usa en ningún flujo, y es
deliberado:**

- El grafo de cada flujo ya es fijo y está versionado en la forma
  que esta escala necesita: cuerpos de cron guardados,
  `FLUJO-PIPELINE.md` y los procedimientos de los skills, con las
  puertas como scripts deterministas que bloquean.
- Las unidades de trabajo son corridas de cron y workers de chat
  (modelo C16, adoptado con su registro), no agentes invocados
  desde un workflow JS: no hay hoy ningún punto donde un gate
  deba decidir en código sobre salidas estructuradas de varios
  agentes en paralelo.

**Disparador de revisión:** el primer flujo donde un gate deba
evaluar en código la salida de agentes paralelos (p. ej.
producción de artes con verificador independiente en la misma
corrida), o donde el snapshot versionado de un workflow aporte
algo que el cuerpo de cron no dé. Cuando ocurra, se adopta para
ese flujo y se anota aquí.

## 3. Capa de juicio del framework (evals capa 2 + A/B del constructor) — estatus

**No se adopta como práctica continua.** Motivo: su costo
(herramientas con juez por modelo y corridas A/B por skill) no se
paga con el beneficio a esta escala, y el juicio real sobre lo no
medible ya lo ejercen las puertas humanas del dueño donde el
sistema las declara (arte, directriz semanal, paquete comercial,
publicación). La capa determinista (C5) sí es obligatoria y está
cubierta o declarada skill por skill.

**Sí se adopta, acotado:** al crear un skill nuevo o subir uno de
versión mayor, su aceptación incluye una comparación contra un
agente genérico (la forma A/B del constructor, aunque sea una
sola corrida documentada) y el resultado se registra en el
CHANGELOG del skill. Sin ese registro, la versión mayor no se
declara terminada.

**Disparador de revisión:** si un skill de juicio (estrategas)
empieza a fallar en producción de forma repetida sin que sus
puertas humanas lo atrapen, la capa de juicio se reevalúa para
ese skill primero.
