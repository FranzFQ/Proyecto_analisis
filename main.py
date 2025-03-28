from ventana import Ventana
import sys

def main():
    ventana = Ventana()
    app = ventana.app
    ventana.ventana_principal()
    sys.exit(app.exec())
    
main()   