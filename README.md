# Générateur de QR Codes vCard

Ce projet Python permet d'importer un fichier Excel et de générer des QR codes SVG contenant des vCards complètes avec toutes les informations de contact.

## Installation

1. Activez votre environnement virtuel :
```bash
source .venv/bin/activate
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Format du fichier Excel

Votre fichier Excel doit contenir les colonnes suivantes :

**Colonnes obligatoires :**
- `prenom` : Prénom
- `nom` : Nom de famille

**Colonnes optionnelles :**
- `profession` : Titre/profession
- `societe` : Nom de l'entreprise/organisation
- `mobile` : Numéro de téléphone mobile
- `pro` : Numéro de téléphone professionnel
- `email` : Adresse email
- `adresse` : Adresse postale complète
- `site_web` : Site web (avec ou sans http://)

### Générer les QR codes

1. Exécutez le script principal :
```bash
python3 qr_generator.py
```

2. Entrez le chemin vers votre fichier Excel quand demandé

3. Les QR codes SVG seront générés dans le dossier `qr_codes/`

## Structure des fichiers générés

- Les QR codes sont sauvegardés en format SVG dans le dossier `qr_codes/`
- Chaque fichier est nommé : `prenom_nom_numeroLigne.svg`
- Les QR codes contiennent des vCards complètes au format standard

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
