import pandas as pd
import mlflow.pyfunc
import mlflow.sklearn
from fastapi import FastAPI, Depends, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .dependencies import get_api_key
from .schemas import ClientData, PredictionResponse

# Configuração do Throttling
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="QuantumFinance Partner Credit Score API", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

MODEL_URI = "models:/QuantumCreditScore/Production"
SCALER_URI = None # Será definido ao carregar o modelo

# Carregar o modelo e o scaler do MLflow
try:
    model = mlflow.pyfunc.load_model(model_uri=MODEL_URI)
    
    # Extraindo o run_id do modelo para encontrar o scaler associado
    model_run_id = model.metadata.run_id
    SCALER_URI = f"runs:/{model_run_id}/scaler"
    scaler = mlflow.sklearn.load_model(SCALER_URI)

    print(f"Modelo carregado com sucesso. Run ID: {model_run_id}")

except Exception as e:
    print(f"Erro ao carregar modelo ou scaler do MLflow: {e}")
    # Em um cenário real, a aplicação não deveria iniciar sem o modelo
    model = None
    scaler = None

@app.get("/")
async def health_check():
    return {"status": "healthy", "model_ready": model is not None}

@app.post("/predict", response_model=PredictionResponse)
@limiter.limit("10/minute") # Limite de 10 requisições por minuto
async def predict_score(
    request: Request, # Necessário para o slowapi
    data: ClientData,
    api_key: str = Depends(get_api_key)
):
    if not model or not scaler:
        raise HTTPException(status_code=503, detail="Modelo não disponível")

    # Preparar os dados para o modelo
    input_df = pd.DataFrame([data.dict()])

    # Aplicar o scaler carregado do MLflow
    input_scaled = scaler.transform(input_df)
    
    # Realizar a predição
    prediction = model.predict(input_scaled)
    score = prediction[0]

    return PredictionResponse(
        client_id="request_example_id", # Em produção, isso viria do input ou seria gerado
        credit_score=score,
        model_version=model.metadata.model_uri
    )