import os
import sys
import shutil
from pathlib import Path
import subprocess

def create_standalone_installer():
    """Crée un installateur autonome en compilant create_installer.py"""
    print("=== Création de l'installateur autonome ===\n")
    
    # Vérifier que l'exécutable principal existe
    exe_path = Path("dist/Sudalys_QR_Generator.exe")
    if not exe_path.exists():
        print("❌ ERREUR: L'exécutable principal n'existe pas!")
        print("Lancez d'abord: python build_scripts/build_exe.py")
        return False
    
    # Vérifier que create_installer.py existe
    installer_script = Path("build_scripts/create_installer.py")
    if not installer_script.exists():
        print("❌ ERREUR: Le script create_installer.py n'existe pas!")
        return False
    
    print("✅ Fichiers source trouvés")
    
    # Créer le dossier de sortie
    output_dir = Path("installer_output")
    output_dir.mkdir(exist_ok=True)
    
    # Compiler l'installateur avec PyInstaller
    print("🔨 Compilation de l'installateur...")
    
    # Vérifier que tous les fichiers existent avant de construire la commande
    required_files = [
        "dist/Sudalys_QR_Generator.exe",
        "assets/logo_sudalys_services.jpg", 
        "data/contacts.xlsx",
        "docs/GUIDE_UTILISATION.md",
        "README.md"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ Fichier manquant: {file_path}")
            return False
    
    # Vérifier que l'icône existe
    icon_path = Path("assets/logo_sudalys_services.ico")
    icon_option = []
    if icon_path.exists():
        icon_option = ["--icon", str(icon_path.absolute())]
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "Sudalys_QR_Generator_Setup",
        "--distpath", str(output_dir),
        "--workpath", "build_installer",
        "--specpath", "build_installer",
        "--clean",
        "--exclude-module", "pandas",
        "--exclude-module", "numpy",
        "--exclude-module", "matplotlib",
        "--exclude-module", "scipy",
        "--exclude-module", "django",
        str(installer_script)
    ]
    
    # Ajouter les fichiers de données avec chemins absolus
    for file_path in required_files:
        abs_path = Path(file_path).absolute()
        cmd.extend(["--add-data", f"{abs_path};."])
    
    # Ajouter l'icône si elle existe
    if icon_option:
        cmd.extend(icon_option)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            installer_exe = output_dir / "Sudalys_QR_Generator_Setup.exe"
            if installer_exe.exists():
                size_mb = installer_exe.stat().st_size / (1024 * 1024)
                print(f"✅ Installateur créé avec succès!")
                print(f"📦 Fichier: {installer_exe}")
                print(f"📏 Taille: {size_mb:.1f} MB")
                print(f"\n🎉 L'installateur autonome est prêt!")
                print(f"👥 Distribuez simplement: {installer_exe.name}")
                return True
            else:
                print("⚠️ Compilation réussie mais fichier non trouvé")
                return False
        else:
            print(f"❌ Erreur de compilation:")
            if result.stderr:
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def copy_files_for_installer():
    """Copie les fichiers nécessaires dans le bon dossier pour l'installateur"""
    print("📋 Préparation des fichiers pour l'installateur...")
    
    # Créer un dossier temporaire pour l'installateur
    installer_files_dir = Path("installer_files")
    if installer_files_dir.exists():
        shutil.rmtree(installer_files_dir)
    installer_files_dir.mkdir()
    
    # Copier tous les fichiers nécessaires
    files_to_copy = [
        ("dist/Sudalys_QR_Generator.exe", "Sudalys_QR_Generator.exe"),
        ("logo_sudalys_services.jpg", "logo_sudalys_services.jpg"),
        ("contacts.xlsx", "contacts.xlsx"),
        ("GUIDE_UTILISATION.md", "GUIDE_UTILISATION.md"),
        ("README.md", "README.md"),
        ("create_installer.py", "create_installer.py")
    ]
    
    for src, dst in files_to_copy:
        src_path = Path(src)
        if src_path.exists():
            shutil.copy2(src_path, installer_files_dir / dst)
            print(f"  ✅ {src}")
        else:
            print(f"  ⚠️ Fichier manquant: {src}")
    
    return installer_files_dir

def main():
    """Fonction principale"""
    print("🚀 Construction de l'installateur autonome Sudalys QR Generator\n")
    
    # Étape 1: Préparer les fichiers
    installer_files_dir = copy_files_for_installer()
    
    # Étape 2: Créer l'installateur
    success = create_standalone_installer()
    
    # Nettoyer les fichiers temporaires
    if installer_files_dir.exists():
        shutil.rmtree(installer_files_dir)
    
    if success:
        print("\n🎯 SUCCÈS TOTAL!")
        print("📦 Votre installateur autonome est prêt dans installer_output/")
        print("👥 Les utilisateurs n'ont qu'à lancer le fichier .exe pour installer!")
    else:
        print("\n💥 Échec de la création de l'installateur")
        sys.exit(1)

if __name__ == "__main__":
    main()
