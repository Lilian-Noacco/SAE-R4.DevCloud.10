# Dockerfile pour Django
FROM python:3.12

WORKDIR /app

# Copier requirements.txt d'abord pour cache efficace
COPY requirements.txt /app/requirements.txt

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copier le reste du contenu du projet
COPY . /app/

# Exposer le port 8000
EXPOSE 8000

# Commande pour démarrer le serveur Django
CMD ["python", "sae410/manage.py", "runserver", "0.0.0.0:8000"]
