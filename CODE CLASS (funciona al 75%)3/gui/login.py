from PyQt6 import uic
from PyQt6.QtWidgets import *

from gui.main import MainWindows
from model.user import Usuario
from data.usuario import UsuarioData
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression



class Login(): 
    def __init__(self):
        self.login = uic.loadUi("gui/login.ui")
        self.initGUI() 
        self.login.lblerror.setText("")
        self.regex = QRegularExpression("^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ. ]+$")
        self.validator = QRegularExpressionValidator(self.regex)
        self.login.txtusuario.setValidator(self.validator)
        
        
        self.login.show()

    def log(self):
        if self.login.txtusuario.text() == "":
            self.login.lblerror.setText("INGRESE USUARIO VALIDO")
            self.login.txtusuario.setFocus()
        elif self.login.txtclave.text() == "":
            self.login.lblerror.setText("INGRESE CONTRASEÑA VALIDA")   
            self.login.txtclave.setFocus() 
        else:
            self.login.lblerror.setText("")
            usu = Usuario(usuario=self.login.txtusuario.text(),password=self.login.txtclave.text())
            usuData = UsuarioData()
            usuData.login(usu)
            res = usuData.login(usu)
            if res:
               self.main = MainWindows()
               self.login.hide()
            else:
                self.login.lblerror.setText("CREDENCIALES NO VALIDAS")    
    def initGUI(self):
        self.login.btnAcceder.clicked.connect(self.log)  