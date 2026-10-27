# Patrones de resiliencia operativa

Patrones portables (independientes del dominio) para workers largos con
dependencias externas — navegador, APIs de terceros, CLIs. Probados en
batalla en My POD (caída de Printify 2026-10-16). El skill
`onboarding-tienda` los aplica al crear los crons de una tienda nueva.

Regla madre: **lo que puede fallar por causas externas no debe costar
trabajo desperdiciado ni requerir memoria humana para retomarse.**

## P1 — Health-check antes de trabajar

Antes de arrancar una corrida larga, verifica que cada dependencia
externa responde. Si no responde, NO ejecutes nada: reporta y programa
reintento. El costo de un chequeo es segundos; el costo de una corrida
inútil es horas.

- Mecánica: `curl -s -o /dev/null -w '%{http_code}' --max-time 15 <url>`.
  Se exige el código esperado (normalmente 200) antes de continuar.
- El endpoint se **calibra por servicio** (verificado, no supuesto).
- Ejemplo tienda 29222324 (NO regla): la app de Printify vive en
  `https://printify.com/app/` (200); `my.printify.com` devuelve 500
  (dominio caído/retirado, verificado 2026-10-16).
- Anti-patrón: asumir sesión/red sanas porque "ayer funcionó".

### P1-bis — El health-check debe ser representativo del canal real de trabajo (recalibrado 2026-10-27, decisión del dueño)

La sonda y el trabajo no siempre viajan por el mismo canal: una petición
anónima por terminal (sin sesión, desde la IP de un centro de datos) puede
ser bloqueada por el servicio aunque el canal real de trabajo — el
navegador con la sesión de la cuenta — funcione perfectamente. Una sonda
así NO es una puerta: es solo una señal.

- Sonda OK (código esperado) → se trabaja.
- Sonda fallida → NO se detiene la corrida ni se consume reintento (P3)
  todavía: se verifica por el **canal real de trabajo** (p. ej. abrir el
  servicio en el navegador de publicación y comprobar que carga).
- Canal real OK → se trabaja, y el reporte anota la divergencia
  («sonda X falló, canal real OK»).
- Canal real fallido (verificado con una segunda comprobación) → recién
  ahí hay salud fallida: se detiene y corre P3.
- Caso real (calibración de Pinterest en My POD, 2026-10-24/26/27):
  `curl https://www.pinterest.com/` devolvió 403 días enteros mientras
  google.com daba 200 y el 2026-10-25, con curl 200, la corrida publicó
  5/5 — el 403 era bloqueo a la IP de salida, no caída del servicio ni
  fallo de credenciales. La regla de ese servicio vive en
  `skills/puerta-pinterest-pin/SKILL.md` (§ «Salud previa a publicar»).
- Anti-patrón: convertir una sonda no representativa en puerta — la
  corrida se detiene días enteros ante un servicio que sí responde.

## P2 — Checkpoints con resume

El avance del lote vive en un archivo de estado versionado (JSON),
actualizado **inmediatamente después de cada unidad de trabajo**
(diseño, pin, listing — la unidad que corresponda). Si el worker muere
a la mitad, la siguiente corrida lee el estado y **retoma donde quedó**,
nunca repite trabajo hecho.

- Esquema ejemplo: `{"lote_actual": {"fecha": "YYYY-MM-DD",
  "unidades": [ids], "fase_a_ok": [ids], "fase_b_ok": [ids]}}`.
- El archivo de estado es **estado de ejecución**: se gitignorea, no se
  versiona (como `data/cola-pins/`).
- Anti-patrón: "la próxima corrida lo rehace todo" o depender de que un
  humano recuerde qué quedó a medias.

## P3 — Reintentos acotados con escalado

Un fallo externo no pierde el día, pero tampoco reintenta en bucle.
Protocolo:

1. Al fallar el health-check (o una fase por causa externa), programa
   UN reintento en ~2 horas (runonce), no al día siguiente.
2. Lleva el contador en el archivo de checkpoints
   (`salud: {fecha, reintentos_hoy}`); tope: 3 intentos/día.
3. Agotados los intentos: reporta "caído todo el día" y escala al dueño;
   el ciclo normal lo retoma mañana.

- El reintento relee el procedimiento canónico (no duplica
  instrucciones) y respeta P2.
- Anti-patrón: reintentar sin tope, o dormir horas dentro de la corrida.

## P4 — Lo verificable va en código, no en criterio

Complemento (doctrina existente): las validaciones mecánicas son
scripts deterministas con veredicto PASS/FAIL (gates), no juicio del
worker. El worker decide; el gate verifica. Un gate que nadie corre no
existe: cada fase corre su gate en orden y se detiene en FAIL.

---
*Promovido a `~/AGENTS.md` el 2026-10-16 (regla de promoción: lección
independiente del dominio).*
