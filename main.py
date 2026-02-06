import uvicorn
import webbrowser
import os

CONFIG_FILE = "run.conf"

def get_config():
    host = "127.0.0.1"
    port = 8000

    # Intentar llegir el fitxer
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    host = lines[0].strip()
                    port = int(lines[1].strip())
                    return host, port
        except Exception:
            print(f" {CONFIG_FILE} not readable. Set config again.")

    # Demanar host i port a l'usuari
    host_input = input(f"Set host [{host}]: ").strip()
    if host_input:
        host = host_input

    port_input = input(f"Set port [{port}]: ").strip()
    if port_input:
        try:
            port = int(port_input)
        except ValueError:
            print(f"Not a valid port. Using {port} instead.")

    # Guardar la configuració
    with open(CONFIG_FILE, "w") as f:
        f.write(f"{host}\n{port}\n")

    return host, port

if __name__ == "__main__":
    host, port = get_config()

    webbrowser.open(f"http://{host}:{port}")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        log_level="info"
    )
