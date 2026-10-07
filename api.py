"""
FastAPI backend exposing the RAG pipeline as a REST API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.pipeline import answer_question

app = FastAPI(title="Bangla Consumer Rights Assistant API")

# CORS: যাতে Streamlit বা অন্য frontend (ভিন্ন domain/port থেকে)
# এই API কল করতে পারে, browser block না করে
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]
    found: bool


@app.get("/")
def root():
    return {"status": "ok", "message": "Bangla Consumer Rights Assistant API is running."}


@app.post("/ask", response_model=AnswerResponse)
def ask(request: QuestionRequest):
    result = answer_question(request.question)
    return AnswerResponse(
        answer=result["answer"],
        sources=result["sources"],
        found=result["found"],
    )