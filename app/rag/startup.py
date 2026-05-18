from pathlib import Path

from app.rag.ingest import (
    read_pdf,
    chunk_text
)

from app.rag.embedder import embed_text
from app.rag.vector_store import add_embeddings

PDF_PATH = "app/documents/transformer.pdf"


def initialize_rag():

    text = read_pdf(PDF_PATH)

    chunks = chunk_text(text)

    embeddings = embed_text(chunks)

    add_embeddings(chunks, embeddings)

    print(f"Indexed {len(chunks)} chunks")