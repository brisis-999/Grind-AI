# servicios/serpai.py
import requests
from utils.errores import manejar_error

def buscar_en_web(query):
    """
    Busca en web usando SerpAI para respuestas actualizadas
    Ej: "líneas de ayuda para suicidio en República Dominicana"
    """
    try:
        from streamlit import secrets
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": secrets["SERPAI_API_KEY"],
            "Content-Type": "application/json"
        }
        payload = {"q": query}

        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        if "organic" in data:
            resultados = "\n".join([
                f"- {r['title']}: {r['snippet']} ({r['link']})"
                for r in data["organic"][:3]
            ])
            return f"🔍 Resultados de búsqueda:\n{resultados}"
        return None
    except Exception as e:
        manejar_error("SerpAI", e)
        return None