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
    prompt: str
):

    contexts = retrieve(prompt)

    context_text = "\n\n".join([
        f"""
SOURCE: {doc['source']}
CHUNK: {doc['chunk_id']}

{doc['text']}
"""
        for doc in contexts
    ])

    history = get_history(session_id)

    messages = []

    system_prompt = f"""
You are a helpful AI assistant.

Use the provided context to answer questions.

Context:
{context_text}
"""

    messages.append({
        "role": "system",
        "content": system_prompt
    })

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": prompt
    })

    add_message(session_id,"user",prompt)

    stream = client.chat(
        model=settings.model_name,
        messages=messages,
        stream=True
    )

    assistant_response = ""

    for chunk in stream:

        content = chunk["message"]["content"]

        if content:

            assistant_response += content

            yield content

    add_message(session_id,"assistant",assistant_response)