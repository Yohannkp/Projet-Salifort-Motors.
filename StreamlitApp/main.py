import streamlit as st
import requests

# Configuration de la page
st.set_page_config(page_title="Prédiction du Turnover des Employés", layout="centered")

# Style CSS personnalisé
st.markdown(
    """
    <style>
        .main { background-color: #f5f7fa; }
        div.stButton > button { width: 100%; padding: 10px; background-color: #007BFF; color: white; border-radius: 10px; }
        div.stButton > button:hover { background-color: #0056b3; }
        .stTextInput > div > div > input { border-radius: 10px; }
        .stSelectbox > div > div > select { border-radius: 10px; }
        .stSlider > div > div { color: #007BFF; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔍 Prédiction du Turnover des Employés")
st.write("**Utilisez cette application pour prédire si un employé est susceptible de quitter l'entreprise.**")

# Saisie des données de l'employé
with st.form("employee_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        satisfaction_level = st.slider("Niveau de satisfaction", 0.0, 1.0, 0.5)
        last_evaluation = st.slider("Dernière évaluation", 0.0, 1.0, 0.7)
        number_project = st.number_input("Nombre de projets", 1, 10, 3)
        average_montly_hours = st.number_input("Heures de travail mensuelles", 50, 400, 200)
    
    with col2:
        time_spend_company = st.number_input("Années passées dans l'entreprise", 1, 10, 3)
        work_accident = st.radio("A eu un accident de travail ?", ["Non", "Oui"])
        promotion_last_5years = st.radio("A reçu une promotion dans les 5 dernières années ?", ["Non", "Oui"])
        department = st.selectbox("Département", ["IT", "RH", "Comptabilité", "Ventes", "Support", "Technique", "Management"], index=0)
        salary = st.selectbox("Niveau de salaire", ["Faible", "Moyen", "Élevé"], index=1)
    
    submitted = st.form_submit_button("🔍 Prédire le Turnover")

# Mapping pour les valeurs numériques des catégories
department_mapping = {"IT": 0, "RH": 1, "Comptabilité": 2, "Ventes": 3, "Support": 4, "Technique": 5, "Management": 6}
salary_mapping = {"Faible": 0, "Moyen": 1, "Élevé": 2}
work_accident = 1 if work_accident == "Oui" else 0
promotion_last_5years = 1 if promotion_last_5years == "Oui" else 0

# Préparation des données pour l'API
data = {
    "satisfaction_level": satisfaction_level,
    "last_evaluation": last_evaluation,
    "number_project": number_project,
    "average_montly_hours": average_montly_hours,
    "time_spend_company": time_spend_company,
    "work_accident": work_accident,
    "promotion_last_5years": promotion_last_5years,
    "department": department_mapping[department],
    "salary": salary_mapping[salary]
}

# Envoi des données à l'API et affichage des résultats
if submitted:
    url = "http://127.0.0.1:8000/predict"  # Assurez-vous que FastAPI tourne sur ce port
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        st.success(f"**Résultat : {result['turnover_prediction']} avec une probabilité de {result['probability']}**")
        st.info(result["message"])
    else:
        st.error("❌ Erreur lors de la connexion à l'API. Vérifiez si FastAPI tourne correctement.")
