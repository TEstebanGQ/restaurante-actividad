from ui.prompts import inputSeguro, confirmarAccion
from utils.screenControllers import limpiarPantalla, pausarPantalla
from core.storage import loadData, saveData, nextIdPedido
from tabulate import tabulate
from datetime import datetime

def gestionPedidosMenu():
    """Menú principal de gestión de pedidos"""
    while True:
        limpiarPantalla()
        print("""
╔═══════════════════════════════════════════╗
║         GESTIÓN DE PEDIDOS               ║
╚═══════════════════════════════════════════╝

1. Tomar pedido (Cliente llega)
2. Ver todos los pedidos
3. Ver pedidos activos
4. Buscar pedido
5. Facturar pedido
6. Cancelar pedido
7. Ver gastos por cliente
8. Regresar al menú principal

═══════════════════════════════════════════
""")
        
        opcion = inputSeguro("Seleccione una opción: ")
        
        if opcion == "1":
            tomarPedido()
        elif opcion == "2":
            verTodosPedidos()
        elif opcion == "3":
            verPedidosActivos()
        elif opcion == "4":
            buscarPedido()
        elif opcion == "5":
            facturarPedido()
        elif opcion == "6":
            cancelarPedido()
        elif opcion == "7":
            verGastosPorCliente()
        elif opcion == "8":
            break
        else:
            print("✗ Opción inválida.")
            pausarPantalla()

def verGastosPorCliente():
    """Muestra el historial de gastos de un cliente"""
    limpiarPantalla()
    data = loadData()
    
    print("""
╔═══════════════════════════════════════════╗
║       GASTOS POR CLIENTE                 ║
╚═══════════════════════════════════════════╝
""")
    
    if not data["clientes"]:
        print("\n✗ No hay clientes registrados.")
        pausarPantalla()
        return
    
    print("\n¿Cómo desea consultar?")
    print("1. Ver gastos de un cliente específico")
    print("2. Ver ranking de clientes (mayor a menor gasto)")
    print("3. Ver todos los clientes con sus gastos")
    
    opcion = inputSeguro("\nSeleccione una opción: ")
    
    if opcion == "1":
        verGastosClienteEspecifico(data)
    elif opcion == "2":
        verRankingClientes(data)
    elif opcion == "3":
        verTodosClientesGastos(data)
    else:
        print("✗ Opción inválida.")
        pausarPantalla()

