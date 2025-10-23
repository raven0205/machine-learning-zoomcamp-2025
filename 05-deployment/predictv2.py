# serve this model as web service
import joblib 
from typing import Literal
from pydantic import BaseModel, Field

from fastapi import FastAPI
import uvicorn


# creating the Pydantic schema for the input JSON
class Converter(BaseModel):
    lead_source: Literal["organic_search", "social_media", "paid_ads", "referral", "events"]
    number_of_courses_viewed: int = Field(..., ge=0)
    annual_income: float = Field(..., ge=0.0)

# creating the Pydantic schema for the output JSON
class PredictResponse(BaseModel):
    c_probability: float
    converted: bool

app = FastAPI(title="converted")
model_file = 'pipeline_v1.bin'

with open(model_file, 'rb') as f_in:
    dv, model = joblib.load(f_in) 

def predict_single(sample_dict: dict):
    X = dv.transform([sample_dict])
    y_pred = model.predict_proba(X) [0, 1]
    return float(y_pred)

@app.post('/predict')

def predict(converter: Converter) -> PredictResponse:
    prob = predict_single(converter.dict())

    return PredictResponse(
        c_probability = prob,
        converted=prob >= 0.5
    )
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)
 