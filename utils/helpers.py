# utils/helpers.py
import json
import os

def detectar_idioma(texto: str) -> str:
    """
    Detecta el idioma del usuario por palabras clave y estructura.
    """
    texto = texto.lower().strip()
    if any(p in texto for p in ["hola", "gracias", "por favor", "necesito"]):
        return "español"
    elif any(p in texto for p in ["hello", "thanks", "please", "need"]):
        return "english"
    elif any(p in texto for p in ["merci", "bonjour", "s'il vous plaît"]):
        return "français"
    elif any(p in texto for p in ["hallo", "danke", "bitte"]):
        return "deutsch"
    else:
        return "español"  # por defecto

def formatear_respuesta(texto: str, nombre: str) -> str:
    """
    Añade estilo, metáforas y personalidad de GRIND a cualquier respuesta.
    """
    inicio = f"🔥 {nombre}, escucha:"
    final = "\n\n💡 Recuerda: el grind no es sufrimiento. Es elección."
    return f"{inicio}\n\n{texto}\n{final}"

def obtener_sabiduria(tema: str) -> str:
    """
    Devuelve una frase sabia según el tema.
    """
    sabidurias = {
        "motivacion": "No necesitas motivación. Necesitas acción.",
        "disciplina": "Tu mente te miente. Tu cuerpo obedece.",
        "crisis": "Escucho tu dolor. No estás solo. Tu vida importa.",
        "hábitos": "1% mejor cada día = 37x en un año."
    }
    return sabidurias.get(tema, "Tu evolución es tu mayor obra.")