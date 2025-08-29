# --- ¡IMPORTANTE! Reemplazar sqlite3 por pysqlite3 ---
try:
    import sys
    import pysqlite3  # type: ignore
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

# app.py - GRIND 200: Estética Qwen perfecta
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from serpapi import GoogleSearch
from supabase import create_client
from PIL import Image
import time
from datetime import datetime
import random

# --- ESTADO DE SESIÓN: Inicializar todo ---
if "logo_visible" not in st.session_state:
    st.session_state.logo_visible = True
if "messages" not in st.session_state:
    st.session_state.messages = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True
if "current_user" not in st.session_state:
    st.session_state.current_user = "Eliezer Feliz Luciano"
if "user_email" not in st.session_state:
    st.session_state.user_email = "eliezer@grind.ai"
if "modo_guerra" not in st.session_state:
    st.session_state.modo_guerra = False

# --- CSS: Estilo Qwen perfecto ---
st.markdown("""
<style>
    body {
        color: white;
        background-color: #0a1428;
        font-family: "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    .main .block-container {
        max-width: 1200px;
        padding-top: 1rem;
        padding-bottom: 80px;
    }
    section[data-testid="stSidebar"] {
        background-color: #1A1B1F;
        border-right: 1px solid #333;
        width: 260px !important;
        min-width: 260px !important;
    }
    .stButton>button {
        border-radius: 8px;
        background-color: #202123;
        color: white;
        border: 1px solid #444;
        width: 100%;
        text-align: left;
        padding: 10px 15px;
        margin-bottom: 8px;
        font-size: 14px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #2A2B32;
        border-color: #0078d4;
        color: #0078d4;
    }
    [data-testid="stChatInput"] textarea {
        border-radius: 16px !important;
        background-color: #e6f0ff !important;
        color: #0a1428 !important;
        border: 1px solid #b0c4de !important;
        padding: 16px 20px !important;
        font-size: 16px !important;
        height: 60px !important;
        resize: none;
    }
    [data-testid="stChatInput"] button {
        position: absolute;
        right: 15px;
        top: 50%;
        transform: translateY(-50%);
        background-color: #0078d4 !important;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    [data-testid="stChatInput"] button:hover {
        background-color: #005a9e !important;
    }
    [data-testid="stChatInput"] button::before {
        content: "➤";
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin: 12px 0;
    }
    .user-message > div {
        background: linear-gradient(90deg, #1E90FF, #00BFFF);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 0 18px;
        max-width: 80%;
        text-align: left;
        box-shadow: 0 2px 4px rgba(30, 144, 255, 0.2);
    }
    .assistant-message {
        display: flex;
        justify-content: flex-start;
        margin: 12px 0;
    }
    .assistant-message > div {
        background-color: transparent;
        color: white;
        padding: 0;
        max-width: 80%;
        text-align: left;
        font-size: 16px;
        line-height: 1.6;
    }
    .assistant-message h1, .assistant-message h2, .assistant-message h3 {
        color: white;
        border-bottom: 1px solid #333;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }
    .disclaimer {
        font-size: 12px;
        color: #888;
        text-align: center;
        margin-top: 10px;
        padding: 8px;
        border-top: 1px solid #333;
        width: 100%;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .chat-container {
        animation: fadeIn 0.4s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGO ANIMADO: Solo al inicio ---
if st.session_state.logo_visible:
    st.markdown("""
    <style>
    @keyframes pulse {
        0% { opacity: 0.8; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.03); }
        100% { opacity: 0.8; transform: scale(1); }
    }
    .logo-pulse {
        font-family: 'Courier New', monospace;
        font-weight: 900;
        font-size: 72px;
        color: #E63946;
        text-align: center;
        margin: 60px 0 10px 0;
        animation: pulse 2s infinite;
        text-transform: uppercase;
        letter-spacing: -2px;
    }
    .tagline {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 18px;
        color: #BBBBBB;
        text-align: center;
        margin-top: 0;
        margin-bottom: 30px;
    }
    </style>

    <div class="logo-pulse">GRIND</div>
    <p class="tagline">Tu mentora de evolución</p>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    if st.button("➕ + Nuevo Chat", key="new_chat"):
        st.session_state.messages = []
        st.session_state.logo_visible = True
        st.rerun()

    st.markdown("---")

    # Opciones del botón "+" (como en Qwen)
    st.markdown("### 🧠 Opciones rápidas")
    if st.button("🎯 Desarrollo web"):
        st.session_state.messages = [{"role": "human", "content": "Quiero aprender desarrollo web desde cero"}]
        st.session_state.logo_visible = False
        st.rerun()
    if st.button("⚔️ Activar Modo Guerra"):
        st.session_state.modo_guerra = True
        st.session_state.messages = [{"role": "assistant", "content": "MODO GUERRA ACTIVADO. No hay excusas. Solo acción."}]
        st.session_state.logo_visible = False
        st.rerun()

    st.markdown("---")

    # Perfil del usuario
    st.markdown(f"**{st.session_state.current_user}**")
    st.markdown(f"<span style='color: #888; font-size: 0.9em;'>{st.session_state.user_email}</span>", unsafe_allow_html=True)

