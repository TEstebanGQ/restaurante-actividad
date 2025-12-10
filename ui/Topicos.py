from core.Storage import loadData, saveData
from ui.UIHelpers import *

def gestionTopicosMenu():
    """Menú principal de gestión de tópicos (mesas/áreas)"""
    opciones = [
        "Ver estado de mesas",
        "Agregar nueva mesa",
        "Modificar mesa",
        "Eliminar mesa",
        "Cambiar disponibilidad",
        "Regresar al menú principal"
    ]
    
    acciones = {
        "1": verTopicos, "2": agregarTopico, "3": modificarTopico,
        "4": eliminarTopico, "5": cambiarDisponibilidad
    }
    
    while True:
        opcion = mostrarMenu(opciones, "GESTIÓN DE TÓPICOS (MESAS)")
        if opcion == "6":
            break
        elif opcion in acciones:
            acciones[opcion]()
        else:
            mostrarMensaje("Opción inválida.", "error")
            pausarPantalla()

def verTopicos():
    """Muestra el estado de todas las mesas"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("ESTADO DE MESAS")
    
    if not data["topicos"]:
        mostrarMensaje("No hay mesas registradas.", "error")
    else:
        tabla = [[t["id"], t["nombre"], " Disponible" if t["disponible"] else "✗ Ocupada"] 
                 for t in data["topicos"]]
        mostrarTabla(tabla, ["ID", "Nombre", "Estado"])
        disponibles = sum(1 for t in data["topicos"] if t["disponible"])
        print(f"\nMesas disponibles: {disponibles}/{len(data['topicos'])}")
    
    pausarPantalla()

def agregarTopico():
    """Agrega una nueva mesa/área"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("AGREGAR NUEVA MESA")
    
    nombre = inputSeguro("Nombre de la mesa/área: ")
    if not nombre:
        mostrarMensaje("Operación cancelada.", "error")
        pausarPantalla()
        return
    
    nuevoId = max([t["id"] for t in data["topicos"]], default=0) + 1
    
    if confirmarOperacion(f"¿Agregar '{nombre}'?", 
                         f"Mesa agregada exitosamente con ID: {nuevoId}"):
        nuevoTopico = {"id": nuevoId, "nombre": nombre, "disponible": True}
        data["topicos"].append(nuevoTopico)
        saveData(data)
    
    pausarPantalla()

def modificarTopico():
    """Modifica el nombre de una mesa"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("MODIFICAR MESA")
    
    topico = seleccionarDeTabla(data, data["topicos"], ["ID", "Nombre"], 
                                 "ID de la mesa a modificar")
    if not topico:
        pausarPantalla()
        return
    
    print(f"\nMesa actual: {topico['nombre']}")
    nuevoNombre = inputSeguro(f"Nuevo nombre (Enter para mantener '{topico['nombre']}'): ")
    
    if nuevoNombre:
        topico["nombre"] = nuevoNombre
        if confirmarOperacion("¿Guardar cambios?", "Mesa modificada exitosamente.", "Cambios descartados."):
            saveData(data)
    else:
        mostrarMensaje("No se realizaron cambios.", "error")
    
    pausarPantalla()

def eliminarTopico():
    """Elimina una mesa del sistema"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("ELIMINAR MESA")
    
    topico = seleccionarDeTabla(data, data["topicos"], ["ID", "Nombre", "Estado"], 
                                 "ID de la mesa a eliminar")
    if not topico:
        pausarPantalla()
        return
    
    if not topico["disponible"]:
        mostrarMensaje("No se puede eliminar una mesa ocupada.", "error")
        pausarPantalla()
        return
    
    if confirmarOperacion(f"¿Eliminar '{topico['nombre']}'?", "Mesa eliminada exitosamente."):
        data["topicos"] = [t for t in data["topicos"] if t["id"] != topico["id"]]
        saveData(data)
    
    pausarPantalla()

def cambiarDisponibilidad():
    """Cambia el estado de disponibilidad de una mesa"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("CAMBIAR DISPONIBILIDAD")
    
    topico = seleccionarDeTabla(data, data["topicos"], ["ID", "Nombre", "Estado"], 
                                 "ID de la mesa")
    if not topico:
        pausarPantalla()
        return
    
    estadoActual = "Disponible" if topico["disponible"] else "Ocupada"
    nuevoEstado = "Ocupada" if topico["disponible"] else "Disponible"
    
    if confirmarOperacion(f"Cambiar estado de '{topico['nombre']}' de {estadoActual} a {nuevoEstado}?", 
                         f"Estado cambiado a: {nuevoEstado}"):
        topico["disponible"] = not topico["disponible"]
        saveData(data)
    
    pausarPantalla()