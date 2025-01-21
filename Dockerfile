# Chargement image de base
# Dockerfile
# Utilisation de l'image officielle Python
FROM python:3-slim

# Initialisation des variables d'environnement
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définition du répertoire de travail
WORKDIR /app

# Copie et installation des dépendances
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copie du projet
COPY . .

# Exposition du port 8000
EXPOSE 8000

# Commande pour lancer le serveur Django
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]