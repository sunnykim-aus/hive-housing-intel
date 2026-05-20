"""
Orchestrates the full ingestion pipeline:
  crawl AHURI → extract PDFs → chunk text → embed → store in ChromaDB
"""
import chromadb
from chromadb.config import Settings
from tqdm import tqdm
from pathlib import Path

from config import AHURI_DIR, CHROMA_DIR, META_FILE, CHUNK_WORDS, CHUNK_OVERLAP_WORDS
from crawler.ahuri import crawl as ahuri_crawl
from pipeline.processor import process_all
from pipeline.embedder import embed

COLLECTION_NAME = "housing_reports"


def get_collection(chroma_dir: Path = CHROMA_DIR):
    client = chromadb.PersistentClient(path=str(chroma_dir))
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def run_crawl(max_reports: int = 500):
    print("=" * 60)
    print("STEP 1: Crawling AHURI reports")
    print("=" * 60)
    ahuri_crawl(
        output_dir=AHURI_DIR,
        meta_file=META_FILE,
        max_reports=max_reports,
    )


def run_ingest(collection=None):
    if collection is None:
        collection = get_collection()

    existing_ids = set(collection.get(include=[])["ids"])
    print(f"Already indexed: {len(existing_ids)} chunks")

    print("\nSTEP 2: Processing PDFs and indexing chunks...")
    total_new = 0
    BATCH = 64

    batch_ids, batch_docs, batch_embeds, batch_metas = [], [], [], []

    for chunks in tqdm(list(process_all(META_FILE, CHUNK_WORDS, CHUNK_OVERLAP_WORDS))):
        new_chunks = [c for c in chunks if c["chunk_id"] not in existing_ids]
        if not new_chunks:
            continue

        texts = [c["text"] for c in new_chunks]
        embeddings = embed(texts)

        for chunk, emb in zip(new_chunks, embeddings):
            batch_ids.append(chunk["chunk_id"])
            batch_docs.append(chunk["text"])
            batch_embeds.append(emb)
            batch_metas.append({
                "source_url": chunk["source_url"],
                "title": chunk["title"],
                "year": chunk["year"] or 0,
                "authors": chunk["authors"],
                "report_type": chunk["report_type"],
                "source_agency": chunk["source_agency"],
                "chunk_index": chunk["chunk_index"],
            })

            if len(batch_ids) >= BATCH:
                collection.add(
                    ids=batch_ids,
                    documents=batch_docs,
                    embeddings=batch_embeds,
                    metadatas=batch_metas,
                )
                total_new += len(batch_ids)
                batch_ids, batch_docs, batch_embeds, batch_metas = [], [], [], []

    if batch_ids:
        collection.add(
            ids=batch_ids,
            documents=batch_docs,
            embeddings=batch_embeds,
            metadatas=batch_metas,
        )
        total_new += len(batch_ids)

    print(f"\nIngestion complete. Added {total_new} new chunks. "
          f"Total in index: {collection.count()}")


def run_full_pipeline(max_reports: int = 500):
    run_crawl(max_reports=max_reports)
    run_ingest()


if __name__ == "__main__":
    import sys
    max_r = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    run_full_pipeline(max_reports=max_r)
