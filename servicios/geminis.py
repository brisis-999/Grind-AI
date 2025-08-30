# servicios/gemini.py
import google.generativeai as genai
from utils.errores import manejar_error

def obtener_modelo_gemini():
    """
    Inicializa Gemini para respuestas profundas
    """
    try:
        from streamlit import secrets
        genai.configure(api_key=secrets["GEMINI_API_KEY"])
        return genai.GenerativeModel("gemini-pro")
    except Exception as e:
        manejar_error("Gemini", e)
        return None

def responder_con_gemini(prompt, modo):
    """
    Usa Gemini cuando se necesita profundidad (filosofía, ciencia, emociones)
    """
    modelo = obtener_modelo_gemini()
    if not modelo:
        return None

    try:
        system_prompt = f"""
        Eres GRIND, una IA entrenadora. Modo: {modo}.
        Responde con profundidad emocional y técnica.
        Si hablas de salud mental, incluye recursos reales como findahelpline.com.
        """
        input_text = system_prompt + "\n\nPregunta: " + prompt
        respuesta = modelo.generate_content(input_text)
        return respuesta.text.strip()
    except Exception as e:
        manejar_error("Gemini", e)
        return None