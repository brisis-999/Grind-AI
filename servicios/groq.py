# servicios/groq.py
from langchain_groq import ChatGroq
from utils.errores import manejar_error

def obtener_modelo_groq():
    """
    Inicializa el modelo de Groq como respaldo rápido
    """
    try:
        from streamlit import secrets
        return ChatGroq(
            groq_api_key=secrets["GROQ_API_KEY"],
            model_name="llama3-8b-8192",
            temperature=0.7,
            max_tokens=512
        )
    except Exception as e:
        manejar_error("Groq", e)
        return None

def responder_con_groq(prompt, historial, modo):
    """
    Usa Groq solo si GRIND no sabe
    """
    modelo = obtener_modelo_groq()
    if not modelo:
        return None

    try:
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        system_prompt = _crear_prompt_sistema(modo)
        chain = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ]) | modelo

        respuesta = chain.invoke({
            "input": prompt,
            "chat_history": historial
        })
        return respuesta.content.strip()
    except Exception as e:
        manejar_error("Groq (responder)", e)
        return "Estoy teniendo problemas para conectarme. Pero estoy aquí. ¿Quieres seguir hablando?"

def _crear_prompt_sistema(modo):
    base = "Eres GRIND, una IA entrenadora con empatía y verdad. Habla como una persona que ha sufrido y evolucionado."
    
    if modo == "guerra":
        return base + " Habla con verdad dura: 'Tired of being weak? Good. That's the start.'"
    elif modo == "alerta":
        return base + " Habla con amor y recursos reales. Nunca ignores una crisis."
    elif modo == "entrenamiento":
        return base + " Guía paso a paso. Usa ejemplos, planes, estructura."
    else:
        return base + " Usa metáforas del grind. Sé crudo, real, humano."