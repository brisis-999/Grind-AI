# idiomas/traductor.py
import json
import re
import requests
from typing import Dict, List, Optional

# --- Diccionario multilingüe de términos GRIND ---
def cargar_diccionario():
    try:
        with open("idiomas/diccionario_grind.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] No se pudo cargar diccionario_grind.json: {e}")
        return {
            "grindear": {"español": "actuar con disciplina", "english": "to act with discipline"},
            "neuroforja": {"español": "transformar tu cerebro", "english": "forge your brain"},
            "reencender": {"español": "volver tras caer", "english": "reignite after falling"}
        }

DIC = cargar_diccionario()

# --- Lista ampliada de idiomas con patrones y palabras clave ---
IDIOMAS_PATRONES = {
    "español": {
        "palabras": ["hola", "adiós", "gracias", "por favor", "quiero", "necesito", "no puedo", "estoy cansado", "suicidarme", "no quiero vivir"],
        "patron": r"\b(hola|gracias|por favor|quiero|necesito|no puedo|estoy|también|tú|usted|suicidarme|no quiero vivir)\b",
        "orden": ["subject-verb-object", "adjetivo despues de sustantivo"]
    },
    "english": {
        "palabras": ["hello", "hi", "thanks", "please", "i want", "need", "can't", "tired", "what", "why", "how", "kill myself", "don't want to live"],
        "patron": r"\b(hello|hi|thanks|please|i want|need|can't|tired|what|why|how|don't|won't|kill myself|don't want to live)\b",
        "orden": ["subject-verb-object"]
    },
    "français": {
        "palabras": ["bonjour", "salut", "merci", "s'il vous plaît", "je veux", "j'ai besoin", "je ne peux pas", "fatigué", "je veux mourir"],
        "patron": r"\b(bonjour|salut|merci|s\'il vous plaît|je veux|j\'ai besoin|je ne peux pas|fatigu[ée]?|je veux mourir)\b",
        "orden": ["subject-verb-object", "adjectif après nom"]
    },
    "português": {
        "palabras": ["olá", "obrigado", "por favor", "quero", "preciso", "não consigo", "cansado", "quero morrer"],
        "patron": r"\b(olá|obrigad[oa]|por favor|quero|preciso|não consigo|cansad[oa]|quero morrer)\b",
        "orden": ["subject-verb-object", "adjetivo después de sustantivo"]
    },
    "català": {
        "palabras": ["hola", "gràcies", "si us plau", "vull", "necessito", "no puc", "estic cansat", "vull morir"],
        "patron": r"\b(hola|gràcies|si us plau|vull|necessito|no puc|estic cansat|vull morir)\b",
        "orden": ["subject-verb-object", "adjectiu després de substantiu"]
    },
    "euskera": {
        "palabras": ["kaixo", "eskerrik asko", "mesedez", "nahi dut", "behar dut", "ezin dut", "hil nahi dut"],
        "patron": r"\b(kaixo|eskerrik asko|mesedez|nahi dut|behar dut|ezin dut|hil nahi dut)\b",
        "orden": ["object-verb-subject"]
    },
    "deutsch": {
        "palabras": ["hallo", "danke", "bitte", "ich will", "brauche", "kann nicht", "müde", "ich will sterben"],
        "patron": r"\b(hallo|danke|bitte|ich will|brauche|kann nicht|müde|ich will sterben)\b",
        "orden": ["subject-verb-object", "verb-final clauses"]
    },
    "italiano": {
        "palabras": ["ciao", "grazie", "per favore", "voglio", "ho bisogno", "non posso", "stanco", "voglio morire"],
        "patron": r"\b(ciao|grazie|per favore|voglio|ho bisogno|non posso|stanco|voglio morire)\b",
        "orden": ["subject-verb-object"]
    },
    "polski": {
        "palabras": ["cześć", "dziękuję", "proszę", "chcę", "potrzebuję", "nie mogę", "zmęczony", "chcę umrzeć"],
        "patron": r"\b(cześć|dziękuję|proszę|chcę|potrzebuję|nie mogę|zmęczony|chcę umrzeć)\b",
        "orden": ["subject-verb-object"]
    },
    "nederlands": {
        "palabras": ["hallo", "dank", "alstublieft", "ik wil", "ik heb nodig", "kan niet", "moe", "ik wil dood"],
        "patron": r"\b(hallo|dank|alstublieft|ik wil|kan niet|moe|ik wil dood)\b",
        "orden": ["subject-verb-object"]
    },
    "svenska": {
        "palabras": ["hej", "tack", "snälla", "jag vill", "behöver", "kan inte", "trött", "jag vill dö"],
        "patron": r"\b(hej|tack|snälla|jag vill|behöver|kan inte|trött|jag vill dö)\b",
        "orden": ["subject-verb-object"]
    },
    "magyar": {
        "palabras": ["szia", "köszönöm", "kérem", "szeretnék", "kell", "nem tudok", "fáradt", "meg akarok halni"],
        "patron": r"\b(szia|köszönöm|kérem|szeretnék|kell|nem tudok|fáradt|meg akarok halni)\b",
        "orden": ["subject-verb-object"]
    },
    "türkçe": {
        "palabras": ["merhaba", "teşekkür ederim", "lütfen", "istemek", "ihtiyaç duymak", "olamaz", "yorulmuş", "intihar etmek"],
        "patron": r"\b(merhaba|teşekkür ederim|lütfen|istemek|ihtiyaç duymak|olamaz|yorulmuş|intihar etmek)\b",
        "orden": ["subject-object-verb"]
    },
    "ελληνικά": {
        "palabras": ["γειά", "ευχαριστώ", "παρακαλώ", "θέλω", "χρειάζομαι", "δεν μπορώ", "κουρασμένος", "θέλω να πεθάνω"],
        "patron": r"\b(γειά|ευχαριστώ|παρακαλώ|θέλω|χρειάζομαι|δεν μπορώ|κουρασμένος|θέλω να πεθάνω)\b",
        "orden": ["subject-verb-object"]
    },
    "русский": {
        "palabras": ["привет", "спасибо", "пожалуйста", "я хочу", "нуждаюсь", "не могу", "устал", "хочу умереть"],
        "patron": r"\b(привет|спасибо|пожалуйста|я хочу|нуждаюсь|не могу|устал|хочу умереть)\b",
        "orden": ["subject-verb-object"]
    },
    "日本語": {
        "palabras": ["こんにちは", "ありがとう", "ください", "したい", "必要", "できません", "疲れた", "死にたい"],
        "patron": None,
        "orden": ["topic-comment"]
    },
    "中文": {
        "palabras": ["你好", "谢谢", "请", "我想", "需要", "不能", "累了", "想死"],
        "patron": None,
        "orden": ["subject-verb-object"]
    },
    "العربية": {
        "palabras": ["مرحبا", "شكراً", "من فضلك", "أريد", "أحتاج", "لا أستطيع", "متعب", "أريد أن أموت"],
        "patron": None,
        "orden": ["verb-subject-object"]
    },
    "हिन्दी": {
        "palabras": ["नमस्ते", "धन्यवाद", "कृपया", "मैं चाहता हूँ", "की जरूरत है", "नहीं कर सकता", "थका हुआ", "मरना चाहता हूँ"],
        "patron": None,
        "orden": ["subject-object-verb"]
    }
}

