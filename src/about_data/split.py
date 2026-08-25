import pandas as pd
import numpy as np

def temporal_split(df, train_end, val_end):
    train = df[df["TransactionDT"] < train_end].copy()
    val = df[(df["TransactionDT"] >= train_end) &(df["TransactionDT"] < val_end)].copy()
    test = df[df["TransactionDT"] >= val_end].copy()

    return train, val, test

