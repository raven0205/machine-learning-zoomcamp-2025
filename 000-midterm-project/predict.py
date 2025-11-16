# 000-midterm-project/predict.py

import joblib 
from typing import Literal
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi import FastAPI
import uvicorn
from features import get_avg_storey
import pandas as pd

# ---------- Pydantic Schemas ----------
# creating the Pydantic schema for the input JSON (raw input before wrangling))
class HDBResaleRequest(BaseModel):
    month: str = Field(..., example="2024-01")
    town: Literal["ANG MO KIO","BEDOK","BISHAN","BUKIT BATOK","BUKIT MERAH","BUKIT PANJANG"
                  ,"BUKIT TIMAH","CENTRAL AREA","CHOA CHU KANG","CLEMENTI","GEYLANG","HOUGANG",
                  "JURONG EAST","JURONG WEST","KALLANG/WHAMPOA","MARINE PARADE","PASIR RIS",
                  "PUNGGOL","QUEENSTOWN","SEMBAWANG","SENGKANG","SERANGOON","TAMPINES",
                  "TOA PAYOH","WOODLANDS","YISHUN"]
    
    flat_type: Literal["1 ROOM", "2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE", "MULTI-GENERATION"]
    block: str = Field(...,example="754")
    street_name: str = Field(...,example="WOODLANDS AVE 4")
    storey_range: str = Field(...,example="07 TO 09")
    floor_area_sqm: float = Field(..., ge=0.0)
    lease_commence_date: int = Field(..., example=1986, ge=1960)
    
# creating the Pydantic schema for the output JSON
class PredictResponse(BaseModel):
    predicted_resale_price: float
    currency: str = "SGD"


# ---------- Load Model ----------

def load(filename):
    with open(filename, 'rb') as f_in:
        return joblib.load(f_in)



app = FastAPI(title="hdb-resale-price-predictor")

model = load('model.pkl')

# ---------- Prediction Endpoint ----------
@app.post("/predict", response_model=PredictResponse)
def predict_price(request: HDBResaleRequest):

    # Convert month to datetime
    sale_year = datetime.strptime(request.month, "%Y-%m").year

    # Feature engineering (same as training)
    input_data = {
        "town": request.town,
        "flat_type": request.flat_type,
        "floor_area_sqm": request.floor_area_sqm,
        "remaining_lease_years": 99 - (sale_year - request.lease_commence_date),
        "avg_storey": get_avg_storey(request.storey_range),
    }

    input_df = pd.DataFrame([input_data])

    # Predict using the loaded model
    if model is None:
        raise RuntimeError("Model not loaded! Train and save model.pkl first.")
    else:
        prediction = model.predict(input_df)[0]

    return PredictResponse(
        predicted_resale_price=round(float(prediction), 2)
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)
 