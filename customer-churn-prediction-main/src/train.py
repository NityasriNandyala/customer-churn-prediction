import joblib
import os
from src.pipeline import train_model

MODEL_PATH = "models/churn_model.pkl"
DATA_PATH = "data/raw/Customer-Churn.csv"


def main():
    os.makedirs("models", exist_ok=True)

    model = train_model(DATA_PATH)

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved at {MODEL_PATH}")


if __name__ == "__main__":
    main()