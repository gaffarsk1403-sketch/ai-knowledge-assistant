from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Document:
    title: str
    content: str


DOCUMENTS = [
    Document(
        title="Release Process",
        content=(
            "Production releases require peer review, automated tests, "
            "staging validation, and a documented rollback plan."
        ),
    ),
    Document(
        title="Incident Response",
        content=(
            "High-priority incidents are triaged by the on-call engineer. "
            "The team records impact, timeline, root cause, and follow-up actions."
        ),
    ),
    Document(
        title="Engineering Standards",
        content=(
            "Services should include structured logging, input validation, "
            "automated tests, clear ownership, and operational documentation."
        ),
    ),
]


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def retrieve(question: str, limit: int = 3) -> list[dict]:
    query_tokens = _tokens(question)
    ranked = []

    for document in DOCUMENTS:
        document_tokens = _tokens(f"{document.title} {document.content}")
        overlap = len(query_tokens & document_tokens)
        score = overlap / max(len(query_tokens), 1)
        ranked.append(
            {
                "title": document.title,
                "content": document.content,
                "score": round(score, 3),
            }
        )

    ranked.sort(key=lambda item: item["score"], reverse=True)
    return [item for item in ranked[:limit] if item["score"] > 0]
