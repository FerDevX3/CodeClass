from datetime import date
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from data.mODULOS import Modulos
from graficas import generar_grafica
from gui.GraphViewer import GraphViewer
import sys
import os

from model.Modulos_Talleres import MODEL_Modulo, MODEL_alumno
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Lector import scan

from asistencias import Registrarasistencia
from data.Alumnos import AlumnoData
from data.historial import Historial

from model.RgistrarAlum import *
from gui.Registrar import *
from data.registrarData import registroData
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QIntValidator
from gui.login  import *



class MainWindows(): 
    def __init__(self):
        self.menu = uic.loadUi("gui/menu.ui")
        self.initGI() 
        #self.main = MainWindows()
        self.menu.showMaximized()
        

    def initGI(self):
        self.menu.actionRegistrar_Alumnos.triggered.connect(self.AbrirRegistro)
        self.menu.actionVer_Grafica.triggered.connect(self.abrir_visualizador_grafica)
        self.menu.actionRegristrar_Asistensia.triggered.connect(self.AbrirAsistencias)
        self.menu.actionHistorial.triggered.connect(self.abrirhistorial)
        self.menu.actionRegistrar_M_dulo.triggered.connect(self.MenuModulo)
        self.menu.actionRegistrar_Alumno.triggered.connect(self.res_alumno_modulo)
        self.menu.actionEliminar.triggered.connect(self.Eliminar_modulo_o_alumno)
        self.registro = uic.loadUi("gui/registrar.ui")
        self.Asistencias = uic.loadUi("gui/registrar_asistencia.ui")
        self.Historial = uic.loadUi("gui/Historial.ui")
        self.modulos = Modulos()



    def Eliminar_modulo_o_alumno(self):
        self.EModulo_alumno = uic.loadUi("gui/elmodulo.ui")
        self.EModulo_alumno.btnMEliminar.clicked.connect(self.Eli_M_A)
        self.EModulo_alumno.cbMDatos.currentIndexChanged.connect(self.llenarDatos)

        self.llenarDatos()
        self.EModulo_alumno.show()
    
    def Eli_M_A(self):
        pass
        

    def res_alumno_modulo(self):
        self.res_alum_a_modulo = uic.loadUi("gui/almodulos.ui")
        self.res_alum_a_modulo.btnMAlumnor.clicked.connect(self.RegistrarAModulo)
        self.llenarcbMO()
        self.res_alum_a_modulo.show()

    def MenuModulo(self):
        self.resmodulo= uic.loadUi("gui/regmodulo.ui")
        self.resmodulo.btnMModulo.clicked.connect(self.SegRegistrar)
        self.resmodulo.show()

    def SegRegistrar (self):
        object = MODEL_Modulo(  
                MNombre = self.resmodulo.txtMNombreM.text(),
                MDesde = self.resmodulo.timeIni.time().toString("hh:mm"),
                MHasta = self.resmodulo.timeFin.time().toString("hh:mm"),
                MDescription = self.resmodulo.txtMDes.toPlainText())
        self.modulos.RegistrarModulo(object.MNombre, object.MDesde, object.MHasta, object.MDescription)
        
    def RegistrarAModulo(self):
         
         dias_seleccionados = []  
    
         if self.res_alum_a_modulo.CheckLunes.isChecked():
            dias_seleccionados.append("Lunes")
            
         if self.res_alum_a_modulo.CheckMartes.isChecked():
            dias_seleccionados.append("Martes")
            
         if self.res_alum_a_modulo.CheckMiercoles.isChecked():
            dias_seleccionados.append("Miercoles")
            
         if self.res_alum_a_modulo.CheckJueves.isChecked():
            dias_seleccionados.append("Jueves")
            
         if self.res_alum_a_modulo.CheckViernes.isChecked():
            dias_seleccionados.append("Viernes")

         dias_str = ",".join(dias_seleccionados)
         
         object = MODEL_alumno(
                        MNie = self.res_alum_a_modulo. txtMNIE.text(),
                        Mmodulo = self.res_alum_a_modulo.cbMmodulos.currentText(),
                        MDia=dias_str)
         self.modulos.registrar_alumno_a_modulo(object.MNie, object.Mmodulo,object.MDia)
        #fecha_y_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    

        
        
    
    def abrirhistorial(self):
        self.Historial.btnBuscar.clicked.connect(self.Busqueda)
        self.llenarcbseccionHistorial()
        self.Historial.show()

    def abrirmodulos(self):
            
            self.modulos = Modulos()
            self.module_ui = uic.loadUi("gui/Modulos_H.ui") # Cargar la UI una sola vez
            
            # Asignar la UI cargada al objeto de la clase Modulos
            self.modulos.module = self.module_ui,
            # Conectar los botones a los métodos de la clase Modulos
            self.module_ui.btnMModulo.clicked.connect(self.modulos.RegistrarAModulo),
            self.module_ui.btnMAlumnor.clicked.connect(lambda: self.modulos.RegistrarAModulo(self.module_ui.txtMNIE.text(), self.module_ui)),
            self.module_ui.btnMEliminar.clicked.connect(self.modulos.eliminar),
            self.llenarcbMO(),
            self.module_ui.showMaximized()

            
        

    def AbrirRegistro(self):
        self.registro.btnIngresar.clicked.connect(self.registrarAlumno)
        self.registro.msmerror_2.setText("")
        self.regex = QRegularExpression("^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ ]+$")
        self.validator = QRegularExpressionValidator(self.regex)
        self.nie_validator = QIntValidator()
        self.registro.txtnie.setValidator(self.nie_validator)  # <--- Y esto
        self.registro.txtnombre.setValidator(self.validator)
        self.registro.show()   
     
    def AbrirAsistencias(self):
        self.Asistencias.btnIngresar.clicked.connect(self.registrarAsistencia)
        self.Asistencias.cbseccion.currentIndexChanged.connect(self.llenarcbnombre)
        self.Asistencias.cbseccion.currentIndexChanged.connect(self.llenarcbapellido)
        self.Asistencias.btnCamWeb.clicked.connect(scan)
      #  self.Asistencias.cbnombre.currentIndexChanged.connect(self.llenarcbapellido)
        self.llenarcbseccion()
        self.Asistencias.show() 
      #  self.llenarcbnombre()  
       # self.llenarcbapellido()
        
    
