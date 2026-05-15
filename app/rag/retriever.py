from app.rag.embedder import embed_text
from app.rag.vector_store import search


def retrieve(query, k=3):

    embedding = embed_text([query])[0]

    results = search(embedding, k)
    
    # Extract text from results (keep source metadata)
    return results


def retrieve_with_sources(query, k=3):
    
    embedding = embed_text([query])[0]
    
    results = search(embedding, k)
    
    # Return both text and source
    return results