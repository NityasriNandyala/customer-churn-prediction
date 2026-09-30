import joblib
import pandas as pd

MODEL_PATH = "models/churn_model.pkl"


def load_model():
    return joblib.load(MODEL_PATH)


def predict(data: dict):
    model = load_model()
    df = pd.DataFrame([data])

    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]

    return pred, prob