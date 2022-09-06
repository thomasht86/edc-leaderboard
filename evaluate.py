import numpy as np
from sklearn.metrics import mean_squared_error
import pandas as pd 

df_test = pd.read_csv("https://github.com/thomasht86/edc-leaderboard/raw/master/data/dummy.csv")

def validate_df(df):
    # Check if dataframe is valid
    is_valid = df.index.equals(df_test.index) & df.columns.equals(df_test.columns)
    return is_valid

def score_df(df):
    # Calculate nrmse of dataframe
    score = mean_squared_error(df_test["Value"], df["Value"])
    return score