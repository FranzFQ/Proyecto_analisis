from codigo import Codigo
from PyQt6.QtWidgets import QApplication ,QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem, QHeaderView 
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication, QLinearGradient, QColor, QBrush, QPalette
from PyQt6.QtCore import Qt, QSize

class Ventana_inventario(Codigo):
    def __init__(self, main_layout, botones, base_datos, nivel):
        super().__init__()
        self.layout = main_layout
        self.botones = botones
        self.base_datos = base_datos
        self.nivel = nivel

    def inventario(self):
        self.limpieza_layout(self.layout)
        self.color_acceso_nivel(self.nivel, self.botones)
        self.color_boton_oprimido(self.botones[3])
        self.activar_botones(self.botones)
        self.botones[3].setEnabled(False)
        
        self.main_layout_ventana_inventario = QHBoxLayout()

        sub_layout = QVBoxLayout()

        layout3 = QHBoxLayout()
        layout3.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        layout4 = QHBoxLayout()
        layout4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.boton_cancelar_venta = QPushButton()
        self.boton_cancelar_venta.setIcon(QIcon(self.imagen("imagenes/editar.png", 50, 50)))
        self.boton_cancelar_venta.setIconSize(QSize(70, 70))
        self.boton_cancelar_venta.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_boton_sin_oprimir(self.boton_cancelar_venta)
        self.boton_cancelar_venta.clicked.connect(self.editar_producto)

        self.boton_eliminar = QPushButton()
        self.boton_eliminar.setIcon(QIcon(self.imagen("imagenes/eliminar.png", 50, 50)))
        self.boton_eliminar.setIconSize(QSize(70, 70))
        self.boton_eliminar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_boton_sin_oprimir(self.boton_eliminar)
        self.boton_eliminar.clicked.connect(self.eliminar_producto)

        self.boton_agregar = QPushButton()
        self.boton_agregar.setIcon(QIcon(self.imagen("imagenes/agregar.png", 50, 50)))
        self.boton_agregar.setIconSize(QSize(70, 70))
        self.boton_agregar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_boton_sin_oprimir(self.boton_agregar)
        self.boton_agregar.clicked.connect(self.agregar_producto)

        self.boton_busqueda = QPushButton()
        self.boton_busqueda.setIcon(QIcon(self.imagen("imagenes/buscar.png", 50, 50)))
        self.boton_busqueda.setIconSize(QSize(70, 70))
        self.boton_busqueda.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_boton_sin_oprimir(self.boton_busqueda)
        self.boton_busqueda.clicked.connect(self.buscar_producto)
        

        self.ingreso_busqueda = QLineEdit()
        self.ingreso_busqueda.setPlaceholderText("Ingrese el nombre del producto...")
        self.color_linea(self.ingreso_busqueda)
        self.ingreso_busqueda.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ingreso_busqueda.setFixedSize(400, 80)
        self.ingreso_busqueda.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # creacion de tabla,
        # Modificar desde la base de datos
        #Matriz de ejemplo
        inventario = self.base_datos.obtener_productos()  # Esto devuelve la lista de diccionarios

        # Crear la tabla con el número correcto de filas y columnas
        # Las columnas son: ID, Nombre, Existencias, Precio, Descripción, Costo (6 columnas), existencia minima
        self.tabla = QTableWidget(len(inventario), 7)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Define los encabezados de las columnas
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Descripcion", "Existencias", "Precio", "Costo", "Existencia mínima"])

        # Llenar la tabla con los datos
        for fila, producto in enumerate(inventario):
            # Convertir los valores a strings (excepto los que ya lo son)
            # Si la existencia es menor a la minima, cambiar el color de la celda

            
            id_item = QTableWidgetItem(str(producto['id']))
            nombre_item = QTableWidgetItem(producto['nombre'])
            descripcion_item = QTableWidgetItem(producto['descripcion'])
            precio_item = QTableWidgetItem(f"Q{producto['precio']:.2f}")  # Formato con 2 decimales
            costo_item = QTableWidgetItem(f"Q{producto['costo']:.2f}")  # Formato con 2 decimales
            existencia_minima_item = QTableWidgetItem(str(producto['stock_minimo']))
            
            # Añadir items a la tabla
            self.tabla.setItem(fila, 0, id_item)
            self.tabla.setItem(fila, 1, nombre_item)
            self.tabla.setItem(fila, 2, descripcion_item)


            if producto['stock'] < producto['stock_minimo']:
                self.tabla.setItem(fila, 3, QTableWidgetItem(str(producto['stock'])))
                self.tabla.item(fila, 3).setBackground(QBrush(QColor(235, 111, 84)))
            else:
                self.tabla.setItem(fila, 3, QTableWidgetItem(str(producto['stock'])))

            self.tabla.setItem(fila, 4, precio_item)
            self.tabla.setItem(fila, 5, costo_item)
            self.tabla.setItem(fila, 6, existencia_minima_item)
            
            # Configurar flags para todos los items
            for col in range(6):
                item = self.tabla.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        # Opcional: Ajustar el tamaño de las columnas al contenido
        # self.tabla.resizeColumnsToContents()

        #Modificacion del color, bordes y fondo de la tabla
        self.color_tabla(self.tabla)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout3.addWidget(self.boton_cancelar_venta)
        layout3.addWidget(self.boton_eliminar)
        layout3.addWidget(self.boton_agregar)
        layout3.addWidget(self.boton_busqueda)
        layout3.addWidget(self.ingreso_busqueda)

        layout4.addWidget(self.tabla)
        
        sub_layout.addLayout(layout3)
        sub_layout.addLayout(layout4)
        self.main_layout_ventana_inventario.addItem(self.espacio(35, 35))
        self.main_layout_ventana_inventario.addLayout(sub_layout)
        self.layout.addLayout(self.main_layout_ventana_inventario)

    def llenar_campos(self, row):
        self.nombre_producto = self.tabla.item(row, 1).text()
        # self.existencia_producto = self.tabla.item(row, 2).text()
        self.descripcion_producto = self.tabla.item(row, 2).text()
        
        self.precio_producto = self.tabla.item(row, 4).text()
        self.existencia_minima = self.tabla.item(row, 6).text()
        # Quitar el formato de moneda
        self.precio_producto = self.precio_producto.replace("Q", "")
        self.ingreso_nombre_producto.setText(self.nombre_producto)

        self.ingreso_precio_producto.setText(self.precio_producto)
        # self.ingreso_existencia_producto.setText(self.existencia_producto)
        self.ingreso_descripcion_producto.setText(self.descripcion_producto)
        self.ingreso_existencia_minima_producto.setText(self.existencia_minima)


    def agregar_producto(self):
        self.boton_cancelar_venta.setEnabled(False)
        self.boton_agregar.setEnabled(False)
        self.main_layout_editar_producto = QHBoxLayout()
        layout_espacio = QVBoxLayout()
        layout_espacio.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_imagen = QVBoxLayout()
        layout_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout2 = QGridLayout()

        image_editar = self.imagen("imagenes/agregar.png", 100, 100)
        imagen = QLabel()
        imagen.setPixmap(image_editar)
        imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagen.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        nombre_producto = QLabel("Nombre del producto: ")
        nombre_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        nombre_producto.setStyleSheet("Color: black")

        self.ingreso_nombre_producto = QLineEdit()
        self.color_linea(self.ingreso_nombre_producto)
        self.ingreso_nombre_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_nombre_producto.setFixedWidth(200)

        existencia_producto = QLabel("Existencias del producto: ")
        existencia_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        existencia_producto.setStyleSheet("Color: black")

        self.ingreso_existencia_producto = QLineEdit()
        self.color_linea(self.ingreso_existencia_producto)

        self.ingreso_existencia_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_existencia_producto.setFixedWidth(200)

        precio_producto = QLabel("Precio del producto: ")
        precio_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        precio_producto.setStyleSheet("Color: black")

        self.ingreso_precio_producto = QLineEdit()
        self.color_linea(self.ingreso_precio_producto)

        self.ingreso_precio_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_precio_producto.setFixedWidth(200)

        descripcion_producto = QLabel("Descripción del producto: ")
        descripcion_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        descripcion_producto.setStyleSheet("Color: black")

        # Existencia mínima
        existencia_minima_producto = QLabel("Existencia mínima del producto: ")
        existencia_minima_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        existencia_minima_producto.setStyleSheet("Color: black")

        self.ingreso_existencia_minima_producto = QLineEdit() # Ingreso de texto de existencia mínima
        self.color_linea(self.ingreso_existencia_minima_producto)
        
        self.ingreso_existencia_minima_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_existencia_minima_producto.setFixedWidth(200)

        self.ingreso_descripcion_producto = QLineEdit()
        self.color_linea(self.ingreso_descripcion_producto)

        self.ingreso_descripcion_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_descripcion_producto.setFixedWidth(200)

        boton_confirmar = QPushButton("Confirmar")
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.confirmar_insercion)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_cancelar.clicked.connect(self.cancelar_insercion)

        layout_espacio.addItem(self.espacio(100, 100))

        layout_imagen.addWidget(imagen)
        layout_imagen.addItem(self.espacio(50, 50))

        layout2.addWidget(nombre_producto, 0, 0)
        layout2.addWidget(self.ingreso_nombre_producto, 0, 1)

        # layout2.addItem(self.espacio(30, 30), 1, 0)
        # layout2.addWidget(existencia_producto, 2, 0)
        # layout2.addWidget(self.ingreso_existencia_producto, 2, 1)

        layout2.addItem(self.espacio(30, 30), 3, 0)
        layout2.addWidget(precio_producto, 4, 0)
        layout2.addWidget(self.ingreso_precio_producto, 4, 1)

        layout2.addItem(self.espacio(30, 30), 5, 0)
        layout2.addWidget(descripcion_producto, 6, 0)
        layout2.addWidget(self.ingreso_descripcion_producto, 6, 1)

        layout2.addItem(self.espacio(30, 30), 7, 0)
        layout2.addWidget(existencia_minima_producto, 8, 0)
        layout2.addWidget(self.ingreso_existencia_minima_producto, 8, 1)


        layout2.addItem(self.espacio(30, 30), 8, 0)
        layout2.addWidget(boton_confirmar, 9, 0)
        layout2.addWidget(boton_cancelar, 9, 1)

        layout1.addLayout(layout_espacio)
        layout1.addLayout(layout_imagen)
        layout1.addLayout(layout2)

        self.main_layout_editar_producto.addItem(self.espacio(30, 60))
        self.main_layout_editar_producto.addLayout(layout1)
        self.main_layout_ventana_inventario.addLayout(self.main_layout_editar_producto)

    def buscar_producto(self):
        # Buscar el producto por nombre en la base de datos
        nombre_producto = self.ingreso_busqueda.text()
        resultado = self.base_datos.buscar_producto_por_nombre(nombre_producto)
        
        if len(resultado) != 0:
            # Limpiar la tabla antes de mostrar los resultados
            self.tabla.clearContents()
            self.tabla.setRowCount(len(resultado))
            # Llenar la tabla con los resultados de la búsqueda
            for fila, producto in enumerate(resultado):
                id_item = QTableWidgetItem(str(producto['id']))
                nombre_item = QTableWidgetItem(producto['nombre'])
                descripcion_item = QTableWidgetItem(producto['descripcion'])
                existencia_item = QTableWidgetItem(str(producto['stock']))
                precio_item = QTableWidgetItem(f"Q{producto['precio']:.2f}")
                costo_item = QTableWidgetItem(f"Q{producto['costo']:.2f}")
                existencia_minima_item = QTableWidgetItem(str(producto['stock_minimo']))

                # Añadir items a la tabla
                self.tabla.setItem(fila, 0, id_item)
                self.tabla.setItem(fila, 1, nombre_item)
                self.tabla.setItem(fila, 2, descripcion_item)
                self.tabla.setItem(fila, 3, existencia_item)
                self.tabla.setItem(fila, 4, precio_item)
                self.tabla.setItem(fila, 5, costo_item)
                self.tabla.setItem(fila, 6, existencia_minima_item)
        else:
            self.mensaje_error("Error", "No se encontraron productos con ese nombre")

        self.ingreso_busqueda.clear()

    def eliminar_producto(self):
        # Eliminar el producto seleccionado en la tabla
        fila = self.tabla.currentRow()
        if fila != -1:
            # Ventana para confirmar eliminacion
            self.confirmar_eliminacion(fila)
            
        else:
            self.mensaje_error("Error", "No se ha seleccionado ningún producto")

    def editar_producto(self):
        self.boton_agregar.setEnabled(False)
        self.boton_cancelar_venta.setEnabled(False)
        self.tabla.cellClicked.connect(self.llenar_campos)
        self.main_layout_editar_producto = QHBoxLayout()
        layout_espacio = QVBoxLayout()
        layout_espacio.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_imagen = QVBoxLayout()
        layout_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout2 = QGridLayout()

        image_editar = self.imagen("imagenes/editar.png", 100, 100)
        imagen = QLabel()
        imagen.setPixmap(image_editar)
        imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagen.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        nombre_producto = QLabel("Nombre del producto: ")
        nombre_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        nombre_producto.setStyleSheet("Color: black")

        self.ingreso_nombre_producto = QLineEdit()
        self.color_linea(self.ingreso_nombre_producto)
        self.ingreso_nombre_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_nombre_producto.setFixedWidth(200)

        # existencia_producto = QLabel("Existencias del producto: ")
        # existencia_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # existencia_producto.setStyleSheet("Color: black")

        # self.ingreso_existencia_producto = QLineEdit()
        # self.color_linea(self.ingreso_existencia_producto)
        # self.ingreso_existencia_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # self.ingreso_existencia_producto.setFixedWidth(200)

        precio_producto = QLabel("Precio del producto: ")
        precio_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        precio_producto.setStyleSheet("Color: black")

        self.ingreso_precio_producto = QLineEdit()
        self.color_linea(self.ingreso_precio_producto)
        self.ingreso_precio_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_precio_producto.setFixedWidth(200)

        descripcion_producto = QLabel("Descripción del producto: ")
        descripcion_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        descripcion_producto.setStyleSheet("Color: black")


        self.ingreso_descripcion_producto = QLineEdit()
        self.color_linea(self.ingreso_descripcion_producto)
        self.ingreso_descripcion_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_descripcion_producto.setFixedWidth(200)


        existencia_minima_producto = QLabel("Existencia mínima del producto: ")
        existencia_minima_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        existencia_minima_producto.setStyleSheet("Color: black")

        self.ingreso_existencia_minima_producto = QLineEdit()
        self.color_linea(self.ingreso_existencia_minima_producto)
        self.ingreso_existencia_minima_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_existencia_minima_producto.setFixedWidth(200)

        boton_confirmar = QPushButton("Confirmar")
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.confirmar_edicion)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_cancelar.clicked.connect(self.cancelar_edicion)

        layout_espacio.addItem(self.espacio(100, 100))

        layout_imagen.addWidget(imagen)
        layout_imagen.addItem(self.espacio(50, 50))

        layout2.addWidget(nombre_producto, 0, 0)
        layout2.addWidget(self.ingreso_nombre_producto, 0, 1)

        # layout2.addItem(self.espacio(30, 30), 1, 0)
        # layout2.addWidget(existencia_producto, 2, 0)
        # layout2.addWidget(self.ingreso_existencia_producto, 2, 1)

        layout2.addItem(self.espacio(30, 30), 3, 0)
        layout2.addWidget(precio_producto, 4, 0)
        layout2.addWidget(self.ingreso_precio_producto, 4, 1)

        layout2.addItem(self.espacio(30, 30), 5, 0)
        layout2.addWidget(descripcion_producto, 6, 0)
        layout2.addWidget(self.ingreso_descripcion_producto, 6, 1)

        layout2.addItem(self.espacio(30, 30), 7, 0)
        layout2.addWidget(existencia_minima_producto, 8, 0)
        layout2.addWidget(self.ingreso_existencia_minima_producto, 8, 1)

        layout2.addItem(self.espacio(30, 30), 9, 0)
        layout2.addWidget(boton_confirmar, 10, 0)
        layout2.addWidget(boton_cancelar, 10, 1)

        layout1.addLayout(layout_espacio)
        layout1.addLayout(layout_imagen)
        layout1.addLayout(layout2)

        self.main_layout_editar_producto.addItem(self.espacio(30, 60))
        self.main_layout_editar_producto.addLayout(layout1)
        self.main_layout_ventana_inventario.addLayout(self.main_layout_editar_producto)

    def confirmar_eliminacion(self, fila):
        aviso = QMessageBox()
        aviso.setStyleSheet("QMessageBox { color: black; background-color: #36dfea;} QPushButton {color: black; background-color: #22a4ac;} QLabel{color: black;}")
        aviso.setWindowIcon(QIcon("imagenes/infomation.ico"))
        aviso.setWindowTitle("¿Eliminar producto?") 
        aviso.setText("¿Seguro que desea eliminar el producto seleccionado?")
        aviso.setIcon(QMessageBox.Icon.Information)
        aviso.addButton("Si", QMessageBox.ButtonRole.YesRole)
        aviso.addButton("No", QMessageBox.ButtonRole.NoRole)
        respuesta = aviso.exec()
        if respuesta == 2:
            id_producto = self.tabla.item(fila, 0).text()
            self.base_datos.eliminar_producto(id_producto)
            self.tabla.removeRow(fila)
            self.limpieza_layout(self.main_layout_ventana_inventario)
            self.inventario()
            self.mensaje_informacion("Producto eliminado", "El producto ha sido eliminado correctamente")
        elif respuesta == 3:
            self.mensaje_informacion("Eliminación cancelada", "El producto no ha sido eliminado")

    def confirmar_edicion(self):
        self.limpieza_layout(self.main_layout_editar_producto)
        self.boton_agregar.setEnabled(True)
        self.boton_cancelar_venta.setEnabled(True)
        # Implementar función para guardar los cambios en la base de datos
        nombre = self.ingreso_nombre_producto.text()
        precio = float(self.ingreso_precio_producto.text().replace("Q", ""))
        descripcion = self.ingreso_descripcion_producto.text()
        id_producto = int(self.tabla.item(self.tabla.currentRow(), 0).text())
        existencia_minima = int(self.ingreso_existencia_minima_producto.text())
        # Aquí se debe de modificar el producto en la base de datos
        self.base_datos.modificar_producto(id_producto, nombre, precio, descripcion, existencia_minima)
        # volver a cargar el inventario
        self.limpieza_layout(self.main_layout_ventana_inventario)
        self.inventario()

        self.mensaje_informacion("Correcciones guardadas", "Los cambios se han guardado correctamente")
    
    def cancelar_edicion(self):
        self.limpieza_layout(self.main_layout_editar_producto)
        self.boton_agregar.setEnabled(True)
        self.boton_cancelar_venta.setEnabled(True)
        self.mensaje_informacion("Correcciones canceladas", "El producto no ha sido modificado")

    def confirmar_insercion(self):
        # Lógica para ingresar productos a la base de datos
        self.limpieza_layout(self.main_layout_editar_producto)
        self.boton_cancelar_venta.setEnabled(True)
        self.boton_agregar.setEnabled(True)

        nombre = self.ingreso_nombre_producto.text()
        # existencia = int(self.ingreso_existencia_producto.text())
        precio = float(self.ingreso_precio_producto.text())
        descripcion = self.ingreso_descripcion_producto.text()
        existencia_minima = int(self.ingreso_existencia_minima_producto.text())

        # Aquí se debe de agregar el producto a la base de datos
        self.base_datos.agregar_producto(nombre, precio, descripcion, existencia_minima)
        
        # Volver a cargar el inventario
        self.limpieza_layout(self.main_layout_ventana_inventario)
        self.inventario()

        self.mensaje_informacion("Inserción realizada", "El producto se ha insertado correctamente")
        
    def cancelar_insercion(self):
        self.limpieza_layout(self.main_layout_editar_producto)
        self.boton_agregar.setEnabled(True)
        self.boton_cancelar_venta.setEnabled(True)
        self.mensaje_informacion("Inserción cancelada", "El producto no se ha insertado")

