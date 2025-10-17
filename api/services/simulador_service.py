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
        "title": "🤖 ¿Qué es la Inteligencia Artificial?",
        "category": "fundamentos",
        "content": """La Inteligencia Artificial (IA) es la capacidad de las máquinas para realizar tareas que normalmente requieren inteligencia humana, como aprender, reconocer patrones, entender el lenguaje y tomar decisiones.

🔍 Ejemplos que usas en tu día a día:
• Asistentes virtuales como Siri o Alexa que responden a tu voz
• Recomendaciones de películas en Netflix según tus gustos
• Filtros de spam que protegen tu correo electrónico
• Reconocimiento facial para desbloquear tu teléfono

La IA está presente en muchas cosas cotidianas, haciéndonos la vida más fácil y segura."""
    },
    {
        "id": "chatgpt_intro",
        "title": "💬 ¿Qué es ChatGPT?",
        "category": "fundamentos",
        "content": """ChatGPT es un asistente de inteligencia artificial desarrollado por la empresa OpenAI. Es como tener un ayudante muy conocedor con quien puedes conversar escribiendo.

✨ ¿Qué puede hacer por ti?
• Responder preguntas sobre casi cualquier tema
• Ayudarte a escribir textos, emails o cartas
• Explicar conceptos complicados de forma simple
• Generar ideas creativas para proyectos o regalos
• Traducir textos a otros idiomas
• Enseñarte paso a paso cómo hacer cosas

ChatGPT funciona leyendo lo que escribes y generando respuestas coherentes basándose en toda la información con la que fue entrenado."""
    },
    {
        "id": "chatgpt_usos",
        "title": "🛠️ Usos prácticos de ChatGPT en tu vida",
        "category": "fundamentos",
        "content": """ChatGPT puede ser tu asistente personal para muchas tareas diarias:

📝 Escritura y comunicación:
• Redactar emails profesionales o personales
• Corregir ortografía y gramática
• Escribir cartas formales o invitaciones

📚 Aprendizaje y conocimiento:
• Explicar temas que no entiendes
• Dar ejemplos prácticos
• Responder dudas paso a paso

🏠 Tareas del hogar y prácticas:
• Crear listas de compras organizadas
• Adaptar recetas según tus necesidades
• Sugerir soluciones a problemas cotidianos

🎨 Creatividad y ocio:
• Generar ideas para regalos personalizados
• Escribir poemas o mensajes especiales
• Planificar viajes o actividades"""
    },
    {
        "id": "prompt_que_es",
        "title": "❓ ¿Qué es un prompt?",
        "category": "prompting",
        "content": """Un "prompt" es simplemente la pregunta o instrucción que le das a ChatGPT. Es tu forma de comunicarte con la inteligencia artificial.

💡 Piénsalo así:
Es como cuando le pides algo a una persona: entre más claro y específico seas, mejor te entenderá y mejor será la respuesta que obtengas.

Ejemplo:
❌ Prompt vago: "Comida"
✅ Prompt claro: "Dame una receta fácil de pasta para 2 personas"

La diferencia está en ser específico y claro con lo que necesitas."""
    },
    {
        "id": "prompt_consejos",
        "title": "✍️ Consejos para hacer buenos prompts",
        "category": "prompting",
        "content": """Sigue estos consejos para obtener mejores respuestas de ChatGPT:

1️⃣ Sé específico y detallado
   ❌ "Háblame de comida"
   ✅ "Dame una receta fácil de pasta para 2 personas con ingredientes simples"

2️⃣ Da contexto sobre tu situación
   ✅ "Soy principiante en jardinería y vivo en departamento. ¿Qué plantas son fáciles de cuidar en macetas?"

3️⃣ Pide el formato que necesitas
   ✅ "Explícamelo de forma sencilla y paso a paso"
   ✅ "Dame una lista numerada con los pasos"

4️⃣ Haz preguntas de seguimiento
   Si algo no queda claro, simplemente pregunta: "¿Podrías explicar mejor esa parte?" o "Dame un ejemplo de eso"

Recuerda: No existe una pregunta tonta. ChatGPT está para ayudarte."""
    },
    {
        "id": "prompt_ejemplos",
        "title": "📋 Ejemplos de buenos prompts",
        "category": "prompting",
        "content": """Aquí tienes ejemplos reales de prompts efectivos que puedes usar:

🎓 Para aprender:
• "Explícame qué es WhatsApp como si tuviera 65 años y nunca lo usé"
• "¿Cómo funciona el home banking? Dame los pasos básicos"

🔒 Para seguridad:
• "Dame 5 consejos para mantener mi computadora segura"
• "¿Cómo identifico un email falso o estafa?"

✉️ Para escribir:
• "Ayúdame a escribir un email para cancelar una suscripción"
• "Redacta una carta para agradecer un favor"

📰 Para resumir:
• "Resume este texto en 3 puntos principales: [tu texto]"

🎁 Para ideas:
• "Necesito ideas de regalos para mi nieto de 10 años que le gusta la ciencia"
• "Sugiéreme actividades para hacer con mis nietos en casa"

¡Copia estos ejemplos y adáptalos a tus necesidades!"""
    },
    {
        "id": "seguridad_basica",
        "title": "🔐 Seguridad básica al usar ChatGPT",
        "category": "seguridad",
        "content": """Es importante usar ChatGPT de forma segura. Sigue estas reglas de oro:

🚫 NUNCA compartas:
• Contraseñas o PINs
• Números de tarjetas de crédito o débito
• Números de documento (DNI, pasaporte)
• Datos bancarios o financieros

⚠️ Ten en cuenta:
• ChatGPT puede equivocarse - no confíes ciegamente en toda la información
• Verifica información importante con otras fuentes
• Para temas médicos, legales o financieros serios, siempre consulta con profesionales

✅ Úsalo con seguridad para:
• Aprender cosas nuevas
• Escribir textos
• Obtener ideas
• Practicar habilidades

Recuerda: La seguridad es tu responsabilidad. Si tienes dudas, mejor no compartas la información."""
    },
    {
        "id": "seguridad_privacidad",
        "title": "🛡️ Protege tu privacidad",
        "category": "seguridad",
        "content": """Tu privacidad es importante. Aprende a protegerla cuando uses ChatGPT:

🔒 NUNCA escribas en ChatGPT:
• Tu dirección completa
• Tu número de documento (DNI)
• Contraseñas de ningún tipo
• Datos de tarjetas bancarias
• Información médica personal detallada
• Fotos privadas tuyas o de tu familia

⚠️ Importante saber:
Las conversaciones que tienes con ChatGPT pueden ser revisadas por la empresa para mejorar el servicio.

💡 Regla de oro:
Trata a ChatGPT como si fuera una conversación en un café público. No digas nada que no dirías en voz alta en un lugar con gente alrededor.

✅ Sí puedes compartir:
• Preguntas generales
• Textos para editar (sin datos personales)
• Dudas sobre temas en general
• Situaciones hipotéticas"""
    },
    {
        "id": "seguridad_estafas",
        "title": "⚠️ Cuidado con estafas relacionadas con IA",
        "category": "seguridad",
        "content": """Los estafadores también usan la IA. Protégete conociendo estos peligros:

🚨 Ten cuidado con:

1️⃣ Sitios web falsos
Sitios que imitan a ChatGPT y te piden datos personales o pagos extraños.

2️⃣ Emails o mensajes sospechosos
Si recibes un email que dice venir de "OpenAI" o "ChatGPT" pidiendo información personal, es probablemente falso.

3️⃣ Ofertas "demasiado buenas"
"Gana dinero fácil con IA", "Invierte en ChatGPT", etc. Son estafas.

4️⃣ Personas que se hacen pasar por soporte técnico
Nadie real te va a pedir contraseñas por teléfono o mensaje.

✅ Mantente seguro:
• Usa SOLO el sitio oficial: chat.openai.com
• Descarga apps SOLO de tiendas oficiales (Google Play, App Store)
• Ante la duda, consulta con un familiar de confianza
• Si algo parece muy bueno para ser verdad, probablemente es una estafa"""
    },
    {
        "id": "limitaciones",
        "title": "⚖️ Limitaciones que debes conocer",
        "category": "fundamentos",
        "content": """ChatGPT es una herramienta poderosa, pero no es perfecta. Conoce sus limitaciones:

📅 Su conocimiento tiene fecha de corte
No sabe de eventos muy recientes ni tiene acceso a información actualizada en tiempo real.

❌ Puede cometer errores
A veces da información incorrecta con mucha confianza. Siempre verifica datos importantes.

🌐 No puede navegar por internet
No puede abrir links, ver páginas web actuales ni buscar información en tiempo real.

🧠 No tiene memoria entre sesiones
Cada conversación nueva es como empezar de cero. No recuerda conversaciones anteriores.

⚕️ No reemplaza a profesionales
NO es un médico, abogado o asesor financiero. Para temas importantes de salud, legales o de dinero, consulta con expertos reales.

🤖 Es una máquina, no una persona
No tiene sentimientos, opiniones personales ni experiencias reales. Genera respuestas basándose en patrones de texto.

💡 Úsalo como lo que es: una herramienta de ayuda, no una fuente de verdad absoluta."""
    },
    {
        "id": "curso_edad",
        "title": "👴👵 Este curso es para ti",
        "category": "curso",
        "content": """¡Bienvenido! Este curso está diseñado especialmente para personas mayores de 60 años que quieren aprender sobre inteligencia artificial y ChatGPT.

✨ Lo que nos hace especiales:

🎯 Sin conocimientos previos necesarios
No importa si no sabes de tecnología. Empezamos desde cero.

⏰ Aprendes a tu propio ritmo
Sin presiones, sin apuros. Tómate el tiempo que necesites.

💼 Ejemplos prácticos y útiles
Todo lo que aprendas podrás aplicarlo en tu vida diaria.

🎮 Práctica sin miedo
Este simulador te permite practicar libremente. No hay forma de "romper" nada o equivocarte de forma permanente.

🤝 Lenguaje claro y cercano
Sin tecnicismos complicados. Si usamos algún término técnico, te lo explicamos con ejemplos simples.

Recuerda: Nunca es tarde para aprender algo nuevo. ¡Estás en el lugar correcto!"""
    },
    {
        "id": "curso_beneficios",
        "title": "🌟 Beneficios de aprender IA en esta etapa",
        "category": "curso",
        "content": """Aprender a usar ChatGPT te traerá muchos beneficios en tu vida diaria:

💻 Te mantiene actualizado con la tecnología
La tecnología avanza rápido. Con este curso te mantienes al día.

✍️ Mejora tu comunicación escrita
Aprende a redactar mejor emails, cartas y mensajes.

🔍 Encuentra información rápidamente
Ya no necesitas buscar en muchos sitios. Pregunta y obtén respuestas al instante.

👨‍👩‍👧‍👦 Conecta con tus nietos
Ayúdalos con tareas escolares o entiende mejor de qué hablan cuando mencionan "la IA".

📚 Aprende nuevas habilidades
Desde cocina hasta jardinería, ChatGPT puede enseñarte paso a paso.

🧠 Mantén tu mente activa
Aprender cosas nuevas ejercita tu cerebro y mantiene tu mente ágil.

🎨 Despierta tu creatividad
Escribe poemas, genera ideas para proyectos, planifica actividades especiales.

🆓 Es gratis practicar
Este simulador es completamente gratuito para que practiques sin límites.

La tecnología no es solo para jóvenes. ¡Es para todos!"""
    },
    {
        "id": "primeros_pasos",
        "title": "🚀 Tus primeros pasos con ChatGPT",
        "category": "curso",
        "content": """¿Listo para empezar? Sigue estos pasos simples para comenzar tu aventura con ChatGPT:

1️⃣ Practica aquí sin presión
Este simulador está hecho para que experimentes libremente. No hay forma de hacer algo "mal".

2️⃣ Empieza con preguntas simples
Prueba con cosas como:
• "¿Qué es...?"
• "¿Cómo puedo...?"
• "Explícame..."

3️⃣ Lee las respuestas con calma
No hay apuro. Tómate tu tiempo para entender cada respuesta.

4️⃣ Haz preguntas de seguimiento
Si algo no queda claro, simplemente pregunta:
• "¿Podrías explicar mejor esa parte?"
• "Dame un ejemplo de eso"
• "¿Hay una forma más simple de hacerlo?"

5️⃣ No temas equivocarte
Los errores son parte del aprendizaje. Cada pregunta te hace aprender algo nuevo.

6️⃣ Experimenta y diviértete
Prueba diferentes tipos de preguntas. ¡Sorpréndete con lo que puedes hacer!

💡 Consejo: Guarda las respuestas útiles que recibas. Cópialas a un documento para consultarlas después.

Recuerda: Todos empezamos como principiantes. ¡Tú puedes hacerlo!"""
    }
]


