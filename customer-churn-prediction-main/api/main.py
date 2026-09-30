from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.schema import CustomerData
from api.utils import predict_churn

app = FastAPI(title="Customer Churn Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "Churn Prediction API is running"}

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Ready to handle requests"}

@app.post("/predict")
def predict(data: CustomerData):
    try:
        prediction, prob, reasons, action = predict_churn(data)

        return {
            "churn_prediction": "Yes" if prediction == 1 else "No",
            "probability": round(float(prob), 2),
            "reasons": reasons,
            "recommended_action": action
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred during prediction processing: {str(e)}"
        )