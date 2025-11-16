# 000-midterm-project/main.py
    
from load import load_data
from features import split_features_target, wrangling
from train import train

if __name__ == "__main__":
    # import data
    df = load_data(path="data/hdb_resale_data_2019-2023.csv")

    # wrangle data
    df_clean = wrangling(df)

    # split features and target
    X, y = split_features_target(df_clean)

    # train and save the model
    train(X, y)
    print("Training completed! model.pkl saved.")