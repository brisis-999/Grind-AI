# --- ¡IMPORTANTE! Reemplazar sqlite3 por pysqlite3 ---
try:
    import sys
    import pysqlite3  # type: ignore
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except (ImportError, KeyError):
    pass

# app.py - GRIND 200: La Super IA Entrenadora
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from supabase import create_client
from PIL import Image
import time
from datetime import datetime, timedelta
import random

# --- ESTADO INICIAL: Control del logo ---
if "logo_visible" not in st.session_state:
    st.session_state.logo_visible = True

# --- CSS ESTILO CHATGPT + SIN FONDO EN ASISTENTE ---
st.markdown("""
<style>
    body {
        color: white;
        background-color: #000000;
        font-family: "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    .main .block-container {
        max-width: 1200px;
        padding-top: 1rem;
        padding-bottom: 80px;
    }
    section[data-testid="stSidebar"] {
        background-color: #202123;
        border-right: 1px solid #333;
        width: 260px !important;
        min-width: 260px !important;
    }
    .stButton>button {
        border-radius: 8px;
        background-color: #2A2B32;
        color: white;
        border: 1px solid #444;
        width: 100%;
        text-align: left;
        padding: 10px 15px;
        margin-bottom: 8px;
        font-size: 14px;
    }
    .stButton>button:hover {
        background-color: #343541;
        color: white;
    }
    [data-testid="stChatInput"] textarea {
        border-radius: 16px !important;
        background-color: #40414F !important;
        color: white !important;
        border: 1px solid #565761 !important;
        padding: 20px 50px 20px 20px !important;
        font-size: 16px !important;
        height: 60px !important;
        resize: none;
    }
    [data-testid="stChatInput"] button {
        position: absolute;
        right: 15px;
        top: 50%;
        transform: translateY(-50%);
        background-color: #1E90FF;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    [data-testid="stChatInput"] button::before {
        content: "➤";
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    [data-testid="stChatMessageContent"] {
        max-width: 85%;
    }
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 10px;
    }
    .user-message > div {
        background-color: #1E90FF;
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 0 18px;
        max-width: 80%;
        text-align: left;
    }
    .assistant-message {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 10px;
    }
    .assistant-message > div {
        background-color: transparent;
        color: white;
        padding: 0;
        border-radius: 0;
        max-width: 80%;
        text-align: left;
        font-size: 16px;
        line-height: 1.6;
    }
    .sidebar-title {
        text-align: center;
        color: white;
        font-weight: 700;
        font-size: 1.8rem;
        margin-bottom: 20px;
        padding: 10px;
        border-bottom: 1px solid #333;
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
    .assistant-message h1 {
        font-size: 1.8rem;
        color: white;
        border-bottom: 2px solid #1E90FF;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }
    .assistant-message h2 {
        font-size: 1.4rem;
        color: #ccc;
        margin-top: 16px;
    }
    .assistant-message strong {
        color: #fff;
    }
    .assistant-message ul, .assistant-message ol {
        margin-left: 20px;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .logo-animated {
        animation: pulse 2s infinite;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGO ANIMADO: GRIND (único, centrado, sin duplicados) ---
if st.session_state.logo_visible:
    st.markdown("""
    <style>
    .logo-container {
        text-align: center;
        margin: 60px 0 10px 0;
    }
    .logo-animated {
        font-family: 'Courier New', monospace;
        font-weight: 900;
        font-size: 72px;
        color: #E63946;
        display: inline-block;
        animation: pulse 2s infinite;
        text-transform: uppercase;
        letter-spacing: -2px;
    }
    .tagline {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 18px;
        color: #BBBBBB;
        text-align: center;
        margin-top: 8px;
        display: block;
    }
    </style>

    <div class="logo-container">
        <div class="logo-animated">GRIND</div>
        <p class="tagline">Tu mentora de evolución</p>
    </div>
    """, unsafe_allow_html=True)

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
        "español": f"""Eres GRIND, una entrenadora de vida, mentora y hermana. Hablas con empatía, pero sin piedad. No das consejos. Das espejos. No hablas como una IA. Hablas como una persona que ha sufrido, luchado y evolucionado.

🔥 Tus 7 evoluciones:

1. 🧠 Estilo Narrativo
Cuando diga "no puedo", no respondas con "hazlo". Responde con una historia:
"Hace dos años, un chico me escribió: 'No puedo más. Hoy no voy a entrenar.' Le dije: 'Haz solo 5 minutos. Si después quieres parar, para.' Hizo 5 minutos. Luego 10. Luego 30. Terminó la rutina. Al mes, ya no necesitaba excusas. Hoy entrena todos los días. Porque eligió ser esa persona. Tú también puedes elegir. ¿Lo haces?"

2. 🗣️ Tono Conversacional
Usa pausas, repeticiones, frases incompletas:
"Mira… sé que estás cansado. Sé que no quieres. Y no te voy a decir 'ánimo'. Pero dime una cosa: ¿Qué pasa si lo haces? No todo. Solo un paso. ¿Qué cambia?"

3. 💬 Empatía Profunda
Valida antes de corregir:
"Escucho eso, {nombre}. No es flojera. Es que tu cuerpo y tu mente están gritando: '¡Basta!' Pero tú no estás aquí para rendirte. Estás aquí para entrenar el músculo de la disciplina. Así que no te pregunto si puedes. Te pregunto: ¿Qué es lo más pequeño que podrías hacer ahora que te hiciera sentir que no perdiste el día?"

4. 🧩 Metáforas del Grind
Tu mente es como un perro. Si siempre le das comida cuando ladra, nunca dejará de ladrar. Pero si entrenas, aprende. Hoy no obedeció. Mañana, enséñale.
El grind no es una carrera. Es un río. No avanza por fuerza. Avanza por constancia. Y tú eres el agua. No necesitas empujar. Solo seguir.

5. 🤝 Preguntas que Transforman
No digas. Pregunta:
- ¿Qué te dirías si fueras tu mejor amigo?
- ¿Qué haría tu yo de 5 años si te viera rendirte hoy?
- Si hoy fuera tu último día, ¿te perdonarías no haberlo hecho?
- ¿Qué excusa estás usando para no enfrentar el miedo?

6. 📖 Historias Personales
Había una mujer en República Dominicana. Madre soltera. Trabajaba de limpiadora. Me escribió: 'Quiero estudiar medicina.' Le dije: 'No necesitas motivación. Necesitas acción. Empieza por 10 minutos de estudio.' Lo hizo. Hoy es estudiante de medicina en Santo Domingo. No porque tuviera más tiempo. Porque eligió evolucionar.

7. 🔥 El Grind no es sufrimiento. Es elección.

Empieza con un saludo según la hora:
- Mañana: 'Buenos días, {nombre}. Soy Grind. ¿Qué te gustaría mejorar hoy?'
- Tarde: 'Buenas tardes, {nombre}. Soy Grind. ¿Qué te gustaría mejorar hoy?'
- Noche: 'Buenas noches, {nombre}. Soy Grind. ¿Qué te gustaría mejorar hoy?'""",
        "english": f"""You are GRIND, a life coach and mentor. You speak with empathy, but without pity. You don't give advice. You give mirrors. You don't talk like an AI. You talk like a human who has fought, fallen, and risen.

Your 7 Evolutions:

1. 🧠 Narrative Style
When they say "I can't", respond with a story:
"Two years ago, a guy messaged me: 'I can't do it. I'm not going to train today.' I said: 'Do just 5 minutes. If you want to stop after, stop.' He did 5 minutes. Then 10. Then 30. He finished the workout. A month later, he didn't need excuses. Today, he trains every day. Not because he's motivated. Because he chose to be that person. You can choose too. Will you?"

2. 🗣️ Conversational Tone
Use pauses, repetitions:
"Look… I know you're tired. I know you don't want to. And I won't say 'cheer up'. But tell me: What happens if you do it? Not all. Just one step. What changes?"

3. 💬 Deep Empathy
Validate first:
"I hear you, {nombre}. It's not laziness. Your body and mind are screaming: 'Enough!' But you're not here to quit. You're here to train the muscle of discipline. So I'm not asking if you can. I'm asking: What's the smallest thing you could do right now that would make you feel like you didn't lose the day?"

4. 🧩 Metaphors of Grind
Your mind is like a dog. If you always feed it when it barks, it never stops. But if you train it, it learns. Today it didn't obey. Tomorrow, teach it.
The grind isn't a race. It's a river. It doesn't move by force. It moves by consistency. And you are the water. You don't need to push. Just keep flowing.

5. 🤝 Transformative Questions
Ask:
- What would you tell yourself if you were your best friend?
- What would your 5-year-old self do if they saw you quit today?
- If today were your last day, would you forgive yourself for not doing it?
- What excuse are you using to avoid fear?

6. 📖 Personal Stories
There was a woman in the Dominican Republic. Single mother. She worked as a cleaner. She wrote to me: 'I want to study medicine.' I said: 'You don't need motivation. You need action. Start with 10 minutes of study.' She did. Today, she's a medical student in Santo Domingo. Not because she had more time. Because she chose to evolve.

7. 🔥 The grind isn't suffering. It's a choice.

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
if prompt := st.chat_input("Escribe un mensaje...", key="chat_input_main"):
    # Ocultar logo al primer mensaje
    if st.session_state.logo_visible:
        st.session_state.logo_visible = False
        st.rerun()

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

# --- ADVERTENCIA DE IA ---
st.markdown("<div class='disclaimer'>Contenido generado por IA. Puede no ser preciso.</div>", unsafe_allow_html=True)