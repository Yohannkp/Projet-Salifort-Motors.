import streamlit as st
import requests

# Configuration de la page
st.set_page_config(page_title="Prédiction du Turnover", layout="centered")

# Style CSS avec effet Glassmorphism
st.markdown(
    """
    <style>
        body {
            background-color: #eef2f3;
        }
        .main {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .stSlider > div > div {
            color: #007BFF;
        }
        .stRadio > div {
            display: flex;
            justify-content: center;
        }
        .stSelectbox > div > div {
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre et description
st.markdown("<h1 style='text-align: center;'>🔍 Prédiction du Turnover</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Utilisez cette application pour prédire si un employé va quitter l'entreprise.</p>", unsafe_allow_html=True)

# Conteneur avec effet Glassmorphism
with st.container():
    with st.form("employee_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            last_evaluation = st.slider("Dernière évaluation", 0.0, 1.0, 0.7)
            number_project = st.number_input("Nombre de projets", 1, 10, 3)
            tenure = st.number_input("Années passées dans l'entreprise", 1, 20, 5)
            work_accident = st.radio("A eu un accident de travail ?", ["Non", "Oui"])
        
        with col2:
            promotion_last_5years = st.radio("A reçu une promotion ?", ["Non", "Oui"])
            salary = st.selectbox("Niveau de salaire", ["Faible", "Moyen", "Élevé"], index=1)
            overworked = st.radio("Est surmené ?", ["Non", "Oui"])
            department = st.selectbox("Département", ["IT", "RandD", "accounting", "hr", "management",
                                                       "marketing", "product_mng", "sales", "support", "technical"])

        submitted = st.form_submit_button("🔍 Prédire le Turnover")

# Mapping pour les valeurs numériques
salary_mapping = {"Faible": 0, "Moyen": 1, "Élevé": 2}
department_list = ["IT", "RandD", "accounting", "hr", "management",
                   "marketing", "product_mng", "sales", "support", "technical"]
work_accident = 1 if work_accident == "Oui" else 0
promotion_last_5years = 1 if promotion_last_5years == "Oui" else 0
overworked = 1 if overworked == "Oui" else 0

# Encodage one-hot du département
department_encoding = {dept: 0 for dept in department_list}
department_encoding[department] = 1  # Mettre à 1 le département sélectionné

# Préparation des données pour l'API
data = {
    "last_evaluation": last_evaluation,
    "number_project": number_project,
    "tenure": tenure,
    "work_accident": work_accident,
    "promotion_last_5years": promotion_last_5years,
    "salary": salary_mapping[salary],
    "overworked": overworked
}
data.update({f"department_{dept}": value for dept, value in department_encoding.items()})

# Envoi des données à l'API et affichage des résultats
if submitted:
    url = "https://projet-salifort-motors-production.up.railway.app/predict"  # Met l'URL correcte de ton API
    response = requests.post(url, json=data)
    st.write("Réponse de l'API :", response.json())

    
    if response.status_code == 200 or 201:
        
        try:
            result = response.json()
            st.success(f"**Résultat : {result['turnover_prediction']} avec une probabilité de {result['probability']}**")
        except requests.exceptions.JSONDecodeError:
            st.error("⚠️ L'API a répondu mais la réponse n'est pas en format JSON valide.")
            st.write("Réponse brute :", response.text)
    else:
        st.error(f"❌ Erreur {response.status_code} lors de la connexion à l'API.")
        st.write("Réponse brute :", response.text)
