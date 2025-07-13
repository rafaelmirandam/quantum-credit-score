from pydantic import BaseModel

class ClientData(BaseModel):
    Age: float
    Annual_Income: float
    Monthly_Inhand_Salary: float
    Num_Bank_Accounts: float
    Num_Credit_Card: float
    Interest_Rate: float
    Num_of_Loan: float
    Delay_from_due_date: float
    Num_of_Delayed_Payment: float
    Changed_Credit_Limit: float
    Outstanding_Debt: float
    Credit_Utilization_Ratio: float
    Total_EMI_per_month: float

    class Config:
        # Exemplo de dados para a documentação da API
        schema_extra = {
            "example": {
                "Age": 28.0,
                "Annual_Income": 55000.0,
                "Monthly_Inhand_Salary": 4500.0,
                "Num_Bank_Accounts": 3,
                "Num_Credit_Card": 4,
                "Interest_Rate": 12.0,
                "Num_of_Loan": 2,
                "Delay_from_due_date": 5,
                "Num_of_Delayed_Payment": 2,
                "Changed_Credit_Limit": 5.0,
                "Outstanding_Debt": 1500.0,
                "Credit_Utilization_Ratio": 30.5,
                "Total_EMI_per_month": 250.0
            }
        }

class PredictionResponse(BaseModel):
    client_id: str
    credit_score: str
    model_version: str