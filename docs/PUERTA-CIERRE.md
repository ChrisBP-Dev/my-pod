# Puerta de cierre — checklist obligatorio para declarar cerrada una mejora

**Qué es:** la puerta que toda mejora, fase o consolidación de
My POD debe pasar ANTES de declararse cerrada (Programa
Estándar My POD, frente F6, 2026-10-23). Nace de la causa común
que el dueño detectó ese día: **cerrábamos mejoras por su
funcionamiento, no por su colocación** — funcionaba, pero
quedaba mal puesto, con valores fosilizados, fugas a la tienda
o huecos sin dueño. Funcionar ya no basta.

Ninguna mejora se declara cerrada con un ítem sin verificar.
Cada ítem se verifica con evidencia (comando, salida, lectura),
no con la palabra de quien la ejecutó.

## Checklist

### (a) Auditoría de colocación
- [ ] Cada pieza nueva o tocada pasó la **prueba de quitar el
  dominio/tienda**: si sobrevive sin el vocabulario de ESTA
  tienda (su id, su nombre, sus precios, sus productos, su
  nicho), es mecanismo y vive en el sistema (skill/doc/script
  de la app); si muere sin ese vocabulario, es **valor de
  ficha** y vive en los datos de la tienda.
- [ ] Barrido de fugas: grep de los identificadores de la
  tienda activa (shop id, nombre, precios, productos, nicho)
  en skills y scripts — cada resultado clasificado:
  mecanismo / ejemplo ficticio etiquetado / histórico fechado
  / fixture / **fuga** (las fugas se corrigen en la misma
  corrida; defaults funcionales con datos de una tienda =
  cero tolerancia).
- [ ] Los valores que la mejora consume desde la ficha están
  en `docs/INVENTARIO-VALORES-FICHA.md` (o se agregan en esta
  corrida), cada uno con su estado y su paso productor.

### (b) Barrido de huecos hacia adelante
- [ ] ¿Qué deja esta mejora **vivo en superficies reales**
  (datos sembrados, estados intermedios, defaults, instancias
  de ensayo, valores provisionales)? Cada remanente con su
  ciclo de vida completo declarado: quién lo retira, cuándo
  y verificado cómo. Ninguna unidad cierra con remanentes
  vivos sin declarar en superficies canónicas.
- [ ] ¿Qué pasa si el flujo corre y falta algo (un valor sin
  configurar, un catálogo ausente, una conexión caída)? El
  comportamiento ante el hueco está definido en el sistema:
  se detiene y reporta qué falta y dónde se llena — nunca
  inventa el valor ni usa un default en silencio.
- [ ] Si la mejora toca un flujo que otros consumen, los
  consumidores quedaron alineados a la forma nueva (ningún
  consumidor operando con la forma vieja en silencio).

### (c) Consumo de líneas vigentes y registros vivos (2026-10-27, recalibración de alineación)
- [ ] Si la mejora toca la ficha, una directriz o un flujo de la
  tienda: `scripts/verificar-consumo-lineas-tienda.py --shop
  <id>` en PASS — toda línea vigente de la ficha llegó a su
  asignación o declaró su pausa (el hueco fundacional: la
  personalización decidida no llegó a ningún artefacto).
- [ ] El `registro-flujo.md` de la tienda quedó actualizado en
  esta corrida si hubo decisión/veredicto del dueño, y el
  `INVENTARIO-VALORES-FICHA.md` refleja el estado real de los
  valores tocados (ambos registros se abandonaron una vez —
  2026-10-19→27 — sin que ninguna puerta lo midiera).

### (c2) Estados de los valores de ficha que toca
- [ ] Todo valor de ficha que la mejora crea, mueve o consume
  quedó con su **estado** declarado: `configurado` (decidido
  por el dueño en su flujo) / `provisional` (sembrado sin su
  pase — con su procedencia escrita) / `sin_configurar`.
- [ ] Ningún valor provisional se presenta como decisión del
  dueño en ningún texto, reporte o doc.

### (d) Suites en verde
- [ ] Las suites de regresión de cada skill tocado corren en
  verde, con la salida registrada en el reporte de cierre.
- [ ] Si la mejora cambia un comportamiento que una suite
  cubría, la suite se actualizó en la misma corrida (el caso
  viejo no sobrevive como expectativa muerta).

### (e) Colocación verificada de artefactos
- [ ] Todo script, herramienta o medición que la mejora usa
  como puerta o mecanismo **vive físicamente dentro del repo
  que la declara** (verificado: los `scripts/` nombrados por
  cada skill tocado existen). Nada vive solo en el entorno de
  quien ejecutó (/tmp, venvs sueltos, su memoria).
- [ ] Todo artefacto que calibra algo (fixtures, sets de
  prueba, mediciones) quedó archivado en el repo el mismo
  día.

### Cierre administrativo
- [ ] Versiones y CHANGELOGs de cada skill tocado,
  actualizados en la misma corrida.
- [ ] Commits en el repo que toca (sistema vs datos,
  separación D1), empujados y verificados con
  `git status -sb` (sin «ahead») — nunca con la cola de la
  salida de un push.
- [ ] El reporte de cierre declara: qué se hizo, la evidencia
  de cada ítem de esta puerta, y los pendientes que quedan
  (con su dueño y su momento) — un pendiente declarado es
  válvula, no ruta: solo procede tras el intento real o
  porque el paso lo declara de otro paso.
