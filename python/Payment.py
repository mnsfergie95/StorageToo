from PyQt6.QtWidgets import QMessageBox, QDialog
from UI.dlgPayment_ui import Ui_dlgPayment

class Payment(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_dlgPayment()
        self.ui.setupUi(self)

       
    