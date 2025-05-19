from codigo import Codigo
from PyQt6.QtWidgets import QInputDialog, QApplication ,QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem, QHeaderView 
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication, QLinearGradient, QColor, QBrush, QPalette
from PyQt6.QtCore import Qt, QSize
from datetime import datetime

class Ventana_compras(Codigo):
    def __init__(self, main_layout, botones, base_datos, id_usuario, nivel):
        super().__init__()
        self.layout = main_layout
        self.botones = botones
        self.base_datos = base_datos
        self.id_usuario = id_usuario
        self.carrito_ingreso = []
        self.fila_ingreso = 0
        self.total_compra = 0
        self.layout_extra: QVBoxLayout | None = None
        self.nivel = nivel

        

    def compras(self):
        self.limpieza_layout(self.layout)
        self.color_acceso_nivel(self.nivel, self.botones)
        self.color_boton_oprimido(self.botones[2])
        self.activar_botones(self.botones)
        self.botones[2].setEnabled(False)

        main_layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout2 = QHBoxLayout()

        self.layout3 = QHBoxLayout()
        self.layout3.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.boton_proveedores = QPushButton()
        self.boton_proveedores.setIcon(QIcon(self.imagen("imagenes/proveedores.png", 90, 90)))
        self.boton_proveedores.setIconSize(QSize(100, 100))
        self.color_boton_sin_oprimir(self.boton_proveedores)
        self.boton_proveedores.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_proveedores.clicked.connect(self.proveedores)

        self.boton_pedido = QPushButton()
        self.boton_pedido.setIcon(QIcon(self.imagen("imagenes/pedido.png", 90, 90)))
        self.boton_pedido.setIconSize(QSize(100, 100))
        self.color_boton_sin_oprimir(self.boton_pedido)
        self.boton_pedido.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_pedido.clicked.connect(self.ingreso_pedido)

        # Agregar botón para acceder a las ordenes de compra (para poder confirmarlas)
        self.boton_ordenes = QPushButton()
        self.boton_ordenes.setIcon(QIcon(self.imagen("imagenes/ordenes.png", 90, 90)))
        self.boton_ordenes.setIconSize(QSize(100, 100))
        self.color_boton_sin_oprimir(self.boton_ordenes)
        self.boton_ordenes.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_ordenes.clicked.connect(self.ordenes_compra)

        informar = QLabel("Oprima uno de los botones que tiene en la parte superior izquierda")
        informar.setStyleSheet("color: Black; font-size: 20px")
        informar.setAlignment(Qt.AlignmentFlag.AlignTop)
        informar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        layout1.addItem(self.espacio(35, 35))
        layout1.addWidget(self.boton_proveedores)
        layout1.addWidget(self.boton_pedido)
        layout1.addWidget(self.boton_ordenes)
        layout1.addStretch()
        
        self.layout3.addStretch()
        self.layout3.addWidget(informar)
        self.layout3.addStretch()

        layout2.addItem(self.espacio(35, 35))
        layout2.addLayout(self.layout3)

        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)

        self.layout.addLayout(main_layout)
    
    def proveedores(self):
        self.limpieza_layout(self.layout3)
        self.boton_proveedores.setEnabled(False)
        self.boton_pedido.setEnabled(True)
        self.boton_ordenes.setEnabled(True)

        layout_main = QVBoxLayout()
        layout_main.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)    

        layout1 = QHBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.layout4 = QHBoxLayout()

        self.boton_agregar = QPushButton()
        self.boton_agregar.setIcon(QIcon(self.imagen("imagenes/agregar.png", 45, 45)))
        self.boton_agregar.setIconSize(QSize(55, 55))
        self.color_boton_sin_oprimir(self.boton_agregar)
        self.boton_agregar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_agregar.clicked.connect(self.agregar_proveedor)

        self.boton_eliminar = QPushButton()
        self.boton_eliminar.setIcon(QIcon(self.imagen("imagenes/eliminar.png", 45, 45)))
        self.boton_eliminar.setIconSize(QSize(55, 55))
        self.color_boton_sin_oprimir(self.boton_eliminar)
        self.boton_eliminar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.boton_editar = QPushButton()
        self.boton_editar.setIcon(QIcon(self.imagen("imagenes/editar.png", 45, 45)))
        self.boton_editar.setIconSize(QSize(55, 55))
        self.color_boton_sin_oprimir(self.boton_editar)
        self.boton_editar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_editar.clicked.connect(self.editar_proveedor)

        self.boton_buscar = QPushButton()
        self.boton_buscar.setIcon(QIcon(self.imagen("imagenes/buscar.png", 45, 45)))
        self.boton_buscar.setIconSize(QSize(55, 55))
        self.color_boton_sin_oprimir(self.boton_buscar)
        self.boton_buscar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_busqueda = QLineEdit()
        self.ingreso_busqueda.setPlaceholderText("Ingrese el ID del proveedor")
        self.color_linea(self.ingreso_busqueda)
        self.ingreso_busqueda.setFixedSize(400, 60)
        self.ingreso_busqueda.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        #Tabla de proveedores
        #proveedores = [["1", "Francisco Queme", "Direccion X", "Ejemplo@gmail.com"]]
        proveedores = self.base_datos.obtener_proveedores()

        #tabla de proveedores
        self.tabla_proveedores = QTableWidget(len(proveedores), 5)

        self.tabla_proveedores.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla_proveedores.setHorizontalHeaderLabels(["ID", "Nombre", "Direccion", "Email", "Teléfono"]) 

        for fila, valor in enumerate(proveedores):
            # Convertir los valores a strings (excepto los que ya lo son)
            # Si la existencia es menor a la minima, cambiar el color de la celda

            
            id_proveedor = QTableWidgetItem(str(valor['id']))
            nombre_proveedor = QTableWidgetItem(valor['nombre'])
            direccion_proveedor = QTableWidgetItem(valor['direccion'])
            email_proveedor = QTableWidgetItem(valor['email'])  # Formato con 2 decimales
            telefono_proveedor = QTableWidgetItem(valor['telefono'])  # Formato con 2 decimales
            
            # Añadir items a la tabla
            self.tabla_proveedores.setItem(fila, 0, id_proveedor)
            self.tabla_proveedores.setItem(fila, 1, nombre_proveedor)
            self.tabla_proveedores.setItem(fila, 2, direccion_proveedor)
            self.tabla_proveedores.setItem(fila, 3, email_proveedor)
            self.tabla_proveedores.setItem(fila, 4, telefono_proveedor)
            
            # Configurar flags para todos los items
            for col in range(5):
                item = self.tabla_proveedores.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        
        self.tabla_proveedores.resizeColumnsToContents()
        self.color_tabla(self.tabla_proveedores)
        self.tabla_proveedores.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_proveedores.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout1.addWidget(self.boton_agregar)
        layout1.addWidget(self.boton_eliminar)
        layout1.addWidget(self.boton_editar)
        layout1.addWidget(self.boton_buscar)
        layout1.addWidget(self.ingreso_busqueda)

        self.layout4.addWidget(self.tabla_proveedores)

        layout_main.addLayout(layout1)
        layout_main.addLayout(self.layout4)

        self.layout3.addLayout(layout_main)
    
    def agregar_proveedor(self):
        # Cada que se complete una insercion o elemiminacion el Layout se tiene que volver a poner como none (esto no es definitivo)
        if self.layout_extra is not None:
            self.limpieza_layout(self.layout_extra)

        self.layout_extra = QVBoxLayout()
        self.layout_extra.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout1 = QGridLayout()
        layout2 = QHBoxLayout()
        layout2.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.boton_agregar.setEnabled(False)
        self.boton_eliminar.setEnabled(True)
        self.boton_editar.setEnabled(True)

        imagen_agregar = self.imagen("imagenes/agregar.png", 90, 90)
        agregar_label = QLabel()
        agregar_label.setPixmap(imagen_agregar)
        agregar_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        agregar_label.setScaledContents(True)

        self.ingreso_nombre = QLineEdit()
        self.color_linea(self.ingreso_nombre)
        self.ingreso_nombre.setFixedSize(200, 30)
        self.ingreso_nombre.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_direccion = QLineEdit()
        self.color_linea(self.ingreso_direccion)
        self.ingreso_direccion.setFixedSize(200, 30)
        self.ingreso_direccion.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_email = QLineEdit()
        self.color_linea(self.ingreso_email)
        self.ingreso_email.setFixedSize(200, 30)
        self.ingreso_email.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_telefono = QLineEdit()
        self.color_linea(self.ingreso_telefono)
        self.ingreso_telefono.setFixedSize(200, 30)
        self.ingreso_telefono.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_nombre = QLabel("Ingrese el nombre: ")
        label_nombre.setStyleSheet("color: Black")
        label_nombre.setFixedWidth(200)
        label_nombre.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_direccion = QLabel("Ingrese la dirección: ")
        label_direccion.setStyleSheet("color: Black")
        label_direccion.setFixedWidth(200)
        label_direccion.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_email = QLabel("Ingrese el email: ")
        label_email.setStyleSheet("color: Black")
        label_email.setFixedWidth(200)
        label_email.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_telefono = QLabel("Ingrese el teléfono: ")
        label_telefono.setStyleSheet("color: Black")
        label_telefono.setFixedWidth(200)
        label_telefono.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        boton_agregar = QPushButton("Agregar")
        self.color_boton_sin_oprimir(boton_agregar)
        boton_agregar.setFixedWidth(150)
        boton_agregar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_agregar.clicked.connect(self.agregar_proveedor_bd)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setFixedWidth(150)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        layout1.addWidget(label_nombre, 0, 0)
        layout1.addWidget(self.ingreso_nombre, 0, 1)
        layout1.addWidget(label_direccion, 1, 0)
        layout1.addWidget(self.ingreso_direccion, 1, 1)
        layout1.addWidget(label_email, 2, 0)
        layout1.addWidget(self.ingreso_email, 2, 1)
        layout1.addWidget(label_telefono, 3, 0)
        layout1.addWidget(self.ingreso_telefono, 3, 1)
        layout1.addWidget(boton_agregar, 4, 0)
        layout1.addWidget(boton_cancelar, 4, 1)

        layout2.addWidget(agregar_label)

        self.layout_extra.addLayout(layout2)
        self.layout_extra.addLayout(layout1)

        self.layout4.addLayout(self.layout_extra)


    def editar_proveedor(self):
        # Cada que se complete una insercion o elemiminacion el Layout se tiene que volver a poner como none (esto no es definitivo)
        if self.layout_extra is not None:
            self.limpieza_layout(self.layout_extra)
        
        self.tabla_proveedores.cellClicked.connect(self.llenar_campos)
        
        self.layout_extra = QVBoxLayout()
        self.layout_extra.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout1 = QGridLayout()
        layout2 = QHBoxLayout()
        layout2.setAlignment(Qt.AlignmentFlag.AlignCenter)   

        self.boton_agregar.setEnabled(True)
        self.boton_eliminar.setEnabled(True)
        self.boton_editar.setEnabled(False)

        imagen_agregar = self.imagen("imagenes/editar.png", 90, 90)
        agregar_label = QLabel()
        agregar_label.setPixmap(imagen_agregar)
        agregar_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        agregar_label.setScaledContents(True)

        self.ingreso_nombre = QLineEdit()
        self.color_linea(self.ingreso_nombre)
        self.ingreso_nombre.setFixedSize(200, 30)
        self.ingreso_nombre.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_direccion = QLineEdit()
        self.color_linea(self.ingreso_direccion)
        self.ingreso_direccion.setFixedSize(200, 30)
        self.ingreso_direccion.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_email = QLineEdit()
        self.color_linea(self.ingreso_email)
        self.ingreso_email.setFixedSize(200, 30)
        self.ingreso_email.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_telefono = QLineEdit()
        self.color_linea(self.ingreso_telefono)
        self.ingreso_telefono.setFixedSize(200, 30)
        self.ingreso_telefono.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)



        label_nombre = QLabel("Ingrese el nombre: ")
        label_nombre.setStyleSheet("color: Black")
        label_nombre.setFixedWidth(200)
        label_nombre.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_direccion = QLabel("Ingrese la dirección: ")
        label_direccion.setStyleSheet("color: Black")
        label_direccion.setFixedWidth(200)
        label_direccion.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_email = QLabel("Ingrese el email: ")
        label_email.setStyleSheet("color: Black")
        label_email.setFixedWidth(200)
        label_email.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_telefono = QLabel("Ingrese el teléfono: ")
        label_telefono.setStyleSheet("color: Black")
        label_telefono.setFixedWidth(200)
        label_telefono.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        boton_confirmar = QPushButton("Confirmar")
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setFixedWidth(150)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.editar_proveedor_bd)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setFixedWidth(150)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_cancelar.clicked.connect(self.cancelar_edicion)

        layout1.addWidget(label_nombre, 0, 0)
        layout1.addWidget(self.ingreso_nombre, 0, 1)
        layout1.addWidget(label_direccion, 1, 0)
        layout1.addWidget(self.ingreso_direccion, 1, 1)
        layout1.addWidget(label_email, 2, 0)
        layout1.addWidget(self.ingreso_email, 2, 1)
        layout1.addWidget(label_telefono, 3, 0)
        layout1.addWidget(self.ingreso_telefono, 3, 1)
        layout1.addWidget(boton_confirmar, 4, 0)
        layout1.addWidget(boton_cancelar, 4, 1)

        layout2.addWidget(agregar_label)

        self.layout_extra.addLayout(layout2)
        self.layout_extra.addLayout(layout1)

        self.layout4.addLayout(self.layout_extra)

    def agregar_proveedor_bd(self):
        nombre = self.ingreso_nombre.text()
        direccion = self.ingreso_direccion.text()
        email = self.ingreso_email.text()
        telefono = self.ingreso_telefono.text()

        if not nombre or not direccion or not email or not telefono:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos.")
            return

        try:
            self.base_datos.agregar_proveedor(nombre, direccion, email, telefono)
            self.mensaje_informacion("Proveedor agregado", "El proveedor ha sido agregado con éxito.")
            self.limpieza_layout(self.layout_extra)
            self.proveedores()
        except Exception as e:
            self.mensaje_error("Error al agregar el proveedor", str(e))

    def editar_proveedor_bd(self):
        nombre = self.ingreso_nombre.text()
        direccion = self.ingreso_direccion.text()
        email = self.ingreso_email.text()
        telefono = self.ingreso_telefono.text()

        if not nombre or not direccion or not email or not telefono:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos.")
            return

        try:
            id_proveedor = int(self.tabla_proveedores.item(self.tabla_proveedores.currentRow(), 0).text())
            self.base_datos.editar_proveedor(id_proveedor, nombre, direccion, email, telefono)
            self.mensaje_informacion("Proveedor editado", "El proveedor ha sido editado con éxito.")
            self.limpieza_layout(self.layout_extra)
            self.proveedores()
        except Exception as e:
            self.mensaje_error("Error al editar el proveedor", str(e))
    
    def cancelar_edicion(self):
        self.limpieza_layout(self.layout_extra)
        self.proveedores()
        self.boton_proveedores.setEnabled(False)
        self.boton_pedido.setEnabled(True)
        self.boton_ordenes.setEnabled(True)

    def llenar_campos(self):
        # Obtener la fila seleccionada
        fila = self.tabla_proveedores.currentRow()

        # Obtener los valores de la fila seleccionada
        nombre_proveedor = self.tabla_proveedores.item(fila, 1).text()
        direccion_proveedor = self.tabla_proveedores.item(fila, 2).text()
        email_proveedor = self.tabla_proveedores.item(fila, 3).text()
        telefono_proveedor = self.tabla_proveedores.item(fila, 4).text()

        # Llenar los campos de texto con los valores obtenidos
        self.ingreso_nombre.setText(nombre_proveedor)
        self.ingreso_direccion.setText(direccion_proveedor)
        self.ingreso_email.setText(email_proveedor)
        self.ingreso_telefono.setText(telefono_proveedor)

    def ingreso_pedido(self):
        self.total_compra = 0
        self.limpieza_layout(self.layout3)
        self.boton_proveedores.setEnabled(True)
        self.boton_ordenes.setEnabled(True)
        self.boton_pedido.setEnabled(False)

        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        layout_tabla1 = QVBoxLayout()

        layout_tabla2 = QVBoxLayout()

        #Tabla de compras  id, nombre, stock, precio, descripcion
        # compras = [["1", "Calculadora", 10, 150]]
        
        inventario = self.base_datos.obtener_productos_ventas()
        self.tabla_inventario = QTableWidget(len(inventario), 5)


        #Tabla de compras
        self.tabla_inventario.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla_inventario.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Existencia Actual", "Costo" ]) 

        # Llenar la tabla con los datos
        for fila, orden in enumerate(inventario):
            # Convertir los valores a strings (excepto los que ya lo son)
            id_item = QTableWidgetItem(str(orden['id']))
            nombre_item = QTableWidgetItem(orden['nombre'])
            descripcion_item = QTableWidgetItem(orden['descripcion'])
            stock_item = QTableWidgetItem(str(orden['stock']))
            precio_item = QTableWidgetItem(f"Q{(orden['precio'] - orden['precio']*0.15):.2f}")  # Formato con 2 decimales
            
            # Añadir items a la tabla
            self.tabla_inventario.setItem(fila, 0, id_item)
            self.tabla_inventario.setItem(fila, 1, nombre_item)
            self.tabla_inventario.setItem(fila, 2, descripcion_item)
            self.tabla_inventario.setItem(fila, 3, stock_item)
            self.tabla_inventario.setItem(fila, 4, precio_item)
            
            # Configurar flags para todos los items
            for col in range(5):
                item = self.tabla_inventario.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        self.tabla_inventario.resizeColumnsToContents()
        self.color_tabla(self.tabla_inventario)
        self.tabla_inventario.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_inventario.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tabla_inventario.cellDoubleClicked.connect(self.agregar_cantidad)

        self.boton_buscar = QPushButton()
        self.boton_buscar.setIcon(QIcon(self.imagen("imagenes/buscar.png", 45, 45)))
        self.boton_buscar.setIconSize(QSize(55, 55))
        self.color_boton_sin_oprimir(self.boton_buscar)
        self.boton_buscar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_busqueda = QLineEdit()
        self.ingreso_busqueda.setPlaceholderText("Ingrese el ID del orden")
        self.color_linea(self.ingreso_busqueda)
        self.ingreso_busqueda.setFixedHeight(60)
        self.ingreso_busqueda.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        #Tabla de Ingreso de nuevo orden
        # ingreso = [["1", "Calculadora", 10, 150]]

        self.tabla_ingreso = QTableWidget(0, 4)

        self.tabla_ingreso.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla_ingreso.setHorizontalHeaderLabels(["ID", "Nombre", "Cantidad", "Costo"]) 


        self.tabla_ingreso.resizeColumnsToContents()
        self.color_tabla(self.tabla_ingreso)
        self.tabla_ingreso.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_ingreso.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        ingreso_label = QLineEdit()
        ingreso_label.setPlaceholderText("Detalles del ingreso")
        self.color_linea(ingreso_label)
        ingreso_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ingreso_label.setFixedHeight(60)
        ingreso_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        ingreso_label.setEnabled(False)

        self.total = QLineEdit()
        self.total.setPlaceholderText(f"Total del ingreso: Q{self.total_compra:.2f}")
        self.color_linea(self.total)
        self.total.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total.setFixedHeight(50)
        self.total.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.total.setEnabled(False)

        boton_confirmar = QPushButton("Confirmar")
        boton_confirmar.setFixedHeight(50)
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.generar_orden_compra) # Generará una orden de compra


        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setFixedHeight(50)
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout1.addWidget(self.ingreso_busqueda)
        layout1.addWidget(self.boton_buscar)

        layout_tabla1.addLayout(layout1)
        layout_tabla1.addWidget(self.tabla_inventario)

        layout2.addWidget(boton_confirmar)
        layout2.addWidget(boton_cancelar)

        layout_tabla2.addWidget(ingreso_label)
        layout_tabla2.addWidget(self.tabla_ingreso)
        layout_tabla2.addWidget(self.total)
        layout_tabla2.addLayout(layout2)
        self.boton_eliminar_item = QPushButton("Eliminar orden seleccionada")
        self.color_boton_sin_oprimir(self.boton_eliminar_item)
        self.boton_eliminar_item.setFixedHeight(50)
        self.boton_eliminar_item.clicked.connect(self.eliminar_orden_ingreso)
        layout_tabla2.addWidget(self.boton_eliminar_item)


        self.layout3.addLayout(layout_tabla1)
        self.layout3.addLayout(layout_tabla2)


    # Función para generar una orden de compra y enviarla a la base de datos

    def generar_orden_compra(self):
        # Solicitar al usuario ingresar el ID del proveedor
        id_proveedor, ok = QInputDialog.getText(None, "ID Proveedor", "Ingrese el ID del proveedor:")
        if not ok or not id_proveedor.isdigit():
            self.mensaje_error("Error", "ID de proveedor inválido.")
            return
        id_proveedor = int(id_proveedor)
        if not self.carrito_ingreso:
            self.mensaje_error("Error", "No hay ordenes en el carrito.")
            return
        # Generar la orden de compra
        try:
            # en compra: id, Proveedor_id, fecha, Empleado_id, total_compra
            # en detalle_compra: orden_id, Compra_id, cantidad, precio_unitario
            id_compra = self.base_datos.agregar_compra(id_proveedor, datetime.now(), self.id_usuario, self.total_compra)
            for orden in self.carrito_ingreso:
                id_orden = orden[0]
                cantidad = orden[1]
                precio_unitario = orden[2]
                self.base_datos.agregar_detalle_compra(id_orden, id_compra, cantidad, precio_unitario, cantidad)
            # El stock del orden se actualizará hasta que se confirme el ingreso (estado pase a 1)
            self.mensaje_informacion("Orden de compra generada", "La orden de compra se ha generado correctamente.")
            # Limpiar la tabla de ingreso
            self.tabla_ingreso.clearContents()
            self.tabla_ingreso.setRowCount(0)
            self.tabla_ingreso.setColumnCount(4)
            self.total.clear()
            self.total.setPlaceholderText("Total del ingreso: Q0")
            self.carrito_ingreso.clear()
            self.total_compra = 0
            self.fila_ingreso = 0


        except Exception as e:
            self.mensaje_error("Error", f"No se pudo generar la orden de compra: {str(e)}")
            return



    def agregar_cantidad(self):
        # Esta función se llamará cuando se haga doble clic en una celda de la tabla de inventario
        self.ventana_cantidad = QWidget()
        self.fondo_degradado(self.ventana_cantidad, "#5DA9F5", "#0037FF")
        self.ventana_cantidad.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        main_layout = QGridLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout1 = QHBoxLayout()
        # Agregar etiqueta de "Ingrese la cantidad"
        label_cantidad = QLabel("Ingrese la cantidad:")
        label_cantidad.setStyleSheet("color: Black")
            
        self.cantidad = QLineEdit()
        self.cantidad.setPlaceholderText("Ingrese la cantidad")
        self.color_linea(self.cantidad)
        self.cantidad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cantidad.setFixedHeight(30)
        self.cantidad.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        boton_confirmar = QPushButton("Confirmar")
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setFixedSize(100, 20)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.confirmar_cantidad_ingreso)
        self.asignacion_tecla(self.ventana_cantidad, "Return", boton_confirmar)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setFixedSize(100, 20)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.asignacion_tecla(self.ventana_cantidad, "Esc", boton_cancelar)
        boton_cancelar.clicked.connect(self.cancelar_cantidad_ingreso)

        layout1.addWidget(boton_confirmar)
        layout1.addWidget(boton_cancelar)

        # Agregar la etiqueta y el campo de texto al layout principal
        main_layout.addWidget(label_cantidad, 0, 0)   
        main_layout.addWidget(self.cantidad, 1, 0)
        main_layout.addLayout(layout1, 2, 0)

        self.ventana_cantidad.setLayout(main_layout)
        self.ventana_cantidad.showNormal()

    def confirmar_cantidad_ingreso(self):
        try:
            # Obtener fila seleccionada y cantidad
            fila = self.tabla_inventario.currentRow()
            cantidad_texto = self.cantidad.text()
            
            # Validar cantidad
            if not cantidad_texto.isdigit() or int(cantidad_texto) <= 0:
                self.mensaje_error("Error", "Ingrese una cantidad válida (número mayor que 0).")
                return

            cantidad = int(cantidad_texto)

            # Obtener datos del producto
            id_producto = int(self.tabla_inventario.item(fila, 0).text())
            nombre_producto = self.tabla_inventario.item(fila, 1).text()
            precio_texto = self.tabla_inventario.item(fila, 4).text()[1:]  # Eliminar 'Q'
            precio_producto = float(precio_texto)
            total_producto = cantidad * precio_producto

            # Verificar si el producto ya está en el carrito
            for i in range(self.tabla_ingreso.rowCount()):
                if int(self.tabla_ingreso.item(i, 0).text()) == id_producto:
                    # Actualizar cantidad existente
                    cantidad_actual = int(self.tabla_ingreso.item(i, 2).text())
                    self.tabla_ingreso.item(i, 2).setText(str(cantidad_actual + cantidad))
                    self.total_compra += total_producto
                    self.total.setPlaceholderText(f"Total del ingreso: Q{self.total_compra:.2f}")
                    self.ventana_cantidad.close()
                    return

            # Si no existe, agregar nueva fila
            fila_nueva = self.tabla_ingreso.rowCount()
            self.tabla_ingreso.insertRow(fila_nueva)

            # Crear items para cada columna
            items = [
                QTableWidgetItem(str(id_producto)),
                QTableWidgetItem(nombre_producto),
                QTableWidgetItem(str(cantidad)),
                QTableWidgetItem(f"Q{precio_producto:.2f}")
            ]

            # Configurar items y añadirlos a la tabla
            for col, item in enumerate(items):
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                self.tabla_ingreso.setItem(fila_nueva, col, item)

            # Actualizar variables de estado
            self.carrito_ingreso.append([id_producto, cantidad, precio_producto])
            self.total_compra += total_producto
            self.total.setPlaceholderText(f"Total del ingreso: Q{self.total_compra:.2f}")
            self.ventana_cantidad.close()

        except Exception as e:
            self.mensaje_error("Error", f"Ocurrió un error al agregar el producto: {str(e)}")

    def cancelar_cantidad_ingreso(self):
        self.ventana_cantidad.close()
        self.cantidad.clear()
        self.cantidad.setPlaceholderText("Ingrese la cantidad")


    # Esta tabla servirá para ver las ordenes de compra, y los detalles de cada una. Servirá para confirmar el ingreso
    def ordenes_compra(self): 
        self.limpieza_layout(self.layout3)
        self.boton_proveedores.setEnabled(True)
        self.boton_pedido.setEnabled(True)
        self.boton_ordenes.setEnabled(False)
        self.total_compra = 0

        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        layout_tabla1 = QVBoxLayout()
        layout_tabla2 = QVBoxLayout()

        # Tabla de compras  id, nombre, stock, precio, descripcion
        # compras = [["1", "Calculadora", 10, 150]]
        
        compras = self.base_datos.obtener_compras_pendientes() # Retorna IdCompra, Proveedor, Fecha, Total
        self.tabla_compras = QTableWidget(len(compras), 4)

        self.carrito_ingreso = []

        #Tabla de compras
        self.tabla_compras.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla_compras.setHorizontalHeaderLabels(["IdCompra", "Proveedor", "Fecha", "Total"]) 

        

        # Llenar la tabla con los datos
        for fila, orden in enumerate(compras):
            # Convertir los valores a strings (excepto los que ya lo son)
            id_item = QTableWidgetItem(str(orden['IdCompra']))
            nombre_item = QTableWidgetItem(orden['Proveedor'])
            fecha_item = QTableWidgetItem(str(orden['Fecha']))
            # Convertir el total a string con formato de moneda
            total_item = QTableWidgetItem(f"Q{orden['Total']:.2f}")  # Formato con 2 decimales
            
            # Añadir items a la tabla
            self.tabla_compras.setItem(fila, 0, id_item)
            self.tabla_compras.setItem(fila, 1, nombre_item)
            self.tabla_compras.setItem(fila, 2, fecha_item)
            self.tabla_compras.setItem(fila, 3, total_item)
            
            # Configurar flags para todos los items
            for col in range(4):
                item = self.tabla_compras.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        self.tabla_compras.resizeColumnsToContents()
        self.color_tabla(self.tabla_compras)
        self.tabla_compras.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_compras.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tabla_compras.cellDoubleClicked.connect(self.ver_detalles_de_orden)

        self.boton_buscar = QPushButton()
        self.boton_buscar.setIcon(QIcon(self.imagen("imagenes/buscar.png", 45, 45)))
        self.boton_buscar.setIconSize(QSize(55, 55))
        self.color_boton_sin_oprimir(self.boton_buscar)
        self.boton_buscar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_busqueda = QLineEdit()
        self.ingreso_busqueda.setPlaceholderText("Ingrese el ID del orden")
        self.color_linea(self.ingreso_busqueda)
        self.ingreso_busqueda.setFixedHeight(60)
        self.ingreso_busqueda.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        #Tabla de Ingreso de nuevo orden
        # ingreso = [["1", "Calculadora", 10, 150]]

        self.tabla_ingreso = QTableWidget(0, 5)

        self.tabla_ingreso.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # Se debe devolver IdProducto, NombreProducto, PrecioUnitario, Cantidad

        self.tabla_ingreso.setHorizontalHeaderLabels(["ID","IdProducto", "Producto", "Precio Unitario", "Cantidad", "Cantidad Recibida"]) 


        self.tabla_ingreso.resizeColumnsToContents()
        self.color_tabla(self.tabla_ingreso)
        self.tabla_ingreso.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_ingreso.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        ingreso_label = QLineEdit()
        ingreso_label.setPlaceholderText("Detalles de orden")
        self.color_linea(ingreso_label)
        ingreso_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ingreso_label.setFixedHeight(60)
        ingreso_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        ingreso_label.setEnabled(False)

        self.total = QLineEdit()
        self.total.setPlaceholderText(f"Total del ingreso: Q{self.total_compra:.2f}")
        self.color_linea(self.total)
        self.total.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total.setFixedHeight(50)
        self.total.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.total.setEnabled(False)

        boton_confirmar = QPushButton("Confirmar")
        boton_confirmar.setFixedHeight(50)
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.confirmar_ingreso) # Validará la orden de compra


        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setFixedHeight(50)
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout1.addWidget(self.ingreso_busqueda)
        layout1.addWidget(self.boton_buscar)

        layout_tabla1.addLayout(layout1)
        layout_tabla1.addWidget(self.tabla_compras)

        layout2.addWidget(boton_confirmar)
        layout2.addWidget(boton_cancelar)

        layout_tabla2.addWidget(ingreso_label)
        layout_tabla2.addWidget(self.tabla_ingreso)
        layout_tabla2.addWidget(self.total)
        layout_tabla2.addLayout(layout2)
        self.boton_eliminar_item = QPushButton("Eliminar orden seleccionado")
        self.color_boton_sin_oprimir(self.boton_eliminar_item)
        self.boton_eliminar_item.setFixedHeight(50)
        self.boton_eliminar_item.clicked.connect(self.eliminar_orden_ingreso)
        layout_tabla2.addWidget(self.boton_eliminar_item)


        self.layout3.addLayout(layout_tabla1)
        self.layout3.addLayout(layout_tabla2)

    def ver_detalles_de_orden(self):
        self.fila_ingreso = 0
        self.total_compra = 0
        fila = self.tabla_compras.currentRow()
        id_orden = int(self.tabla_compras.item(fila, 0).text())
        detalles = self.base_datos.obtener_detalle_compra(id_orden)
        
        # Configurar tabla
        self.tabla_ingreso.clear()
        self.tabla_ingreso.setRowCount(0)
        self.tabla_ingreso.setColumnCount(6)
        self.tabla_ingreso.setHorizontalHeaderLabels([
            "ID", "IdProducto", "Producto", 
            "Precio Unitario", "Cantidad", "Cantidad Recibida"
        ])
        
        # Habilitar edición para la tabla
        self.tabla_ingreso.setEditTriggers(
            QTableWidget.EditTrigger.DoubleClicked | 
            QTableWidget.EditTrigger.EditKeyPressed
        )
        
        for detalle in detalles:
            row = self.tabla_ingreso.rowCount()
            self.tabla_ingreso.insertRow(row)
            
            # Crear items para columnas no editables
            for col, value in enumerate([
                str(detalle['ID']),
                str(detalle['IdProducto']),
                detalle['NombreProducto'],
                f"Q{detalle['PrecioUnitario']:.2f}",
                str(detalle['Cantidad'])
            ]):
                item = QTableWidgetItem(value)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                self.tabla_ingreso.setItem(row, col, item)
            
            # Item editable para Cantidad Recibida (columna 5)
            item_recibida = QTableWidgetItem(str(detalle['CantidadRecibida']))
            item_recibida.setFlags(
                Qt.ItemFlag.ItemIsEnabled | 
                Qt.ItemFlag.ItemIsSelectable | 
                Qt.ItemFlag.ItemIsEditable
            )
            self.tabla_ingreso.setItem(row, 5, item_recibida)
            
            self.total_compra += detalle['PrecioUnitario'] * detalle['Cantidad']
            self.fila_ingreso += 1
        
        self.total.setPlaceholderText(f"Total del ingreso: Q{self.total_compra:.2f}")
        
        # Asegurar que las columnas se muestren correctamente
        self.tabla_ingreso.resizeColumnsToContents()



    def confirmar_ingreso(self):  
        try:
            # Recorrer la tabla_ingreso para obtener detalles del carrito
            # y actualizar el stock de cada orden
            fila = self.tabla_compras.currentRow()
            id_orden = int(self.tabla_compras.item(fila, 0).text())

            for i in range(self.tabla_ingreso.rowCount()):
                # Verificar que la cantidad sea igual a la cantidad recibida
                id_detalle = int(self.tabla_ingreso.item(i, 0).text())
                id_producto = int(self.tabla_ingreso.item(i, 1).text())
                precio_unitario = float(self.tabla_ingreso.item(i, 3).text()[1:])
                cantidad = int(self.tabla_ingreso.item(i, 4).text())
                cantidad_recibida = int(self.tabla_ingreso.item(i, 5).text())

                if cantidad_recibida != cantidad:
                    # Modificar el detalle de la orden en bd
                    cantidad = cantidad_recibida
                    self.base_datos.modificar_detalle_compra(id_detalle, cantidad)


                # Agregar al carrito de ingreso
                self.carrito_ingreso.append([id_producto, cantidad, precio_unitario, id_detalle])

            for producto in self.carrito_ingreso:
                id_producto = producto[0]
                cantidad = producto[1]
                # Actualizar el stock del producto

                self.base_datos.aumentar_stock_producto(id_producto, cantidad)
            # Cambiar el estado de la orden a 1 (confirmada)
            self.base_datos.confirmar_orden_compra(id_orden)

            self.mensaje_informacion("Ingreso confirmado", "El ingreso se ha registrado correctamente.")
            # Recargar la tabla de compras
            self.ordenes_compra()
            # Limpiar la tabla de ingreso
            self.tabla_ingreso.clearContents()
            self.tabla_ingreso.setRowCount(0)
            self.tabla_ingreso.setColumnCount(4)
            self.total.clear()
            self.total.setPlaceholderText("Total del ingreso: Q0")
            self.carrito_ingreso.clear()
            self.total_compra = 0
            self.fila_ingreso = 0

        except Exception as e:
            self.mensaje_error("Error", f"No se pudo registrar el ingreso: {str(e)}")

    def eliminar_orden_ingreso(self):
        fila = self.tabla_ingreso.currentRow()
        if fila == -1:
            self.mensaje_error("Error", "Seleccione un orden para eliminar.")
            return

        subtotal = float(self.tabla_ingreso.item(fila, 3).text()[1:]) * int(self.tabla_ingreso.item(fila, 2).text())
        self.total_compra -= subtotal
        self.total.setPlaceholderText(f"Total del ingreso: Q{self.total_compra:.2f}")

        id_a_eliminar = int(self.tabla_ingreso.item(fila, 0).text())
        self.carrito_ingreso = [item for item in self.carrito_ingreso if item[0] != id_a_eliminar]

        self.tabla_ingreso.removeRow(fila)
        self.fila_ingreso -= 1

    def cancelar_ingreso(self):
        self.tabla_ingreso.clearContents()
        self.tabla_ingreso.setRowCount(0)
        self.tabla_ingreso.setColumnCount(4)
        self.total.clear()
        self.total.setPlaceholderText("Total del ingreso: Q0")
        self.carrito_ingreso.clear()
        self.total_compra = 0
        self.fila_ingreso = 0

