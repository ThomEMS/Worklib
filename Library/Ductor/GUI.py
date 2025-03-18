from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QDateEdit, QStackedWidget, QDialog,
    QFormLayout, QComboBox, QDialogButtonBox, QTextEdit, QInputDialog, QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt6.QtCore import QDate
import sys
from System import System
from fpdf import FPDF
from Branche import Branche
from Duct import Duct
from Coude import Coude
import os

class ProjectSetup(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
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
         # Collect user inputs
        client_name_str = self.client_name.text() or "Client inconnu"
        client_number_str = self.client_number.text() or "0000"
        calc_name_str = self.calc_name.text() or "Calcul"

        # Pass them to your DesignPage
        self.parent_app.design_page.set_project_info(
            client_name=client_name_str,
            project_number=client_number_str,
            calc_name=calc_name_str
        )
        self.parent_app.stacked_widget.setCurrentIndex(1)

class MyPDF(FPDF):
    def __init__(self, client_name, project_number, calc_name):
        super().__init__()
        self.client_name = client_name
        self.project_number = project_number
        self.calc_name = calc_name

    def header(self):
        # Path to your logo
        logo_path = os.path.abspath("company_logo.png")

        # Insert the logo (adjust x, y, w to suit your layout)
        self.image(logo_path, x=10, y=10, w=30)


        self.set_font("Arial", "B", 12)
        # Print a centered project header line
        self.cell(0, 8, f"Projet : {self.calc_name}", ln=True, align="C")

        self.cell(0, 8, f"Client: {self.client_name}", ln=True, align="C")

        # Then show the current date
        self.cell(0, 8, f"Date: {QDate.currentDate().toString('dd/MM/yyyy')}", ln=True, align="C")

        # Add a bit more spacing after
        self.ln(15)
         # Draw a line below the header area
        
        self.line(10, 35, 200, 35)

    def footer(self):
        # Position 15 mm from bottom
        self.set_y(-15)
        self.set_font("Arial", "I", 8)

        # Print the footer text, centered
        self.cell(0, 10, "Calculé par Ductor V0, tous droits réservés", 0, 0, "C")         


class DesignPage(QWidget):
    def __init__(self):
        super().__init__()
        self.system = None  # System will be initialized when receiving calc_name
        self.initUI()
    
    def set_project_info(self, client_name, project_number, calc_name):
        """Called by ProjectSetup to populate design page info."""
        self.client_name = client_name
        self.project_number = project_number
        self.calc_name = calc_name

        # Also create the system with a default name (calc_name, for example)
        self.system = System(self.calc_name)
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
        
        # Modify / Remove Button
        self.modify_remove_button = QPushButton("Modifier / Supprimer un élément")
        self.modify_remove_button.setEnabled(False)
        self.modify_remove_button.clicked.connect(self.modify_or_remove_item)
        layout.addWidget(self.modify_remove_button)
        
        # Export Button
        self.export_button = QPushButton("Exporter en PDF")
        self.export_button.clicked.connect(self.export_to_pdf)
        layout.addWidget(self.export_button)
        
        self.setLayout(layout)
    
    def add_branch(self):
        branch_name, ok = QInputDialog.getText(self, "Nouvelle Branche", "Nom de la branche:")
        if ok and branch_name:
            new_branch = Branche(branch_name)
            self.system.ajouter_branche(new_branch)
            self.branch_selector.addItem(branch_name)
            self.update_summary()
    
    def add_duct(self):
        """Triggered when user clicks 'Ajouter un Conduit'."""
        selected_branch = self.branch_selector.currentText()
        if selected_branch == "Sélectionner une branche":
            return

        # Create the dialog just for length, diameter, flow
        dialog = AddDuctDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Find the branch object
            branch = next((b for b in self.system.branches if b.name == selected_branch), None)
            if not branch:
                return

            # Generate an automatic name like <branchName><index>
            duct_count = len(branch.conduits) + 1
            auto_name = f"{selected_branch}{duct_count}"

            # Create the duct
            try:
                length = float(dialog.length.text())
                diameter = float(dialog.diameter.text())
                flow = float(dialog.flow.text())
            except ValueError:
                # Handle invalid numeric input
                return

            duct = Duct(auto_name, length, diameter, flow)
            branch.ajouter_conduit(duct)

            self.update_summary()
    
    def add_multiple_fittings(self):
        selected_branch = self.branch_selector.currentText()
        if selected_branch != "Sélectionner une branche":
            dialog = AddMultipleFittingsDialog(self.system, selected_branch)
            dialog.exec()
            self.update_summary()
    
    def modify_or_remove_item(self):
        selected_branch = self.branch_selector.currentText()
        if selected_branch == "Sélectionner une branche":
            return
        
        branch = next((b for b in self.system.branches if b.name == selected_branch), None)
        if not branch:
            return
        
        items = [f"Conduit: {c.name}" for c in branch.conduits] + [f"Raccord: {r.name}" for r in branch.coudes]
        item, ok = QInputDialog.getItem(self, "Modifier / Supprimer un élément", "Sélectionner un élément:", items, editable=False)
        
        if ok and item:
            for conduit in branch.conduits:
                if f"Conduit: {conduit.name}" == item:
                    action, ok = QInputDialog.getItem(self, "Action", "Que voulez-vous faire?", ["Modifier", "Supprimer"], editable=False)
                    if ok:
                        if action == "Modifier":
                            self.modify_duct(branch, conduit)
                        elif action == "Supprimer":
                            branch.conduits.remove(conduit)
            
            for raccord in branch.coudes:
                if f"Raccord: {raccord.name}" == item:
                    action, ok = QInputDialog.getItem(self, "Action", "Que voulez-vous faire?", ["Modifier", "Supprimer"], editable=False)
                    if ok:
                        if action == "Modifier":
                            self.modify_fitting(branch, raccord)
                        elif action == "Supprimer":
                            branch.coudes.remove(raccord)
        
        self.update_summary()
    
    def modify_duct(self, branch, conduit):
        length, ok = QInputDialog.getDouble(self, "Modifier Conduit", "Nouvelle Longueur (m):", conduit.length, 0.1, 100.0, 2)
        if ok:
            conduit.length = length
        diameter, ok = QInputDialog.getDouble(self, "Modifier Conduit", "Nouveau Diamètre (mm):", conduit.diameter, 50, 1000, 2)
        if ok:
            conduit.diameter = diameter
        self.update_summary()
    
    def modify_fitting(self, branch, raccord):
        mlc, ok = QInputDialog.getDouble(self, "Modifier Raccord", "Nouveau MLC:", raccord.mlc, 0.1, 10.0, 2)
        if ok:
            raccord.mlc = mlc
        self.update_summary()
    
    def update_summary(self):
        if not self.system:
            return
        
        self.system_summary.setText(str(self.system))

    def update_buttons(self):
        has_selection = self.branch_selector.currentText() != "Sélectionner une branche"
        self.add_duct_button.setEnabled(has_selection)
        self.add_fitting_button.setEnabled(has_selection)
        self.modify_remove_button.setEnabled(has_selection)
    
        
    def export_to_pdf(self):
        if not self.system:
            return
        
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Exporter en PDF", "", "PDF Files (*.pdf);;All Files (*)"
        )
        
        if file_name:
            if not file_name.endswith(".pdf"):
                file_name += ".pdf"
            
            pdf = MyPDF(
                client_name=self.client_name,
                project_number=self.project_number,
                calc_name=self.calc_name
            )
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            # Main body content
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 8, str(self.system))

            pdf.output(file_name)



