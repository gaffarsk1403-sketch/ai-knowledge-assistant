from fastapi import FastAPI

from app.models import AskRequest, AskResponse, SourceSnippet
from app.services.llm import generate_answer
from app.services.retrieval import retrieve


app = FastAPI(
    title="AI Knowledge Assistant",
    version="1.0.0",
    description="A small retrieval-augmented LLM API for grounded Q&A.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    matches = retrieve(request.question)
    answer = generate_answer(request.question, matches)

    return AskResponse(
        answer=answer,
        sources=[SourceSnippet(**item) for item in matches],
    )
