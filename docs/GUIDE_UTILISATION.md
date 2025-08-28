# Guide d'utilisation - Générateur de QR Codes Sudalys

## Installation

1. **Version portable (recommandée)**
   - Exécutez simplement le fichier `Sudalys_QR_Generator.exe` fourni
   - Aucune installation n'est requise

2. **Compilation depuis les sources**
   - Installez Python 3.9 ou supérieur
   - Installez les dépendances : `pip install -r requirements.txt`
   - Compilez l'application : exécutez `build_exe.bat`
   - L'exécutable sera créé dans le dossier `dist`

## Utilisation de l'application

### Interface principale

L'application propose deux modes d'utilisation :
- **Saisie manuelle** : pour créer un QR code à la fois
- **Import Excel** : pour générer plusieurs QR codes à partir d'un fichier Excel

### Mode Saisie manuelle

1. Remplissez les champs avec les informations de contact :
   - **Prénom** et **Nom** (obligatoires)
   - Profession
   - Société
   - Mobile
   - Téléphone Pro
   - Email
   - Adresse (voir formats supportés ci-dessous)
   - Site Web

2. Cliquez sur **Générer QR Code** pour créer un aperçu du QR code

3. Cliquez sur **Enregistrer QR Code** pour sauvegarder le QR code au format SVG

### Mode Import Excel

1. Sélectionnez un fichier Excel contenant les contacts (format par défaut : `contacts.xlsx`)
   - Le fichier doit contenir au minimum les colonnes `prenom` et `nom`
   - Colonnes optionnelles : `profession`, `societe`, `mobile`, `pro`, `email`, `adresse`, `site_web`

2. Cliquez sur **Générer tous les QR Codes** pour créer les QR codes pour tous les contacts

3. Vous pouvez également sélectionner un contact dans la liste pour générer son QR code individuellement

### Formats d'adresse supportés

L'application prend en charge plusieurs formats d'adresse :

1. Format standard : `123 rue de Paris 75001 PARIS`
2. Avec pays : `123 rue de Paris 75001 PARIS I FRANCE`
3. Format inversé : `123 rue de Paris PARIS 75001`
4. Format avec parenthèses : `123 rue de Paris PARIS (75001)`
5. Format international : `123 rue de Paris F-75001 PARIS`

Pour obtenir les meilleurs résultats, utilisez le format standard.

## Emplacement des QR codes générés

Les QR codes sont enregistrés aux emplacements suivants :

- **Version compilée (.exe)** : Dans le dossier `Documents\Sudalys_QR_Codes` de l'utilisateur
- **Version développement** : Dans le sous-dossier `qr_codes` du répertoire de l'application

L'application vous proposera d'ouvrir automatiquement le dossier contenant les QR codes après leur génération.

## Format des QR codes

Les QR codes sont générés au format SVG (Scalable Vector Graphics), ce qui permet :
- Un redimensionnement sans perte de qualité
- Une impression de haute qualité
- Une compatibilité avec tous les logiciels de graphisme

## Contenu des QR codes

Les QR codes contiennent des données au format vCard 3.0, qui sont compatibles avec la plupart des applications de contacts sur smartphones et ordinateurs.

## Support technique

Pour toute question ou assistance, veuillez contacter le support technique de Sudalys Services.
