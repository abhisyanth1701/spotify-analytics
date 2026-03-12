import pandas as pd

def load_data():
    df=pd.read_csv("data/dataset.csv")
    return df

def explore_data(df):
    print("Shape of the dataset:", df.shape)
    print("\nColumns:",df.columns.tolist())
    print("\nFirst 5 rows:")
    print(df.head())