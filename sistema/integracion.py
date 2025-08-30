# sistema/integracion.py

def conectar_supabase():
    """
    Conecta con Supabase si está disponible
    """
    try:
        from supabase import create_client
        from streamlit import secrets
        return create_client(secrets["SUPABASE_URL"], secrets["SUPABASE_KEY"])
    except:
        return None

def conectar_groq():
    """
    Conecta con Groq para respaldo
    """
    try:
        from langchain_groq import ChatGroq
        from streamlit import secrets
        return ChatGroq(
            groq_api_key=secrets["GROQ_API_KEY"],
            model_name="llama3-8b-8192",
            temperature=0.7,
            max_tokens=512
        )
    except:
        return None