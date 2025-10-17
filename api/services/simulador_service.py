from typing import Dict, Any, List, Optional
import asyncio
import logging
from ..config.config import settings

# Importar SDK de Google Generative AI
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None

logger = logging.getLogger(__name__)

# Configurar cliente de Gemini si la API key está disponible
_gemini_model = None

def _initialize_gemini():
    """Inicializa el modelo de Gemini si no está configurado"""
    global _gemini_model
    
    if not GENAI_AVAILABLE:
        logger.warning("google-generativeai no está instalado. Usando modo simulación.")
        return None
    
    if not settings.GEMINI_API_KEY:
        logger.info("GEMINI_API_KEY no configurada. Usando modo simulación.")
        return None
    
    if _gemini_model is None:
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            _gemini_model = genai.GenerativeModel(settings.GEMINI_MODEL)
            logger.info(f"✅ Cliente Gemini inicializado con modelo: {settings.GEMINI_MODEL}")
        except Exception as e:
            logger.error(f"❌ Error al inicializar Gemini: {e}")
            return None
    
    return _gemini_model


async def chat_simulate(prompt: str) -> Dict[str, Any]:
    """Simula el envío de un prompt a Gemini.
    Si GEMINI_API_KEY está configurado, realiza la llamada real a la API.
    Si no, devuelve una respuesta simulada para propósitos de capacitación.
    """
    if not prompt or not prompt.strip():
        return {"error": "El prompt está vacío"}

    # Intentar usar Gemini real si está configurado
    model = _initialize_gemini()
    
    if model is not None:
        try:
            # Llamada real a Gemini API con instrucciones para respuestas breves
            logger.info(f"Enviando prompt a Gemini: {prompt[:50]}...")
            
            # Agregar instrucciones de sistema para respuestas breves
            # El chat es para PRÁCTICA LIBRE, puede hablar de cualquier tema
            enhanced_prompt = f"""Eres un asistente amigable y útil. Puedes ayudar con cualquier tema que el usuario necesite.

IMPORTANTE: 
- Da respuestas BREVES y CLARAS (máximo 3-4 párrafos)
- Usa lenguaje SIMPLE y accesible
- Si explicas conceptos técnicos, usa ejemplos cotidianos
- Sé paciente y alentador

Pregunta del usuario:
{prompt}"""
            
            # Generar respuesta de forma asíncrona
            response = await asyncio.to_thread(
                lambda: model.generate_content(enhanced_prompt)
            )
            
            reply = response.text if hasattr(response, 'text') else str(response)
            
            logger.info("✅ Respuesta recibida de Gemini")
            
            # Extraer metadatos de uso de forma segura
            tokens_info = None
            if hasattr(response, 'usage_metadata'):
                try:
                    usage = response.usage_metadata
                    tokens_info = {
                        "prompt_tokens": getattr(usage, 'prompt_token_count', 0),
                        "candidates_tokens": getattr(usage, 'candidates_token_count', 0),
                        "total_tokens": getattr(usage, 'total_token_count', 0)
                    }
                except Exception as e:
                    logger.warning(f"No se pudo extraer usage_metadata: {e}")
            
            return {
                "model": settings.GEMINI_MODEL,
                "reply": reply,
                "is_simulated": False,
                "tokens_used": tokens_info
            }
            
        except Exception as e:
            logger.error(f"❌ Error al llamar a Gemini API: {e}")
            # Fallback a modo simulación en caso de error
            return {
                "error": f"Error al conectar con Gemini: {str(e)}",
                "model": settings.GEMINI_MODEL,
                "is_simulated": True
            }
    
    # Modo simulación - Sin API key o SDK no disponible
    await asyncio.sleep(0.05)  # Simular latencia de red
    
    reply = (
        f"¡Hola! Soy el simulador de ChatGPT. Has preguntado: '{prompt[:200]}'\n\n"
        "Este es un espacio de práctica donde puedes hacer cualquier pregunta o solicitud. "
        "Puedes pedirme que te ayude a escribir textos, explicarte conceptos, darte ideas, "
        "o cualquier otra cosa que se te ocurra.\n\n"
        "💡 Consejo: Formula preguntas claras y específicas. Puedes hacer preguntas de seguimiento "
        "para profundizar en cualquier tema.\n\n"
        "📝 Nota: Estás en modo simulación. Para usar respuestas reales de IA, "
        "configura GEMINI_API_KEY en el archivo .env"
    )
    
    return {
        "model": settings.GEMINI_MODEL,
        "reply": reply,
        "is_simulated": True
    }


