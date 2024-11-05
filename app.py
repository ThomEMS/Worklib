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
        self.ductulator_tab = QWidget()  # Nouvel onglet Ductulator
        
        # Ajouter les onglets au widget à onglets
        self.tabs.addTab(self.home_tab, "Accueil")
        self.tabs.addTab(self.conversion_tab, "Conversion")
        self.tabs.addTab(self.ductulator_tab, "Ductulator")  # Ajouter l'onglet
        
        # Configurer l'onglet d'accueil
        self.home_layout = QVBoxLayout()
        self.home_tab.setLayout(self.home_layout)
        
        # Historique des conversions
        self.conversion_history = []
        
        # Configurer l'onglet de conversion
        self.setup_conversion_tab()
        
        # Configurer l'onglet Ductulator
        self.setup_ductulator_tab()

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

        # Section Couple
        self.create_conversion_section("Couple", ["newton_mètres", "livres_pieds"], self.right_column)

        # Section Débits Volumique
        self.create_conversion_section("Débits volumique", ["litres_par_seconde", "millilitres_par_seconde", "gallons_par_minute", "mètres_cubes_par_seconde", "pieds_cubes_par_seconde", "litres_par_minute", "mètres_cubes_par_heure"], self.left_column)

        # Section Débits massique
        self.create_conversion_section("Débits massique", ["kilogrammes_par_seconde", "grammes_par_seconde", "tonnes_par_seconde", "livres_par_seconde"], self.right_column)

        # Ajouter les colonnes au layout principal
        self.column_layout.addLayout(self.left_column)
        self.column_layout.addLayout(self.right_column)
        self.conversion_layout.addLayout(self.column_layout)

        # Liste de l'historique des conversions
        self.history_list = QListWidget()
        self.conversion_layout.addWidget(self.history_list)
        
        self.conversion_tab.setLayout(self.conversion_layout)

    def setup_ductulator_tab(self):
        ductulator_layout = QVBoxLayout()
        
        # Groupes de saisie pour deux ensembles distincts
        self.group1_layout, self.cfm_input1, self.head_loss_input1 = self.create_duct_sizing_group("Ensemble 1")
        self.group2_layout, self.cfm_input2, self.head_loss_input2 = self.create_duct_sizing_group("Ensemble 2")
        
        # Ajouter les deux groupes au layout principal
        ductulator_layout.addLayout(self.group1_layout)
        ductulator_layout.addLayout(self.group2_layout)
        
        # Bouton pour effectuer le dimensionnement pour les deux ensembles
        self.size_button = QPushButton("Dimensionner")
        self.size_button.clicked.connect(self.perform_duct_sizing)
        ductulator_layout.addWidget(self.size_button)
        
        # Boîte pour afficher les résultats pour chaque ensemble
        self.result_box1 = QListWidget()
        self.result_box2 = QListWidget()
        ductulator_layout.addWidget(QLabel("Résultats pour l'ensemble 1:"))
        ductulator_layout.addWidget(self.result_box1)
        ductulator_layout.addWidget(QLabel("Résultats pour l'ensemble 2:"))
        ductulator_layout.addWidget(self.result_box2)
        
        # Historique des dimensionnements
        self.history_list_ductulator = QListWidget()
        ductulator_layout.addWidget(QLabel("Historique des réponses:"))
        ductulator_layout.addWidget(self.history_list_ductulator)
        
        # Définir le layout pour l'onglet Ductulator
        self.ductulator_tab.setLayout(ductulator_layout)

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

    def create_duct_sizing_group(self, title):
        group_layout = QVBoxLayout()
        
        group_layout.addWidget(QLabel(f"{title} - CFM:"))
        cfm_input = QLineEdit()
        cfm_input.setPlaceholderText("Entrez le CFM")
        group_layout.addWidget(cfm_input)
        
        group_layout.addWidget(QLabel(f"{title} - Perte de charge (perte/100 ft):"))
        head_loss_input = QLineEdit()
        head_loss_input.setPlaceholderText("Entrez la perte de charge")
        group_layout.addWidget(head_loss_input)
        
        return group_layout, cfm_input, head_loss_input

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

    def perform_duct_sizing(self):
        try:
            # Récupérer les valeurs du premier ensemble
            cfm1 = float(self.cfm_input1.text())
            head_loss1 = float(self.head_loss_input1.text())
            combinations1 = eng.square_duct_diam_mm(cfm1, head_loss1)
            
            # Afficher les résultats pour l'ensemble 1
            self.result_box1.clear()
            if combinations1:
                for combo in combinations1:
                    self.result_box1.addItem(f"{combo[0]} mm x {combo[1]} mm")
            else:
                self.result_box1.addItem("Aucune combinaison trouvée.")
            
            # Récupérer les valeurs du second ensemble
            cfm2 = float(self.cfm_input2.text())
            head_loss2 = float(self.head_loss_input2.text())
            combinations2 = eng.square_duct_diam_mm(cfm2, head_loss2)
            
            # Afficher les résultats pour l'ensemble 2
            self.result_box2.clear()
            if combinations2:
                for combo in combinations2:
                    self.result_box2.addItem(f"{combo[0]} mm x {combo[1]} mm")
            else:
                self.result_box2.addItem("Aucune combinaison trouvée.")
            
            # Ajouter à l'historique
            history_entry = f"Ensemble 1: {cfm1} CFM, {head_loss1} Pa - Ensemble 2: {cfm2} CFM, {head_loss2} Pa"
            self.history_list_ductulator.addItem(history_entry)
            
        except ValueError as e:
            self.result_box1.clear()
            self.result_box1.addItem(f"Erreur : {str(e)}")
            self.result_box2.clear()
            self.result_box2.addItem(f"Erreur : {str(e)}")

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
