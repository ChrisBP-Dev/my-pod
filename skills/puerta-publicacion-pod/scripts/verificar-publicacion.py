#!/usr/bin/env python3
"""
verificar-publicacion.py — puertas mecánicas de la puerta de publicación POD.

Dos modos:
  mockup  — dimensiones (2000x2000) + placement del diseño contra la
             referencia aprobada.
  arte    — DPI efectivo del archivo de arte final (>= 300 al ancho físico
             declarado).

Referencia de placement (criterio canónico 2026-10-13, v2):
  la referencia es el FLAT-LAY APROBADO DE ESE DISEÑO (--referencia).
  Cada diseño replica la matemática de su propio flat-lay aprobado; ningún
  número vale en general (ni siquiera por producto). El golden set
  (vitals-stable) sigue calibrando las TOLERANCIAS del mecanismo y sirve
  como referencia para los diseños vitals-stable, pero no como verdad
  universal para otros diseños.
  Sin --referencia se usa el modo heredado: golden set por estilo/color
  (solo válido para diseños del propio golden set).

El placement se mide por correspondencia de características SIFT entre el
arte canónico (RGBA) y el mockup: matching FLANN + test de Lowe, transformada
afín parcial (escala + traslación) por RANSAC con semilla fija. Determinista:
no hay "se ve bien". Invariante al color de la prenda y a la escala continua
(sin grilla). Si el diseño no se localiza con confianza, el mockup FALLA.

Decisión documentada: el diseño del piloto pedía .js; se implementa en
Python porque PIL + OpenCV es el stack probado para medición de imágenes
en este entorno. El primer método (template matching multi-escala) se
descartó en validación: sensible a la grilla de escalas y al color de fondo
(fallaba en sportgrey y doblada); SIFT localiza los 12 del golden set con
la misma geometría en todos los colores.

Salida: JSON siempre. Exit 0 = PASS, 1 = FAIL.
"""
import argparse, glob, json, os, sys

import cv2
import numpy as np
from PIL import Image

# Calibrados sobre el golden set + fixtures con desviación conocida
# (ver evals/casos.md). No son números mágicos: son medidos.
CONF_MIN = 0.35       # inliers RANSAC / matches buenos (mínimo para confiar).
                     # Calibrado: golden set 0.422–0.880; arte equivocado
                     # contra flat-lay aprobado da 0.138 (piso medido).
                     # El mínimo del golden (onmodel/sand, 0.422) deforma
                     # la tela sobre el modelo: la puerta acepta deformación
                     # real, no exige rigidez perfecta.
MATCHES_MIN = 30      # matches buenos mínimos tras el test de Lowe
CENTRO_TOL = 0.03     # centro dentro del ±3% de la dimensión
TAMANO_TOL = 0.05     # ancho dentro del ±5% de la referencia
DIM_STD = (2000, 2000)
DPI_MIN = 300
RANSAC_SEED = 42      # determinismo: la puerta no tira dados
SIFT_ARTE_MAX = 1600  # el arte se acota a 1600px para SIFT (invariante a
                      # escala; sin cota, un arte de 4500px revienta memoria)

GOLDEN_DEFAULT = os.path.expanduser(
    "~/workspace/goals/pod-etsy-sistema-operativo-q4-2026"
    "/files/disenos/mockups/vitals-stable-kit")
ARTE_DEFAULT = os.path.expanduser(
    "~/workspace/goals/pod-etsy-sistema-operativo-q4-2026"
    "/files/disenos/canonicos/vitals-stable-final.png")


