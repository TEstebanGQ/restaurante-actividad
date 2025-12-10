import os
import sys

def pausarPantalla():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    try:
        input('\nPresione ENTER para continuar...')
    except KeyboardInterrupt:
        print("\n✗ Operación cancelada.")

def limpiarPantalla():
    """Limpia la pantalla de la consola según el sistema operativo"""
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")