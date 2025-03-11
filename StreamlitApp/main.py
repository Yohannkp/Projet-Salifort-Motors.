import streamlit as st
import requests

# Configuration de la page
st.set_page_config(page_title="Prédiction du Turnover", layout="wide")

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
        last_evaluation = st.slider("Dernière évaluation", 0.0, 1.0, 0.7)
        number_project = st.number_input("Nombre de projets", 1, 10, 3)
        tenure = st.number_input("Ancienneté dans l'entreprise (années)", 1, 10, 3)
        work_accident = st.radio("A eu un accident de travail ?", ["Non", "Oui"])
        promotion_last_5years = st.radio("Promotion dans les 5 dernières années ?", ["Non", "Oui"])
        overworked = st.radio("Est-il surmené ?", ["Non", "Oui"])
    
    with col2:
        salary = st.selectbox("Niveau de salaire", ["Faible", "Moyen", "Élevé"], index=1)
        
        # Sélection du département avec encodage one-hot
        department = st.selectbox(
            "Département", 
            ["IT", "RandD", "Accounting", "HR", "Management", "Marketing",
             "Product Management", "Sales", "Support", "Technical"]
        )
    
    submitted = st.form_submit_button("🔍 Prédire le Turnover")

# Mapping des valeurs pour correspondre aux attentes du modèle
work_accident = 1 if work_accident == "Oui" else 0
promotion_last_5years = 1 if promotion_last_5years == "Oui" else 0
overworked = 1 if overworked == "Oui" else 0
salary_mapping = {"Faible": 0, "Moyen": 1, "Élevé": 2}
salary = salary_mapping[salary]

# Encodage one-hot pour le département
department_mapping = {
    "IT": "department_IT",
    "RandD": "department_RandD",
    "Accounting": "department_accounting",
    "HR": "department_hr",
    "Management": "department_management",
    "Marketing": "department_marketing",
    "Product Management": "department_product_mng",
    "Sales": "department_sales",
    "Support": "department_support",
    "Technical": "department_technical"
}

# Initialisation des valeurs one-hot
department_encoded = {key: 0 for key in department_mapping.values()}
department_encoded[department_mapping[department]] = 1

# Construction des données à envoyer à l'API
data = {
    "last_evaluation": last_evaluation,
    "number_project": number_project,
    "tenure": tenure,
    "work_accident": work_accident,
    "promotion_last_5years": promotion_last_5years,
    "salary": salary,
    "overworked": overworked,
    **department_encoded  # Ajout des départements encodés
}

# Envoi des données à l'API et affichage des résultats
if submitted:
    url = "https://projet-salifort-motors-production.up.railway.app/predict"  # Vérifie que FastAPI tourne sur ce port
    st.write("Données envoyées à l'API :", data)  # Debugging
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        try:
            result = response.json()
            
            # Interprétation de la prédiction
            prediction_text = "L'employé va rester dans l'entreprise" if result["turnover_prediction"] == 0 else "⚠️ L'employé risque de partir !"
            probability = result["probability"]

            # Affichage du résultat avec une barre de progression
            st.success(f"**Résultat : {prediction_text}**")
            st.progress(int(probability * 100))  # Convertir en pourcentage
            
            st.write(f"📊 **Probabilité de départ : {probability * 100:.2f}%**")
            
        except requests.exceptions.JSONDecodeError:
            st.error("⚠️ L'API a répondu mais la réponse n'est pas en format JSON valide.")
            st.write("Réponse brute :", response.text)
    else:
        st.error(f"❌ Erreur {response.status_code} - Vérifie si les données envoyées sont correctes.")
        st.write("Réponse brute :", response.text)
