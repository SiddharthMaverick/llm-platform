from app.rag.retriever import retrieve

from app.services.ollama_service import client

from app.services.memory import (
    add_message,
    get_history,
    clear_history
)

from app.core.config import settings


async def rag_chat(
    session_id: str,
    prompt: str,
    system_prompt: str | None = None,
    use_context: bool = True,
    mode: str | None = None,
):

    contexts = []
    if use_context:
        try:
            contexts = retrieve(prompt)
        except Exception as e:
            yield f"Error retrieving context: {str(e)}"
            return

    context_text = "\n\n".join([
        f"""
SOURCE: {doc['source']}
CHUNK: {doc['chunk_id']}

{doc['text']}
"""
        for doc in contexts
    ])

    history = get_history(session_id)

    default_system = """
You are a helpful AI assistant.

Use the provided context to answer questions.
"""

    system_prompt = system_prompt.strip() if system_prompt else default_system

    if mode:
        system_prompt = f"[MODE: {mode}]\n{system_prompt}"

    if use_context:
        system_prompt += f"\n\nContext:\n{context_text or 'No relevant context found.'}"
    else:
        system_prompt += "\n\nIgnore any retrieved document context for this request."

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages.extend(history)
    messages.append({
        "role": "user",
        "content": prompt
    })

    add_message(session_id, "user", prompt)

    try:
        stream = client.chat(
            model=settings.model_name,
            messages=messages,
            stream=True
        )
    except Exception as e:
        yield f"LLM error: {str(e)}"
        return

    assistant_response = ""

    for chunk in stream:
        content = chunk.get("message", {}).get("content")
        if content:
            assistant_response += content
            yield content

    add_message(session_id, "assistant", assistant_response)
