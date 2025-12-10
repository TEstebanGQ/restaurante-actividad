from core.Storage import loadData, saveData
from ui.UIHelpers import *

CATEGORIAS = ["platillos", "bebidas", "adicionales"]

def gestionProductosMenu():
    """Menú principal de gestión de productos"""
    opciones = [
        "Ver todos los productos",
        "Agregar producto",
        "Modificar producto",
        "Eliminar producto",
        "Regresar al menú principal"
    ]
    
    acciones = {
        "1": verProductos, "2": agregarProducto,
        "3": modificarProducto, "4": eliminarProducto
    }
    
    while True:
        opcion = mostrarMenu(opciones, "GESTIÓN DE PRODUCTOS")
        if opcion == "5":
            break
        elif opcion in acciones:
            acciones[opcion]()
        else:
            mostrarMensaje("Opción inválida.", "error")
            pausarPantalla()

def verProductos():
    """Muestra todos los productos del restaurante"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("LISTADO DE PRODUCTOS")
    
    for categoria in CATEGORIAS:
        print(f"\n--- {categoria.upper()} ---")
        tabla = [[p["id"], p["nombre"], f"${p['precio']:,.0f}"] for p in data["productos"][categoria]]
        mostrarTabla(tabla, ["ID", "Nombre", "Precio"], "")
    
    pausarPantalla()

def seleccionarCategoria():
    """Selecciona una categoría de producto"""
    print("\nSeleccione el tipo de producto:")
    for i, cat in enumerate(CATEGORIAS, 1):
        print(f"{i}. {cat.capitalize()}")
    
    tipo = inputSeguro("\nTipo: ")
    if tipo in ["1", "2", "3"]:
        return CATEGORIAS[int(tipo) - 1]
    
    mostrarMensaje("Tipo inválido.", "error")
    return None

def agregarProducto():
    """Agrega un nuevo producto al menú"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("AGREGAR NUEVO PRODUCTO")
    
    categoria = seleccionarCategoria()
    if not categoria:
        pausarPantalla()
        return
    
    nombre = inputSeguro("Nombre del producto: ")
    precioStr = inputSeguro("Precio: ")
    
    if not nombre or not precioStr:
        mostrarMensaje("Operación cancelada.", "error")
        pausarPantalla()
        return
    
    precio = validarNumero(precioStr, "Precio inválido.")
    if not precio:
        pausarPantalla()
        return
    
    productosCategoria = data["productos"][categoria]
    nuevoId = max([p["id"] for p in productosCategoria], default=0) + 1
    
    if confirmarOperacion(f"¿Agregar {nombre} a {categoria} por ${precio:,.0f}?", 
                         "Producto agregado exitosamente."):
        nuevoProducto = {"id": nuevoId, "nombre": nombre, "precio": precio}
        data["productos"][categoria].append(nuevoProducto)
        saveData(data)
    
    pausarPantalla()

def modificarProducto():
    """Modifica un producto existente"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("MODIFICAR PRODUCTO")
    
    categoria = seleccionarCategoria()
    if not categoria:
        pausarPantalla()
        return
    
    productos = data["productos"][categoria]
    print(f"\n--- {categoria.upper()} ---")
    
    producto = seleccionarDeTabla(data, productos, ["ID", "Nombre", "Precio"], 
                                   "ID del producto a modificar")
    if not producto:
        pausarPantalla()
        return
    
    print(f"\nProducto actual: {producto['nombre']} - ${producto['precio']:,.0f}")
    nuevoNombre = inputSeguro(f"Nuevo nombre (Enter para mantener '{producto['nombre']}'): ")
    nuevoPrecio = inputSeguro(f"Nuevo precio (Enter para mantener {producto['precio']}): ")
    
    if nuevoNombre: producto["nombre"] = nuevoNombre
    if nuevoPrecio:
        precio = validarNumero(nuevoPrecio)
        if precio: producto["precio"] = precio
    
    if confirmarOperacion("¿Guardar cambios?", "Producto modificado exitosamente.", "Cambios descartados."):
        saveData(data)
    
    pausarPantalla()

def eliminarProducto():
    """Elimina un producto del menú"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("ELIMINAR PRODUCTO")
    
    categoria = seleccionarCategoria()
    if not categoria:
        pausarPantalla()
        return
    
    productos = data["productos"][categoria]
    print(f"\n--- {categoria.upper()} ---")
    
    producto = seleccionarDeTabla(data, productos, ["ID", "Nombre", "Precio"], 
                                   "ID del producto a eliminar")
    if not producto:
        pausarPantalla()
        return
    
    if confirmarOperacion(f"¿Eliminar '{producto['nombre']}'?", "Producto eliminado exitosamente."):
        data["productos"][categoria] = [p for p in productos if p["id"] != producto["id"]]
        saveData(data)
    
    pausarPantalla()