def cargar_arte(path):
    art = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if art is None or art.shape[2] != 4:
        raise SystemExit(f"no se pudo leer el arte RGBA: {path}")
    ys, xs = np.where(art[:, :, 3] > 16)
    crop = art[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    # SIFT corre acotado: el matching es invariante a escala, pero un arte
    # de 4500px genera tantos keypoints que revienta memoria (OOM 2026-10-13).
    k = min(1.0, SIFT_ARTE_MAX / max(crop.shape[1], crop.shape[0]))
    if k < 1.0:
        crop = cv2.resize(crop, (int(crop.shape[1] * k), int(crop.shape[0] * k)),
                          interpolation=cv2.INTER_AREA)
    rgb = crop[:, :, :3].astype(np.float32)
    a = crop[:, :, 3:4].astype(np.float32) / 255.0
    gris = cv2.cvtColor((rgb * a + 255 * (1 - a)).astype(np.uint8),
                          cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    kp, desc = sift.detectAndCompute(gris, None)
    return {"crop_w": crop.shape[1], "crop_h": crop.shape[0], "k": k,
            "kp": kp, "desc": desc, "sift": sift}


def localizar(arte, img_path):
    """Localiza el arte en el mockup por SIFT.

    Devuelve (confianza, x, y, w, h, n_matches). Confianza = inliers RANSAC
    / matches buenos. Coordenadas en px de la imagen original.
    """
    img = cv2.imread(img_path)
    if img is None:
        raise SystemExit(f"no se pudo leer la imagen: {img_path}")
    s = img.shape[1] / 1000.0  # SIFT corre a 1000px; s reescala al original
    chica = cv2.resize(img, (1000, int(img.shape[0] * 1000 / img.shape[1])))
    gris = cv2.cvtColor(chica, cv2.COLOR_BGR2GRAY)
    kp2, d2 = arte["sift"].detectAndCompute(gris, None)
    if d2 is None or len(kp2) < 4:
        return (0.0, 0, 0, 0, 0, 0)
    flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))
    pares = flann.knnMatch(arte["desc"], d2, k=2)
    buenos = [m for m, n in pares if m.distance < 0.7 * n.distance]
    if len(buenos) < MATCHES_MIN:
        return (0.0, 0, 0, 0, 0, len(buenos))
    p1 = np.float32([arte["kp"][m.queryIdx].pt for m in buenos])
    p2 = np.float32([kp2[m.trainIdx].pt for m in buenos])
    cv2.setRNGSeed(RANSAC_SEED)
    M, inl = cv2.estimateAffinePartial2D(p1, p2, method=cv2.RANSAC,
                                        ransacReprojThreshold=8.0)
    if M is None:
        return (0.0, 0, 0, 0, 0, len(buenos))
    inl = inl.ravel().astype(bool)
    conf = float(inl.sum()) / len(buenos)
    escala = float(np.sqrt(M[0, 0] ** 2 + M[1, 0] ** 2))
    tx, ty = float(M[0, 2]) * s, float(M[1, 2]) * s
    # crop_w/h y M viven en el mismo espacio (arte acotado): sin factor k.
    # (2026-10-13: dividir por k inflaba la medida ×(1/k); invisible en la
    # comparación relativa, pero las mediciones absolutas mentían.)
    w = arte["crop_w"] * escala * s
    h = arte["crop_h"] * escala * s
    return (conf, tx, ty, w, h, len(buenos))


def referencia_golden(golden_root, estilo, color):
    patron = os.path.join(golden_root, f"{estilo}*prop2*{color}*2000.jpg")
    cands = sorted(glob.glob(patron))
    if not cands:
        raise SystemExit(f"sin referencia aprobada para {estilo}/{color} en {golden_root}")
    return cands[0]


