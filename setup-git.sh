#!/bin/bash
# Script pour configurer Git localement pour ce dépôt

echo "Configuration Git locale pour ce dépôt uniquement"
echo ""
echo "Entrez votre nom d'utilisateur Git (ou appuyez sur Entrée pour utiliser 'stranix'):"
read -r git_name
git_name=${git_name:-stranix}

echo "Entrez votre email Git (ou appuyez sur Entrée pour utiliser 'stranix@stranix.net'):"
read -r git_email
git_email=${git_email:-stranix@stranix.net}

git config user.name "$git_name"
git config user.email "$git_email"

echo ""
echo "✓ Configuration Git locale mise à jour:"
echo "  Nom: $(git config user.name)"
echo "  Email: $(git config user.email)"
echo ""
echo "Cette configuration s'applique uniquement à ce dépôt."
