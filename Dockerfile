# Utiliser une image de base Python
FROM python:3.12

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l’application dans le conteneur
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir fastapi uvicorn scikit-learn pandas numpy

# Exposer le port 8000
EXPOSE 8000

# Lancer l'API FastAPI avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
