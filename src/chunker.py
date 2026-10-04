"""
Splits cleaned law text into section-wise chunks.
NOTE: Section markers in this PDF are bare numbers like "১।" or "২৷"
(no "ধারা" word prefix) — pattern adjusted after inspecting real
extraction output in Step 4.
"""

import re
import json


# বাংলা সংখ্যা (০-৯) + দাড়ি (। বা ৷) দিয়ে section marker ধরা হচ্ছে
SECTION_PATTERN = r"(?<![০-৯])(?<!\()([০-৯]+)[।৷]"


def chunk_by_section(text: str) -> list[dict]:
    matches = list(re.finditer(SECTION_PATTERN, text))

    chunks = []

    # প্রথম section marker-এর আগে যা থাকবে (ভূমিকা অংশ)
    if matches:
        preamble = text[:matches[0].start()].strip()
        if preamble:
            chunks.append({"section": "প্রারম্ভিক অংশ", "content": preamble})

    for i, match in enumerate(matches):
        section_num = match.group(1)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        if content:
            chunks.append({"section": f"ধারা {section_num}", "content": content})

    return chunks


def split_long_chunks(chunks: list[dict], max_chars: int = 800, overlap: int = 100) -> list[dict]:
    result = []
    for chunk in chunks:
        content = chunk["content"]
        section = chunk["section"]

        if len(content) <= max_chars:
            result.append(chunk)
            continue

        start = 0
        while start < len(content):
            end = start + max_chars
            piece = content[start:end]
            result.append({"section": section, "content": piece.strip()})
            start = end - overlap

    return result


def save_chunks(chunks: list[dict], path: str = "data/processed/chunks.json"):
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)


def load_chunks(path: str = "data/processed/chunks.json") -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    from src.loader import load_pdf_text, clean_text

    raw = load_pdf_text("data/raw/consumer_rights_act_bn.pdf")
    cleaned = clean_text(raw)
    chunks = chunk_by_section(cleaned)
    chunks = split_long_chunks(chunks)

    print(f"Total chunks: {len(chunks)}")
    for c in chunks[:5]:
        print("----")
        print(c["section"])
        print(c["content"][:200])

    save_chunks(chunks)