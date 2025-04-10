import sys
from PyQt6.QtWidgets import QApplication ,QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem, QHeaderView 
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication, QLinearGradient, QColor, QBrush, QPalette
from PyQt6.QtCore import Qt, QSize

class Codigo:
    def __init__(self):    
        self.app = QApplication(sys.argv)
        self.ventanas: list[QWidget] |  None = [None, None]

# Funciones para optimizar el codigo
    def fondo_degradado(self, window: QWidget, color1, color2):
        gradiente = QLinearGradient(0, 0, window.width(), window.height())
        color1 = self.conversion_color(color1)
        color2 = self.conversion_color(color2)
        gradiente.setColorAt(0.0, QColor(color1[0], color1[1], color1[2]))
        gradiente.setColorAt(1.0, QColor(color2[0], color2[1], color2[2]))

        pincel = QBrush(gradiente)

        paleta = window.palette()
        paleta.setBrush(QPalette.ColorRole.Window, pincel)
        window.setPalette(paleta)

    def conversion_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def limpieza_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                sub_layout = item.layout()
                if sub_layout is not None:
                    self.limpieza_layout(sub_layout)
    
    def mensaje_error(self, titulo, mensaje):
        mesaje_error = QMessageBox()
        mesaje_error.setIcon(QMessageBox.Icon.Warning)
        mesaje_error.setStyleSheet("QMessageBox { color: black; background-color: #e15f5f;} QPushButton {color: black; background-color: #ff0000;} QLabel{color: black;}")
        mesaje_error.setWindowIcon(QIcon("imagenes/warning.ico")) 
        mesaje_error.setWindowTitle(titulo)
        mesaje_error.setText(mensaje)
        mesaje_error.setDefaultButton(QMessageBox.StandardButton.Ok)
        mesaje_error.exec()

    def mensaje_informacion(self, titulo, mensaje):
        mensaje_informacion = QMessageBox()
        mensaje_informacion.setStyleSheet("QMessageBox { color: black; background-color: #36dfea;} QPushButton {color: black; background-color: #22a4ac;} QLabel{color: black;}")
        mensaje_informacion.setWindowIcon(QIcon("imagenes/infomation.ico"))
        mensaje_informacion.setWindowTitle(titulo)
        mensaje_informacion.setText(mensaje)
        mensaje_informacion.setIcon(QMessageBox.Icon.Information)
        mensaje_informacion.setDefaultButton(QMessageBox.StandardButton.Ok) 
        mensaje_informacion.exec()

    def color_boton_sin_oprimir(self, boton: QPushButton):
        boton.setStyleSheet("QPushButton {background-color: white; border: 3px solid black; color: black} QPushButton:hover {background-color: #38B3F5;} QPushButton:pressed {background-color: #2268F5;}")

    def color_boton_oprimido(self, boton: QPushButton):
        boton.setStyleSheet("QPushButton {background-color: #00CAE0; border: 3px solid black;} QPushButton:hover {background-color: #38B3F5;} QPushButton:pressed {background-color: #2268F5;}")

    def imagen(self, ruta, ancho, alto):
        imagen = QPixmap(ruta)
        imagen = imagen.scaled(ancho, alto, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        return imagen

    def activar_botones(self, botones: list[QPushButton]):
        botones[0].setEnabled(True)
        botones[1].setEnabled(True)
        botones[2].setEnabled(True)
        botones[3].setEnabled(True)

    def recoloreas_botones(self, botones: list[QPushButton]):
        self.color_boton_sin_oprimir(botones[0])
        self.color_boton_sin_oprimir(botones[1])
        self.color_boton_sin_oprimir(botones[2])
        self.color_boton_sin_oprimir(botones[3])

    def color_tabla(self, tabla):
        tabla.setStyleSheet("QTableWidget {background-color: white; border: 5px solid black;} QTableWidget::item {background-color: 00f4ff; color: black;} QTableWidget::item:selected {background-color: #1fdde5; color: black;} QTableWidget::item:hover {background-color: #4cd9df; color: black;} QHeaderView::section {background-color: #94fbff; color: black;}")

    def ventana_maxima(self, window: QWidget):
        window.showFullScreen()
        pantalla = QGuiApplication.primaryScreen() 
        screen_rect = pantalla.availableGeometry()
        window.setGeometry(screen_rect)
    
    def espacio(self, x: int, y: int):
        return QSpacerItem(x, y, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    
    def color_linea(self, linea: QLineEdit):
        linea.setStyleSheet("Color: black; background-color: white; border: 3px solid black;")
