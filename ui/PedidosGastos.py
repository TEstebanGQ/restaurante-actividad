from core.Storage import loadData
from core.PedidosHelpers import calcularEstadisticasCliente, calcularProductosMasPedidos, calcularRankingClientes
from ui.UIHelpers import *

def verGastosPorCliente():
    """Muestra el historial de gastos de un cliente"""
    limpiarPantalla()
    data = loadData()
    mostrarHeader("GASTOS POR CLIENTE")
    
    if not data["clientes"]:
        mostrarMensaje("No hay clientes registrados.", "error")
        pausarPantalla()
        return
    
    print("\n¿Cómo desea consultar?")
    print("1. Ver gastos de un cliente específico")
    print("2. Ver ranking de clientes (mayor a menor gasto)")
    print("3. Ver todos los clientes con sus gastos")
    
    opcion = inputSeguro("\nSeleccione una opción: ")
    
    acciones = {
        "1": lambda: verGastosClienteEspecifico(data),
        "2": lambda: verRankingClientes(data),
        "3": lambda: verTodosClientesGastos(data)
    }
    
    if opcion in acciones:
        acciones[opcion]()
    else:
        mostrarMensaje("Opción inválida.", "error")
        pausarPantalla()

def verGastosClienteEspecifico(data):
    """Ver gastos detallados de un cliente"""
    limpiarPantalla()
    mostrarHeader("GASTOS DE CLIENTE ESPECÍFICO")
    
    criterio = inputSeguro("\nBuscar cliente por nombre o teléfono: ")
    if not criterio:
        return
    
    resultados = buscarPorCriterio(data["clientes"], criterio, ["nombre", "telefono"])
    
    if not resultados:
        mostrarMensaje("No se encontraron clientes.", "error")
        pausarPantalla()
        return
    
    print("\n--- CLIENTES ENCONTRADOS ---")
    cliente = seleccionarDeTabla(data, resultados, ["ID", "Nombre", "Teléfono"], "ID del cliente")
    if not cliente:
        pausarPantalla()
        return
    
    stats = calcularEstadisticasCliente(data["pedidos"], cliente["id"])
    
    limpiarPantalla()
    mostrarHeader("HISTORIAL DE GASTOS")
    print(f"\nCliente: {cliente['nombre']}\nTeléfono: {cliente.get('telefono', 'N/A')}")
    
    if stats["total"] == 0:
        mostrarMensaje("Este cliente no tiene pedidos registrados.", "error")
        pausarPantalla()
        return
    
    # Mostrar pedidos
    print("\n--- PEDIDOS REALIZADOS ---")
    pedidosCliente = stats["facturados"] + stats["activos"] + stats["cancelados"]
    tabla = [[p["id"], p["nombre_mesa"], p["fecha"], p["estado"].upper(), f"${p['total']:,.0f}"] 
             for p in pedidosCliente]
    mostrarTabla(tabla, ["ID Pedido", "Mesa", "Fecha", "Estado", "Total"], "")
    
    # Mostrar resumen
    print(f"""
═══════════════════════════════════════════
RESUMEN:
  • Total de pedidos: {stats['total']}
  • Pedidos pagados: {len(stats['facturados'])}
  • Pedidos activos: {len(stats['activos'])}
  • Pedidos cancelados: {len(stats['cancelados'])}

GASTOS:
  • Total gastado (pagado): ${stats['totalFacturado']:,.0f}
  • Total pendiente: ${stats['totalPendiente']:,.0f}
  • Total general: ${stats['totalGeneral']:,.0f}
═══════════════════════════════════════════
""")
    
    # Productos más pedidos
    productos = calcularProductosMasPedidos(pedidosCliente)
    if productos:
        print("\n--- PRODUCTOS MÁS PEDIDOS ---")
        tablaProductos = [[nombre, f"{datos['cantidad']}x", f"${datos['total']:,.0f}"] 
                          for nombre, datos in productos]
        mostrarTabla(tablaProductos, ["Producto", "Cantidad", "Total"], "")
    
    pausarPantalla()

def verRankingClientes(data):
    """Muestra ranking de clientes por gasto total"""
    limpiarPantalla()
    mostrarHeader("RANKING DE CLIENTES")
    
    ranking = calcularRankingClientes(data["clientes"], data["pedidos"])
    
    if not ranking:
        mostrarMensaje("No hay clientes con pedidos facturados.", "error")
        pausarPantalla()
        return
    
    print("\n--- TOP CLIENTES POR GASTO ---")
    tablaRanking = [[idx + 1, datos["nombre"], datos["telefono"], datos["pedidos"], 
                     f"${datos['total']:,.0f}"] for idx, (_, datos) in enumerate(ranking)]
    mostrarTabla(tablaRanking, ["#", "Cliente", "Teléfono", "Pedidos", "Total Gastado"], "")
    
    totalGeneral = sum(datos["total"] for _, datos in ranking)
    promedio = totalGeneral / len(ranking) if ranking else 0
    
    print(f"""
═══════════════════════════════════════════
ESTADÍSTICAS:
  • Total de clientes activos: {len(ranking)}
  • Gasto total acumulado: ${totalGeneral:,.0f}
  • Gasto promedio por cliente: ${promedio:,.0f}
═══════════════════════════════════════════
""")
    
    pausarPantalla()

def verTodosClientesGastos(data):
    """Muestra todos los clientes con sus gastos"""
    limpiarPantalla()
    mostrarHeader("TODOS LOS CLIENTES Y SUS GASTOS")
    
    infoClientes = []
    for cliente in data["clientes"]:
        stats = calcularEstadisticasCliente(data["pedidos"], cliente["id"])
        infoClientes.append({
            "id": cliente["id"],
            "nombre": cliente["nombre"],
            "pedidos_total": stats["total"],
            "pedidos_pagados": len(stats["facturados"]),
            "total_gastado": stats["totalFacturado"],
            "total_pendiente": stats["totalPendiente"]
        })
    
    infoClientes.sort(key=lambda x: x["total_gastado"], reverse=True)
    
    tabla = [[c["id"], c["nombre"], c["pedidos_total"], c["pedidos_pagados"], 
              f"${c['total_gastado']:,.0f}", 
              f"${c['total_pendiente']:,.0f}" if c['total_pendiente'] > 0 else "-"] 
             for c in infoClientes]
    
    mostrarTabla(tabla, ["ID", "Cliente", "Pedidos", "Pagados", "Total Gastado", "Pendiente"], "")
    pausarPantalla()