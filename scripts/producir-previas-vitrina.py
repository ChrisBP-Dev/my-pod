#!/usr/bin/env python3
"""Producir las previas de revisión de la vitrina EN VIVO (My POD).

Reemplaza, para la entrega de propuestas, al antiguo generador de
paquete (`generar-datos-vitrina.py`, flujo de siembra retirado en la
fase «vitrina de lectura en vivo», 2026-10-26 —
docs/PROPUESTA-VITRINA-LECTURA-EN-VIVO.md §3-H2 y docs/VITRINA-VIVA.md).

Qué hace, por cada diseño entregado:

1. Lee la entrada del registro de la tienda y compone las previas
   deterministas desde el PNG de producción (fondo oscuro #17181c y
   fondo claro #f4f1ea, ancho 1100): el dueño juzga el arte como se
   verá sobre prenda oscura o clara. Nunca una regeneración
   «parecida».
2. Las escribe en el HOGAR DECLARADO del entregable dentro de los
   datos de la tienda:
   `data/tiendas/<tienda-id>/propuestas/<slug>/previa-oscura.jpg` y
   `previa-clara.jpg` (en personalizables, además
   `simulacion-oscura.jpg` y `simulacion-clara.jpg`).
   Ese hogar es el único donde un medio se versiona en el repo de
   datos (excepción acotada del dueño, 2026-10-26; el puente
   `registros-datos.py` y el `.gitignore` del repo de datos la
   declaran igual).
3. Declara el resultado EN LA ENTRADA del registro (la vitrina en
   vivo lee de ahí, con lista blanca): `dimensiones_px` medido del
   PNG real y el bloque `vitrina` con las rutas de las previas, el
   `arte_ref` del que salieron y la fecha de entrega. Una previa sin
   su declaración en el registro no existe para la vitrina.
4. Personalizables: es la PUERTA MECÁNICA del criterio — sin
   simulación válida en el registro o sin `ficha_razon` completa,
   FALLA con el error exacto y no produce nada (la validación es la
   misma que cerraba el paquete en el flujo anterior).

No genera paquete, no siembra, no toca ninguna superficie: deja el
entregable en su hogar y el registro declarándolo. Commitear es del
flujo que lo invoca (`registros-datos.py commit`, como todo registro).

Uso:
    python3 scripts/producir-previas-vitrina.py \
        --tienda <shop_id> [--slugs p058,p059] \
        [--repo ~/workspace/my-pod] [--ancho-previa 1100]

Sin `--slugs`, toma el lote actual de `estado-propuestas.json`.
Imprime un resumen JSON por diseño en stdout.
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

from PIL import Image

FONDO_OSCURO = (23, 24, 28)
FONDO_CLARO = (244, 241, 234)

# Campos obligatorios de la ficha de razón de un personalizable
# (puerta-arte-propuesta, «La ficha de razón»). Sin ficha completa
# no hay entrega: este script es la puerta mecánica de ese criterio.
FICHA_CAMPOS = [
    "razon",
    "prueba_borrado",
    "campos",
    "comprador_destinatario_ocasion",
    "clase_encaje",
    "ejemplo_simulacion",
    "peor_caso",
    "producto_destino",
    "plan_zonas",
]


def validar_personalizable(slug: str, entrada: dict, repo: Path) -> dict:
    """Devuelve {simulacion_path, ficha} o termina con error claro."""
    sim_rel = entrada.get("simulacion", "")
    sim_path = repo / sim_rel if sim_rel else None
    if not sim_path or not sim_path.exists():
        print(f"ERROR: {slug} es personalizable pero no tiene simulación "
              f"válida en el registro (`simulacion`: {sim_rel!r}). "
              "Sin simulación no hay entrega (puerta-arte-propuesta).",
              file=sys.stderr)
        raise SystemExit(1)
    ficha = entrada.get("ficha_razon")
    if not isinstance(ficha, dict):
        print(f"ERROR: {slug} es personalizable y no trae `ficha_razon`. "
              "Sin ficha completa no hay entrega.", file=sys.stderr)
        raise SystemExit(1)
    faltan = [c for c in FICHA_CAMPOS if not ficha.get(c)]
    if faltan:
        print(f"ERROR: {slug}: ficha_razon incompleta, faltan: "
              f"{', '.join(faltan)}.", file=sys.stderr)
        raise SystemExit(1)
    for campo in ficha["campos"]:
        if not campo.get("nombre") or not campo.get("tipo"):
            print(f"ERROR: {slug}: cada campo de la ficha trae `nombre` "
                  "y `tipo` (texto/dropdown/imagen).", file=sys.stderr)
            raise SystemExit(1)
        if campo["tipo"] == "texto" and not campo.get("limite"):
            print(f"ERROR: {slug}: el campo {campo['nombre']!r} es de "
                  "texto y no declara `limite` de caracteres.",
                  file=sys.stderr)
            raise SystemExit(1)
        if campo["tipo"] == "dropdown" and not campo.get("opciones"):
            print(f"ERROR: {slug}: el campo {campo['nombre']!r} es "
                  "dropdown y no declara `opciones` (vocabulario cerrado).",
                  file=sys.stderr)
            raise SystemExit(1)
    return {"simulacion_path": sim_path, "ficha": ficha}


def dimensiones_de(arte_path: Path) -> dict:
    with Image.open(arte_path) as im:
        return {"ancho_px": im.width, "alto_px": im.height}


def hacer_previa(arte_path: Path, destino: Path, fondo, ancho: int) -> None:
    arte = Image.open(arte_path).convert("RGBA")
    if arte.width > ancho:
        alto = round(arte.height * ancho / arte.width)
        arte = arte.resize((ancho, alto), Image.LANCZOS)
    lienzo = Image.new("RGBA", arte.size, fondo + (255,))
    lienzo.alpha_composite(arte)
    destino.parent.mkdir(parents=True, exist_ok=True)
    lienzo.convert("RGB").save(destino, "JPEG", quality=88, optimize=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tienda", required=True,
                    help="id de tienda (carpeta en data/tiendas/)")
    ap.add_argument("--repo", default="",
                    help="raíz física de la instancia (donde vive data/); "
                         "default: la raíz de la app de este script")
    ap.add_argument("--slugs", default="",
                    help="lista separada por comas; default: lote actual "
                         "del estado de propuestas")
    ap.add_argument("--ancho-previa", type=int, default=1100)
    args = ap.parse_args()

    repo = (Path(args.repo).expanduser() if args.repo
            else Path(__file__).resolve().parent.parent)
    base_tienda = repo / "data" / "tiendas" / args.tienda
    registro_path = base_tienda / "registro-listings.json"
    estado_path = base_tienda / "estado-propuestas.json"
    if not registro_path.exists():
        print(f"ERROR: no existe el registro: {registro_path}",
              file=sys.stderr)
        return 1
    registro = json.loads(registro_path.read_text(encoding="utf-8"))

    if args.slugs:
        slugs = [s.strip() for s in args.slugs.split(",") if s.strip()]
    else:
        if not estado_path.exists():
            print(f"ERROR: no existe el estado: {estado_path}",
                  file=sys.stderr)
            return 1
        estado = json.loads(estado_path.read_text(encoding="utf-8"))
        slugs = estado.get("lote_actual", {}).get("disenos", [])
    if not slugs:
        print("ERROR: lote vacío (sin slugs).", file=sys.stderr)
        return 1

    resumen = []
    for slug in slugs:
        entrada = registro.get(slug)
        if entrada is None:
            print(f"ERROR: {slug} no está en el registro de la tienda.",
                  file=sys.stderr)
            return 1
        arte_rel = entrada.get("arte", "")
        arte_path = repo / arte_rel
        if not arte_path.exists():
            print(f"ERROR: no existe el arte de {slug}: {arte_path}",
                  file=sys.stderr)
            return 1
        hogar = base_tienda / "propuestas" / slug
        hogar_rel = f"data/tiendas/{args.tienda}/propuestas/{slug}"
        hacer_previa(arte_path, hogar / "previa-oscura.jpg",
                     FONDO_OSCURO, args.ancho_previa)
        hacer_previa(arte_path, hogar / "previa-clara.jpg",
                     FONDO_CLARO, args.ancho_previa)
        bloque = {
            "arte_ref": arte_rel,
            "previa_oscura": f"{hogar_rel}/previa-oscura.jpg",
            "previa_clara": f"{hogar_rel}/previa-clara.jpg",
            "fecha_entrega": date.today().isoformat(),
        }
        if entrada.get("personalizable") is True:
            valido = validar_personalizable(slug, entrada, repo)
            hacer_previa(valido["simulacion_path"],
                         hogar / "simulacion-oscura.jpg",
                         FONDO_OSCURO, args.ancho_previa)
            hacer_previa(valido["simulacion_path"],
                         hogar / "simulacion-clara.jpg",
                         FONDO_CLARO, args.ancho_previa)
            bloque["simulacion_oscura"] = \
                f"{hogar_rel}/simulacion-oscura.jpg"
            bloque["simulacion_clara"] = \
                f"{hogar_rel}/simulacion-clara.jpg"
        entrada["dimensiones_px"] = dimensiones_de(arte_path)
        entrada["vitrina"] = bloque
        resumen.append({"slug": slug, **bloque,
                        "dimensiones_px": entrada["dimensiones_px"]})

    registro_path.write_text(
        json.dumps(registro, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(json.dumps({"ok": True, "tienda": args.tienda,
                      "disenos": resumen}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
