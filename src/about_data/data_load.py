import pandas as pd
from dotenv import load_dotenv
import os

def load_df(data_path):
    transaction_path = os.path.join(data_path, r"raw/train_transaction.csv/train_transaction.csv")
    identity_path = os.path.join(data_path, r"raw/train_identity.csv/train_identity.csv")
    transaction_df = pd.read_csv(transaction_path)
    identity_df = pd.read_csv(identity_path)
    full_df = transaction_df.merge(identity_df, on="TransactionID", how="left")
    full_df = full_df.sort_values("TransactionDT").reset_index(drop=True)