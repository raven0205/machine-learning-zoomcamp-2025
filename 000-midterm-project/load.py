# 000-midterm-project/load.py
import pandas as pd
from typing import List, Dict, Union

# month	town	flat_type	block	street_name	storey_range	floor_area_sqm	lease_commence_date	resale_price

# Map your CSV columns to the right pandas dtypes
dtype_map: Dict[str, Union[str, pd.CategoricalDtype]] = {
    "month": "string", # e.g., "2020-01", "2021-June"
    "town": "string",  # e.g., "ANG MO KIO"
    "block": "string",  # e.g., "123A"
    "flat_type": "category", # "1 ROOM", "2 ROOM", etc.
    "street_name": "string",  # e.g., "ANG MO KIO AVE 3"
    "storey_range": "string",  # "01 TO 03", "04 TO 06", etc.
    "floor_area_sqm": "float64", # e.g., 45.0, 75.5
    "lease_commence_date": "Int64", # e.g., 1985, 1990
    "resale_price": "float64" # e.g., 250000.0, 550000.0
}

# List the date columns to parse
parse_date_map: List[str] = [
    "month"
]   

# List all strings that should be treated as NaN
na_values_map: List[str] = ["", "NA", "N/A", "na", "n/a"]

def load_data(
        path: str = None,
        parse_dates: List[str] = parse_date_map,
        na_values: List[str] = na_values_map) -> pd.DataFrame:
    """Load the HDB resale data from a CSV file with proper dtypes, date parsing, and NaN handling."""
    # Load the data
    if path is None:
        raise ValueError("A valid file path must be provided to load the data.")
    
    df = pd.read_csv(
        path,
        dtype=dtype_map,
        parse_dates=parse_dates,
        na_values=na_values,
        keep_default_na=True,
    )
    
    return df

