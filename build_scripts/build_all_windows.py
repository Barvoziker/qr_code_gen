#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script complet pour créer l'exécutable ET l'installeur Windows
"""
import os
import sys
import subprocess
from pathlib import Path

def build_exe():
    """Compile l'exécutable Windows"""
    print("=== Étape 1: Compilation de l'exécutable ===")
    
    result = subprocess.run([sys.executable, "build_scripts/build_windows_simple.py"])
    
    if result.returncode == 0:
        exe_path = Path("dist/Sudalys_QR_Generator.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"[OK] Exécutable créé: {exe_path} ({size_mb:.1f} MB)")
            return True
    
    print("[ERREUR] Échec de la compilation de l'exécutable")
    return False

def build_installer():
    """Compile l'installeur Windows"""
    print("\n=== Étape 2: Création de l'installeur ===")
    
    result = subprocess.run([sys.executable, "build_scripts/build_standalone_installer.py"])
    
    if result.returncode == 0:
        installer_path = Path("installer_output/Sudalys_QR_Generator_Setup.exe")
        if installer_path.exists():
            size_mb = installer_path.stat().st_size / (1024 * 1024)
            print(f"[OK] Installeur créé: {installer_path} ({size_mb:.1f} MB)")
            return True
    
    print("[ERREUR] Échec de la création de l'installeur")
    return False

def main():
    """Fonction principale"""
    print("=== Build complet Windows - EXE + Installeur ===\n")
    
    # Étape 1: Compiler l'exécutable
    if not build_exe():
        print("\n[ERREUR] Arrêt: impossible de créer l'exécutable")
        sys.exit(1)
    
    # Étape 2: Créer l'installeur
    if not build_installer():
        print("\n[ERREUR] Arrêt: impossible de créer l'installeur")
        sys.exit(1)
    
    # Succès total
    print("\n=== BUILD COMPLET RÉUSSI! ===")
    print("\nFichiers créés:")
    print("  - dist/Sudalys_QR_Generator.exe (exécutable portable)")
    print("  - installer_output/Sudalys_QR_Generator_Setup.exe (installeur)")
    print("\nDistribution:")
    print("  - Exécutable: pour utilisation directe sans installation")
    print("  - Installeur: pour installation complète avec raccourcis")

if __name__ == "__main__":
    main()
