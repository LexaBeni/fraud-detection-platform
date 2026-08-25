from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import average_precision_score, roc_auc_score, f1_score, precision_score, recall_score

def get_preprocessor(X):
    cat_cols = X.select_dtypes(include=['object']).columns.tolist()

    num_cols = X.select_dtypes(include=['number']).columns.tolist()

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=True))])


    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, num_cols),
        ("cat", categorical_pipeline, cat_cols)])

    return preprocessor

def create_pipeline(X):
    preprocessor = get_preprocessor(X)

    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("model", LogisticRegression(max_iter=1000, class_weight="balanced", solver="liblinear"))])

    return pipe

def evaluate_model(model, X, y):
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:,1]

    return {"pr_auc": average_precision_score(y, probabilities),
            "roc_auc": roc_auc_score(y, probabilities),
            "precision": precision_score(y, predictions, zero_division=0),
            "recall": recall_score(y, predictions, zero_division=0),
            "f1": f1_score(y, predictions, zero_division=0)
            }