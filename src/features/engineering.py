import pandas as pd
import numpy as np

base_features = ['TransactionDT', "TransactionAmt", "ProductCD", "P_emaildomain", "R_emaildomain"]
extended_features = base_features + ["card1", "card2", "card4", "card5", "card6", "addr1", "addr2", "dist1", "dist2", "D1"]
symbols = ['D',"card", "addr", "dist"]
def add_missing_features(df):

    df_copy = df.copy()

    df_copy['missing_count'] = df_copy[extended_features].isna().sum(axis=1)

    for i in symbols:
        df_copy[f'missing_{i}_count'] = df_copy.filter(regex = f"^{i}").isna().sum(axis=1)

    return df_copy

def add_time_features(df):

    df = df.copy()

    df["transaction_day"] = df["TransactionDT"] // 86400

    df["transaction_hour"] = (df["TransactionDT"] % 86400) // 3600

    return df


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

top_10_emails = ['gmail.com',
 'yahoo.com',
 'hotmail.com',
 'anonymous.com',
 'aol.com',
 'comcast.net',
 'icloud.com',
 'outlook.com',
 'msn.com',
 'att.net']

def add_email_features(df, usual_emails):
    df = df.copy()
    
    for col in ["P_emaildomain", "R_emaildomain"]:
        df[f'{col}_is_missing'] = df[col].isna().astype(int)

        df[f"{col}_provider"] = df[col].fillna("missing").str.split(".").str[0]

    df['domain_math'] = (df["P_emaildomain"].fillna("missing") == df["R_emaildomain"].fillna("missing")).astype(int)

    is_p_unusual = ~df["P_emaildomain"].isin(usual_emails)
    is_r_unusual = ~df["R_emaildomain"].isin(usual_emails)

    df['is_unusual_email'] = (is_p_unusual | is_r_unusual).astype(int)

    return df

def add_combined_features(df):
    card4_clean = df["card4"].fillna("missing").astype(str)
    card6_clean = df["card6"].fillna("missing").astype(str)
    product_clean = df["ProductCD"].fillna("missing").astype(str)
    card1_str = df["card1"].fillna(-1).astype(int).astype(str)
    card2_str = df["card2"].fillna(-1).astype(int).astype(str)
    addr1_str = df["addr1"].fillna(-1).astype(int).astype(str)

    df["card_product"] = card4_clean + "_" + product_clean
    df["email_product"] = df["P_emaildomain"].fillna("missing").astype(str) + "_" + product_clean
    df["card_addr"] = card1_str + "_" + addr1_str
    df["card2_product"] = card2_str + "_" + product_clean
    df["card4_card6"] = card4_clean + "_" + card6_clean
    df["card2_card4"] = card2_str + "_" + card4_clean

    return df


def create_advanced_time_features(df):
    df = df.copy()

    df["transaction_weekday"] = df["transaction_day"] % 7

    df["is_weekend"] = (df["transaction_weekday"] >= 5).astype(int)

    df['is_night'] = ((df["transaction_hour"] < 6) | (df['transaction_hour'] >= 22)).astype(int)

    return df


def add_distance_features(df):
    df = df.copy()

    df["dist1_is_missing"] = df["dist1"].isna().astype("int8")
    df["dist2_is_missing"] = df["dist2"].isna().astype("int8")

    return df

def add_all_features(df):
    df = add_missing_features(df)
    df = add_time_features(df)
    df = add_amount_features(df)
    df = create_d_time_features(df)
    df = add_email_features(df, top_10_emails)
    df = add_combined_features(df)
    df = add_distance_features(df)
    df = create_advanced_time_features(df)

    drop_cols = ["TransactionDT", "transaction_day", "transaction_hour"]

    df = df.drop(columns=[col for col in drop_cols if col in df.columns])
    return df