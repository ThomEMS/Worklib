from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QDateEdit, QStackedWidget, QDialog,
    QFormLayout, QComboBox, QDialogButtonBox, QTextEdit, QInputDialog, QHBoxLayout
)
from PyQt6.QtCore import QDate
import sys
from System import System
from Branche import Branche
from Duct import Duct
from Coude import Coude

class ProjectSetup(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.client_name = QLineEdit()
        self.client_number = QLineEdit()
        self.calc_name = QLineEdit()
        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())
        self.client_number.textChanged.connect(self.update_calc_name)

        form_layout = QFormLayout()
        form_layout.addRow("Nom du Client:", self.client_name)
        form_layout.addRow("No Client:", self.client_number)
        form_layout.addRow("Nom du Calcul:", self.calc_name)
        form_layout.addRow("Date:", self.date)
        layout.addLayout(form_layout)

        self.next_button = QPushButton("Suivant")
        self.next_button.clicked.connect(self.go_to_design_page)
        layout.addWidget(self.next_button)
        
        self.setLayout(layout)
    
    def update_calc_name(self):
        self.calc_name.setText(f"{self.client_number.text()}_Calcul d'Air")

    def go_to_design_page(self):
        calc_name = self.calc_name.text() if self.calc_name.text() else "Système de Ventilation"
        
        # Retrieve the DesignPage instance from the stacked widget
        design_page = self.stacked_widget.widget(1)  # Assuming DesignPage is the second widget (index 1)
        design_page.set_system_name(calc_name)
        
        self.stacked_widget.setCurrentIndex(1)

class DesignPage(QWidget):
    def __init__(self):
        super().__init__()
        self.system = None  # System will be initialized when receiving calc_name
        self.initUI()

    def set_system_name(self, calc_name):
        self.system = System(calc_name)
        self.update_summary()

    def initUI(self):
        layout = QVBoxLayout()

        # Résumé du système avec indentation
        self.system_summary = QTextEdit()
        self.system_summary.setReadOnly(True)
        self.system_summary.setPlaceholderText("Résumé du système...")
        layout.addWidget(self.system_summary)

        # Menu déroulant pour sélectionner une branche
        self.branch_selector = QComboBox()
        self.branch_selector.addItem("Sélectionner une branche")
        self.branch_selector.currentIndexChanged.connect(self.update_buttons)
        layout.addWidget(self.branch_selector)

        # Boutons
        self.add_branch_button = QPushButton("Nouvelle Branche")
        self.add_branch_button.clicked.connect(self.add_branch)
        layout.addWidget(self.add_branch_button)

        self.add_duct_button = QPushButton("Ajouter un Conduit")
        self.add_duct_button.setEnabled(False)
        self.add_duct_button.clicked.connect(self.add_duct)
        layout.addWidget(self.add_duct_button)

        self.add_fitting_button = QPushButton("Ajouter plusieurs Raccords")
        self.add_fitting_button.setEnabled(False)
        self.add_fitting_button.clicked.connect(self.add_multiple_fittings)
        layout.addWidget(self.add_fitting_button)
        
        self.setLayout(layout)
    
    def add_branch(self):
        branch_name, ok = QInputDialog.getText(self, "Nouvelle Branche", "Nom de la branche:")
        if ok and branch_name:
            new_branch = Branche(branch_name)
            self.system.ajouter_branche(new_branch)
            self.branch_selector.addItem(branch_name)
            self.update_summary()
    
    def add_duct(self):
        selected_branch = self.branch_selector.currentText()
        if selected_branch != "Sélectionner une branche":
            dialog = AddDuctDialog(self.system, selected_branch)
            dialog.exec()
            self.update_summary()
    
    def add_multiple_fittings(self):
        selected_branch = self.branch_selector.currentText()
        if selected_branch != "Sélectionner une branche":
            dialog = AddMultipleFittingsDialog(self.system, selected_branch)
            dialog.exec()
            self.update_summary()
    
    def update_summary(self):
        if not self.system:
            return
        
        self.system_summary.setText(str(self.system))

    def update_buttons(self):
        has_selection = self.branch_selector.currentText() != "Sélectionner une branche"
        self.add_duct_button.setEnabled(has_selection)
        self.add_fitting_button.setEnabled(has_selection)

