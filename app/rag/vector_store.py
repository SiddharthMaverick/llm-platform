import faiss
import numpy as np

index = faiss.IndexFlatL2(384)


def add_embeddings(embeddings):

    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    index.add(embeddings)


def search(query_embedding, k=3):

    query_embedding = np.array(
        [query_embedding],
        dtype="float32"
    )

    distances, indices = index.search(
        query_embedding,
        k
    )

    return indices