#################  Registrar alumno  ##############
    def registrarAlumno(self):
        self.registro.txtnie.setValidator(self.nie_validator)
        self.nombre = self.registro.txtnombre.text()
        self.apellido = self.registro.txtapellido.text()
        self.nie = self.registro.txtnie.text()

        if self.nie == "":
         self.mbox = QMessageBox()
         self.mbox.setText("DEBE DIGITAR UN NIE ")
         self.mbox.exec()
         self.registro.txtnie.setFocus()   
        elif self.validator.validate(self.nombre, 0)[0] != QRegularExpressionValidator.State.Acceptable:
          self.mbox = QMessageBox()
          self.mbox.setText("DEBE DIGITAR UN NOMBRE VÁLIDO (solo letras)")
          self.mbox.exec() 
          self.registro.txtnombre.setFocus()
        elif self.validator.validate(self.apellido, 0)[0] != QRegularExpressionValidator.State.Acceptable:
         self.mbox = QMessageBox()
         self.mbox.setText("DEBE DIGITAR UN APELLIDO VÁLIDO (solo letras)")
         self.mbox.exec()
         self.registro.txtapellido.setFocus()
        elif self.registro.cbseccion.currentText() == "Seleccionar Seccion":
         self.mbox = QMessageBox()
         self.mbox.setText("DEBE ELEGIR UNA SECCION")
         self.mbox.exec()
         self.registro.cbseccion.setFocus() 
        else:
            registrarA = Registrarestudiante(
            seccion = self.registro.cbseccion.currentText(),
            nombre = self.registro.txtnombre.text().capitalize() ,
            apellido = self.registro.txtapellido.text().capitalize() ,
            nie = self.registro.txtnie.text()
            )
            objData = registroData()
            mbox = QMessageBox()
            if objData.RegistarAlumn(info=registrarA):
                mbox.setText("REGISTRO GUARDADO")
                self.limpiarRegistro()
            else :
                mbox.setText("NO FUE POSIBLE GUARDAR EL REGISTRO")
            mbox.exec()   


    def limpiarRegistro(self):
        self.registro.txtnie.setText("")
        self.registro.txtnombre.setText("")
        self.registro.txtapellido.setText("")
        self.registro.cbseccion.setCurrentIndex(0)
       
