import os

from openai import OpenAI


SYSTEM_PROMPT = """You are a concise enterprise knowledge assistant.
Answer only from the supplied context. If the context is insufficient,
say that you do not have enough information. Do not invent policies,
numbers, or operational details."""


def generate_answer(question: str, context: list[dict]) -> str:
    if not context:
        return "I do not have enough information in the knowledge base to answer that."

    context_text = "\n\n".join(
        f"[{item['title']}]\n{item['content']}" for item in context
    )

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return (
            "Relevant context was found, but no LLM API key is configured. "
            f"Top source: {context[0]['title']}."
        )

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    response = client.responses.create(
        model=model,
        instructions=SYSTEM_PROMPT,
        input=(
            f"Context:\n{context_text}\n\n"
            f"Question: {question}\n"
            "Answer in 2-4 sentences and ground the answer in the context."
        ),
    )

    return response.output_text.strip()