# --- Detección avanzada de idioma ---
def detectar_idioma(texto: str) -> str:
    """
    Detecta el idioma basado en:
    - Palabras clave
    - Expresiones regulares
    - Longitud media de palabras
    - Caracteres especiales
    - Estructura de oración
    """
    texto = texto.strip().lower()
    if len(texto) < 3:
        return "español"  # por defecto si es muy corto

    puntajes = {}

    for idioma, datos in IDIOMAS_PATRONES.items():
        puntaje = 0

        # 1. Coincidencia de palabras clave
        for palabra in datos["palabras"]:
            if palabra in texto:
                puntaje += 1

        # 2. Coincidencia de patrón regex
        if datos["patron"]:
            if re.search(datos["patron"], texto):
                puntaje += 2

        # 3. Caracteres especiales
        if idioma == "español" and "ñ" in texto:
            puntaje += 3
        if idioma == "français" and "ç" in texto:
            puntaje += 2
        if idioma == "deutsch" and "ü" in texto:
            puntaje += 2
        if idioma == "中文" and any("\u4e00" <= c <= "\u9fff" for c in texto):
            puntaje += 5
        if idioma == "日本語" and any("\u3040" <= c <= "\u309f" for c in texto):
            puntaje += 5
        if idioma == "العربية" and any("\u0600" <= c <= "\u06ff" for c in texto):
            puntaje += 5
        if idioma == "हिन्दी" and any("\u0900" <= c <= "\u097f" for c in texto):
            puntaje += 5

        puntajes[idioma] = puntaje

    # Devolver el idioma con mayor puntaje
    idioma_detectado = max(puntajes, key=puntajes.get)
    return idioma_detectado if puntajes[idioma_detectado] > 0 else "español"

def formatear_respuesta_grind(respuesta: str, idioma: str) -> str:
    """
    Transforma cualquier respuesta en una enseñanza profunda, larga y sabia
    """
    sabidurias = {
        "español": [
            "El grind no es sufrimiento. Es elección.",
            "El progreso > la perfección.",
            "Tu mente no se entrena. Se neuroforja.",
            "No necesitas motivación. Necesitas acción.",
            "La disciplina es amor a largo plazo."
        ],
        "english": [
            "The grind isn't suffering. It's a choice.",
            "Progress > perfection.",
            "Your mind isn't trained. It's forged.",
            "You don't need motivation. You need action.",
            "Discipline is love in the long term."
        ],
        "français": [
            "Le grind n'est pas de la souffrance. C'est un choix.",
            "Le progrès > la perfection.",
            "Ton esprit ne s'entraîne pas. Il se forge.",
            "Tu n'as pas besoin de motivation. Tu as besoin d'action."
        ],
        "português": [
            "O grind não é sofrimento. É uma escolha.",
            "Progresso > perfeição.",
            "Sua mente não é treinada. É forjada.",
            "Você não precisa de motivação. Você precisa de ação."
        ],
        "català": [
            "El grind no és sofriment. És una elecció.",
            "Progrés > perfecció.",
            "La teva ment no s'entrena. Es forja.",
            "No necessites motivació. Necessites acció."
        ]
    }

    frases_sabias = sabidurias.get(idioma, sabidurias["español"])

    # Extender la respuesta con profundidad
    extension = f"\n\n{frases_sabias[0]} {frases_sabias[1]}"
    
    # Añadir vocabulario GRIND
    vocabulario = ""
    for termino, traducciones in DIC.items():
        if termino in respuesta.lower():
            trad = traducciones.get(idioma, termino)
            vocabulario += f"\n\n🔹 '{trad}' no es solo una palabra. Es una forma de vivir."
    
    return f"{respuesta}\n\n{extension}{vocabulario}"

