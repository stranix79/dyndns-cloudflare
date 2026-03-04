#!/bin/bash
# Script pour construire l'image Docker avec version automatique

set -e

# Récupérer le nom de l'image depuis docker-compose ou utiliser la valeur par défaut
IMAGE_NAME="${IMAGE_NAME:-dyndns-cloudflare-dyndns}"
DOCKER_HUB_REPO="${DOCKER_HUB_REPO:-stranix79/dyndns-cloudflare}"
PLATFORM="${PLATFORM:-linux/amd64}"

# Générer la version
VERSION=$(./version.sh)
FULL_IMAGE_NAME="${IMAGE_NAME}:${VERSION}"
LATEST_IMAGE_NAME="${IMAGE_NAME}:latest"
DOCKER_HUB_VERSION="${DOCKER_HUB_REPO}:${VERSION}"
DOCKER_HUB_LATEST="${DOCKER_HUB_REPO}:latest"

echo "=========================================="
echo "Construction de l'image Docker"
echo "=========================================="
echo "Image locale: ${FULL_IMAGE_NAME}"
echo "Docker Hub:   ${DOCKER_HUB_VERSION}"
echo "Plateforme:   ${PLATFORM}"
echo "Version:      ${VERSION}"
echo "=========================================="
echo ""

# Construire l'image avec la version
docker build \
    --platform "${PLATFORM}" \
    --tag "${FULL_IMAGE_NAME}" \
    --tag "${LATEST_IMAGE_NAME}" \
    --tag "${DOCKER_HUB_VERSION}" \
    --tag "${DOCKER_HUB_LATEST}" \
    .

echo ""
echo "✅ Image construite avec succès!"
echo "   Version locale: ${FULL_IMAGE_NAME}"
echo "   Latest locale:  ${LATEST_IMAGE_NAME}"
echo "   Docker Hub:     ${DOCKER_HUB_VERSION}"
echo "   Docker Hub latest: ${DOCKER_HUB_LATEST}"
echo ""
echo "Pour démarrer le conteneur:"
echo "  docker-compose up -d"
echo ""
echo "Pour pousser vers Docker Hub:"
echo "  make push"
echo "  ou"
echo "  ./push.sh"
