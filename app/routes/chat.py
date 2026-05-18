import uuid

from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.rag_service import rag_chat
from app.core.logging import logger

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):

    session_id = request.session_id or str(uuid.uuid4())
    logger.info(
        f"Received prompt={request.prompt} session_id={session_id} "
        f"use_context={request.use_context} mode={request.mode}"
    )

    generator = rag_chat(
        session_id=session_id,
        prompt=request.prompt,
        system_prompt=request.system_prompt,
        use_context=request.use_context,
        mode=request.mode,
    )

    return StreamingResponse(
        generator,
        media_type="text/plain"
    )


@router.post("/session/clear")
async def clear_session(session_id: str = Body(..., embed=True)):
    from app.services.memory import clear_history

    if not session_id:
        raise HTTPException(status_code=400, detail="session_id is required")

    clear_history(session_id)
    return {"cleared": True, "session_id": session_id}
