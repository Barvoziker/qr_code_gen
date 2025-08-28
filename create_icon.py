from PIL import Image
import os

def create_icon():
    """Convertit le logo JPG en icône ICO avec une qualité optimale"""
    try:
        # Vérifier si le logo existe
        logo_path = "logo_sudalys_services.jpg"
        if not os.path.exists(logo_path):
            print(f"ERREUR: Le fichier {logo_path} n'existe pas!")
            return False
            
        # Ouvrir l'image
        img = Image.open(logo_path)
        
        # Convertir en mode RGBA si ce n'est pas déjà le cas
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Créer des versions de différentes tailles avec antialiasing
        icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        resized_images = []
        
        for size in icon_sizes:
            resized_img = img.resize(size, Image.LANCZOS)
            resized_images.append(resized_img)
        
        # Enregistrer en tant qu'icône avec toutes les tailles
        icon_path = "logo_sudalys_services.ico"
        resized_images[0].save(icon_path, format="ICO", sizes=icon_sizes, append_images=resized_images[1:])
        
        print(f"Icône créée avec succès: {icon_path}")
        return True
        
    except Exception as e:
        print(f"ERREUR lors de la création de l'icône: {e}")
        return False

if __name__ == "__main__":
    create_icon()
