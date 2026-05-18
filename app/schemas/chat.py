from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):

    session_id: Optional[str] = None
    prompt: str
    system_prompt: Optional[str] = None
    use_context: bool = True
    mode: Optional[str] = None
