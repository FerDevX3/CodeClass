import Conexion as con
from model.RgistrarAlum import Registrarestudiante

class registroData():

    def __init__(self) -> None:
         try:
            self.db = con.conexion().conectar()
            self.cursor = self.db.cursor()
            sql_tablaRegistros  ="""CREATE TABLE IF NOT EXISTS Registros 
            (id INTEGER  AUTOINCREMENT,
            NIE INT PRIMARY KEY UNIQUE,
            seccion varchar(3) not null,
            apellido varchar(50) not null,
            nombre varchar(50) not null
            )"""
            
            self.cursor.execute(sql_tablaRegistros )
            self.db.commit()
            self.cursor.close()
            self.db.close()
            print("TABLA REGISTROS OK")
         except Exception as ex :
            print("TABLA REGISTROS NO LOGRADO")
       
    def RegistarAlumn(self,info:Registrarestudiante):
        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        self.cursor.execute(""" 
        INSERT INTO Registros (NIE,seccion,apellido,nombre) VALUES ({},'{}','{}','{}')
        """.format(info._nie,info._seccion,info._apellido,info._nombre))
        self.db.commit()
        if self.cursor.rowcount == 1:
            return True
        else:
            return False
        
        