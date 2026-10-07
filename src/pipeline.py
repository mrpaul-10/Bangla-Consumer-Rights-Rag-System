"""
Full RAG pipeline: retrieval + generation, with an out-of-scope guard.
"""

from src.retriever import VectorStore
from src.generator import generate_answer

# Step 7-এর real data দেখে ঠিক করা হয়েছে:
# relevant answer-গুলোর distance ছিল ~0.2-0.45, তাই buffer সহ 0.65 (৬৫ কে চেঞ্জ করে ৮০ করা হলো আকুরেসি চেক করার জন্য )
DISTANCE_THRESHOLD = 0.80


def answer_question(query: str, top_k: int = 5) -> dict:
    store = VectorStore()
    results = store.query(query, top_k=top_k)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    if not documents or min(distances) > DISTANCE_THRESHOLD:
        return {
            "answer": "দুঃখিত, এই তথ্য আইনের প্রদত্ত অংশে পাওয়া যায়নি। এটি সম্ভবত এই আইনের আওতার বাইরের একটি বিষয়।",
            "sources": [],
            "found": False,
        }

    context_chunks = [
        {"section": meta["section"], "content": doc}
        for doc, meta in zip(documents, metadatas)
    ]

    answer = generate_answer(query, context_chunks)
    not_found_phrase = "পাওয়া যায়নি"
    actually_found = not_found_phrase not in answer

    sources = list({c["section"].strip() for c in context_chunks}) if actually_found else []

    return {
        "answer": answer,
        "sources": sources,
        "found": actually_found,
    }


if __name__ == "__main__":
    test_queries = [
        "অভিযোগ কীভাবে দায়ের করতে হয়?",
        "ঢাকার আবহাওয়া কেমন আজ?",  # সম্পূর্ণ out-of-scope প্রশ্ন, test করার জন্য
    ]

    for q in test_queries:
        print(f"প্রশ্ন: {q}")
        result = answer_question(q)
        print(f"উত্তর: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print(f"Found: {result['found']}")
        print("----")