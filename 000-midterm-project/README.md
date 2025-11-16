## HDB Resale Price Prediction Model Deployment
* Project Overview
This project implements and deploys a machine learning model designed to forecast the resale prices of Housing and Development Board (HDB) flats in Singapore. The aim is to allow stakeholders like real estate analysts, investors or buyers to learn about the recent trend and estimate property worth for their decision-making. The final deliverable is a containerized web service that provides real-time price predictions via a simple API endpoint.

* Data
The model uses preprocessed HDB resale transaction data from 2019-2023, as data/hdb_resale_data_cleaned.csv.
The full dataset from 2017 to 2025 can be downloaded from [Resale Flat Prices | HDB | data.gov.sg](https://data.gov.sg/datasets/d_8b84c4ee58e3cfc0ece0d773c8ca6abc/view).


## Key Data Fields

| Column Name | Description |
|------------|-------------|
| month | Month of sale (YYYY-MM) |
| town | Flat location (e.g., Woodlands, Jurong East) |
| flat_type | e.g., 4 ROOM, 5 ROOM |
| floor_area_sqm | Living area in sqm |
| storey_range | Floor range of flat |
| flat_model | Flat model type |
| lease_commence_date | Lease start year |

---

## Project Structure

```bash
├── train.py           # Trains model and saves artifacts
├── predict.py         # API service for predictions
├── model.pkl          # Trained model (generated after training)
├── preprocessor.pkl   # Data transformer (generated after training)
├── Dockerfile         # Docker deployment setup
└── README.md
```

## ⚙️ How to Run the Project

### Train the Model
Run model training and export artifacts:

```bash
python train.py
```
The train.py script handles data preparation, feature engineering, model training, and persistence (saving the model).
....

### Start the web service locally
```bash 
python predict.py
```
The service will start on http://127.0.0.1:5000 (or the specific port defined in predict.py).

### Testing the API Endpoint
You can now send a sample request to the /predict endpoint.

Endpoint: POST http://127.0.0.1:5000/predict

Sample JSON Request Body:

```bash
{
    "month": "2023-01",
    "town": "WOODLANDS",
    "flat_type": "4 ROOM",
    "block": "708",
    "street_name": "WOODLANDS DR 70",
    "storey_range": "04 TO 06",
    "floor_area_sqm": 102.0,
    "lease_commence_date": 1996
}
```

## Deployment (Docker)
To run the application inside a container, which ensures reproducibility across environments:

```bash
# 1. Build the Docker image (Name it 'hdb-predictor')
docker build -t hdb-predictor .

# 2. Run the container, mapping the container's port 5000 to the host's port 8080
docker run -d -p 8080:5000 --name hdb-service hdb-predictor
The service will now be available at http://localhost:8080/predict.
```