FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie tous les fichiers et dossiers du projet (app, sql, web_ui.py, etc.)
COPY . .

# Lance l'application web au lieu de l'ancien script
CMD ["python", "web_ui.py"]