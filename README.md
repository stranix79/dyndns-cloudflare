# Cloudflare Dynamic DNS Updater

Script Python pour mettre à jour automatiquement un record DNS Cloudflare avec votre IP publique actuelle.

## Description

Ce script tourne en continu et vérifie périodiquement votre IP publique pour mettre à jour automatiquement le record DNS `home.stranix.net` sur Cloudflare si l'IP a changé. Il peut être exécuté directement ou dans un conteneur Docker.

## Prérequis

- Un compte Cloudflare avec une zone DNS configurée
- Un token d'API Cloudflare avec les permissions appropriées
- Python 3.7+ (si exécution locale)
- Docker (si utilisation du conteneur)

## Configuration

### Configuration avec fichier .env (recommandé)

1. Copiez le fichier d'exemple :
```bash
cp .env.example .env
```

2. Éditez le fichier `.env` et ajoutez votre token Cloudflare :
```bash
CLOUDFLARE_TOKEN=votre_token_ici
CLOUDFLARE_ZONE=stranix.net
CLOUDFLARE_RECORD=home.stranix.net
CHECK_INTERVAL=300
```

⚠️ **Important** : Le fichier `.env` est déjà dans `.gitignore` et ne sera pas commité sur GitHub.

### Variables d'environnement

- `CLOUDFLARE_TOKEN` : Token d'API Cloudflare (requis)
- `CLOUDFLARE_ZONE` : Nom de la zone DNS (par défaut: `stranix.net`)
- `CLOUDFLARE_RECORD` : Nom complet du record DNS (par défaut: `home.stranix.net`)
- `CHECK_INTERVAL` : Intervalle de vérification en secondes (par défaut: `300` = 5 minutes)

## Utilisation

### Exécution locale

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Configurer les variables d'environnement :
```bash
# Option 1: Utiliser un fichier .env (recommandé)
cp .env.example .env
# Éditez .env avec votre token

# Option 2: Exporter les variables directement
export CLOUDFLARE_TOKEN="votre_token_ici"
export CHECK_INTERVAL=300  # Optionnel: vérification toutes les 5 minutes
```

3. Exécuter le script (il tournera en continu) :
```bash
python update_dns.py
```

Le script vérifiera périodiquement votre IP publique et mettra à jour le DNS si nécessaire. Appuyez sur `Ctrl+C` pour l'arrêter.

### Utilisation avec Docker

#### Construction de l'image

**Avec version automatique (recommandé)**
```bash
make build-version
# ou
./build.sh
```

**Construction manuelle pour amd64**
```bash
docker build --platform linux/amd64 -t cloudflare-dyndns .
```

**Construction pour l'architecture native**
```bash
docker build -t cloudflare-dyndns .
```

#### Exécution du conteneur en mode continu

**Option 1 : Utiliser un fichier .env (recommandé)**
```bash
# Créez d'abord le fichier .env avec votre token
cp .env.example .env
# Éditez .env avec votre token

docker run -d \
  --name cloudflare-dyndns \
  --platform linux/amd64 \
  --env-file .env \
  --restart unless-stopped \
  cloudflare-dyndns
```

**Option 2 : Passer les variables directement**
```bash
docker run -d \
  --name cloudflare-dyndns \
  --platform linux/amd64 \
  -e CLOUDFLARE_TOKEN="votre_token_ici" \
  -e CLOUDFLARE_ZONE="stranix.net" \
  -e CLOUDFLARE_RECORD="home.stranix.net" \
  -e CHECK_INTERVAL=300 \
  --restart unless-stopped \
  cloudflare-dyndns
```

Le conteneur tournera en continu et vérifiera périodiquement votre IP publique.

#### Voir les logs

```bash
docker logs -f cloudflare-dyndns
```

#### Arrêter le conteneur

```bash
docker stop cloudflare-dyndns
docker rm cloudflare-dyndns
```

### Utilisation avec Docker Compose (recommandé)

Le fichier `docker-compose.yml` est configuré pour utiliser l'image Docker Hub (`stranix79/dyndns-cloudflare:latest`) par défaut. Cela permet de :
- ✅ Utiliser les versions publiées depuis Docker Hub
- ✅ Conserver l'historique des versions dans le registry
- ✅ Toujours utiliser la dernière version avec `:latest`

