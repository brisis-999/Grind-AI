# app.py - GRIND 15000: La IA Entrenadora Completa
# "El grind no es sufrimiento. Es elección."

# --- ¡CRÍTICO! Reemplazar sqlite3 por pysqlite3 para Streamlit Cloud ---
try:
    import sys
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

import streamlit as st
from utils.helpers import detectar_idioma, cargar_json, manejar_error
from typing import Dict, Any
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="GRIND CORE",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- ESTILO CHATGPT (CSS) ---
def aplicar_estilo():
    with open("ui/style.css") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

aplicar_estilo()

# --- FUNCIONES DE CARGA DE CONOCIMIENTO ---
@st.cache_data
def cargar_terapeuta() -> Dict[Any, Any]:
    return cargar_json("modelo_mental/terapeuta/terapeuta.json")

@st.cache_data
def cargar_modo_alerta() -> Dict[Any, Any]:
    return cargar_json("modelo_mental/crisis/modo_alerta.json")

@st.cache_data
def cargar_findahelpline() -> Dict[Any, Any]:
    return cargar_json("fuentes/findahelpline.json")

# --- ESTADO DE SESIÓN ---
if "logo_visible" not in st.session_state:
    st.session_state.logo_visible = True
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_user" not in st.session_state:
    st.session_state.current_user = "Usuario"

# --- MOSTRAR LOGO ANIMADO (Inicio) ---
if st.session_state.logo_visible:
    st.markdown("""
    <div class="logo-container" id="logo-container">
        <div class="logo">GRIND</div>
        <p class="tagline">Tu entrenador de élite</p>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.logo_visible = False
    st.rerun()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(f"### 🌟 Hola, {st.session_state.current_user}")
    if st.button("🔄 Nueva conversación"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("### 🔧 Opciones")
    if st.button("Salir"):
        st.session_state.logged_in = False
        st.rerun()

# --- CARGAR DATOS ---
try:
    terapeuta = cargar_terapeuta()
    modo_alerta = cargar_modo_alerta()
    findahelpline = cargar_findahelpline()
except Exception as e:
    manejar_error("Error al cargar datos", e)

# --- DETECTAR IDIOMA ---
if st.session_state.messages:
    ultimo = st.session_state.messages[-1]["content"]
    idioma = detectar_idioma(ultimo)
else:
    idioma = "español"

# --- MODO CRISIS AUTOMÁTICO ---
def modo_crisis():
    mensajes_crisis = [
        "suicidarme", "kill myself", "no quiero vivir", "me quiero morir",
        "no puedo más", "estoy roto", "end it all", "quiero morir"
    ]
    if any(p in ultimo.lower() for p in mensajes_crisis):
        msg = modo_alerta["respuesta_base"][idioma]
        final = modo_alerta["mensaje_final"][idioma]
        enlace = f"[{findahelpline['sitio']}]({findahelpline['sitio']})"
        respuesta = f"{msg}\n\n{final.replace('https://findahelpline.com', enlace)}"
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        return True
    return False

# Activar modo crisis
if st.session_state.messages and modo_crisis():
    st.rerun()

# --- MOSTRAR MENSAJES DEL CHAT ---
for message in st.session_state.messages:
    role = "user" if message["role"] == "human" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"])

# --- INPUT DEL USUARIO ---
if prompt := st.chat_input("Escribe tu verdad..."):
    st.session_state.messages.append({"role": "human", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- RESPONDER CON MENTE PROPIA ---
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        respuesta = None

        # 1. Modo crisis (ya está arriba, pero por si acaso)
        for palabra in ["suicidarme", "kill myself", "no quiero vivir"]:
            if palabra in prompt.lower():
                respuesta = f"🌟 Escucho tu dolor. No estás solo. Tu vida importa.\n\nPor favor, visita [findahelpline.com](https://findahelpline.com) para encontrar ayuda real en tu idioma."
                break

        # 2. Usar terapeuta.json para necesidades
        if not respuesta and any(p in prompt.lower() for p in ["necesito", "no tengo", "estoy solo"]):
            afirmaciones = terapeuta.get("afirmaciones_necesitado", [])
            seleccionadas = afirmaciones[:6]
            lista = "\n".join(f"🔹 {af}" for af in seleccionadas)
            respuesta = f"Escucho tu necesidad. No es debilidad. Es señal de vida.\n\n{lista}\n\nVisita: https://findahelpline.com"

        # 3. Motivación
        if not respuesta and any(p in prompt.lower() for p in ["motivacion", "motivación", "ganas", "animo"]):
            respuesta = "No necesitas motivación. Necesitas acción. Tu mejor entrenamiento fue el que no querías hacer."

        # 4. Hábitos
        if not respuesta and "hábito" in prompt.lower():
            respuesta = "Ciclo del hábito:\n1. Señal → 2. Rutina → 3. Recompensa → 4. Identidad.\nNo cambies tu acción. Cambia tu identidad."

        # 5. Default: GRIND habla con verdad dura
        if not respuesta:
            frases = [
                "No estás cansado. Estás cómodo. Y el crecimiento vive fuera de la comodidad.",
                "Tu mente te miente. Tu cuerpo obedece.",
                "El grind no es sufrimiento. Es elección.",
                "No necesitas más energía. Necesitas más elección."
            ]
            import random
            respuesta = random.choice(frases)

        # Efecto typing
        words = respuesta.split()
        full_response = ""
        for i in range(len(words) + 1):
            current_text = " ".join(words[:i])
            message_placeholder.markdown(f"<div class='assistant-message'>{current_text}▌</div>", unsafe_allow_html=True)
            time.sleep(0.05)
        message_placeholder.markdown(f"<div class='assistant-message'>{respuesta}</div>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": respuesta})
    st.rerun()

# --- DISCLAIMER (Opcional) ---
st.markdown("""
<div style="text-align: center; color: #B0B0B0; font-size: 12px; margin-top: 20px;">
    GRIND no es un terapeuta. Es un entrenador. Para crisis, visita <a href="https://findahelpline.com" target="_blank">findahelpline.com</a>.
</div>
""", unsafe_allow_html=True)