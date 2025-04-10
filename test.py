from Base_datos import BaseDatos

print("Iniciando base de datos...")
base_datos = BaseDatos('root', 'admin')
            #Aquí se inicia base de datos
if base_datos.conexion and base_datos.conexion.is_connected():
    print("Base de datos iniciada correctamente")
else:
    print("La base de datos no se ha iniciado ")