def verGastosClienteEspecifico(data):
    """Ver gastos detallados de un cliente"""
    limpiarPantalla()
    
    print("""
╔═══════════════════════════════════════════╗
║    GASTOS DE CLIENTE ESPECÍFICO          ║
╚═══════════════════════════════════════════╝
""")
    
    criterio = inputSeguro("\nBuscar cliente por nombre o teléfono: ")
    if not criterio:
        return
    
    criterio = criterio.lower()
    resultados = [
        c for c in data["clientes"] 
        if criterio in c["nombre"].lower() or criterio in c.get("telefono", "").lower()
    ]
    
    if not resultados:
        print("✗ No se encontraron clientes.")
        pausarPantalla()
        return
    
    print("\n--- CLIENTES ENCONTRADOS ---")
    tabla = [[c["id"], c["nombre"], c["telefono"]] for c in resultados]
    print(tabulate(tabla, headers=["ID", "Nombre", "Teléfono"], tablefmt="grid"))
    
    id_cliente = inputSeguro("\nID del cliente: ")
    cliente = next((c for c in resultados if c["id"] == id_cliente), None)
    
    if not cliente:
        print("✗ Cliente no seleccionado.")
        pausarPantalla()
        return
    
    # Obtener pedidos del cliente
    pedidos_cliente = [p for p in data["pedidos"] if p["id_cliente"] == id_cliente]
    
    limpiarPantalla()
    print(f"""
╔═══════════════════════════════════════════╗
║    HISTORIAL DE GASTOS                   ║
╚═══════════════════════════════════════════╝

Cliente: {cliente['nombre']}
Teléfono: {cliente.get('telefono', 'N/A')}
""")
    
    if not pedidos_cliente:
        print("\n✗ Este cliente no tiene pedidos registrados.")
        pausarPantalla()
        return
    
    # Mostrar pedidos
    print("\n--- PEDIDOS REALIZADOS ---")
    tabla_pedidos = [
        [
            p["id"],
            p["nombre_mesa"],
            p["fecha"],
            p["estado"].upper(),
            f"${p['total']:,.0f}"
        ]
        for p in pedidos_cliente
    ]
    print(tabulate(tabla_pedidos, headers=["ID Pedido", "Mesa", "Fecha", "Estado", "Total"], tablefmt="grid"))
    
    # Calcular estadísticas
    total_gastado = sum(p["total"] for p in pedidos_cliente)
    pedidos_facturados = [p for p in pedidos_cliente if p["estado"] == "facturado"]
    pedidos_activos = [p for p in pedidos_cliente if p["estado"] == "activo"]
    pedidos_cancelados = [p for p in pedidos_cliente if p["estado"] == "cancelado"]
    
    total_facturado = sum(p["total"] for p in pedidos_facturados)
    total_pendiente = sum(p["total"] for p in pedidos_activos)
    
    print(f"""
═══════════════════════════════════════════
RESUMEN:
  • Total de pedidos: {len(pedidos_cliente)}
  • Pedidos pagados: {len(pedidos_facturados)}
  • Pedidos activos: {len(pedidos_activos)}
  • Pedidos cancelados: {len(pedidos_cancelados)}

GASTOS:
  • Total gastado (pagado): ${total_facturado:,.0f}
  • Total pendiente: ${total_pendiente:,.0f}
  • Total general: ${total_gastado:,.0f}
═══════════════════════════════════════════
""")
    
    # Mostrar productos más pedidos por este cliente
    productos_count = {}
    for pedido in pedidos_cliente:
        for item in pedido["items"]:
            nombre = item["nombre"]
            if nombre in productos_count:
                productos_count[nombre]["cantidad"] += item["cantidad"]
                productos_count[nombre]["total"] += item["subtotal"]
            else:
                productos_count[nombre] = {
                    "cantidad": item["cantidad"],
                    "total": item["subtotal"]
                }
    
    if productos_count:
        print("\n--- PRODUCTOS MÁS PEDIDOS ---")
        productos_ordenados = sorted(productos_count.items(), key=lambda x: x[1]["cantidad"], reverse=True)[:5]
        tabla_productos = [
            [nombre, f"{datos['cantidad']}x", f"${datos['total']:,.0f}"]
            for nombre, datos in productos_ordenados
        ]
        print(tabulate(tabla_productos, headers=["Producto", "Cantidad", "Total"], tablefmt="grid"))
    
    pausarPantalla()

