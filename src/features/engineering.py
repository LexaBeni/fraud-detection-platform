import pandas as pd
import numpy as np

base_features = ['TransactionDT', "TransactionAmt", "ProductCD", "P_emaildomain", "R_emaildomain"]
extended_features = base_features + ["card1", "card2", "card4", "card6", "addr1", "addr2", "dist1", "dist2"]
symbols = ['V', 'D', 'M', 'C', 'id', "card", "addr", "dist"]
def add_missing_features(df):

    df= df.copy()

    df['missing_count'] = df.isna().sum(axis=1)

    for i in symbols:
        df[f'missing_{i}_count'] = df.filter(regex = f"^{i}").isna().sum(axis=1)

    return df

def add_time_features(df):

    df = df.copy()

    df["transaction_day"] = df["TransactionDT"] // 86400

    df["transaction_hour"] = (df["TransactionDT"] % 86400) // 3600

    return df

def create_engineered_features(df):
    result = df[extended_features].copy()

    missing_features = add_missing_features(df)
    missing_columns = ["missing_count", *[f"missing_{symbol}_count" for symbol in symbols],]
    result = result.join(missing_features[missing_columns])
    result = add_time_features(result)

    return result