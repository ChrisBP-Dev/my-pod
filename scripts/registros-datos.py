#!/usr/bin/env python3
"""registros-datos.py — el ciclo «escribir = commitear» tras la
separación de registros (D1, migración a Rameli v0.17.0).

Desde el 2026-10-21 la app vive en DOS repos:

- **Sistema** — este repo (`my-pod`): skills, docs y scripts.
  Bajo `data/` solo trackea el esqueleto (`.gitkeep`).
- **Datos** — repo privado `my-pod-datos` (clon local en
  `~/workspace/my-pod-datos`): los **registros de la instancia**
  (texto bajo `data/`: ficha/config/registro/ledger de la
  tienda y registros globales de texto). Es el respaldo
  versionado de la instancia (D2: el respaldo ES este repo).

Los archivos físicos NO se movieron: los registros siguen
viviendo en `~/workspace/my-pod/data/...`, que es donde los
skills, scripts y crons los leen y escriben. Este script es
el puente de versionado:

- `commit -m "mensaje"`: sincroniza los registros físicos
  hacia el clon de datos (copia altas/cambios, retira bajas),
  commitea ahí SOLO si hay cambios y pushea. Verifica que el
  repo de datos no quede «ahead».
- `pull`: trae el repo de datos (`git pull`) y sincroniza
  sus registros hacia el árbol físico (restauración o
  arranque en una máquina nueva).

Qué es «registro» (y qué no):
- SÍ: todo archivo de TEXTO bajo `data/`.
- NO (nunca se versiona en ningún repo): medios (las 18
  extensiones del chequeo 5 de Rameli: video/audio/ráster),
  checkpoints locales `data/tiendas/*/estado-*.json`, CSV
  crudos de `data/ventas-csv/` y el contenido transitorio de
  `data/cola-pins/`.
- Los `.gitkeep` son **esqueleto**, no registros: cada repo
  trackea los suyos y el puente NO los sincroniza (ni los
  copia ni los retira en ningún sentido).

Uso:
    python3 scripts/registros-datos.py commit -m "Pinterest diario 2026-10-21: registro de pins publicados"
    python3 scripts/registros-datos.py pull
    python3 scripts/registros-datos.py estado

El clon de datos se busca en `$MY_POD_DATOS_DIR` o en
`~/workspace/my-pod-datos`.
"""

import os
import shutil
import subprocess
import sys

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS_DIR = os.environ.get(
    "MY_POD_DATOS_DIR",
    os.path.join(os.path.dirname(APP_DIR), "my-pod-datos"),
)
DATA_REL = "data"

# Medios: lista del chequeo 5 de Rameli (DATOS-INSTANCIA.md §5).
MEDIA_EXTS = {
    ".mp4", ".mov", ".mkv", ".webm", ".mp3", ".wav", ".flac",
    ".png", ".jpg", ".jpeg", ".webp", ".avif", ".heic", ".heif",
    ".gif", ".bmp", ".tif", ".tiff",
}


def es_registro(rel):
    """rel: ruta relativa a la raíz de la app, con '/' — p. ej.
    'data/tiendas/<tienda-id>/config.json'. True si se versiona
    en el repo de datos."""
    if not rel.startswith(DATA_REL + "/"):
        return False
    partes = rel.split("/")
    nombre = partes[-1]
    if nombre == ".gitkeep":
        return False  # esqueleto: lo trackea cada repo, no se sincroniza
    if os.path.splitext(nombre)[1].lower() in MEDIA_EXTS:
        return False
    # Checkpoints locales de corrida: jamás versionados.
    if (len(partes) == 4 and partes[1] == "tiendas"
            and nombre.startswith("estado-") and nombre.endswith(".json")):
        return False
    # CSV crudos de ventas: importación regenerable.
    if len(partes) == 3 and partes[1] == "ventas-csv" and nombre.endswith(".csv"):
        return False
    # Cola transitoria de pins: solo viaja su .gitkeep.
    if partes[1] == "cola-pins" and nombre != ".gitkeep":
        return False
    return True


def listar_registros(raiz):
    """Mapa ruta-relativa -> ruta absoluta de los registros
    físicos bajo <raiz>/data."""
    encontrados = {}
    base = os.path.join(raiz, DATA_REL)
    if not os.path.isdir(base):
        return encontrados
    for dirpath, _dirnames, filenames in os.walk(base):
        for nombre in filenames:
            absoluta = os.path.join(dirpath, nombre)
            rel = os.path.relpath(absoluta, raiz).replace(os.sep, "/")
            if es_registro(rel):
                encontrados[rel] = absoluta
    return encontrados


