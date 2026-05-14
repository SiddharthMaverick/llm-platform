from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.ollama_service import stream_response
from app.core.logging import logger

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):

    logger.info(f"Received prompt: {request.prompt}")

    generator = stream_response(request.prompt)

    return StreamingResponse(
        generator,
        media_type="text/plain"
    )