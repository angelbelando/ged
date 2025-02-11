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
# Installer les dépendances Python
RUN pip install -r requirements.txt

# Copie du projet
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposition du port 8000
EXPOSE 8000

# Commande pour lancer le serveur Django
# Commande pour lancer Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "ged.wsgi:application"]