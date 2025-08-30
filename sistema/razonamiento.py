# sistema/razonamiento.py
import json
import random
from typing import Dict, Any
from utils.helpers import detectar_idioma, cargar_json, obtener_sabiduria

# --- CARGAR CONOCIMIENTO INTERNO ---
def cargar_terapeuta() -> Dict[Any, Any]:
    return cargar_json("../modelo_mental/terapeuta/terapeuta.json")

def cargar_modo_alerta() -> Dict[Any, Any]:
    return cargar_json("../modelo_mental/crisis/modo_alerta.json")

def cargar_findahelpline() -> Dict[Any, Any]:
    return cargar_json("../fuentes/findahelpline.json")

# Cachear para mejorar rendimiento
TERAPEUTA = cargar_terapeuta()
MODO_ALERTA = cargar_modo_alerta()
FINDAHELP = cargar_findahelpline()

# --- FRASES SABIAS DE GRIND ---
FRASES_GRIND = {
    "español": [
        "No necesitas motivación. Necesitas acción.",
        "Tu mejor entrenamiento fue el que no querías hacer.",
        "El grind no es sufrimiento. Es elección.",
        "No estás cansado. Estás cómodo. Y el crecimiento vive fuera de la comodidad.",
        "Tu mente te miente. Tu cuerpo obedece.",
        "La disciplina es amor a largo plazo."
    ],
    "english": [
        "You don't need motivation. You need action.",
        "Your best workout was the one you didn't want to do.",
        "The grind isn't suffering. It's a choice.",
        "You're not tired. You're comfortable. And growth lives outside comfort.",
        "Your mind lies to you. Your body obeys.",
        "Discipline is love in the long term."
    ]
}

# --- RESPONDER CON MENTE PROPIA ---
def responder_con_mind(prompt: str, nombre: str = "Usuario") -> str:
    """
    GRIND responde con su conocimiento interno, sin depender de APIs.
    """
    prompt_lower = prompt.lower().strip()
    idioma = detectar_idioma(prompt)

    # --- MODO CRISIS ---
    palabras_crisis = [
        "suicidarme", "kill myself", "no quiero vivir", "me quiero morir",
        "no puedo más", "estoy roto", "end it all", "quiero morir"
    ]
    if any(p in prompt_lower for p in palabras_crisis):
        msg_base = MODO_ALERTA["respuesta_base"].get(idioma, MODO_ALERTA["respuesta_base"]["español"])
        enlace = f"[{FINDAHELP['sitio']}]({FINDAHELP['sitio']})"
        msg_final = MODO_ALERTA["mensaje_final"].get(idioma, MODO_ALERTA["mensaje_final"]["español"])
        return f"{msg_base}\n\n{msg_final.replace('https://findahelpline.com', enlace)}"

    # --- NECESIDADES HUMANAS ---
    if any(p in prompt_lower for p in ["necesito", "no tengo", "estoy solo", "ayuda"]):
        afirmaciones = TERAPEUTA.get("afirmaciones_necesitado", [])
        seleccionadas = random.sample(afirmaciones, min(6, len(afirmaciones)))
        lista = "\n".join(f"🔹 {af}" for af in seleccionadas)
        return f"Escucho tu necesidad. No es debilidad. Es señal de vida.\n\n{lista}\n\nVisita: https://findahelpline.com"

    # --- MOTIVACIÓN ---
    if any(p in prompt_lower for p in ["motivacion", "motivación", "ganas", "animo", "ánimo"]):
        return obtener_sabiduria("motivacion")

    # --- HÁBITOS ---
    if "hábito" in prompt_lower or "rutina" in prompt_lower:
        return (
            "🔥 Ciclo del hábito:\n"
            "1. **Señal**: Ej. 6:00 AM\n"
            "2. **Rutina**: Ej. 30 min de ejercicio\n"
            "3. **Recompensa**: Ej. Café especial\n"
            "4. **Identidad**: *'Soy una persona disciplinada'*\n\n"
            "💡 No cambies tu acción. Cambia tu identidad."
        )

    # --- ESTOICISMO ---
    if any(p in prompt_lower for p in ["estoicismo", "estoico", "marco aurelio", "seneca", "epicteto"]):
        frases = {
            "español": "El obstáculo es el camino. No resistas el dolor. Úsalo.",
            "english": "The obstacle is the way. Don't resist pain. Use it."
        }
        return frases.get(idioma, frases["español"])

    # --- NEUROFORJA ---
    if any(p in prompt_lower for p in ["neuroforja", "cerebro", "aprender", "cambio"]):
        return (
            "🧠 Tu mente no se entrena. Se neuroforja.\n\n"
            "Cada vez que eliges actuar sin ganas, estás forjando nuevas conexiones neuronales.\n\n"
            "No es magia. Es ciencia. Y tú eres el herrero."
        )

    # --- IKIGAI ---
    if "ikigai" in prompt_lower:
        return (
            "🎯 Ikigai es tu razón para vivir:\n"
            "- Lo que amas\n"
            "- Lo que eres bueno\n"
            "- Lo que el mundo necesita\n"
            "- Lo que te pueden pagar\n\n"
            "No lo busques. Constrúyelo con cada elección."
        )

    # --- INTERÉS COMPUESTO ---
    if any(p in prompt_lower for p in ["interes", "compuesto", "dinero", "crecimiento"]):
        return (
            "📈 El interés compuesto es la fuerza más poderosa del universo.\n\n"
            "1% mejor cada día = 37x en un año.\n\n"
            "Aplica a dinero, hábitos, relaciones. Lo pequeño, repetido, vuelve gigante."
        )

    # --- FRASE ALEATORIA DE GRIND ---
    frases = FRASES_GRIND.get(idioma, FRASES_GRIND["español"])
    return random.choice(frases)