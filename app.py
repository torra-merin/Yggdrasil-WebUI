import os
import platform
import shutil
import subprocess
import json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

# -------------------------
# Detecta yggdrasilctl
# -------------------------
def find_yggdrasilctl():
    config = load_config()
    if "yggdrasilctl_path" in config and os.path.exists(config["yggdrasilctl_path"]):
        return config["yggdrasilctl_path"]

    system = platform.system()
    paths_to_check = []

    if system == "Windows":
        paths_to_check = [
            r"C:\Program Files\Yggdrasil\yggdrasilctl.exe",
            r"C:\Program Files (x86)\Yggdrasil\yggdrasilctl.exe",
        ]
    elif system == "Linux":
        paths_to_check = [
            "/usr/bin/yggdrasilctl",
            "/usr/local/bin/yggdrasilctl",
            "/snap/bin/yggdrasilctl",
        ]
    elif system == "Darwin":
        paths_to_check = [
            "/usr/local/bin/yggdrasilctl",
            "/opt/homebrew/bin/yggdrasilctl",
        ]

    for path in paths_to_check:
        if os.path.exists(path):
            return path

    which_path = shutil.which("yggdrasilctl")
    if which_path:
        return which_path

    return None

YGGCTL = find_yggdrasilctl()

# -------------------------
# Funcions Yggdrasil
# -------------------------
def run_yggctl(args):
    if not YGGCTL:
        return "ERROR: yggdrasilctl no trobat"

    try:
        result = subprocess.run(
            [YGGCTL] + args,
            capture_output=True,
            text=True
        )
        return result.stdout.strip() or result.stderr.strip()
    except Exception as e:
        return str(e)

def parse_peers(raw):
    peers = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        uri = parts[0]
        status = " ".join(parts[1:]) if len(parts) > 1 else ""
        if uri.startswith(("tls://", "tcp://", "quic://")):
            peers.append({"uri": uri, "status": status})
    return peers

# -------------------------
# Control servei Yggdrasil
# -------------------------
def is_yggdrasil_running():
    system = platform.system()
    try:
        if system == "Windows":
            result = subprocess.run(["sc", "query", "yggdrasil"], capture_output=True, text=True)
            return "RUNNING" in result.stdout
        elif system in ["Linux", "Darwin"]:
            result = subprocess.run(["systemctl", "is-active", "yggdrasil"], capture_output=True, text=True)
            return result.stdout.strip() == "active"
    except Exception:
        return False

@app.get("/yggdrasil-state")
def yggdrasil_state():
    running = is_yggdrasil_running()
    return {"running": running}

@app.post("/yggdrasil-toggle")
def yggdrasil_toggle():
    system = platform.system()
    if system == "Windows":
        return JSONResponse({"error": "Start/Stop via Services MMC only"}, status_code=400)

    running = is_yggdrasil_running()
    try:
        if running:
            subprocess.run(["sudo", "systemctl", "stop", "yggdrasil"], capture_output=True)
        else:
            subprocess.run(["sudo", "systemctl", "start", "yggdrasil"], capture_output=True)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    return JSONResponse({"running": not running})

# -------------------------
# Configuració manual de yggdrasilctl
# -------------------------
@app.post("/set-yggdrasil-path")
def set_yggdrasil_path(path: str = Form(...)):
    if os.path.exists(path):
        save_config({"yggdrasilctl_path": path})
        global YGGCTL
        YGGCTL = path
        return RedirectResponse("/", status_code=303)
    else:
        return HTMLResponse("<strong>Invalid path</strong>", status_code=400)

# -------------------------
# Rutes principals
# -------------------------
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    self_info = run_yggctl(["getself"])
    peers_raw = run_yggctl(["getpeers"])
    peers = parse_peers(peers_raw)
    tun = run_yggctl(["gettun"])

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "ygg_found": bool(YGGCTL),
            "self_info": self_info,
            "peers": peers,
            "tun": tun,
            "platform_system": platform.system(),
        },
    )

@app.post("/add-peer")
def add_peer(uri: str = Form(...)):
    run_yggctl(["addpeer", f"uri={uri}"])
    return RedirectResponse("/", status_code=303)

@app.post("/remove-peer")
def remove_peer(uri: str = Form(...)):
    run_yggctl(["removepeer", f"uri={uri}"])
    return RedirectResponse("/", status_code=303)
