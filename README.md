# 🎯 Générateur de QR Code vCard - Sudalys Services

Application desktop moderne pour générer des QR codes vCard à partir de données de contact, avec interface graphique intuitive et compilation en exécutable autonome.

## 📁 Architecture du Projet

```
qr_code_gen/
├── 📂 src/                     # Code source principal
│   ├── qr_app.py              # Application principale (interface GUI)
│   └── qr_generator.py        # Logique de génération QR codes
├── 📂 build_scripts/          # Scripts de compilation
│   ├── build_exe.py           # Compilation exécutable
│   ├── build_standalone_installer.py  # Création installateur
│   ├── create_installer.py    # Interface d'installation
│   └── create_icon.py         # Utilitaire création icône
├── 📂 assets/                 # Ressources graphiques
│   ├── logo_sudalys_services.jpg
│   └── logo_sudalys_services.ico
├── 📂 data/                   # Données d'exemple
│   └── contacts.xlsx          # Fichier Excel exemple
├── 📂 docs/                   # Documentation
│   └── GUIDE_UTILISATION.md   # Guide utilisateur détaillé
├── 📂 installer_output/       # Installateur final
├── 📂 qr_codes/              # QR codes générés (créé automatiquement)
├── requirements.txt           # Dépendances Python
├── build_all.bat             # Script de build complet
└── README.md                 # Ce fichier
```

## ✨ Fonctionnalités

### 🖱️ Interface Utilisateur
- **Saisie manuelle** : Formulaire intuitif pour données individuelles
- **Import Excel** : Traitement en lot avec aperçu des données
- **Aperçu temps réel** : Visualisation du QR code avant sauvegarde
- **Interface moderne** : Design professionnel avec onglets

### 📱 Génération QR Codes
- **Format vCard 3.0** : Compatible tous smartphones
- **Export SVG** : Format vectoriel haute qualité
- **Parsing intelligent** : Analyse automatique des adresses
- **Validation données** : Vérification champs obligatoires

### 🔧 Compilation & Distribution
- **Exécutable 15MB** : Optimisé, de 3GB à 15MB
- **Installateur autonome** : Aucune dépendance externe
- **Installation utilisateur** : Pas de droits administrateur
- **Désinstallation propre** : Suppression complète

## 🚀 Utilisation Rapide

### Installation Développeur
```bash
# Cloner et installer
git clone <repository>
cd qr_code_gen
pip install -r requirements.txt

# Lancer l'application
python src/qr_app.py
```

### Compilation Complète
```bash
# Tout compiler en une fois
build_all.bat

# Ou étape par étape
python build_scripts/build_exe.py
python build_scripts/build_standalone_installer.py
```

## 📋 Formats de Données

### Saisie Manuelle
- **Obligatoire** : Prénom, Nom
- **Optionnel** : Profession, Société, Mobile, Téléphone Pro, Email, Adresse, Site Web

### Fichier Excel
Colonnes supportées : `prenom`, `nom`, `profession`, `societe`, `mobile`, `pro`, `email`, `adresse`, `site_web`

### Formats d'Adresse
- Standard : `123 rue de Paris 75001 PARIS`
- Avec pays : `123 rue de Paris 75001 PARIS I FRANCE`  
- Format inversé : `123 rue de Paris PARIS 75001`
- Avec parenthèses : `123 rue de Paris PARIS (75001)`

## 🛠️ Technologies

| Composant | Technologie | Usage |
|-----------|-------------|-------|
| Interface | Tkinter | GUI native Python |
| QR Codes | qrcode + PIL | Génération et rendu |
| Excel | openpyxl | Lecture fichiers .xlsx |
| Compilation | PyInstaller | Exécutable Windows |
| Installation | Python + WinAPI | Installateur autonome |

## 📦 Distribution

### Pour les Utilisateurs Finaux
1. Télécharger `Sudalys_QR_Generator_Setup.exe`
2. Double-clic pour installer
3. Choisir raccourci bureau (optionnel)
4. Lancer l'application

### Pour les Développeurs
1. Modifier le code source dans `src/`
2. Tester avec `python src/qr_app.py`
3. Compiler avec `build_all.bat`
4. Distribuer l'installateur

## 🎯 Optimisations Réalisées

- **Taille exécutable** : 3GB → 15MB (99.5% réduction)
- **Dépendances** : Suppression pandas, django-qrcode
- **Exclusions PyInstaller** : Modules inutiles exclus
- **Architecture propre** : Séparation logique des composants
- **Installation utilisateur** : Pas de droits admin requis

## 📞 Support

Pour toute question ou problème :
- 📧 Email : support@sudalys.com
- 📖 Documentation : `docs/GUIDE_UTILISATION.md`
- 🐛 Issues : Créer une issue sur le repository

## Structure des fichiers générés

- Les QR codes sont sauvegardés en format SVG dans le dossier `qr_codes/`
- Chaque fichier est nommé : `prenom_nom_numeroLigne.svg`

## Exemple de vCard générée

```
BEGIN:VCARD
VERSION:3.0
FN:Jean Dupont
N:Dupont;Jean;;;
TITLE:Développeur
ORG:TechCorp
EMAIL:jean.dupont@email.com
TEL;TYPE=CELL:06 12 34 56 78
TEL;TYPE=WORK:01 23 45 67 89
ADR:;;123 Rue de la Paix, 75001 Paris;;;;
URL:https://www.jeandupont.fr
END:VCARD
```

## Fonctionnalités

- **Gestion flexible** : Seuls prénom et nom sont obligatoires
- **Champs optionnels** : Tous les autres champs sont facultatifs
- **URLs automatiques** : Ajout automatique de https:// si manquant
- **Validation des données** : Ignore les cellules vides ou invalides
- **Format standard** : vCards compatibles avec tous les appareils
