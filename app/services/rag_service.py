from app.rag.retriever import retrieve
from app.services.ollama_service import client
from app.core.config import settings


async def rag_chat(prompt: str):

    contexts = retrieve(prompt)

    context_text = "\n\n".join([doc["text"] for doc in contexts])

    augmented_prompt = f"""
Use the following context to answer the question.

Context:
{context_text}

Question:
{prompt}
"""

    stream = client.chat(
        model=settings.model_name,
        messages=[
            {
                "role": "user",
                "content": augmented_prompt
            }
        ],
        stream=True
    )

    for chunk in stream:

        content = chunk["message"]["content"]

        if content:
            yield content