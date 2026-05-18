import faiss
import pickle
import numpy as np
from pathlib import Path

VECTOR_STORE_DIR = Path("vector_store")

VECTOR_STORE_DIR.mkdir(exist_ok=True)

INDEX_PATH = VECTOR_STORE_DIR / "faiss.index"
DOCS_PATH = VECTOR_STORE_DIR / "documents.pkl"

index = faiss.IndexFlatL2(384)

documents = []


def add_embeddings(chunks, embeddings, doc_source="unknown"):

    global documents
    global index

    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    index.add(embeddings)

    for idx, chunk in enumerate(chunks):
        documents.append({
            "text": chunk,
            "source": doc_source,
            "chunk_id": len(documents)
        })


def search(query_embedding, k=3):

    global documents
    global index

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


def save_index():

    global index
    global documents

    faiss.write_index(
        index,
        str(INDEX_PATH)
    )

    with open(DOCS_PATH, "wb") as f:

        pickle.dump(documents, f)

    print("Vector store saved")


def load_index():

    global index
    global documents

    if INDEX_PATH.exists():

        index = faiss.read_index(
            str(INDEX_PATH)
        )

        with open(DOCS_PATH, "rb") as f:

            documents = pickle.load(f)

        print(
            f"Loaded {len(documents)} chunks"
        )

        return True

    return False