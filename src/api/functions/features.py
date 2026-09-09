import pandas as pd

from src.api.schemas.prediction import PredictionRequest
from src.features.engineering import add_all_features


def prepare_all_features(payload: PredictionRequest):
    row = payload.model_dump()

    df = pd.DataFrame([row])

    df = add_all_features(df)

    return df
