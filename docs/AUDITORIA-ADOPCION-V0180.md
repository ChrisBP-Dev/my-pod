# Auditoría de adopción — My POD × Rameli v0.18.0 (2026-10-21)

> Pieza obligada de esta migración: el delta 0.17.0 → 0.18.0
> trae capacidad nueva, así que la auditoría **no es
> diferible** (nota de migración v0.18.0 en
> `rameli/MIGRACIONES.md`). Registro de la unidad:
> `docs/MIGRACION-RAMELI-V0180.md`. Método: matriz de la
> capacidad nueva × flujos, con veredicto y evidencia en el
> repositorio por celda — nada de memoria. Donde la
> evidencia no alcanza, la celda dice **sin evidencia**.
> Esta unidad se ejecuta como **actualización completa**
> por mandato del dueño (2026-10-21 08:50 EDT): la fase de
> mejora v0.17.0 se ejecuta en la misma operación (ver §4).

## Método y bases verificadas

- **Framework de referencia:** repo `rameli`, `VERSION` =
  **0.18.0** (commit de fusión del PR #9 `bbb587c`; tag
  `v0.18.0` verificado por `git ls-remote`; Release de
  GitHub v0.18.0 Latest verificado por el orquestador al
  abrir la operación); delta en su `CHANGELOG.md` y la
  nota en `MIGRACIONES.md`. Regresión del framework:
  **24 ok, 0 fallos** (registrada en su CHANGELOG).
- **Aplicación auditada:** repo `my-pod`, `main` en
  `af00e35` al abrir (pin **0.17.0**); rama de la unidad:
  `migracion-rameli-v0180`.
- **Verificaciones corridas en vivo para esta auditoría**
  (2026-10-21): línea base idéntica antes y después —
  `rameli lint` **VERDE** total; `rameli test` **53 casos,
  0 fallas** (13+4+3+18+15), con los mismos 4 avisos
  preexistentes de skills sin `evals/`; `rameli validar`
  en la instancia viva **0 fallos, 0 avisos** antes y
  después del pin.
- **Precedente:** `docs/AUDITORIA-ADOPCION-V0170.md`
  (matriz contra v0.17.0, brecha B1-17 y observación del
  ritual de los lunes). Esta auditoría **confirma** los
  veredictos cuyas evidencias siguen en pie, **agrega**
  la capacidad nueva del delta (**C27, C28**) y **cobra**
  B1-17 (ver §3).

## Leyenda de veredictos

| Código | Significado |
|---|---|
| **P** | Adoptado y probado — evidencia de uso real |
| **A** | Adoptado sin estrenar — escrito/instanciado, sin corrida real |
| **NA** | No aplica — con motivo declarado |
| **B** | Brecha real — remite a la propuesta de la fase de mejora |
| **SE** | Sin evidencia — el repo no permite verificarlo |

## 1. La capacidad nueva del delta

- **C27 — Declaración del repo de registros y ámbito de
  instancia por separación (NUEVA, v0.18.0).**
  (`rameli/docs/DATOS-INSTANCIA.md` §4 y §5.) La
  separación de registros se **declara** en
  `rameli.json → datos.repo_datos` (objeto con `url`
  obligatoria; `nombre`, `contiene`, `nota` opcionales; o
  cadena con la URL). Con separación declarada, el
  chequeo 4 trata un hogar presente pero **sin ninguno**
  de sus registros requeridos como **AVISO** («registros
  sin restaurar» / «sin registros en esta copia»), no
  FALLO; el hogar **parcial** sigue siendo FALLO y sin
  declaración el FALLO se conserva intacto.
- **C28 — Doctrina de actualización completa (NUEVA,
  v0.18.0).** (`rameli/MIGRACIONES.md`, sección propia.)
  Cuando el dueño ordena una actualización como completa,
  la orden ES el dale de la operación entera (migración →
  auditoría → propuesta → ejecución de la fase de mejora),
  con aprobación delegable al orquestador y registro de
  cada decisión; lo genuinamente del dueño (decisiones de
  producto irreducibles) se le sigue trayendo.

## 2. Matriz de la capacidad nueva por flujo

