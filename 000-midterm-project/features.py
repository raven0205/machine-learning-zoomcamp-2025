# 000-midterm-project/features.py
import pandas as pd
import numpy as np
from typing import List

# Define the helper function outside of wrangling
def get_avg_storey(storey_range: str) -> float:
    """Extracts the average storey number (e.g., '04 TO 06' -> 5.0)."""
    if pd.isna(storey_range): 
        return np.nan
        
    try:
        low, high = map(int, storey_range.split(' TO '))
        return (low + high) / 2
    except (ValueError, AttributeError):
        # CORRECTED: Use np.nan for missing float values instead of pd.NA
        return np.nan 

def wrangling(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs data cleaning, date parsing, and feature engineering 
    specifically for the HDB Resale Price model.
    """
    df = df.copy()
    
    # 1. Date Parsing and Year/Month Extraction
    df["month"] = pd.to_datetime(df["month"], errors='coerce') 
    df['year_of_sale'] = df['month'].dt.year

    # 2. Rename for Clarity and Calculate Remaining Lease
    df = df.rename(columns={'lease_commence_date': 'lease_commence_year'})
    
    # Calculate remaining lease years
    df['remaining_lease_years'] = (
        99 - (df['year_of_sale'] - df['lease_commence_year'])
    )

    # 3. Feature Extraction: Average Storey (Uses the helper function)
    df['avg_storey'] = df['storey_range'].apply(get_avg_storey)
    
    # 4. Drop Source Columns
    df = df.drop(columns=[
        'month',
        'year_of_sale', 
        'storey_range',           # Source of avg_storey
        'lease_commence_year'     # Source of remaining_lease_years
    ], axis=1)

    # 5. Handle missing values
    df = df.dropna(subset=[
        'remaining_lease_years', 
        'avg_storey', 
        'floor_area_sqm', 
        'resale_price'
    ]).reset_index(drop=True)
    
    return df

def get_feature_names() -> List[str]:
    """
    Returns the final list of feature names used for modeling.
    """
    feature_names = [
        "town",
        "flat_type",
        "floor_area_sqm",
        "remaining_lease_years",
        "avg_storey"
    ]
    return feature_names

def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Splits the DataFrame into features and target variable."""
    target_name = "resale_price"
    
    X = df.loc[:, get_feature_names()]
    y = df[target_name]
    
    return X, y