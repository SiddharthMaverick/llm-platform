from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routes.chat import router as chat_router
from app.rag.startup import initialize_rag
from app.routes.health import (
    router as health_router
)
from app.middleware.timing import (
    TimingMiddleware
)
from app.routes.upload import (
    router as upload_router
)
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TimingMiddleware
)
# Mount static files
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.on_event("startup")
async def startup_event():

    initialize_rag()


app.include_router(chat_router)

app.include_router(health_router)
app.include_router(upload_router)
@app.get("/")
async def root():
    return FileResponse("static/index.html")