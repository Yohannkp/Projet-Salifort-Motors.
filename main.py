from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel
import uvicorn
import os

# Charger le modèle entraîné
# with open("hr_rf2.pickle", "rb") as file:
#     model = pickle.load(file)  
model_path = os.path.join(os.path.dirname(__file__), "hr_rf2.pickle")

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Le fichier {model_path} est introuvable sur Railway !")

with open(model_path, "rb") as file:
    model = pickle.load(file)

# print("Nombre de features attendus :", model.n_features_in_)
# # Vérifier si le modèle a stocké les noms des features
# if hasattr(model, "feature_names_in_"):
#     print("Features attendues :", model.feature_names_in_)
# else:
#     print("Le modèle n'a pas stocké les noms des features.")

# Définition de l'API FastAPI
app = FastAPI(title="Turnover Prediction API", description="Prédit si un employé va quitter l'entreprise", version="1.0")

# Page d'accueil
@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de prédiction du turnover des employés. Utilisez l'endpoint /predict pour envoyer des données."}

# Schéma des données d'entrée
class EmployeeData(BaseModel):
    last_evaluation: float
    number_project: int
    tenure: int
    work_accident: int
    promotion_last_5years: int
    salary: int
    department_IT: int
    department_RandD: int
    department_accounting: int
    department_hr: int
    department_management: int
    department_marketing: int
    department_product_mng: int
    department_sales: int
    department_support: int
    department_technical: int
    overworked: int


@app.post("/predict")
def predict_turnover(data: EmployeeData):
    # Convertir les données en tableau numpy
    input_data = np.array([[
        data.last_evaluation,
        data.number_project,
        data.tenure,
        data.work_accident,
        data.promotion_last_5years,
        data.salary,
        data.department_IT,
        data.department_RandD,
        data.department_accounting,
        data.department_hr,
        data.department_management,
        data.department_marketing,
        data.department_product_mng,
        data.department_sales,
        data.department_support,
        data.department_technical,
        data.overworked
    ]])
    
    # Vérifier la taille des features envoyées
    print("Données reçues :", data.dict())
    print("Nombre de features envoyées :", input_data.shape[1])
    
    # Prédiction
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    
    return {"turnover_prediction": int(prediction), "probability": round(float(probability), 4)}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Railway définit dynamiquement le port
    uvicorn.run(app, host="", port=port)
