from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel
import uvicorn

# Charger le modèle entraîné
with open("hr_rf2.pickle", "rb") as file:
    model = pickle.load(file)

# Définition de l'API FastAPI
app = FastAPI(title="Turnover Prediction API", description="Prédit si un employé va quitter l'entreprise", version="1.0")

# Page d'accueil
@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de prédiction du turnover des employés. Utilisez l'endpoint /predict pour envoyer des données."}

# Schéma des données d'entrée
class EmployeeData(BaseModel):
    satisfaction_level: float
    last_evaluation: float
    number_project: int
    average_montly_hours: int
    time_spend_company: int
    work_accident: int
    promotion_last_5years: int
    department: int
    salary: int

@app.post("/predict")
def predict_turnover(data: EmployeeData):
    # Convertir les données en tableau numpy
    input_data = np.array([[
        data.satisfaction_level,
        data.last_evaluation,
        data.number_project,
        data.average_montly_hours,
        data.time_spend_company,
        data.work_accident,
        data.promotion_last_5years,
        data.department,
        data.salary
    ]])
    
    # Prédiction
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    
    return {"turnover_prediction": int(prediction), "probability": round(float(probability), 4)}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
