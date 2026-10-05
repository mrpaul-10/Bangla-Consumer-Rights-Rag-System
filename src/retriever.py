"""
Vector store (ChromaDB) setup, indexing, and retrieval logic.
"""

import chromadb
from chromadb.utils import embedding_functions


class VectorStore:
    def __init__(self, collection_name: str = "consumer_rights_bn", persist_path: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_path)
        self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name, embedding_function=self.embed_fn
        )

    def add_chunks(self, chunks: list[dict]):
        self.collection.add(
            documents=[c["content"] for c in chunks],
            metadatas=[{"section": c["section"]} for c in chunks],
            ids=[f"chunk_{i}" for i in range(len(chunks))],
        )

    def query(self, query_text: str, top_k: int = 4):
        return self.collection.query(query_texts=[query_text], n_results=top_k)

    def count(self):
        return self.collection.count()


if __name__ == "__main__":
    store = VectorStore()
    print(f"Documents in store: {store.count()}\n")

    test_queries = [
        "পণ্য ভেজাল হলে ভোক্তা কী প্রতিকার পেতে পারেন?",
        "অভিযোগ কীভাবে দায়ের করতে হয়?",
        "ভোক্তা অধিকার লঙ্ঘনের শাস্তি কী?",
    ]

    for q in test_queries:
        print(f"প্রশ্ন: {q}")
        results = store.query(q, top_k=3)
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            print(f"  [{meta['section']}] (distance: {dist:.3f})")
            print(f"  {doc[:150]}...")
        print("----")