from core.Storage import loadData, saveData, nextIdPedido, nextIdCliente
from core.PedidosHelpers import crearPedido, actualizarEstadoPedido
from ui.UIHelpers import *
from ui.PedidosGastos import verGastosPorCliente

def gestionPedidosMenu():
    """Menú principal de gestión de pedidos"""
    opciones = [
        "Tomar pedido (Cliente llega)",
        "Ver todos los pedidos",
        "Ver pedidos activos",
        "Buscar pedido",
        "Facturar pedido",
        "Cancelar pedido",
        "Ver gastos por cliente",
        "Regresar al menú principal"
    ]
    
    acciones = {
        "1": tomarPedido, "2": verTodosPedidos, "3": verPedidosActivos,
        "4": buscarPedido, "5": facturarPedido, "6": cancelarPedido,
        "7": verGastosPorCliente
    }
    
    while True:
        opcion = mostrarMenu(opciones, "GESTIÓN DE PEDIDOS")
        if opcion == "8":
            break
        elif opcion in acciones:
            acciones[opcion]()
        else:
            mostrarMensaje("Opción inválida.", "error")
            pausarPantalla()

def tomarPedido():
    """Toma el pedido de un cliente que llega al restaurante"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("TOMAR PEDIDO")
    
    cliente = seleccionarORegistrarCliente(data)
    if not cliente:
        return
    
    data = loadData()  # Recargar datos
    mesa = seleccionarMesa(data)
    if not mesa:
        return
    
    items, total = agregarProductosAlPedido(data, cliente, mesa)
    if not items:
        return
    
    if confirmarPedidoFinal(cliente, mesa, items, total):
        guardarPedido(data, cliente["id"], cliente["nombre"], mesa["id"], mesa["nombre"], items, total)
    
    pausarPantalla()

def seleccionarORegistrarCliente(data):
    """Selecciona un cliente existente o registra uno nuevo"""
    print("\n¿El cliente está registrado?")
    print("1. Sí, buscar cliente existente")
    print("2. No, registrar nuevo cliente")
    print("3. Cliente sin nombre (anónimo)")
    
    opcion = inputSeguro("\nSeleccione una opción: ")
    
    if opcion == "1":
        return buscarClienteExistente(data)
    elif opcion == "2":
        return registrarClienteRapido(data)
    elif opcion == "3":
        return registrarClienteAnonimo(data)
    else:
        mostrarMensaje("Opción inválida.", "error")
        pausarPantalla()
        return None

def buscarClienteExistente(data):
    """Busca un cliente existente"""
    if not data["clientes"]:
        mostrarMensaje("No hay clientes registrados.", "error")
        pausarPantalla()
        return None
    
    criterio = inputSeguro("\nBuscar cliente por nombre o teléfono: ")
    if not criterio:
        return None
    
    resultados = buscarPorCriterio(data["clientes"], criterio, ["nombre", "telefono"])
    if not resultados:
        mostrarMensaje("No se encontraron clientes.", "error")
        pausarPantalla()
        return None
    
    print("\n--- CLIENTES ENCONTRADOS ---")
    return seleccionarDeTabla(data, resultados, ["ID", "Nombre", "Teléfono"], "ID del cliente")

def registrarClienteRapido(data):
    """Registra un cliente rápidamente"""
    nombre = inputSeguro("\nNombre del cliente: ")
    if not nombre:
        return None
    
    telefono = inputSeguro("Teléfono (opcional, Enter para omitir): ") or "N/A"
    nuevoId = nextIdCliente(data)
    
    cliente = {"id": nuevoId, "nombre": nombre, "telefono": telefono, "email": ""}
    data["clientes"].append(cliente)
    saveData(data)
    
    print(f"✓ Cliente {nombre} registrado con ID: {nuevoId}")
    pausarPantalla()
    return cliente

def registrarClienteAnonimo(data):
    """Registra un cliente anónimo"""
    nuevoId = nextIdCliente(data)
    cliente = {"id": nuevoId, "nombre": "Cliente Anónimo", "telefono": "N/A", "email": ""}
    data["clientes"].append(cliente)
    saveData(data)
    return cliente

def seleccionarMesa(data):
    """Selecciona una mesa disponible"""
    mesasDisponibles = [t for t in data["topicos"] if t["disponible"]]
    
    if not mesasDisponibles:
        print("\n✗ No hay mesas disponibles en este momento.")
        if confirmarAccion("¿Desea ver el pedido para llevar? (S/N): "):
            return {"id": 0, "nombre": "Para Llevar"}
        pausarPantalla()
        return None
    
    print("\n--- MESAS DISPONIBLES ---")
    tablaM = [[m["id"], m["nombre"]] for m in mesasDisponibles]
    mostrarTabla(tablaM, ["ID", "Nombre"], "")
    print("0. Para llevar (sin mesa)")
    
    idMesa = inputSeguro("\nID de la mesa (o 0 para llevar): ")
    
    try:
        idMesa = int(idMesa)
        if idMesa == 0:
            return {"id": 0, "nombre": "Para Llevar"}
        
        mesa = next((m for m in mesasDisponibles if m["id"] == idMesa), None)
        if not mesa:
            mostrarMensaje("Mesa no encontrada o no disponible.", "error")
            pausarPantalla()
            return None
        return mesa
    except ValueError:
        mostrarMensaje("ID inválido.", "error")
        pausarPantalla()
        return None

def agregarProductosAlPedido(data, cliente, mesa):
    """Agrega productos al pedido"""
    items = []
    total = 0
    
    while True:
        limpiarPantalla()
        mostrarHeader("AGREGAR PRODUCTOS")
        print(f"\nCliente: {cliente['nombre']}\nMesa: {mesa['nombre']}\nTotal actual: ${total:,.0f}")
        
        if items:
            print("\n--- ITEMS EN EL PEDIDO ---")
            tablaItems = [[i["nombre"], i["cantidad"], f"${i['precio']:,.0f}", f"${i['subtotal']:,.0f}"] 
                          for i in items]
            mostrarTabla(tablaItems, ["Producto", "Cant.", "Precio", "Subtotal"], "")
        
        print("\n1. Agregar platillo\n2. Agregar bebida\n3. Agregar adicional\n4. Finalizar pedido")
        
        opcion = inputSeguro("\nSeleccione una opción: ")
        
        if opcion == "4":
            if not items:
                mostrarMensaje("Debe agregar al menos un producto.", "error")
                pausarPantalla()
                continue
            break
        elif opcion in ["1", "2", "3"]:
            resultado = agregarProducto(data, int(opcion))
            if resultado:
                items.append(resultado)
                total += resultado["subtotal"]
                mostrarMensaje(f"{resultado['cantidad']}x {resultado['nombre']} agregado(s).", "success")
                pausarPantalla()
        else:
            mostrarMensaje("Opción inválida.", "error")
            pausarPantalla()
    
    return items, total

def agregarProducto(data, tipoOpcion):
    """Agrega un producto específico"""
    categorias = ["platillos", "bebidas", "adicionales"]
    categoria = categorias[tipoOpcion - 1]
    productos = data["productos"][categoria]
    
    print(f"\n--- {categoria.upper()} ---")
    tablaProd = [[p["id"], p["nombre"], f"${p['precio']:,.0f}"] for p in productos]
    mostrarTabla(tablaProd, ["ID", "Nombre", "Precio"], "")
    
    idProducto = inputSeguro("\nID del producto: ")
    cantidad = inputSeguro("Cantidad: ")
    
    try:
        producto = next((p for p in productos if p["id"] == int(idProducto)), None)
        if not producto:
            mostrarMensaje("Producto no encontrado.", "error")
            return None
        
        cant = int(cantidad)
        if cant <= 0:
            mostrarMensaje("La cantidad debe ser mayor a 0.", "error")
            return None
        
        return {
            "nombre": producto["nombre"],
            "precio": producto["precio"],
            "cantidad": cant,
            "subtotal": producto["precio"] * cant,
            "categoria": categoria
        }
    except ValueError:
        mostrarMensaje("Entrada inválida.", "error")
        return None

def confirmarPedidoFinal(cliente, mesa, items, total):
    """Confirma el pedido final"""
    limpiarPantalla()
    mostrarHeader("CONFIRMAR PEDIDO")
    print(f"Cliente: {cliente['nombre']}\nMesa: {mesa['nombre']}")
    print("\n--- DETALLE DEL PEDIDO ---")
    tablaItems = [[i["nombre"], i["cantidad"], f"${i['precio']:,.0f}", f"${i['subtotal']:,.0f}"] 
                  for i in items]
    mostrarTabla(tablaItems, ["Producto", "Cant.", "Precio", "Subtotal"], "")
    print(f"\n{'TOTAL A PAGAR:':.<30} ${total:,.0f}")
    
    return confirmarAccion("\n¿Confirmar pedido? (S/N): ")

def guardarPedido(data, idCliente, nombreCliente, idMesa, nombreMesa, items, total):
    """Guarda el pedido en el sistema"""
    nuevoId = nextIdPedido(data)
    nuevoPedido = crearPedido(idCliente, nombreCliente, idMesa, nombreMesa, items, total)
    nuevoPedido["id"] = nuevoId
    
    data["pedidos"].append(nuevoPedido)
    
    # Marcar mesa como ocupada
    if idMesa != 0:
        for t in data["topicos"]:
            if t["id"] == idMesa:
                t["disponible"] = False
                break
    
    saveData(data)
    print(f"\n✓ Pedido {nuevoId} tomado exitosamente.")
    print(f"✓ Total del pedido: ${total:,.0f}")
    print(f"✓ Cliente: {nombreCliente}")

def verTodosPedidos():
    """Muestra todos los pedidos"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("TODOS LOS PEDIDOS")
    
    if not data["pedidos"]:
        mostrarMensaje("No hay pedidos registrados.", "error")
    else:
        tabla = [[p["id"], p["nombre_cliente"], p["nombre_mesa"], f"${p['total']:,.0f}", 
                  p["estado"].upper(), p["fecha"]] for p in data["pedidos"]]
        mostrarTabla(tabla, ["ID", "Cliente", "Mesa", "Total", "Estado", "Fecha"])
    
    pausarPantalla()

