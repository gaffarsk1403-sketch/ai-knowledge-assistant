# AI Knowledge Assistant

A small end-to-end AI/LLM project that demonstrates grounded question answering over an internal knowledge base.

The goal is to show a practical application architecture rather than a toy prompt demo: retrieval, prompt grounding, API orchestration, source visibility, tests, and a clear path toward production hardening.

## What it does

A user asks a question through a REST API. The application:

1. validates the request;
2. retrieves relevant knowledge snippets;
3. supplies only those snippets to the LLM;
4. instructs the model not to invent missing information;
5. returns the answer together with the source snippets used.

## Tech stack

- Python
- FastAPI
- OpenAI API
- Pydantic
- Pytest
- REST/JSON
- Retrieval-augmented generation concepts

## Architecture

```text
Client
  |
  v
FastAPI /ask
  |
  +--> Retrieval Service ----> Knowledge Base
  |
  +--> LLM Service ---------> OpenAI model
  |
  v
Grounded answer + sources
```

The retrieval and LLM layers are intentionally separated so either component can be upgraded independently. See [docs/architecture.md](docs/architecture.md) for production evolution ideas.

## Run locally

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it using the command appropriate for your operating system.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the model

Copy `.env.example` to `.env` and set your API key:

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

Export/load those environment variables before starting the API.

### 4. Start the service

```bash
uvicorn app.main:app --reload
```

Open the generated FastAPI docs at `/docs`.

## Example request

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is required before a production release?"}'
```

Example response:

```json
{
  "answer": "Production releases require peer review, automated tests, staging validation, and a documented rollback plan.",
  "sources": [
    {
      "title": "Release Process",
      "content": "Production releases require peer review, automated tests, staging validation, and a documented rollback plan.",
      "score": 0.5
    }
  ]
}
```

## Testing

```bash
pytest
```

The included tests verify that relevant knowledge is retrieved and unrelated questions do not receive fabricated context.

## Engineering choices

- **Grounded answers:** the system prompt tells the model to answer only from retrieved context.
- **Separation of concerns:** API, retrieval, data models, and LLM orchestration live in separate modules.
- **Graceful local behavior:** if no API key is configured, the service still demonstrates retrieval instead of failing silently.
- **Source transparency:** every response includes the context used to produce the answer.
- **No employer data:** all sample knowledge in this repository is synthetic.

## Next improvements

- embeddings and vector search;
- document upload and chunking;
- React/Next.js front end;
- authentication and role-aware access;
- evaluation tests for groundedness and hallucination;
- observability for latency, model usage, and failures;
- caching and model fallback;
- prompt versioning and automated quality checks.

## Why I built this

I wanted a compact example of how I approach an AI-enabled feature end to end: define the use case, isolate the model behind a service boundary, retrieve the right context, validate outputs, expose the capability through an API, add tests, and document how the design could evolve for production.

This is a portfolio project and does not contain proprietary or employer code, data, or business logic.
