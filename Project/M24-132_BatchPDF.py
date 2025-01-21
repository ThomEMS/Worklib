import os
import pandas as pd
import pdfplumber
import re

# Chemin vers le dossier contenant les fichiers PDF
pdf_directory = "C:/Users/thomas.pelletier/OneDrive - EMS/M24-132/PDF/St-Pacome Rapport"

# Liste pour stocker les données extraites
extracted_data = []

# Parcourir tous les fichiers PDF dans le dossier
for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
        file_path = os.path.join(pdf_directory, filename)
        
        # Extraire la date du fichier à partir de son nom
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
        if date_match:
            report_date = date_match.group(1)
        else:
            continue  # Si aucune date trouvée, ignorer le fichier
        
        # Ouvrir le fichier PDF et extraire les tableaux
        with pdfplumber.open(file_path) as pdf:
            tables = pdf.pages[0].extract_table()
            
            if tables:
                # Sélectionner les 3 dernières lignes du tableau et les 3 premières colonnes
                selected_rows = tables[-3:]  # Dernières lignes
                selected_data = [row[:3] for row in selected_rows]  # Premières colonnes

                # Ajouter les données extraites à la liste
                extracted_data.append({
                    "Date": report_date,
                    "Total Volume PCPP-P1P2 (m3)": selected_data[0][1],
                    "Total Volume PCPP-P3P4 (m3)": selected_data[0][2],
                    "Minimum PCPP-P1P2 (m3)": selected_data[1][1],
                    "Minimum PCPP-P3P4 (m3)": selected_data[1][2],
                    "Maximum PCPP-P1P2 (m3)": selected_data[2][1],
                    "Maximum PCPP-P3P4 (m3)": selected_data[2][2]
                })

# Convertir les données extraites en DataFrame
df = pd.DataFrame(extracted_data)

# Fixer la date comme index et transposer le DataFrame
df.set_index("Date", inplace=True)
df_transposed = df.T

# Enregistrer les données consolidées dans un fichier Excel
output_path =  "C:/Users/thomas.pelletier/OneDrive - EMS/M24-132/consolidated_data.xlsx"
df_transposed.to_excel(output_path)

print(f"Données consolidées enregistrées dans {output_path}")
