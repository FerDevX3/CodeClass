from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, Qt
from graficas import generar_grafica

class GraphViewer(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("gui/graph_viewer.ui", self)
        self.initUI()

    def initUI(self):
        self.lblGraphDisplay = self.ui.lblGraphDisplay
        self.update_graph()

        # Configurar el temporizador para actualizar la gráfica cada 5 segundos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(5000) # 5000 ms = 5 segundos

    def update_graph(self):
        generar_grafica()
        pixmap = QPixmap('grafica_asistencia.png')
        # Escalar la imagen para que se ajuste al QLabel
        scaled_pixmap = pixmap.scaled(self.lblGraphDisplay.size(), 
                                     aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, 
                                     transformMode=Qt.TransformationMode.SmoothTransformation)
        self.lblGraphDisplay.setPixmap(scaled_pixmap)
