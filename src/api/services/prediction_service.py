from src.api.functions.features import prepare_all_features
from src.api.models.prediction import Prediction
from src.api.core.logger import logger
from src.roles import UserRole
from src.api.models.prediction import Prediction
from sqlalchemy import select
from src.api.core.exceptions import PredictionNotFound

class PredictionService:

    def __init__(self, model, db):
        self.db = db
        self.model = model

    def predict(self, df, user, threshold: float = 0.18):
        if self.model is None:
            raise ValueError("Model is not found")

        try:
            df = prepare_all_features(df)

            prob = (self.model.predict_proba(df)[0, 1])

            pred = int((prob > threshold))
        except Exception as e:
            logger.exception(e)
            raise ValueError("Invalid payload.")

        label = "FRAUD" if pred == 1 else "VALID"

        prediction_db = Prediction(
            prediction_probability = prob,
            prediction = pred,
            threshold = threshold,
            label = label,
            user_id = user.id)

        self.db.add(prediction_db)
        self.db.commit()
        self.db.refresh(prediction_db)

        return{
            "prediction" : label,
            "probability": round(float(prob), 4)
        }

    def get_prediction(self, prediction_id: int, user):

        stmt = select(Prediction).where(Prediction.id == prediction_id)

        if user.role != UserRole.ADMIN:
            stmt = stmt.where(Prediction.user_id == user.id)

        result = self.db.execute(stmt).scalar_one_or_none()

        if not result:
            raise PredictionNotFound(prediction_id)
        return {
            "prediction": result.label,
            "probability": round(float(result.prediction_probability), 4),
            "threshold": result.threshold,
            "created_at": result.created_at,
        }

    def get_prediction_history(self, user, condition, offset, limit):
        stmt = select(Prediction)

        if user.role != UserRole.ADMIN:
            stmt = stmt.where(Prediction.user_id == user.id)

        if condition:
            stmt = stmt.where(Prediction.label == condition)

        stmt = stmt.order_by(Prediction.created_at.desc()).offset(offset).limit(limit)

        result = self.db.execute(stmt).scalars().all()

        return [
            {
                "prediction": prediction.label,
                "probability": round(float(prediction.prediction_probability), 4),
                "threshold": prediction.threshold,
                "created_at": prediction.created_at,
            }
            for prediction in result
        ]

    def delete_prediction(self, prediction_id, user):
        stmt = select(Prediction).where(Prediction.id == prediction_id)

        if user.role != UserRole.ADMIN:
            stmt = stmt.where(Prediction.user_id == user.id)

        prediction = self.db.execute(stmt).scalar_one_or_none()

        if not prediction:
            raise PredictionNotFound(prediction_id)

        self.db.delete(prediction)

        self.db.commit()