# Simulador ChatGPT - Backend de Capacitación

API backend para un simulador de ChatGPT diseñado para capacitar a personas mayores de 60 años en el uso de inteligencia artificial.

## 🚀 Características

- **Simulador de Chat**: Endpoint que simula conversaciones con ChatGPT
- **Sistema RAG**: Base de conocimiento sobre IA, ChatGPT, prompting y seguridad
- **Diseñado para adultos mayores**: Contenido adaptado y explicaciones claras
- **Modo simulación**: Funciona sin API key para práctica segura

## 📋 Requisitos

- Python 3.8+
- pip

## 🛠️ Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar variables de entorno (opcional):
```bash
cp .env.example .env
# Editar .env y agregar tu GEMINI_API_KEY si deseas usar la API real
```

## ▶️ Ejecutar el servidor

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

O en PowerShell:
```powershell
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Endpoints

### GET /
Página de bienvenida con lista de endpoints disponibles

### GET /health
Verificación de estado del servicio

### POST /simulador/chat
Simula una conversación con ChatGPT

**Request:**
```json
{
  "prompt": "¿Qué es la inteligencia artificial?"
}
```

**Response:**
```json
{
  "model": "gemini-2.5-flash",
  "reply": "...",
  "is_simulated": true
}
```

### POST /simulador/rag
Consulta la base de conocimiento del curso

**Request:**
```json
{
  "question": "¿Cómo hacer buenos prompts?"
}
```

**Response:**
```json
{
  "answer": "...",
  "sources": [...],
  "total_results": 3
}
```

## 📖 Documentación Interactiva

Una vez iniciado el servidor, visita:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🗂️ Estructura del Proyecto

```
api/
├── __init__.py
├── main.py              # Aplicación FastAPI principal
├── config/
│   ├── __init__.py
│   └── config.py        # Configuración y settings
├── routes/
│   ├── __init__.py
│   └── simulador_router.py  # Rutas del simulador
└── services/
    ├── __init__.py
    └── simulador_service.py  # Lógica de negocio y KB
```

## 🔐 Seguridad

- El modo simulación NO requiere API key
- En producción, asegurar endpoints con autenticación
- Configurar CORS apropiadamente para producción

## 📝 Base de Conocimiento (RAG)

El sistema incluye información sobre:
- ✅ Fundamentos de IA y ChatGPT
- ✅ Técnicas de prompting
- ✅ Seguridad y privacidad
- ✅ Contenido adaptado para adultos mayores
- ✅ Limitaciones y mejores prácticas

## 🤝 Contribuir

Este proyecto está diseñado para capacitación. Siéntete libre de expandir la base de conocimiento o agregar nuevos endpoints.
