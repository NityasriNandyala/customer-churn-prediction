import requests

url = "https://customer-churn-prediction-xkxz.onrender.com/predict"

data = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 70,
    "TotalCharges": 800,
    "Contract": "Month-to-month",
    "InternetService": "Fiber optic"
}

res = requests.post(url, json=data)
print(res.status_code)
print(res.text)