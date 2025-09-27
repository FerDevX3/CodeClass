from PyQt6 import uic
from PyQt6.QtWidgets import *

class RegistrosWindows(): 
    def __init__(self):
        self.v= uic.loadUi("gui/registrar.ui")
        self.v.show()
   