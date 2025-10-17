# 🔄 Actualización del Sistema RAG y Chat

## Cambios Implementados

### 1. **Chat con Respuestas Breves** ✅

El endpoint `/simulador/chat` ahora incluye un **system prompt** que garantiza:
- ✅ Respuestas **breves** (máximo 3-4 párrafos)
- ✅ Lenguaje **simple y claro** sin tecnicismos
- ✅ Uso de **analogías cotidianas** para conceptos técnicos
- ✅ Adaptado específicamente para **adultos mayores (+60 años)**

**Prompt interno:**
```
Eres un asistente educativo para adultos mayores (+60 años) aprendiendo sobre 
inteligencia artificial y ChatGPT.

IMPORTANTE: Da respuestas BREVES y CLARAS (máximo 3-4 párrafos). 
Usa lenguaje simple sin tecnicismos. Si es necesario explicar algo técnico, 
hazlo con analogías cotidianas.
```

### 2. **RAG Híbrido (KB + Gemini)** ✅

El endpoint `/simulador/rag` ahora funciona en **dos etapas**:

#### Etapa 1: Búsqueda en Knowledge Base Local
- Busca primero en los 13 documentos del KNOWLEDGE_BASE
- Si encuentra coincidencias, devuelve hasta 3 resultados más relevantes
- Respuesta rápida sin consumir API

#### Etapa 2: Fallback a Gemini (si no encuentra en KB)
- Si NO encuentra respuesta en el KB, consulta automáticamente con Gemini
- Usa un **system prompt** específico del curso
- Respuestas **breves** (2-3 párrafos máximo)
- Lenguaje **simple** adaptado a adultos mayores
- Contexto enfocado en el curso de IA y ChatGPT

**Prompt interno para RAG:**
```
Eres un instructor de un curso sobre inteligencia artificial y ChatGPT 
para adultos mayores (+60 años).

IMPORTANTE: 
- Responde de forma BREVE (máximo 2-3 párrafos)
- Usa lenguaje SIMPLE y CLARO, sin tecnicismos
- Si usas términos técnicos, explícalos con ejemplos cotidianos
- Enfócate en aplicaciones prácticas para adultos mayores
```

### 3. **Campo source_type en Respuestas** ✅

Las respuestas de `/simulador/rag` ahora incluyen un campo `source_type` que indica la fuente:

- `"knowledge_base"`: Respuesta encontrada en el KB local
- `"gemini_ai"`: Respuesta generada por Gemini (no encontrada en KB)
- `"not_found"`: No hay respuesta disponible (sin API configurada)
- `"error"`: Error al consultar Gemini

## Ejemplos de Uso

### Ejemplo 1: Pregunta en el Knowledge Base

**Request:**
```json
POST /simulador/rag
{
  "question": "qué es chatgpt"
}
```

**Response:**
```json
{
  "answer": "1. ¿Qué es ChatGPT?\nChatGPT es un asistente de IA...",
  "sources": [
    {
      "id": "chatgpt_intro",
      "title": "¿Qué es ChatGPT?",
      "category": "fundamentos"
    }
  ],
  "total_results": 1,
  "source_type": "knowledge_base"
}
```

### Ejemplo 2: Pregunta NO en Knowledge Base (usa Gemini)

**Request:**
```json
POST /simulador/rag
{
  "question": "cómo puedo usar chatgpt para planificar mis vacaciones"
}
```

**Response:**
```json
{
  "answer": "ChatGPT puede ser un excelente compañero para planificar tus vacaciones. Aquí te explico cómo:\n\nPuedes pedirle que te sugiera destinos según tu presupuesto, tus intereses y la época del año. Por ejemplo: 'Quiero viajar en verano con $2000, me gusta la playa y la tranquilidad, ¿qué destinos me recomiendas?'\n\nTambién puede ayudarte a crear un itinerario día por día, sugerir restaurantes locales, explicarte sobre el clima, y hasta darte consejos prácticos como qué documentos necesitas o qué ropa llevar.",
  "sources": [],
  "total_results": 1,
  "source_type": "gemini_ai"
}
```

### Ejemplo 3: Chat con respuestas breves

**Request:**
```json
POST /simulador/chat
{
  "prompt": "Explícame qué es la inteligencia artificial"
}
```

**Response (breve):**
```json
{
  "model": "gemini-2.5-flash",
  "reply": "La inteligencia artificial es cuando las computadoras aprenden a hacer tareas que normalmente requieren inteligencia humana. Imagínalo como enseñarle a una máquina a reconocer patrones y tomar decisiones.\n\nEjemplos que usas en tu vida diaria: cuando Netflix te recomienda películas, cuando tu teléfono reconoce tu cara para desbloquearse, o cuando Google te ayuda a encontrar información.\n\nLa IA no piensa como nosotros, pero puede procesar muchísima información muy rápido y encontrar soluciones útiles.",
  "is_simulated": false,
  "tokens_used": {
    "prompt_tokens": 45,
    "candidates_tokens": 98,
    "total_tokens": 143
  }
}
```

## Ventajas de estos Cambios

### Para el Usuario:
✅ **Respuestas más cortas**: Más fáciles de leer y entender
✅ **Lenguaje más claro**: Sin jerga técnica innecesaria
✅ **Mayor cobertura**: Si el KB no tiene la respuesta, Gemini la genera
✅ **Contexto apropiado**: Todas las respuestas están adaptadas al público objetivo

### Para el Desarrollador:
✅ **Trazabilidad**: El campo `source_type` indica de dónde vino la respuesta
✅ **Eficiencia**: KB primero (rápido y gratis), Gemini después (más costoso)
✅ **Logging mejorado**: Cada llamada a Gemini se registra
✅ **Graceful degradation**: Funciona sin API, con KB solo, o con ambos

## Flujo de RAG Híbrido

```
Usuario hace pregunta
        ↓
¿Está en KNOWLEDGE_BASE?
        ↓
    SÍ → Devuelve desde KB (rápido, gratis)
        ↓
    NO → ¿Hay GEMINI_API_KEY?
              ↓
          SÍ → Consulta Gemini (con system prompt)
              ↓
          NO → Mensaje de "no encontrado" + sugerencias
```

## Testing

Para probar el nuevo comportamiento:

```powershell
# 1. Pregunta en KB (debe devolver knowledge_base)
$body = @{ question = "qué es chatgpt" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/simulador/rag" -Method Post -ContentType "application/json" -Body $body

# 2. Pregunta NO en KB (debe consultar Gemini si hay API key)
$body = @{ question = "cómo organizar mis fotos en la computadora" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/simulador/rag" -Method Post -ContentType "application/json" -Body $body

# 3. Chat con respuestas breves
$body = @{ prompt = "Explícame qué son los algoritmos" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/simulador/chat" -Method Post -ContentType "application/json" -Body $body
```

---

**Fecha**: 17 de Octubre 2025  
**Estado**: ✅ Implementado y funcional
