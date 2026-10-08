from app.services.retrieval import retrieve


def test_retrieval_returns_release_document():
    results = retrieve("What is required before a production release?")

    assert results
    assert results[0]["title"] == "Release Process"


def test_retrieval_returns_empty_for_unrelated_query():
    results = retrieve("What is the office cafeteria menu?")

    assert results == []
