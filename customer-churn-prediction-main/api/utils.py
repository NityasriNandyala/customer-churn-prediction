import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "churn_model.pkl"
model = joblib.load(MODEL_PATH)

def get_reasons(data):
    reasons = []

    if data.MonthlyCharges > 80:
        reasons.append("High monthly charges")

    if data.Contract == "Month-to-month":
        reasons.append("Short-term contract")

    if data.tenure < 12:
        reasons.append("Low tenure")

    if data.SeniorCitizen == 1:
        reasons.append("Senior customer may benefit from extra support")

    if data.OnlineSecurity == "No" and data.InternetService != "No":
        reasons.append("No online security service")

    if data.PaymentMethod == "Electronic check":
        reasons.append("Electronic check payment method")

    return reasons

def get_action(prob):
    if prob > 0.8:
        return "Offer discount or retention call"
    elif prob > 0.6:
        return "Send promotional email"
    else:
        return "No immediate action needed"

def predict_churn(data):
    input_data = pd.DataFrame([{
        "gender": data.gender,
        "SeniorCitizen": data.SeniorCitizen,
        "Partner": data.Partner,
        "Dependents": data.Dependents,
        "tenure": data.tenure,
        "PhoneService": data.PhoneService,
        "OnlineSecurity": data.OnlineSecurity,
        "OnlineBackup": data.OnlineBackup,
        "DeviceProtection": data.DeviceProtection,
        "TechSupport": data.TechSupport,
        "StreamingTV": data.StreamingTV,
        "Contract": data.Contract,
        "PaperlessBilling": data.PaperlessBilling,
        "PaymentMethod": data.PaymentMethod,
        "MonthlyCharges": data.MonthlyCharges,
        "TotalCharges": data.TotalCharges,
        "InternetService": data.InternetService
    }])

    prediction = int(model.predict(input_data)[0])
    prob = float(model.predict_proba(input_data)[0][1])

    reasons = get_reasons(data)
    action = get_action(prob)

    return prediction, prob, reasons, action