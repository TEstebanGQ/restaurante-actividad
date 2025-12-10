import json
import os

DATA_PATH = "data/restaurante.json"

def loadData():
    """Carga los datos del restaurante desde el archivo JSON"""
    os.makedirs("data", exist_ok=True)
    
    if not os.path.exists(DATA_PATH):
        return {
            "productos": {
                "platillos": [
                    {"id": 1, "nombre": "Carne Asada", "precio": 18000},
                    {"id": 2, "nombre": "Hígado", "precio": 12000},
                    {"id": 3, "nombre": "Pastas", "precio": 15000}
                ],
                "bebidas": [
                    {"id": 1, "nombre": "Pepsi", "precio": 2000},
                    {"id": 2, "nombre": "Coca Cola", "precio": 2500},
                    {"id": 3, "nombre": "Colombiana", "precio": 1500}
                ],
                "adicionales": [
                    {"id": 1, "nombre": "Papas a la Francesa", "precio": 5000},
                    {"id": 2, "nombre": "Ensalada", "precio": 7000},
                    {"id": 3, "nombre": "Yuca Frita", "precio": 8000}
                ]
            },
            "clientes": [],
            "topicos": [
                {"id": 1, "nombre": "Mesa 1", "disponible": True},
                {"id": 2, "nombre": "Mesa 2", "disponible": True},
                {"id": 3, "nombre": "Mesa 3", "disponible": True},
                {"id": 4, "nombre": "Terraza", "disponible": True},
                {"id": 5, "nombre": "VIP", "disponible": True}
            ],
            "pedidos": []
        }

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def saveData(data):
    """Guarda los datos del restaurante en el archivo JSON"""
    os.makedirs("data", exist_ok=True)
    
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def nextIdCliente(data):
    """Genera el siguiente ID para un cliente"""
    if not data["clientes"]:
        return "C00001"
    
    ultimo = int(data["clientes"][-1]["id"][1:])
    nuevo = ultimo + 1
    return f"C{str(nuevo).zfill(5)}"

def nextIdPedido(data):
    """Genera el siguiente ID para un pedido"""
    if not data["pedidos"]:
        return "P00001"
    
    ultimo = int(data["pedidos"][-1]["id"][1:])
    nuevo = ultimo + 1
    return f"P{str(nuevo).zfill(5)}"