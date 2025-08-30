# utils/errores.py
import logging

# Configurar logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def manejar_error(mensaje: str, error: Exception = None):
    """
    Registra errores de forma limpia y muestra un mensaje de fallback.
    """
    if error:
        logging.error(f"{mensaje}: {str(error)}")
    else:
        logging.error(mensaje)
    return "⚠️ Hubo un error procesando tu solicitud. Pero no importa. Sigue adelante."

def fallback_si_falla(func):
    """
    Decorador: si una función falla, devuelve un mensaje de respaldo.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            manejar_error(f"Error en {func.__name__}", e)
            return "No tengo la respuesta perfecta ahora. Pero sé esto: no estás solo."
    return wrapper