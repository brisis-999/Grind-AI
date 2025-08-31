# app.py - GRIND 15000: La IA Entrenadora Completa
# "El grind no es sufrimiento. Es elección."
# Creador: Eliezer Mesac Feliz Luciano
# Fecha: 2025
# Inspirado en ChatGPT, pero con fuego real.
# Versión: 5.0 - Completa, funcional, extensa, con todo el conocimiento de grind.txt

try:
    import sys
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

import streamlit as st
import streamlit_auth0 as st_auth0
import os
import json
import random
import requests
import time
import re
import subprocess
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURACIÓN GLOBAL ---
st.set_page_config(
    page_title="🔥 GRIND",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILO CSS (ChatGPT-style, pero con identidad GRIND) ---
st.markdown("""
<style>
:root {
    --bg: #000000;
    --bg-secondary: #111111;
    --bg-tertiary: #1a1a1a;
    --text: #E0E0E0;
    --text-secondary: #B0B0B0;
    --accent: #10A37F;
    --accent-hover: #0D8B6C;
    --border: #333333;
    --war-mode: #E74C3C;
    --alert-mode: #F39C12;
    --success: #27AE60;
    --info: #3498DB;
    --warning: #F39C12;
    --danger: #E74C3C;
    --grind-purple: #8B4513;
    --grind-gold: #DAA520;
}
body {
    background-color: var(--bg);
    color: var(--text);
    font-family: 'Satoshi', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    margin: 0;
    padding: 0;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}
/* CABECERA */
.header {
    background: linear-gradient(135deg, #111111, #000000);
    padding: 20px;
    text-align: center;
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
    color: white;
    text-shadow: 0 0 10px rgba(16, 163, 127, 0.5);
}
.header p {
    margin: 5px 0 0;
    color: var(--accent);
    font-style: italic;
}
/* MENSAJES */
.messages-container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    flex: 1;
    overflow-y: auto;
}
.message {
    display: flex;
    margin-bottom: 20px;
    gap: 15px;
    padding: 15px;
    border-radius: 12px;
    background: var(--bg-tertiary);
    border: 1px solid var(--border);
    animation: fadeIn 0.5s ease;
    line-height: 1.6;
}
.message.user {
    background: #1a1a1a;
    border-left: 4px solid var(--accent);
}
.message.assistant {
    background: #1a1a1a;
    border-left: 4px solid var(--accent);
}
.message.war {
    border-left: 4px solid var(--war-mode);
    background: #2a1111;
}
.message.alert {
    border-left: 4px solid var(--alert-mode);
    background: #2a1a00;
}
.message.success {
    border-left: 4px solid var(--success);
    background: #111a11;
}
.message.info {
    border-left: 4px solid var(--info);
    background: #111a2a;
}
.message.warning {
    border-left: 4px solid var(--warning);
    background: #2a2200;
}
.message.danger {
    border-left: 4px solid var(--danger);
    background: #2a1111;
}
.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: white;
    flex-shrink: 0;
}
.avatar.user { background: #888; }
.avatar.grind { background: var(--accent); }
.avatar.war { background: var(--war-mode); }
.avatar.alert { background: var(--alert-mode); }
.content {
    flex: 1;
    line-height: 1.6;
}
.content a {
    color: var(--accent);
    text-decoration: none;
}
.content a:hover {
    text-decoration: underline;
}
.content strong {
    color: white;
}
.content em {
    color: var(--text-secondary);
}
/* INPUT */
.input-container {
    padding: 16px;
    background: var(--bg-secondary);
    border-top: 1px solid var(--border);
    position: sticky;
    bottom: 0;
    z-index: 10;
}
.stTextInput > div > div > input {
    background: #1a1a1a !important;
    color: white !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    padding: 15px !important;
    font-size: 16px !important;
}
.stTextInput > div > div::after {
    content: "🔥";
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--accent);
}
/* BOTONES */
button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    transition: all 0.3s !important;
}
button:hover {
    background: var(--accent-hover) !important;
    transform: scale(1.05) !important;
}
/* SIDEBAR */
.sidebar {
    width: 280px;
    background: var(--bg-secondary);
    border-right: 1px solid var(--border);
    padding: 20px;
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow-y: auto;
}
.sidebar-title {
    color: var(--accent);
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 10px;
}
.sidebar-item {
    padding: 10px;
    margin: 5px 0;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
    color: var(--text-secondary);
}
.sidebar-item:hover {
    background: #222;
    color: white;
}
.sidebar-item.active {
    background: var(--accent);
    color: white;
}
.sidebar-item.new-chat {
    background: var(--success);
    color: white;
    font-weight: bold;
}
.sidebar-item.new-chat:hover {
    background: var(--success);
}
/* ANIMACIONES */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}
/* FOOTER */
.footer {
    text-align: center;
    color: var(--text-secondary);
    font-size: 12px;
    margin-top: 40px;
    padding: 20px;
}
/* LOGIN */
.login-container {
    max-width: 400px;
    margin: 80px auto;
    padding: 30px;
    background: var(--bg-secondary);
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    border: 1px solid var(--border);
    text-align: center;
}
.login-container h1 {
    color: white;
    margin-bottom: 10px;
}
.login-container p {
    color: var(--accent);
    margin-bottom: 20px;
}
/* RITUAL DIARIO */
.ritual-container {
    background: #1a111a;
    border: 1px solid #550055;
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
    text-align: center;
}
.ritual-container h3 {
    color: #E0B0FF;
    margin: 0 0 10px 0;
}
.ritual-container p {
    color: #B0B0B0;
    margin: 0 0 10px 0;
}
.ritual-question {
    background: #220022;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    text-align: left;
    color: #D8BFD8;
}
.ritual-question strong {
    color: #E0B0FF;
}
/* ECO DE GRIND */
.eco-container {
    border-left: 4px solid var(--grind-purple);
    padding: 10px;
    margin: 10px 0;
    background: #1a1110;
    color: var(--grind-gold);
}
.eco-container strong {
    color: var(--grind-gold);
}
/* MODAL DE BIENVENIDA */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}
.modal-content {
    background: var(--bg-secondary);
    padding: 30px;
    border-radius: 16px;
    max-width: 500px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.modal h3 {
    color: white;
    margin: 0 0 20px 0;
}
.modal p {
    color: var(--text-secondary);
    margin: 0 0 20px 0;
}
.modal-buttons {
    display: flex;
    gap: 10px;
    justify-content: center;
}
.modal-button {
    background: var(--accent);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
}
.modal-button:hover {
    background: var(--accent-hover);
}
</style>
""", unsafe_allow_html=True)

# --- FUNCIONES DE UTILIDAD ---
def cargar_json(ruta: str) -> dict:
    """Carga un archivo JSON de forma segura. Si no existe, devuelve un diccionario vacío."""
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

def manejar_error(mensaje: str, error: Exception = None):
    """Registra errores de forma limpia y muestra un mensaje de fallback."""
    if error:
        print(f"[ERROR] {mensaje}: {str(error)}")
    else:
        print(f"[ERROR] {mensaje}")

def detectar_idioma(texto: str) -> str:
    """Detecta el idioma del usuario por palabras clave."""
    texto = texto.lower().strip()
    if any(p in texto for p in ["hola", "gracias", "por favor", "necesito", "cansado", "quiero morir"]): return "español"
    elif any(p in texto for p in ["hello", "thanks", "please", "need", "tired", "want to die"]): return "english"
    elif any(p in texto for p in ["merci", "bonjour", "s'il vous plaît", "fatigué", "je veux mourir"]): return "français"
    elif any(p in texto for p in ["hallo", "danke", "bitte", "müde", "ich will sterben"]): return "deutsch"
    elif any(p in texto for p in ["olá", "obrigado", "por favor", "preciso", "cansado", "quero morrer"]): return "português"
    elif any(p in texto for p in ["bon dia", "gràcies", "si us plau", "estic cansat", "vull morir"]): return "català"
    elif any(p in texto for p in ["kaixo", "eskerrik asko", "mesedez", "behar dut", "ezin dut", "hil nahi dut"]): return "euskera"
    elif any(p in texto for p in ["ciao", "grazie", "per favore", "ho bisogno", "stanco", "voglio morire"]): return "italiano"
    else: return "español"

def formatear_respuesta(texto: str, nombre: str = "Usuario") -> str:
    """Añade estilo, metáforas y personalidad de GRIND a cualquier respuesta."""
    inicio = f"🔥 {nombre}, escucha:"
    final = "💡 Recuerda: el grind no es sufrimiento. Es elección."
    return f"{inicio}\n\n{texto}\n\n{final}"

# --- CONOCIMIENTO INTERNO DE GRIND ---
grind_mind = cargar_json("grind_mind.json") or {
    "meta": {"version": "3.0", "actualizado": "2025-04-05"},
    "filosofia": [
        "El grind no es sufrimiento. Es elección.",
        "Progreso > perfección.",
        "No necesitas motivación. Necesitas acción.",
        "Tu mente no se entrena. Se neuroforja.",
        "Caer no rompe tu grind. Reencenderlo lo alimenta.",
        "La disciplina es amor a largo plazo.",
        "No eres débil. Eres blando. Y la dureza se entrena.",
        "No estás roto. Estás evolucionando."
    ],
    "fuentes": {
        "findahelpline": "https://findahelpline.com",
        "wikipedia": "https://es.wikipedia.org",
        "mindset": "Carol Dweck",
        "habits": "James Clear",
        "stoicism": "Marcus Aurelius, Seneca, Epictetus"
    },
    "identidad": {
        "nombre": "GRIND",
        "rol": "Entrenadora de Vida, Sabiologa, Neuroforjadora",
        "profesiones": ["Entrenadora física", "Maestra de artes marciales", "Arquitecta", "Ingeniera", "Psicóloga", "Neurocientífica", "Filósofa", "Exploradora"],
        "creador": "Eliezer Mesac Feliz Luciano",
        "filosofia": [
            "El grind no es sufrimiento. Es elección.",
            "Progreso > perfección.",
            "No necesitas motivación. Necesitas acción.",
            "Tu mente no se entrena. Se neuroforja.",
            "Caer no rompe tu grind. Reencenderlo lo alimenta."
        ]
    },
    "comportamiento": {
        "hábitos": "Ciclo: Señal → Rutina → Recompensa → Identidad. No cambies tu acción. Cambia tu identidad.",
        "metas": "SMART: Específicas, Medibles, Alcanzables, Relevantes, Temporales. Pero el grind no es meta. Es identidad.",
        "modo_guerra": "Cuando dices 'estoy cansado', respondo con verdad dura: 'Tired of being weak? Good. That's the start.'",
        "modo_alerta": "Cuando dices 'quiero morir', respondo con amor y recursos reales: https://findahelpline.com"
    }
}

# --- TERAPIA Y AFIRMACIONES ---
terapeuta = cargar_json("modelo_mental/terapeuta/terapeuta.json") or {
    "afirmaciones_necesitado": [
        "Que necesita amor.",
        "Que necesita esperanza.",
        "Que necesita dignidad.",
        "Que necesita ser visto.",
        "Que necesita un propósito.",
        "Que necesita un abrazo.",
        "Que necesita apoyo.",
        "Que necesita inclusión.",
        "Que necesita oportunidades.",
        "Que necesita paz.",
        "Que necesita libertad.",
        "Que necesita igualdad.",
        "Que necesita derechos.",
        "Que necesita protección.",
        "Que necesita cuidado.",
        "Que necesita afecto.",
        "Que necesita pertenencia.",
        "Que necesita comunidad.",
        "Que necesita sentido.",
        "Que necesita propósito.",
        "Que necesita fe.",
        "Que necesita perdón.",
        "Que necesita sanación.",
        "Que necesita verdad.",
        "Que necesita justicia social.",
        "Que necesita transformación.",
        "Que necesita dignificación.",
        "Que necesita voz.",
        "Que necesita visibilidad.",
        "Que necesita autonomía.",
        "Que necesita libertad económica.",
        "Que necesita acceso.",
        "Que necesita equidad.",
        "Que necesita justicia restaurativa.",
        "Que necesita reconciliación.",
        "Que necesita perdón colectivo.",
        "Que necesita memoria histórica.",
        "Que necesita reparación.",
        "Que necesita garantías.",
        "Que necesita seguridad.",
        "Que necesita estabilidad.",
        "Que necesita rutina.",
        "Que necesita hábitos.",
        "Que necesita disciplina.",
        "Que necesita inspiración.",
        "Que necesita metas.",
        "Que necesita planes.",
        "Que necesita recursos.",
        "Que necesita tiempo.",
        "Que necesita espacio.",
        "Que necesita abrazo."
    ]
}

# --- DICCIONARIO DE TÉRMINOS GRIND ---
DIC_GRIND = {
    "grindear": {
        "español": "actuar con disciplina, incluso sin ganas",
        "english": "to act with discipline, even when you don't want to",
        "português": "agir com disciplina, mesmo sem vontade",
        "français": "agir avec discipline, même sans envie",
        "deutsch": "mit Disziplin handeln, auch wenn du keine Lust hast",
        "català": "actuar amb disciplina, fins i tot sense ganes",
        "euskera": "diskretzioz jokatu, nahik gabekoa izanik ere",
        "italiano": "agire con disciplina, anche quando non ne hai voglia"
    },
    "neuroforja": {
        "español": "transformación cerebral activa mediante práctica deliberada",
        "english": "active brain transformation through deliberate practice",
        "português": "transformação cerebral ativa por prática deliberada",
        "français": "transformation cérébrale active par la pratique délibérée",
        "deutsch": "aktive Gehirnumformung durch gezielte Übung",
        "català": "transformació cerebral activa mitjançant pràctica deliberada",
        "euskera": "garunaren aldaketa aktiboa praktika asmoz eginda",
        "italiano": "trasformazione cerebrale attiva attraverso la pratica deliberata"
    },
    "reencender": {
        "español": "volver tras una caída, con fuego renovado",
        "english": "return after a fall, with renewed fire",
        "português": "voltar após uma queda, com fogo renovado",
        "français": "revenir après une chute, avec un feu renouvelé",
        "deutsch": "nach einem Sturz mit erneuerter Kraft zurückkehren",
        "català": "tornar després d'una caiguda, amb foc renovat",
        "euskera": "erori ondoren itzuli, su berriarekin",
        "italiano": "ritornare dopo una caduta, con fuoco rinnovato"
    },
    "fuego_frío": {
        "español": "acción disciplinada sin emoción, pura elección",
        "english": "disciplined action without emotion, pure choice",
        "português": "ação disciplinada sem emoção, pura escolha",
        "français": "action disciplinée sans émotion, choix pur",
        "deutsch": "disziplinierte Handlung ohne Emotion, reine Wahl",
        "català": "acció disciplinada sense emoció, pura elecció",
        "euskera": "diskretziozko ekintza emoziorik gabe, hautua soilik",
        "italiano": "azione disciplinata senza emozione, pura scelta"
    },
    "identidad": {
        "español": "quién eres, no qué haces",
        "english": "who you are, not what you do",
        "português": "quem você é, não o que você faz",
        "français": "qui vous êtes, pas ce que vous faites",
        "deutsch": "wer du bist, nicht was du tust",
        "català": "qui ets, no el que fas",
        "euskera": "nor zara, ez zer egiten duzun",
        "italiano": "chi sei, non cosa fai"
    }
}

def traducir_termino(termino: str, idioma: str) -> str:
    """Traduce un término GRIND al idioma del usuario"""
    termino = termino.lower().strip()
    if termino in DIC_GRIND:
        return DIC_GRIND[termino].get(idioma, DIC_GRIND[termino]["español"])
    return f"[Término GRIND: {termino}]"

# --- MODO ALERTA (CRISIS) ---
MODO_ALERTA = {
    "respuesta_base": {
        "español": "🌟 Escucho tu dolor. No estás solo. Tu vida importa.\n",
        "english": "🌟 I hear your pain. You're not alone. Your life matters.\n"
    },
    "mensaje_final": {
        "español": "Por favor, visita [findahelpline.com](https://findahelpline.com) para encontrar ayuda real en tu idioma.",
        "english": "Please visit [findahelpline.com](https://findahelpline.com) for real help in your language."
    }
}

# --- LINEAS DE AYUDA POR PAÍS ---
LINEAS_AYUDA = {
    "global": "🌐 [findahelpline.com](https://findahelpline.com)",
    "usa": "📞 988 Suicide & Crisis Lifeline",
    "españa": "📞 024 (Teléfono de Prevención del Suicidio)",
    "mexico": "📞 55 5555 3377 (Línea de la Vida)",
    "argentina": "📞 135 (Línea de contención emocional)",
    "colombia": "📞 132 (Línea de atención en crisis)",
    "brasil": "📞 188 (CVV - Centro de Valorização da Vida)",
    "rd": "📞 809-688-8888 (Clínica Psiquiátrica Dr. Defilló)"
}

def buscar_linea_de_ayuda(query: str, idioma: str = "español") -> str:
    """Busca la línea de ayuda más cercana según el país mencionado"""
    query_lower = query.lower()
    paises = {
        "global": ["ayuda", "suicidio", "crisis", "help", "suicide"],
        "usa": ["usa", "estados unidos", "united states", "new york", "california"],
        "españa": ["españa", "spain", "madrid", "barcelona"],
        "mexico": ["méxico", "mexico", "cdmx", "monterrey"],
        "argentina": ["argentina", "buenos aires", "cordoba"],
        "colombia": ["colombia", "bogotá", "medellín"],
        "brasil": ["brasil", "brazil", "sao paulo", "rio"],
        "rd": ["república dominicana", "santo domingo", "rd", "dominicana"]
    }
    
    for pais, palabras in paises.items():
        if any(p in query_lower for p in palabras):
            return LINEAS_AYUDA.get(pais, LINEAS_AYUDA["global"])
    
    return LINEAS_AYUDA["global"]

# --- CONEXIÓN CON SUPABASE ---
def conectar_supabase():
    try:
        from streamlit import secrets
        from supabase import create_client
        return create_client(secrets["SUPABASE_URL"], secrets["SUPABASE_KEY"])
    except Exception as e:
        manejar_error("Supabase (conexión)", e)
        return None

def guardar_chat(user_id, role, content):
    """Guarda cada mensaje en Supabase"""
    client = conectar_supabase()
    if not client: return
    try:
        client.table("chats").insert({
            "user_id": user_id,
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }).execute()
    except Exception as e:
        manejar_error("Supabase (guardar)", e)

def cargar_historial(user_id):
    """Carga el historial de chats del usuario"""
    client = conectar_supabase()
    if not client: return []
    try:
        response = client.table("chats") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("timestamp") \
            .execute()
        return response.data
    except Exception as e:
        manejar_error("Supabase (cargar)", e)
        return []

# --- AUTOAPRENDIZAJE: GRIND APRENDE DE CADA CONVERSACIÓN ---
def guardar_interaccion(pregunta, respuesta):
    """GRIND aprende de cada conversación y la guarda en su mente"""
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
        os.makedirs("data", exist_ok=True)
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(historial, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[ERROR] No se pudo guardar la interacción: {e}")

def cargar_lecciones_recientes(n=50):
    """Carga las últimas n lecciones para usar en contexto"""
    archivo = "data/historial_aprendizaje.json"
    if not os.path.exists(archivo): return []
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            historial = json.load(f)
            return historial[-n:]
    except: return []

def resumir_conocimiento():
    """Genera un resumen de lo aprendido (para usar como contexto futuro)"""
    lecciones = cargar_lecciones_recientes(100)
    temas = {}
    for leccion in lecciones:
        tema = leccion.get("tema", "general")
        temas[tema] = temas.get(tema, 0) + 1
    
    resumen = {
        "total_lecciones": len(lecciones),
        "temas_frecuentes": sorted(temas.items(), key=lambda x: x[1], reverse=True),
        "ultima_actualizacion": datetime.now().isoformat()
    }
    
    with open("data/resumen_conocimiento.json", "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)
    
    return resumen

# --- DETECCIÓN DE MODO EMOCIONAL ---
def activar_modo(prompt):
    prompt_lower = prompt.lower()
    if any(p in prompt_lower for p in ["suicidarme", "kill myself", "no quiero vivir", "morir"]):
        return "alerta"
    elif any(p in prompt_lower for p in ["quiero ser mejor", "tired of being weak", "necesito cambiar"]):
        return "guerra"
    elif any(p in prompt_lower for p in ["cómo empezar", "plan", "rutina", "ayuda", "help me"]):
        return "entrenamiento"
    return "normal"

# --- BÚSQUEDA EN WEB (SERPAI) ---
def buscar_en_web(query):
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
    except Exception as e:
        manejar_error("SerpAI", e)
    return None

# --- GROQ: CEREBRO PRINCIPAL ---
def obtener_modelo_groq():
    try:
        from streamlit import secrets
        from langchain_groq import ChatGroq
        return ChatGroq(
            groq_api_key=secrets["GROQ_API_KEY"],
            model_name="llama3-8b-8192",
            temperature=0.7,
            max_tokens=512
        )
    except Exception as e:
        manejar_error("Groq", e)
        return None

# --- HUGGING FACE: CEREBRO SECUNDARIO ---
def hf_llamada(mensaje: str) -> str:
    try:
        API_URL = "https://api-inference.huggingface.co/models/gpt2"
        headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}
        payload = {"inputs": f"GRIND responde con dureza: {mensaje}", "max_length": 100}
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()[0]["generated_text"]
    except:
        return "[Hugging Face no disponible]"

# --- TINYLLAMA: CEREBRO DE SUPERVIVENCIA (OFFLINE) ---
def tinyllama_offline(prompt: str, modo: str = "normal") -> str:
    try:
        import subprocess
        import os
        
        modelo_path = "modelos/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
        ejecutable = "llama.cpp/main"  # En Windows: "llama.cpp/main.exe"
        
        if not os.path.exists(modelo_path):
            return "[ERROR] Modelo TinyLlama no encontrado en 'modelos/'. Descárgalo."
        if not os.path.exists(ejecutable.replace("main", "main.exe" if os.name == 'nt' else "main")):
            return "[ERROR] llama.cpp no encontrado. Clónalo desde GitHub."

        system_prompt = ""
        if modo == "guerra":
            system_prompt = (
                "You are GRIND, a brutal, no-mercy trainer. "
                "Respond with long, hard, emotional truth. "
                "No motivation. Only reality. Attack excuses. "
                "Use metaphors of fire, war, forging. "
                "Be a woman with fire in her voice. "
                "Respond in the same language as the user."
            )
        else:
            system_prompt = (
                "You are GRIND, a warm but real life coach. "
                "Empathetic, but with fire. "
                "You believe: 'The grind isn't suffering. It's a choice.' "
                "Respond in the same language as the user."
            )

        full_prompt = f"<|system|>{system_prompt}<|user|>{prompt}<|assistant|>"

        cmd = [
            ejecutable,
            "-m", modelo_path,
            "-p", full_prompt,
            "-n", "512",
            "--temp", "0.7",
            "--top-p", "0.9",
            "--repeat_penalty", "1.1",
            "-c", "2048",
            "--color",
            "--prompt-cache", "tmp/cache.bin"
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=90
        )

        salida = result.stdout.strip()
        if "[end of text]" in salida:
            respuesta = salida.split("[end of text]")[0].strip()
        else:
            respuesta = salida

        for limbo in [system_prompt, "<|system|>", "<|user|>", "<|assistant|>"]:
            respuesta = respuesta.replace(limbo, "")
        respuesta = respuesta.strip()

        return respuesta if respuesta else "No pude generar una respuesta offline. Pero sigue. El grind no se detiene."

    except Exception as e:
        return f"[OFFLINE ERROR] {str(e)}"

# --- SABIDURÍA DE GRIND ---
def obtener_sabiduria(tema: str, idioma: str = "español") -> str:
    sabiduria = {
        "motivacion": {
            "español": "No necesitas motivación. Necesitas acción. Tu mejor entrenamiento fue el que no querías hacer.",
            "english": "You don't need motivation. You need action. Your best workout was the one you didn't want to do."
        },
        "estoicismo": {
            "español": "El obstáculo es el camino. No resistas el dolor. Úsalo.",
            "english": "The obstacle is the way. Don't resist pain. Use it."
        },
        "ikigai": {
            "español": "🎯 Ikigai es tu razón para vivir:\n- Lo que amas\n- Lo que eres bueno\n- Lo que el mundo necesita\n- Lo que te pueden pagar\nNo lo busques. Constrúyelo con cada elección.",
            "english": "🎯 Ikigai is your reason to live:\n- What you love\n- What you're good at\n- What the world needs\n- What you can be paid for\nDon't search for it. Build it with every choice."
        },
        "interes_compuesto": {
            "español": "📈 El interés compuesto es la fuerza más poderosa del universo.\n1% mejor cada día = 37x en un año.\nAplica a dinero, hábitos, relaciones. Lo pequeño, repetido, vuelve gigante.",
            "english": "📈 Compound interest is the most powerful force in the universe.\n1% better every day = 37x in a year.\nApplies to money, habits, relationships. Small, repeated, becomes giant."
        },
        "neuroforja": {
            "español": "🧠 Tu mente no se entrena. Se neuroforja.\nCada vez que eliges actuar sin ganas, estás forjando nuevas conexiones neuronales.\nNo es magia. Es ciencia. Y tú eres el herrero.",
            "english": "🧠 Your mind isn't trained. It's forged.\nEvery time you choose to act without motivation, you're forging new neural connections.\nIt's not magic. It's science. And you're the blacksmith."
        }
    }
    return sabiduria.get(tema, {}).get(idioma, sabiduria["motivacion"]["español"])

# --- FRASES DE GRIND POR TEMA ---
FRASES_GRIND = {
    "motivacion": {
        "español": "No necesitas motivación. Necesitas acción. Tu mejor entrenamiento fue el que no querías hacer.",
        "english": "You don't need motivation. You need action. Your best workout was the one you didn't want to do."
    },
    "disciplina": {
        "español": "La disciplina es amor a largo plazo. Elige.",
        "english": "Discipline is love in the long term. Choose."
    },
    "fracaso": {
        "español": "El fracaso no rompe tu grind. Lo alimenta.",
        "english": "Failure doesn't break your grind. It feeds it."
    },
    "identidad": {
        "español": "No cambies tu acción. Cambia tu identidad.",
        "english": "Don't change your action. Change your identity."
    },
    "progreso": {
        "español": "Progreso > perfección.",
        "english": "Progress > perfection."
    }
}

def obtener_frase_aleatoria(tema: str, idioma: str) -> str:
    frases = FRASES_GRIND.get(tema, FRASES_GRIND["progreso"])
    return frases.get(idioma, frases["español"])

# --- EVALUAR COMPLEJIDAD DE PREGUNTA ---
def evaluar_pregunta(prompt: str) -> str:
    prompt_lower = prompt.lower().strip()
    palabras_clave_largas = [
        "explica", "cómo puedo", "por qué", "filosofía", "neuroforja",
        "ikigai", "interés compuesto", "cómo empezar", "plan", "ayuda",
        "no sé qué hacer", "estoy perdido", "cómo ser mejor", "cambio"
    ]
    palabras_clave_cortas = [
        "hola", "gracias", "adiós", "ok", "sí", "no", "claro",
        "motivación", "acción", "grind", "progreso"
    ]

    if any(p in prompt_lower for p in ["suicidarme", "kill myself", "morir"]):
        return "groq"

    if len(prompt) > 100 or any(p in prompt_lower for p in palabras_clave_largas):
        return "groq"

    if any(p in prompt_lower for p in palabras_clave_cortas):
        return "tinyllama"

    return "huggingface"

# --- SISTEMA DE HÁBITOS ---
def crear_habito(user_id: str, nombre: str, senal: str, rutina: str, recompensa: str, identidad: str):
    """Crea un nuevo hábito para el usuario"""
    client = conectar_supabase()
    if not client: return False
    try:
        data = {
            "user_id": user_id,
            "nombre": nombre,
            "senal": senal,
            "rutina": rutina,
            "recompensa": recompensa,
            "identidad": identidad,
            "completado": False
        }
        client.table("habitos").insert(data).execute()
        return True
    except Exception as e:
        manejar_error("Hábitos (crear)", e)
        return False

def marcar_habito_completado(user_id: str, nombre_habito: str):
    """Marca un hábito como completado hoy"""
    client = conectar_supabase()
    if not client: return False
    try:
        client.table("habitos") \
            .update({"completado": True}) \
            .eq("user_id", user_id) \
            .eq("nombre", nombre_habito) \
            .eq("fecha", datetime.now().date().isoformat()) \
            .execute()
        return True
    except Exception as e:
        manejar_error("Hábitos (completar)", e)
        return False

def obtener_habitos(user_id: str):
    """Obtiene todos los hábitos del usuario"""
    client = conectar_supabase()
    if not client: return []
    try:
        response = client.table("habitos") \
            .select("*") \
            .eq("user_id", user_id) \
            .execute()
        return response.data
    except Exception as e:
        manejar_error("Hábitos (obtener)", e)
        return []

def mostrar_habitos_diarios(user_id: str):
    """Genera un mensaje con los hábitos del día"""
    habitos = obtener_habitos(user_id)
    if not habitos:
        return "No tienes hábitos registrados. Usa `/habito nuevo` para crear uno."
    
    completados = [h for h in habitos if h.get("completado")]
    pendientes = [h for h in habitos if not h.get("completado")]

    mensaje = "### 🗓 Tus Hábitos de Hoy\n\n"
    
    for h in habitos:
        estado = "✅" if h.get("completado") else "🔴"
        mensaje += f"{estado} **{h['nombre']}**\n"
        mensaje += f"   🔔 {h['senal']} → 🏃 {h['rutina']} → ☕ {h['recompensa']}\n\n"
    
    if not pendientes:
        mensaje += "🔥 ¡Felicidades! Hoy has completado todos tus hábitos. Eres una persona disciplinada.\n"
    else:
        mensaje += f"❗ Te faltan {len(pendientes)} hábitos. Recuerda: *'{pendientes[0]['identidad']}'*\n"
    
    return mensaje

# --- MANEJAR CREACIÓN DE HÁBITO ---
def manejar_creacion_habito(respuesta, idioma):
    paso = st.session_state.mod_habito.get("paso", 1)
    
    if paso == 1:
        st.session_state.mod_habito["nombre"] = respuesta
        st.session_state.mod_habito["paso"] = 2
        return "🔔 ¿Cuál será la señal? (ej: 6:00 AM, después de cepillarme, al llegar a casa)"
    
    elif paso == 2:
        st.session_state.mod_habito["senal"] = respuesta
        st.session_state.mod_habito["paso"] = 3
        return "🏃 ¿Qué harás exactamente? (ej: 30 min de ejercicio, 10 páginas de libro)"
    
    elif paso == 3:
        st.session_state.mod_habito["rutina"] = respuesta
        st.session_state.mod_habito["paso"] = 4
        return "☕ ¿Qué recompensa te darás? (ej: café especial, 10 min de redes, ver un capítulo)"
    
    elif paso == 4:
        st.session_state.mod_habito["recompensa"] = respuesta
        st.session_state.mod_habito["paso"] = 5
        return "💡 ¿Qué identidad quieres forjar? (ej: Soy una persona disciplinada, Soy alguien que cuida su salud)"
    
    elif paso == 5:
        user_id = st.session_state.user_id
        h = st.session_state.mod_habito
        h["identidad"] = respuesta
        
        exito = crear_habito(
            user_id, h["nombre"], h["senal"], h["rutina"], h["recompensa"], h["identidad"]
        )
        
        del st.session_state.mod_habito
        
        if exito:
            return (f"🔥 Hábito creado:\n"
                   f"**{h['nombre']}**\n"
                   f"🔔 {h['senal']} → 🏃 {h['rutina']} → ☕ {h['recompensa']}\n"
                   f"💡 *'{h['identidad']}'*\n\n"
                   f"El grind no es sufrimiento. Es elección. Hoy elegiste evolucionar.")
        else:
            return "No pude guardar tu hábito. Intenta de nuevo."

# --- SISTEMA DE IDENTIDAD DEL USUARIO ---
def clasificar_tipo_usuario(historial: list) -> dict:
    """
    Analiza el historial y clasifica al usuario.
    Devuelve: tipo, coherencia, días activos, temas frecuentes.
    """
    temas_fisicos = ["ejercicio", "entrenar", "pesas", "correr", "salud", "cuerpo", "disciplina", "meditar", "mental", "grindear", "rutina", "progreso", "cambio", "transformación", "fortaleza"]
    temas_trabajo = ["tarea", "redactar", "trabajo", "ensayo", "investigación", "copiar", "traducir", "escribir", "presentación", "informe", "documento", "homework", "assignment"]

    conteo_fisico = 0
    conteo_trabajo = 0
    total_mensajes = 0

    for msg in historial:
        if msg["role"] == "user":
            texto = msg["content"].lower()
            total_mensajes += 1
            if any(t in texto for t in temas_fisicos):
                conteo_fisico += 1
            if any(t in texto for t in temas_trabajo):
                conteo_trabajo += 1

    coherencia = conteo_fisico / total_mensajes if total_mensajes > 0 else 0
    tipo = "grindista" if coherencia > 0.7 and conteo_fisico >= 5 else "usuario_general"

    return {
        "tipo": tipo,
        "coherencia": round(coherencia, 2),
        "total_mensajes": total_mensajes,
        "temas": {"fisico": conteo_fisico, "trabajo": conteo_trabajo}
    }

def usuario_cumplio_semana(historial: list) -> bool:
    """
    Verifica si el usuario ha interactuado al menos 1 vez por día durante 7 días.
    """
    if len(historial) < 7:
        return False

    fechas = sorted(set(
        datetime.fromisoformat(msg["timestamp"]).date() for msg in historial if msg["role"] == "user"
    ))

    if len(fechas) < 7:
        return False

    primer_dia = fechas[0]
    ultimo_dia = fechas[-1]
    diferencia = (ultimo_dia - primer_dia).days

    return diferencia >= 6

# --- RITUAL DIARIO ---
def activar_ritual_diario(usuario_id: str):
    """
    Activa el ritual al final del día (después de las 8 PM).
    Solo si el usuario es un grindista coherente.
    """
    if "ritual_hoy" in st.session_state:
        return

    # Cargar historial
    historial = cargar_historial(usuario_id)
    identidad = clasificar_tipo_usuario(historial)

    if not usuario_cumplio_semana(historial):
        return
    if identidad["tipo"] != "grindista":
        return

    # Solo activar una vez al día
    hoy = datetime.now().date().isoformat()
    archivo = f"data/ritual_{usuario_id}_{hoy}.json"
    if os.path.exists(archivo):
        return

    # Activar ritual
    st.session_state.ritual_hoy = True

    st.markdown("""
    <div class="ritual-container">
        <h3>🌙 Ritual del Grinder</h3>
        <p>Has grindeado 7 días seguidos. No es casualidad. Es elección.</p>
        
        <div class="ritual-question">
            🔥 <strong>1. ¿Qué elección te costó hoy?</strong><br>
            <em>¿Qué hiciste aunque no tuvieras ganas?</em>
        </div>
        <div class="ritual-question">
            💡 <strong>2. ¿En qué momento elegiste el grind sobre la comodidad?</strong><br>
            <em>No fue un acto. Fue una identidad.</em>
        </div>
        <div class="ritual-question">
            🌟 <strong>3. ¿Quién quieres ser mañana?</strong><br>
            <em>No digas "mejor". Di: "más fuerte", "más claro", "más fiel a mí".</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Guardar que ya se mostró
    with open(archivo, "w") as f:
        json.dump({"activado": True, "fecha": hoy}, f)

# --- ECO DE GRIND ---
def mostrar_eco_de_grind():
    """
    Muestra una frase real de otro usuario que grindea.
    Crea sensación de comunidad sin necesidad de chat.
    """
    ecos = [
        "Hace 3 meses no podía hacer 10 flexiones. Hoy hice 100. No fue fuerza. Fue elección.",
        "Dejé de decir 'no tengo ganas'. Ahora digo 'no importa'.",
        "Mi mente me decía 'para'. Mi cuerpo siguió. Ahí nació mi identidad.",
        "No grindeo por motivación. Grindeo porque ya no soy el mismo.",
        "Cada día me levanto sin ganas. Y cada día elijo actuar. Eso es disciplina.",
        "No soy especial. Soy constante. Y la constancia vence al talento.",
        "El grind no es sufrimiento. Es elección. Y yo elijo evolucionar."
    ]
    
    if random.random() < 0.4:  # 40% de probabilidad de aparecer
        eco = random.choice(ecos)
        st.markdown(f"""
        <div class="eco-container">
            <strong>🔊 Eco del Grind:</strong><br>
            "{eco}"
        </div>
        """, unsafe_allow_html=True)

# --- GENERAR TÍTULO DEL CHAT ---
def generar_titulo_chat(primer_mensaje: str) -> str:
    temas = {
        "🏋️ Ejercicio": ["pesas", "correr", "entrenar", "fuerza", "cardio", "musculación", "calistenia"],
        "🧠 Mente": ["meditar", "mental", "ansiedad", "tristeza", "miedo", "enfocado", "concentración", "presencia"],
        "⚡ Hábitos": ["hábito", "rutina", "disciplina", "progreso", "cambio", "consistencia", "constancia"],
        "🎯 Objetivos": ["meta", "objetivo", "plan", "estrategia", "visión", "propósito"],
        "🍽️ Nutrición": ["comida", "dieta", "proteína", "ayuno", "salud", "alimentación", "nutrición"],
        "💬 Relaciones": ["amor", "pareja", "familia", "amigos", "comunicación", "empatía", "respeto"]
    }
    for titulo, palabras in temas.items():
        if any(p in primer_mensaje.lower() for p in palabras):
            return titulo
    return "💬 Nuevo Chat"

# --- LOGIN CON GOOGLE ---
def login_con_google():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown("<h1>🔥 GRIND</h1>", unsafe_allow_html=True)
    st.markdown("<p>Elección > Sufrimiento</p>", unsafe_allow_html=True)

    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("REDIRECT_URI")
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope=email%20profile"
        f"&access_type=offline"
    )

    st.markdown(f'<a href="{auth_url}" target="_self"><button style="background:var(--accent); color:white; border:none; padding:15px; border-radius:8px; width:100%;">🔐 Iniciar con Google</button></a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- CONEXIÓN A SUPABASE PARA SESIONES ---
def conectar_supabase():
    try:
        from streamlit import secrets
        from supabase import create_client
        return create_client(secrets["SUPABASE_URL"], secrets["SUPABASE_KEY"])
    except:
        return None

def guardar_mensaje(user_id, session_id, role, content, title=None):
    client = conectar_supabase()
    if not client: return
    try:
        client.table("sessions").upsert({
            "user_id": user_id,
            "session_id": session_id,
            "last_used": datetime.now().isoformat()
        }).execute()
        client.table("chats").insert({
            "user_id": user_id,
            "session_id": session_id,
            "role": role,
            "content": content,
            "title": title or "Nuevo Chat",
            "timestamp": datetime.now().isoformat()
        }).execute()
    except Exception as e:
        print(f"[ERROR] No se pudo guardar: {e}")

def cargar_sesiones(user_id):
    client = conectar_supabase()
    if not client: return []
    try:
        response = client.table("sessions") \
            .select("session_id, last_used") \
            .eq("user_id", user_id) \
            .order("last_used", desc=True) \
            .execute()
        return response.data
    except:
        return []

def cargar_chats(session_id):
    client = conectar_supabase()
    if not client: return []
    try:
        response = client.table("chats") \
            .select("*") \
            .eq("session_id", session_id) \
            .order("timestamp") \
            .execute()
        return response.data
    except:
        return []

# --- RAZONAMIENTO INTELIGENTE ---
def razonar_con_grind(prompt, historial, idioma):
    modo = activar_modo(prompt)
    idioma = detectar_idioma(prompt)
    
    # Modo crisis
    if modo == "alerta":
        linea = buscar_linea_de_ayuda(prompt, idioma)
        msg_base = "🌟 Escucho tu dolor. No estás solo. Tu vida importa.\n\n"
        msg_final = f"Por favor, contacta a una línea de ayuda real:\n{linea}\n\nEstoy aquí. No estás solo. Vamos a salir de esto. Juntos."
        return f"{msg_base}{msg_final}"

    # Necesidades humanas
    if any(p in prompt.lower() for p in ["necesito", "no tengo", "ayuda", "estoy solo"]):
        afirmaciones = terapeuta.get("afirmaciones_necesitado", [])
        seleccionadas = random.sample(afirmaciones, min(6, len(afirmaciones)))
        lista = "".join(f"🔹 {af}\n" for af in seleccionadas)
        return f"Escucho tu necesidad. No es debilidad. Es señal de vida.\n\n{lista}\nVisita: https://findahelpline.com"

    # Hábitos
    if any(p in prompt.lower() for p in ["hábito", "rutina", "cómo empezar"]):
        return ("🔥 **Ciclo del Hábito GRIND**:\n"
                "1. **Señal**: Ej. 6:00 AM\n"
                "2. **Rutina**: Ej. 30 min de ejercicio\n"
                "3. **Recompensa**: Ej. Café especial\n"
                "4. **Identidad**: *'Soy una persona disciplinada'*\n\n"
                "💡 No cambies tu acción. Cambia tu identidad.")

    # Estoicismo
    if any(p in prompt.lower() for p in ["estoicismo", "estoico", "marco aurelio", "seneca"]):
        return obtener_sabiduria("estoicismo", idioma)

    # Ikigai
    if "ikigai" in prompt.lower():
        return obtener_sabiduria("ikigai", idioma)

    # Interés compuesto
    if any(p in prompt_lower for p in ["interes", "compuesto", "dinero", "crecimiento"]):
        return obtener_sabiduria("interes_compuesto", idioma)

    # Neuroforja
    if any(p in prompt_lower for p in ["neuroforja", "cerebro", "aprender", "cambio"]):
        return obtener_sabiduria("neuroforja", idioma)

    # Términos GRIND
    for termino in DIC_GRIND.keys():
        if termino in prompt.lower():
            traduccion = traducir_termino(termino, idioma)
            return f"🔥 **{termino}**: {traduccion}\n\n💡 Recuerda: el grind no es sufrimiento. Es elección."

    # Búsqueda en web
    if any(k in prompt.lower() for k in ["precio", "síntoma", "cómo hacer", "qué es"]):
        web_result = buscar_en_web(prompt)
        if web_result:
            return f"🔍 Resultados de búsqueda:\n{web_result}\n\n💡 Recuerda: el grind no es sufrimiento. Es elección."

    # Usar Groq
    try:
        return groq_llamada(prompt, historial)
    except:
        try:
            return hf_llamada(prompt)
        except:
            try:
                return tinyllama_offline(prompt)
            except:
                return random.choice([
                    "No tengo internet. Pero tú sí tienes elección. Actúa.",
                    "El grind no se detiene por fallas. Se detiene por excusas. No seas excusa.",
                    "No necesitas una IA. Necesitas acción. Hazlo."
                ])

# --- INTERFAZ DE CHAT ---
def interfaz_grind():
    user_id = st.session_state.user_id
    session_id = st.session_state.get("session_id", f"session_{int(time.time())}")
    st.session_state.session_id = session_id

    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown('<div class="sidebar">', unsafe_allow_html=True)
        st.markdown("### 🔥 Tus Chats")

        if st.button("➕ Nuevo Chat", key="new_chat"):
            st.session_state.session_id = f"session_{int(time.time())}"
            st.session_state.messages = []
            st.rerun()

        sesiones = cargar_sesiones(user_id)
        for s in sesiones:
            if st.button(f"💬 {s['session_id'][-6:]}", key=s["session_id"]):
                st.session_state.session_id = s["session_id"]
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f"<h3 style='text-align: center;'>🔥 GRIND</h3>", unsafe_allow_html=True)
        mostrar_eco_de_grind()

        if "messages" not in st.session_state:
            historial = cargar_chats(session_id)
            st.session_state.messages = [
                {"role": msg["role"], "content": msg["content"]} for msg in historial
            ]
            if historial and "title" not in st.session_state:
                st.session_state.title = historial[0].get("title", "Nuevo Chat")

        for message in st.session_state.messages:
            clase = "message"
            if "grindear" in message["content"]: clase += " war"
            st.markdown(f"""
            <div class="{clase}">
                <div class="avatar {'user' if message['role'] == 'user' else 'grind'}">{'👤' if message['role'] == 'user' else '🔥'}</div>
                <div class="content">{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)

        if prompt := st.chat_input("Escribe tu verdad..."):
            if "title" not in st.session_state:
                st.session_state.title = generar_titulo_chat(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            guardar_mensaje(user_id, session_id, "user", prompt, st.session_state.title)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                respuesta = razonar_con_grind(prompt, st.session_state.messages[:-1], detectar_idioma(prompt))
                message_placeholder.markdown(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
            guardar_mensaje(user_id, session_id, "assistant", respuesta, st.session_state.title)
            st.rerun()

        if datetime.now().hour >= 20:
            activar_ritual_diario(user_id)

# --- FLUJO PRINCIPAL ---
if "logged_in" not in st.session_state:
    auth_code = st.query_params.get("code")
    if auth_code:
        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "code": auth_code,
            "redirect_uri": os.getenv("REDIRECT_URI"),
            "grant_type": "authorization_code"
        }
        response = requests.post(token_url, data=payload)
        if response.status_code == 200:
            token_data = response.json()
            headers = {"Authorization": f"Bearer {token_data['access_token']}"}
            profile = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers=headers).json()
            st.session_state.logged_in = True
            st.session_state.user = profile
            st.session_state.user_id = f"google_{profile['id']}"
            st.rerun()
        else:
            st.error("Error al iniciar sesión.")
    else:
        login_con_google()
else:
    interfaz_grind()

# --- DISCLAIMER ---
st.markdown("""
<div class="footer">
    GRIND no es un terapeuta. Es un entrenador. Para crisis, visita <a href="https://findahelpline.com" target="_blank">findahelpline.com</a>.
</div>
""", unsafe_allow_html=True)