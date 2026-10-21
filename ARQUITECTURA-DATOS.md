# Arquitectura de Datos — Pod Limpio

## Principio

Los datos se separan en **compartidos** (iguales para todos) y **por tienda**
(cada tienda gestiona lo suyo).

## Estructura

```
data/
  # COMPARTIDO — catálogo del sistema, igual para todos los usuarios
  productos/          # Fichas de producto (Gildan 18000...): área de impresión,
                      #   regla de colocación. Viene de Printify, no cambia por tienda.
  artes-print/        # Diseños del usuario (sus creaciones, reutilizables
                      #   en cualquier tienda).
  banco-keywords/     # Keywords (compartido).

  # POR TIENDA — todo lo que es operación de UNA tienda vive aquí
  tiendas/
    <tienda-id>/        # Ej: 29222324 (Tú Dale POD - Store)
      config.json        # Nombre, IDs de Printify/Etsy, precios,
                        #   calendario de descuentos, Share & Save.
      direccion-tienda.md  # Directriz semanal de la estratega (humano):
                        #   reparto, mix, precios, NO-hacer. Vigencia 7 días.
      config-propuestas.json  # Directriz semanal MÁQUINA (contrato
                        #   docs/CONTRATO-TIPO-PRODUCTO.md v1.0): tipo_lote
                        #   (mpl/single/mixto), componentes, temas, precios.
                        #   Lo escribe la estratega; lo lee el cron diario.
      registro-listings.json  # Registro de listings de la tienda
                        #   (propuestas, drafts, publicados, porqués).
      ledger-ventas.json  # Ledger de ventas y performance por listing.
      registro-flujo.md   # Estado de los flujos de la tienda.
      investigaciones/    # Investigación semanal y trend-scan, por fecha
                        #   (<fecha>-investigacion.md / <fecha>-tendencias.md).
                        #   La estratega lee las más recientes de aquí.
      revisiones/         # Actas de revisión (viernes), por fecha.
      estado-propuestas.json / estado-pinterest.json /
      estado-publicacion.json  # Checkpoints de ejecución (locales,
                        #   gitignoreados): viven junto a su tienda.
      modelos/           # (LEGADO del sistema de mockups propios,
                        #   eliminado 2026-10-14: sin uso vivo.)
                        # Modelos de ESTA tienda (5 canónicos)
        <modelo-id>/      # latina-30, afroamericana-38, latino-24, rubia-22, pelirroja-24
          referencia.webp  # Cara canónica
          ficha.json       # Descripción, edad aparente
      backgrounds/       # Backgrounds por TEMPORADA para ESTA tienda
        <temporada>-<año>.json  # Ej: navidad-2026.json
                        # Define ambiente, elementos, iluminación, qué transmite
      mockups/           # Mockups generados para ESTA tienda
        flatlays/
        dobladas/
        zooms/
        onmodel/
```

## Por qué así

- **Productos y bases**: son datos del catálogo (Printify). El Gildan 18000
  es el mismo para ti, para tu familiar, para cualquiera. No se duplican.
- **Artes**: son tus creaciones. Las puedes usar en varias tiendas.
- **Modelos**: son una decisión de PRESENTACIÓN de cada tienda. Tu tienda
  puede usar un modelo; la de tu familiar, otro. O pueden compartir — pero
  la gestión es por tienda.
- **Backgrounds**: igual que modelos, es presentación. Cada tienda define
  los suyos.
- **Mockups**: los genera Printify (flujo Printify-first, 2026-10-14);
  qué mockups se usan lo declara el esquema de la config de cada
  tienda. La app no genera mockups propios.

## Multi-usuario

Si le pasas el sistema a un familiar:
1. Se crea `data/tiendas/<nueva-tienda>/`.
2. Esa tienda tiene sus propios modelos y backgrounds.
3. Reutiliza el catálogo compartido (productos, artes del dueño).
4. Puede reutilizar tus artes o crear los suyos.

No hay "memoria local" misteriosa: todo está en `data/`, versionado y
accesible por la app.

## Alcance: qué es global y qué es por tienda

- **Global (catálogo del dueño):** `artes-print/` y `productos/`.
  Un diseño es creación del dueño, no de una tienda: la misma pieza
  puede venderse en varias tiendas SIN duplicar el binario (duplicar
  crearía dos "versiones finales" que divergen). La física del
  producto (área de impresión, proveedor) tampoco depende de la
  tienda. Por eso su ruta NO lleva tienda, deliberadamente.
- **Por tienda** (`data/tiendas/<id>/`): config/ficha (precios,
  esquema de mockups, calendario), estrategia y registro de flujo.
