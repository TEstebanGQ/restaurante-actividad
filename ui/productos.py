from ui.prompts import inputSeguro, confirmarAccion
from utils.screenControllers import limpiarPantalla, pausarPantalla
from core.storage import loadData, saveData
from tabulate import tabulate

def gestionProductosMenu():
    """Menú principal de gestión de productos"""
    while True:
        limpiarPantalla()
        print("""
╔═══════════════════════════════════════════╗
║        GESTIÓN DE PRODUCTOS              ║
╚═══════════════════════════════════════════╝

1. Ver todos los productos
2. Agregar producto
3. Modificar producto
4. Eliminar producto
5. Regresar al menú principal

═══════════════════════════════════════════
""")
        
        opcion = inputSeguro("Seleccione una opción: ")
        
        if opcion == "1":
            verProductos()
        elif opcion == "2":
            agregarProducto()
        elif opcion == "3":
            modificarProducto()
        elif opcion == "4":
            eliminarProducto()
        elif opcion == "5":
            break
        else:
            print("✗ Opción inválida.")
            pausarPantalla()

def verProductos():
    """Muestra todos los productos del restaurante"""
    limpiarPantalla()
    data = loadData()
    productos = data["productos"]
    
    print("""
╔═══════════════════════════════════════════╗
║           LISTADO DE PRODUCTOS           ║
╚═══════════════════════════════════════════╝
""")
    
    print("\n--- PLATILLOS ---")
    tabla_platillos = [
        [p["id"], p["nombre"], f"${p['precio']:,.0f}"]
        for p in productos["platillos"]
    ]
    print(tabulate(tabla_platillos, headers=["ID", "Nombre", "Precio"], tablefmt="grid"))
    
    print("\n--- BEBIDAS ---")
    tabla_bebidas = [
        [b["id"], b["nombre"], f"${b['precio']:,.0f}"]
        for b in productos["bebidas"]
    ]
    print(tabulate(tabla_bebidas, headers=["ID", "Nombre", "Precio"], tablefmt="grid"))
    
    print("\n--- ADICIONALES ---")
    tabla_adicionales = [
        [a["id"], a["nombre"], f"${a['precio']:,.0f}"]
        for a in productos["adicionales"]
    ]
    print(tabulate(tabla_adicionales, headers=["ID", "Nombre", "Precio"], tablefmt="grid"))
    
    pausarPantalla()

def agregarProducto():
    """Agrega un nuevo producto al menú"""
    limpiarPantalla()
    data = loadData()
    
    print("""
╔═══════════════════════════════════════════╗
║          AGREGAR NUEVO PRODUCTO          ║
╚═══════════════════════════════════════════╝
""")
    
    print("\nSeleccione el tipo de producto:")
    print("1. Platillo")
    print("2. Bebida")
    print("3. Adicional")
    
    tipo = inputSeguro("\nTipo: ")
    
    if tipo not in ["1", "2", "3"]:
        print("✗ Tipo inválido.")
        pausarPantalla()
        return
    
    nombre = inputSeguro("Nombre del producto: ")
    if not nombre:
        print("✗ Operación cancelada.")
        pausarPantalla()
        return
    
    precio = inputSeguro("Precio: ")
    if not precio:
        print("✗ Operación cancelada.")
        pausarPantalla()
        return
    
    try:
        precio = float(precio)
        if precio <= 0:
            print("✗ El precio debe ser mayor a 0.")
            pausarPantalla()
            return
    except ValueError:
        print("✗ Precio inválido.")
        pausarPantalla()
        return
    
    # Determinar categoría y siguiente ID
    if tipo == "1":
        categoria = "platillos"
    elif tipo == "2":
        categoria = "bebidas"
    else:
        categoria = "adicionales"
    
    productos_categoria = data["productos"][categoria]
    nuevo_id = max([p["id"] for p in productos_categoria], default=0) + 1
    
    nuevo_producto = {
        "id": nuevo_id,
        "nombre": nombre,
        "precio": precio
    }
    
    if confirmarAccion(f"\n¿Agregar {nombre} a {categoria} por ${precio:,.0f}? (S/N): "):
        data["productos"][categoria].append(nuevo_producto)
        saveData(data)
        print("✓ Producto agregado exitosamente.")
    else:
        print("✗ Operación cancelada.")
    
    pausarPantalla()

