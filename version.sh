#!/bin/bash
# Script pour générer automatiquement un numéro de version

# Option 1: Utiliser le tag git s'il existe
GIT_TAG=$(git describe --tags --exact-match 2>/dev/null)
if [ -n "$GIT_TAG" ]; then
    echo "$GIT_TAG"
    exit 0
fi

# Option 2: Utiliser le commit hash court avec date
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null)
GIT_DATE=$(git log -1 --format=%cd --date=format:%Y%m%d 2>/dev/null)

if [ -n "$GIT_COMMIT" ] && [ -n "$GIT_DATE" ]; then
    echo "${GIT_DATE}-${GIT_COMMIT}"
    exit 0
fi

# Option 3: Utiliser la date actuelle si git n'est pas disponible
DATE=$(date +%Y%m%d-%H%M%S)
echo "$DATE"
exit 0
