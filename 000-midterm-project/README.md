## HDB Resale Price Prediction Model Deployment

<img src="image/house.webp" alt="HDB Resale Price" width="200"/>

**Project Overview** 
* This project implements and deploys a machine learning model designed to forecast the resale prices of Housing and Development Board (HDB) flats in Singapore. The aim is to allow stakeholders like real estate analysts, investors or buyers to learn about the recent trend and estimate property worth for their decision-making. The final deliverable is a containerized web service that provides real-time price predictions via a simple API endpoint.

**Data**
* The model uses processed HDB resale transaction data from 2019-2023, as `data/hdb_resale_data_2019-2023.csv`.
The full dataset can be downloaded from [Resale Flat Prices | HDB | data.gov.sg](https://data.gov.sg/datasets?topics=housing&resultId=189).


## Data Fields
The dataset used contains all the listed features, excluding `Flat Model` and `Remaining Lease`, which are included only in the revised version of the dataset on the website.

| Column Name | Description | Examples    |
|------------|-------------|--------------|
| month | Month of sale (YYYY-MM) | 2021-01 |
| town | Flat location | WOODLANDS |
| flat_type | Type of flat | EXECUTIVE |
| block | Block number | 23 |
| street_name | Name of street | WOODLANDS DR 70 |
| floor_area_sqm | Living area in sqm |  70 |
| storey_range | Floor range of flat | 01 TO 03 |
| lease_commence_date | Lease start year | 2012 |
| resale_price | Price (in SGD Dollars) | 520000 |

---

## Project Structure

```bash

000-midterm-project  # hdb-price-predictor project
├── image
|   └── house.webp
├── Dockerfile   # Docker deployment setup
├── features.py  # 2. To clean and extract the feature
├── load.py      # 1. To load the dataset
├── main.py      # 4. To consolidate: load -> clean -> train "__main__"
├── model.pkl    # 5. output: trained model 
├── Pipfile
├── Pipfile.lock
├── predict.py   # 6. To run the FastAPI service for predictions "@app"
├── README.md    
├── test.py      # 7. A sample test file to predict on
├── train.py     # 3. To split data and save trained model
└── data
    └── hdb_resale_data_202...csv
```

## ⚙️ How to Run the Project

This project predicts HDB resale prices using a trained machine learning model and serves predictions via a FastAPI API.

### 1️⃣ Clone the Repository
```bash
# Go to the main page of the repository you want to clone
git clone <repository_url> <directory_name>

# Navigate into the new directory and check its contents
cd <project_folder_name>
ls
```
### 2️⃣ Setup Python Environment (Pipenv)
```bash
# Install dependencies
pipenv install

# Activate virtual environment
pipenv shell
```

### 3️⃣ Train the Model (Optional)
The train.py script handles data preparation, feature engineering, model training, and saving the model as `model.pkl`.
If you want to retrain the model:
```bash
python main.py
```

### 4️⃣ Run the FastAPI Service
The service will start on http://127.0.0.1:9696 (or the specific port defined in predict.py).

Swagger UI for testing: http://127.0.0.1:9696/docs
```bash 
# run the FastAPI server
python predict.py
```


### 5️⃣ Test Predictions
In Pipenv shell, you can use test.py or curl to send a sample request to the /predict endpoint: POST http://localhost:9696/predict

* Method 1: Run the prediction on `test.py` to send request

```bash
# Run the test file containing JSON request body
python test.py
```
* Method 2: Run the cURL to send request
```bash
curl -X POST "http://127.0.0.1:9696/predict" \
-H "Content-Type: application/json" \
-d '{
  "month":"2024-06",
  "town":"WOODLANDS",
  "flat_type":"4 ROOM",
  "block":"754",
  "street_name":"WOODLANDS AVE 4",
  "storey_range":"07 TO 09",
  "floor_area_sqm":90.0,
  "lease_commence_date":1986
}'
```

## 🚀 Running the Project with Docker (Alternative)
If you want to run the HDB Resale Price Predictor without installing Python or dependencies locally, you can use Docker.

### 1️⃣ Build the Docker Image
From the project root (`000-midterm-project`), run:

```bash
docker build -t hdb-resale-api .
```
### 2️⃣ Run the Docker Container

Start the container and map the container port `9696` to your local machine (e.g., `8080`):

```bash
docker run -p 8080:9696 --name hdb-api hdb-resale-api
```
The service will now be available at http://localhost:8080/predict.

### 3️⃣ Access the FastAPI Service

Once the container is running, you can test predictions via cURL:
```curl
curl -X POST "http://127.0.0.1:8080/predict" \
-H "Content-Type: application/json" \
-d '{
  "month":"2024-06",
  "town":"WOODLANDS",
  "flat_type":"4 ROOM",
  "block":"754",
  "street_name":"WOODLANDS AVE 4",
  "storey_range":"07 TO 09",
  "floor_area_sqm":90.0,
  "lease_commence_date":1986
}'

```

For more information, you can open the API documentation in your browser:
http://localhost:8080/docs
