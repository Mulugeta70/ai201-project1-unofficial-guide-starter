"""
End-to-end RAG query pipeline.

ask(question) -> {answer, sources, chunks}
  1. Retrieve the top-5 most similar chunks from ChromaDB.
  2. Format them as numbered context blocks with source URLs.
  3. Call Groq (llama-3.3-70b-versatile) with a strict grounding prompt.
  4. Return the answer plus the list of source URLs.
"""

import os
from dotenv import load_dotenv
from groq import Groq

from ingest import build_chunks
from retrieve import build_vector_store, retrieve, DEFAULT_K

load_dotenv()

# ---------------------------------------------------------------------------
# Module-level singletons — initialised once on first call to ask()
# ---------------------------------------------------------------------------

_collection = None
_model      = None
_groq       = None


def _init():
    global _collection, _model, _groq
    if _collection is None:
        chunks      = build_chunks("documents")
        _collection, _model = build_vector_store(chunks)
        _groq       = Groq(api_key=os.environ["GROQ_API_KEY"])


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are an assistant that answers questions about computer science student experiences \
using only the documents provided to you.

Rules you must follow without exception:
1. Answer using ONLY the information that appears in the numbered context blocks below.
2. Do not use any knowledge from your training data.
3. For every claim you make, cite the source number in square brackets, e.g. [1] or [2].
4. If the provided context does not contain enough information to answer the question, \
respond with exactly this sentence and nothing else:
   "I don't have enough information on that in my documents."
5. Do not speculate, infer, or fill gaps with outside knowledge."""


def _build_user_message(question: str, chunks: list[dict]) -> str:
    context_blocks = []
    for i, chunk in enumerate(chunks, 1):
        context_blocks.append(
            f"[{i}] Source: {chunk['source']}\n"
            f"{chunk['text']}"
        )
    context = "\n\n".join(context_blocks)
    return (
        f"Context:\n\n{context}\n\n"
        f"Question: {question}"
    )


# ---------------------------------------------------------------------------
# Main ask function
# ---------------------------------------------------------------------------

def ask(question: str, k: int = DEFAULT_K) -> dict:
    """
    Run the full RAG pipeline for a question.

    Returns:
        answer  — LLM response grounded in retrieved chunks
        sources — deduplicated list of source URLs that were retrieved
        chunks  — the raw retrieved chunks (text + metadata + distance)
    """
    _init()

    hits = retrieve(question, _collection, _model, k=k)

    user_message = _build_user_message(question, hits)

    response = _groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        temperature=0.2,
        max_tokens=1024,
    )

    answer = response.choices[0].message.content.strip()

    # Deduplicate sources while preserving the retrieval order
    seen    = set()
    sources = []
    for h in hits:
        if h["source"] not in seen:
            seen.add(h["source"])
            sources.append(h["source"])

    return {
        "answer":  answer,
        "sources": sources,
        "chunks":  hits,
    }


# ---------------------------------------------------------------------------
# CLI smoke test (run directly to verify end-to-end before the UI)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_questions = [
        # Evaluation-plan questions
        "What do people suggest to CS students who feel they are not smart enough to succeed?",
        "What advice do people give for surviving a difficult Operating Systems course?",
        # Out-of-domain question — system must decline
        "What is the capital of France?",
    ]

    for q in test_questions:
        print("\n" + "=" * 70)
        print(f"Q: {q}")
        print("=" * 70)
        result = ask(q)
        print(f"A: {result['answer']}")
        print("\nSources retrieved:")
        for s in result["sources"]:
            print(f"  {s}")
