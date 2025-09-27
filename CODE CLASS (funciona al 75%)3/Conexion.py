import sqlite3

class conexion():
    def __init__(self):

        try:
            self.con = sqlite3.connect("estudiates.db")
            #self.create_tablas()
        except Exception as ex:
            print(ex)

    def create_tablas(self):
        sql_tabla ="""CREATE TABLE IF NOT EXISTS usuarios 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario text ,
        password text)"""
        cur = self.con.cursor()
        cur.execute(sql_tabla)
        cur.close()
        self.create_admis()

    def create_admis(self):
        try:
            sql_admis =""" INSERT INTO usuarios(usuario,password) VALUES ('{}','{}')""".format("leo.mnjvr","leo12345")
            cur = self.con.cursor()
            cur.execute(sql_admis)
            self.con.commit()
        except Exception as ex:
            print(ex)
            
    def conectar(self):
        return self.con


    
