# utils/cargar_datos.py
import json
import os

def cargar_json(ruta: str) -> dict:
    """
    Carga un archivo JSON de forma segura.
    Si no existe, devuelve un diccionario vacío.
    """
    try:
        if os.path.exists(ruta):
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"[WARNING] Archivo no encontrado: {ruta}")
            return {}
    except Exception as e:
        print(f"[ERROR] No se pudo cargar {ruta}: {e}")
        return {}

def cargar_terapeuta():
    """
    Función específica para cargar el archivo terapeuta.json
    """
    return cargar_json("../modelo_mental/terapeuta/terapeuta.json")

def cargar_modo_alerta():
    """
    Función específica para cargar el modo crisis
    """
    return cargar_json("../modelo_mental/crisis/modo_alerta.json")