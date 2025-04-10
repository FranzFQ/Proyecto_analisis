from codigo import Codigo
from PyQt6.QtWidgets import QApplication ,QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem, QHeaderView 
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication, QLinearGradient, QColor, QBrush, QPalette
from PyQt6.QtCore import Qt, QSize

class Ventana_ventas(Codigo):
    def __init__(self, main_layout, botones, base_datos):
        super().__init__()
        self.layout2 = main_layout
        self.botones = botones
        self.base_datos = base_datos

    def ventas(self):
        self.limpieza_layout(self.layout2)
        self.recoloreas_botones(self.botones)
        self.color_boton_oprimido(self.botones[1])
        self.activar_botones(self.botones)
        self.botones[1].setEnabled(False)
        
        main_layout = QHBoxLayout()
        layout1 = QGridLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout2 = QGridLayout()
        layout2.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)

        boton_buscar = QPushButton()
        boton_buscar.setIcon(QIcon(self.imagen("imagenes/buscar.png", 50, 50)))
        boton_buscar.setIconSize(QSize(62, 62))
        self.color_boton_sin_oprimir(boton_buscar)
        boton_buscar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_busqueda_ventas = QLineEdit()
        self.color_linea(self.ingreso_busqueda_ventas)
        self.ingreso_busqueda_ventas.setPlaceholderText("Ingrese el nombre del producto...")
        self.ingreso_busqueda_ventas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ingreso_busqueda_ventas.setFixedSize(300, 70)
        self.ingreso_busqueda_ventas.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        inventario = self.base_datos.obtener_productos()
        for i in range(len(inventario)):
            inventario[i] = list(map(str, inventario[i]))

        self.tabla_ventas = QTableWidget(len(inventario), len(inventario[0]))

        self.fila = len(inventario)
        self.columna = len(inventario[0])
        self.items = []

        self.tabla_ventas.setHorizontalHeaderLabels(["ID", "Nombre", "Existencias", "Precio", "Descripcion"])

        for fila in range(self.fila):
            for columna in range(self.columna):
                self.tabla_ventas.setItem(fila, columna, QTableWidgetItem(inventario[fila][columna]))
                item = self.tabla_ventas.item(fila, columna)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        self.color_tabla(self.tabla_ventas)
        self.tabla_ventas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_ventas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        carrito_prueba = [["Algo", "10", "40Q"]]
        self.tabla_carrito = QTableWidget(len(carrito_prueba), len(carrito_prueba[0]))
        fila = len(carrito_prueba)
        columna = len(carrito_prueba[0])
        items = []

        self.tabla_carrito.setHorizontalHeaderLabels(["Nombre", "Cantidad", "Precio"])

        for fila in range(fila):
            for columna in range(columna):
                self.tabla_carrito.setItem(fila, columna, QTableWidgetItem(inventario[fila][columna]))
                item = self.tabla_carrito.item(fila, columna)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        self.color_tabla(self.tabla_carrito)
        self.tabla_carrito.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_carrito.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        carrito = QLineEdit()
        self.color_linea(carrito)
        carrito.setPlaceholderText("Carrito")
        carrito.setAlignment(Qt.AlignmentFlag.AlignCenter)
        carrito.setFixedSize(400, 70)
        carrito.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        carrito.setEnabled(False)
        
        self.total = QLineEdit()
        self.color_linea(self.total)
        self.total.setPlaceholderText("Total de venta")
        self.total.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total.setFixedSize(400, 70)
        self.total.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.total.setEnabled(False)

        self.boton_confirmar_venta = QPushButton("Confirmar")
        self.boton_confirmar_venta.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_boton_sin_oprimir(self.boton_confirmar_venta)
        self.boton_confirmar_venta.clicked.connect(self.editar_producto)

        self.boton_cancelar_venta = QPushButton("Confirmar")
        self.boton_cancelar_venta.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_boton_sin_oprimir(self.boton_cancelar_venta)
        self.boton_cancelar_venta.clicked.connect(self.editar_producto)

        layout2.addWidget(self.total, 0, 0)
        layout2.addWidget(self.boton_confirmar_venta, 1, 0)
        layout2.addWidget(self.boton_cancelar_venta, 1, 1)

        layout1.addItem(self.espacio(60, 60), 0, 0, 3, 0)
        layout1.addWidget(self.ingreso_busqueda_ventas, 0, 1)
        layout1.addWidget(boton_buscar, 0, 2)
        layout1.addWidget(self.tabla_ventas, 1, 0, 1, 5)

        layout1.addItem(self.espacio(60, 10), 0, 6, 2, 6)
        layout1.addWidget(carrito, 0, 7)
        layout1.addItem(self.espacio(100, 10), 0, 7, 1, 10)
        layout1.addWidget(self.tabla_carrito, 1, 7, 1, 10)

        layout1.addItem(self.espacio(100, 10), 3, 0, 3, 5)
        layout1.addLayout(layout2, 3, 7)

        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        main_layout.addItem(self.espacio(250, 10))

        self.layout2.addLayout(main_layout)