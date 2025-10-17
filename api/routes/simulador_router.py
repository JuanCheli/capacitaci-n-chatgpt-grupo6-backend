from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services.simulador_service import chat_simulate, rag_answer

router = APIRouter(prefix="/simulador", tags=["simulador"])


class ChatRequest(BaseModel):
    prompt: str


class RagRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    """
    Endpoint para simular una conversación con ChatGPT.
    Recibe un prompt y devuelve una respuesta simulada (o real si hay API key configurada).
    """
    result = await chat_simulate(req.prompt)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/rag")
async def rag_endpoint(req: RagRequest):
    """
    Endpoint para consultar la base de conocimiento del curso (RAG).
    Responde preguntas sobre IA, ChatGPT, prompting, seguridad y el curso.
    """
    result = await rag_answer(req.question)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
