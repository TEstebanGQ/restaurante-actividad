from datetime import datetime

def calcularEstadisticasCliente(pedidos, idCliente):
    """Calcula estadísticas de un cliente"""
    pedidosCliente = [p for p in pedidos if p["id_cliente"] == idCliente]
    pedidosFacturados = [p for p in pedidosCliente if p["estado"] == "facturado"]
    pedidosActivos = [p for p in pedidosCliente if p["estado"] == "activo"]
    pedidosCancelados = [p for p in pedidosCliente if p["estado"] == "cancelado"]
    
    return {
        "total": len(pedidosCliente),
        "facturados": pedidosFacturados,
        "activos": pedidosActivos,
        "cancelados": pedidosCancelados,
        "totalFacturado": sum(p["total"] for p in pedidosFacturados),
        "totalPendiente": sum(p["total"] for p in pedidosActivos),
        "totalGeneral": sum(p["total"] for p in pedidosCliente)
    }

def calcularProductosMasPedidos(pedidos):
    """Calcula los productos más pedidos de un conjunto de pedidos"""
    productosCount = {}
    for pedido in pedidos:
        for item in pedido["items"]:
            nombre = item["nombre"]
            if nombre in productosCount:
                productosCount[nombre]["cantidad"] += item["cantidad"]
                productosCount[nombre]["total"] += item["subtotal"]
            else:
                productosCount[nombre] = {"cantidad": item["cantidad"], "total": item["subtotal"]}
    
    return sorted(productosCount.items(), key=lambda x: x[1]["cantidad"], reverse=True)[:5]

def crearPedido(idCliente, nombreCliente, idMesa, nombreMesa, items, total):
    """Crea un objeto de pedido nuevo"""
    return {
        "id_cliente": idCliente,
        "nombre_cliente": nombreCliente,
        "id_mesa": idMesa,
        "nombre_mesa": nombreMesa,
        "items": items,
        "total": total,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estado": "activo"
    }

def actualizarEstadoPedido(data, idPedido, nuevoEstado, liberarMesa=True):
    """Actualiza el estado de un pedido y opcionalmente libera la mesa"""
    for pedido in data["pedidos"]:
        if pedido["id"] == idPedido:
            pedido["estado"] = nuevoEstado
            if liberarMesa and pedido["id_mesa"] != 0:
                for topico in data["topicos"]:
                    if topico["id"] == pedido["id_mesa"]:
                        topico["disponible"] = True
                        break
            return True
    return False

def calcularRankingClientes(clientes, pedidos):
    """Calcula el ranking de clientes por gasto total"""
    gastosClientes = {}
    
    for cliente in clientes:
        pedidosCliente = [p for p in pedidos if p["id_cliente"] == cliente["id"]]
        totalPagado = sum(p["total"] for p in pedidosCliente if p["estado"] == "facturado")
        
        if totalPagado > 0:
            gastosClientes[cliente["id"]] = {
                "nombre": cliente["nombre"],
                "telefono": cliente.get("telefono", "N/A"),
                "pedidos": len([p for p in pedidosCliente if p["estado"] == "facturado"]),
                "total": totalPagado
            }
    
    return sorted(gastosClientes.items(), key=lambda x: x[1]["total"], reverse=True)