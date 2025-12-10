from core.Storage import loadData, saveData, nextIdCliente
from ui.UIHelpers import *

def gestionClientesMenu():
    """Menú principal de gestión de clientes"""
    opciones = [
        "Ver todos los clientes",
        "Registrar nuevo cliente",
        "Modificar cliente",
        "Eliminar cliente",
        "Buscar cliente",
        "Regresar al menú principal"
    ]
    
    acciones = {
        "1": verClientes, "2": registrarCliente, "3": modificarCliente,
        "4": eliminarCliente, "5": buscarCliente
    }
    
    while True:
        opcion = mostrarMenu(opciones, "GESTIÓN DE CLIENTES")
        if opcion == "6":
            break
        elif opcion in acciones:
            acciones[opcion]()
        else:
            mostrarMensaje("Opción inválida.", "error")
            pausarPantalla()

def verClientes():
    """Muestra todos los clientes registrados"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("LISTADO DE CLIENTES")
    
    if not data["clientes"]:
        mostrarMensaje("No hay clientes registrados.", "error")
    else:
        tabla = [[c["id"], c["nombre"], c["telefono"], c.get("email") or "N/A"] for c in data["clientes"]]
        mostrarTabla(tabla, ["ID", "Nombre", "Teléfono", "Email"])
    
    pausarPantalla()

def registrarCliente():
    """Registra un nuevo cliente"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("REGISTRAR NUEVO CLIENTE")
    
    nombre = inputSeguro("Nombre completo: ")
    telefono = inputSeguro("Teléfono: ")
    
    if not nombre or not telefono:
        mostrarMensaje("Operación cancelada.", "error")
        pausarPantalla()
        return
    
    email = inputSeguro("Email (opcional, Enter para omitir): ") or ""
    
    if confirmarOperacion(f"¿Registrar a {nombre}?", 
                         f"Cliente registrado exitosamente con ID: {nextIdCliente(data)}"):
        nuevoCliente = {
            "id": nextIdCliente(data),
            "nombre": nombre,
            "telefono": telefono,
            "email": email
        }
        data["clientes"].append(nuevoCliente)
        saveData(data)
    
    pausarPantalla()

def modificarCliente():
    """Modifica los datos de un cliente"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("MODIFICAR CLIENTE")
    
    cliente = seleccionarDeTabla(data, data["clientes"], ["ID", "Nombre", "Teléfono"], 
                                  "ID del cliente a modificar")
    if not cliente:
        pausarPantalla()
        return
    
    print(f"\nCliente actual: {cliente['nombre']} - {cliente['telefono']}")
    nuevoNombre = inputSeguro(f"Nuevo nombre (Enter para mantener '{cliente['nombre']}'): ")
    nuevoTelefono = inputSeguro(f"Nuevo teléfono (Enter para mantener '{cliente['telefono']}'): ")
    nuevoEmail = inputSeguro(f"Nuevo email (Enter para mantener '{cliente.get('email', '')}'): ")
    
    if nuevoNombre: cliente["nombre"] = nuevoNombre
    if nuevoTelefono: cliente["telefono"] = nuevoTelefono
    if nuevoEmail is not None: cliente["email"] = nuevoEmail
    
    if confirmarOperacion("¿Guardar cambios?", "Cliente modificado exitosamente.", "Cambios descartados."):
        saveData(data)
    
    pausarPantalla()

def eliminarCliente():
    """Elimina un cliente del sistema"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("ELIMINAR CLIENTE")
    
    cliente = seleccionarDeTabla(data, data["clientes"], ["ID", "Nombre", "Teléfono"], 
                                  "ID del cliente a eliminar")
    if not cliente:
        pausarPantalla()
        return
    
    if confirmarOperacion(f"¿Eliminar a '{cliente['nombre']}'?", "Cliente eliminado exitosamente."):
        data["clientes"] = [c for c in data["clientes"] if c["id"] != cliente["id"]]
        saveData(data)
    
    pausarPantalla()

def buscarCliente():
    """Busca un cliente por nombre o teléfono"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("BUSCAR CLIENTE")
    
    criterio = inputSeguro("Buscar por nombre o teléfono: ")
    if not criterio:
        pausarPantalla()
        return
    
    resultados = buscarPorCriterio(data["clientes"], criterio, ["nombre", "telefono"])
    
    if resultados:
        print(f"\n✓ Se encontraron {len(resultados)} cliente(s):")
        tabla = [[c["id"], c["nombre"], c["telefono"], c.get("email", "N/A")] for c in resultados]
        mostrarTabla(tabla, ["ID", "Nombre", "Teléfono", "Email"])
    else:
        mostrarMensaje("No se encontraron clientes con ese criterio.", "error")
    
    pausarPantalla()