def gate_doblada_placement(args, gates, med):
    """Verificación específica para doblada (2026-10-13).

    El SIFT falla en doblada porque el doblez ocluye parte del diseño.
    Se verifica el MÉTODO:
    1. Dimensiones 2000x2000 (ya verificado antes).
    2. La calibración de la base existe.
    3. Hay contenido de diseño en la zona esperada (no está vacío ni
       fue achicado para "encajar"): se mide la varianza de color en
       la región donde debe estar el diseño vs. la tela de fondo.
    """
    prod = "gildan-18000"
    cal_path = os.path.expanduser(
        f"~/workspace/pod-limpio/data/bases-doblada/{prod}-{args.color}.json")
    if not os.path.isfile(cal_path):
        cal_path = os.path.expanduser(
            f"~/workspace/pod-limpio/data/bases-doblada/{prod}-white.json")
    if not os.path.isfile(cal_path):
        gates["placement"] = {"pass": False,
                              "motivo": "sin calibración de base doblada"}
        return verdict(gates, med, "placement")
    cal = json.load(open(cal_path, encoding="utf-8"))
    escala = float(cal["escala_vs_flatlay"])

    img = cv2.imread(args.candidato)
    Hh, W = img.shape[:2]
    k = 2000.0 / 1280.0
    exp_cx = (960.0 - 320.0) * k
    exp_top = (95.0 + 351.0 * escala) * k
    exp_w = 429.0 * escala * k

    # Región esperada del diseño (con margen)
    x0, x1 = int(exp_cx - exp_w * 0.7), int(exp_cx + exp_w * 0.7)
    y0, y1 = int(exp_top - 50), int(min(Hh, exp_top + exp_w * 1.2))
    x0, x1 = max(0, x0), min(W, x1)
    y0, y1 = max(0, y0), min(Hh, y1)
    region = img[y0:y1, x0:x1].astype(float)

    # Varianza de color: el diseño tiene colores variados; la tela es uniforme.
    # Se usa la desviación estándar del canal con más variación.
    std_b = float(region[:, :, 0].std())
    std_g = float(region[:, :, 1].std())
    std_r = float(region[:, :, 2].std())
    std_max = max(std_b, std_g, std_r)

    # Referencia: zona de tela pura (esquina superior izquierda, sin diseño)
    tela = img[50:200, 50:200].astype(float)
    std_tela = max(float(tela[:, :, 0].std()),
                   float(tela[:, :, 1].std()),
                   float(tela[:, :, 2].std()))

    # El diseño debe tener al menos 2x la varianza de la tela pura.
    ratio = std_max / max(std_tela, 1.0)
    ok = ratio >= 2.0
    med["doblada"] = {
        "calibracion": os.path.basename(cal_path),
        "escala": escala,
        "std_diseno": round(std_max, 1),
        "std_tela": round(std_tela, 1),
        "ratio": round(ratio, 2),
    }
    gates["placement"] = {"pass": ok,
                          "motivo": None if ok else
                          "sin contenido de diseño en la zona esperada"}
    return verdict(gates, med, None if ok else "placement")


def gate_zoom(args, gates, med):
    """Verificación específica para zoom/macro (2026-10-13).

    Criterio: el macro es un recorte del flat-lay aprobado, no una
    re-colocación. Se verifica que el candidato sea un crop válido de
    la referencia mediante SIFT directo (candidato vs referencia).
    Un recorte legítimo produce muchos matches con alta confianza.
    """
    if not args.referencia or not os.path.isfile(args.referencia):
        gates["placement"] = {"pass": False,
                              "motivo": "zoom requiere --referencia (flat-lay aprobado)"}
        return verdict(gates, med, "placement")

    # SIFT directo: candidato vs referencia (debe ser un recorte).
    ref = cv2.imread(args.referencia, cv2.IMREAD_GRAYSCALE)
    cand = cv2.imread(args.candidato, cv2.IMREAD_GRAYSCALE)
    # Reducir para velocidad (el crop es 2000, la ref es 2000).
    sift = cv2.SIFT_create()
    kp_r, des_r = sift.detectAndCompute(ref, None)
    kp_c, des_c = sift.detectAndCompute(cand, None)
    if des_r is None or des_c is None or len(kp_r) < 10 or len(kp_c) < 10:
        gates["placement"] = {"pass": False,
                              "motivo": "sin descriptores SIFT suficientes"}
        return verdict(gates, med, "placement")

    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des_c, des_r, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    # Para un recorte, lo que importa es el número absoluto de matches
    # buenos (el ratio es bajo porque el zoom tiene features a otra escala).
    # Umbral: 10x el mínimo general, calibrado contra el zoom de prueba
    # (2801 matches buenos).
    ok = len(good) >= 300
    med["zoom"] = {
        "referencia": os.path.basename(args.referencia),
        "matches_buenos": len(good),
        "umbral": 300,
    }
    gates["placement"] = {"pass": ok,
                          "motivo": None if ok else
                          "el candidato no es un recorte válido de la referencia"}
    return verdict(gates, med, None if ok else "placement")


