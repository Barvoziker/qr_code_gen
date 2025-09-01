#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour compiler l'application en .exe Windows avec Docker
"""
import os
import subprocess
import sys

def check_docker():
    """Vérifie si Docker est installé"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Docker détecté: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("ERREUR: Docker n'est pas installé!")
    print("Installez Docker avec: sudo apt install docker.io")
    return False

def create_dockerfile():
    """Crée un Dockerfile pour la compilation Windows"""
    dockerfile_content = """FROM python:3.10-windowsservercore

# Installer les dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier le code source
COPY src/ /app/src/
COPY assets/ /app/assets/
COPY data/ /app/data/

WORKDIR /app

# Compiler l'application
RUN pyinstaller --name Sudalys_QR_Generator --onefile --windowed --clean --log-level WARN --exclude-module pandas --exclude-module numpy --exclude-module matplotlib --exclude-module scipy --hidden-import openpyxl --hidden-import qrcode --hidden-import PIL --add-data "assets/logo_sudalys_services.jpg;." --add-data "data/contacts.xlsx;." --icon "assets/logo_sudalys_services.ico" src/qr_app.py

# Copier l'exécutable vers un volume
CMD ["cmd", "/c", "copy", "dist\\Sudalys_QR_Generator.exe", "C:\\output\\"]
"""
    
    with open("Dockerfile.windows", "w") as f:
        f.write(dockerfile_content)
    
    print("Dockerfile créé: Dockerfile.windows")

def build_with_docker():
    """Compile avec Docker"""
    print("Compilation avec Docker...")
    
    # Créer le Dockerfile
    create_dockerfile()
    
    # Créer le dossier de sortie
    os.makedirs("dist", exist_ok=True)
    
    # Construire l'image Docker
    print("Construction de l'image Docker...")
    result = subprocess.run([
        'docker', 'build', 
        '-f', 'Dockerfile.windows',
        '-t', 'qr-generator-windows',
        '.'
    ])
    
    if result.returncode != 0:
        print("ERREUR: Échec de la construction de l'image Docker")
        return False
    
    # Exécuter le conteneur
    print("Exécution du conteneur...")
    result = subprocess.run([
        'docker', 'run', '--rm',
        '-v', f'{os.getcwd()}/dist:/output',
        'qr-generator-windows'
    ])
    
    if result.returncode == 0:
        exe_path = "dist/Sudalys_QR_Generator.exe"
        if os.path.exists(exe_path):
            print(f"✅ Exécutable Windows créé: {exe_path}")
            return True
    
    print("❌ Échec de la compilation")
    return False

def main():
    """Fonction principale"""
    print("=== Compilation Windows (.exe) avec Docker ===\n")
    
    if not check_docker():
        return False
    
    success = build_with_docker()
    
    if success:
        print("\n🎉 Processus terminé avec succès!")
    else:
        print("\n❌ Processus terminé avec des erreurs.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
