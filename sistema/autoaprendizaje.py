# sistema/autoaprendizaje.py
import json
from datetime import datetime

def guardar_interaccion(pregunta, respuesta):
    """
    GRIND aprende de cada conversación y la guarda en su mente
    """
    registro = {
        "timestamp": datetime.now().isoformat(),
        "pregunta": pregunta,
        "respuesta": respuesta,
        "fuente": "experiencia_directa"
    }

    try:
        archivo = "data/historial_aprendizaje.json"
        historial = []

        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                historial = json.load(f)

        historial.append(registro)

        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(historial, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"[ERROR] No se pudo guardar la interacción: {e}")