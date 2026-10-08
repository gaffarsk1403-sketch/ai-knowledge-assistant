# Architecture

## Request flow

1. A client sends a question to `POST /ask`.
2. The retrieval layer ranks small knowledge-base documents by token overlap.
3. The highest-value snippets are assembled as grounded context.
4. The LLM service sends the question and retrieved context to the configured model.
5. The API returns both the generated answer and the source snippets used.

## Why this design

The project intentionally separates retrieval, LLM orchestration, and the API layer. That keeps the code testable and makes it straightforward to replace the sample retrieval algorithm with embeddings or a vector database later.

## Production evolution

A production version could add:

- vector embeddings and a managed vector store;
- document ingestion and chunking;
- authentication and role-aware retrieval;
- prompt/version management;
- request tracing, latency and token metrics;
- evaluation datasets for groundedness and answer quality;
- rate limiting, caching, retries and model fallbacks;
- PII redaction and content-safety controls.
