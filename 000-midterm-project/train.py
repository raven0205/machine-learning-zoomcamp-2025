# 000-midterm-project/train.py
# train.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer

from features import wrangling, split_features_target
from load import load_data

MODEL_PATH = "model.pkl"

def train(X: pd.DataFrame, y: pd.Series) -> None:
    """Train a regression model to predict HDB resale prices."""

    # Identify categorical and numerical columns
    categorical_cols = ["town", "flat_type"]
    numerical_cols = ["floor_area_sqm", "remaining_lease_years", "avg_storey"]

    # Preprocessing: encoding + scaling
    preprocessor = ColumnTransformer(
        transformers=[
            # Numerical: Impute then Scale
            ("num", Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]), numerical_cols),
            # Categorical: Impute then OneHotEncode
            ("cat", Pipeline([('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('onehot', OneHotEncoder(handle_unknown="ignore"))]), categorical_cols),
        ],
        # Add a 'drop' step for high-cardinality columns if any
        remainder='drop'
    )

    # Full pipeline: preprocessing + model
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
        ]
    )

    # Train-test-val split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.25, random_state=42
    )  # 0.25 x 0.8 = 0.2

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate performance
    y_pred = model.predict(X_val)
    mse = mean_squared_error(y_val, y_pred)
    r2 = r2_score(y_val, y_pred)

    print("Model Performance")
    print(f"RMSE: {mse ** 0.5:,.2f}")
    print(f"R² Score: {r2:.4f}")

    # Save trained model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved as {MODEL_PATH}")

