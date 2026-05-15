from app.rag.ingest import read_pdf, chunk_text
from app.rag.embedder import embed_text
from app.rag.vector_store import add_embeddings, clear_embeddings
import os
from pathlib import Path

DOCUMENTS_PATH = "app/documents"


def initialize_rag():

    clear_embeddings()
    total_chunks = 0
    
    # Get all PDF files from documents folder
    pdf_files = sorted(Path(DOCUMENTS_PATH).glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {DOCUMENTS_PATH}")
        return
    
    for pdf_path in pdf_files:
        doc_name = pdf_path.name
        print(f"Indexing {doc_name}...")
        
        try:
            text = read_pdf(str(pdf_path))
            chunks = chunk_text(text)
            embeddings = embed_text(chunks)
            add_embeddings(chunks, embeddings, doc_source=doc_name)
            total_chunks += len(chunks)
            print(f"  ✓ Added {len(chunks)} chunks from {doc_name}")
        except Exception as e:
            print(f"  ✗ Error processing {doc_name}: {e}")
    
    print(f"\n✓ Successfully indexed {total_chunks} chunks from {len(pdf_files)} documents")