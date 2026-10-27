# Diseño — Mecanismo de decisiones estratégicas de tienda (F1)

**Unidad:** Recalibración de My POD, F1 · **Fecha:** 2026-10-27 ·
**Estado: SUPERSEDIDO el 2026-10-27 por `docs/AUDITORIA-ALINEACION-RAMELI-2026-10-27.md`** (pedido del dueño: auditar primero contra Rameli; el remedio aquí inventaba un registro paralelo a hogares que el framework y la app ya asignan). Se conserva como historia fechada; NO es el plan vigente.
Rama: `recalibracion-decisiones-tienda` (nada fusiona sin su palabra).

## 1. El hueco, verificado hoy (no teórico)

El validador pasa en verde (`rameli validar`: 0 fallos, 0 avisos,
9 skills) y aun así el sistema perdió un foco que el dueño repitió:

- La personalización es técnicamente viable desde el 2026-10-20 y el
  dueño ordenó un piloto; pero su estado «canónico» vive en
  `config-propuestas.json → personalizados.estado`, es decir, dentro
  de la **salida semanal** de la estratega (vigencia 7 días). Una
  decisión permanente guardada en un artefacto semanal **caduca cada
  semana** y la siguiente corrida puede omitirla en silencio.
- `config.json → personalizacion` (la ficha) no declara el estado:
  es un puntero al artefacto semanal. La jerarquía está invertida —
  la ficha debería mandar y la directriz semanal obedecerla.
- `config-propuestas.json` vigente declara
  `personalizados.cupo_en_flujo_diario = 0`: el foco existe en la
  conversación y en el piloto, pero el contrato que lee el cron dice
  cero. Nadie mintió; simplemente ningún mecanismo cruza «foco
  declarado por el dueño» contra «cupo en el contrato».
- La investigación 2026-10-26 vuelve a **proponer** la personalización
  (PROP-INV-2026-10-26-04, no aplicada) porque no lee un registro de
  «ya decidido»: lo decidido y lo propuesto viven en el mismo plano
  de prosa y se re-proponen en bucle.
- La palabra «bordado» no aparece en `config.json`. Su doctrina
  técnica (fuente plana, colores sólidos, sin degradados/sombras/
  textura de puntadas, máx. 6 hilos) vive dispersa en el porqué de
  p070/p071 y en notas — ningún consumidor la lee de un lugar.
- Solo `puerta-arte-propuesta` declara el camino de lectura canónica
  de registros (`registros-datos.py pull` antes de leer). Los demás
  skills lectores (`publicador-lote`, `publicar-printify-etsy`,
  `paquete-listing-etsy`, `puerta-pinterest-pin`,
  `conectar-etsy-api`) no lo declaran: leen la copia física como si
  fuera la realidad. La fricción de hoy (copia vieja de
  `decisiones.json` casi pisada; la guarda repo-primero lo detuvo)
  nació de ese hueco.

**Causa raíz (doctrina del dueño, 2026-10-24):** no es un caso, es
el flujo: no existe una capa de «decisión estratégica de tienda» con
hogar, esquema y consumidores declarados. Hay ficha (valores
calibrados), hay directriz semanal (táctica) y hay propuestas
(prosa) — y nada que obligue a que las tres digan lo mismo.

## 2. Principio del mecanismo

Tres capas, tres tiempos, sin mezcla:

| Capa | Tiempo | Hogar | Quién la cambia |
|---|---|---|---|
| **Decisión estratégica** | Permanente (hasta que el dueño la cambie) | Ficha de la tienda | Solo dale del dueño, registrado |
| **Directriz semanal** | 7 días | `direccion-tienda.md` + `config-propuestas.json` | La estratega, **obedeciendo** la capa 1 |
| **Propuesta** | Hasta su dale o descarte | Investigación / directriz §PROPUESTAS | Nace `sin_dale`; al dale, **sube** a la capa 1 y deja de proponerse |

La prueba de cada capa: si mañana la estratega re-emite su
directriz desde cero, las decisiones de la capa 1 siguen ahí y la
directriz nueva tiene que reflejarlas o fallar la puerta (§5).

## 3. Hogar y esquema (decisión de estructura #1, para su dale)

**Recomendación: bloque `decisiones_estrategicas` en el
`config.json` de la tienda (la ficha).** Es donde ya viven
`estrategia_precios` y `productos_aprobados`, es lo que el
`INVENTARIO-VALORES-FICHA.md` inventaría, y «la ficha declara; los
skills ejecutan». Alternativa descartada con motivo: un archivo
`decisiones-estrategicas.json` separado — diffs más limpios, pero
fragmenta la ficha en dos hogares y cada consumidor tendría dos
fuentes que cruzar; el hueco que cerramos nació de fuentes
dispersas, no de archivos grandes.

