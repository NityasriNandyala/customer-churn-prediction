from pydantic import BaseModel

class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    MonthlyCharges: float
    TotalCharges: float
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    InternetService: str