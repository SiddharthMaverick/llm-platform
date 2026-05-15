from app.rag.embedder import embed_text
from app.rag.vector_store import search


def retrieve(query, k=3):

    embedding = embed_text([query])[0]

    results = search(embedding, k)

    return results