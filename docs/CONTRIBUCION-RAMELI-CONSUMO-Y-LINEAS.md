# Contribución propuesta a Rameli — consumo declarado↔consumido y líneas vigentes de instancia

**Estado: PROPUESTA DOCUMENTADA (2026-10-27) — no aplicada al
framework.** Se prepara como pull request documentado según
`rameli/docs/CONTRIBUCIONES.md` cuando el dueño lo decida; esta
unidad la deja escrita y probada en la aplicación. Origen:
auditoría de alineación `docs/AUDITORIA-ALINEACION-RAMELI-2026-10-27.md`.

## 1. El problema (caso real)

Una aplicación Rameli perdió en silencio una línea que su dueño
había decidido: la ficha no la declaraba (su estado vivía en la
salida periódica de un skill, con vigencia de 7 días), el
artefacto consumidor declaraba cupo 0, y la investigación
siguiente volvió a **proponer** lo ya decidido porque ningún
registro de «ya decidido» gobernaba su entrada. El validador de
colocación pasó en verde durante todo el episodio — correctamente:
verifica colocación, no consumo. Ninguna puerta del framework
cruza «lo que la ficha declara» contra «lo que la salida
periódica asigna», ni «lo que un productor emite» contra «lo
que su consumidor declara leer».

## 2. La capa

Framework, por la prueba de quitar el dominio: «una declaración
vigente de la instancia debe llegar al artefacto que la ejecuta,
y eso se verifica en el cierre de quien emite el artefacto» no
contiene vocabulario de tiendas, canales ni nichos. Las
instanciaciones (qué líneas, qué bloques de asignación) son de
cada aplicación.

## 3. El cambio propuesto (acotado, dos piezas)

**Pieza A — Patrón «línea vigente de instancia» (doc del
framework, p. ej. en `DATOS-MULTIUNIDAD.md` o doc nuevo):** la
ficha de una unidad puede declarar líneas vigentes — decisiones
abiertas del dueño con estado (`operativa|piloto|pausada`), su
origen y fecha y, si aplica, un cupo mínimo — siguiendo el mismo
patrón de bloque calibrado que ya usan los valores de ficha
(nota con la decisión y su fecha, disparadores de
recalibración). Las salidas periódicas **asignan contra** las
líneas; nunca declaran su estado.

**Pieza B — Chequeo de consumo (protocolo de cierre, hermano
del protocolo de `VALIDACION-COLOCACION.md`):** al cerrar la
emisión de un artefacto periódico, el emisor verifica — con un
helper determinista de la aplicación, calibrado en ambos
sentidos — que toda línea vigente aplicable recibió asignación
en el artefacto o una pausa declarada con su motivo. Sin
asignación y sin pausa = el cierre no pasa. El framework impone
la propiedad y el momento (el cierre del emisor); el helper y
los nombres de bloque son de la aplicación.
**Pieza C (menor) — Agenda que invoca skill:** declarar en el
mismo doc que una agenda externa que despierta un flujo de la
aplicación **invoca** el skill dueño del flujo y no duplica su
método en su cuerpo; la aplicación mantiene un inventario de
agendas (agenda → skill → estado) en su doc de flujo, para que
la deriva agenda↔skill sea detectable. (Caso previo de la misma
aplicación: auditoría v0.11.0, B3 — un consumidor-agenda quedó
atrás respecto a su skill.)

## 4. La evidencia

- El episodio completo, con fechas y artefactos, en
  `docs/AUDITORIA-ALINEACION-RAMELI-2026-10-27.md` §§1–4 de
  esta aplicación.
- Adopción probada en la aplicación (misma unidad): líneas en
  la ficha, estado retirado del artefacto semanal, helper
  `scripts/verificar-consumo-lineas-tienda.py` calibrado contra
  el artefacto real previo al arreglo (FAIL nombrando la línea)
  y contra el estado alineado (PASS), integrado al cierre del
  skill emisor y a la puerta de cierre de la aplicación, con
  casos permanentes en la suite de regresión de ese skill.
- La investigación convertida en skill (entradas desde la
  ficha, puerta «lo decidido no se re-propone») elimina la
  segunda mitad del episodio en la misma adopción.

## 5. Compatibilidad

Aditivo puro: no cambia `lint`, `test`, `validar` ni el formato
de skills; ninguna aplicación queda en violación retroactiva.
Cada aplicación lo adopta en su siguiente migración o fase,
declarando sus líneas y su helper.
