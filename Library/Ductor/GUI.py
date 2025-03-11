from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QDateEdit, QStackedWidget, QDialog,
    QFormLayout, QComboBox, QDialogButtonBox, QTextEdit, QInputDialog
)
from PyQt6.QtCore import QDate
import sys
from System import System
from Branche import Branche
from Duct import Duct
from Coude import Coude

class DesignPage(QWidget):
    def __init__(self):
        super().__init__()
        self.system = System("Système de Ventilation")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Résumé du système
        self.system_summary = QTextEdit()
        self.system_summary.setReadOnly(True)
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

        self.add_fitting_button = QPushButton("Ajouter un Raccord")
        self.add_fitting_button.setEnabled(False)
        self.add_fitting_button.clicked.connect(self.add_fitting)
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
    
    def add_fitting(self):
        selected_branch = self.branch_selector.currentText()
        if selected_branch != "Sélectionner une branche":
            dialog = AddFittingDialog(self.system, selected_branch)
            dialog.exec()
            self.update_summary()
    
    def update_summary(self):
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

        self.name = QLineEdit()
        self.length = QLineEdit()
        self.diameter = QLineEdit()
        self.flow = QLineEdit()

        form_layout.addRow("Nom:", self.name)
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
        duct = Duct(self.name.text(), float(self.length.text()), float(self.diameter.text()), float(self.flow.text()))
        for branch in self.system.branches:
            if branch.name == self.selected_branch:
                branch.ajouter_conduit(duct)
                break
        self.accept()

class AddFittingDialog(QDialog):
    def __init__(self, system, selected_branch):
        super().__init__()
        self.system = system
        self.selected_branch = selected_branch
        self.setWindowTitle("Ajouter un Raccord")
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.name = QComboBox()
        self.name.addItems(["Coude 90° long", "Coude 90° court", "Coude 45°", "Té symétrique", "Té asymétrique"])
        self.diameter = QLineEdit()
        self.flow = QLineEdit()
        
        form_layout.addRow("Type de Raccord:", self.name)
        form_layout.addRow("Diamètre (mm):", self.diameter)
        form_layout.addRow("Débit (CFM):", self.flow)

        layout.addLayout(form_layout)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.create_fitting)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)
    
    def create_fitting(self):
        mlc_values = {"Coude 90° long": 1.2, "Coude 90° court": 1.5, "Coude 45°": 0.8, "Té symétrique": 1.7, "Té asymétrique": 2.1}
        fitting = Coude(self.name.currentText(), mlc_values[self.name.currentText()], float(self.diameter.text()), float(self.flow.text()))
        for branch in self.system.branches:
            if branch.name == self.selected_branch:
                branch.ajouter_coude(fitting)
                break
        self.accept()

app = QApplication(sys.argv)
main_window = DesignPage()
main_window.show()
sys.exit(app.exec())