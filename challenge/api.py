import fastapi
import os
import joblib
from pydantic import BaseModel, conint
from typing import List
import pandas as pd
from .model import DelayModel
from .train import Train
from .validations import ValidOpera, ValidTipoVuelo
from google.cloud import storage
from contextlib import asynccontextmanager

MODEL_PATH = "models/delay_model.joblib"

app = fastapi.FastAPI()
model_predictor = DelayModel()

BUCKET_NAME = os.getenv("GCS_BUCKET")
MODEL_PATH_GCS = "model/delay_model.joblib"
TEMP_MODEL_PATH = "/tmp/delay_model.joblib"

if os.path.exists(MODEL_PATH):
    model_predictor._model = joblib.load(MODEL_PATH)

class _DummyModel:
    def predict(self, features: pd.DataFrame) -> List[int]:
        return [0] * len(features)

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):

    if os.getenv("TESTING_ENV") == "true":
        model_predictor._model = _DummyModel()
    else:
        if BUCKET_NAME:
            try:
                client = storage.Client()
                bucket = client.bucket(BUCKET_NAME)
                blob = bucket.blob(MODEL_PATH_GCS)
                if blob.exists():
                    blob.download_to_filename(TEMP_MODEL_PATH)
                    model_predictor._model = joblib.load(TEMP_MODEL_PATH)
                    print("Model loaded successfully from GCS.")
                else:
                    print("Warning: Model file not found in GCS.")
            except Exception as e:
                print(f"Error loading model from GCS: {e}")
        else:
            print("Warning: GCS_BUCKET_NAME env var not set.")
    
    yield

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
    if not BUCKET_NAME:
        raise fastapi.HTTPException(status_code=500, detail="GCS_BUCKET_NAME env var not set.")
    try:
        Train.train_and_save(BUCKET_NAME)
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"model/delay_model.joblib")
        blob.download_to_filename("/tmp/delay_model.joblib")
        model_predictor._model = joblib.load("/tmp/delay_model.joblib")
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