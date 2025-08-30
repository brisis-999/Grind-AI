# servicios/supabase.py
from supabase import create_client
from utils.errores import manejar_error
from datetime import datetime

def conectar_supabase():
    """
    Conecta con Supabase para guardar chats y hábitos
    """
    try:
        from streamlit import secrets
        return create_client(secrets["SUPABASE_URL"], secrets["SUPABASE_KEY"])
    except Exception as e:
        manejar_error("Supabase (conexión)", e)
        return None

def guardar_chat(user_id, role, content):
    """
    Guarda cada mensaje en Supabase
    """
    client = conectar_supabase()
    if not client:
        return

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
    """
    Carga el historial de chats del usuario
    """
    client = conectar_supabase()
    if not client:
        return []

    try:
        response = client.table("chats") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("timestamp") \
            .execute()
        return response.data if hasattr(response, 'data') else []
    except Exception as e:
        manejar_error("Supabase (cargar)", e)
        return []