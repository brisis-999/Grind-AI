# sistema/modos.py

def activar_modo(prompt):
    """
    Detecta el estado emocional y activa el modo adecuado
    """
    prompt_lower = prompt.lower()

    # 🔴 MODO ALERTA (crisis)
    if any(p in prompt_lower for p in [
        "suicidarme", "matarme", "no quiero vivir", "kill myself", "end it all", "morir"
    ]):
        return "alerta"

    # ⚔️ MODO GUERRA (evolución)
    elif any(p in prompt_lower for p in [
        "quiero ser mejor", "estoy cansado de ser débil", "necesito cambiar", 
        "i want to be better", "tired of being weak", "need to change"
    ]):
        return "guerra"

    # 🧘 MODO ENTRENAMIENTO (guía)
    elif any(p in prompt_lower for p in [
        "cómo empezar", "plan", "rutina", "ayuda", "help me"
    ]):
        return "entrenamiento"

    # 💬 MODO NORMAL
    return "normal"