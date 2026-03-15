import subprocess
import time
import sys
import os

def run_services():
    print("--- Verificação de Ambiente SCTEC ---")
    
    # Garante que a pasta de dados existe
    if not os.path.exists("data"):
        print("📁 Criando diretório 'data' para persistência...")
        os.makedirs("data")
    
    # Verifica arquivos essenciais
    files_to_check = ["app/main.py", "frontend/main.py"]
    for f in files_to_check:
        if not os.path.exists(f):
            print(f"❌ Erro crítico: Arquivo {f} não encontrado!")
            return

    print("✅ Ambiente validado. Iniciando serviços...")
    print("-----------------------------------")
    
    # 1. Inicia o Backend (FastAPI)
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    print("🚀 Back-end (API) iniciado em http://127.0.0.1:8000")

    # Aguarda um pouco para o backend subir
    time.sleep(2)

    # 2. Inicia o Frontend (Streamlit)
    try:
        print("🎨 Abrindo Front-end (Streamlit)...")
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "frontend/main.py"],
            check=True
        )
    except KeyboardInterrupt:
        print("\n\nTerminando serviços...")
    finally:
        backend_process.terminate()
        print("🛑 Serviços encerrados.")

if __name__ == "__main__":
    run_services()
