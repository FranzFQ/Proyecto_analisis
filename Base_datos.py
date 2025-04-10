import pymysql
from pymysql import cursors


class BaseDatos:
    def __init__(self, user, password):
        self.conexion = pymysql.connect(
            host="localhost",
            user=user,
            password=password,
            database="modelo_proyecto",
            cursorclass=cursors.DictCursor)  # Para obtener resultados como diccionarios

    def agregar_producto(self, nombre, precio, stock, descripcion, existencia_minima):
        with self.conexion.cursor() as cursor:
            sql = """INSERT INTO modelo_proyecto.producto 
                    (nombre, precio, stock, descripcion, costo, stock_minimo) 
                    VALUES (%s, %s, %s, %s, %s, %s)"""
            costo = precio - (precio * 0.15)
            cursor.execute(sql, (nombre, precio, stock, descripcion, costo, existencia_minima))
        self.conexion.commit()

    def obtener_productos(self):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                SELECT id, nombre, stock, precio, descripcion, costo 
                FROM modelo_proyecto.producto
            """)
            return cursor.fetchall()

    def eliminar_producto(self, id):
        with self.conexion.cursor() as cursor:
            cursor.execute("DELETE FROM producto WHERE id = %s", (id,))
        self.conexion.commit()

    def buscar_producto_por_nombre(self, nombre):
        with self.conexion.cursor() as cursor:
            cursor.execute("""
                SELECT id, nombre, stock, precio, descripcion, costo 
                FROM modelo_proyecto.producto 
                WHERE nombre LIKE %s
            """, (f"%{nombre}%",))
            return cursor.fetchall()

    def modificar_producto(self, id, nombre, precio, descripcion, stock, existencia_minima):
        with self.conexion.cursor() as cursor:
            sql = """
                UPDATE producto 
                SET nombre = %s, precio = %s, descripcion = %s, 
                    stock = %s, stock_minimo = %s, costo = %s 
                WHERE id = %s
            """
            costo = precio - (precio * 0.15)
            cursor.execute(sql, (nombre, precio, descripcion, stock, existencia_minima, costo, id))
        self.conexion.commit()