Esquema por decisión:

```json
{
  "id": "personalizacion",
  "tipo": "foco | metodo | doctrina | producto",
  "titulo": "Personalización (nombre + credencial, track single-P)",
  "estado": "operativa | piloto | pausada | propuesta_sin_dale | retirada",
  "dale": {"fecha": "2026-10-20", "origen": "prueba sandbox en vivo con el dueño; piloto single automático"},
  "vigencia": {"desde": "2026-10-20", "hasta": null},
  "cupo_minimo_en_flujo_diario": 2,
  "terminos": ["personaliz", "single-p", "nombre + credencial"],
  "doctrina_ref": "skills/estratega-tienda/SKILL.md §Personalizados + skills/publicar-printify-etsy/SKILL.md §Track Single-P",
  "consumidores": ["estratega-tienda", "propuestas-fase-a", "puerta-arte-propuesta", "publicar-printify-etsy"],
  "nota": "El MPL no soporta personalización: todo personalizado va por track single (decisión 2026-10-15)."
}
```

- `cupo_minimo_en_flujo_diario` es **piso, no techo** (decisión de
  estructura #2): la estratega puede asignar más en la semana; nunca
  menos sin registrar un `pausada` con dale. `null` para decisiones
  sin cupo (métodos/doctrinas).
- **Bordado = decisión propia, tipo `metodo`** (decisión de
  estructura #3): no es un sub-campo de personalización. Se cruzan
  (p070 es ambos) pero el bordado puede vivir sin personalizar y la
  personalización sin bordar (DTG). Su `doctrina_ref` apunta al canon
  técnico (fuente plana…) que F5 moverá a su hogar declarado en la
  puerta; su consumidor natural es `puerta-arte-propuesta`.
- `estado: propuesta_sin_dale` permite registrar una propuesta
  **como dato** (con su PROP-INV de origen) sin que ningún
  consumidor la ejecute: la puerta la trata como no-operativa y la
  investigación deja de re-proponerla porque ya está registrada.
- Cambiar `estado`, `cupo` o `vigencia` de una decisión es un acto
  del dueño: el skill que lo escribe registra `dale.fecha/origen`;
  sin dale, el escritor solo puede crear entradas `sin_dale`.

## 4. Productores y consumidores (se declara en cada skill)

| Skill / flujo | Lee (de la ficha) | Produce que otro lee |
|---|---|---|
| `estratega-tienda` | `decisiones_estrategicas` (entrada nueva obligatoria), `estrategia_precios`, ledger, investigaciones | `direccion-tienda.md` + `config-propuestas.json` con `decision_id` en cada tema/bloque que ejecuta una decisión; PROPUESTAS solo para lo `sin_dale` |
| Investigación semanal + trend scan (equipo) | `decisiones_estrategicas` — lo decidido NO se re-propone; lo nuevo nace como entrada `sin_dale` o PROP-INV que cita el `id` que crearía | `investigaciones/*.md` (insumo de la estratega) |
| Cron de propuestas / Fase A (worker) | `config-propuestas.json` (táctico) + la decisión citada en cada tema (doctrina y cupo) | Propuestas con `decision_id` y `metodo` (`dtg|bordado`) en el registro |
| `puerta-arte-propuesta` | La decisión y su `doctrina_ref` (en bordado: fuente plana, máx. 6 hilos…) + `config-propuestas` | Veredicto de puerta; entrega y recogida-aplicación |
| `publicar-printify-etsy` | `estado` de la decisión (Single-P solo si `operativa|piloto`) + ficha del producto | Drafts/listings |
| `onboarding-tienda` | — | **Produce el bloque** al abrir tienda (paso nuevo: cierra el hueco «sin paso» del inventario para este valor) |
| `estratega-pinterest` / `puerta-pinterest-pin` | Solo lectura indirecta: pins de listings cuyo registro cita la decisión | Cola de pins |

Y transversal, **camino de lectura canónica de registros** (se
declara en TODOS los skills que lean registros de la tienda, no
solo en los que escriben): antes de leer, `registros-datos.py pull`;
la copia física es caché; la realidad es el repo de datos.

## 5. La puerta de consistencia (el motor que faltaba)

Script nuevo `scripts/verificar-decisiones-tienda.py --shop <id>`
(sistema, no registro) + su paso en el cierre de la estratega, en el
arranqu
...[truncated 2071 chars]