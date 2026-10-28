# Contribución propuesta a Rameli — la capa de agendas programadas

Documentada el 2026-10-27 a pedido del dueño, tras el barrido de
integridad de My POD. NO aplicada a `rameli`: se presenta como
propuesta (PR) cuando el dueño lo decida, como la contribución de
consumo de líneas (`CONTRIBUCION-RAMELI-CONSUMO-Y-LINEAS.md`).
My POD ya implementa la propuesta como referencia viva.

## El hueco

Rameli prescribe las capas que viven DENTRO del repo de la
aplicación (skills con entradas/salidas/puerta, fichas que
declaran, registros en la fuente) y `rameli validar` verifica su
colocación. Pero una aplicación operada por agentes se ejecuta
también por **agendas programadas** (los crons del entorno), y
esa capa vive FUERA del repo: el scheduler guarda los cuerpos en
su propio almacén y el framework no dice nada de ella — ni qué
puede contener un cuerpo, ni dónde se declara, ni cómo se valida.

Resultado medido en My POD (dos casos reales):

1. **Deriva de método (2026-10-22, «B3»):** el cuerpo de la agenda
   de propuestas duplicaba el método de un skill y quedó atrás
   cuando el skill cambió; hubo que corregirlo a mano.
2. **Referencia muerta invisible (2026-10-27):** el mismo cuerpo
   citaba `scripts/generar-datos-vitrina.py`, retirado el
   2026-10-26 con la vitrina de lectura en vivo. Ninguna puerta
   lo vio — ni `rameli validar` (el cuerpo no está en el repo) ni
   los lint/test de skills — y el error solo apareció porque un
   humano releyó el cuerpo antes de reactivar la agenda. Otro
   vigía arrastraba un contexto desmentido hacía 4 días.

El mecanismo (despertar agentes por horario) es legítimo y
necesario; lo que falta es su GOBIERNO dentro del sistema.

## El principio general (sin vocabulario de dominio)

Toda superficie que ORDENA trabajo de una aplicación y vive
fuera de su repo — agendas del programador del entorno, hooks,
disparadores — es una **capa declarada de la aplicación**, no un
detalle del operador. Si el framework no la declara, esa
superficie crece por acreción: cada operador la escribe a su
manera, duplica el método de los skills y deriva en silencio,
porque ninguna validación la alcanza. El anti-patrón tiene
nombre propio para poder prohibirlo: **calibrar en la agenda**
— ajustar el método donde se ejecuta en vez de donde el sistema
lo declara. Junto con la contribución de consumo de líneas
vigentes, esta propuesta cubre las dos fronteras que el
framework hoy no gobierna: lo que entra a la aplicación (las
líneas que la instancia declara y alguien debe consumir) y lo
que la despierta desde fuera (las agendas que la operan).

## La propuesta (contrato de agendas para el framework)

1. **La aplicación declara sus agendas** en su propio cuerpo
   (inventario en el FLUJO o equivalente): qué agenda existe, qué
   skill invoca y su estado. Agenda sin skill = hueco declarado.
2. **El cuerpo de una agenda INVOCA, no duplica:** ordena ejecutar
   el procedimiento de un skill (y conserva solo lo que el
   scheduler posee: horario, reintentos, reglas de entrega). Si
   un cuerpo difiere del skill, manda el skill y la diferencia se
   reporta como hueco.
3. **Validación cruzada repo ↔ agendas:** una puerta mecánica de
   la aplicación comprueba que todo lo que los cuerpos de agenda
   (y los SKILL.md y el FLUJO) citan — scripts, skills, rutas de
   la app — EXISTA. Se corre antes de activar o reactivar una
   agenda y al cerrar unidades que toquen cuerpos o scripts.
   `rameli validar` no puede hacerla (no ve el almacén del
   scheduler); la puerta vive en la app y el framework la exige
   por contrato.

## Implementación de referencia (My POD, 2026-10-27)

- Inventario de agendas en `FLUJO-PIPELINE.md` con la regla 3.
- `scripts/verificar-referencias.py`: escanea los cuerpos de las
  agendas de la app (proyecciones del scheduler), los SKILL.md y
  el FLUJO; falla nombrando cada referencia muerta. Calibrado en
  ambos sentidos el día de su nacimiento (PASS sobre 44 textos
  reales; FAIL ante una referencia sembrada).
- Cuerpos recalibrados a invocar skills (propuestas diarias e
  investigación semanal, 2026-10-27).
- Protocolo de gobierno en el FLUJO de la app: crear/modificar
  una agenda exige método en el skill → cuerpo que invoca →
  inventario actualizado → verificación en PASS → registro.
- El verificador también exige que cada cuerpo recurrente
  NOMBRE el skill que el inventario declara (la invocación es
  mecánica, no una costumbre).

## Cómo evolucionaría el framework si la adopta

1. **Contrato escrito** (documentación del framework): la capa
   de agendas queda nombrada entre las capas de una aplicación,
   con las tres reglas y el anti-patrón prohibido — cualquier
   aplicación nueva nace con la capa declarada.
2. **Verificador de referencia en el framework:** la puerta
   mecánica (existencia de referencias + invocación nombrada)
   se ofrece como script de referencia parametrizable (dónde
   viven las proyecciones de las agendas de ESA instalación),
   para que cada aplicación no la reimplemente.
3. **Extensión futura de `rameli validar`:** si una aplicación
   declara en su repo un manifiesto de agendas (id, skill que
   invoca, dónde se leen sus cuerpos), el validador puede
   incluir la capa en su veredicto y cerrar el hueco de raíz:
   ninguna superficie que ordena trabajo queda fuera del
   veredicto del framework.

El beneficio no es de una sola aplicación: toda aplicación
construida con el framework que opere con agentes programados
— esta tienda, el sistema de canales, cualquier otra — hereda
la misma protección, porque el defecto no era del dominio: era
de la frontera entre el repo y el entorno, que es exactamente
el territorio del framework.
