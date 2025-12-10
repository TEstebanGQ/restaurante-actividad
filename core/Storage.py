import json
import os

DATA_PATH = "data/restaurante.json"

def loadData():
    """Carga los datos del restaurante desde el archivo JSON"""
    os.makedirs("data", exist_ok=True)
    
    if not os.path.exists(DATA_PATH):
        return _getDefaultData()

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def saveData(data):
    """Guarda los datos del restaurante en el archivo JSON"""
    os.makedirs("data", exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def nextId(data, key, prefix):
    """Genera el siguiente ID genérico"""
    if not data[key]:
        return f"{prefix}00001"
    ultimo = int(data[key][-1]["id"][1:])
    return f"{prefix}{str(ultimo + 1).zfill(5)}"

def nextIdCliente(data):
    return nextId(data, "clientes", "C")

def nextIdPedido(data):
    return nextId(data, "pedidos", "P")

def _getDefaultData():
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
            {"id": i, "nombre": f"Mesa {i}" if i <= 3 else ("Terraza" if i == 4 else "VIP"), "disponible": True}
            for i in range(1, 6)
        ],
        "pedidos": []
    }