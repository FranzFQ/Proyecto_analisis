import pytest
from unittest.mock import MagicMock
from ventana_inicio import Ventana_inicio
import pymysql

@pytest.fixture
def app_fixture(qtbot, mocker):
    ventana = Ventana_inicio()
    
    # Simular conexión exitosa
    mock_conexion = MagicMock()
    mock_conexion.open = True
    mock_conexion.ping.return_value = None
    mocker.patch('Base_datos.BaseDatos', return_value=mock_conexion)
    
    ventana.inicio()
    
    return ventana

def test_verificacion_conexion_fallida(qtbot, mocker):
    # Configurar mock para simular error de conexión
    mocker.patch('pymysql.connect', side_effect=pymysql.Error("Error de conexión"))
    
    ventana = Ventana_inicio()
    ventana.inicio()
    
    # Simular entrada de usuario
    ventana.ingreso_usuario.setText("usuario_invalido")
    ventana.ingreso_contrasenia.setText("password_invalido")
    
    # Ejecutar verificación
    ventana.verificacion()
    
    # Verificar que los campos se limpiaron
    assert ventana.ingreso_usuario.text() == ""
    assert ventana.ingreso_contrasenia.text() == ""

def test_verificacion_conexion_exitosa(app_fixture):
    # Simulamos que el usuario y la contraseña son correctos
    app_fixture.ingreso_usuario.setText("usuario_prueba")
    app_fixture.ingreso_contrasenia.setText("password_prueba")
    
    # Ejecutar la verificación
    app_fixture.verificacion()

    # Verificar si la ventana se oculta (esto sucede si la conexión es exitosa)
    assert app_fixture.window1.isHidden()