def verPedidosActivos():
    """Muestra solo los pedidos activos"""
    limpiarPantalla()
    data = loadData()
    pedidosActivos = [p for p in data["pedidos"] if p["estado"] == "activo"]
    mostrarHeader("PEDIDOS ACTIVOS")
    
    if not pedidosActivos:
        mostrarMensaje("No hay pedidos activos.", "error")
    else:
        tabla = [[p["id"], p["nombre_cliente"], p["nombre_mesa"], f"${p['total']:,.0f}", p["fecha"]] 
                 for p in pedidosActivos]
        mostrarTabla(tabla, ["ID", "Cliente", "Mesa", "Total", "Fecha"])
    
    pausarPantalla()

def buscarPedido():
    """Busca y muestra el detalle de un pedido"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("BUSCAR PEDIDO")
    
    idPedido = inputSeguro("ID del pedido: ")
    pedido = next((p for p in data["pedidos"] if p["id"] == idPedido), None)
    
    if not pedido:
        mostrarMensaje("Pedido no encontrado.", "error")
    else:
        limpiarPantalla()
        mostrarHeader("DETALLE DEL PEDIDO")
        print(f"\nID Pedido: {pedido['id']}\nCliente: {pedido['nombre_cliente']}")
        print(f"Mesa: {pedido['nombre_mesa']}\nFecha: {pedido['fecha']}")
        print(f"Estado: {pedido['estado'].upper()}")
        
        print("\n--- ITEMS DEL PEDIDO ---")
        tablaItems = [[i["nombre"], i["cantidad"], f"${i['precio']:,.0f}", f"${i['subtotal']:,.0f}"] 
                      for i in pedido["items"]]
        mostrarTabla(tablaItems, ["Producto", "Cant.", "Precio", "Subtotal"], "")
        print(f"\n{'TOTAL:':.<30} ${pedido['total']:,.0f}")
    
    pausarPantalla()

def facturarPedido():
    """Factura y cierra un pedido"""
    limpiarPantalla()
    data = loadData()
    pedidosActivos = [p for p in data["pedidos"] if p["estado"] == "activo"]
    mostrarHeader("FACTURAR PEDIDO")
    
    if not pedidosActivos:
        mostrarMensaje("No hay pedidos activos para facturar.", "error")
        pausarPantalla()
        return
    
    tabla = [[p["id"], p["nombre_cliente"], p["nombre_mesa"], f"${p['total']:,.0f}"] 
             for p in pedidosActivos]
    mostrarTabla(tabla, ["ID", "Cliente", "Mesa", "Total"])
    
    idPedido = inputSeguro("\nID del pedido a facturar: ")
    pedido = next((p for p in data["pedidos"] if p["id"] == idPedido and p["estado"] == "activo"), None)
    
    if not pedido:
        mostrarMensaje("Pedido no encontrado o ya está facturado.", "error")
        pausarPantalla()
        return
    
    limpiarPantalla()
    mostrarHeader(f"FACTURA - PEDIDO {pedido['id']}")
    print(f"\nCliente: {pedido['nombre_cliente']}\nMesa: {pedido['nombre_mesa']}\nFecha: {pedido['fecha']}")
    
    print("\n--- DETALLE ---")
    tablaItems = [[i["nombre"], i["cantidad"], f"${i['precio']:,.0f}", f"${i['subtotal']:,.0f}"] 
                  for i in pedido["items"]]
    mostrarTabla(tablaItems, ["Producto", "Cant.", "Precio", "Subtotal"], "")
    print(f"\n{'TOTAL A PAGAR:':.<30} ${pedido['total']:,.0f}")
    
    if confirmarAccion("\n¿Confirmar pago? (S/N): "):
        actualizarEstadoPedido(data, idPedido, "facturado")
        saveData(data)
        mostrarMensaje("Pedido facturado exitosamente.", "success")
        print(f"✓ Mesa '{pedido['nombre_mesa']}' liberada.")
    else:
        mostrarMensaje("Operación cancelada.", "error")
    
    pausarPantalla()

def cancelarPedido():
    """Cancela un pedido activo"""
    limpiarPantalla()
    data = loadData()
    pedidosActivos = [p for p in data["pedidos"] if p["estado"] == "activo"]
    mostrarHeader("CANCELAR PEDIDO")
    
    if not pedidosActivos:
        mostrarMensaje("No hay pedidos activos para cancelar.", "error")
        pausarPantalla()
        return
    
    tabla = [[p["id"], p["nombre_cliente"], p["nombre_mesa"], f"${p['total']:,.0f}"] 
             for p in pedidosActivos]
    mostrarTabla(tabla, ["ID", "Cliente", "Mesa", "Total"])
    
    idPedido = inputSeguro("\nID del pedido a cancelar: ")
    pedido = next((p for p in data["pedidos"] if p["id"] == idPedido and p["estado"] == "activo"), None)
    
    if not pedido:
        mostrarMensaje("Pedido no encontrado o no está activo.", "error")
        pausarPantalla()
        return
    
    if confirmarAccion(f"\n¿Cancelar pedido {idPedido} de {pedido['nombre_cliente']}? (S/N): "):
        actualizarEstadoPedido(data, idPedido, "cancelado")
        saveData(data)
        mostrarMensaje("Pedido cancelado exitosamente.", "success")
        print(f"✓ Mesa '{pedido['nombre_mesa']}' liberada.")
    else:
        mostrarMensaje("Operación cancelada.", "error")
    
    pausarPantalla()