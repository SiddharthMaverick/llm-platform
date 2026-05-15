import faiss
import numpy as np

index = faiss.IndexFlatL2(384)

documents = []


def add_embeddings(chunks, embeddings):

    global documents

    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    index.add(embeddings)

    documents.extend(chunks)


def search(query_embedding, k=3):

    global documents

    query_embedding = np.array(
        [query_embedding],
        dtype="float32"
    )

    distances, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for idx in indices[0]:

        if 0 <= idx < len(documents):

            results.append(documents[idx])

    return results