from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os

API_KEY = os.environ.get("QF_API_KEY", "quantumfinance_secret_token_12345") # Deve ser gerenciado via variáveis de ambiente
API_KEY_NAME = "X-API-KEY"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Chave de API inválida"
        )