def git(directorio, *args, check=True):
    resultado = subprocess.run(
        ["git", "-C", directorio, *args],
        capture_output=True, text=True,
    )
    if check and resultado.returncode != 0:
        sys.stderr.write(
            f"git -C {directorio} {' '.join(args)} falló:\n"
            f"{resultado.stdout}{resultado.stderr}\n"
        )
        sys.exit(2)
    return resultado


def exigir_repo_datos():
    if not os.path.isdir(os.path.join(DATOS_DIR, ".git")):
        sys.stderr.write(
            f"No existe el clon del repo de datos en {DATOS_DIR}.\n"
            "Clónalo: git clone git@github.com:ChrisBP-Dev/my-pod-datos.git "
            f"{DATOS_DIR}\n"
        )
        sys.exit(2)


def sincronizar(origen_raiz, destino_raiz):
    """Espejo de registros origen -> destino. Devuelve
    (copiados, retirados)."""
    origen = listar_registros(origen_raiz)
    destino = listar_registros(destino_raiz)
    copiados = 0
    for rel, absoluta in sorted(origen.items()):
        destino_abs = os.path.join(destino_raiz, *rel.split("/"))
        if os.path.isfile(destino_abs):
            with open(absoluta, "rb") as f:
                contenido = f.read()
            with open(destino_abs, "rb") as f:
                if f.read() == contenido:
                    continue
        os.makedirs(os.path.dirname(destino_abs), exist_ok=True)
        shutil.copyfile(absoluta, destino_abs)
        copiados += 1
    retirados = 0
    for rel, absoluta in sorted(destino.items()):
        if rel not in origen:
            os.remove(absoluta)
            retirados += 1
    return copiados, retirados


def cmd_commit(args):
    exigir_repo_datos()
    mensaje = None
    i = 0
    while i < len(args):
        if args[i] == "-m" and i + 1 < len(args):
            mensaje = args[i + 1]
            i += 2
        else:
            sys.stderr.write(f"Argumento no reconocido: {args[i]}\n")
            sys.exit(2)
    if not mensaje:
        sys.stderr.write('Falta el mensaje: commit -m "mensaje"\n')
        sys.exit(2)
    # El repo de datos manda en su propio historial: primero
    # se trae lo remoto, para commitear sobre la punta real.
    git(DATOS_DIR, "pull", "--ff-only", "origin", "main")
    copiados, retirados = sincronizar(APP_DIR, DATOS_DIR)
    git(DATOS_DIR, "add", "-A", "--", DATA_REL)
    estado = git(DATOS_DIR, "status", "--porcelain", "--", DATA_REL)
    if not estado.stdout.strip():
        print("registros: sin cambios — nada que commitear en my-pod-datos")
        return
    git(DATOS_DIR, "commit", "--quiet", "-m", mensaje)
    git(DATOS_DIR, "push", "origin", "main")
    verificacion = git(DATOS_DIR, "status", "-sb")
    print(
        f"registros: {copiados} copiado(s), {retirados} retirado(s); "
        f"commit+push en my-pod-datos OK"
    )
    print(verificacion.stdout.strip().splitlines()[0])
    if "ahead" in verificacion.stdout:
        sys.stderr.write("ERROR: my-pod-datos quedó ahead tras el push\n")
        sys.exit(2)


def cmd_pull(_args):
    exigir_repo_datos()
    git(DATOS_DIR, "pull", "--ff-only", "origin", "main")
    copiados, retirados = sincronizar(DATOS_DIR, APP_DIR)
    print(
        f"registros: pull de my-pod-datos OK; {copiados} archivo(s) "
        f"actualizado(s) en el árbol físico, {retirados} retirado(s)"
    )


def cmd_estado(_args):
    exigir_repo_datos()
    fisicos = listar_registros(APP_DIR)
    en_datos = listar_registros(DATOS_DIR)
    print(f"registros físicos en la app: {len(fisicos)}")
    print(f"registros en el clon de datos: {len(en_datos)}")
    verificacion = git(DATOS_DIR, "status", "-sb")
    print(verificacion.stdout.strip().splitlines()[0])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("commit", "pull", "estado"):
        sys.stderr.write(__doc__)
        sys.exit(2)
    comando = sys.argv[1]
    if comando == "commit":
        cmd_commit(sys.argv[2:])
    elif comando == "pull":
        cmd_pull(sys.argv[2:])
    else:
        cmd_estado(sys.argv[2:])


if __name__ == "__main__":
    main()
