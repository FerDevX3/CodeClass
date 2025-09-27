import Conexion as con
from PyQt6.QtWidgets import *
import sqlite3

class Historial():

    def BuscarPorFecha(self,FechaDesde,FechaHasta):
        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        resultado = self.cursor.execute(""" 
        SELECT
        res.NIE, res.seccion, res.nombre, res.apellido, asis.fecha_y_hora , asis.motivo, asis.Descripción
        FROM
        registros as res
        INNER JOIN
        Asistencias as asis 
        ON res.NIE = asis.NIE
        Where asis.fecha_y_hora>= ? AND asis.fecha_y_hora <= ? ;
  
        """,(FechaDesde,FechaHasta))
        Buscar  = resultado.fetchall() 
        self.db.commit()
        return Buscar

    def BuscarPorNIE(self,nie):#,nombre,apellido,seccion,fechaDesde,FechasHasta,Motivo)
        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        resultado = self.cursor.execute(""" 
        SELECT
        res.NIE, res.seccion, res.nombre, res.apellido, asis.fecha_y_hora,  asis.motivo, asis.Descripción       
        FROM
        registros as res
        INNER JOIN
        Asistencias as asis 
        ON res.NIE = asis.NIE
        Where res.NIE = ? ;
  
        """,(nie,))
        Buscar  = resultado.fetchall() 
        self.db.commit()
        return Buscar

    def BuscarNIE(nie):#,nombre,apellido,seccion,fechaDesde,FechasHasta,Motivo)
        db = con.conexion().conectar()
        cursor = db.cursor()
        resultado = cursor.execute(""" 
        select NIE, seccion
        FROM registros 
        Where NIE = ? ;
        """,(nie,))
        Buscar  = resultado.fetchall() 
        db.commit()
        return Buscar
                   
    def BuscarPorNombre(self,nombre,apellido,seccion):
        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        nombre_f = f"%{nombre}%"
        apellido_f = f"%{apellido}%"
        sql=""" 
        SELECT
        res.NIE, res.seccion, res.nombre, res.apellido, asis.fecha_y_hora,  asis.motivo, asis.Descripción       
        FROM
        registros as res
        INNER JOIN
        Asistencias as asis 
        ON res.NIE = asis.NIE
        Where res.nombre like ? AND res.apellido like ? AND res.seccion =?;
        """
        
        resultado = self.cursor.execute(sql,(nombre_f,apellido_f,seccion))
        Buscar  = resultado.fetchall() 
        self.db.commit()
        return Buscar

    def buscarporseccion(self,seccion):
        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        resultado = self.cursor.execute(""" 
        SELECT
        res.NIE, res.seccion, res.nombre, res.apellido, asis.fecha_y_hora,  asis.motivo, asis.Descripción       , asis.Descripción 
        FROM
        registros as res
        INNER JOIN
        Asistencias as asis 
        ON res.NIE = asis.NIE
        Where res.seccion =?;
        """,(seccion,))
        Buscar  = resultado.fetchall() 
        self.db.commit()
        return Buscar
         
        

    def buscarpormotivo(self,motivo):
        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        resultado = self.cursor.execute(""" 
        SELECT
        res.NIE, res.seccion, res.nombre, res.apellido, asis.fecha_y_hora,  asis.motivo, asis.Descripción       
        FROM
        registros as res
        INNER JOIN
        Asistencias as asis 
        ON res.NIE = asis.NIE
        Where asis.motivo =?;
        """,(motivo,))
        Buscar  = resultado.fetchall() 
        self.db.commit()
        return Buscar
        
    def buscarportodosloscampos(self,nie,nombre,apellido,seccion,fechasD,fechaH,motivo):    
        self.db = con.conexion().conectar()
        self.cursor = self.db.cursor()
        resultado = self.cursor.execute(""" 
        SELECT
        res.NIE, res.seccion, res.nombre, res.apellido, asis.fecha_y_hora, asis.motivo , asis.motivo, asis.Descripción
        FROM
        registros as res
        INNER JOIN
        Asistencias as asis 
        ON res.NIE = asis.NIE
        Where res.NIE= ? AND res.nombre= ? AND res.apellido = ? AND res.seccion = ? AND asis.fecha_y_hora>= ? AND asis.fecha_y_hora <= ? AND asis.motivo =?;
        """,(nie,nombre,apellido,seccion,fechasD,fechaH,motivo))
        Buscar  = resultado.fetchall() 
        self.db.commit()
        return Buscar