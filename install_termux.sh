
#!/bin/bash

echo "🔧 Installation DedSec Device Info sur Termux"
echo "=============================================="

# Mise à jour des packages
echo "📦 Mise à jour des packages Termux..."
pkg update -y && pkg upgrade -y

# Installation des dépendances système
echo "🛠️ Installation des dépendances système..."
pkg install -y python git clang python-dev

# Permission de stockage
echo "📁 Configuration des permissions de stockage..."
termux-setup-storage

# Mise à jour pip
echo "🐍 Mise à jour de pip..."
pip install --upgrade pip

echo "✅ Installation terminée!"
echo ""
echo "🚀 Pour utiliser le script :"
echo "   python device_info.py"
echo ""
echo "🎭 Pour l'animation DedSec :"
echo "   python Dedsec.py"