- **Hueco CERRADO (2026-10-19, decisión del dueño — no se espera a
  la segunda tienda):** `direccion-tienda.md`,
  `config-propuestas.json`, `registro-listings.json`,
  `ledger-ventas.json` y los `estado-*.json` vivían en la raíz de
  `data/` siendo operación de UNA tienda. Desde hoy viven en
  `data/tiendas/<id>/` (árbol de arriba), y todos los punteros
  vivos (skills, scripts, crons, ruta de lectura) apuntan ahí.
  Las investigaciones y las actas, que vivían solo en el log de
  memoria fuera de la app, tienen casa propia en la tienda
  (`investigaciones/`, `revisiones/`).
- **Escribir = commitear en la misma corrida (regla 2026-10-19;
  re-apuntada por la separación D1, 2026-10-21):**
  todo documento vivo de una tienda que un agente escriba
  (directriz, config, registro, ledger, investigación, acta) se
  commitea y pushea en la corrida que lo escribe, con verificación
  (sin "ahead" en el repo que toca). Un documento vivo sin commitear
  es trabajo sin respaldar y la causa raíz de registros divergentes
  entre frentes (caso real: la directriz del 2026-10-19 quedó un
  día entero sin guardar).
- **Mapa de repos (D1, 2026-10-21 — dos repos por aplicación):**
  el **repo del sistema** (este, `my-pod`) versiona solo sistema
  (skills, docs, scripts) y el esqueleto de datos (`.gitkeep` de
  los hogares declarados); los **registros de la instancia** —
  todo el texto bajo `data/`, por tienda y global — se versionan
  en el repo privado **`my-pod-datos`** (clon local en
  `~/workspace/my-pod-datos`), que es además su respaldo (D2).
  Los archivos físicos no se movieron: viven en `data/` como
  siempre y los flujos los leen ahí. El puente de versionado es
  `scripts/registros-datos.py`: `commit -m "<mensaje>"` sincroniza
  los registros físicos al repo de datos, commitea y pushea;
  `pull` restaura el árbol físico desde el repo de datos. Los
  medios no se versionan en ningún repo (política de instancia)
  y los checkpoints `estado-*.json` tampoco (son locales).
- **Versiones anteriores de documentos vivos:** la directriz y el
  config son UN archivo vivo por tienda; al rotar se sobrescriben
  y la versión anterior queda en el historial **del repo de
  datos** (ese es su archivo — no se crean copias
  `direccion-anterior.md` ni carpetas paralelas). Investigaciones
  y actas son fechadas por nombre y se acumulan en su carpeta:
  son el insumo histórico que la estratega lee, no se
  sobrescriben ni se borran al rotar.

## Ciclo de vida de los activos (2026-10-19, criterio del dueño)

1. **Un hogar canónico y un estado.** Todo activo vive en el hogar
   que esta arquitectura declara y tiene estado: *candidato*,
   *aprobado*, *en producción* o *descartado*. Un activo sin hogar
   o sin estado es un hallazgo, no un archivo más.
2. **El candidato vive en zona de descarte** (`candidatos-<id>/` o
   `tmp/`), identificable como tal. Al aprobarse, el ganador se
   MUEVE a su hogar canónico y los perdedores se borran en el mismo
   cierre.
3. **Descartado = borrado.** No se archiva "por si acaso": queda la
   huella en el registro (qué fue, quién lo descartó, cuándo) sin
   conservar el binario. Si se reintenta, se parte de cero.
4. **Lo en producción se referencia desde el registro** y se
   commitea: un binario canónico que solo existe en el disco local
   está en riesgo de pérdida, no "guardado". En la pasada de
   remanentes, todo binario sin referencia y sin estado se evalúa
   y se resuelve (mover, registrar o borrar), nunca se deja.
5. **El checkpoint muere con su flujo.** Al cerrar el flujo, su
   `estado-*.json` se resume en el registro o doc correspondiente
   y se borra; un checkpoint de un flujo cerrado es estado muerto
   que finge ser reanudable.
6. **El registro fechado se queda, declarado.** Cuando el detalle
   de una unidad cerrada es evidencia (una auditoría, una
   corrección), no vive como `estado-*` sino como registro con
   fecha en el nombre, y se declara aquí. Registros vigentes:
   `data/auditoria-2026-10-15/` (auditoría de mockups, histórica)
   y `data/registro-correccion-recortes-2026-10-19.json` (detalle
   de la corrección de recortes, resumida en
   `data/tiendas/29222324/registro-flujo.md`; su nombre original
   era `estado-correccion-recortes.json` y se renombró el
   2026-10-19, en la ejecución P5 de la auditoría de adopción,
   para que ningún lector lo crea un checkpoint reanudable).
