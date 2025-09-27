import Conexion as con
from model.Modulos_Talleres import MODEL_Modulo, MODEL_alumno
from PyQt6 import uic
from PyQt6.QtWidgets import *

class  Modulos:   
    def __init__(self):
        pass

    def RegistrarModulo(self,MNombre, MDesde, MHasta, MDescription):
        db = con.conexion().conectar()
        cursor = db.cursor ()
        cursor.execute(""" 
        INSERT INTO talleres (modulo, FechaI,FechaF, Descrpcion) VALUES (?,?,?,?);
     """,(MNombre, MDesde, MHasta, MDescription))
        db.commit()
        self.mbox = QMessageBox()
        self.mbox.setText("Modulo guardado")
        self.mbox.exec()
        if cursor.rowcount == 1:
         return True
        else:
         return False

    def eliminar(self, id):
        pass 

    def registrar_alumno_a_modulo(self,MNie,modulo,MDia):
         db = con.conexion().conectar()
         
         cursor = db.cursor()
         cursor.execute(""" 
         INSERT INTO Modulos(NIE, modulo,Dias) VALUES (?, ?,?)
     """, (MNie, modulo,MDia))
         db.commit()
         if cursor.rowcount == 1:
          return True
         else:
           return False    
        
    def listaMo(self):
        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        res = self.cursor.execute("SELECT DISTINCT modulo FROM talleres ORDER BY modulo")
        modulo = res.fetchall()
        
        return modulo
        

          