################   Registrar Asistencias ##############
    
    
    def llenarcbMO(self):
            objData = Modulos()
            modulo = objData.listaMo()
            # Referencia corregida al objeto de la interfaz de usuario
            self.res_alum_a_modulo.cbMmodulos.clear()
            # Extrae el primer elemento de cada tupla para rellenar el combobox
            for item in modulo:
                self.res_alum_a_modulo.cbMmodulos.addItem(item[0])
        
    def llenarcbnombre(self):
        
        objData = AlumnoData()
        datos = objData.listanombre(self.Asistencias.cbseccion.currentText())
        self.Asistencias.cbnombre.clear()
        for item in datos:
            self.Asistencias.cbnombre.addItem(item[0])

    def llenarcbapellido(self):
        self.Asistencias.cbnombre.currentIndexChanged.connect(self.llenarcbapellido)
        objData = AlumnoData()
        datos = objData.listaapellido(self.Asistencias.cbseccion.currentText(),self.Asistencias.cbnombre.currentText())
        self.Asistencias.cbapellido.clear()
        for item in datos:
            self.Asistencias.cbapellido.addItem(item[0])
        
    def llenarcbseccion(self):
        objData = AlumnoData()
        datos = objData.listaA()
        self.Asistencias.cbseccion.clear()
        for item in datos:
            self.Asistencias.cbseccion.addItem(item[0])

    def llenarDatos(self):
        objData = AlumnoData()
        datos = objData.listaD(self.EModulo_alumno.cbMDatos.currentIndex())
        self.EModulo_alumno.cbMObjetos.clear()
        for item in datos:
            self.EModulo_alumno.cbMObjetos.addItem(str(item[0]), item[0])        
    
    def registrarAsistencia(self):
    
        if self.Asistencias.cbseccion.currentText() == "Seleccionar Sección":
            mbox = QMessageBox()
            mbox.setText("DEBE ELEGIR UNA SECCION")
            mbox.exec()
            self.Asistencias.cbseccion.setFocus()   
        elif self.Asistencias.cbnombre.currentText() == "Seleccionar Nombre":
            mbox = QMessageBox()
            mbox.setText("DEBE ELEGIR UN NOMBRE")
            mbox.exec()
            self.Asistencias.cbnombre.setFocus()   
        elif self.Asistencias.cbapellido.currentText() == "Seleccionar Apellido":
            mbox = QMessageBox()
            mbox.setText("DEBE ELEGIR UN APELLIDO")
            mbox.exec()
            self.Asistencias.cbapellido.setFocus()  
        elif self.Asistencias.cbmotivo.currentText() == "Seleccionar Motivo":
            mbox = QMessageBox()
            mbox.setText("DEBE ELEGIR UN MOTIVO")
            mbox.exec()
            self.Asistencias.cbmotivo.setFocus()        
        else:
            registraA= Registrarasistencia(
              sseccion = self.Asistencias.cbseccion.currentText(),
              nnombre = self.Asistencias.cbnombre.currentText(),
              aapellido = self.Asistencias.cbapellido.currentText(),
              mmotivo = self.Asistencias.cbmotivo.currentText(),
              ddescripcion = self.Asistencias.txtDes.toPlainText()
              )
            objData = AlumnoData()
            mbox = QMessageBox()
            re=objData.NIe(registraA)
            if re:
                nie_value = re[0][0]
                objData.RegistrarAsistencia(nie_value,registraA._mmotivo,registraA._descripcion)
                mbox.setText("Asistencias GUARDADO")
                generar_grafica() # Regenerar la gráfica después de guardar la asistencia
                self.limpiarAsistencias()
            else :
                mbox.setText("NO FUE POSIBLE GUARDAR EL Asistencias")
            mbox.exec() 


    def limpiarAsistencias(self):
        self.Asistencias.cbnombre.setCurrentIndex(0)
        self.Asistencias.cbapellido.setCurrentIndex(0)
        self.Asistencias.cbseccion.setCurrentIndex(0)
        self.Asistencias.cbmotivo.setCurrentIndex(0)

