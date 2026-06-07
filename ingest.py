"""
Document ingestion and chunking pipeline.

Loads all .txt files from documents/, cleans each one, splits into chunks
using paragraph boundaries with a 600-char max, 50-char overlap, and
100-char minimum, then returns chunks with source metadata attached.
"""

import re
import random
from pathlib import Path


# ---------------------------------------------------------------------------
# Stage 1: Load documents
# ---------------------------------------------------------------------------

def load_documents(directory: str) -> list[dict]:
    """
    Read every .txt file in directory.
    Extracts the SOURCE: line as metadata and keeps full raw text.
    Returns a list of dicts: {filename, source, raw_text}
    """
    docs = []
    for path in sorted(Path(directory).glob("*.txt")):
        raw = path.read_text(encoding="utf-8")
        source = ""
        for line in raw.splitlines():
            if line.startswith("SOURCE: "):
                source = line[len("SOURCE: "):].strip()
                break
        docs.append({
            "filename": path.name,
            "source": source,
            "raw_text": raw,
        })
    return docs


# ---------------------------------------------------------------------------
# Stage 2: Clean documents
# ---------------------------------------------------------------------------

def clean_document(text: str) -> str:
    """
    Remove header metadata lines, the comments separator, markdown frontmatter,
    markdown horizontal rules, and HTML entities.
    Preserves all substantive content (question body + comment text).
    """
    lines = text.splitlines()
    cleaned = []

    # Strip YAML frontmatter block: starts at the first standalone '---' line
    # and ends at the next standalone '---' line (both are discarded).
    in_frontmatter = False
    frontmatter_done = False
    for line in lines:
        stripped = line.strip()

        if stripped.startswith(("TITLE: ", "AUTHOR: ", "SOURCE: ")):
            continue
        if stripped == "--- COMMENTS ---":
            continue

        # Detect YAML frontmatter delimiters in dev.to documents
        if stripped == "---" and not frontmatter_done:
            if not in_frontmatter:
                in_frontmatter = True  # entering frontmatter
                continue
            else:
                in_frontmatter = False  # leaving frontmatter
                frontmatter_done = True
                continue

        if in_frontmatter:
            continue  # skip all lines inside frontmatter

        # Remove standalone markdown horizontal rules that survived
        if stripped == "---":
            continue

        cleaned.append(line)

    text = "\n".join(cleaned)

    # Decode HTML entities left from the original fetch
    replacements = [
        ("&amp;",  "&"),
        ("&lt;",   "<"),
        ("&gt;",   ">"),
        ("&quot;", '"'),
        ("&#x27;", "'"),
        ("&#x2F;", "/"),
        ("&nbsp;", " "),
    ]
    for entity, char in replacements:
        text = text.replace(entity, char)
    # Remove any remaining numeric or named entities
    text = re.sub(r"&#\d+;", "", text)
    text = re.sub(r"&[a-z]{2,6};", "", text)

    # Collapse runs of 3+ blank lines down to two
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ---------------------------------------------------------------------------
# Stage 3: Chunking
# ---------------------------------------------------------------------------

def _split_at_sentences(text: str, max_size: int, overlap: int) -> list[str]:
    """
    Break a single paragraph that exceeds max_size at sentence boundaries.
    Carries the last `overlap` characters of the previous sub-chunk into
    the start of the next one.
    """
    # Split on sentence-ending punctuation followed by whitespace
    sentence_re = re.compile(r'(?<=[.!?])\s+')
    sentences = [s.strip() for s in sentence_re.split(text) if s.strip()]

    chunks = []
    current = ""

    for sentence in sentences:
        candidate = (current + " " + sentence).strip() if current else sentence
        if len(candidate) <= max_size:
            current = candidate
        else:
            if current:
                chunks.append(current)
                tail = current[-overlap:] if len(current) > overlap else current
                new_start = (tail + " " + sentence).strip()
                # If tail + sentence already exceeds max, skip the tail to stay within limit
                if len(new_start) <= max_size:
                    current = new_start
                else:
                    current = sentence if len(sentence) <= max_size else sentence[:max_size]
            else:
                # Single sentence longer than max_size — keep it whole
                chunks.append(sentence)
                current = ""

    if current:
        chunks.append(current)

    return chunks


