"""
Semantic search over the ChromaDB vector store.
Supports optional filters by year range, report type, and source agency.
"""
from pipeline.embedder import embed
from pipeline.ingest import get_collection
from config import MAX_SYNTHESIS_CHUNKS


def search(
    query: str,
    n_results: int = MAX_SYNTHESIS_CHUNKS,
    year_min=None,
    year_max=None,
    report_types=None,
    agencies=None,
):
    """
    Returns a list of result dicts, each containing:
      text, title, year, authors, report_type, source_url, source_agency, distance
    """
    collection = get_collection()
    if collection.count() == 0:
        return []

    query_embedding = embed([query])[0]

    where_clauses = []
    if year_min is not None:
        where_clauses.append({"year": {"$gte": year_min}})
    if year_max is not None:
        where_clauses.append({"year": {"$lte": year_max}})
    if report_types:
        where_clauses.append({"report_type": {"$in": report_types}})
    if agencies:
        where_clauses.append({"source_agency": {"$in": agencies}})

    where = {"$and": where_clauses} if len(where_clauses) > 1 else (where_clauses[0] if where_clauses else None)

    query_kwargs = dict(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count()),
        include=["documents", "metadatas", "distances"],
    )
    if where:
        query_kwargs["where"] = where

    results = collection.query(**query_kwargs)

    output = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        output.append({
            "text": doc,
            "title": meta.get("title", "Unknown"),
            "year": meta.get("year") or "Unknown",
            "authors": meta.get("authors", ""),
            "report_type": meta.get("report_type", ""),
            "source_url": meta.get("source_url", ""),
            "source_agency": meta.get("source_agency", ""),
            "relevance_score": round(1 - dist, 3),
        })

    return output