def verRankingClientes(data):
    """Muestra ranking de clientes por gasto total"""
    limpiarPantalla()
    
    print("""
╔═══════════════════════════════════════════╗
║    RANKING DE CLIENTES                   ║
╚═══════════════════════════════════════════╝
""")
    
    # Calcular gastos por cliente
    gastos_clientes = {}
    
    for cliente in data["clientes"]:
        pedidos = [p for p in data["pedidos"] if p["id_cliente"] == cliente["id"]]
        total_pagado = sum(p["total"] for p in pedidos if p["estado"] == "facturado")
        
        if total_pagado > 0:  # Solo clientes que han pagado
            gastos_clientes[cliente["id"]] = {
                "nombre": cliente["nombre"],
                "telefono": cliente.get("telefono", "N/A"),
                "pedidos": len([p for p in pedidos if p["estado"] == "facturado"]),
                "total": total_pagado
            }
    
    if not gastos_clientes:
        print("\n✗ No hay clientes con pedidos facturados.")
        pausarPantalla()
        return
    
    # Ordenar por total gastado
    ranking = sorted(gastos_clientes.items(), key=lambda x: x[1]["total"], reverse=True)
    
    print("\n--- TOP CLIENTES POR GASTO ---")
    tabla_ranking = [
        [
            idx + 1,
            datos["nombre"],
            datos["telefono"],
            datos["pedidos"],
            f"${datos['total']:,.0f}"
        ]
        for idx, (id_cliente, datos) in enumerate(ranking)
    ]
    print(tabulate(tabla_ranking, headers=["#", "Cliente", "Teléfono", "Pedidos", "Total Gastado"], tablefmt="grid"))
    
    # Estadísticas generales
    total_general = sum(datos["total"] for _, datos in ranking)
    promedio = total_general / len(ranking) if ranking else 0
    
    print(f"""
═══════════════════════════════════════════
ESTADÍSTICAS:
  • Total de clientes activos: {len(ranking)}
  • Gasto total acumulado: ${total_general:,.0f}
  • Gasto promedio por cliente: ${promedio:,.0f}
═══════════════════════════════════════════
""")
    
    pausarPantalla()

def verTodosClientesGastos(data):
    """Muestra todos los clientes con sus gastos"""
    limpiarPantalla()
    
    print("""
╔═══════════════════════════════════════════╗
║    TODOS LOS CLIENTES Y SUS GASTOS       ║
╚═══════════════════════════════════════════╝
""")
    
    if not data["clientes"]:
        print("\n✗ No hay clientes registrados.")
        pausarPantalla()
        return
    
    # Calcular info para cada cliente
    info_clientes = []
    
    for cliente in data["clientes"]:
        pedidos = [p for p in data["pedidos"] if p["id_cliente"] == cliente["id"]]
        pedidos_facturados = [p for p in pedidos if p["estado"] == "facturado"]
        pedidos_activos = [p for p in pedidos if p["estado"] == "activo"]
        
        total_gastado = sum(p["total"] for p in pedidos_facturados)
        total_pendiente = sum(p["total"] for p in pedidos_activos)
        
        info_clientes.append({
            "id": cliente["id"],
            "nombre": cliente["nombre"],
            "pedidos_total": len(pedidos),
            "pedidos_pagados": len(pedidos_facturados),
            "total_gastado": total_gastado,
            "total_pendiente": total_pendiente
        })
    
    # Ordenar por total gastado
    info_clientes.sort(key=lambda x: x["total_gastado"], reverse=True)
    
    tabla = [
        [
            c["id"],
            c["nombre"],
            c["pedidos_total"],
            c["pedidos_pagados"],
            f"${c['total_gastado']:,.0f}",
            f"${c['total_pendiente']:,.0f}" if c['total_pendiente'] > 0 else "-"
        ]
        for c in info_clientes
    ]
    
    print(tabulate(tabla, headers=["ID", "Cliente", "Pedidos", "Pagados", "Total Gastado", "Pendiente"], tablefmt="grid"))
    
    pausarPantalla()