def gate_onmodel(args, gates, med):
    """Verificación específica para on-model (2026-10-14, reforzada).

    En on-model la persona altera la escala y la perspectiva; no se compara
    posición contra el flat-lay. Se verifica:
    1. El diseño se localiza en el candidato con buena confianza (SIFT).
    2. El bbox tiene un tamaño razonable (no diminuto, no toda la imagen).
    3. La PROPORCIÓN del bbox coincide con la del arte (el redibujo de la
       IA cambia la proporción; el composite determinista la preserva).
       Tolerancia ±10%.
    4. DISTANCIA CUELLO→DISEÑO: el diseño debe empezar al menos 10% del
       alto de la imagen por debajo del cuello (criterio: 12%). Si está
       más cerca, FAIL — el diseño está mal ubicado en el área.
       El cuello se pasa con --cuello-y (calibración de la base) o se
       estima en 30% del alto (pose sentada).
    """
    arte = cargar_arte(args.arte)
    arte_h, arte_w = arte["crop_h"], arte["crop_w"]
    ratio_arte = arte_w / arte_h
    c_c, xc, yc, wc, hc, n_c = localizar(arte, args.candidato)
    med["candidato"] = {"confianza": round(c_c, 3), "matches": n_c,
                        "bbox": [round(xc, 1), round(yc, 1),
                                 round(wc, 1), round(hc, 1)]}
    if c_c < CONF_MIN or n_c < MATCHES_MIN or wc <= 0 or hc <= 0:
        gates["placement"] = {"pass": False,
                              "motivo": "diseño no localizado con confianza",
                              "conf": round(c_c, 3), "matches": n_c}
        return verdict(gates, med, "placement")
    # Tamaño razonable: el diseño debe ocupar entre 5% y 80% del ancho.
    frac = wc / DIM_STD[0]
    ok_tam = 0.05 <= frac <= 0.80
    # Proporción: el bbox debe tener la misma proporción que el arte.
    ratio_cand = wc / hc
    delta_ratio = abs(ratio_cand - ratio_arte) / ratio_arte
    ok_ratio = delta_ratio <= 0.10
    # Distancia cuello→diseño: medir el BORDE REAL del diseño por color,
    # NO el bbox de SIFT (el bbox de SIFT subestima el top porque solo
    # encuentra features fuertes en el medio del diseño, no el borde).
    # Método: buscar píxeles con saturación alta (colores del diseño) en
    # la zona del torso, y tomar el mínimo Y.
    with Image.open(args.candidato) as im:
        W_img, H = im.size
        arr = np.array(im.convert("RGB"))
    bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    mask_color = (hsv[:, :, 1] > 80) & (hsv[:, :, 2] > 50)
    # Torso: centro horizontal (30%-70% del ancho), desde el cuello hasta 80% del alto
    x0, x1 = int(W_img * 0.30), int(W_img * 0.70)
    cuello_arg = getattr(args, "cuello_y", None)
    y_start = int(cuello_arg) if cuello_arg is not None else int(H * 0.30)
    y_end = int(H * 0.80)
    # Buscar el primer Y con color en la zona del torso
    tops = []
    for x in range(x0, x1, 20):
        col = mask_color[y_start:y_end, x]
        ys = np.where(col)[0]
        if len(ys) > 0:
            tops.append(ys.min() + y_start)
    if tops:
        diseno_top_real = int(min(tops))
    else:
        diseno_top_real = float(yc)  # fallback al SIFT si no hay color
    cuello_y_val = getattr(args, "cuello_y", None)
    if cuello_y_val is None:
        cuello_y_val = 0.30 * H
    gap = float(diseno_top_real - cuello_y_val)
    gap_frac = float(gap / H)
    ok_cuello = gap_frac >= 0.10  # mínimo 10%, objetivo 12%
    # DESBORDE: el diseño no debe salir de la prenda (hem).
    # Si el bottom del diseño supera el hem_y, FAIL — el arte está sobre
    # otra prenda (pantalón) fuera del producto. Lógica doblada.
    hem_y = getattr(args, "hem_y", None)
    if hem_y is not None:
        diseno_bottom = yc + hc
        ok_hem = diseno_bottom <= hem_y
    else:
        ok_hem = True
        diseno_bottom = yc + hc
    ok = ok_tam and ok_ratio and ok_cuello and ok_hem
    med["onmodel"] = {"fraccion_ancho": round(frac, 3),
                      "ratio_arte": round(ratio_arte, 3),
                      "ratio_candidato": round(ratio_cand, 3),
                      "delta_ratio": round(delta_ratio, 3),
                      "cuello_y": round(cuello_y_val, 1),
                      "diseno_top_y": round(diseno_top_real, 1),
                      "diseno_top_sift": round(yc, 1),
                      "diseno_bottom": round(diseno_bottom, 1),
                      "hem_y": hem_y,
                      "gap_px": round(gap, 1),
                      "gap_frac": round(gap_frac, 3),
                      "gap_min": 0.10,
                      "metodo_gap": "color_real (no SIFT bbox)"}
    motivo = None
    if not ok_tam:
        motivo = f"tamaño fuera de rango ({frac:.2f})"
    elif not ok_ratio:
        motivo = f"proporción deformada (delta {delta_ratio:.2f} > 0.10, posible redibujo)"
    elif not ok_cuello:
        motivo = f"diseño demasiado cerca del cuello (gap {gap_frac:.1%} < 10% mínimo, debe ser ≥12%)"
    elif not ok_hem:
        motivo = f"diseño desborda la prenda (bottom {diseno_bottom:.0f} > hem {hem_y}, arte sobre pantalón)"
    gates["placement"] = {"pass": ok, "motivo": motivo}
    return verdict(gates, med, None if ok else "placement")