def modificarProducto():
    """Modifica un producto existente"""
    limpiarPantalla()
    data = loadData()
    
    print("""
╔═══════════════════════════════════════════╗
║          MODIFICAR PRODUCTO              ║
╚═══════════════════════════════════════════╝
""")
    
    print("\nSeleccione el tipo de producto:")
    print("1. Platillo")
    print("2. Bebida")
    print("3. Adicional")
    
    tipo = inputSeguro("\nTipo: ")
    
    if tipo not in ["1", "2", "3"]:
        print("✗ Tipo inválido.")
        pausarPantalla()
        return
    
    categoria = ["platillos", "bebidas", "adicionales"][int(tipo) - 1]
    productos = data["productos"][categoria]
    
    if not productos:
        print(f"✗ No hay productos en {categoria}.")
        pausarPantalla()
        return
    
    print(f"\n--- {categoria.upper()} ---")
    tabla = [[p["id"], p["nombre"], f"${p['precio']:,.0f}"] for p in productos]
    print(tabulate(tabla, headers=["ID", "Nombre", "Precio"], tablefmt="grid"))
    
    id_producto = inputSeguro("\nID del producto a modificar: ")
    
    try:
        id_producto = int(id_producto)
        producto = next((p for p in productos if p["id"] == id_producto), None)
        
        if not producto:
            print("✗ Producto no encontrado.")
            pausarPantalla()
            return
        
        print(f"\nProducto actual: {producto['nombre']} - ${producto['precio']:,.0f}")
        
        nuevo_nombre = inputSeguro(f"Nuevo nombre (Enter para mantener '{producto['nombre']}'): ")
        nuevo_precio = inputSeguro(f"Nuevo precio (Enter para mantener {producto['precio']}): ")
        
        if nuevo_nombre:
            producto["nombre"] = nuevo_nombre
        
        if nuevo_precio:
            try:
                producto["precio"] = float(nuevo_precio)
            except ValueError:
                print("✗ Precio inválido, se mantiene el anterior.")
        
        if confirmarAccion("\n¿Guardar cambios? (S/N): "):
            saveData(data)
            print("✓ Producto modificado exitosamente.")
        else:
            print("✗ Cambios descartados.")
        
    except ValueError:
        print("✗ ID inválido.")
    
    pausarPantalla()

def eliminarProducto():
    """Elimina un producto del menú"""
    limpiarPantalla()
    data = loadData()
    
    print("""
╔═══════════════════════════════════════════╗
║          ELIMINAR PRODUCTO               ║
╚═══════════════════════════════════════════╝
""")
    
    print("\nSeleccione el tipo de producto:")
    print("1. Platillo")
    print("2. Bebida")
    print("3. Adicional")
    
    tipo = inputSeguro("\nTipo: ")
    
    if tipo not in ["1", "2", "3"]:
        print("✗ Tipo inválido.")
        pausarPantalla()
        return
    
    categoria = ["platillos", "bebidas", "adicionales"][int(tipo) - 1]
    productos = data["productos"][categoria]
    
    if not productos:
        print(f"✗ No hay productos en {categoria}.")
        pausarPantalla()
        return
    
    print(f"\n--- {categoria.upper()} ---")
    tabla = [[p["id"], p["nombre"], f"${p['precio']:,.0f}"] for p in productos]
    print(tabulate(tabla, headers=["ID", "Nombre", "Precio"], tablefmt="grid"))
    
    id_producto = inputSeguro("\nID del producto a eliminar: ")
    
    try:
        id_producto = int(id_producto)
        producto = next((p for p in productos if p["id"] == id_producto), None)
        
        if not producto:
            print("✗ Producto no encontrado.")
            pausarPantalla()
            return
        
        if confirmarAccion(f"\n¿Eliminar '{producto['nombre']}'? (S/N): "):
            data["productos"][categoria] = [p for p in productos if p["id"] != id_producto]
            saveData(data)
            print("✓ Producto eliminado exitosamente.")
        else:
            print("✗ Operación cancelada.")
        
    except ValueError:
        print("✗ ID inválido.")
    
    pausarPantalla()