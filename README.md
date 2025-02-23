# Recommander
Recommend part of the final product: Once the data has been retrieved from the user with the chatbot, we use it to recommend the right person to the user.   The expected result is a perfect match between the applicant and the professional



🔍 Fonctionnalité

Cette API prend en entrée un utilisateur et un dataset de profils (chercheurs & pros) et retourne les Top 3 recommandations les plus pertinentes, avec les critères les plus influents.
🚀 Guide d’Utilisation de l’API
1️⃣ Installation des dépendances

Avant d'exécuter l'API, assure-toi d'avoir Python installé.
Installe les dépendances avec :

pip install fastapi uvicorn scikit-learn pandas numpy

2️⃣ Lancer l’API

Dans le terminal, exécute :

uvicorn main:app --reload

    L’API sera accessible à http://127.0.0.1:8000.
    La documentation interactive Swagger est disponible à http://127.0.0.1:8000/docs.

3️⃣ Faire une Requête à l’API

Tu peux utiliser Postman, Curl ou un script Python pour tester l’API.
📌 Exemple de Requête POST en Python

import requests

# 📌 Définir les données d'entrée (utilisateur + dataset)
user_data = {
    "role": "chercheur",
    "language": "fr",
    "data": {
        "expectations": "Rencontrer des experts en data science",
        "about": "Je suis un chercheur en IA",
        "domain": "IA",
        "experience": "5 ans d'expérience en machine learning",
        "help": "Besoin d'échanger sur les nouvelles technologies IA",
        "passions": "big data, NLP",
        "histoires": "J'ai travaillé sur plusieurs projets open-source"
    }
}

dataset = [
    {
        "role": "pro",
        "language": "fr",
        "data": {
            "expectations": "Partager mon expertise en IA",
            "about": "Data scientist en entreprise",
            "domain": "IA",
            "experience": "10 ans en deep learning",
            "help": "J'aime encadrer des jeunes chercheurs",
            "passions": "data science, IA",
            "histoires": "J'ai mentoré plusieurs étudiants en IA"
        }
    }
]

# 📌 Envoyer la requête à l'API
url = "http://127.0.0.1:8000/recommend/"
response = requests.post(url, json={"user_data": user_data, "dataset": dataset})

# 📌 Afficher la réponse
print(response.json())

4️⃣ Résultat Attendu

L'API renverra un Top 3 des meilleures recommandations :

{
    "user_input": {
        "role": "chercheur",
        "language": "fr",
        "data": {
            "expectations": "Rencontrer des experts en data science",
            "about": "Je suis un chercheur en IA"
        }
    },
    "top_3_recommendations": [
        {
            "role": "pro",
            "domain": "IA",
            "experience": "10 ans en deep learning",
            "about": "Data scientist en entreprise",
            "similarity_score": 0.87
        }
    ],
    "top_features": [
        ["expectations", 0.55],
        ["about", 0.32]
    ]
}

🐳 Dockerisation de l'Application

Nous allons maintenant dockeriser l’application pour pouvoir l'exécuter sans dépendances locales.

# Lancer l'API FastAPI avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

2️ Construire l’Image Docker

Dans le terminal, exécute :

docker build -t recommender-api .

Cela crée une image Docker nommée recommender-api.
3️ Lancer le Conteneur Docker

Une fois l’image construite, exécute :

docker run -p 8000:8000 recommender-api

    L’API sera maintenant accessible via http://127.0.0.1:8000.
    La documentation Swagger reste accessible sur http://127.0.0.1:8000/docs.

4️ Tester l’API Dockerisée

Tu peux envoyer des requêtes avec Postman ou utiliser le script Python ci-dessus.
