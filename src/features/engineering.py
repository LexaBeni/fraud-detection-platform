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

def add_amount_features(df):
    df = df.copy()

    df["transaction_amt_log"] = np.log1p(df["TransactionAmt"])

    df["amount_decimal"] = (df["TransactionAmt"] % 1)

    return df

def create_d_time_features(df):
    df = df.copy()

    df["hour_sin"] = np.sin(2 * np.pi * df["transaction_hour"] / 24)

    df["hour_cos"] = np.cos(2 * np.pi * df["transaction_hour"] / 24)

    return df

top_10_emails = ['servicios-ta.com',
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

def create_d_features(df):
    df = create_engineered_features(df)
    df = add_amount_features(df)
    df = create_d_time_features(df)
    df = add_email_features(df, top_10_emails)
    df = add_combined_features(df)
    return df