def chunk_text(
    text: str,
    max_size: int = 600,
    overlap: int = 50,
    min_size: int = 100,
) -> list[str]:
    """
    Split cleaned document text into chunks.

    Strategy:
      1. Split on double-newline paragraph boundaries.
      2. Discard paragraphs shorter than min_size (metadata remnants, etc.).
      3. Keep paragraphs at or under max_size as a single chunk.
      4. Split paragraphs over max_size at sentence boundaries with overlap.
    """
    paragraphs = text.split("\n\n")
    chunks = []

    for para in paragraphs:
        para = para.strip()
        if len(para) < min_size:
            continue
        if len(para) <= max_size:
            chunks.append(para)
        else:
            sub = _split_at_sentences(para, max_size, overlap)
            # Apply min_size filter to sub-chunks too
            chunks.extend(s for s in sub if len(s) >= min_size)

    return chunks


# ---------------------------------------------------------------------------
# Stage 4: Build the full chunk corpus with metadata
# ---------------------------------------------------------------------------

def build_chunks(directory: str = "documents") -> list[dict]:
    """
    Run the full pipeline: load → clean → chunk.
    Returns a list of dicts: {text, source, filename, chunk_index}
    """
    docs = load_documents(directory)
    all_chunks = []

    for doc in docs:
        cleaned = clean_document(doc["raw_text"])
        chunks = chunk_text(cleaned)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text":        chunk,
                "source":      doc["source"],
                "filename":    doc["filename"],
                "chunk_index": i,
            })

    return all_chunks


# ---------------------------------------------------------------------------
# Inspection helpers (run when executed directly)
# ---------------------------------------------------------------------------

def _length_stats(chunks: list[dict]) -> dict:
    lengths = [len(c["text"]) for c in chunks]
    return {
        "count": len(lengths),
        "min":   min(lengths),
        "max":   max(lengths),
        "avg":   round(sum(lengths) / len(lengths)),
    }


def main():
    print("=" * 60)
    print("STAGE 1 — Loading documents")
    print("=" * 60)
    docs = load_documents("documents")
    for d in docs:
        print(f"  {d['filename']}  ({len(d['raw_text'])} chars raw)")
    print(f"\n  Total documents: {len(docs)}\n")

    print("=" * 60)
    print("STAGE 2 — Cleaning (printing one document after cleaning)")
    print("=" * 60)
    sample_doc = next(d for d in docs if "advice_for_new_cs_student" in d["filename"])
    cleaned_sample = clean_document(sample_doc["raw_text"])
    print(cleaned_sample[:1200])
    print("  [... truncated for display ...]\n")

    print("=" * 60)
    print("STAGE 3 — Chunking all documents")
    print("=" * 60)
    chunks = build_chunks("documents")
    stats = _length_stats(chunks)
    print(f"  Total chunks : {stats['count']}")
    print(f"  Min length   : {stats['min']} chars")
    print(f"  Max length   : {stats['max']} chars")
    print(f"  Avg length   : {stats['avg']} chars\n")

    print("=" * 60)
    print("STAGE 4 — 5 representative chunks (random sample)")
    print("=" * 60)
    random.seed(42)
    sample = random.sample(chunks, min(5, len(chunks)))
    for i, c in enumerate(sample, 1):
        print(f"\n--- Chunk {i} ---")
        print(f"Source   : {c['source']}")
        print(f"File     : {c['filename']}  (chunk #{c['chunk_index']})")
        print(f"Length   : {len(c['text'])} chars")
        print(f"Text     :\n{c['text']}")

    print("\n" + "=" * 60)
    print("Chunks per document:")
    print("=" * 60)
    from collections import Counter
    per_doc = Counter(c["filename"] for c in chunks)
    for fname, count in sorted(per_doc.items()):
        print(f"  {count:3d}  {fname}")


if __name__ == "__main__":
    main()
