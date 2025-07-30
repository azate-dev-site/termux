
# DedSec Device Info Tool

Un outil éducatif en Python pour collecter des informations détaillées sur un appareil et sa localisation.

## 🚀 Fonctionnalités

- Collecte automatique d'informations système (CPU, mémoire, disques, réseau)
- Géolocalisation basée sur l'IP avec multiple sources
- Installation automatique des dépendances
- Sauvegarde des données en JSON
- Interface console stylisée DedSec

## 📦 Installation

### Sur Termux (Android)

1. Installer les dépendances système :
```bash
pkg update && pkg upgrade
pkg install python git
```

2. Cloner le repository :
```bash
git clone https://github.com/azate-dev-site/termux.git
cd dedsec-device-info
```

3. Exécuter le script :
```bash
python device_info.py
```

### Installation générale

1. Cloner le repository :
```bash
git clone https://github.com/azate-dev-site/termux.git
cd termux
```

2. Les dépendances Python sont installées automatiquement au premier lancement

## 🎯 Utilisation

### Script principal
```bash
python device_info.py
```

### Animation DedSec
```bash

```

## 📋 Dépendances

- Python 3.6+
- psutil (auto-installé)
- requests (auto-installé)
- geocoder (auto-installé)

## 🗂️ Structure du projet

```
dedsec-device-info/
├── device_info.py      # Script principal
├── Dedsec.py           # Animation DedSec
├── README.md           # Documentation
├── pyproject.toml      # Configuration Python
└── device_info_log.json # Logs générés
```

## ⚠️ Avertissement

Ce projet est à des fins **éducatives uniquement**. Utilisez-le de manière responsable et éthique.

## 📱 Compatibilité Termux

Le script fonctionne parfaitement sur Termux avec quelques limitations :
- GPS réel non disponible (utilise la géolocalisation IP)
- Certaines informations système peuvent être limitées
- Permissions Android requises pour certaines fonctionnalités

## 🔧 Dépannage

### Erreur d'installation de packages
```bash
pkg install python-dev clang
pip install --upgrade pip
```

### Problème de permissions
```bash
termux-setup-storage
```

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