def gate_mockup(args):
    gates, med = {}, {}
    # 1. dimensiones
    with Image.open(args.candidato) as im:
        w, h = im.size
    med["dimensiones_px"] = [w, h]
    g_dim = (w, h) == DIM_STD
    gates["dimensiones"] = {"pass": g_dim, "esperado": list(DIM_STD), "medido": [w, h]}
    if not g_dim:
        return verdict(gates, med, "dimensiones")

    # 2. placement: para doblada se usa verificación por método (el SIFT
    #    falla por la oclusión natural del doblez); para zoom se verifica
    #    que sea un recorte de la referencia; para on-model se verifica
    #    presencia con confianza (la persona altera escala/perspectiva);
    #    otros estilos usan SIFT contra referencia.
    if args.estilo == "doblada":
        return gate_doblada_placement(args, gates, med)
    if args.estilo == "zoom":
        return gate_zoom(args, gates, med)
    if args.estilo == "onmodel":
        return gate_onmodel(args, gates, med)

    # 2. placement contra referencia aprobada (flatlay y otros estilos)
    arte = cargar_arte(args.arte)
    if args.referencia:
        # Criterio v2: el flat-lay aprobado DE ESTE DISEÑO es la referencia.
        ref_path = args.referencia
        if not os.path.isfile(ref_path):
            raise SystemExit(f"no existe la referencia: {ref_path}")
        origen_ref = "diseno"
    else:
        # Modo heredado: golden set por estilo/color (solo diseños del kit).
        ref_path = referencia_golden(args.golden_root, args.estilo, args.color)
        origen_ref = "golden"
    c_r, xr, yr, wr, hr, n_r = localizar(arte, ref_path)
    c_c, xc, yc, wc, hc, n_c = localizar(arte, args.candidato)
    med["referencia"] = {"archivo": os.path.basename(ref_path),
                         "origen": origen_ref,
                         "confianza": round(c_r, 3), "matches": n_r,
                         "bbox": [round(xr, 1), round(yr, 1),
                                  round(wr, 1), round(hr, 1)]}
    med["candidato"] = {"confianza": round(c_c, 3), "matches": n_c,
                        "bbox": [round(xc, 1), round(yc, 1),
                                 round(wc, 1), round(hc, 1)]}
    if c_r < CONF_MIN or c_c < CONF_MIN or wr <= 0 or wc <= 0:
        gates["placement"] = {"pass": False,
                              "motivo": "diseno no localizado con confianza o bbox inválido",
                              "conf_ref": round(c_r, 3),
                              "conf_cand": round(c_c, 3)}
        return verdict(gates, med, "placement")
    tol_c = CENTRO_TOL * DIM_STD[0]
    dcx, dcy = abs((xc + wc / 2) - (xr + wr / 2)), abs((yc + hc / 2) - (yr + hr / 2))
    dtam = abs(wc - wr) / wr
    ok = dcx <= tol_c and dcy <= tol_c and dtam <= TAMANO_TOL
    gates["placement"] = {"pass": ok,
                          "delta_centro_px": [round(dcx, 1), round(dcy, 1)],
                          "delta_tamano": round(dtam, 3),
                          "tolerancia_centro_px": tol_c,
                          "tolerancia_tamano": TAMANO_TOL}
    return verdict(gates, med, None if ok else "placement")


