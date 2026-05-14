from ollama import Client

from app.core.config import settings

client = Client(host=settings.ollama_host)


async def stream_response(prompt: str):

    stream = client.chat(
        model=settings.model_name,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True
    )

    for chunk in stream:

        content = chunk["message"]["content"]

        if content:
            yield content
