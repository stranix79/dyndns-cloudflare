.PHONY: help build build-version build-push push login up down logs version clean

# Variables
IMAGE_NAME := dyndns-cloudflare-dyndns
DOCKER_HUB_REPO := stranix79/dyndns-cloudflare
PLATFORM := linux/amd64

help: ## Affiche l'aide
	@echo "Commandes disponibles:"
	@echo "  make build          - Construire l'image Docker (sans version)"
	@echo "  make build-version  - Construire l'image avec version automatique"
	@echo "  make build-push     - Construire et pousser vers Docker Hub"
	@echo "  make push           - Pousser l'image vers Docker Hub"
	@echo "  make login          - Se connecter à Docker Hub"
	@echo "  make version        - Afficher la version générée"
	@echo "  make up             - Démarrer le service (utilise Docker Hub)"
	@echo "  make up-local       - Démarrer le service avec build local"
	@echo "  make down           - Arrêter le service"
	@echo "  make logs           - Voir les logs du service"
	@echo "  make clean          - Nettoyer les images Docker"

version: ## Générer et afficher la version
	@./version.sh

build: ## Construire l'image Docker (latest uniquement)
	docker build --platform $(PLATFORM) -t $(IMAGE_NAME):latest .

build-version: ## Construire l'image avec version automatique
	@DOCKER_HUB_REPO=$(DOCKER_HUB_REPO) ./build.sh

build-push: build-version push ## Construire et pousser vers Docker Hub

push: ## Pousser l'image vers Docker Hub
	@DOCKER_HUB_REPO=$(DOCKER_HUB_REPO) ./push.sh

login: ## Se connecter à Docker Hub
	@echo "Connexion à Docker Hub..."
	@docker login

up: ## Démarrer le service (utilise l'image Docker Hub)
	docker-compose up -d --pull always

up-local: ## Démarrer le service avec build local
	docker-compose -f docker-compose.local.yml up -d --build

down: ## Arrêter le service
	docker-compose down

logs: ## Voir les logs
	docker-compose logs -f

clean: ## Nettoyer les images Docker
	docker-compose down --rmi local
	@echo "Images nettoyées"
