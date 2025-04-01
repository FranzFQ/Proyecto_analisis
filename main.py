from ventana import Ventana
import sys

def main():
    ventana = Ventana()
    app = ventana.app
    ventana.inicio()
    sys.exit(app.exec())
    
main()   