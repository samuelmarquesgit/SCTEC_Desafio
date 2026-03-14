import subprocess
import time
import sys
import os

def run_services():
    print("Iniciando SCTEC (Back-end + Front-end)...")
    
    # 1. Inicia o Backend (FastAPI)
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    print("Back-end (API) iniciado em http://127.0.0.1:8000")

    # Aguarda um pouco para o backend subir
    time.sleep(2)

    # 2. Inicia o Frontend (Streamlit)
    try:
        print("Abrindo Front-end (Streamlit)...")
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "frontend/main.py"],
            check=True
        )
    except KeyboardInterrupt:
        print("\n\nTerminando serviços...")
    finally:
        backend_process.terminate()
        print("Serviços encerrados.")

if __name__ == "__main__":
    run_services()
