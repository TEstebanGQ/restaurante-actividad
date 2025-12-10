from ui.prompts import inputSeguro, confirmarAccion
from utils.screenControllers import limpiarPantalla, pausarPantalla
from ui.productos import gestionProductosMenu
from ui.clientes import gestionClientesMenu
from ui.topicos import gestionTopicosMenu
from ui.pedidos import gestionPedidosMenu

def menuPrincipal():
    """Menú principal del sistema de restaurante"""
    while True:
        limpiarPantalla()
        print("""
╔═══════════════════════════════════════════╗
║    SISTEMA DE GESTIÓN DE RESTAURANTE     ║
╚═══════════════════════════════════════════╝

Seleccione una opción:

1. Gestión de Productos
2. Gestión de Clientes
3. Gestión de Tópicos (Mesas)
4. Gestión de Pedidos
5. Salir

═══════════════════════════════════════════
""")

        opcion = inputSeguro("Seleccione una opción: ")

        if opcion == "1":
            gestionProductosMenu()
        elif opcion == "2":
            gestionClientesMenu()
        elif opcion == "3":
            gestionTopicosMenu()
        elif opcion == "4":
            gestionPedidosMenu()
        elif opcion == "5":
            if confirmarAccion("¿Desea salir del programa? (S/N): "):
                print("\n✓ Gracias por usar el Sistema de Restaurante.")
                print("¡Hasta pronto!\n")
                break
        else:
            print("✗ Opción inválida.")
            pausarPantalla()