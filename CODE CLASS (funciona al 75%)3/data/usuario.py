import Conexion as con
from model.user import Usuario

class UsuarioData():
   
       
    def login(self,usuario:Usuario):
        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        res = self.cursor.execute("SELECT *FROM usuarios WHERE usuario='{}' AND password = '{}'".format(usuario._usuario,usuario._password))
        fila = res.fetchone()
        if fila:
            usuario = Usuario(usuario =fila[1],password =fila[2])
            return usuario
        else:
            return None