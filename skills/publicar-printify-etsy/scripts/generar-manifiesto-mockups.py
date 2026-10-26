#!/usr/bin/env python3
"""Generador del manifiesto de selección de mockups
(publicar-printify-etsy v0.11.0, §M5).

La selección de mockups la hace el WORKER con este algoritmo
determinista — nunca el dueño, nunca los defaults que Printify
deje marcados. Dadas las entradas (colores FINALES del borrador,
post-revisión del dueño §M2; catálogo canónico de tomas de cada
producto; pesos de la composición), produce el manifiesto JSON:
cada espacio del listing con producto/color/toma/rol, los
colores vendidos sin representación visual DECLARADOS con su
motivo, y las sustituciones regladas.

MODO: por ahora SOLO fixture (`--desde-json`). El modo en vivo
(leer el borrador por API y confirmar disponibilidad de cada
toma por color en Printify) llega con el piloto de publicación;
sin él, la disponibilidad por color no se verifica y el
manifiesto lo declara en su campo `modo`.

Formato de la entrada (`--desde-json`):
{
  "diseno": "p000",
  "total_imagenes": "<el de la ficha de la tienda, ≤20>",
  "tabla_tallas_por_producto": 1,
  "items": [
    {"producto": "gildan-18000",
     "rol_en_listing": "principal" | "secundario",
     "espacios_visuales": 5,
     "color_prioritario": "Navy",
     "colores": [{"nombre": "Navy", "tono": "oscuro"}, ...],
     "catalogo": {"tomas": [ {id, camera_label, rol, prioridad} ],
                  "tomas_a_evitar": [ {id, ...} ]}}
  ]
}
El `catalogo` de cada item es la sección `tomas_preferidas` del
producto (data/productos/<producto>.json) + su `tomas_a_evitar`.

Algoritmo (determinista, §M5 del skill). Modelo v2 —
POOL PRIMARIO ROTATIVO (calibración del dueño 2026-10-26,
reemplaza al héroe fijo + garantías de la v1):
 1. Orden de colores por item: primero el color prioritario
    (dato de entrada: juicio de contraste del worker +
    rotación de héroes del lote); después alternando tonos
    (opuesto al del prioritario primero) conservando el orden
    de entrada dentro de cada tono.
 2. Héroe: la primera toma del POOL primario (rol principal,
    ordenado por prioridad) ROTADO por `rotacion` de la
    entrada (índice del diseño en su lote), en el color
    prioritario. Sin héroe fijo y sin color fijo.
 3. Distribución del pool: cada toma restante del pool, en
    el siguiente color del orden — las favoritas se reparten
    entre los colores antes de repetir una toma en otro color.
 4. Plana (solo si el catálogo la declara): cubre el primer
    color sin representar; si todos están, va en el prioritario.
 5. Cobertura y relleno: colores sin representar con tomas
    aún no usadas; al final la extensión (rol secundaria) y
    la plana en otros colores (la plana sí puede repetirse en
    otro color: evidencia p046). Sin repetir jamás el par
    (toma, color) ni una toma no-plana en dos colores.
 6. Sustitución reglada: si el rol pedido no tiene toma
    disponible, se baja al siguiente rol de la lista de
    preferencia y la sustitución queda registrada.
 6. Al final, 1 tabla de tallas por producto.
Si un producto no trae catálogo, o el catálogo no tiene toma
de rol principal / tabla de tallas, el generador se DETIENE
(exit 2) y reporta: producto sin catálogo no entra a
producción (§M5).

Uso:
    generar-manifiesto-mockups.py --desde-json entrada.json
                                  [--salida manifiesto.json]
Sin --salida, el manifiesto va a stdout.
"""
import argparse
import json
import sys

ROLES_MODELO = ("principal", "secundaria")
RELLENO = ("plana", "doblada-decorada", "detalle")


