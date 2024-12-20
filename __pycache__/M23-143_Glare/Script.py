import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

def analyze_glare(image, threshold=200):
    """
    Analyse une image pour détecter les zones d'éblouissement, en excluant une région triangulaire non importante.
    
    Entrées:
        - image : Image couleur (numpy.ndarray).
        - threshold : Valeur d'intensité pour détecter l'éblouissement (int).
        
    Sorties:
        - glare_area : Aire totale des zones d'éblouissement en pixels (float).
        - annotated_image : Image annotée avec les contours des zones d'éblouissement et la région exclue (numpy.ndarray).
    """
    # Dimensions de l'image
    h, w = image.shape[:2]
    
    # Créer un masque pour exclure la région triangulaire
    mask = np.zeros((h, w), dtype=np.uint8)
    triangle_points = np.array([[w - 1, h // 2], [w - 1, h - 1], [0, h - 1]], dtype=np.int32)
    cv2.fillPoly(mask, [triangle_points], 255)  # Remplir le triangle avec du blanc (255)
    
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Appliquer un seuil pour détecter les zones lumineuses
    _, bright_areas = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    
    # Appliquer le masque pour exclure la région triangulaire
    bright_areas = cv2.bitwise_and(bright_areas, bright_areas, mask=cv2.bitwise_not(mask))
    
    # Trouver les contours des zones lumineuses
    contours, _ = cv2.findContours(bright_areas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Calculer l'aire totale des zones lumineuses
    glare_area = sum(cv2.contourArea(c) for c in contours)
    
    # Annoter l'image originale
    annotated_image = image.copy()
    cv2.drawContours(annotated_image, contours, -1, (0, 0, 255), 2)  # Rouge pour les contours
    cv2.polylines(annotated_image, [triangle_points], isClosed=True, color=(255, 0, 0), thickness=2)  # Triangle bleu
    
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

def process_images(threshold=200, input_dir=".", output_dir="."):
    """
    Traite toutes les images pour détecter les zones d'éblouissement avec exclusion de la région triangulaire.
    Inclut des statistiques de pourcentage d'augmentation par rapport à l'image baseline.
    
    Entrées:
        - threshold : Valeur de seuil pour détecter l'éblouissement (int).
        - input_dir : Dossier contenant les images (str).
        - output_dir : Dossier où sauvegarder les résultats (str).
    """
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".jpeg")]
    if not image_files:
        print(f"Aucune image .jpeg trouvée dans le dossier {input_dir}.")
        return
    
    results = []
    annotated_images = []
    
    # Traiter les images
    for file in image_files:
        full_path = os.path.join(input_dir, file)
        image = cv2.imread(full_path)
        if image is None:
            print(f"Erreur: Impossible de charger l'image {full_path}.")
            continue
        
        # Analyser les zones d'éblouissement
        glare_area, annotated_image = analyze_glare(image, threshold)
        results.append((file, glare_area))
        annotated_images.append((file, annotated_image))
        
        # Enregistrer l'image annotée
        annotated_filename = os.path.join(output_dir, file.replace(".jpeg", "_annotated.jpeg"))
        save_image(annotated_image, annotated_filename)
    
    # Identifier l'aire baseline
    baseline_result = next((r for r in results if "baseline" in r[0].lower()), None)
    if baseline_result is None:
        print("Aucune image baseline trouvée.")
        return
    
    baseline_area = baseline_result[1]
    print(f"Aire baseline : {baseline_area:.2f} pixels")
    
    # Calculer les augmentations
    percentage_increases = []
    for file, area in results:
        if baseline_area > 0:
            increase = ((area - baseline_area) / baseline_area) * 100
        else:
            increase = float('inf')  # Augmentation infinie si baseline est zéro
        percentage_increases.append((file, area, increase))
    
    # Afficher les résultats
    print("\nRésumé des zones d'éblouissement et augmentations :")
    for file, area, increase in percentage_increases:
        print(f"{file} : Aire = {area:.2f} pixels, Augmentation = {increase:.2f}%")
    
    # Graphique des zones d'éblouissement
    filenames, glare_areas, increases = zip(*percentage_increases)
    plt.figure(figsize=(10, 5))
    
    # Histogramme des aires
    plt.subplot(1, 2, 1)
    plt.bar(filenames, glare_areas, color='skyblue')
    plt.title("Aire des zones lumineuses")
    plt.xlabel("Images")
    plt.ylabel("Aire (pixels)")
    plt.xticks(rotation=45, ha="right")
    
    # Graphique des augmentations
    plt.subplot(1, 2, 2)
    plt.bar(filenames, increases, color='orange')
    plt.title("Pourcentage d'augmentation")
    plt.xlabel("Images")
    plt.ylabel("Augmentation (%)")
    plt.xticks(rotation=45, ha="right")
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "glare_analysis_statistics.png"))
    plt.show()

if __name__ == "__main__":
    threshold = 200
    input_dir = r"C:\Users\thomas.pelletier\Documents\GitHub\Worklib\__pycache__\M23-143_Glare"
    output_dir = input_dir  # Enregistre les résultats dans le même dossier
    process_images(threshold, input_dir, output_dir)
