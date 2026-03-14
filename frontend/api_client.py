import httpx
import os
from typing import List, Dict, Any, Optional

# Carrega a URL do backend de variáveis de ambiente ou usa o padrão
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

class APIClient:
    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url

    def get_empreendimentos(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        try:
            response = httpx.get(f"{self.base_url}/empreendimentos", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao buscar empreendimentos: {e}")
            return []

    def get_empreendimento(self, id: int) -> Optional[Dict[str, Any]]:
        try:
            response = httpx.get(f"{self.base_url}/empreendimentos/{id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao buscar empreendimento {id}: {e}")
            return None

    def create_empreendimento(self, data: Dict[str, Any]) -> bool:
        try:
            response = httpx.post(f"{self.base_url}/empreendimentos", json=data)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Erro ao criar empreendimento: {e}")
            return False

    def update_empreendimento(self, id: int, data: Dict[str, Any]) -> bool:
        try:
            response = httpx.put(f"{self.base_url}/empreendimentos/{id}", json=data)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Erro ao atualizar empreendimento {id}: {e}")
            return False

    def delete_empreendimento(self, id: int) -> bool:
        try:
            response = httpx.delete(f"{self.base_url}/empreendimentos/{id}")
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Erro ao deletar empreendimento {id}: {e}")
            return False

    def check_health(self) -> bool:
        try:
            response = httpx.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False
