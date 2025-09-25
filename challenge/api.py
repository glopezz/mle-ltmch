import fastapi
import os
import joblib
from pydantic import BaseModel, conint
from typing import List
import pandas as pd
from .model import DelayModel
from .train import Train
from .validations import ValidOpera, ValidTipoVuelo

MODEL_PATH = "models/delay_model.joblib"

app = fastapi.FastAPI()
model_predictor = DelayModel()

if os.path.exists(MODEL_PATH):
    model_predictor._model = joblib.load(MODEL_PATH)

@app.exception_handler(fastapi.exceptions.RequestValidationError)
async def validation_exception_handler(request: fastapi.Request, exc: fastapi.exceptions.RequestValidationError):
    return fastapi.responses.JSONResponse(
        status_code=fastapi.status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )
class Flight(BaseModel):
    OPERA: ValidOpera
    TIPOVUELO: ValidTipoVuelo
    MES: conint(ge=1, le=12)

class FlightsRequest(BaseModel):
    flights: List[Flight]

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/train")
async def train_endpoint():
    try:
        Train.train_and_save("data/data.csv")
        model_predictor._model = joblib.load(MODEL_PATH)
        return {"message": "Training completed and model reloaded."}
    except Exception as e:
        return {"error": f"An error occurred during training: {e}"}

@app.post("/predict", status_code=200)
async def post_predict(request: FlightsRequest) -> dict:
    if model_predictor._model is None:
        return {"error": "The model has not been trained. Please execute the /train endpoint first."}
    
    input_df = pd.DataFrame([f.dict() for f in request.flights])
    
    features = model_predictor.preprocess(input_df)
    predictions = model_predictor.predict(features)
    
    return {"predict": predictions}