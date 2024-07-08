
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QGroupBox, QListWidget
)
from PySide6.QtCore import Qt
import workbook as eng

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Outil de Conversion d'Unités")
        
        # Créer le widget à onglets
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Créer les onglets
        self.home_tab = QWidget()
        self.conversion_tab = QWidget()
        
        # Ajouter les onglets au widget à onglets
        self.tabs.addTab(self.home_tab, "Accueil")
        self.tabs.addTab(self.conversion_tab, "Conversion")
        
        # Configurer l'onglet d'accueil
        self.home_layout = QVBoxLayout()
        self.home_tab.setLayout(self.home_layout)
        
        # Historique des conversions
        self.conversion_history = []
        
        # Configurer l'onglet de conversion
        self.setup_conversion_tab()
    
    def setup_conversion_tab(self):
        self.conversion_layout = QVBoxLayout()
        
        # Champ de saisie pour la valeur à convertir
        self.input_value = QLineEdit()
        self.input_value.setPlaceholderText("Entrez la valeur à convertir")
        
        # Menus déroulants pour la sélection des unités
        self.from_unit = QComboBox()
        self.to_unit = QComboBox()
        
        # Remplir les menus déroulants
        units = [
            "litres", "millilitres", "gallons", "mètres_cubes", "pieds_cubes", 
            "newton_mètres", "livres_pieds", "joules", "btu", "calories", "kwh",
            "mètres", "millimètres", "centimètres", "pieds", "kilomètres", "miles",
            "kilogrammes", "grammes", "livres", "onces",
            "celsius", "fahrenheit"
        ]
        self.from_unit.addItems(units)
        self.to_unit.addItems(units)
        
        # Bouton de conversion
        self.convert_button = QPushButton("Convertir")
        self.convert_button.clicked.connect(self.perform_conversion)
        
        # Étiquette de résultat dans une boîte groupée
        self.result_group = QGroupBox("Résultat")
        self.result_layout = QVBoxLayout()
        self.result_label = QLabel("Le résultat s'affichera ici")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_layout.addWidget(self.result_label)
        self.result_group.setLayout(self.result_layout)
        
        # Liste de l'historique des conversions
        self.history_list = QListWidget()

        # Agencements
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_value)
        input_layout.addWidget(self.from_unit)
        input_layout.addWidget(self.to_unit)
        
        self.conversion_layout.addLayout(input_layout)
        self.conversion_layout.addWidget(self.convert_button)
        self.conversion_layout.addWidget(self.result_group)
        self.conversion_layout.addWidget(self.history_list)
        
        self.conversion_tab.setLayout(self.conversion_layout)
    
    def perform_conversion(self):
        try:
            value = float(self.input_value.text())
            from_unit = self.from_unit.currentText()
            to_unit = self.to_unit.currentText()
            result = eng.convert_unit(value, from_unit, to_unit)
            result_text = f"{value} {from_unit} = {result} {to_unit}"
            self.result_label.setText(result_text)
            
            # Ajouter le résultat à l'historique
            self.update_history(result_text)
        except ValueError as e:
            self.result_label.setText(f"Erreur : {str(e)}")

    def update_history(self, result_text):
        # Ajouter le nouveau résultat en haut de la liste
        self.conversion_history.insert(0, result_text)
        # Limiter l'historique à 10 éléments
        if len(self.conversion_history) > 10:
            self.conversion_history.pop()
        # Mettre à jour la liste affichée
        self.history_list.clear()
        self.history_list.addItems(self.conversion_history)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())