class AddDuctDialog(QDialog):
    def __init__(self, system, selected_branch):
        super().__init__()
        self.system = system
        self.selected_branch = selected_branch
        self.setWindowTitle("Ajouter un Conduit")
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.length = QLineEdit()
        self.diameter = QLineEdit()
        self.flow = QLineEdit()

        form_layout.addRow("Longueur (m):", self.length)
        form_layout.addRow("Diamètre (mm):", self.diameter)
        form_layout.addRow("Débit (CFM):", self.flow)

        layout.addLayout(form_layout)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.create_duct)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)
    
    def create_duct(self):
        duct = Duct(float(self.length.text()), float(self.diameter.text()), float(self.flow.text()))
        for branch in self.system.branches:
            if branch.name == self.selected_branch:
                branch.ajouter_conduit(duct)
                break
        self.accept()

class AddMultipleFittingsDialog(QDialog):
    def __init__(self, system, selected_branch):
        super().__init__()
        self.system = system
        self.selected_branch = selected_branch
        self.setWindowTitle("Ajouter Plusieurs Raccords")
        self.layout = QVBoxLayout()
        
        self.fitting_entries = []
        self.add_fitting_row()
        
        self.add_more_button = QPushButton("Ajouter un autre type de raccord")
        self.add_more_button.clicked.connect(self.add_fitting_row)
        self.layout.addWidget(self.add_more_button)
        
        self.add_custom_button = QPushButton("Ajouter un raccord personnalisé")
        self.add_custom_button.clicked.connect(self.add_custom_fitting_row)
        self.layout.addWidget(self.add_custom_button)

        self.diameter = QLineEdit()
        self.flow = QLineEdit()
        
        form_layout = QFormLayout()
        form_layout.addRow("Diamètre (mm):", self.diameter)
        form_layout.addRow("Débit (CFM):", self.flow)
        self.layout.addLayout(form_layout)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.create_fittings)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)
        self.setLayout(self.layout)
    
    def add_fitting_row(self):
        row_layout = QHBoxLayout()
        fitting_type = QComboBox()
        fitting_type.addItems(["Coude 90° Aube", "Coude 90° court", "Coude 45°", "Té vers Branche", "Duct to room", "Grilles", "Room to duct"])
        quantity = QLineEdit()
        quantity.setPlaceholderText("Quantité")
        row_layout.addWidget(fitting_type)
        row_layout.addWidget(quantity)
        self.layout.insertLayout(self.layout.count() - 4, row_layout)
        self.fitting_entries.append((fitting_type, quantity))
    
    def add_custom_fitting_row(self):
        row_layout = QHBoxLayout()
        custom_name = QLineEdit()
        custom_name.setPlaceholderText("Nom du raccord")
        custom_mlc = QLineEdit()
        custom_mlc.setPlaceholderText("MLC")
        quantity = QLineEdit()
        quantity.setPlaceholderText("Quantité")
        row_layout.addWidget(custom_name)
        row_layout.addWidget(custom_mlc)
        row_layout.addWidget(quantity)
        self.layout.insertLayout(self.layout.count() - 4, row_layout)
        self.fitting_entries.append((custom_name, custom_mlc, quantity))
    
    def create_fittings(self):
        mlc_values = {"Coude 90° Aube": 0.7, "Coude 90° court": 1.3, "Coude 45°": 0.5, "Té vers Branche": 0.3, "Duct to room": 1, "Grilles": 6, "Room to duct": 0.35}
        
        for entry in self.fitting_entries:
            if isinstance(entry[0], QComboBox):  # Standard fitting
                fitting_name = entry[0].currentText()
                try:
                    qty = int(entry[1].text())
                except ValueError:
                    qty = 1
                for _ in range(qty):
                    fitting = Coude(fitting_name, mlc_values[fitting_name], float(self.diameter.text()), float(self.flow.text()))
                    for branch in self.system.branches:
                        if branch.name == self.selected_branch:
                            branch.ajouter_coude(fitting)
                            break
            else:  # Custom fitting
                custom_name = entry[0].text()
                try:
                    custom_mlc = float(entry[1].text())
                    qty = int(entry[2].text())
                except ValueError:
                    continue  # Skip invalid entries
                for _ in range(qty):
                    fitting = Coude(custom_name, custom_mlc, float(self.diameter.text()), float(self.flow.text()))
                    for branch in self.system.branches:
                        if branch.name == self.selected_branch:
                            branch.ajouter_coude(fitting)
                            break
        self.accept()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DUCTOR V0")
        self.stacked_widget = QStackedWidget()

        self.project_setup = ProjectSetup(self.stacked_widget)
        self.design_page = DesignPage()

        self.stacked_widget.addWidget(self.project_setup)
        self.stacked_widget.addWidget(self.design_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

app = QApplication(sys.argv)
main_window = App()
main_window.show()
sys.exit(app.exec())
