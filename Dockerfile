FROM python:3.11-slim

WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le script
COPY update_dns.py .

# Rendre le script exécutable
RUN chmod +x update_dns.py

# Exécuter le script
CMD ["python", "update_dns.py"]