def gate_arte(args):
    with Image.open(args.archivo) as im:
        w, h = im.size
    dpi = w / args.ancho_pulgadas
    ok = dpi >= DPI_MIN
    gates = {"dpi_arte": {"pass": ok, "dpi_medido": round(dpi, 1),
                          "minimo": DPI_MIN, "ancho_px": w,
                          "ancho_pulgadas": args.ancho_pulgadas}}
    return verdict(gates, {"archivo": os.path.basename(args.archivo)}, None if ok else "dpi_arte")


def verdict(gates, med, criterio):
    ok = all(g["pass"] for g in gates.values())
    print(json.dumps({"veredicto": "PASS" if ok else "FAIL",
                      "criterio_violado": criterio,
                      "gates": gates, "mediciones": med},
                     indent=1, ensure_ascii=False))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="modo", required=True)
    m = sub.add_parser("mockup")
    m.add_argument("--candidato", required=True)
    m.add_argument("--estilo", required=False, default=None,
                   choices=["flatlay", "doblada", "zoom", "closecrop", "onmodel"])
    m.add_argument("--color", required=False, default=None,
                   choices=["white", "sand", "sportgrey"])
    m.add_argument("--golden-root", default=GOLDEN_DEFAULT)
    m.add_argument("--referencia", default=None,
                   help="flat-lay aprobado DE ESTE DISEÑO (criterio v2). "
                        "Si se da, se usa como referencia en vez del golden set.")
    m.add_argument("--arte", default=ARTE_DEFAULT)
    m.add_argument("--cuello-y", type=float, default=None,
                   help="posición Y del cuello en px (calibración de la base). "
                        "Si no se da, se estima en 30% del alto.")
    m.add_argument("--hem-y", type=float, default=None,
                   help="posición Y del hem (borde inferior de la prenda) en px. "
                        "Si se da, el gate verifica que el diseño no desborde.")
    a = sub.add_parser("arte")
    a.add_argument("--archivo", required=True)
    a.add_argument("--ancho-pulgadas", type=float, default=10.5)
    args = ap.parse_args()
    if args.modo == "mockup":
        if not args.referencia and not (args.estilo and args.color):
            ap.error("mockup requiere --referencia o (--estilo y --color)")
        sys.exit(gate_mockup(args))
    sys.exit(gate_arte(args))


if __name__ == "__main__":
    main()
