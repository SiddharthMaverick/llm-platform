import uuid

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.rag_service import rag_chat
from app.core.logging import logger

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):

    session_id = request.session_id or str(uuid.uuid4())
    logger.info(f"Received prompt: {request.prompt} session_id={session_id}")

    generator = rag_chat(
        session_id,
        request.prompt
    )

    return StreamingResponse(
        generator,
        media_type="text/plain"
    )