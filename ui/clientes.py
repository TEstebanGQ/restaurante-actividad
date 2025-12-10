from ui.prompts import inputSeguro, confirmarAccion
from utils.screenControllers import limpiarPantalla, pausarPantalla
from core.storage import loadData, saveData, nextIdCliente
from tabulate import tabulate

def gestionClientesMenu():
    """Menú principal de gestión de clientes"""
    while True:
        limpiarPantalla()
        print("""
╔═══════════════════════════════════════════╗
║         GESTIÓN DE CLIENTES              ║
╚═══════════════════════════════════════════╝

1. Ver todos los clientes
2. Registrar nuevo cliente
3. Modificar cliente
4. Eliminar cliente
5. Buscar cliente
6. Regresar al menú principal

═══════════════════════════════════════════
""")
        
        opcion = inputSeguro("Seleccione una opción: ")
        
        if opcion == "1":
            verClientes()
        elif opcion == "2":
            registrarCliente()
        elif opcion == "3":
            modificarCliente()
        elif opcion == "4":
            eliminarCliente()
        elif opcion == "5":
            buscarCliente()
        elif opcion == "6":
            break
        else:
            print("✗ Opción inválida.")
            pausarPantalla()

def verClientes():
    """Muestra todos los clientes registrados"""
    limpiarPantalla()
    data = loadData()
    clientes = data["clientes"]
    
    print("""
╔═══════════════════════════════════════════╗
║        LISTADO DE CLIENTES               ║
╚═══════════════════════════════════════════╝
""")
    
    if not clientes:
        print("\n✗ No hay clientes registrados.")
        pausarPantalla()
        return
    
    tabla = [
        [c["id"], c["nombre"], c["telefono"], c["email"] if c.get("email") else "N/A"]
        for c in clientes
    ]
    print(tabulate(tabla, headers=["ID", "Nombre", "Teléfono", "Email"], tablefmt="grid"))
    
    pausarPantalla()

def registrarCliente():
    """Registra un nuevo cliente"""
    limpiarPantalla()
    data = loadData()
    
    print("""
╔═══════════════════════════════════════════╗
║        REGISTRAR NUEVO CLIENTE           ║
╚═══════════════════════════════════════════╝
""")
    
    nombre = inputSeguro("Nombre completo: ")
    if not nombre:
        print("✗ Operación cancelada.")
        pausarPantalla()
        return
    
    telefono = inputSeguro("Teléfono: ")
    if not telefono:
        print("✗ Operación cancelada.")
        pausarPantalla()
        return
    
    email = inputSeguro("Email (opcional, Enter para omitir): ")
    
    if confirmarAccion(f"\n¿Registrar a {nombre}? (S/N): "):
        nuevo_id = nextIdCliente(data)
        
        nuevo_cliente = {
            "id": nuevo_id,
            "nombre": nombre,
            "telefono": telefono,
            "email": email if email else ""
        }
        
        data["clientes"].append(nuevo_cliente)
        saveData(data)
        
        print(f"✓ Cliente registrado exitosamente con ID: {nuevo_id}")
    else:
        print("✗ Operación cancelada.")
    
    pausarPantalla()

def modificarCliente():
    """Modifica los datos de un cliente"""
    limpiarPantalla()
    data = loadData()
    clientes = data["clientes"]
    
    print("""
╔═══════════════════════════════════════════╗
║          MODIFICAR CLIENTE               ║
╚═══════════════════════════════════════════╝
""")
    
    if not clientes:
        print("\n✗ No hay clientes registrados.")
        pausarPantalla()
        return
    
    tabla = [
        [c["id"], c["nombre"], c["telefono"]]
        for c in clientes
    ]
    print(tabulate(tabla, headers=["ID", "Nombre", "Teléfono"], tablefmt="grid"))
    
    id_cliente = inputSeguro("\nID del cliente a modificar: ")
    
    cliente = next((c for c in clientes if c["id"] == id_cliente), None)
    
    if not cliente:
        print("✗ Cliente no encontrado.")
        pausarPantalla()
        return
    
    print(f"\nCliente actual: {cliente['nombre']} - {cliente['telefono']}")
    
    nuevo_nombre = inputSeguro(f"Nuevo nombre (Enter para mantener '{cliente['nombre']}'): ")
    nuevo_telefono = inputSeguro(f"Nuevo teléfono (Enter para mantener '{cliente['telefono']}'): ")
    nuevo_email = inputSeguro(f"Nuevo email (Enter para mantener '{cliente.get('email', '')}'): ")
    
    if nuevo_nombre:
        cliente["nombre"] = nuevo_nombre
    if nuevo_telefono:
        cliente["telefono"] = nuevo_telefono
    if nuevo_email is not None:
        cliente["email"] = nuevo_email
    
    if confirmarAccion("\n¿Guardar cambios? (S/N): "):
        saveData(data)
        print("✓ Cliente modificado exitosamente.")
    else:
        print("✗ Cambios descartados.")
    
    pausarPantalla()

def eliminarCliente():
    """Elimina un cliente del sistema"""
    limpiarPantalla()
    data = loadData()
    clientes = data["clientes"]
    
    print("""
╔═══════════════════════════════════════════╗
║          ELIMINAR CLIENTE                ║
╚═══════════════════════════════════════════╝
""")
    
    if not clientes:
        print("\n✗ No hay clientes registrados.")
        pausarPantalla()
        return
    
    tabla = [
        [c["id"], c["nombre"], c["telefono"]]
        for c in clientes
    ]
    print(tabulate(tabla, headers=["ID", "Nombre", "Teléfono"], tablefmt="grid"))
    
    id_cliente = inputSeguro("\nID del cliente a eliminar: ")
    
    cliente = next((c for c in clientes if c["id"] == id_cliente), None)
    
    if not cliente:
        print("✗ Cliente no encontrado.")
        pausarPantalla()
        return
    
    if confirmarAccion(f"\n¿Eliminar a '{cliente['nombre']}'? (S/N): "):
        data["clientes"] = [c for c in clientes if c["id"] != id_cliente]
        saveData(data)
        print("✓ Cliente eliminado exitosamente.")
    else:
        print("✗ Operación cancelada.")
    
    pausarPantalla()

def buscarCliente():
    """Busca un cliente por nombre o teléfono"""
    limpiarPantalla()
    data = loadData()
    clientes = data["clientes"]
    
    print("""
╔═══════════════════════════════════════════╗
║           BUSCAR CLIENTE                 ║
╚═══════════════════════════════════════════╝
""")
    
    if not clientes:
        print("\n✗ No hay clientes registrados.")
        pausarPantalla()
        return
    
    criterio = inputSeguro("Buscar por nombre o teléfono: ")
    if not criterio:
        print("✗ Operación cancelada.")
        pausarPantalla()
        return
    
    criterio = criterio.lower()
    resultados = [
        c for c in clientes 
        if criterio in c["nombre"].lower() or criterio in c["telefono"]
    ]
    
    if not resultados:
        print("\n✗ No se encontraron clientes con ese criterio.")
    else:
        print(f"\n✓ Se encontraron {len(resultados)} cliente(s):\n")
        tabla = [
            [c["id"], c["nombre"], c["telefono"], c.get("email", "N/A")]
            for c in resultados
        ]
        print(tabulate(tabla, headers=["ID", "Nombre", "Teléfono", "Email"], tablefmt="grid"))
    
    pausarPantalla()