import mysql.connector

class BaseDatos:
    def __init__(self, user, password):
        self.conexion = mysql.connector.connect(
            host = "localhost",
            user = user,
            password = password,
            database = 'modelo_proyecto')
        
    def agregar_producto(self, nombre, precio, stock, descripcion, existencia_minima):
        cursor = self.conexion.cursor()
        cursor.execute(f"INSERT INTO `modelo_proyecto`.`producto` (`nombre`, `precio`, `stock`, `descripcion`, `costo`, `stock_minimo`) VALUES ('{nombre}', {precio}, {stock},'{descripcion}', {precio - (precio * .15)}, {existencia_minima});") #cambiar nombre de la base de datos y la tabla
        self.conexion.commit()
        cursor.close()

    def obtener_productos(self):
        cursor = self.conexion.cursor()
        #inventario = [["1", "Caja de lapices","2","15Q", "Descripcion 1"]
        cursor.execute("SELECT id, nombre, stock, precio, descripcion, costo FROM modelo_proyecto.producto")
        resultado = cursor.fetchall()
        cursor.close()
        return resultado

    def eliminar_producto(self, id):
        cursor = self.conexion.cursor()
        cursor.execute(f"DELETE FROM producto WHERE id = {id}")
        self.conexion.commit()
        cursor.close()

    def buscar_producto_por_nombre(self, nombre):
        cursor = self.conexion.cursor()
        cursor.execute(f"SELECT id, nombre, stock, precio, descripcion, costo FROM modelo_proyecto.producto WHERE nombre LIKE '%{nombre}%'")
        resultado = cursor.fetchall()
        cursor.close()
        return resultado

    def modificar_producto(self, id, nombre, precio, descripcion, stock, existencia_minima):
        cursor = self.conexion.cursor()
        cursor.execute(f"UPDATE producto SET nombre = '{nombre}', precio = '{precio}', descripcion = '{descripcion}', stock = '{stock}', stock_minimo = '{existencia_minima}', costo = '{precio - (precio * .15)}' WHERE id = {id}")
        self.conexion.commit()
        cursor.close()

