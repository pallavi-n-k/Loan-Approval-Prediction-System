from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

# Load saved model
with open("loan_model.pkl", "rb") as file:
    model = pickle.load(file)

# Load scaler
with open("scaler.pkl", "rb") as file:
    scaler = pickle.load(file)

# Create FastAPI app
app = FastAPI()

# Input schema
class LoanData(BaseModel):
    Gender: int
    Married: int
    Dependents: int
    Education: int
    Self_Employed: int
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: int
    TotalIncome: float
    Income_Loan_Ratio: float
    EMI: float

# Home route
@app.get("/")
def home():
    return {"message": "Loan Prediction API Running"}

# Prediction route
@app.post("/predict")
def predict(data: LoanData):

    input_data = np.array([[
        data.Gender,
        data.Married,
        data.Dependents,
        data.Education,
        data.Self_Employed,
        data.ApplicantIncome,
        data.CoapplicantIncome,
        data.LoanAmount,
        data.Loan_Amount_Term,
        data.Credit_History,
        data.Property_Area,
        data.TotalIncome,
        data.Income_Loan_Ratio,
        data.EMI
    ]])

    # Scale input
    scaled_data = scaler.transform(input_data)

    # Prediction
    prediction = model.predict(scaled_data)

    result = "Approved" if prediction[0] == 1 else "Rejected"

    return {
        "Loan Prediction": result
    }
