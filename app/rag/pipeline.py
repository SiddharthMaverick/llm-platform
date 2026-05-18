from app.rag.ingest import (
    read_pdf,
    chunk_text
)

from app.rag.embedder import (
    embed_text
)

from app.rag.vector_store import (
    add_embeddings,
    save_index
)


def process_document(pdf_path):

    print(f"Processing {pdf_path}")

    text = read_pdf(pdf_path)

    chunks = chunk_text(
        text=text,
        source=pdf_path
    )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embed_text(texts)

    add_embeddings(
        chunks,
        embeddings
    )

    save_index()

    print(
        f"Indexed {len(chunks)} chunks "
        f"from {pdf_path}"
    )