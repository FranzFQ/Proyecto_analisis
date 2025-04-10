import sys
from codigo import Codigo
from ventana_usuarios import Ventana_usuarios
from ventana_ventas import Ventana_ventas
from ventana_compras import Ventana_compras
from ventana_inventario import Ventana_inventario
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

class Ventana_principal(Codigo):
    def __init__(self, ventanas, Linea1, Linea2, base_datos):
        super().__init__()
        self.ventanas = ventanas
        self.base_datos = base_datos
        self.line1 = Linea1
        self.line2 = Linea2
        self.botones: list[QPushButton] = []

    def principal(self):
        self.window2 = QWidget()
        self.window2.setWindowIcon(QIcon("imagenes/logo.ico"))
        self.fondo_degradado(self.window2, "#0037FF", "#5DA9F5")
        self.window2.setWindowTitle("Bienvenido usuario: " + "admin")

        main_layout = QHBoxLayout()
        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.layout2 = QVBoxLayout()
        self.layout2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        sub_layout2 = QHBoxLayout()
        
        self.boton_inicio = QPushButton()
        self.boton_inicio.setIcon(QIcon(self.imagen("imagenes/inicio.png", 80, 80)))
        self.boton_inicio.setIconSize(QSize(150, 100))
        self.color_boton_sin_oprimir(self.boton_inicio)
        self.boton_inicio.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_inicio.clicked.connect(self.regreso)

        self.boton_usuario = QPushButton()
        self.boton_usuario.setIcon(QIcon(self.imagen("imagenes/usuarios.png", 100, 100)))
        self.boton_usuario.setIconSize(QSize(150, 150))
        self.color_boton_sin_oprimir(self.boton_usuario)
        self.boton_usuario.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_usuario.clicked.connect(self.ventana_usuarios)

        self.boton_ventas = QPushButton()
        self.boton_ventas.setIcon(QIcon(self.imagen("imagenes/ventas.png", 100, 100)))
        self.boton_ventas.setIconSize(QSize(150, 150))
        self.color_boton_sin_oprimir(self.boton_ventas)
        self.boton_ventas.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_ventas.clicked.connect(self.ventana_ventas)

        self.boton_compras = QPushButton()
        self.boton_compras.setIcon(QIcon(self.imagen("imagenes/compras.png", 100, 100)))
        self.boton_compras.setIconSize(QSize(150, 150))
        self.color_boton_sin_oprimir(self.boton_compras)
        self.boton_compras.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_compras.clicked.connect(self.ventana_compras)

        self.boton_inventario = QPushButton()
        self.boton_inventario.setIcon(QIcon(self.imagen("imagenes/inventario.png", 100, 100)))
        self.boton_inventario.setIconSize(QSize(150, 150))
        self.color_boton_sin_oprimir(self.boton_inventario)
        self.boton_inventario.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_inventario.clicked.connect(self.ventana_inventario)

        self.logo = QLabel()
        self.logo.setPixmap(self.imagen("imagenes/logo_libreria.png", 400, 400))
        self.logo.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        if len (self.botones) == 0:
            self.botones.append(self.boton_usuario)
            self.botones.append(self.boton_ventas)
            self.botones.append(self.boton_compras)
            self.botones.append(self.boton_inventario)
        else:
            pass

        sub_layout2.addWidget(self.logo)

        self.layout2.addLayout(sub_layout2)

        layout1.addWidget(self.boton_inicio)
        layout1.addItem(self.espacio(10, 10))
        layout1.addWidget(self.boton_usuario)
        layout1.addItem(self.espacio(10, 10))
        layout1.addWidget(self.boton_ventas)
        layout1.addItem(self.espacio(10, 10))
        layout1.addWidget(self.boton_compras)
        layout1.addItem(self.espacio(10, 10))
        layout1.addWidget(self.boton_inventario)
        
        main_layout.addLayout(layout1)
        main_layout.addLayout(self.layout2)
        self.window2.setLayout(main_layout)
        self.ventanas[1] = self.window2
        self.ventana_maxima(self.window2)

    def ventana_usuarios(self):
        self.usu = Ventana_usuarios(self.layout2, self.botones, self.base_datos)
        self.usu.usuario()

    def ventana_ventas(self):
        self.ven = Ventana_ventas(self.layout2, self.botones, self.base_datos)
        self.ven.ventas()

    def ventana_compras(self):
        self.com = Ventana_compras(self.layout2, self.botones, self.base_datos)
        self.com.compras()

    def ventana_inventario(self):
        self.inv = Ventana_inventario(self.layout2, self.botones, self.base_datos)
        self.inv.inventario()

    def regreso(self):
        aviso = QMessageBox()
        aviso.setStyleSheet("QMessageBox { color: black; background-color: #36dfea;} QPushButton {color: black; background-color: #22a4ac;} QLabel{color: black;}")
        aviso.setWindowIcon(QIcon("imagenes/infomation.ico"))
        aviso.setWindowTitle("¿Cerrar sesion?")
        aviso.setText("Seguro que quiere cerrar la sesion actual")
        aviso.setIcon(QMessageBox.Icon.Information)
        aviso.addButton("Si", QMessageBox.ButtonRole.YesRole)
        aviso.addButton("No", QMessageBox.ButtonRole.NoRole)
        respuesta = aviso.exec()
        if respuesta == 2:
            sub_layout2 = QHBoxLayout()
            self.limpieza_layout(self.layout2)
            sub_layout2.addWidget(self.logo)
            self.layout2.addLayout(sub_layout2)
            self.activar_botones(self.botones)
            self.recoloreas_botones(self.botones)
            self.window2.close()
            self.line1.clear()
            self.line2.clear()
            self.ventanas[0].showNormal()
            self.mensaje_informacion("Sesion cerrada", "La sesion se ha cerrado correctamente")
        
        elif respuesta == 3:
            self.mensaje_informacion("Cierre de sesion cancelada", "La sesion se a cancelado correctamente")