################# BUSCAR ###################

    def llenarcbseccionHistorial(self):
        objData = AlumnoData()
        datos = objData.listaA()
        self.Historial.cbBusSeccion.clear()
        for item in datos:
            self.Historial.cbBusSeccion.addItem(item[0])

    def Busqueda(self):
        busquedap = self.Historial.cbBus.currentText()
        mbox = QMessageBox()
        
        fecha1 = self.Historial.txtFechaDesde.date().toPyDate()
        fecha2 = self.Historial.txtFechaHasta.date().toPyDate()
        nie = self.Historial.txtBusNIE.text()
        nombre = self.Historial.txtBusNombre.text()
        apellido = self.Historial.txtBusApellido.text()
        seccion = self.Historial.cbBusSeccion.currentText()
        motivo = self.Historial.cbBusMotivo.currentText()

        objData = Historial()
        Buscar = None

        if busquedap == "NIE":
            if nie:
                Buscar = objData.BuscarPorNIE(nie)
            else:
                mbox.setText("INGRESE UN NIE PARA INICIAR LA BÚSQUEDA")
                mbox.exec()
                return
        elif busquedap == "Nombre completo":
            if nombre and apellido:
                Buscar = objData.BuscarPorNombre(nombre, apellido, seccion)
            else:
                mbox.setText("INGRESE NOMBRE Y APELLIDO PARA INICIAR LA BÚSQUEDA")
                mbox.exec()
                return
        elif busquedap == "Seccion":
            if seccion != " ":
                Buscar = objData.buscarporseccion(seccion)
            else:
                mbox.setText("SELECCIONE UNA SECCIÓN PARA INICIAR LA BÚSQUEDA")
                mbox.exec()
                return
        elif busquedap == "Rango de Fechas":
            if fecha1 and fecha2:
                Buscar = objData.BuscarPorFecha(fecha1, fecha2)
            else:
                mbox.setText("SELECCIONE UN RANGO DE FECHAS PARA INICIAR LA BÚSQUEDA")
                mbox.exec()
                return
        elif busquedap == "Motivo":
            if motivo != "Motivo":
                Buscar = objData.buscarpormotivo(motivo)
            else:
                mbox.setText("SELECCIONE UN MOTIVO PARA INICIAR LA BÚSQUEDA")
                mbox.exec()
                return
        elif busquedap == "Por todos los campos":
            if nie and nombre and apellido and seccion != " " and fecha1 and fecha2 and motivo != "Motivo":
                Buscar = objData.buscarportodosloscampos(nie, nombre, apellido, seccion, fecha1, fecha2, motivo)
            else:
                mbox.setText("DEBE LLENAR TODOS LOS CAMPOS PARA INICIAR LA BÚSQUEDA")
                mbox.exec()
                return
        else:
            mbox.setText("Seleccione un metodo de busqueda")
            mbox.exec()
            return

        if Buscar:
            self.Historial.tableHistorial.setRowCount(len(Buscar))
            fila = 0
            for item in Buscar:
                self.Historial.tableHistorial.setItem(fila, 0, QTableWidgetItem(str(item[0])))
                self.Historial.tableHistorial.setItem(fila, 1, QTableWidgetItem(str(item[2])))
                self.Historial.tableHistorial.setItem(fila, 2, QTableWidgetItem(str(item[3])))
                self.Historial.tableHistorial.setItem(fila, 3, QTableWidgetItem(str(item[1])))
                self.Historial.tableHistorial.setItem(fila, 4, QTableWidgetItem(str(item[4])))
                self.Historial.tableHistorial.setItem(fila, 5, QTableWidgetItem(str(item[5])))
                self.Historial.tableHistorial.setItem(fila, 6, QTableWidgetItem(str(item[6])))
                fila += 1
        else:
            mbox.setText("No se encontraron registros")
            mbox.exec()

    def abrir_visualizador_grafica(self):
        self.graph_viewer = GraphViewer()
        self.graph_viewer.show()