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

## 2. Orquestación — la doctrina es una: workers fríos

**(Sección reescrita el 2026-10-19, corrección pedida por el
dueño: la versión original presentaba las primitivas del
entorno como una "forma de trabajo alternativa no adoptada", y
ese encuadre fabricó una confusión — como si hubiera dos
caminos rivales entre los que se elige por gusto. No los hay.)**

La doctrina de ejecución de esta app es la del framework,
una sola: **workers fríos** (chat nuevo, brief limpio con el
objetivo y los punteros a los skills, sin heredar historial),
adoptada por flujo en la migración a v0.11.0 con su registro
en `docs/MIGRACION-RAMELI-V0110.md`. Lo que varía entre flujos
no es la doctrina, es **el despertador**:

- **El chat orquestador**, cuando un humano conversa y decide
  (etapas de calibración e iteración: el chat decide y despacha
  workers; no ejecuta él mismo ni crece con el trabajo).
- **El cron**, cuando el trabajo es programado (etapa de
  automatización: el cron despierta la corrida y la corrida
  trabaja con la misma doctrina — workers, checkpoints,
  registro).

Donde un flujo no usa worker, el motivo está en ese mismo
registro de adopción (puertas dentro de un flujo, tareas de
1–2 pasos, la conexión a Etsy que exige el clic del dueño en
vivo, el onboarding guiado por fases).

Las primitivas que la arquitectura del framework describe
como disponibles en el entorno (la Pieza 4: workflows con
snapshot, `agent()` con schema, verificador-reparación en
código) **no son una doctrina rival ni una alternativa entre
la que esta app "eligió" no estar**: son capacidades del
entorno que hoy ningún flujo necesita. Si un flujo futuro las
necesita, se usan dentro de la misma doctrina (un worker las
invoca como invoca cualquier herramienta) y se anota aquí.

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
