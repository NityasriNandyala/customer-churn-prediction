import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import GradientBoostingClassifier

def train_model(data_path):
    df = pd.read_csv(data_path)

    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df = df.dropna()

    model_features = [
        "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
        "PhoneService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "Contract", "PaperlessBilling",
        "PaymentMethod", "MonthlyCharges", "TotalCharges", "InternetService",
    ]
    X = df[model_features]
    y = df["Churn"].map({"Yes": 1, "No": 0})

    numeric_features = ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]
    categorical_features = [
        "gender", "Partner", "Dependents", "PhoneService", "OnlineSecurity",
        "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
        "Contract", "PaperlessBilling", "PaymentMethod", "InternetService",
    ]

    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ])

    pipeline = Pipeline([
        ("preprocessing", preprocessor),
        ("model", GradientBoostingClassifier())
    ])

    pipeline.fit(X, y)

    return pipeline