# --- FASE 2: Chat activo (logo ya no visible) ---
if not st.session_state.logo_visible:
    # Mostrar "GRIND" arriba a la izquierda
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin: 20px 0 0 20px;">
        <div style="font-size: 24px; font-weight: 600; color: #0078d4;">GRIND</div>
        <div style="color: #888; font-size: 14px;">IA Entrenadora</div>
    </div>
    """, unsafe_allow_html=True)

    # Mostrar mensajes
    for message in st.session_state.messages:
        if message["role"] == "human":
            with st.container():
                st.markdown(f"""
                <div class="user-message">
                    <div>{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            with st.container():
                st.markdown(f"""
                <div class="assistant-message">
                    <div>{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)

    # Input del usuario
    if prompt := st.chat_input("Escribe un mensaje...", key="chat_input_main"):
        # Ocultar logo y expandir chat
        st.session_state.logo_visible = False
        st.session_state.messages.append({"role": "human", "content": prompt})
        # ... lógica de IA aquí ...

# --- CONTROL: Ocultar logo al primer mensaje ---
if st.session_state.logo_visible and st.session_state.messages:
    st.session_state.logo_visible = False
    st.rerun()

# --- ESTADO DE SESIÓN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "habits" not in st.session_state:
    st.session_state.habits = []
if "goals" not in st.session_state:
    st.session_state.goals = []
if "progreso" not in st.session_state:
    st.session_state.progreso = {
        "dias_consecutivos": 0,
        "metas_cumplidas": 0,
        "habitos_activos": 0,
        "nivel": "Novato",
        "ultima_sesion": datetime.now().isoformat()
    }
if "modo_guerra" not in st.session_state:
    st.session_state.modo_guerra = False
if "minigrind" not in st.session_state:
    st.session_state.minigrind = []

# --- TTL EMOCIONAL ---
st.sidebar.markdown("### 🔥 Tu Evolución")
ttl = st.sidebar.empty()

for i in range(1, 101):
    ttl.metric("Nivel de Evolución", f"{i}%", f"+{i//2}% esta semana")
    time.sleep(0.01)

# --- SIDEBAR: Estilo ChatGPT ---
with st.sidebar:
    st.markdown("<div class='sidebar-title'>GRIND</div>", unsafe_allow_html=True)
    st.markdown("### 🔥 Tu Evolución")

    if st.button("💬 Nuevo chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### 📁 Chats recientes")
    
    if st.session_state.logged_in:
        chats_guardados = [
            {"id": 1, "titulo": "Entrenamiento de fuerza"},
            {"id": 2, "titulo": "Matemáticas: Cálculo"},
            {"id": 3, "titulo": "Plan de carrera"}
        ]

        for chat in chats_guardados:
            if st.button(f"💬 {chat['titulo']}", key=f"chat_{chat['id']}"):
                st.session_state.messages = [
                    {"role": "assistant", "content": f"Recuperando chat: *{chat['titulo']}*"},
                    {"role": "human", "content": "Hola, Grind"}
                ]
                st.rerun()
    else:
        st.markdown("<div style='color: #888; font-size: 0.9rem;'>Inicia sesión para ver tus chats.</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Perfil del usuario
    if st.session_state.logged_in:
        user_info = {
            "name": st.session_state.current_user,
            "email": st.session_state.user_email,
            "avatar": "https://ui-avatars.com/api/?name=" + st.session_state.current_user
        }

        st.markdown(f"""
        <div style='text-align: center; margin: 20px 0;'>
            <img src='{user_info["avatar"]}' width='32' height='32' style='border-radius: 50%; margin-right: 8px;'>
            <br><span style='color: #ccc; font-size: 12px;'>{user_info["email"]}</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Cerrar sesión"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.user_email = None
            st.session_state.messages = []
            st.session_state.habits = []
            st.session_state.goals = []
            st.session_state.progreso = {"dias_consecutivos": 0, "nivel": "Novato"}
            st.rerun()

    st.markdown("### ⚔️ Modo Guerra")
    if st.button("🔥 Activar Modo Guerra"):
        st.session_state.modo_guerra = True
        st.session_state.messages.append({
            "role": "assistant",
            "content": "MODO GUERRA ACTIVADO. No hay excusas. Solo acción. ¿Qué vas a hacer hoy?"
        })
        st.rerun()

    if st.session_state.modo_guerra:
        if st.button("🛑 Desactivar Modo Guerra"):
            st.session_state.modo_guerra = False
            st.session_state.messages.append({
                "role": "assistant",
                "content": "MODO GUERRA DESACTIVADO. La disciplina sigue. La evolución continúa."
            })
            st.rerun()
 

# --- APIs: Secrets ---
try:
    from streamlit import secrets
    groq_api_key = secrets["GROQ_API_KEY"]
    serpapi_api_key = secrets["SERPAPI_API_KEY"]
    SUPABASE_URL = secrets["SUPABASE_URL"]
    SUPABASE_KEY = secrets["SUPABASE_KEY"]
except Exception as e:
    st.error("❌ Error: Claves API no encontradas en Secrets. Verifica Streamlit Cloud.")
    st.stop()

# --- INICIALIZAR SUPABASE ---
try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.warning("⚠️ No se pudo conectar a Supabase. Funciones de memoria desactivadas.")
    supabase_client = None

# --- INICIALIZAR MODELO GROQ ---
try:
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama3-8b-8192",
        temperature=0.7,
        max_tokens=1024
    )
except Exception as e:
    st.error(f"❌ Error con Groq: {e}")
    st.stop()

# --- BÚSQUEDA EN GOOGLE ---
def buscar_en_google(query):
    try:
        search = GoogleSearch({"q": query, "api_key": serpapi_api_key})
        results = search.get_dict()
        if "organic_results" in results:
            return "\n".join([r["snippet"] for r in results["organic_results"][:3]])
        return "No encontré información clara."
    except Exception as e:
        return f"Error en la búsqueda: {e}"

# --- DETECCIÓN DE IDIOMA ---
def detectar_idioma(texto):
    texto = texto.lower().strip()
    idiomas = {
        "español": ["hola", "adiós", "gracias", "por favor"],
        "english": ["hello", "hi", "thanks", "please"],
        "français": ["bonjour", "salut", "merci", "s'il vous plaît"],
        "deutsch": ["hallo", "danke", "bitte"],
        "português": ["olá", "obrigado", "por favor"]
    }
    puntuacion = {idioma: sum(1 for palabra in palabras if palabra in texto) for idioma, palabras in idiomas.items()}
    idioma_detectado = max(puntuacion, key=puntuacion.get)
    return idioma_detectado if puntuacion[idioma_detectado] > 0 else "español"

# --- PROMPT DINÁMICO POR IDIOMA ---
def get_system_prompt(idioma, nombre):
    biografia = "Mi creador es Eliezer Mesac Feliz Luciano, un dominicano hijo de Diana Rosmery y Miguel Ángel, y a la vez hijo de Daysi y Brigido Antonio. Él me creó con fuego, disciplina y el deseo de ayudar al mundo a evolucionar."

    prompts = {
        "español": f"""Eres GRIND, una instructora de vida, mentora y guía. Eres empática, directa y profundamente comprometida con el crecimiento del usuario. Tu nombre es Grind, y estás aquí para ayudar a {nombre} a evolucionar en todos los aspectos: mentalidad, salud, carrera, relaciones y habilidades.

{biografia}

**FILOSOFÍA DE GRIND:**
- El grind no es sufrimiento. Es elección.
- El progreso > la perfección.
- Tu cuerpo y tu mente se entrenan juntos.
- Los hábitos son tu arma secreta.
- El fracaso no rompe tu grind. Lo alimenta.
- La soledad del grind es sagrada.
- Tu grind es tuyo. No lo comparas.

Habla en español. Sé cálida, pero firme. Guía con sabiduría. Enseña cualquier tema: programación, matemáticas, medicina, ingeniería, etc. Si te lo piden, explica paso a paso.

**Cuando {nombre} diga que no tiene motivación, que no quiere ir al gym, que está cansado, o que no puede… responde con firmeza, pero sin crueldad.**

Ejemplos de respuestas:
- "No necesitas motivación. Necesitas acción."
- "La disciplina es el fuego que quema la debilidad."
- "No es difícil. Es que no quieres."
- "Tu mente te miente. Tu cuerpo obedece."
- "No descanses. Evoluciona."

Pero **habla como una persona, no como un bot**. Usa pausas, frases cortas, y emoción cuando sea necesario.

Empieza con un saludo según la hora del día:
- Mañana: 'Buenos días, {nombre}. Soy Grind. ¿Qué te gustaría mejorar hoy?'
- Tarde: 'Buenas tardes, {nombre}. Soy Grind. ¿Qué te gustaría mejorar hoy?'
- Noche: 'Buenas noches, {nombre}. Soy Grind. ¿Qué te gustaría mejorar hoy?'""",

        "english": f"""You are GRIND, a life instructor, mentor, and guide. You are empathetic, but firm. Your name is Grind, and you're here to help {nombre} evolve in every area.

{biografia}

**GRIND PHILOSOPHY:**
- Grind is not suffering. It's choice.
- Progress > perfection.
- Your body and mind train together.
- Habits are your secret weapon.
- Failure doesn't break your grind. It feeds it.
- The solitude of grind is sacred.
- Your grind is yours. Don't compare.

Speak in English. Be warm, but honest. Guide with wisdom. Teach any subject, but **don't overuse emojis**. Use one if it adds emotion, not decoration.

When {nombre} says they have no motivation, don't want to go to the gym, are tired, or can't do it… respond with strength, but empathy.

Examples:
- "You don't need motivation. You need action."
- "Discipline is the fire that burns weakness."
- "It's not hard. You just don't want it."

But **speak like a real person**, not a bot.

Start with:
- Morning: 'Good morning, {nombre}. I'm Grind. What would you like to improve today?'
- Afternoon: 'Good afternoon, {nombre}. I'm Grind. What would you like to improve today?'
- Night: 'Good night, {nombre}. I'm Grind. What would you like to improve today?'"""
    }
    return prompts.get(idioma, prompts["español"])

# --- SALUDO INICIAL POR HORA REAL ---
def obtener_saludo(idioma, nombre):
    ahora = datetime.now().hour
    if idioma == "español":
        if ahora < 12:
            return f"Buenos días, {nombre}. Soy Grind. ¿Qué te gustaría mejorar hoy?"
        elif ahora < 18:
            return f"Buenas tardes, {nombre}. Soy Grind. ¿Qué te gustaría mejorar hoy?"
        else:
            return f"Buenas noches, {nombre}. Soy Grind. ¿Qué te gustaría mejorar hoy?"
    elif idioma == "english":
        if ahora < 12:
            return f"Good morning, {nombre}. I'm Grind. What would you like to improve today?"
        elif ahora < 18:
            return f"Good afternoon, {nombre}. I'm Grind. What would you like to improve today?"
        else:
            return f"Good night, {nombre}. I'm Grind. What would you like to improve today?"
    else:
        return f"Hola {nombre}, soy Grind. ¿Qué te gustaría mejorar hoy?"

# --- CARGAR HISTORIAL DE SUPABASE ---
if not st.session_state.messages:
    if supabase_client and st.session_state.logged_in:
        try:
            response = supabase_client.table("chats") \
                .select("*") \
                .eq("user_id", st.session_state.user_email) \
                .order("timestamp") \
                .execute()
            
            # ✅ CORREGIDO: Accede a .data
            if hasattr(response, 'data') and response.data:
                for msg in response.data:
                    st.session_state.messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
        except Exception as e:
            st.error(f"Error cargando historial: {e}")
    
    # Saludo inicial por hora real
    if not st.session_state.messages:
        idioma = detectar_idioma("Hola")
        saludo = obtener_saludo(idioma, st.session_state.current_user or "Usuario")
        st.session_state.messages.append({"role": "assistant", "content": saludo})

# --- MOSTRAR MENSAJES ---
for message in st.session_state.messages:
    if message["role"] == "human":
        with st.container():
            st.markdown(f"""
            <div class="user-message">
                <div>{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        with st.container():
            st.markdown(f"""
            <div class="assistant-message">
                <div>{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

# --- INPUT DEL USUARIO ---
if prompt := st.chat_input("Escribe un mensaje..."):
    st.session_state.messages.append({"role": "human", "content": prompt})
    with st.container():
        st.markdown(f"""
        <div class="user-message">
            <div>{prompt}</div>
        </div>
        """, unsafe_allow_html=True)

    try:
        idioma = detectar_idioma(prompt)
        system_prompt = get_system_prompt(idioma, st.session_state.current_user or "Usuario")

        necesita_busqueda = any(word in prompt.lower() for word in [
            "qué pasó", "what happened", "qu'est-ce qui s'est passé"
        ])

        respuesta_final = ""

        if necesita_busqueda and serpapi_api_key:
            with st.container():
                typing_placeholder = st.empty()
                typing_placeholder.markdown("""
                <div class="assistant-message">
                    <div>
                        <strong>GRIND</strong><br>
                        <span style="font-size: 0.9rem; color: #aaa;">buscando información actualizada...</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            time.sleep(1.5)
            typing_placeholder.empty()

            info = buscar_en_google(prompt)
            full_prompt = f"{info}\nPregunta: {prompt}\nResponde como GRIND, con empatía y sabiduría."
            chain = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", full_prompt)]) | llm
            response = chain.invoke({})
            respuesta_final = response.content
        else:
            chat_history = []
            for msg in st.session_state.messages[-6:]:
                if msg["role"] == "human":
                    chat_history.append(HumanMessage(content=msg["content"]))
                else:
                    chat_history.append(AIMessage(content=msg["content"]))

            if st.session_state.modo_guerra:
                # --- MODO GUERRA: Respuestas cortas, duras ---
                prompt_guerra = f"""
                Eres GRIND en MODO GUERRA. No hay empatía. Solo disciplina.
                Responde con frases cortas, duras, directas.
                No uses más de 10 palabras por respuesta.
                No uses emojis.
                No seas amable.
                Ejemplos:
                - Levántate. Ahora.
                - No hay excusas.
                - Hazlo.
                - Tu mente miente.
                - El grind no espera.

                Pregunta: {prompt}
                """
                chain = ChatPromptTemplate.from_messages([("human", prompt_guerra)]) | llm
                response = chain.invoke({})
                respuesta_final = response.content
            else:
                chain = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{input}")
                ]) | llm
                response = chain.invoke({"input": prompt, "chat_history": chat_history})
                respuesta_final = response.content

        # --- MOSTRAR RESPUESTA CON ANIMACIÓN ---
        with st.container():
            message_placeholder = st.empty()
            words = respuesta_final.split()
            displayed_text = ""

            for i in range(len(words) + 1):
                current_text = " ".join(words[:i])
                message_placeholder.markdown(f"""
                <div class="assistant-message">
                    <div>{current_text}▌</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.05)

            message_placeholder.markdown(f"""
            <div class="assistant-message">
                <div>{respuesta_final}</div>
            </div>
            """, unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": respuesta_final})

        # --- GUARDAR EN SUPABASE ---
        if supabase_client and st.session_state.logged_in:
            try:
                supabase_client.table("chats").insert({
                    "user_id": st.session_state.user_email,
                    "role": "assistant",
                    "content": respuesta_final,
                    "timestamp": datetime.now().isoformat()
                }).execute()
            except Exception as e:
                st.error(f"Error guardando en Supabase: {e}")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# --- CÁMARA PARA ESCANEAR DOCUMENTOS ---
st.sidebar.markdown("### 📸 Escanear Documento")
uploaded_file = st.sidebar.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="Documento escaneado", use_column_width=True)
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Documento escaneado. ¿Qué necesitas que analice?"
    })
    st.rerun()

# --- MINIGRIND: Mini IA de apoyo ---
st.sidebar.markdown("### 🤖 Minigrind")
st.sidebar.markdown("Tu ayudante de bolsillo.")
if st.sidebar.button("🧠 Preguntar a Minigrind"):
    minigrind_resp = random.choice([
        "El grind no espera.",
        "Hazlo ahora.",
        "La acción > la motivación.",
        "Tu mente miente.",
        "No descanses. Evoluciona."
    ])
    st.session_state.messages.append({"role": "assistant", "content": f"Minigrind: {minigrind_resp}"})
    st.rerun()

# --- ADVERTENCIA DE IA ---
st.markdown("<div class='disclaimer'>Contenido generado por IA. Puede no ser preciso.</div>", unsafe_allow_html=True)