import os
import subprocess
import sys
import threading
import time

# ── Platform detection ────────────────────────────────────────────────────────
IS_WINDOWS = sys.platform == "win32"

REPO_DIR     = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(REPO_DIR, "frontend")
MAIN_PY      = os.path.join(REPO_DIR, "main.py")
VENV_DIR     = os.path.join(REPO_DIR, "venv")

if IS_WINDOWS:
    PYTHON_EXE = os.path.join(VENV_DIR, "Scripts", "python.exe")
    VENV_BIN   = os.path.join(VENV_DIR, "Scripts")
else:
    PYTHON_EXE = os.path.join(VENV_DIR, "bin", "python")
    VENV_BIN   = os.path.join(VENV_DIR, "bin")


def stream_output(process, prefix):
    try:
        for line in process.stdout:
            print(f"[{prefix}] {line.strip()}")
    except Exception:
        pass


def run():
    if not os.path.exists(PYTHON_EXE):
        print(f"Virtual environment not found at: {PYTHON_EXE}")
        print("Please run the install script first.")
        return

    env = os.environ.copy()
    env["PATH"] = VENV_BIN + os.pathsep + env["PATH"]
    env["PYTHONIOENCODING"] = "utf-8"

    print("==== AI Academic Assistant ====\n")
    print("Installing frontend dependencies...")

    try:
        subprocess.run(
            ["npm", "install"],
            cwd=FRONTEND_DIR,
            check=True,
            shell=IS_WINDOWS
        )
    except Exception as e:
        print(f"Frontend dependency installation failed: {e}")
        return

    print("\nStarting frontend dev server...\n")

    try:
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],   # ← always 3 separate items
            cwd=FRONTEND_DIR,
            env=env,
            shell=IS_WINDOWS,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1
        )

        frontend_thread = threading.Thread(
            target=stream_output, args=(frontend_process, "Frontend")
        )
        frontend_thread.daemon = True
        frontend_thread.start()

        time.sleep(3)

    except Exception as e:
        print(f"Frontend failed: {e}")
        return

    print("\n" + "=" * 50)
    print("Starting backend server...")
    print("=" * 50 + "\n")

    try:
        if os.getenv("DEBUG_AI") == "off":
            args = [PYTHON_EXE, "-m", "gunicorn", "main:app", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "--host", "127.0.0.1", "--port", "80"]
        else:
            args = [PYTHON_EXE, "-m", "gunicorn", "--reload", "main:app", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "--host", "127.0.0.1", "--port", "80"]


        backend_process = subprocess.Popen(
           args,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1
        )

        for line in backend_process.stdout:
            print(f"[Backend] {line}", end="")

    except KeyboardInterrupt:
        print("\n\nShutting down...")
        backend_process.terminate()
        frontend_process.terminate()
    except Exception as e:
        print(f"Backend failed: {e}")


if __name__ == "__main__":
    run()
