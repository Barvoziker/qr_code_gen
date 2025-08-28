import os
import sys
import shutil
import winreg
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path
import subprocess
import zipfile

class SudalysInstaller:
    def __init__(self):
        self.app_name = "Sudalys QR Generator"
        self.app_version = "1.0"
        self.publisher = "Sudalys Services"
        
        # Chemins d'installation (dossier utilisateur pour éviter les droits admin)
        self.install_dir = Path.home() / "AppData" / "Local" / "Sudalys QR Generator"
        self.desktop_shortcut = Path.home() / "Desktop" / f"{self.app_name}.lnk"
        self.start_menu_dir = Path(os.environ.get('APPDATA', '')) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Sudalys QR Generator"
        
        # Fichiers à installer (chemins relatifs au projet)
        project_root = Path(__file__).parent.parent
        self.files_to_install = [
            project_root / "dist/Sudalys_QR_Generator.exe",
            project_root / "assets/logo_sudalys_services.jpg", 
            project_root / "data/contacts.xlsx",
            project_root / "docs/GUIDE_UTILISATION.md",
            project_root / "README.md"
        ]
        
        self.root = None
        self.progress_var = None
        self.progress_bar = None
        self.status_label = None
        
    def create_gui(self):
        """Crée l'interface graphique d'installation"""
        self.root = tk.Tk()
        self.root.title(f"Installation - {self.app_name}")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text=f"Installation de {self.app_name}", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_text = f"""Bienvenue dans l'assistant d'installation de {self.app_name} v{self.app_version}
        
Ce programme va installer {self.app_name} sur votre ordinateur.

Éditeur: {self.publisher}
Dossier d'installation: {self.install_dir}"""
        
        desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.LEFT)
        desc_label.pack(pady=(0, 20))
        
        # Options d'installation
        options_frame = ttk.LabelFrame(main_frame, text="Options d'installation", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.desktop_var = tk.BooleanVar(value=True)
        desktop_check = ttk.Checkbutton(options_frame, text="Créer un raccourci sur le Bureau", 
                                       variable=self.desktop_var)
        desktop_check.pack(anchor=tk.W)
        
        self.start_menu_var = tk.BooleanVar(value=True)
        start_menu_check = ttk.Checkbutton(options_frame, text="Créer un raccourci dans le menu Démarrer", 
                                          variable=self.start_menu_var)
        start_menu_check.pack(anchor=tk.W)
        
        # Barre de progression
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.pack(fill=tk.X)
        
        self.status_label = ttk.Label(progress_frame, text="Prêt à installer")
        self.status_label.pack(pady=(5, 0))
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        self.install_btn = ttk.Button(button_frame, text="Installer", command=self.start_installation)
        self.install_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_btn = ttk.Button(button_frame, text="Annuler", command=self.root.quit)
        self.cancel_btn.pack(side=tk.LEFT)
        
        return self.root
    
    def update_progress(self, value, status):
        """Met à jour la barre de progression"""
        self.progress_var.set(value)
        self.status_label.config(text=status)
        self.root.update()
    
    def create_shortcut(self, target_path, shortcut_path, description=""):
        """Crée un raccourci Windows"""
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(target_path)
            shortcut.WorkingDirectory = str(target_path.parent)
            shortcut.Description = description
            shortcut.save()
            return True
        except ImportError:
            # Fallback: créer un fichier batch
            batch_content = f'@echo off\nstart "" "{target_path}"\n'
            batch_path = shortcut_path.with_suffix('.bat')
            with open(batch_path, 'w') as f:
                f.write(batch_content)
            return True
        except Exception as e:
            print(f"Erreur création raccourci: {e}")
            return False
    
    def add_to_registry(self):
        """Ajoute l'application au registre pour la désinstallation"""
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\SudalysQRGenerator"
            
            # Utiliser HKEY_CURRENT_USER au lieu de HKEY_LOCAL_MACHINE pour éviter les droits admin
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, self.app_name)
                winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, self.app_version)
                winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, self.publisher)
                winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, str(self.install_dir))
                winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, 
                                 f'"{self.install_dir / "uninstall.exe"}"')
                winreg.SetValueEx(key, "NoModify", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "NoRepair", 0, winreg.REG_DWORD, 1)
            return True
        except Exception as e:
            print(f"Erreur registre: {e}")
            return False
    
    def create_uninstaller(self):
        """Crée un désinstalleur"""
        uninstall_script = f'''import os
import sys
import shutil
import winreg
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

def remove_from_registry():
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, 
                        r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\SudalysQRGenerator")
        return True
    except:
        return False

def main():
    root = tk.Tk()
    root.withdraw()
    
    if messagebox.askyesno("Désinstallation", "Voulez-vous vraiment désinstaller {self.app_name}?"):
        try:
            # Supprimer les raccourcis
            desktop_shortcut = Path.home() / "Desktop" / "{self.app_name}.lnk"
            if desktop_shortcut.exists():
                desktop_shortcut.unlink()
            
            start_menu_dir = Path(os.environ.get('APPDATA', '')) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Sudalys QR Generator"
            if start_menu_dir.exists():
                shutil.rmtree(start_menu_dir)
            
            # Supprimer du registre
            remove_from_registry()
            
            # Supprimer le dossier d'installation (sauf ce script)
            install_dir = Path("{self.install_dir}")
            for item in install_dir.iterdir():
                if item.name != "uninstall.exe":
                    if item.is_file():
                        item.unlink()
                    else:
                        shutil.rmtree(item)
            
            messagebox.showinfo("Désinstallation", "{self.app_name} a été désinstallé avec succès.")
            
            # Se supprimer soi-même
            os.system(f'timeout /t 2 /nobreak > nul && del "{sys.executable}"')
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la désinstallation: {{e}}")
    
    root.destroy()

if __name__ == "__main__":
    main()
'''
        
        uninstall_path = self.install_dir / "uninstall.py"
        with open(uninstall_path, 'w', encoding='utf-8') as f:
            f.write(uninstall_script)
        
        # Compiler le désinstalleur en exe (optionnel)
        return True
    
    def start_installation(self):
        """Lance le processus d'installation"""
        try:
            self.install_btn.config(state='disabled')
            self.cancel_btn.config(state='disabled')
            
            # Étape 1: Vérifier les fichiers
            self.update_progress(10, "Vérification des fichiers...")
            
            # Si on est dans un exécutable PyInstaller, les fichiers sont dans _MEIPASS
            if getattr(sys, 'frozen', False):
                base_path = Path(sys._MEIPASS)
                self.files_to_install = [
                    base_path / "Sudalys_QR_Generator.exe",
                    base_path / "logo_sudalys_services.jpg",
                    base_path / "contacts.xlsx", 
                    base_path / "GUIDE_UTILISATION.md",
                    base_path / "README.md"
                ]
            
            for file_path in self.files_to_install:
                if not Path(file_path).exists():
                    raise FileNotFoundError(f"Fichier manquant: {file_path}")
            
            # Étape 2: Créer le dossier d'installation
            self.update_progress(20, "Création du dossier d'installation...")
            self.install_dir.mkdir(parents=True, exist_ok=True)
            
            # Étape 3: Copier les fichiers
            self.update_progress(30, "Copie des fichiers...")
            for i, file_path in enumerate(self.files_to_install):
                src = Path(file_path)
                dst = self.install_dir / src.name
                shutil.copy2(src, dst)
                progress = 30 + (i + 1) * 30 / len(self.files_to_install)
                self.update_progress(progress, f"Copie de {src.name}...")
            
            # Étape 4: Créer les raccourcis
            exe_path = self.install_dir / "Sudalys_QR_Generator.exe"
            
            if self.desktop_var.get():
                self.update_progress(70, "Création du raccourci Bureau...")
                self.create_shortcut(exe_path, self.desktop_shortcut, self.app_name)
            
            if self.start_menu_var.get():
                self.update_progress(80, "Création du raccourci menu Démarrer...")
                self.start_menu_dir.mkdir(parents=True, exist_ok=True)
                start_shortcut = self.start_menu_dir / f"{self.app_name}.lnk"
                self.create_shortcut(exe_path, start_shortcut, self.app_name)
            
            # Étape 5: Ajouter au registre
            self.update_progress(90, "Enregistrement dans le système...")
            self.add_to_registry()
            
            # Étape 6: Créer le désinstalleur
            self.update_progress(95, "Création du désinstalleur...")
            self.create_uninstaller()
            
            # Terminé
            self.update_progress(100, "Installation terminée!")
            
            messagebox.showinfo("Installation réussie", 
                              f"{self.app_name} a été installé avec succès!\n\n"
                              f"Dossier d'installation: {self.install_dir}")
            
            # Proposer de lancer l'application
            if messagebox.askyesno("Lancer l'application", 
                                 f"Voulez-vous lancer {self.app_name} maintenant?"):
                subprocess.Popen([str(exe_path)])
            
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror("Erreur d'installation", f"Erreur: {e}")
            self.install_btn.config(state='normal')
            self.cancel_btn.config(state='normal')

def main():
    """Fonction principale"""
    installer = SudalysInstaller()
    root = installer.create_gui()
    root.mainloop()

if __name__ == "__main__":
    main()