def tomarPedido():
    """Toma el pedido de un cliente que llega al restaurante"""
    limpiarPantalla()
    data = loadData()
    
    print("""
╔═══════════════════════════════════════════╗
║          TOMAR PEDIDO                    ║
╚═══════════════════════════════════════════╝
""")
    
    # Registrar cliente (nuevo o existente)
    print("\n¿El cliente está registrado?")
    print("1. Sí, buscar cliente existente")
    print("2. No, registrar nuevo cliente")
    print("3. Cliente sin nombre (anónimo)")
    
    opcion = inputSeguro("\nSeleccione una opción: ")
    
    cliente = None
    
    if opcion == "1":
        # Buscar cliente existente
        if not data["clientes"]:
            print("✗ No hay clientes registrados.")
            pausarPantalla()
            return
        
        criterio = inputSeguro("\nBuscar cliente por nombre o teléfono: ")
        if not criterio:
            return
        
        criterio = criterio.lower()
        resultados = [
            c for c in data["clientes"] 
            if criterio in c["nombre"].lower() or criterio in c["telefono"]
        ]
        
        if not resultados:
            print("✗ No se encontraron clientes.")
            pausarPantalla()
            return
        
        print("\n--- CLIENTES ENCONTRADOS ---")
        tabla = [[c["id"], c["nombre"], c["telefono"]] for c in resultados]
        print(tabulate(tabla, headers=["ID", "Nombre", "Teléfono"], tablefmt="grid"))
        
        id_cliente = inputSeguro("\nID del cliente: ")
        cliente = next((c for c in resultados if c["id"] == id_cliente), None)
        
        if not cliente:
            print("✗ Cliente no seleccionado.")
            pausarPantalla()
            return
    
    elif opcion == "2":
        # Registrar nuevo cliente rápido
        nombre = inputSeguro("\nNombre del cliente: ")
        if not nombre:
            return
        
        telefono = inputSeguro("Teléfono (opcional, Enter para omitir): ")
        if telefono is None:
            telefono = "N/A"
        
        from core.storage import nextIdCliente
        nuevo_id = nextIdCliente(data)
        
        cliente = {
            "id": nuevo_id,
            "nombre": nombre,
            "telefono": telefono,
            "email": ""
        }
        
        data["clientes"].append(cliente)
        saveData(data)
        print(f"✓ Cliente {nombre} registrado con ID: {nuevo_id}")
        pausarPantalla()
    
    elif opcion == "3":
        # Cliente anónimo
        from core.storage import nextIdCliente
        nuevo_id = nextIdCliente(data)
        
        cliente = {
            "id": nuevo_id,
            "nombre": "Cliente Anónimo",
            "telefono": "N/A",
            "email": ""
        }
        
        data["clientes"].append(cliente)
        saveData(data)
    
    else:
        print("✗ Opción inválida.")
        pausarPantalla()
        return
    
    if not cliente:
        print("✗ Error al obtener cliente.")
        pausarPantalla()
        return
    
    # Recargar datos después de posible registro
    data = loadData()
    
    # Seleccionar mesa
    mesas_disponibles = [t for t in data["topicos"] if t["disponible"]]
    
    if not mesas_disponibles:
        print("\n✗ No hay mesas disponibles en este momento.")
        if confirmarAccion("¿Desea ver el pedido para llevar? (S/N): "):
            # Pedido para llevar (sin mesa)
            mesa = {"id": 0, "nombre": "Para Llevar"}
            id_mesa = 0
        else:
            pausarPantalla()
            return
    else:
        print("\n--- MESAS DISPONIBLES ---")
        tabla_mesas = [[m["id"], m["nombre"]] for m in mesas_disponibles]
        print(tabulate(tabla_mesas, headers=["ID", "Nombre"], tablefmt="grid"))
        print("0. Para llevar (sin mesa)")
        
        id_mesa = inputSeguro("\nID de la mesa (o 0 para llevar): ")
        
        try:
            id_mesa = int(id_mesa)
            
            if id_mesa == 0:
                mesa = {"id": 0, "nombre": "Para Llevar"}
            else:
                mesa = next((m for m in mesas_disponibles if m["id"] == id_mesa), None)
                
                if not mesa:
                    print("✗ Mesa no encontrada o no disponible.")
                    pausarPantalla()
                    return
        except ValueError:
            print("✗ ID inválido.")
            pausarPantalla()
            return
    
    # Agregar productos al pedido
    items_pedido = []
    total = 0
    
    while True:
        limpiarPantalla()
        print(f"""
╔═══════════════════════════════════════════╗
║          AGREGAR PRODUCTOS               ║
╚═══════════════════════════════════════════╝

Cliente: {cliente['nombre']}
Mesa: {mesa['nombre']}
Total actual: ${total:,.0f}
""")
        
        if items_pedido:
            print("\n--- ITEMS EN EL PEDIDO ---")
            tabla_items = [
                [i["nombre"], i["cantidad"], f"${i['precio']:,.0f}", f"${i['subtotal']:,.0f}"]
                for i in items_pedido
            ]
            print(tabulate(tabla_items, headers=["Producto", "Cant.", "Precio", "Subtotal"], tablefmt="grid"))
        
        print("\n1. Agregar platillo")
        print("2. Agregar bebida")
        print("3. Agregar adicional")
        print("4. Finalizar pedido")
        
        opcion = inputSeguro("\nSeleccione una opción: ")
        
        if opcion == "4":
            if not items_pedido:
                print("✗ Debe agregar al menos un producto.")
                pausarPantalla()
                continue
            break
        elif opcion in ["1", "2", "3"]:
            categoria = ["platillos", "bebidas", "adicionales"][int(opcion) - 1]
            productos = data["productos"][categoria]
            
            print(f"\n--- {categoria.upper()} ---")
            tabla_prod = [[p["id"], p["nombre"], f"${p['precio']:,.0f}"] for p in productos]
            print(tabulate(tabla_prod, headers=["ID", "Nombre", "Precio"], tablefmt="grid"))
            
            id_producto = inputSeguro("\nID del producto: ")
            
            try:
                id_producto = int(id_producto)
                producto = next((p for p in productos if p["id"] == id_producto), None)
                
                if not producto:
                    print("✗ Producto no encontrado.")
                    pausarPantalla()
                    continue
                
                cantidad = inputSeguro("Cantidad: ")
                cantidad = int(cantidad)
                
                if cantidad <= 0:
                    print("✗ La cantidad debe ser mayor a 0.")
                    pausarPantalla()
                    continue
                
                subtotal = producto["precio"] * cantidad
                
                items_pedido.append({
                    "nombre": producto["nombre"],
                    "precio": producto["precio"],
                    "cantidad": cantidad,
                    "subtotal": subtotal,
                    "categoria": categoria
                })
                
                total += subtotal
                print(f"✓ {cantidad}x {producto['nombre']} agregado(s).")
                pausarPantalla()
                
            except ValueError:
                print("✗ Entrada inválida.")
                pausarPantalla()
        else:
            print("✗ Opción inválida.")
            pausarPantalla()
    
    # Confirmar pedido
    limpiarPantalla()
    print("""
╔═══════════════════════════════════════════╗
║          CONFIRMAR PEDIDO                ║
╚═══════════════════════════════════════════╝
""")
    
    print(f"Cliente: {cliente['nombre']}")
    print(f"Mesa: {mesa['nombre']}")
    print("\n--- DETALLE DEL PEDIDO ---")
    tabla_items = [
        [i["nombre"], i["cantidad"], f"${i['precio']:,.0f}", f"${i['subtotal']:,.0f}"]
        for i in items_pedido
    ]
    print(tabulate(tabla_items, headers=["Producto", "Cant.", "Precio", "Subtotal"], tablefmt="grid"))
    print(f"\n{'TOTAL A PAGAR:':.<30} ${total:,.0f}")
    
    if confirmarAccion("\n¿Confirmar pedido? (S/N): "):
        nuevo_id = nextIdPedido(data)
        
        nuevo_pedido = {
            "id": nuevo_id,
            "id_cliente": id_cliente,
            "nombre_cliente": cliente["nombre"],
            "id_mesa": id_mesa,
            "nombre_mesa": mesa["nombre"],
            "items": items_pedido,
            "total": total,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "estado": "activo"
        }
        
        data["pedidos"].append(nuevo_pedido)
        
        # Marcar mesa como ocupada (solo si no es para llevar)
        if id_mesa != 0:
            for t in data["topicos"]:
                if t["id"] == id_mesa:
                    t["disponible"] = False
                    break
        
        saveData(data)
        
        print(f"\n✓ Pedido {nuevo_id} tomado exitosamente.")
        print(f"✓ Total del pedido: ${total:,.0f}")
        print(f"✓ Cliente: {cliente['nombre']}")
    else:
        print("✗ Pedido cancelado.")
    
    pausarPantalla()

