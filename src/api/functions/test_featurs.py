from src.api.functions.features import prepare_all_features
from src.api.schemas.prediction import PredictionRequest

def test_prepare_all_features():
    payload = PredictionRequest(
        TransactionDT=123456,
        TransactionAmt=100.50,
        ProductCD="W",
        P_emaildomain="gmail.com",
        card1=1234,
        card4="visa",
        card6="debit",
    )

    df = prepare_all_features(payload)

    assert len(df) == 1
    assert len(df.columns) == 45
    assert "isFraud" not in df.columns
    print(len(df.columns))

test_prepare_all_features()