| Flujo | C27 | C28 | Evidencia / motivo |
|---|---|---|---|
| **F1 Propuestas (flujo v2)** | **P** | NA | Sus registros viven en `my-pod-datos` y su cron commitea vía `scripts/registros-datos.py` (mecánica D1); la declaración `datos.repo_datos` lo hace visible al sistema desde esta migración. C28 no es un flujo de la tienda. |
| **F2 Publicación por lote** | **P** | NA | El registro del lote commitea en el repo de datos vía el puente (verificado en el lote del 2026-10-20 y en esta unidad). |
| **F3 Pinterest diario** | **P** | NA | Corrida real de hoy (2026-10-21): su commit de cierre vía el puente dejó `my-pod-datos` en `0843bcb` («Pinterest diario 2026-10-21»), sin ahead. |
| **F4 Dirección semanal** (estratega + investigación + trend-scan) | **P** | NA | Sus salidas (directriz, config, investigaciones, tendencias) son registros que commitean en `my-pod-datos` con el puente (cuerpos de cron re-apuntados en D1). |
| **F5 Onboarding de tienda** | **A** | NA | El playbook declara que una tienda nueva nace con su hogar en `data/tiendas/<id>/` y su ciclo de commit por el puente; con la declaración en `rameli.json`, un clon frío de la app ya sabe dónde restaurar los registros. Sin estrenar con una tienda nueva tras v0.18.0. |
| **F6 Conexión Etsy API** | NA | NA | Sin registros propios bajo `data/` más allá del config de la tienda (cubierto por F4/F7). |
| **F7 Operación comercial** | **P** | NA | `config.json` (precios/calendario) es registro de instancia: el cron `etsy-sale-25-to-20-oct31` ya trae su paso de commit al repo de datos (sumado en D1). |
| **F8 Puertas transversales** | **P** | NA | `rameli validar` ES la puerta de C27: probada en esta unidad en los dos estados + control de hogar parcial (ver §3). |
| **F9 Mantenimiento del sistema** | **P** | **P** | Esta unidad ES C28 en ejercicio: mandato del dueño 2026-10-21 08:50 EDT, aprobación delegada a Jarvis, P1 ejecutada como framework (Rameli v0.18.0) y P2 ejecutada aquí; las decisiones quedan registradas en `docs/MIGRACION-RAMELI-V0180.md` y en la fase de mejora v0.17.0 cerrada como EJECUTADA. |

## 3. Respuestas expresas a la nota de migración v0.18.0

- **¿La app separó registros?** Sí — separación D1
  ejecutada el 2026-10-21 en la unidad v0.17.0 (repo
  privado `my-pod-datos`, historia por split de rutas,
  sistema sin registros en árbol ni en historial).
- **¿El repo está declarado en `repo_datos`?** Sí, desde
  esta migración: `datos.repo_datos` en `rameli.json`,
  forma canónica de objeto (`nombre` `my-pod-datos`,
  `url` `git@github.com:ChrisBP-Dev/my-pod-datos.git`,
  `contiene` `data`, `nota` con la mecánica y D2). Es la
  ejecución de la brecha **B1-17** — **CERRADA**.
- **¿Validó en los dos estados?** Sí, con evidencia de
  esta unidad (clones en `/tmp/clon-v0180`, desechables;
  los resultados quedan registrados en el registro de
  migración):
  - **Instancia restaurada** (la viva: sistema + registros
    físicos + puente verificado): `rameli validar`
    **0 fallos, 0 avisos**. Réplica en frío (clon del
    sistema + clon de datos + `registros-datos.py pull`,
    144 registros restaurados): **0 fallos**, 1 aviso de
    ámbito por `data/auditoria-2026-10-15` (zona de media
    de esta instancia que no viaja en ningún repo — el
    mismo aviso registrado en la unidad v0.17.0).
  - **Clon de solo sistema:** **0 fallos**, con AVISO de
    hogar «presente pero sin registros en esta copia»
    (más los avisos de ámbito esperados por los registros
    globales y la zona de historial de instancia). Antes
    de v0.18.0 este estado daba FALLO de hogar incompleto.
  - **Control de ámbito estrecho:** el mismo clon con el
    hogar **parcial** (solo `config.json`) → **FALLO**
    «hogar incompleto» (3 fallos), como manda el canon: la
    adopción no suaviza hogares rotos.

## 4. El resto de la matriz

Se **confirman** los veredictos de la auditoría v0.17.0
con la evidencia de hoy (lint verde, regresión idéntica
de 53 casos, `rameli validar` 0/0 en la instancia viva,
mapa de datos sin cambios de layout salvo la declaración
`repo_datos`). La **observación del ritual de los lunes**
de esa auditoría se cobra como **P2 ejecutada** en esta
unidad (evidencia y decisión en el registro de
migración): el ritual tiene función propia frente a
`equipo-pod-investigacion-semanal` — no hay duplicación
total — y sus rutas quedaron corregidas al layout
vigente.

## 5. Brechas y observaciones nuevas

- **Sin brechas nuevas del delta.** La fila de separación
  de registros que la nota v0.18.0 suma a la matriz queda
  en **P** (declarada y probada en los dos estados).
- **Hallazgo de barrido marcado para el dueño (no es del
  delta; ver el inventario completo en el registro de
  migración):** el cron `pod-ritual-viernes-h12` lee las
  reglas H11/H13 en `docs/operacion/` del workspace del
  goal — sin equivalente portado en esta app — y su
  `ledger-registros.md` quedó en 14 filas del 2026-10-16
  frente al registro vivo de la tienda; además sus reglas
  (kill 60 días / observación 30 días, H11) difieren de
  las que enuncia `equipo-pod-revision-viernes` (matar
  «sin tracción en 30 días»). Elegir la fuente de reglas
  vigente (portar H11/H13 a la app, unificar en la
  revisión de viernes, o retirar el ritual) es una
  decisión de producto: queda **marcada**, no resuelta en
  silencio. El ritual NO se retiró en esta unidad: tiene
  funciones no duplicadas (condiciones de activación de
  Ads, fee bleed mensual, centro de comando).