def verTodosPedidos():
    """Muestra todos los pedidos"""
    limpiarPantalla()
    data = loadData()
    pedidos = data["pedidos"]
    
    print("""
╔═══════════════════════════════════════════╗
║          TODOS LOS PEDIDOS               ║
╚═══════════════════════════════════════════╝
""")
    
    if not pedidos:
        print("\n✗ No hay pedidos registrados.")
        pausarPantalla()
        return
    
    tabla = [
        [
            p["id"],
            p["nombre_cliente"],
            p["nombre_mesa"],
            f"${p['total']:,.0f}",
            p["estado"].upper(),
            p["fecha"]
        ]
        for p in pedidos
    ]
    print(tabulate(tabla, headers=["ID", "Cliente", "Mesa", "Total", "Estado", "Fecha"], tablefmt="grid"))
    
    pausarPantalla()

def verPedidosActivos():
    """Muestra solo los pedidos activos"""
    limpiarPantalla()
    data = loadData()
    pedidos_activos = [p for p in data["pedidos"] if p["estado"] == "activo"]
    
    print("""
╔═══════════════════════════════════════════╗
║         PEDIDOS ACTIVOS                  ║
╚═══════════════════════════════════════════╝
""")
    
    if not pedidos_activos:
        print("\n✗ No hay pedidos activos.")
        pausarPantalla()
        return
    
    tabla = [
        [
            p["id"],
            p["nombre_cliente"],
            p["nombre_mesa"],
            f"${p['total']:,.0f}",
            p["fecha"]
        ]
        for p in pedidos_activos
    ]
    print(tabulate(tabla, headers=["ID", "Cliente", "Mesa", "Total", "Fecha"], tablefmt="grid"))
    
    pausarPantalla()

