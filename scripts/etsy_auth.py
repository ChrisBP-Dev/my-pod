"""Auth Etsy API — helper portable (CAPA SISTEMA).

- Los secretos viven en el archivo local 0600 (nunca en repo/chat/logs).
- El access token dura 1h: este helper lo refresca automáticamente con
  el refresh token rotatorio y actualiza el archivo.
- La ruta del archivo sale del config de la tienda
  (MY_POD_TIENDA_CONFIG -> etsy_api.secrets_file); default documentado.

Uso:
    from etsy_auth import get_headers
    headers = get_headers()  # {"x-api-key": ..., "Authorization": ...}
"""

import calendar
import json
import os
import time
import urllib.parse
import urllib.request

_SECRETS_DEFAULT = os.path.expanduser("~/.config/my-pod/etsy-api.json")
_TIENDA_DEFAULT = os.path.expanduser(
    "~/workspace/my-pod/data/tiendas/29222324/config.json")
_TOKEN_URL = "https://api.etsy.com/v3/public/oauth/token"


def secrets_path():
    cfg = os.path.expanduser(os.environ.get("MY_POD_TIENDA_CONFIG",
                                            _TIENDA_DEFAULT))
    try:
        c = json.load(open(cfg))
        p = (c.get("etsy_api") or {}).get("secrets_file")
        if p:
            return os.path.expanduser(p)
    except Exception:
        pass
    return _SECRETS_DEFAULT


def _expirado(sec, margen=120):
    try:
        exp = sec.get("expires_at", "")
        # formato ISO UTC "2026-10-16T16:24:14+00:00"
        ts = calendar.timegm(time.strptime(exp[:19], "%Y-%m-%dT%H:%M:%S"))
        return time.time() > ts - margen
    except Exception:
        return True


def _refresh(sec, path):
    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "client_id": sec["keystring"],
        "refresh_token": sec["refresh_token"],
    }).encode()
    req = urllib.request.Request(
        _TOKEN_URL, data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as r:
        tok = json.load(r)
    sec["access_token"] = tok["access_token"]
    sec["refresh_token"] = tok.get("refresh_token", sec["refresh_token"])
    exp_in = tok.get("expires_in", 3600)
    sec["expires_at"] = time.strftime("%Y-%m-%dT%H:%M:%S+00:00",
                                      time.gmtime(time.time() + exp_in))
    with open(path, "w") as f:
        json.dump(sec, f, indent=2)
    os.chmod(path, 0o600)
    return sec


def load_secrets():
    """Lee los secretos y refresca el token si está por vencer."""
    path = secrets_path()
    sec = json.load(open(path))
    if _expirado(sec):
        sec = _refresh(sec, path)
    return sec


def get_headers(sec=None):
    """Headers listos para la API. Si el dict pasado está vencido (o no
    se pasa ninguno), carga+refresca desde el archivo."""
    if sec is None or _expirado(sec):
        sec = load_secrets()
    return {"x-api-key": sec["keystring"] + ":" + sec["shared_secret"],
            "Authorization": "Bearer " + sec["access_token"]}