class AddDuctDialog(QDialog):
    def __init__(self):
        super().__init__()
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

        # OK / Cancel
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.validate_inputs)  # Validate on OK
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def validate_inputs(self):
        """
        Validate each input. If any are invalid, highlight them in red
        and prevent closing by returning early. Otherwise accept().
        """
        valid = True

        # Clear previous highlights
        self.length.setStyleSheet("")
        self.diameter.setStyleSheet("")
        self.flow.setStyleSheet("")

        # 1) Validate length
        try:
            length_val = float(self.length.text())
            if length_val <= 0:
                raise ValueError("Length must be positive")
        except ValueError:
            self.length.setStyleSheet("background-color: #ffcccc;")  # red highlight
            valid = False

        # 2) Validate diameter
        try:
            diameter_val = float(self.diameter.text())
            if diameter_val <= 0:
                raise ValueError("Diameter must be positive")
        except ValueError:
            self.diameter.setStyleSheet("background-color: #ffcccc;")
            valid = False

        # 3) Validate flow
        try:
            flow_val = float(self.flow.text())
            if flow_val < 0:
                raise ValueError("Flow cannot be negative")
        except ValueError:
            self.flow.setStyleSheet("background-color: #ffcccc;")
            valid = False

        if not valid:
            # Optionally show a message box to the user
            QMessageBox.warning(self, "Invalid Input", "Please correct the highlighted fields.")
            return  # Do not close the dialog

        # If all inputs valid
        self.accept()  # Closes dialog with DialogCode.Accepted
    
    
