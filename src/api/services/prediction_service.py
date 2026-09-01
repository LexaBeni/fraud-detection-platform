from src.api.functions.features import prepare_all_features
from src.api.models.prediction import Prediction
from src.api.core.logger import logger

class PredictionService:

    def __init__(self, model, db):
        self.db = db
        self.model = model

    def predict(self, df, threshold: int | None = 18):
        if self.model is None:
            raise ValueError("Model is not found")

        df = prepare_all_features(df)

        try:
            prob = (self.model.predict_proba(df)[0, 1])

            pred = (prob > threshold).astype(int)
        except Exception as e:
            logger.exception(e)
            raise ValueError("Invalid payload.")

        label = "FRAUD" if pred == 1 else "VALID"

        prediction_db = Prediction(
            prediction_probability = prob,
            prediction = pred,
            threshold = threshold,
            label = label)

        self.db.add(prediction_db)
        self.db.commit()
        self.db.refresh(prediction_db)

        return{
            "prediction" : label,
            "probability": round(prob, 2)
        }

        

        