1. **Créez le fichier `.env`** (si ce n'est pas déjà fait) :
```bash
cp .env.example .env
# Éditez .env avec votre token Cloudflare
```

2. **Démarrez le service** (utilise l'image Docker Hub) :
```bash
# Démarrer le service (récupère automatiquement la dernière version)
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter le service
docker-compose down
```

**Pour développement local** (construire l'image localement) :
```bash
# Utiliser le fichier docker-compose.local.yml pour construire localement
docker-compose -f docker-compose.local.yml up -d --build

# Ou avec Make
make up-local
```

Le conteneur vérifiera automatiquement votre IP publique toutes les 5 minutes (configurable via `CHECK_INTERVAL` dans `.env`) et mettra à jour le DNS Cloudflare si nécessaire.

**Note** : L'image est construite pour la plateforme `linux/amd64` pour assurer la compatibilité, même sur des machines ARM (Apple Silicon).

### Versioning automatique

Le projet inclut un système de versioning automatique basé sur Git :

- **Avec tag Git** : Si un tag existe (ex: `v1.0.0`), il sera utilisé
- **Sans tag** : Format `YYYYMMDD-COMMIT_HASH` (ex: `20260302-5bc22cd`)
- **Sans Git** : Format `YYYYMMDD-HHMMSS` basé sur la date

#### Utilisation avec Make (recommandé)

```bash
# Construire avec version automatique
make build-version

# Construire et pousser vers Docker Hub
make build-push

# Pousser vers Docker Hub (après build)
make push

# Se connecter à Docker Hub
make login

# Voir la version générée
make version

# Démarrer le service (utilise l'image Docker Hub :latest)
make up

# Démarrer le service avec build local (pour développement)
make up-local

# Voir les logs
make logs

# Arrêter le service
make down
```

#### Utilisation manuelle

```bash
# Générer la version
./version.sh

# Construire avec version (tagge aussi pour Docker Hub)
./build.sh

# Pousser vers Docker Hub
./push.sh

# Ou construire manuellement avec la version
VERSION=$(./version.sh)
docker build --platform linux/amd64 \
  -t dyndns-cloudflare-dyndns:${VERSION} \
  -t dyndns-cloudflare-dyndns:latest \
  -t stranix79/dyndns-cloudflare:${VERSION} \
  -t stranix79/dyndns-cloudflare:latest .
```

### Publication sur Docker Hub

Les images sont automatiquement taggées pour Docker Hub (`stranix79/dyndns-cloudflare`) lors de la construction.

**Première utilisation :**
```bash
# Se connecter à Docker Hub
make login
# ou
docker login

# Construire et pousser
make build-push
```

**Utilisation de l'image depuis Docker Hub :**
```bash
# Récupérer l'image
docker pull stranix79/dyndns-cloudflare:latest

# Ou avec une version spécifique
VERSION=$(./version.sh)
docker pull stranix79/dyndns-cloudflare:${VERSION}
```

## Fonctionnalités

- ✅ Exécution en continu avec vérification périodique
- ✅ Récupération automatique de l'IP publique
- ✅ Mise à jour du record DNS Cloudflare uniquement si l'IP a changé
- ✅ Création automatique du record s'il n'existe pas
- ✅ Vérification avant mise à jour (évite les appels API inutiles)
- ✅ Gestion d'erreurs robuste avec continuation en cas d'erreur temporaire
- ✅ Support de plusieurs services pour récupérer l'IP publique
- ✅ Arrêt propre avec gestion des signaux (SIGINT, SIGTERM)
- ✅ Compatible Docker avec redémarrage automatique
- ✅ Intervalle de vérification configurable

## Permissions Cloudflare requises

Le token Cloudflare doit avoir les permissions suivantes :
- `Zone:Read` pour la zone concernée
- `DNS:Edit` pour la zone concernée

## Notes de sécurité

⚠️ **Important** : 
- Le fichier `.env` est déjà dans `.gitignore` et ne sera **jamais** commité sur GitHub
- Ne commitez jamais votre token Cloudflare dans le dépôt Git
- Utilisez toujours le fichier `.env` pour stocker vos secrets
- Le fichier `.env.example` peut être commité car il ne contient pas de valeurs sensibles

## Dépannage

### Erreur "Zone non trouvée"
Vérifiez que le nom de la zone (`CLOUDFLARE_ZONE`) correspond exactement à votre zone Cloudflare.

### Erreur "Permission denied"
Vérifiez que votre token Cloudflare a les permissions nécessaires pour modifier les DNS.

### Erreur "Impossible de récupérer l'IP publique"
Le script essaie plusieurs services. Si tous échouent, vérifiez votre connexion Internet.
