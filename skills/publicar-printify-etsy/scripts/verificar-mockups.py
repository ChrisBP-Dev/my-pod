#!/usr/bin/env python3
"""Puerta de cobertura de mockups (publicar-printify-etsy
v0.11.0, §M5).

Verifica un manifiesto de selección de mockups (producido por
`generar-manifiesto-mockups.py`) contra la entrada que lo
originó: los colores habilitados FINALES de cada item (los que
el dueño dejó en su revisión §M2), el catálogo canónico de
tomas de cada producto y los pesos de la composición.

Sin PASS de esta puerta, §M7 (publicar) NO corre. Si falla,
corrige el WORKER re-seleccionando en la fuente (regenerar el
manifiesto con el algoritmo), jamás manipulando el manifiesto
para pasar la medición — misma doctrina que la puerta de
video (incidente p046).

Chequeos (modo fixture, `--desde-json` = la misma entrada del
generador; el cruce contra lo marcado en Printify llega con el
modo en vivo del piloto de publicación):
 1. Conteo: espacios visuales por producto = peso declarado;
    tablas de tallas = 1 por producto; total = total_imagenes.
 2. Imagen principal: la posición 1 es del producto principal
    de la composición, con la toma de rol principal de
    prioridad 1 de su catálogo y su color prioritario.
 3. Garantías mínimas por producto: ≥2 tomas con modelo
    (principal/secundaria) si tiene ≥2 espacios; ≥1 plana si
    tiene ≥3; si sus colores traen claros y oscuros y tiene
    ≥2 espacios, al menos un color claro y uno oscuro
    aparecen en sus espacios.
 4. Ninguna toma CON MODELO (principal/secundaria) repetida
    en dos colores ni dos veces en el mismo item (la plana
    sí puede repetirse en otro color: evidencia p046).
 5. Ninguna toma fuera del catálogo de su producto; ninguna
    toma de su lista `tomas_a_evitar`.
 6. Los colores vendidos sin representación visual están
    DECLARADOS en el manifiesto, exactamente: ni uno sin
    declarar, ni uno declarado que sí aparece.

Exit 0 = PASS. Exit 1 = FAIL (motivos legibles, uno por
línea). Exit 2 = error de uso / archivos ilegibles.

Uso:
    verificar-mockups.py --manifiesto manifiesto.json \
                         --desde-json entrada.json
"""
import argparse
import json
import sys

ROLES_MODELO = ("principal", "secundaria")