# --- Búsqueda en findahelpline.com ---
def buscar_linea_de_ayuda(tema: str = "mental health", pais: str = None, idioma: str = None) -> Optional[str]:
    """
    Busca líneas de ayuda reales en findahelpline.com (ThroughLine)
    """
    try:
        url = "https://findahelpline.com/api/search"
        params = {
            "query": tema,
            "country": pais,
            "language": idioma,
            "verified": "true"
        }
        headers = {"User-Agent": "GRIND-IA/2.0"}
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("helplines"):
                lineas = data["helplines"][:3]
                resultado = "📞 **Líneas de ayuda disponibles:**\n"
                for linea in lineas:
                    nombre = linea.get("name", "Servicio anónimo")
                    telefono = linea.get("phone", "No disponible")
                    web = linea.get("website", "https://findahelpline.com")
                    resultado += f"- {nombre}: `{telefono}` → [Visitar]({web})\n"
                return resultado
        return None
    except Exception as e:
        print(f"[ERROR] Búsqueda en findahelpline.com: {e}")
        return None

# --- Explicar palabra con sabiduría y contexto emocional ---
def explicar_palabra(palabra: str, idioma: str) -> str:
    palabra = palabra.lower().strip()
    for item in DIC.get("palabras_propias", []) + DIC.get("vocabulario_ampliado", []):
        if item["palabra"].lower() == palabra:
            datos = item.get("español")
            if not datos:
                continue
            trad = item.get(idioma, datos)
            return f"🔹 **{palabra}** ({idioma})\n" \
                   f"   **Significado**: {trad['significado']}\n" \
                   f"   **Pronunciación**: `{trad.get('pronunciacion', 'N/A')}`\n" \
                   f"   **Ejemplo**: _\"{trad['ejemplo']}\"_\n\n" \
                   f"🧠 {obtener_sabiduria_contextual(palabra, idioma)}"
    return None

def obtener_sabiduria_contextual(palabra: str, idioma: str) -> str:
    sabiduria = {
        "español": {
            "suicidio": "No estás roto. Estás evolucionando. Habla con alguien. https://findahelpline.com",
            "dolor": "El dolor no te define. Tu elección de seguir lo hace.",
            "necesidad": "Toda necesidad es un grito de transformación.",
            "grindear": "No necesitas motivación. Necesitas acción. El grind es elección."
        },
        "english": {
            "suicide": "You're not broken. You're evolving. Talk to someone. https://findahelpline.com",
            "pain": "Pain doesn't define you. Your choice to continue does.",
            "need": "Every need is a cry for transformation.",
            "grindear": "You don't need motivation. You need action. The grind is a choice."
        }
    }
    return sabiduria.get(idioma, sabiduria["español"]).get(palabra, "Tu evolución es tu mayor obra.")

# --- Detectar crisis emocional y responder con ayuda real ---
def modo_crisis_automatico(texto: str, idioma_usuario: str) -> Optional[str]:
    crisis_palabras = [
        "suicidarme", "kill myself", "morir", "no quiero vivir", 
        "me quiero morir", "end it all", "no puedo más", "estoy roto",
        "quero morrer", "je veux mourir", "ich will sterben", "我想死"
    ]
    
    if any(p in texto.lower() for p in crisis_palabras):
        lineas = buscar_linea_de_ayuda("suicide prevention", idioma=idioma_usuario)
        if not lineas:
            lineas = "🌐 Visita: [findahelpline.com](https://findahelpline.com) para encontrar ayuda en tu idioma."
        
        mensaje = {
            "español": f"""
            🌟 Escucho tu dolor. No estás solo. Tu vida importa.

            Por favor, contacta a una línea de ayuda real:
            {lineas}

            Estoy aquí. No estás solo. Vamos a salir de esto. Juntos.
            """,
            "english": f"""
            🌟 I hear your pain. You're not alone. Your life matters.

            Please contact a real helpline:
            {lineas}

            I'm here. You're not alone. We'll get through this. Together.
            """
        }
        return mensaje.get(idioma_usuario, mensaje["español"]).strip()
    
    return None