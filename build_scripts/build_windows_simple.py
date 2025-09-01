#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple pour compiler l'application en .exe Windows
À utiliser directement sur une machine Windows
"""
import os
import sys
import shutil
from pathlib import Path

def clean_build_directories():
    """Nettoie les répertoires build et dist"""
    print("Nettoyage des répertoires build et dist...")
    
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    print("Nettoyage terminé.")

def build_windows_executable():
    """Compile l'application en .exe Windows avec PyInstaller"""
    print("Compilation de l'application en .exe Windows...")
    
    # Nom du fichier principal
    main_file = "src/qr_app.py"
    
    # Vérifier que le fichier principal existe
    if not os.path.exists(main_file):
        print(f"ERREUR: Le fichier {main_file} n'existe pas!")
        return False
    
    # Nom de l'application
    app_name = "Sudalys_QR_Generator"
    
    # Chemin de l'icône (si disponible)
    icon_path = ""
    if os.path.exists("assets/logo_sudalys_services.ico"):
        icon_path = "--icon=assets/logo_sudalys_services.ico"
    
    # Fichiers à inclure (Windows utilise ; comme séparateur)
    data_files = [
        "--add-data", f"assets/logo_sudalys_services.jpg;.",
        "--add-data", f"data/contacts.xlsx;."
    ]
    
    # Options PyInstaller pour Windows
    pyinstaller_options = [
        "--name", app_name,
        "--onefile",
        "--windowed",
        "--clean",
        "--log-level", "WARN",
        "--exclude-module", "pandas",
        "--exclude-module", "numpy",
        "--exclude-module", "matplotlib",
        "--exclude-module", "scipy",
        "--exclude-module", "django",
        "--exclude-module", "tkinter.test",
        "--exclude-module", "test",
        "--exclude-module", "unittest",
        "--exclude-module", "doctest",
        "--exclude-module", "pdb",
        "--exclude-module", "pydoc",
        "--exclude-module", "sqlite3",
        "--exclude-module", "multiprocessing",
        "--exclude-module", "concurrent",
        "--hidden-import", "openpyxl",
        "--hidden-import", "qrcode",
        "--hidden-import", "PIL"
    ]
    
    # Construire la commande PyInstaller
    cmd_parts = ["pyinstaller"]
    cmd_parts.extend(pyinstaller_options)
    
    if icon_path:
        cmd_parts.append(icon_path)
    
    for data_file in data_files:
        cmd_parts.append(data_file)
    
    cmd_parts.append(main_file)
    
    # Convertir la commande en chaîne
    cmd = " ".join(cmd_parts)
    
    # Exécuter la commande
    print(f"Exécution de la commande: {cmd}")
    result = os.system(cmd)
    
    if result == 0:
        print("\nCompilation réussie!")
        exe_path = os.path.join("dist", f"{app_name}.exe")
        if os.path.exists(exe_path):
            print(f"Exécutable Windows créé: {exe_path}")
            return True
        else:
            print(f"AVERTISSEMENT: L'exécutable n'a pas été trouvé à l'emplacement attendu: {exe_path}")
            return False
    else:
        print("\nERREUR: La compilation a échoué!")
        return False

def main():
    """Fonction principale"""
    print("=== Script de compilation Windows (.exe) ===\n")
    
    # Vérifier qu'on est sur Windows
    if not sys.platform.startswith('win'):
        print("AVERTISSEMENT: Ce script est conçu pour Windows.")
        print("Vous êtes sur:", sys.platform)
    
    # Nettoyer les répertoires build et dist
    clean_build_directories()
    
    # Compiler l'application
    success = build_windows_executable()
    
    if success:
        print("\nProcessus de compilation terminé avec succès.")
        print("Votre fichier .exe est prêt dans le dossier dist/")
    else:
        print("\nProcessus de compilation terminé avec des erreurs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
