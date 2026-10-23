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
  "total_imagenes": 10,
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

Algoritmo (determinista, §M5 del skill):
 1. Orden de colores por item: primero el color prioritario
    (dato de entrada: juicio de contraste del worker +
    rotación de héroes del lote); después alternando tonos
    (opuesto al del prioritario primero) conservando el orden
    de entrada dentro de cada tono.
 2. Garantías mínimas por item, en este orden: toma de rol
    principal en el color prioritario; toma de rol secundaria
    (pose distinta) en el siguiente color; y una plana, cuyo
    color sale de la cobertura (si queda un color sin
    representar, la plana lo cubre; si todos están
    representados, va en el prioritario). Corrección
    2026-10-23: antes la plana iba siempre en el prioritario
    y en items de 3 espacios dejaba un tercer color sin foto
    pudiendo entrar (piloto seco p058).
 3. Cobertura por turnos: cada color aún no representado
    recibe un espacio, rotando los roles de relleno
    (plana → doblada-decorada → detalle).
 4. Espacios restantes: se llenan rotando roles de relleno y
    colores en orden de prioridad, sin repetir par (toma,
    color) y sin repetir jamás una toma CON MODELO (roles
    principal/secundaria) en otro color.
 5. Sustitución reglada: si el rol pedido no tiene toma
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
    usados_modelo = set()   # toma con modelo: única en TODO el item
    usados_par = set()      # (toma, color): nunca se repite
    slots = []
    sustituciones = []

    def elegir(roles_preferidos, color):
        for rol in roles_preferidos:
            for toma in por_rol(catalogo, rol):
                tid = toma["id"]
                if tid in evitar or (tid, color) in usados_par:
                    continue
                if rol in ROLES_MODELO and tid in usados_modelo:
                    continue
                usados_par.add((tid, color))
                if rol in ROLES_MODELO:
                    usados_modelo.add(tid)
                return toma, rol
        return None, None

    def agregar(roles_preferidos, color, motivo_rol):
        toma, rol_real = elegir(roles_preferidos, color)
        if toma is None:
            return False
        if rol_real != roles_preferidos[0]:
            sustituciones.append(
                {"producto": producto, "color": color,
                 "rol_pedido": roles_preferidos[0],
                 "rol_usado": rol_real, "toma": toma["id"],
                 "motivo": "sin toma disponible del rol pedido; "
                           "se bajó al siguiente rol de preferencia"})
        slots.append({"producto": producto, "color": color,
                      "toma_id": toma["id"],
                      "camera_label": toma.get("camera_label"),
                      "rol": rol_real, "uso": motivo_rol})
        return True

    # 1–2. Garantías: principal y secundaria (poses distintas)
    if not agregar(["principal"], orden[0], "garantia-principal"):
        raise ValueError(f"{producto}: no se pudo asignar la toma "
                         f"principal")
    if E >= 2:
        segundo = orden[1] if len(orden) > 1 else orden[0]
        agregar(["secundaria", "principal"], segundo,
                "garantia-secundaria")
    # 3. Garantía: una plana por item; su color sale de la
    # cobertura — si queda un color sin representar, la plana
    # lo cubre; si todos están representados, va en el
    # prioritario. (Corrección 2026-10-23, piloto seco p058.)
    if E >= 3:
        representados = {s["color"] for s in slots}
        sin_rep = [c for c in orden if c not in representados]
        color_plana = sin_rep[0] if sin_rep else orden[0]
        agregar(["plana"], color_plana, "garantia-plana")
    # 4. Cobertura por turnos de colores no representados
    i_relleno = 0
    for color in orden:
        if len(slots) >= E:
            break
        if any(s["color"] == color for s in slots):
            continue
        roles = list(RELLENO[i_relleno % len(RELLENO):]) + \
            list(RELLENO[:i_relleno % len(RELLENO)]) + ["secundaria"]
        if agregar(roles, color, "cobertura"):
            i_relleno += 1
    # 5. Relleno de espacios restantes
    i_color = 0
    while len(slots) < E:
        color = orden[i_color % len(orden)]
        roles = list(RELLENO[i_relleno % len(RELLENO):]) + \
            list(RELLENO[:i_relleno % len(RELLENO)]) + \
            ["secundaria", "principal"]
        if agregar(roles, color, "relleno"):
            i_relleno += 1
            i_color += 1
        else:
            i_color += 1
            if i_color > len(orden) * (len(RELLENO) + 2):
                break  # no hay combinación (toma, color) disponible
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
    total_imagenes = entrada.get("total_imagenes", 10)
    tablas_por_producto = entrada.get("tabla_tallas_por_producto", 1)

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
                    "producto": item["producto"], "color": None,
                    "toma_id": tablas[0]["id"],
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
                        "(publicar-printify-etsy v0.11.0, §M5)",
        "modo": "fixture — la disponibilidad de cada toma por "
                "color en Printify NO está verificada en este "
                "modo (llega con el piloto de publicación)",
        "diseno": entrada.get("diseno"),
        "total_imagenes": total_imagenes,
        "items": [{"producto": it["producto"],
                   "rol_en_listing": it.get("rol_en_listing"),
                   "espacios_visuales": it["espacios_visuales"],
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
