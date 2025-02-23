from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# 📌 Classe pour recevoir l'input utilisateur
class UserInput(BaseModel):
    user_data: dict  # JSON contenant les infos du chercheur/pro à analyser
    dataset: list  # Liste de tous les autres chercheurs & pros

# 📌 Fonction de nettoyage des données
def clean_text(value):
    if isinstance(value, list):
        return " ".join(map(str, value))
    elif isinstance(value, dict):
        return json.dumps(value)  # Convertir dict en string JSON
    elif pd.isna(value):
        return ""
    return str(value).strip()

# 📌 Fonction pour préparer les données
def prepare_data(data):
    df = pd.DataFrame(data)
    
    # Vérifier si la colonne "data" existe et extraire les valeurs
    if "data" in df.columns:
        for key in ["expectations", "domain", "experience", "about", "help", "passions", "histoires"]:
            df[key] = df["data"].apply(lambda x: x.get(key, "") if isinstance(x, dict) else "")

    # Nettoyer les colonnes textuelles
    for col in ["expectations", "domain", "experience", "about", "help", "passions", "histoires"]:
        df[col] = df[col].apply(clean_text)

    return df

# 📌 Fonction principale de recommandation
def get_top_recommendations(user_data, dataset, top_n=3):
    # Transformer les données en DataFrame
    dataset_df = prepare_data(dataset)
    user_df = prepare_data([user_data])  

    # 📌 Définir les critères à comparer
    criteres = ["expectations", "domain", "experience", "about", "help", "passions", "histoires"]

    # 📌 Initialisation d'un dictionnaire pour stocker les résultats
    similarity_results = {}

    # 📌 Appliquer TF-IDF et calculer la similarité pour chaque critère
    for critere in criteres:
        vectorizer = TfidfVectorizer()
        
        # Vérifier que la colonne contient bien du texte
        if user_df[critere].str.strip().eq("").all() or dataset_df[critere].str.strip().eq("").all():
            continue  

        # Vectorisation des textes
        user_tfidf = vectorizer.fit_transform(user_df[critere])
        dataset_tfidf = vectorizer.transform(dataset_df[critere])

        # Calcul de la similarité cosinus
        similarity_matrix = cosine_similarity(user_tfidf, dataset_tfidf)
        similarity_results[critere] = similarity_matrix[0]  # Récupérer la similarité pour l'utilisateur donné

    # 📌 Fusionner les scores en une seule matrice de score final
    valid_criteres = list(similarity_results.keys())
    final_scores = np.mean([similarity_results[c] for c in valid_criteres], axis=0)

    # 📌 Trouver les meilleures correspondances
    dataset_df["similarity_score"] = final_scores
    top_matches = dataset_df.nlargest(top_n, "similarity_score")

    # 📌 Extraire les Top Features qui influencent le plus la recommandation
    feature_importance = {critere: similarity_results[critere].mean() for critere in valid_criteres}
    top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)

    # 📌 Retourner les résultats sous forme JSON
    return {
        "user_input": user_data,
        "top_3_recommendations": top_matches[["role", "domain", "experience", "about", "similarity_score"]].to_dict(orient="records"),
        "top_features": top_features
    }

# 📌 Endpoint pour obtenir les recommandations
@app.post("/recommend/")
async def recommend(user_input: UserInput):
    try:
        result = get_top_recommendations(user_input.user_data, user_input.dataset)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 📌 Pour lancer l'API : uvicorn main:app --reload
