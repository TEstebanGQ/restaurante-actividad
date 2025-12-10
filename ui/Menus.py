from ui.Prompts import inputSeguro, confirmarAccion
from ui.UIHelpers import mostrarMenu
from ui.Productos import gestionProductosMenu
from ui.Clientes import gestionClientesMenu
from ui.Topicos import gestionTopicosMenu
from ui.Pedidos import gestionPedidosMenu

def menuPrincipal():
    """Menú principal del sistema de restaurante"""
    opciones = [
        "Gestión de Productos",
        "Gestión de Clientes",
        "Gestión de Tópicos (Mesas)",
        "Gestión de Pedidos",
        "Salir"
    ]
    
    acciones = {
        "1": gestionProductosMenu,
        "2": gestionClientesMenu,
        "3": gestionTopicosMenu,
        "4": gestionPedidosMenu
    }
    
    while True:
        opcion = mostrarMenu(opciones, "SISTEMA DE GESTIÓN DE RESTAURANTE")
        
        if opcion == "5":
            if confirmarAccion("¿Desea salir del programa? (S/N): "):
                print("\n Gracias por usar el Sistema de Restaurante.")
                print("¡Hasta pronto!\n")
                break
        elif opcion in acciones:
            acciones[opcion]()
        else:
            print(" Opción inválida.")
            from utils.ScreenControllers import pausarPantalla
            pausarPantalla()