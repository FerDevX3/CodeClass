from PyQt6.QtWidgets import QApplication
from gui.login import Login 

class CodeClass():
    def __init__(self):
        self.app = QApplication([])    # Crear QApplication
        self.login = Login()  
        
        self.app.exec() # Mostrar ventana