class AddMultipleFittingsDialog(QDialog):
    def __init__(self, system, selected_branch):
        super().__init__()
        self.system = system
        self.selected_branch = selected_branch
        self.setWindowTitle("Ajouter Plusieurs Raccords")
        self.layout = QVBoxLayout()
        
        self.fitting_entries = []
        self.add_fitting_row()  # Start with one standard fitting row by default
        
        self.add_more_button = QPushButton("Ajouter un autre type de raccord")
        self.add_more_button.clicked.connect(self.add_fitting_row)
        self.layout.addWidget(self.add_more_button)
        
        self.add_custom_button = QPushButton("Ajouter un raccord personnalisé")
        self.add_custom_button.clicked.connect(self.add_custom_fitting_row)
        self.layout.addWidget(self.add_custom_button)

        # Global diameter/flow fields
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
        """
        Adds a row for a standard fitting.
        The user picks from a QComboBox and provides a quantity.
        """
        row_layout = QHBoxLayout()
        fitting_type = QComboBox()
        fitting_type.addItems([
            "Coude 90° Aube", "Coude 90° court", "Coude 45°", 
            "Té vers Branche", "Duct to room", "Grilles", "Room to duct"
        ])
        quantity = QLineEdit()
        quantity.setPlaceholderText("Quantité")
        row_layout.addWidget(fitting_type)
        row_layout.addWidget(quantity)
        # Insert above the last 4 elements (buttons, etc.)
        self.layout.insertLayout(self.layout.count() - 4, row_layout)
        self.fitting_entries.append((fitting_type, quantity))
    
    def add_custom_fitting_row(self):
        """
        Adds a row for a custom fitting:
        - QLineEdit for name
        - QLineEdit for MLC
        - QLineEdit for quantity
        """
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
        """
        Validate the user inputs (highlight invalid fields in red).
        If everything is valid, create the fittings and accept the dialog.
        """
        from PyQt6.QtWidgets import QMessageBox  # Ensure you've imported this at top-level as well

        # Clear old highlights
        self.diameter.setStyleSheet("")
        self.flow.setStyleSheet("")

        valid = True
        
        # 1) Validate global diameter
        try:
            d_val = float(self.diameter.text())
            if d_val <= 0:
                raise ValueError()
        except ValueError:
            self.diameter.setStyleSheet("background-color: #ffcccc;")
            valid = False
        
        # 2) Validate global flow
        try:
            f_val = float(self.flow.text())
            if f_val < 0:
                raise ValueError()
        except ValueError:
            self.flow.setStyleSheet("background-color: #ffcccc;")
            valid = False

        # We'll store which rows are valid so we only create them if all is good
        parsed_entries = []  # (fitting_name, mlc, qty) or (custom_name, custom_mlc, qty)

        mlc_values = {
            "Coude 90° Aube": 0.7,
            "Coude 90° court": 1.3,
            "Coude 45°": 0.5,
            "Té vers Branche": 0.3,
            "Duct to room": 1,
            "Grilles": 6,
            "Room to duct": 0.35
        }
        
        # 3) Validate each fitting row
        for entry in self.fitting_entries:
            if isinstance(entry[0], QComboBox):
                # Standard fitting row => (QComboBox, QLineEdit)
                combo_box, qty_line = entry
                qty_line.setStyleSheet("")

                try:
                    qty_val = int(qty_line.text())
                    if qty_val <= 0:
                        raise ValueError()
                except ValueError:
                    qty_line.setStyleSheet("background-color: #ffcccc;")
                    valid = False
                    continue  # skip storing this entry

                fitting_name = combo_box.currentText()
                mlc = mlc_values[fitting_name]  # guaranteed from dictionary
                parsed_entries.append((fitting_name, mlc, qty_val))
            
            else:
                # Custom fitting row => (QLineEdit custom_name, QLineEdit custom_mlc, QLineEdit quantity)
                custom_name, custom_mlc, qty_line = entry
                custom_name.setStyleSheet("")
                custom_mlc.setStyleSheet("")
                qty_line.setStyleSheet("")

                # Validate name not empty
                if not custom_name.text().strip():
                    custom_name.setStyleSheet("background-color: #ffcccc;")
                    valid = False
                    continue

                try:
                    mlc_val = float(custom_mlc.text())
                    if mlc_val <= 0:
                        raise ValueError()
                except ValueError:
                    custom_mlc.setStyleSheet("background-color: #ffcccc;")
                    valid = False
                    continue

                try:
                    qty_val = int(qty_line.text())
                    if qty_val <= 0:
                        raise ValueError()
                except ValueError:
                    qty_line.setStyleSheet("background-color: #ffcccc;")
                    valid = False
                    continue

                parsed_entries.append((custom_name.text(), mlc_val, qty_val))

        # If anything is invalid, show message and keep dialog open
        if not valid:
            QMessageBox.warning(self, "Invalid Input", "Veuillez corriger les champs en surbrillance.")
            return

        # 4) If valid => create the fittings and accept the dialog
        # Insert them into the branch
        for entry in parsed_entries:
            if entry[0] in mlc_values:
                # It's a standard fitting
                fitting_name, mlc, qty = entry
                for _ in range(qty):
                    fitting = Coude(fitting_name, mlc, d_val, f_val)
                    for branch in self.system.branches:
                        if branch.name == self.selected_branch:
                            branch.ajouter_coude(fitting)
                            break
            else:
                # It's a custom fitting
                custom_name, custom_mlc, qty = entry
                for _ in range(qty):
                    fitting = Coude(custom_name, custom_mlc, d_val, f_val)
                    for branch in self.system.branches:
                        if branch.name == self.selected_branch:
                            branch.ajouter_coude(fitting)
                            break

        self.accept()  # close the dialog with DialogCode.Accepted


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()

        # Instantiate the pages
        self.project_setup = ProjectSetup(self)  # pass 'self' -> the App
        self.design_page = DesignPage()

        # Add them to stacked_widget
        self.stacked_widget.addWidget(self.project_setup)
        self.stacked_widget.addWidget(self.design_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)


app = QApplication(sys.argv)
main_window = App()
main_window.show()
sys.exit(app.exec())