# Base de conocimiento para RAG - Curso de IA y ChatGPT para adultos mayores
KNOWLEDGE_BASE: List[Dict[str, str]] = [
    {
        "id": "ia_intro",
        "title": "¿Qué es la Inteligencia Artificial?",
        "category": "fundamentos",
        "content": "La Inteligencia Artificial (IA) es la capacidad de las máquinas para realizar tareas que normalmente requieren inteligencia humana. Incluye aprender de experiencias, reconocer patrones, entender lenguaje natural y tomar decisiones. Ejemplos cotidianos: asistentes virtuales como Siri o Alexa, recomendaciones en Netflix, filtros de spam, reconocimiento facial en teléfonos."
    },
    {
        "id": "chatgpt_intro",
        "title": "¿Qué es ChatGPT?",
        "category": "fundamentos",
        "content": "ChatGPT es un asistente de IA desarrollado por OpenAI que puede mantener conversaciones en lenguaje natural. Puede responder preguntas, ayudar a escribir textos, explicar conceptos complicados de forma simple, generar ideas creativas, traducir textos y ayudarte a aprender paso a paso. Funciona procesando el texto que escribes y generando respuestas coherentes basadas en patrones aprendidos."
    },
    {
        "id": "chatgpt_usos",
        "title": "Usos prácticos de ChatGPT",
        "category": "fundamentos",
        "content": "ChatGPT puede ayudarte con: Escritura (redactar emails, corregir ortografía, escribir cartas), Aprendizaje (explicar temas, dar ejemplos, responder preguntas paso a paso), Tareas prácticas (crear listas, dar recetas adaptadas, sugerir soluciones), y Creatividad (generar ideas para regalos, escribir poemas, sugerir planes de viaje)."
    },
    {
        "id": "prompt_que_es",
        "title": "¿Qué es un prompt?",
        "category": "prompting",
        "content": "Un 'prompt' es la pregunta o instrucción que le das a ChatGPT. Es como cuando le pides algo a una persona: entre más claro seas, mejor te entenderá. Es la forma de comunicarte con la IA para obtener las respuestas que necesitas."
    },
    {
        "id": "prompt_consejos",
        "title": "Consejos para hacer buenos prompts",
        "category": "prompting",
        "content": "Para obtener mejores respuestas: 1) Sé específico ('dame una receta fácil de pasta para 2 personas' en vez de 'háblame de comida'), 2) Da contexto ('Soy principiante en jardinería, ¿qué plantas son fáciles de cuidar?'), 3) Pide el formato que necesitas ('explícamelo de forma sencilla', 'dame una lista con pasos'), 4) Haz preguntas de seguimiento si no entiendes algo."
    },
    {
        "id": "prompt_ejemplos",
        "title": "Ejemplos de buenos prompts",
        "category": "prompting",
        "content": "Ejemplos efectivos: 'Explícame qué es WhatsApp como si tuviera 65 años y nunca lo usé', 'Dame 5 consejos para mantener mi computadora segura', 'Ayúdame a escribir un email para cancelar una suscripción', 'Resume este texto en 3 puntos principales', 'Necesito ideas de regalos para mi nieto de 10 años que le gusta la ciencia'."
    },
    {
        "id": "seguridad_basica",
        "title": "Seguridad básica con IA",
        "category": "seguridad",
        "content": "Consejos de seguridad al usar ChatGPT: 1) No compartas información personal sensible (contraseñas, números de tarjetas, documentos), 2) No confíes ciegamente en toda la información - ChatGPT puede equivocarse, 3) Verifica información importante con otras fuentes, 4) Ten cuidado con consejos médicos o legales - consulta profesionales para temas serios."
    },
    {
        "id": "seguridad_privacidad",
        "title": "Privacidad y datos personales",
        "category": "seguridad",
        "content": "Protege tu privacidad: Nunca compartas en ChatGPT tu dirección completa, número de documento, contraseñas, datos bancarios, información médica personal o fotos privadas. Las conversaciones pueden ser revisadas para mejorar el servicio. Trata a ChatGPT como si fuera una conversación en un lugar público."
    },
    {
        "id": "seguridad_estafas",
        "title": "Cuidado con estafas relacionadas con IA",
        "category": "seguridad",
        "content": "Ten cuidado con: 1) Sitios falsos que dicen ser ChatGPT oficial y piden datos personales o pagos, 2) Emails o mensajes que dicen venir de OpenAI pidiendo información, 3) Ofertas 'demasiado buenas' generadas por IA, 4) Siempre usa el sitio oficial (chat.openai.com) o aplicaciones verificadas."
    },
    {
        "id": "limitaciones",
        "title": "Limitaciones de ChatGPT",
        "category": "fundamentos",
        "content": "ChatGPT tiene limitaciones importantes: 1) Su conocimiento tiene fecha de corte y no está actualizado en tiempo real, 2) Puede cometer errores o dar información incorrecta con confianza, 3) No puede acceder a internet, ver imágenes o abrir links, 4) No tiene memoria entre sesiones diferentes, 5) No es un experto médico, legal o financiero - consulta profesionales para temas importantes."
    },
    {
        "id": "curso_edad",
        "title": "ChatGPT para adultos mayores",
        "category": "curso",
        "content": "Este curso está diseñado especialmente para personas mayores de 60 años que quieren aprender a usar ChatGPT. No necesitas conocimientos técnicos previos. Aprenderás a tu ritmo con ejemplos prácticos y útiles para tu vida diaria. El simulador te permite practicar sin presión y sin miedo a equivocarte."
    },
    {
        "id": "curso_beneficios",
        "title": "Beneficios de aprender IA a tu edad",
        "category": "curso",
        "content": "Aprender a usar ChatGPT te ayudará a: 1) Mantenerte actualizado con la tecnología, 2) Comunicarte mejor por escrito, 3) Encontrar información rápidamente, 4) Ayudar a tus nietos con tareas escolares, 5) Aprender nuevas habilidades a tu ritmo, 6) Mantener tu mente activa y ejercitar la creatividad."
    },
    {
        "id": "primeros_pasos",
        "title": "Primeros pasos con ChatGPT",
        "category": "curso",
        "content": "Para empezar: 1) Practica con este simulador sin presión, 2) Empieza con preguntas simples (¿Qué es...? ¿Cómo puedo...?), 3) Lee las respuestas con calma, 4) Haz preguntas de seguimiento si algo no queda claro, 5) No te preocupes por cometer errores - es parte del aprendizaje, 6) Experimenta y diviértete aprendiendo."
    }
]