async def rag_answer(question: str) -> Dict[str, Any]:
    """Responde preguntas sobre el curso de IA y ChatGPT usando Gemini.
    Sistema RAG que consulta directamente con Gemini para respuestas dinámicas
    y personalizadas según cada pregunta del estudiante.
    """
    if not question or not question.strip():
        return {"error": "La pregunta está vacía"}
    
    # Usar Gemini directamente con un prompt optimizado para la capacitación
    model = _initialize_gemini()
    
    if model is not None:
        try:
            # Prompt especializado para el curso de capacitación
            enhanced_question = f"""Eres un instructor experto y paciente de un curso sobre inteligencia artificial y ChatGPT, diseñado específicamente para adultos mayores de 60 años.

🎯 CONTEXTO DEL CURSO:
Este es un curso práctico que enseña a personas mayores a usar ChatGPT y entender conceptos básicos de IA. Los estudiantes no tienen conocimientos técnicos previos.

📚 TEMAS DEL CURSO:
• Fundamentos de IA: Qué es, cómo funciona, ejemplos cotidianos
• ChatGPT: Qué es, qué puede hacer, usos prácticos en la vida diaria
• Prompting: Cómo hacer buenas preguntas, técnicas, ejemplos
• Seguridad: Privacidad, datos personales, cuidado con estafas
• Beneficios: Por qué aprender IA a esta edad, aplicaciones prácticas

✍️ ESTILO DE RESPUESTA:
- Usa lenguaje SIMPLE y CERCANO, sin tecnicismos
- Máximo 2-3 párrafos cortos y directos
- Incluye emojis para hacer la respuesta más amigable (1-2 emojis máximo)
- Usa ejemplos COTIDIANOS que adultos mayores puedan relacionar
- Sé ALENTADOR y MOTIVADOR
- Si explicas algo técnico, compáralo con situaciones de la vida real

❌ EVITA:
- Términos técnicos complejos (o explícalos de forma muy simple)
- Respuestas largas y densas
- Jerga de internet o tecnológica
- Asumir conocimientos previos

Pregunta del estudiante:
{question}

Responde de forma clara, práctica y motivadora. Si la pregunta no está relacionada con el curso, redirígela amablemente hacia los temas del curso. SEA BREVE Y CONCISO"""
            
            logger.info(f"Consultando Gemini RAG para: {question[:50]}...")
            
            response = await asyncio.to_thread(
                lambda: model.generate_content(enhanced_question)
            )
            
            reply = response.text if hasattr(response, 'text') else str(response)
            
            logger.info("✅ Respuesta RAG recibida de Gemini")
            
            return {
                "answer": reply,
                "sources": [{"type": "gemini_ai", "note": "Respuesta generada por IA especializada en capacitación"}],
                "total_results": 1,
                "source_type": "gemini_ai"
            }
            
        except Exception as e:
            logger.error(f"❌ Error al consultar Gemini para RAG: {e}")
            return {
                "answer": f"Ocurrió un error al procesar tu pregunta: {str(e)}. Por favor, intenta nuevamente o reformula tu pregunta.",
                "sources": [],
                "total_results": 0,
                "source_type": "error"
            }
    
    # Sin Gemini disponible - mensaje de fallback con información útil
    fallback_answer = f"""💡 **Sobre tu pregunta: "{question}"**

Para responder preguntas del curso, necesito que configures la API de Gemini.

📚 **Temas del curso que puedo ayudarte:**
• ¿Qué es la Inteligencia Artificial?
• ¿Qué es y cómo usar ChatGPT?
• Cómo hacer buenas preguntas (prompts)
• Seguridad y privacidad al usar IA
• Beneficios de aprender IA para adultos mayores

🔧 **Para activar las respuestas reales:**
Configura GEMINI_API_KEY en el archivo .env

¿Tienes alguna otra pregunta sobre estos temas?"""
    
    return {
        "answer": fallback_answer,
        "sources": [],
        "total_results": 0,
        "source_type": "not_found"
    }