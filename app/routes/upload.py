from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    BackgroundTasks
)

from app.rag.pipeline import (
    process_document
)

router = APIRouter()

DOCUMENTS_DIR = Path(
    "app/documents"
)

DOCUMENTS_DIR.mkdir(
    exist_ok=True
)


@router.post("/upload")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):

    file_path = (
        DOCUMENTS_DIR / file.filename
    )

    with open(file_path, "wb") as f:

        content = await file.read()

        f.write(content)

    background_tasks.add_task(
        process_document,
        str(file_path)
    )

    return {
        "message":
        f"{file.filename} uploaded successfully"
    }