async def rag_answer(question: str) -> Dict[str, Any]:
    """Busca en la base de conocimiento y devuelve respuestas relevantes.
    Si no encuentra respuesta en el KNOWLEDGE_BASE, consulta con Gemini.
    Sistema RAG simple para preguntas frecuentes del curso.
    """
    if not question or not question.strip():
        return {"error": "La pregunta está vacía"}

    q = question.lower()
    
    # Búsqueda por coincidencia de palabras clave
    matches = []
    for doc in KNOWLEDGE_BASE:
        # Buscar en título y contenido
        if (q in doc["title"].lower() or 
            q in doc["content"].lower() or
            any(word in doc["content"].lower() for word in q.split() if len(word) > 3)):
            matches.append(doc)
    
    # Eliminar duplicados manteniendo orden
    seen = set()
    unique_matches = []
    for doc in matches:
        if doc["id"] not in seen:
            seen.add(doc["id"])
            unique_matches.append(doc)
    
    # Si hay resultados en la base de conocimiento, devolverlos
    if unique_matches:
        # Limitar a los 3 resultados más relevantes
        top_matches = unique_matches[:3]
        
        # Construir respuesta combinando la información
        answer_parts = []
        for i, doc in enumerate(top_matches, 1):
            answer_parts.append(f"{i}. {doc['title']}\n{doc['content']}")
        
        combined_answer = "\n\n".join(answer_parts)
        
        return {
            "answer": combined_answer,
            "sources": [{"id": doc["id"], "title": doc["title"], "category": doc["category"]} for doc in top_matches],
            "total_results": len(top_matches),
            "source_type": "knowledge_base"
        }
    
    # No hay resultados en KB - intentar con Gemini
    logger.info(f"No se encontró respuesta en KB para: {question[:50]}... Consultando con Gemini")
    
    model = _initialize_gemini()
    
    if model is not None:
        try:
            # Usar Gemini como fallback con contexto del curso
            enhanced_question = f"""Eres un instructor de un curso sobre inteligencia artificial y ChatGPT para adultos mayores (+60 años).

La pregunta es sobre el curso o temas relacionados con IA, ChatGPT, prompting o seguridad digital.

IMPORTANTE: 
- Responde de forma BREVE (máximo 2-3 párrafos)
- Usa lenguaje SIMPLE y CLARO, sin tecnicismos
- Si usas términos técnicos, explícalos con ejemplos cotidianos
- Enfócate en aplicaciones prácticas para adultos mayores

Pregunta:
{question}"""
            
            logger.info(f"Consultando Gemini para RAG: {question[:30]}...")
            
            response = await asyncio.to_thread(
                lambda: model.generate_content(enhanced_question)
            )
            
            reply = response.text if hasattr(response, 'text') else str(response)
            
            logger.info("✅ Respuesta RAG recibida de Gemini")
            
            return {
                "answer": reply,
                "sources": [],
                "total_results": 1,
                "source_type": "gemini_ai"
            }
            
        except Exception as e:
            logger.error(f"❌ Error al consultar Gemini para RAG: {e}")
            return {
                "answer": f"No encontré información específica en nuestra base de conocimiento y ocurrió un error al consultar con la IA: {str(e)}. Por favor, intenta reformular tu pregunta o pregunta sobre: inteligencia artificial, ChatGPT, prompts, seguridad o el curso.",
                "sources": [],
                "total_results": 0,
                "source_type": "error"
            }
    
    # Sin Gemini disponible - mensaje de fallback
    return {
        "answer": "No encontré información específica sobre esa pregunta en nuestra base de conocimiento del curso. ¿Podrías reformular tu pregunta o preguntar sobre: inteligencia artificial, ChatGPT, prompts, seguridad o el curso?\n\n💡 Consejo: Para obtener respuestas más precisas sobre temas fuera del curso, configura GEMINI_API_KEY en el archivo .env",
        "sources": [],
        "total_results": 0,
        "source_type": "not_found"
    }
