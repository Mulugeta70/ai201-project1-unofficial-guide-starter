"""
Embedding and retrieval pipeline.

Embeds chunks produced by ingest.py using all-MiniLM-L6-v2,
stores them in a local ChromaDB collection with source metadata,
and exposes a retrieve() function for semantic search.
"""

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import build_chunks

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COLLECTION_NAME = "unofficial_guide"
CHROMA_DIR      = "chroma_db"
EMBED_MODEL     = "all-MiniLM-L6-v2"
DEFAULT_K       = 5


# ---------------------------------------------------------------------------
# Stage 1: Build the vector store
# ---------------------------------------------------------------------------

def build_vector_store(
    chunks: list[dict],
    persist_dir: str = CHROMA_DIR,
    model_name: str = EMBED_MODEL,
) -> tuple[chromadb.Collection, SentenceTransformer]:
    """
    Embed all chunks and upsert into a local ChromaDB collection.

    If the collection already exists and contains data, skips re-embedding.
    Returns (collection, model) so the caller can reuse the model for queries.
    """
    client     = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    model = SentenceTransformer(model_name)

    if collection.count() == len(chunks):
        print(f"Collection already contains {collection.count()} chunks — skipping re-embedding.")
        return collection, model

    print(f"Embedding {len(chunks)} chunks with {model_name} ...")

    ids        = [f"{c['filename']}_{c['chunk_index']}" for c in chunks]
    texts      = [c["text"] for c in chunks]
    metadatas  = [
        {
            "source":      c["source"],
            "filename":    c["filename"],
            "chunk_index": c["chunk_index"],
        }
        for c in chunks
    ]

    # Embed in one batch — all-MiniLM-L6-v2 is fast enough for 491 chunks
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_list=True)

    # Upsert so running twice doesn't create duplicates
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Stored {collection.count()} chunks in ChromaDB at '{persist_dir}/'.\n")
    return collection, model


# ---------------------------------------------------------------------------
# Stage 2: Retrieval
# ---------------------------------------------------------------------------

def retrieve(
    query: str,
    collection: chromadb.Collection,
    model: SentenceTransformer,
    k: int = DEFAULT_K,
) -> list[dict]:
    """
    Embed the query and return the top-k most similar chunks.

    Each returned dict contains:
        text        — chunk content
        source      — original URL
        filename    — source .txt file
        chunk_index — position within that document
        distance    — cosine distance (lower = more similar)
    """
    query_embedding = model.encode([query], convert_to_list=True)
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append({
            "text":        text,
            "source":      meta["source"],
            "filename":    meta["filename"],
            "chunk_index": meta["chunk_index"],
            "distance":    round(dist, 4),
        })

    return hits


# ---------------------------------------------------------------------------
# Test retrieval with evaluation-plan queries
# ---------------------------------------------------------------------------

def print_results(query: str, hits: list[dict]) -> None:
    print(f"\nQuery: {query!r}")
    print("-" * 70)
    for i, h in enumerate(hits, 1):
        print(f"  [{i}] distance={h['distance']}  |  {h['filename']} chunk#{h['chunk_index']}")
        print(f"      source: {h['source']}")
        print(f"      text  : {h['text'][:220]}")
        if len(h["text"]) > 220:
            print("             [...]")
        print()


def main():
    # Build corpus and load into ChromaDB
    chunks     = build_chunks("documents")
    collection, model = build_vector_store(chunks)

    # Three of the five evaluation-plan queries
    test_queries = [
        "What do people suggest to CS students who feel they are not smart enough to succeed?",
        "What advice do people give for surviving a difficult Operating Systems course?",
        "How do students recommend building a visible portfolio and online presence while in school?",
    ]

    print("\n" + "=" * 70)
    print("RETRIEVAL TEST — 3 evaluation queries")
    print("=" * 70)

    for query in test_queries:
        hits = retrieve(query, collection, model, k=DEFAULT_K)
        print_results(query, hits)

    # Summary: distance score health check
    print("=" * 70)
    print("Distance health check (all top-1 results across 3 queries):")
    for query in test_queries:
        hits = retrieve(query, collection, model, k=1)
        flag = "GOOD" if hits[0]["distance"] < 0.5 else "WEAK"
        print(f"  [{flag}] dist={hits[0]['distance']}  {query[:60]}")


if __name__ == "__main__":
    main()
