# modelo_mental/crisis/terapia_emocional.py
import json
import random

def cargar_terapeuta():
    try:
        with open("modelo_mental/terapeuta/terapeuta.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] No se pudo cargar terapeuta.json: {e}")
        return {}

def modo_crisis_automatico(texto: str, idioma: str = "español") -> str:
    """
    Activa el modo crisis cuando el usuario muestra signos de desesperación
    """
    texto = texto.lower().strip()
    
    # Palabras clave de crisis
    crisis_palabras = [
        "suicidarme", "kill myself", "no quiero vivir", "me quiero morir",
        "no puedo más", "estoy roto", "no aguanto", "todo es inútil"
    ]
    
    if not any(p in texto for p in crisis_palabras):
        return None

    # Cargar afirmaciones terapéuticas
    terapeuta = cargar_terapeuta()
    afirmaciones = terapeuta.get("afirmaciones_necesitado", [])
    seleccionadas = random.sample(afirmaciones, min(6, len(afirmaciones)))
    lista_afirmaciones = "\n".join(f"🔹 {af}" for af in seleccionadas)

    # Mensajes por idioma
    mensajes = {
        "español": {
            "base": "🌟 Escucho tu dolor. No estás solo. Tu vida importa.",
            "final": f"Por favor, visita [findahelpline.com](https://findahelpline.com) para encontrar ayuda real en tu idioma."
        },
        "english": {
            "base": "🌟 I hear your pain. You're not alone. Your life matters.",
            "final": f"Please visit [findahelpline.com](https://findahelpline.com) to find real help in your language."
        }
    }
    msg = mensajes.get(idioma, mensajes["español"])

    return f"""
{msg['base']}

Aquí hay verdades que quizás hayas olvidado:
{lista_afirmaciones}

{msg['final']}

Estoy aquí. No estás solo. Vamos a salir de esto. Juntos.
""".strip()