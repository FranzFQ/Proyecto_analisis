from codigo import Codigo
from PyQt6.QtWidgets import QApplication ,QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem, QHeaderView 
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication, QLinearGradient, QColor, QBrush, QPalette
from PyQt6.QtCore import Qt, QSize

class Ventana_usuarios(Codigo):
    def __init__(self, main_layout, botones, base_datos):
        super().__init__()
        self.layout2 = main_layout
        self.botones = botones
        self.base_datos = base_datos

    def usuario(self):
        self.limpieza_layout(self.layout2)
        self.recoloreas_botones()
        self.color_boton_oprimido(self.boton_usuario)
        self.activar_botones()
        self.boton_usuario.setEnabled(False)
