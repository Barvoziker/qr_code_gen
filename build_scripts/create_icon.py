from PIL import Image
import os

def create_icon():
    """
    Convertit le logo JPG en icône ICO
    """
    try:
        # Chemins mis à jour pour la nouvelle architecture
        jpg_path = "../assets/logo_sudalys_services.jpg"
        ico_path = "../assets/logo_sudalys_services.ico"
        
        # Ouvrir l'image JPG
        img = Image.open(jpg_path)
        
        # Redimensionner pour les tailles d'icône standard
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # Créer une liste d'images redimensionnées
        icon_images = []
        for size in sizes:
            resized_img = img.resize(size, Image.LANCZOS)
            icon_images.append(resized_img)
        
        # Sauvegarder comme ICO
        icon_images[0].save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in icon_images])
        
        print(f"Icône créée avec succès: {ico_path}")
        return True
        
    except Exception as e:
        print(f"Erreur lors de la création de l'icône: {e}")
        return False

if __name__ == "__main__":
    create_icon()
