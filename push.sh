#!/bin/bash
# Script pour pousser l'image Docker vers Docker Hub

set -e

DOCKER_HUB_REPO="${DOCKER_HUB_REPO:-stranix79/dyndns-cloudflare}"
VERSION=$(./version.sh)

DOCKER_HUB_VERSION="${DOCKER_HUB_REPO}:${VERSION}"
DOCKER_HUB_LATEST="${DOCKER_HUB_REPO}:latest"

echo "=========================================="
echo "Push vers Docker Hub"
echo "=========================================="
echo "Repository: ${DOCKER_HUB_REPO}"
echo "Version:    ${VERSION}"
echo "=========================================="
echo ""

# Note: La vérification de connexion sera gérée automatiquement par Docker
# Si vous n'êtes pas connecté, Docker affichera un message d'erreur approprié

# Vérifier si les images existent
if ! docker image inspect "${DOCKER_HUB_VERSION}" &>/dev/null; then
    echo "❌ L'image ${DOCKER_HUB_VERSION} n'existe pas"
    echo "   Construisez d'abord avec: make build-version"
    exit 1
fi

echo "Poussage de la version ${VERSION}..."
docker push "${DOCKER_HUB_VERSION}"

echo ""
echo "Poussage du tag latest..."
docker push "${DOCKER_HUB_LATEST}"

echo ""
echo "✅ Images poussées avec succès vers Docker Hub!"
echo "   Version: ${DOCKER_HUB_VERSION}"
echo "   Latest:  ${DOCKER_HUB_LATEST}"
echo ""
echo "Pour utiliser l'image depuis Docker Hub:"
echo "  docker pull ${DOCKER_HUB_VERSION}"
echo "  docker run -d --name dyndns --env-file .env --platform linux/amd64 ${DOCKER_HUB_VERSION}"
