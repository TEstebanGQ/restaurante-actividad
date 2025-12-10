from tabulate import tabulate
from utils.ScreenControllers import limpiarPantalla, pausarPantalla
from ui.Prompts import inputSeguro, confirmarAccion

def mostrarHeader(titulo):
    """Muestra un encabezado formateado"""
    print(f"""
╔═══════════════════════════════════════════╗
║{titulo.center(43)}║
╚═══════════════════════════════════════════╝
""")

def mostrarTabla(datos, headers, mensaje=""):
    """Muestra una tabla formateada"""
    if mensaje:
        print(f"\n{mensaje}")
    print(tabulate(datos, headers=headers, tablefmt="grid"))

def mostrarMensaje(mensaje, tipo="info"):
    """Muestra un mensaje formateado"""
    simbolo = "✓" if tipo == "success" else "✗"
    print(f"\n{simbolo} {mensaje}")

def seleccionarDeTabla(data, items, headers, mensaje, id_field="id"):
    """Función genérica para seleccionar un item de una tabla"""
    if not items:
        mostrarMensaje("No hay elementos disponibles.", "error")
        pausarPantalla()
        return None
    
    tabla = [[item.get(h.lower(), "") for h in headers] for item in items]
    mostrarTabla(tabla, headers)
    
    id_seleccionado = inputSeguro(f"\n{mensaje}: ")
    if not id_seleccionado:
        return None
    
    try:
        id_seleccionado = int(id_seleccionado) if id_field == "id" else id_seleccionado
        return next((item for item in items if item[id_field] == id_seleccionado), None)
    except ValueError:
        mostrarMensaje("ID inválido.", "error")
        return None

def buscarPorCriterio(items, criterio, campos):
    """Busca items por criterio en múltiples campos"""
    criterio = criterio.lower()
    return [item for item in items if any(criterio in str(item.get(campo, "")).lower() for campo in campos)]

def confirmarOperacion(mensaje, accion_si, accion_no="Operación cancelada."):
    """Confirma una operación y ejecuta acciones"""
    if confirmarAccion(f"\n{mensaje} (S/N): "):
        mostrarMensaje(accion_si, "success")
        return True
    else:
        mostrarMensaje(accion_no, "error")
        return False

def mostrarMenu(opciones, titulo):
    """Muestra un menú genérico y retorna la opción seleccionada"""
    limpiarPantalla()
    mostrarHeader(titulo)
    
    for i, opcion in enumerate(opciones, 1):
        print(f"{i}. {opcion}")
    print("\n═══════════════════════════════════════════")
    
    return inputSeguro("Seleccione una opción: ")

def validarNumero(valor, mensaje_error="Valor inválido"):
    """Valida que un valor sea numérico"""
    try:
        numero = float(valor)
        if numero <= 0:
            mostrarMensaje("El valor debe ser mayor a 0.", "error")
            return None
        return numero
    except ValueError:
        mostrarMensaje(mensaje_error, "error")
        return None