#librerias
import Conexion as con #se importa la clase conexion con la base de datos
from asistencias import Registrarasistencia # se importa la clase Registrarasistencia
from datetime import datetime #se eimporta la clase datetime

#objeto alumno o clase alumno que contiene todos los metodos relacionados para "RegistrarAlumno"
class AlumnoData():
    #se define la fucion que inicial la cual es conectarse ala base de dato y crear una tabla si no existe
    def __init__(self) -> None: 
         try:
            self.db = con.conexion().conectar()
            self.cursor = self.db.cursor()
            sql_tablaAsistencias  ="""CREATE TABLE IF NOT EXISTS Asistencias 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            NIE INT,
            fecha_y_hora date
            )"""
            
            self.cursor.execute(sql_tablaAsistencias )
            self.db.commit()
            self.cursor.close()
            self.db.close()
            #print("TABLA Asistencias OK")
         except Exception as ex :
            #print("TABLA Asistencias ",ex)
            print(ex)


   
    #se define una funcion que consulte a la base de datos por los nombres 
    def listanombre(self,seccion):
        
        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        res = self.cursor.execute("""select nombre from registros  WHERE seccion = 
        '{}' order by nombre""".format(seccion))
        nombre = res.fetchall()
        return nombre
    
    #se define una funcion que consulte a la base de datos por los apellidos 
    def listaapellido(self,seccion,nombre):
        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        res = self.cursor.execute("""select apellido from registros  WHERE seccion = 
        '{}' AND nombre = '{}'order by nombre""".format(seccion,nombre))
        apellido = res.fetchall()
        return apellido
    
    def listaA(self):
        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        res = self.cursor.execute("select DISTINCT seccion  from registros order by nombre")
        seccion = res.fetchall()
        return seccion
    
    def listaD(self,dato):
        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        if dato == 0:
            res = self.cursor.execute("select  DISTINCT modulo from modulos ")
        elif dato == 1:
            res = self.cursor.execute("select  DISTINCT NIE from modulos ")
        objeto = res.fetchall()
        return objeto
    
    def NIe(self,data:Registrarasistencia):
        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        res = self.cursor.execute("""SELECT NIE FROM registros WHERE 
        seccion =? AND apellido =? AND nombre = ?""",(data._sseccion,data._aapellido,data._nnombre))
        nie = res.fetchall()
        return nie
    
    

    def RegistrarAsistencia(self, nie, motivo,Des):
        fecha_y_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        self.cursor.execute(""" 
        INSERT INTO Asistencias (NIE, fecha_y_hora, motivo,Descripción) VALUES (?, ?, ?, ?)
    """, (nie, fecha_y_hora_actual, motivo,Des))
        self.db.commit()

        if self.cursor.rowcount == 1:
         return True
        else:
         return False
   
    def RegistrarScam(nie, motivo):
        fecha_y_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        db = con.conexion().conectar()
        cursor = db.cursor()
        cursor.execute(""" 
        INSERT INTO Asistencias (NIE, fecha_y_hora, motivo) VALUES (?, ?, ?)
     """, (nie, fecha_y_hora_actual, motivo))
        db.commit()
        if cursor.rowcount == 1:
         return True
        else:
         return False
   