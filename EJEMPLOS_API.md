# Ejemplos de Requests para probar la API

## Usando curl (bash/terminal)

### 1. Verificar que el servidor está corriendo
```bash
curl http://localhost:8000/
```

### 2. Health check
```bash
curl http://localhost:8000/health
```

### 3. Simular chat
```bash
curl -X POST http://localhost:8000/simulador/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explícame qué es la inteligencia artificial de forma simple"}'
```

### 4. Consulta RAG - Seguridad
```bash
curl -X POST http://localhost:8000/simulador/rag \
  -H "Content-Type: application/json" \
  -d '{"question": "consejos de seguridad"}'
```

### 5. Consulta RAG - Prompting
```bash
curl -X POST http://localhost:8000/simulador/rag \
  -H "Content-Type: application/json" \
  -d '{"question": "cómo hacer buenos prompts"}'
```

---

## Usando PowerShell (Windows)

### 1. Verificar servidor
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get
```

### 2. Health check
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```

### 3. Simular chat
```powershell
$body = @{
    prompt = "¿Qué es ChatGPT y para qué sirve?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/simulador/chat" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

### 4. Consulta RAG
```powershell
$body = @{
    question = "qué es un prompt"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/simulador/rag" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

---

## Usando Python requests

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# 2. Chat simulado
response = requests.post(
    f"{BASE_URL}/simulador/chat",
    json={"prompt": "Dame 3 consejos para usar ChatGPT"}
)
print(response.json())

# 3. Consulta RAG
response = requests.post(
    f"{BASE_URL}/simulador/rag",
    json={"question": "seguridad con IA"}
)
print(response.json())
```

---

## Usando JavaScript/Fetch

```javascript
const BASE_URL = "http://localhost:8000";

// 1. Chat simulado
fetch(`${BASE_URL}/simulador/chat`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    prompt: "¿Cómo puedo escribir mejores prompts?"
  })
})
.then(response => response.json())
.then(data => console.log(data));

// 2. Consulta RAG
fetch(`${BASE_URL}/simulador/rag`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: "privacidad con ChatGPT"
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Casos de prueba completos

### Caso 1: Usuario nuevo que pregunta sobre ChatGPT
```json
POST /simulador/rag
{
  "question": "qué es chatgpt"
}
```

### Caso 2: Usuario que quiere aprender a hacer prompts
```json
POST /simulador/rag
{
  "question": "ejemplos de prompts"
}
```

### Caso 3: Usuario preocupado por seguridad
```json
POST /simulador/rag
{
  "question": "seguridad y privacidad"
}
```

### Caso 4: Usuario practicando con el simulador
```json
POST /simulador/chat
{
  "prompt": "Ayúdame a escribir un email de agradecimiento a un amigo que me regaló un libro"
}
```

### Caso 5: Usuario preguntando sobre limitaciones
```json
POST /simulador/rag
{
  "question": "limitaciones de chatgpt"
}
```

---

## Respuestas esperadas

### Chat simulado (sin API key)
```json
{
  "model": "gemini-2.5-flash",
  "reply": "¡Hola! Soy el simulador de ChatGPT. Has preguntado: '...'...",
  "is_simulated": true
}
```

### Chat real (con API key)
```json
{
  "model": "gemini-2.5-flash",
  "reply": "La inteligencia artificial es...",
  "is_simulated": false,
  "tokens_used": {...}
}
```

### RAG (con resultados en KB)
```json
{
  "answer": "1. Consejos para hacer buenos prompts\nPara obtener mejores respuestas...",
  "sources": [
    {
      "id": "prompt_consejos",
      "title": "Consejos para hacer buenos prompts",
      "category": "prompting"
    }
  ],
  "total_results": 2,
  "source_type": "knowledge_base"
}
```

### RAG (respuesta de Gemini - no encontrado en KB)
```json
{
  "answer": "Una respuesta breve y clara generada por Gemini sobre el tema consultado...",
  "sources": [],
  "total_results": 1,
  "source_type": "gemini_ai"
}
```

### RAG (sin resultados ni API)
```json
{
  "answer": "No encontré información específica sobre esa pregunta...",
  "sources": [],
  "total_results": 0,
  "source_type": "not_found"
}
```
