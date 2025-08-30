# app.py - GRIND 15000: La IA Entrenadora Completa
# "El grind no es sufrimiento. Es elección."

# --- ¡CRÍTICO! Reemplazar sqlite3 por pysqlite3 para Streamlit Cloud ---
try:
    import sys
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

# --- CARGAR MÓDULO UTILS DE FORMA SEGURA ---
import sys
import os

# Asegurarse de que el directorio actual esté en el path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from utils.helpers import detectar_idioma, cargar_json, manejar_error
    print("✅ Módulo 'utils.helpers' cargado correctamente")
except ImportError as e:
    print(f"❌ Error al importar utils.helpers: {e}")

    # Definir funciones fallback
    def detectar_idioma(texto: str) -> str:
        return "español"

    def cargar_json(ruta: str) -> dict:
        print(f"[WARNING] No se pudo cargar {ruta}")
        return {}

    def manejar_error(mensaje: str, error=None):
        print(f"[ERROR] {mensaje}")
        return "Lo siento, no pude procesar tu solicitud."

# --- CONFIGURACIÓN DE PÁGINA ---
import streamlit as st

st.set_page_config(
    page_title="GRIND CORE",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- ESTILO CHATGPT (CSS) ---
def aplicar_estilo():
    try:
        with open("ui/style.css") as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.markdown(
            """
            <style>
            body { background-color: #343541; color: #ECECF1; }
            .stChatMessage { max-width: 800px; margin: 0 auto; }
            </style>
            """,
            unsafe_allow_html=True
        )

aplicar_estilo()

# --- ESTADO DE SESIÓN ---
if "logo_visible" not in st.session_state:
    st.session_state.logo_visible = True
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CARGAR DATOS (con manejo de errores) ---
try:
    terapeuta = cargar_json("modelo_mental/terapeuta/terapeuta.json")
    findahelpline = cargar_json("fuentes/findahelpline.json")
except Exception as e:
    manejar_error("Error al cargar datos externos", e)
    terapeuta = {}
    findahelpline = {"sitio": "https://findahelpline.com"}

# --- MOSTRAR LOGO ANIMADO (Inicio) ---
if st.session_state.logo_visible:
    st.markdown("""
    <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                background-color: #343541; display: flex; flex-direction: column; 
                justify-content: center; align-items: center; z-index: 1000;">
        <div style="font-size: 60px; font-weight: 700; color: white;">GRIND</div>
        <p style="margin-top: 10px; font-size: 18px; color: #10A37F; font-style: italic;">
            Tu entrenador de élite
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Botón oculto para avanzar después de 2 segundos
    if st.button("Cargar Chat", key="btn_cargar", help="Este botón se activa automáticamente"):
        st.session_state.logo_visible = False

    # Inyecta JavaScript para hacer clic automáticamente después de 2 segundos
    st.markdown("""
    <script>
    setTimeout(function() {
        const buttons = window.parent.document.querySelectorAll('button');
        buttons.forEach(button => {
            if (button.innerText.includes('Cargar Chat')) {
                button.click();
            }
        });
    }, 2000);
    </script>
    """, unsafe_allow_html=True)

    # Detiene la ejecución aquí hasta que se cierre el logo
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🌟 Usuario")
    if st.button("🔄 Nueva conversación"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("### 🔧 Opciones")
    if st.button("Salir"):
        st.session_state.logged_in = False
        st.rerun()

# --- DETECTAR IDIOMA ---
idioma = "español"
if st.session_state.messages:
    ultimo = st.session_state.messages[-1]["content"]
    idioma = detectar_idioma(ultimo)

# --- MODO CRISIS AUTOMÁTICO ---
def modo_crisis():
    mensajes_crisis = [
        "suicidarme", "kill myself", "no quiero vivir", "me quiero morir",
        "no puedo más", "estoy roto", "end it all", "quiero morir", "kill me"
    ]
    if any(p in ultimo.lower() for p in mensajes_crisis):
        msg_base = "🌟 Escucho tu dolor. No estás solo. Tu vida importa."
        enlace = f"[{findahelpline['sitio']}]({findahelpline['sitio']})"
        msg_final = f"Por favor, visita {enlace} para encontrar ayuda real en tu idioma."
        respuesta = f"{msg_base}\n\n{msg_final}"
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
import time

if prompt := st.chat_input("Escribe tu verdad..."):
    st.session_state.messages.append({"role": "human", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- RESPONDER CON MENTE PROPIA ---
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        respuesta = None

        # 1. Modo crisis
        for palabra in ["suicidarme", "kill myself", "no quiero vivir"]:
            if palabra in prompt.lower():
                respuesta = f"🌟 Escucho tu dolor. No estás solo. Tu vida importa.\n\nPor favor, visita [findahelpline.com](https://findahelpline.com) para encontrar ayuda real en tu idioma."
                break

        # 2. Necesidades humanas
        if not respuesta and any(p in prompt.lower() for p in ["necesito", "no tengo", "ayuda"]):
            afirmaciones = terapeuta.get("afirmaciones_necesitado", [
                "Que necesita amor.", "Que necesita esperanza.", "Que necesita dignidad."
            ])
            seleccionadas = afirmaciones[:6]
            lista = "\n".join(f"🔹 {af}" for af in seleccionadas)
            respuesta = f"Escucho tu necesidad.\n\n{lista}\n\nVisita: https://findahelpline.com"

        # 3. Motivación
        if not respuesta and any(p in prompt.lower() for p in ["motivacion", "motivación", "ganas", "animo"]):
            respuesta = "No necesitas motivación. Necesitas acción. Tu mejor entrenamiento fue el que no querías hacer."

        # 4. Hábitos
        if not respuesta and "hábito" in prompt.lower():
            respuesta = "Ciclo del hábito:\n1. Señal → 2. Rutina → 3. Recompensa → 4. Identidad.\nNo cambies tu acción. Cambia tu identidad."

        # 5. Default: GRIND responde con verdad
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
            message_placeholder.markdown(f"<div style='white-space: pre-line;'>{current_text}▌</div>", unsafe_allow_html=True)
            time.sleep(0.05)
        message_placeholder.markdown(f"<div style='white-space: pre-line;'>{respuesta}</div>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": respuesta})
    st.rerun()

# --- DISCLAIMER ---
st.markdown("""
<div style="text-align: center; color: #B0B0B0; font-size: 12px; margin-top: 20px;">
    GRIND no es un terapeuta. Es un entrenador. Para crisis, visita <a href="https://findahelpline.com" target="_blank">findahelpline.com</a>.
</div>
""", unsafe_allow_html=True)