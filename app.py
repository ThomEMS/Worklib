
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
        
        # Diviser en deux colonnes
        self.column_layout = QHBoxLayout()
        self.left_column = QVBoxLayout()
        self.right_column = QVBoxLayout()
        
        # Section Volume
        self.create_conversion_section("Volume", ["litres", "millilitres", "gallons", "mètres_cubes", "pieds_cubes"], self.left_column)

        # Section Longueur
        self.create_conversion_section("Longueur", ["mètres", "millimètres", "centimètres", "pieds", "kilomètres", "miles"], self.left_column)
        
        # Section Poids/Masse
        self.create_conversion_section("Poids/Masse", ["kilogrammes", "grammes", "livres", "onces"], self.left_column)

        # Section Énergie
        self.create_conversion_section("Énergie", ["joules", "btu", "calories", "kwh"], self.right_column)

        # Section Température
        self.create_conversion_section("Température", ["celsius", "fahrenheit"], self.right_column)

        # Section Force
        self.create_conversion_section("Force", ["newton_mètres", "livres_pieds"], self.right_column)

        # Ajouter les colonnes au layout principal
        self.column_layout.addLayout(self.left_column)
        self.column_layout.addLayout(self.right_column)
        self.conversion_layout.addLayout(self.column_layout)

        # Liste de l'historique des conversions
        self.history_list = QListWidget()
        self.conversion_layout.addWidget(self.history_list)
        
        self.conversion_tab.setLayout(self.conversion_layout)
    
    def create_conversion_section(self, title, units, parent_layout):
        group = QGroupBox(title)
        layout = QVBoxLayout()

        input_value = QLineEdit()
        input_value.setPlaceholderText("Entrez la valeur à convertir")
        
        from_unit = QComboBox()
        to_unit = QComboBox()
        from_unit.addItems(units)
        to_unit.addItems(units)
        
        convert_button = QPushButton("Convertir")
        convert_button.clicked.connect(lambda: self.perform_conversion(input_value, from_unit, to_unit, layout))
        
        result_group = QGroupBox("Résultat")
        result_layout = QVBoxLayout()
        result_label = QLabel("Le résultat s'affichera ici")
        result_label.setAlignment(Qt.AlignCenter)
        result_layout.addWidget(result_label)
        result_group.setLayout(result_layout)
        
        input_layout = QHBoxLayout()
        input_layout.addWidget(input_value)
        input_layout.addWidget(from_unit)
        input_layout.addWidget(to_unit)
        
        layout.addLayout(input_layout)
        layout.addWidget(convert_button)
        layout.addWidget(result_group)
        group.setLayout(layout)
        
        parent_layout.addWidget(group)
    
    def perform_conversion(self, input_value, from_unit, to_unit, result_layout):
        try:
            value = float(input_value.text())
            from_unit_text = from_unit.currentText()
            to_unit_text = to_unit.currentText()
            result = eng.convert_unit(value, from_unit_text, to_unit_text)
            result_text = f"{value} {from_unit_text} = {result} {to_unit_text}"
            
            # Mettre à jour l'étiquette de résultat
            result_label = result_layout.itemAt(2).widget().layout().itemAt(0).widget()
            result_label.setText(result_text)
            
            # Ajouter le résultat à l'historique
            self.update_history(result_text)
        except ValueError as e:
            result_label.setText(f"Erreur : {str(e)}")

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