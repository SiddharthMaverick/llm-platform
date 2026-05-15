from app.rag.build_index import *
from app.rag.retriever import retrieve

query = "What is attention?"

results = retrieve(query)

for i, result in enumerate(results):

    print(f"\nResult {i+1}:\n")

    print(result)