def ordenar_colores(item):
    colores = item["colores"]
    prio = item["color_prioritario"]
    nombres = [c["nombre"] for c in colores]
    if prio not in nombres:
        raise ValueError(f"color_prioritario {prio!r} no está en "
                         f"los colores habilitados de {item['producto']}")
    tono = {c["nombre"]: c.get("tono") for c in colores}
    resto = [n for n in nombres if n != prio]
    opuesto = "claro" if tono[prio] == "oscuro" else "oscuro"
    orden = [prio]
    buckets = {t: [n for n in resto if tono[n] == t] for t in
               ("claro", "oscuro", None)}
    turno = [opuesto, tono[prio]] if tono[prio] in ("claro", "oscuro") \
        else [None]
    # alterna opuesto / mismo tono hasta agotar; lo sin tono va al final
    while any(buckets[t] for t in turno):
        for t in turno:
            if buckets[t]:
                orden.append(buckets[t].pop(0))
    orden.extend(buckets[None])
    return orden


def por_rol(catalogo, rol):
    return sorted((t for t in catalogo.get("tomas", [])
                   if t.get("rol") == rol),
                  key=lambda t: t.get("prioridad", 99))


def generar_item(item):
    """Devuelve (slots_sin_posicion, sustituciones)."""
    producto = item["producto"]
    catalogo = item.get("catalogo") or {}
    if not catalogo.get("tomas"):
        raise ValueError(f"{producto}: sin catálogo de tomas "
                         f"(tomas_preferidas vacío o ausente) — "
                         f"producto sin catálogo no entra a producción")
    if not por_rol(catalogo, "principal"):
        raise ValueError(f"{producto}: el catálogo no tiene toma de "
                         f"rol principal")
    evitar = {t["id"] for t in catalogo.get("tomas_a_evitar", [])}
    E = item["espacios_visuales"]
    orden = ordenar_colores(item)
    slots = []
    sustituciones = []

    # Modelo de selección v2 (calibración del dueño 2026-10-26):
    # POOL PRIMARIO ROTATIVO. El catálogo declara un pool de
    # tomas de rol principal (las favoritas del dueño); no hay
    # héroe fijo ni color fijo: el pool rota entre listings
    # según `rotacion` de la entrada (índice del diseño en su
    # lote) y las favoritas se reparten entre los colores antes
    # de repetir una toma en otro color.
    pool = por_rol(catalogo, "principal")
    rot = int(item.get("rotacion", 0)) % len(pool)
    pool_rot = pool[rot:] + pool[:rot]
    planas = por_rol(catalogo, "plana")
    extension = por_rol(catalogo, "secundaria")
    usados = set()       # (toma_id, color): nunca se repite
    usados_toma = set()  # toma ya usada (la plana sí puede repetirse en otro color)

    def agregar(toma, color, uso):
        tid = toma["id"]
        if tid in evitar or (tid, color) in usados:
            return False
        if toma.get("rol") != "plana" and tid in usados_toma:
            return False
        usados.add((tid, color))
        if toma.get("rol") != "plana":
            usados_toma.add(tid)
        slots.append({"producto": producto, "color": color,
                      "toma_id": tid,
                      "etiqueta_printify": toma.get("etiqueta_printify"),
                      "camera_label": toma.get("camera_label"),
                      "rol": toma.get("rol"), "uso": uso})
        return True

    # 1. Héroe: la primera toma del pool rotado, en el color
    # prioritario (que también rota por diseño vía la entrada).
    if not agregar(pool_rot[0], orden[0], "heroe-pool"):
        raise ValueError(f"{producto}: no se pudo asignar la toma "
                         f"del pool primario")
    # 2. Distribución del pool: cada toma restante del pool, en
    # el siguiente color del orden (favoritas × colores).
    i_color = 1
    for toma in pool_rot[1:]:
        if len(slots) >= E:
            break
        while i_color < len(orden) and \
                (toma["id"], orden[i_color]) in usados:
            i_color += 1
        if i_color >= len(orden):
            break
        if agregar(toma, orden[i_color], "pool-distribuido"):
            i_color += 1
    # 3. Plana (solo si el catálogo la declara): cubre el primer
    # color sin representar; si todos están, va en el prioritario.
    if planas and len(slots) < E:
        representados = {s["color"] for s in slots}
        sin_rep = [c for c in orden if c not in representados]
        color_plana = sin_rep[0] if sin_rep else orden[0]
        agregar(planas[0], color_plana, "garantia-plana")
    # 3b. Pool restante: si el pool tiene más tomas que colores,
    # las que no cupieron en la distribución entran en el primer
    # color con par libre — ninguna favorita queda fuera antes
    # de que otra se repita (la distribución va primero).
    for toma in pool_rot:
        if len(slots) >= E:
            break
        if toma["id"] in usados_toma:
            continue
        for color in orden:
            if agregar(toma, color, "pool-restante"):
                break
    # 4. Cobertura: cada color sin representar, con la primera
    # toma aún no usada (pool restante, plana, extensión).
    for color in orden:
        if len(slots) >= E:
            break
        if any(s["color"] == color for s in slots):
            continue
        for toma in pool_rot + planas + extension:
            if agregar(toma, color, "cobertura"):
                break
    # 4b. Cobertura tardía (corrección 2026-10-26, caso p061):
    # si un color sigue sin representar tras el paso 4 porque
    # ya no quedaban tomas sin usar, entra con la primera toma
    # del pool cuyo par con ese color esté libre. La cobertura
    # de colores manda sobre cualquier repetición.
    if len(slots) < E:
        representados = {s["color"] for s in slots}
        for color in orden:
            if len(slots) >= E:
                break
            if color in representados:
                continue
            for toma in pool_rot:
                tid = toma["id"]
                if tid in evitar or (tid, color) in usados:
                    continue
                usados.add((tid, color))
                usados_toma.add(tid)
                slots.append({"producto": producto, "color": color,
                              "toma_id": tid,
                              "etiqueta_printify":
                                  toma.get("etiqueta_printify"),
                              "camera_label": toma.get("camera_label"),
                              "rol": toma.get("rol"),
                              "uso": "cobertura"})
                representados.add(color)
                break
    # 5. Relleno: la extensión (rol secundaria — p. ej. la
    # Lifestyle de extensión) y la plana en otros colores.
    for toma in extension + planas:
        if len(slots) >= E:
            break
        for color in orden:
            if len(slots) >= E:
                break
            agregar(toma, color, "relleno")
    # 6. Repetición en segundo color (criterio del dueño
    # 2026-10-26): agotadas las tomas sin usar, las favoritas
    # SÍ pueden repetirse en un color distinto — el presupuesto
    # real (techo de plataforma) manda sobre la unicidad; lo
    # que nunca se repite es el par (toma, color). Para este
    # paso se levanta la unicidad por toma, no la del par.
    if len(slots) < E:
        # Round-robin entre tomas: cada pasada le da a cada
        # favorita su siguiente color libre antes de que alguna
        # acumule un tercero.
        progreso = True
        while len(slots) < E and progreso:
            progreso = False
            for toma in pool_rot + extension:
                if len(slots) >= E:
                    break
                tid = toma["id"]
                if tid in evitar:
                    continue
                for color in orden:
                    if (tid, color) in usados:
                        continue
                    usados.add((tid, color))
                    slots.append({"producto": producto,
                                  "color": color,
                                  "toma_id": tid,
                                  "etiqueta_printify":
                                      toma.get("etiqueta_printify"),
                                  "camera_label":
                                      toma.get("camera_label"),
                                  "rol": toma.get("rol"),
                                  "uso": "favorita-segundo-color"})
                    progreso = True
                    break
    return slots, sustituciones, orden


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--desde-json", required=True,
                    help="entrada fixture (formato en el docstring)")
    ap.add_argument("--salida",
                    help="ruta del manifiesto (default: stdout)")
    args = ap.parse_args()

    with open(args.desde_json) as f:
        entrada = json.load(f)
    # El presupuesto de fotos lo declara LA FICHA de la tienda
    # (calibración visual de onboarding-tienda), con techo de
    # plataforma 20 (Etsy, desde ago-2025). Sin total declarado
    # no hay default: el generador se detiene (Programa
    # Estándar My POD F3, 2026-10-23 — antes el default quemado
    # era 10, el esquema propio de una tienda).
    total_imagenes = entrada.get("total_imagenes")
    if total_imagenes is None:
        print("DETENIDO: la entrada no declara `total_imagenes` "
              "— el presupuesto de fotos se lee de la ficha de "
              "la tienda (mpl.esquema_mockups), no tiene default.")
        return 2
    if total_imagenes > 20:
        print(f"DETENIDO: total_imagenes={total_imagenes} supera "
              f"el techo de plataforma (20 fotos por listing en "
              f"Etsy desde ago-2025).")
        return 2
    tablas_por_producto = entrada.get("tabla_tallas_por_producto", 1)
    # Semántica declarada del total (corrección 2026-10-24,
    # hallazgo P3 de la prueba de frío): `total_imagenes` es la
    # META EXACTA de la ficha = suma de los espacios visuales de
    # los items + las tablas de tallas. Si no cuadra, la ficha es
    # inconsistente y el generador se detiene AQUÍ, con el
    # desglose — nunca genera de menos y deja que la puerta
    # falle tarde por conteo.
    suma_espacios = sum(int(i.get("espacios_visuales", 0))
                        for i in entrada["items"])
    tablas_total = tablas_por_producto * len(entrada["items"])
    if total_imagenes != suma_espacios + tablas_total:
        print(f"DETENIDO: ficha inconsistente — total_imagenes="
              f"{total_imagenes} pero los espacios visuales suman "
              f"{suma_espacios} y las tablas {tablas_total} "
              f"(esperado {suma_espacios + tablas_total}). Corrige "
              f"la ficha (pesos o total) en su paso de calibración; "
              f"el generador no elige por la tienda.")
        return 2

    espacios = []
    sustituciones = []
    sin_representacion = []
    try:
        for item in entrada["items"]:
            slots, subs, orden = generar_item(item)
            espacios.extend(slots)
            sustituciones.extend(subs)
            representados = {s["color"] for s in slots}
            for color in orden:
                if color not in representados:
                    sin_representacion.append({
                        "producto": item["producto"], "color": color,
                        "motivo": "sin espacios tras garantías mínimas "
                                  "y cobertura por turnos "
                                  f"(espacios_visuales="
                                  f"{item['espacios_visuales']})"})
        # tablas de tallas al final, una por producto
        for item in entrada["items"]:
            catalogo = item.get("catalogo") or {}
            tablas = por_rol(catalogo, "tabla_tallas")
            if not tablas and tablas_por_producto:
                raise ValueError(
                    f"{item['producto']}: el catálogo no tiene toma "
                    f"de rol tabla_tallas")
            for _ in range(tablas_por_producto):
                espacios.append({
                    "producto": item["producto"],
                    "color": item["color_prioritario"],
                    "toma_id": tablas[0]["id"],
                    "etiqueta_printify": tablas[0].get("etiqueta_printify"),
                    "camera_label": tablas[0].get("camera_label"),
                    "rol": "tabla_tallas", "uso": "tabla-de-tallas"})
    except ValueError as e:
        print(f"DETENIDO: {e}")
        return 2

    for i, s in enumerate(espacios, 1):
        s_ordenado = {"posicion": i}
        s_ordenado.update(s)
        espacios[i - 1] = s_ordenado

    manifiesto = {
        "version_formato": 1,
        "generado_por": "generar-manifiesto-mockups.py "
                        "(publicar-printify-etsy, §M5)",
        "modo": "fixture — la disponibilidad de cada toma por "
                "color en Printify NO está verificada en este "
                "modo (llega con el piloto de publicación)",
        "diseno": entrada.get("diseno"),
        "total_imagenes": total_imagenes,
        "items": [{"producto": it["producto"],
                   "rol_en_listing": it.get("rol_en_listing"),
                   "espacios_visuales": it["espacios_visuales"],
                   "rotacion": it.get("rotacion", 0),
                   "color_prioritario": it["color_prioritario"],
                   "colores_habilitados":
                       [c["nombre"] for c in it["colores"]]}
                  for it in entrada["items"]],
        "espacios": espacios,
        "colores_sin_representacion": sin_representacion,
        "sustituciones": sustituciones,
    }
    texto = json.dumps(manifiesto, indent=2, ensure_ascii=False)
    if args.salida:
        with open(args.salida, "w") as f:
            f.write(texto + "\n")
        print(f"manifiesto escrito en {args.salida}: "
              f"{len(espacios)} espacios · "
              f"{len(sin_representacion)} colores sin representación "
              f"declarados · {len(sustituciones)} sustituciones")
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
