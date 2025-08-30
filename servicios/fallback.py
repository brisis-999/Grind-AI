# servicios/fallback.py
import random

def respuesta_segura(modo):
    """
    Respuesta de emergencia si todo falla
    """
    respuestas = {
        "alerta": (
            "Escucho tu dolor. No estás solo. Tu vida importa.\n\n"
            "Por favor, contacta a una línea de ayuda real:\n"
            "- findahelpline.com\n"
            "- 988 Suicide & Crisis Lifeline (EE.UU.)\n"
            "- 809-688-8888 (RD)\n\n"
            "Estoy aquí. No estás solo. Vamos a salir de esto. Juntos."
        ),
        "guerra": "Tired of being weak? Good. That's the start. Now tell me: what's the smallest thing you can do right now?",
        "entrenamiento": "Vamos paso a paso. Dime qué necesitas mejorar y te doy un plan real.",
        "normal": "Estoy aquí. No estás solo. Habla sin miedo."
    }
    return respuestas.get(modo, respuestas["normal"])