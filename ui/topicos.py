from ui.prompts import inputSeguro, confirmarAccion
from utils.screenControllers import limpiarPantalla, pausarPantalla
from core.storage import loadData, saveData
from tabulate import tabulate

def gestionTopicosMenu():
    """Menú principal de gestión de tópicos (mesas/áreas)"""
    while True:
        limpiarPantalla()
        print("""
╔═══════════════════════════════════════════╗
║      GESTIÓN DE TÓPICOS (MESAS)         ║
╚═══════════════════════════════════════════╝

1. Ver estado de mesas
2. Agregar nueva mesa
3. Modificar mesa
4. Eliminar mesa
5. Cambiar disponibilidad
6. Regresar al menú principal

═══════════════════════════════════════════
""")
        
        opcion = inputSeguro("Seleccione una opción: ")
        
        if opcion == "1":
            verTopicos()
        elif opcion == "2":
            agregarTopico()
        elif opcion == "3":
            modificarTopico()
        elif opcion == "4":
            eliminarTopico()
        elif opcion == "5":
            cambiarDisponibilidad()
        elif opcion == "6":
            break
        else:
            print("✗ Opción inválida.")
            pausarPantalla()

def verTopicos():
    """Muestra el estado de todas las mesas"""
    limpiarPantalla()
    data = loadData()
    topicos = data["topicos"]
    
    print("""
╔═══════════════════════════════════════════╗
║         ESTADO DE MESAS                  ║
╚═══════════════════════════════════════════╝
""")
    
    if not topicos:
        print("\n✗ No hay mesas registradas.")
        pausarPantalla()
        return
    
    tabla = [
        [
            t["id"], 
            t["nombre"], 
            "✓ Disponible" if t["disponible"] else "✗ Ocupada"
        ]
        for t in topicos
    ]
    print(tabulate(tabla, headers=["ID", "Nombre", "Estado"], tablefmt="grid"))
    
    disponibles = sum(1 for t in topicos if t["disponible"])
    print(f"\nMesas disponibles: {disponibles}/{len(topicos)}")
    
    pausarPantalla()

def agregarTopico():
    """Agrega una nueva mesa/área"""
    limpiarPantalla()
    data = loadData()
    
    print("""
╔═══════════════════════════════════════════╗
║          AGREGAR NUEVA MESA              ║
╚═══════════════════════════════════════════╝
""")
    
    nombre = inputSeguro("Nombre de la mesa/área: ")
    if not nombre:
        print("✗ Operación cancelada.")
        pausarPantalla()
        return
    
    topicos = data["topicos"]
    nuevo_id = max([t["id"] for t in topicos], default=0) + 1
    
    nuevo_topico = {
        "id": nuevo_id,
        "nombre": nombre,
        "disponible": True
    }
    
    if confirmarAccion(f"\n¿Agregar '{nombre}'? (S/N): "):
        data["topicos"].append(nuevo_topico)
        saveData(data)
        print(f"✓ Mesa agregada exitosamente con ID: {nuevo_id}")
    else:
        print("✗ Operación cancelada.")
    
    pausarPantalla()

def modificarTopico():
    """Modifica el nombre de una mesa"""
    limpiarPantalla()
    data = loadData()
    topicos = data["topicos"]
    
    print("""
╔═══════════════════════════════════════════╗
║          MODIFICAR MESA                  ║
╚═══════════════════════════════════════════╝
""")
    
    if not topicos:
        print("\n✗ No hay mesas registradas.")
        pausarPantalla()
        return
    
    tabla = [[t["id"], t["nombre"]] for t in topicos]
    print(tabulate(tabla, headers=["ID", "Nombre"], tablefmt="grid"))
    
    id_topico = inputSeguro("\nID de la mesa a modificar: ")
    
    try:
        id_topico = int(id_topico)
        topico = next((t for t in topicos if t["id"] == id_topico), None)
        
        if not topico:
            print("✗ Mesa no encontrada.")
            pausarPantalla()
            return
        
        print(f"\nMesa actual: {topico['nombre']}")
        nuevo_nombre = inputSeguro(f"Nuevo nombre (Enter para mantener '{topico['nombre']}'): ")
        
        if nuevo_nombre:
            topico["nombre"] = nuevo_nombre
            
            if confirmarAccion("\n¿Guardar cambios? (S/N): "):
                saveData(data)
                print("✓ Mesa modificada exitosamente.")
            else:
                print("✗ Cambios descartados.")
        else:
            print("✗ No se realizaron cambios.")
        
    except ValueError:
        print("✗ ID inválido.")
    
    pausarPantalla()

def eliminarTopico():
    """Elimina una mesa del sistema"""
    limpiarPantalla()
    data = loadData()
    topicos = data["topicos"]
    
    print("""
╔═══════════════════════════════════════════╗
║          ELIMINAR MESA                   ║
╚═══════════════════════════════════════════╝
""")
    
    if not topicos:
        print("\n✗ No hay mesas registradas.")
        pausarPantalla()
        return
    
    tabla = [[t["id"], t["nombre"], "Disponible" if t["disponible"] else "Ocupada"] for t in topicos]
    print(tabulate(tabla, headers=["ID", "Nombre", "Estado"], tablefmt="grid"))
    
    id_topico = inputSeguro("\nID de la mesa a eliminar: ")
    
    try:
        id_topico = int(id_topico)
        topico = next((t for t in topicos if t["id"] == id_topico), None)
        
        if not topico:
            print("✗ Mesa no encontrada.")
            pausarPantalla()
            return
        
        if not topico["disponible"]:
            print("✗ No se puede eliminar una mesa ocupada.")
            pausarPantalla()
            return
        
        if confirmarAccion(f"\n¿Eliminar '{topico['nombre']}'? (S/N): "):
            data["topicos"] = [t for t in topicos if t["id"] != id_topico]
            saveData(data)
            print("✓ Mesa eliminada exitosamente.")
        else:
            print("✗ Operación cancelada.")
        
    except ValueError:
        print("✗ ID inválido.")
    
    pausarPantalla()

def cambiarDisponibilidad():
    """Cambia el estado de disponibilidad de una mesa"""
    limpiarPantalla()
    data = loadData()
    topicos = data["topicos"]
    
    print("""
╔═══════════════════════════════════════════╗
║       CAMBIAR DISPONIBILIDAD             ║
╚═══════════════════════════════════════════╝
""")
    
    if not topicos:
        print("\n✗ No hay mesas registradas.")
        pausarPantalla()
        return
    
    tabla = [
        [t["id"], t["nombre"], "✓ Disponible" if t["disponible"] else "✗ Ocupada"]
        for t in topicos
    ]
    print(tabulate(tabla, headers=["ID", "Nombre", "Estado"], tablefmt="grid"))
    
    id_topico = inputSeguro("\nID de la mesa: ")
    
    try:
        id_topico = int(id_topico)
        topico = next((t for t in topicos if t["id"] == id_topico), None)
        
        if not topico:
            print("✗ Mesa no encontrada.")
            pausarPantalla()
            return
        
        estado_actual = "Disponible" if topico["disponible"] else "Ocupada"
        nuevo_estado = "Ocupada" if topico["disponible"] else "Disponible"
        
        if confirmarAccion(f"\nCambiar estado de '{topico['nombre']}' de {estado_actual} a {nuevo_estado}? (S/N): "):
            topico["disponible"] = not topico["disponible"]
            saveData(data)
            print(f"✓ Estado cambiado a: {nuevo_estado}")
        else:
            print("✗ Operación cancelada.")
        
    except ValueError:
        print("✗ ID inválido.")
    
    pausarPantalla()