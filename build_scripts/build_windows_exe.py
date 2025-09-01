#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour compiler l'application en .exe Windows depuis Linux avec Wine
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_wine_installation():
    """Vérifie si Wine est installé"""
    try:
        result = subprocess.run(['wine', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Wine détecté: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("ERREUR: Wine n'est pas installé!")
    print("Installez Wine avec: sudo apt install wine")
    return False

def check_windows_python():
    """Vérifie si Python Windows est installé dans Wine"""
    try:
        result = subprocess.run(['wine', 'python', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Python Windows détecté: {result.stdout.strip()}")
            return True
    except:
        pass
    
    print("ERREUR: Python Windows n'est pas installé dans Wine!")
    print("Téléchargez et installez Python pour Windows depuis python.org")
    print("Puis installez avec: wine python-3.x.x-amd64.exe")
    return False

def install_windows_dependencies():
    """Installe les dépendances Python dans Wine"""
    print("Installation des dépendances Windows...")
    
    # Installer pip si nécessaire
    subprocess.run(['wine', 'python', '-m', 'ensurepip', '--upgrade'], 
                  capture_output=True)
    
    # Installer les dépendances
    deps = ['qrcode[pil]==7.4.2', 'openpyxl==3.1.2', 'pillow==10.2.0', 'pyinstaller==6.5.0']
    
    for dep in deps:
        print(f"Installation de {dep}...")
        result = subprocess.run(['wine', 'python', '-m', 'pip', 'install', dep], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ERREUR lors de l'installation de {dep}: {result.stderr}")
            return False
    
    print("Dépendances installées avec succès!")
    return True

def build_windows_exe():
    """Compile l'application en .exe avec Wine"""
    print("Compilation de l'application en .exe Windows...")
    
    # Nettoyer les répertoires
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Nom de l'application
    app_name = "Sudalys_QR_Generator"
    main_file = "src/qr_app.py"
    
    # Options PyInstaller pour Windows
    cmd = [
        'wine', 'python', '-m', 'PyInstaller',
        '--name', app_name,
        '--onefile',
        '--windowed',
        '--clean',
        '--log-level', 'WARN',
        '--exclude-module', 'pandas',
        '--exclude-module', 'numpy',
        '--exclude-module', 'matplotlib',
        '--exclude-module', 'scipy',
        '--hidden-import', 'openpyxl',
        '--hidden-import', 'qrcode',
        '--hidden-import', 'PIL',
        '--add-data', f'assets/logo_sudalys_services.jpg;.',
        '--add-data', f'data/contacts.xlsx;.',
    ]
    
    # Ajouter l'icône si disponible
    if os.path.exists("assets/logo_sudalys_services.ico"):
        cmd.extend(['--icon', 'assets/logo_sudalys_services.ico'])
    
    cmd.append(main_file)
    
    print(f"Exécution de: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        exe_path = os.path.join("dist", f"{app_name}.exe")
        if os.path.exists(exe_path):
            print(f"\n✅ Compilation réussie!")
            print(f"📁 Exécutable Windows créé: {exe_path}")
            return True
        else:
            print(f"❌ L'exécutable n'a pas été trouvé: {exe_path}")
            return False
    else:
        print("❌ La compilation a échoué!")
        return False

def main():
    """Fonction principale"""
    print("=== Compilation Windows (.exe) depuis Linux ===\n")
    
    # Vérifications préalables
    if not check_wine_installation():
        return False
    
    if not check_windows_python():
        return False
    
    # Installer les dépendances
    if not install_windows_dependencies():
        return False
    
    # Compiler
    success = build_windows_exe()
    
    if success:
        print("\n🎉 Processus terminé avec succès!")
        print("Votre .exe Windows est prêt à être distribué.")
    else:
        print("\n❌ Processus terminé avec des erreurs.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