def buscarPedido():
    """Busca y muestra el detalle de un pedido"""
    limpiarPantalla()
    data = loadData()
    
    print("""
╔═══════════════════════════════════════════╗
║          BUSCAR PEDIDO                   ║
╚═══════════════════════════════════════════╝
""")
    
    id_pedido = inputSeguro("ID del pedido: ")
    
    pedido = next((p for p in data["pedidos"] if p["id"] == id_pedido), None)
    
    if not pedido:
        print("✗ Pedido no encontrado.")
        pausarPantalla()
        return
    
    limpiarPantalla()
    print(f"""
╔═══════════════════════════════════════════╗
║          DETALLE DEL PEDIDO              ║
╚═══════════════════════════════════════════╝

ID Pedido: {pedido['id']}
Cliente: {pedido['nombre_cliente']}
Mesa: {pedido['nombre_mesa']}
Fecha: {pedido['fecha']}
Estado: {pedido['estado'].upper()}
""")
    
    print("\n--- ITEMS DEL PEDIDO ---")
    tabla_items = [
        [i["nombre"], i["cantidad"], f"${i['precio']:,.0f}", f"${i['subtotal']:,.0f}"]
        for i in pedido["items"]
    ]
    print(tabulate(tabla_items, headers=["Producto", "Cant.", "Precio", "Subtotal"], tablefmt="grid"))
    print(f"\n{'TOTAL:':.<30} ${pedido['total']:,.0f}")
    
    pausarPantalla()

