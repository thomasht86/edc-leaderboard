import numpy as np
from sklearn.metrics import mean_absolute_error
import pandas as pd 

df_test = pd.read_csv("https://docs.google.com/spreadsheets/d/19ToQ6RTxCW_6h4-UPVmaNYXoyuvRaWLXjJaVR8-jdMw/export?format=csv")

def validate_df(df):
    # Check if dataframe is valid
    is_valid = df.index.equals(df_test.index) & df.columns.equals(df_test.columns)
    return is_valid

def score_df(df):
    # Calculate mae of dataframe
    score = mean_absolute_error(df_test["Value"], df["Value"])
    return score