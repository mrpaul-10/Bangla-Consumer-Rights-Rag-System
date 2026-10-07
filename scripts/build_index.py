"""
One-time script: loads PDF, cleans, chunks, indexes into vector store.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.loader import load_pdf_text, clean_text
from src.chunker import chunk_by_section, split_long_chunks, save_chunks
from src.retriever import VectorStore

PDF_PATH = "data/raw/consumer_rights_act_bn.pdf"

def main():
    print("Loading PDF...")
    raw = load_pdf_text(PDF_PATH)
    cleaned = clean_text(raw)

    print("Chunking by section...")
    chunks = chunk_by_section(cleaned)
    chunks = split_long_chunks(chunks)
    save_chunks(chunks)
    print(f"Created {len(chunks)} chunks.")

    print("Indexing into vector store...")
    store = VectorStore()
    store.reset()
    store.add_chunks(chunks)
    print(f"Done. Total documents in store: {store.count()}")

if __name__ == "__main__":
    main()