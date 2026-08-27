import pandas as pd
import numpy as np

base_features = ['TransactionDT', "TransactionAmt", "ProductCD", "P_emaildomain", "R_emaildomain"]
extended_features = base_features + ["card1", "card2", "card4", "card5", "card6", "addr1", "addr2", "dist1", "dist2", "D1"]
symbols = ['V', 'D', 'M', 'C', 'id', "card", "addr", "dist"]
def add_missing_features(df):

    df_copy = df.copy()

    avail_cols = [c for c in df_copy.columns if c != 'isFraud']

    df_copy['missing_count'] = df_copy[avail_cols].isna().sum(axis=1)

    for i in symbols:
        df_copy[f'missing_{i}_count'] = df_copy.filter(regex = f"^{i}").isna().sum(axis=1)

    return df_copy

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

def add_amount_features(df):
    df = df.copy()

    df["transaction_amt_log"] = np.log1p(df["TransactionAmt"])

    df["amount_decimal"] = (df["TransactionAmt"] % 1)

    df["amount_rounded"] = (np.isclose(df["TransactionAmt"] % 1, 0, atol=1e-6) ).astype(int)

    return df

def create_d_time_features(df):
    df = df.copy()

    df["hour_sin"] = np.sin(2 * np.pi * df["transaction_hour"] / 24)

    df["hour_cos"] = np.cos(2 * np.pi * df["transaction_hour"] / 24)

    return df

top_15_emails = ['protonmail.com',
 'hotmail.de',
 'aim.com',
 'yahoo.co.jp',
 'ptd.net',
 'servicios-ta.com',
 'twc.com',
 'q.com',
 'suddenlink.net',
 'cableone.net',
 'netzero.com',
 'frontiernet.net',
 'centurylink.net',
 'sc.rr.com',
 'netzero.net']

def add_email_features(df, unusual_emails):
    df = df.copy()
    
    for col in ["P_emaildomain", "R_emaildomain"]:
        df[f'{col}_is_missing'] = df[col].isna().astype(int)

        df[f"{col}_provider"] = df[col].fillna("missing").str.split(".").str[0]

    df['domain_math'] = (df["P_emaildomain"].fillna("missing") == df["R_emaildomain"].fillna("missing")).astype(int)

    is_p_unusual = df["P_emaildomain"].isin(unusual_emails)
    is_r_unusual = df["R_emaildomain"].isin(unusual_emails)

    df['is_unusual_email'] = (is_p_unusual | is_r_unusual).astype(int)

    return df

def add_combined_features(df):
    df = df.copy()
    df["card_product"] = df["card4"].astype(str) + "_" + df["ProductCD"].astype(str)
    df["email_product"] = df["P_emaildomain"].astype(str) + "_" + df["ProductCD"].astype(str)
    df["card_addr"] = df["card1"].astype(str) + "_" + df["addr1"].astype(str)

    return df

def add_group_aggregations(df):
    df = df.copy()

    df["uid"] = (df["card1"].astype(str) + "_" + df["card2"].astype(str) + "_" + df["card5"].astype(str) + "_" + df["addr1"].astype(str) + "_" + df["D1"].astype(str))

    uid_mean = df.groupby("uid")['TransactionAmt'].transform("mean")
    uid_std = df.groupby("uid")['TransactionAmt'].transform("std")

    df['TransactionAmt_to_mean_uid'] = df['TransactionAmt'] / (uid_mean + 1e-5)
    df['TransactionAmt_to_std_uid'] = (df['TransactionAmt'] - uid_mean) / (uid_std + 1e-5)

    return df

def create_d_features(df):
    df = create_engineered_features(df)
    df = add_amount_features(df)
    df = create_d_time_features(df)
    df = add_email_features(df, top_15_emails)
    df = add_combined_features(df)

    return df

def create_d_aggregations_features(df):
    df = create_d_features(df)
    df = add_group_aggregations(df)

    if "uid" in df.columns.tolist():
            df = df.drop(columns=["uid"])

    return df

def create_advanced_time_features(df):
    df = df.copy()

    df["transaction_weekday"] = df["transaction_day"] % 7

    df["is_weekend"] = (df["transaction_weekday"] >= 5).astype(int)

    df['is_night'] = ((df["transaction_hour"] < 6) | (df['transaction_hour']) >= 22).astpe(int)

    return df

def add_interaction_features(df):
    df = df.copy()

    df["card2_product"] = (df["card2"].astype(str) + "_" + df["ProductCD"].astype(str))

    df["card4_card6"] = (df["card4"].astype(str) + "_" + df["card6"].astype(str))

    df["card2_card4"] = (df["card2"].astype(str) + "_" + df["card4"].astype(str))

    return df

def add_distance_features(df):
    df = df.copy()

    df["dist_diff"] = df["dist1"] - df["dist2"]

    df["dist_sum"] = df["dist1"] + df["dist2"]

    return df