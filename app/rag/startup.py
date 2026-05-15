from pathlib import Path

from app.rag.ingest import (
    read_pdf,
    chunk_text
)

from app.rag.embedder import embed_text

from app.rag.vector_store import (
    add_embeddings,
    save_index,
    load_index
)

DOCUMENTS_DIR = Path("app/documents")


def initialize_rag():

    loaded = load_index()

    if loaded:

        print("Using existing vector store")

        return

    print("Building new vector store")

    all_chunks = []

    for pdf_file in DOCUMENTS_DIR.glob("*.pdf"):

        text = read_pdf(str(pdf_file))

        chunks = chunk_text(
            text=text,
            source=pdf_file.name
        )

        all_chunks.extend(chunks)

    texts = [
        chunk["text"]
        for chunk in all_chunks
    ]

    embeddings = embed_text(texts)

    add_embeddings(
        all_chunks,
        embeddings
    )

    save_index()

    print(
        f"Indexed {len(all_chunks)} chunks"
    )