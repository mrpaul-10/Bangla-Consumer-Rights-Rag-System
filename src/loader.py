"""
Loads and cleans raw text from the Bangla law PDF.
"""

import re


def load_pdf_text(path: str) -> str:
    """
    Extract text using PyMuPDF (fitz), with sort=True for better
    reading-order handling on this PDF's multi-column layout.
    This is the PRIMARY extractor — pdfplumber gave broken matra/kar
    ordering on this PDF's font, so we use PyMuPDF instead.
    """
    import fitz  # PyMuPDF

    doc = fitz.open(path)
    full_text = []
    for page in doc:
        full_text.append(page.get_text("text", sort=True))
    return "\n".join(full_text)


def load_pdf_text_pdfplumber_fallback(path: str) -> str:
    """
    Fallback extractor using pdfplumber, kept in case a different
    PDF (future scope) renders better with this library instead.
    NOTE: on the Consumer Rights Act PDF, this gave broken matra
    ordering — do not use as default for this document.
    """
    import pdfplumber

    full_text = []
    with pdfplumber.open(path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                full_text.append(text)
            else:
                print(f"[WARN] No extractable text on page {page_num}")
    return "\n".join(full_text)


def clean_text(text: str) -> str:
    """Basic cleanup: collapse repeated newlines/spaces, strip page numbers."""
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n\d{1,3}\n", "\n", text)
    return text.strip()


if __name__ == "__main__":
    raw = load_pdf_text("data/raw/consumer_rights_act_bn.pdf")
    cleaned = clean_text(raw)
    print(cleaned[:2000])
    print(f"\n\nTotal characters extracted: {len(cleaned)}")