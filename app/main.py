from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.rag.startup import initialize_rag

app = FastAPI()


@app.on_event("startup")
async def startup_event():

    initialize_rag()


app.include_router(chat_router)


@app.get("/")
async def root():

    return {
        "message": "LLM platform running"
    }