def facturarPedido():
    """Factura y cierra un pedido"""
    limpiarPantalla()
    data = loadData()
    pedidos_activos = [p for p in data["pedidos"] if p["estado"] == "activo"]
    
    print("""
╔═══════════════════════════════════════════╗
║          FACTURAR PEDIDO                 ║
╚═══════════════════════════════════════════╝
""")
    
    if not pedidos_activos:
        print("\n✗ No hay pedidos activos para facturar.")
        pausarPantalla()
        return
    
    tabla = [
        [p["id"], p["nombre_cliente"], p["nombre_mesa"], f"${p['total']:,.0f}"]
        for p in pedidos_activos
    ]
    print(tabulate(tabla, headers=["ID", "Cliente", "Mesa", "Total"], tablefmt="grid"))
    
    id_pedido = inputSeguro("\nID del pedido a facturar: ")
    
    pedido = next((p for p in data["pedidos"] if p["id"] == id_pedido and p["estado"] == "activo"), None)
    
    if not pedido:
        print("✗ Pedido no encontrado o ya está facturado.")
        pausarPantalla()
        return
    
    # Mostrar detalle
    limpiarPantalla()
    print(f"""
╔═══════════════════════════════════════════╗
║          FACTURA - PEDIDO {pedido['id']}            ║
╚═══════════════════════════════════════════╝

Cliente: {pedido['nombre_cliente']}
Mesa: {pedido['nombre_mesa']}
Fecha: {pedido['fecha']}
""")
    
    print("\n--- DETALLE ---")
    tabla_items = [
        [i["nombre"], i["cantidad"], f"${i['precio']:,.0f}", f"${i['subtotal']:,.0f}"]
        for i in pedido["items"]
    ]
    print(tabulate(tabla_items, headers=["Producto", "Cant.", "Precio", "Subtotal"], tablefmt="grid"))
    print(f"\n{'TOTAL A PAGAR:':.<30} ${pedido['total']:,.0f}")
    
    if confirmarAccion("\n¿Confirmar pago? (S/N): "):
        # Cambiar estado del pedido
        for p in data["pedidos"]:
            if p["id"] == id_pedido:
                p["estado"] = "facturado"
                break
        
        # Liberar mesa
        for t in data["topicos"]:
            if t["id"] == pedido["id_mesa"]:
                t["disponible"] = True
                break
        
        saveData(data)
        
        print("\n✓ Pedido facturado exitosamente.")
        print(f"✓ Mesa '{pedido['nombre_mesa']}' liberada.")
    else:
        print("✗ Operación cancelada.")
    
    pausarPantalla()

def cancelarPedido():
    """Cancela un pedido activo"""
    limpiarPantalla()
    data = loadData()
    pedidos_activos = [p for p in data["pedidos"] if p["estado"] == "activo"]
    
    print("""
╔═══════════════════════════════════════════╗
║          CANCELAR PEDIDO                 ║
╚═══════════════════════════════════════════╝
""")
    
    if not pedidos_activos:
        print("\n✗ No hay pedidos activos para cancelar.")
        pausarPantalla()
        return
    
    tabla = [
        [p["id"], p["nombre_cliente"], p["nombre_mesa"], f"${p['total']:,.0f}"]
        for p in pedidos_activos
    ]
    print(tabulate(tabla, headers=["ID", "Cliente", "Mesa", "Total"], tablefmt="grid"))
    
    id_pedido = inputSeguro("\nID del pedido a cancelar: ")
    
    pedido = next((p for p in data["pedidos"] if p["id"] == id_pedido and p["estado"] == "activo"), None)
    
    if not pedido:
        print("✗ Pedido no encontrado o no está activo.")
        pausarPantalla()
        return
    
    if confirmarAccion(f"\n¿Cancelar pedido {id_pedido} de {pedido['nombre_cliente']}? (S/N): "):
        # Cambiar estado del pedido
        for p in data["pedidos"]:
            if p["id"] == id_pedido:
                p["estado"] = "cancelado"
                break
        
        # Liberar mesa
        for t in data["topicos"]:
            if t["id"] == pedido["id_mesa"]:
                t["disponible"] = True
                break
        
        saveData(data)
        
        print("\n✓ Pedido cancelado exitosamente.")
        print(f"✓ Mesa '{pedido['nombre_mesa']}' liberada.")
    else:
        print("✗ Operación cancelada.")
    
    pausarPantalla()