def cargar(ruta):
    with open(ruta) as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifiesto", required=True)
    ap.add_argument("--desde-json", required=True,
                    help="entrada fixture (la misma del generador)")
    args = ap.parse_args()
    try:
        manifiesto = cargar(args.manifiesto)
        entrada = cargar(args.desde_json)
    except (OSError, json.JSONDecodeError) as e:
        print(f"error de uso: {e}")
        return 2

    motivos = []
    items = {it["producto"]: it for it in entrada["items"]}
    espacios = manifiesto.get("espacios", [])
    visuales = [s for s in espacios if s.get("rol") != "tabla_tallas"]
    tablas = [s for s in espacios if s.get("rol") == "tabla_tallas"]
    # Sin default quemado (Programa Estándar F3, 2026-10-23): el
    # presupuesto viene de la ficha vía la entrada; si falta, la
    # puerta falla nombrándolo (antes asumía 10 en silencio,
    # residual detectado en la prueba de frío F7).
    total_esperado = entrada.get("total_imagenes")
    if total_esperado is None:
        motivos.append("la entrada no declara `total_imagenes` "
                       "(presupuesto de la ficha de la tienda); "
                       "la puerta no asume ningún total")
    tablas_esperadas = entrada.get("tabla_tallas_por_producto", 1)

    # 1. Conteo
    if len(espacios) != total_esperado:
        motivos.append(f"conteo total: {len(espacios)} espacios, "
                       f"esperados {total_esperado}")
    for prod, item in items.items():
        n = sum(1 for s in visuales if s["producto"] == prod)
        if n != item["espacios_visuales"]:
            motivos.append(f"{prod}: {n} espacios visuales, "
                           f"esperados {item['espacios_visuales']} "
                           f"(peso de la composición)")
        nt = sum(1 for s in tablas if s["producto"] == prod)
        if nt != tablas_esperadas:
            motivos.append(f"{prod}: {nt} tablas de tallas, "
                           f"esperadas {tablas_esperadas}")
    principal = next((it for it in entrada["items"]
                      if it.get("rol_en_listing") == "principal"), None)
    if principal is None:
        motivos.append("la entrada no declara producto principal")
        principal = entrada["items"][0] if entrada["items"] else {}

    catalogos = {}
    for prod, item in items.items():
        cat = item.get("catalogo") or {}
        catalogos[prod] = {
            "tomas": {t["id"]: t for t in cat.get("tomas", [])},
            "evitar": {t["id"] for t in cat.get("tomas_a_evitar", [])},
        }

    # 2. Imagen principal — pool primario ROTATIVO (calibración
    # del dueño 2026-10-26): la esperada es la toma del pool
    # según la `rotacion` de la entrada, no siempre la prioridad 1.
    if espacios:
        p1 = espacios[0]
        cat_p = catalogos.get(principal.get("producto"), {"tomas": {}})
        principales = [t for t in cat_p["tomas"].values()
                       if t.get("rol") == "principal"]
        principales.sort(key=lambda t: t.get("prioridad", 99))
        rot = int(principal.get("rotacion", 0)) % len(principales) \
            if principales else 0
        esperada = principales[rot]["id"] if principales else None
        if p1.get("producto") != principal.get("producto"):
            motivos.append(
                f"imagen principal: es de {p1.get('producto')}, "
                f"debe ser del producto principal "
                f"({principal.get('producto')})")
        if p1.get("rol") != "principal" or p1.get("toma_id") != esperada:
            motivos.append(
                f"imagen principal: toma {p1.get('toma_id')} "
                f"(rol {p1.get('rol')}), debe ser {esperada} "
                f"(pool primario, rotación {rot})")
        if p1.get("color") != principal.get("color_prioritario"):
            motivos.append(
                f"imagen principal: color {p1.get('color')}, debe "
                f"ser el prioritario "
                f"({principal.get('color_prioritario')})")
    else:
        motivos.append("manifiesto sin espacios")

    # 3–5. Por producto
    for prod, item in items.items():
        cat = catalogos[prod]
        propios = [s for s in visuales if s["producto"] == prod]
        E = item["espacios_visuales"]
        n_modelo = sum(1 for s in propios
                       if s.get("rol") in ROLES_MODELO)
        if E >= 2 and n_modelo < 2:
            motivos.append(f"{prod}: garantías mínimas — solo "
                           f"{n_modelo} tomas con modelo "
                           f"(mínimo 2 con {E} espacios)")
        # La plana solo se exige si el catálogo del producto la
        # declara (calibración 2026-10-26: la playera no usa
        # plana por decisión del dueño; su garantía es el pool).
        declara_plana = any(t.get("rol") == "plana"
                            for t in cat["tomas"].values())
        if E >= 3 and declara_plana and not any(
                s.get("rol") == "plana" for s in propios):
            motivos.append(f"{prod}: garantías mínimas — ninguna "
                           f"toma plana con {E} espacios")
        tonos = {c["nombre"]: c.get("tono")
                 for c in item["colores"]}
        if E >= 2 and "claro" in tonos.values() \
                and "oscuro" in tonos.values():
            tonos_vistos = {tonos.get(s.get("color"))
                            for s in propios}
            if "claro" not in tonos_vistos \
                    or "oscuro" not in tonos_vistos:
                motivos.append(
                    f"{prod}: garantías mínimas — el set trae "
                    f"claros y oscuros pero los espacios no "
                    f"muestran ambos tonos")
        vistos_modelo = {}
        for s in propios:
            tid = s.get("toma_id")
            if tid in cat["evitar"]:
                motivos.append(f"{prod}: toma a evitar usada: {tid}")
            if tid not in cat["tomas"]:
                motivos.append(f"{prod}: toma fuera de catálogo: "
                               f"{tid}")
            if s.get("rol") in ROLES_MODELO:
                if tid in vistos_modelo:
                    motivos.append(
                        f"{prod}: pose/modelo repetida — la toma "
                        f"{tid} aparece en "
                        f"{vistos_modelo[tid]} y en {s.get('color')}")
                vistos_modelo[tid] = s.get("color")

    # 6. Colores sin representación: declarados = reales
    declarados = {(d["producto"], d["color"])
                  for d in manifiesto.get(
                      "colores_sin_representacion", [])}
    reales = set()
    for prod, item in items.items():
        representados = {s.get("color") for s in visuales
                         if s["producto"] == prod}
        for c in item["colores"]:
            if c["nombre"] not in representados:
                reales.add((prod, c["nombre"]))
    for prod, color in sorted(reales - declarados):
        motivos.append(f"{prod}: color sin representación NO "
                       f"declarado en el manifiesto: {color}")
    for prod, color in sorted(declarados - reales):
        motivos.append(f"{prod}: color declarado sin "
                       f"representación pero sí aparece: {color}")

    if motivos:
        print("RESULTADO: FAIL — puerta de cobertura de mockups")
        for m in motivos:
            print(f" - {m}")
        return 1
    print(f"RESULTADO: PASS — {len(visuales)} espacios visuales, "
          f"{len(tablas)} tablas, "
          f"{len(declarados)} colores sin representación "
          f"declarados; imagen principal correcta")
    return 0


if __name__ == "__main__":
    sys.exit(main())
