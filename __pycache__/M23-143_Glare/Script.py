import cv2
import os

def analyze_glare(image, threshold=200):
    """
    Analyse une image pour détecter les zones d'éblouissement.
    
    Entrées:
        - image : Image couleur (numpy.ndarray).
        - threshold : Valeur d'intensité pour détecter l'éblouissement (int).
        
    Sorties:
        - glare_area : Aire totale des zones d'éblouissement en pixels (float).
        - annotated_image : Image annotée avec les contours des zones d'éblouissement (numpy.ndarray).
    """
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Appliquer un seuil
    _, bright_areas = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    
    # Trouver les contours
    contours, _ = cv2.findContours(bright_areas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Calculer l'aire totale des zones lumineuses
    glare_area = sum(cv2.contourArea(c) for c in contours)
    
    # Annoter l'image originale avec les contours
    annotated_image = image.copy()
    cv2.drawContours(annotated_image, contours, -1, (0, 0, 255), 2)  # Rouge pour les contours
    
    return glare_area, annotated_image

def save_image(image, filename):
    """
    Enregistre une image dans un fichier.
    
    Entrées:
        - image : Image à enregistrer (numpy.ndarray).
        - filename : Nom du fichier de sortie (str).
    """
    cv2.imwrite(filename, image)
    print(f"Image enregistrée sous {filename}")

def process_images(threshold=200):
    """
    Traite toutes les images du dossier courant pour détecter les zones d'éblouissement.
    
    Entrées:
        - threshold : Valeur de seuil pour détecter l'éblouissement (int).
    """
    # Récupérer les fichiers .jpg dans le dossier courant
    current_dir = os.getcwd()
    image_files = [f for f in os.listdir(current_dir) if f.endswith(".jpeg")]
    
    if not image_files:
        print("Aucune image .jpg trouvée dans le dossier courant.")
        return
    
    results = []
    
    for file in image_files:
        # Charger l'image
        image = cv2.imread(file)
        if image is None:
            print(f"Erreur: Impossible de charger l'image {file}")
            continue
        
        # Analyser l'image
        glare_area, annotated_image = analyze_glare(image, threshold)
        results.append((file, glare_area))
        
        # Générer un nom de fichier pour l'image annotée
        annotated_filename = file.replace(".jpg", "_annotated.jpg")
        save_image(annotated_image, annotated_filename)
    
    # Résumé des résultats
    print("\nRésumé des zones d'éblouissement :")
    for file, area in results:
        print(f"{file} : Zone d'éblouissement = {area:.2f} pixels")


if __name__ == "__main__":
    # Valeur de seuil pour détecter l'éblouissement
    threshold = 200
    
    # Traiter les images
    process_images(threshold)
