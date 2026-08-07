def chunk_text_semantically(text: str, max_chars: int = 40, overlap: int = 10) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(len(words), start + max(1, max_chars // 5))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end >= len(words):
            break
        start = max(0, end - overlap)
    return chunks


def build_contextual_chunks(chunks: list[str], headers: list[str] | None = None) -> list[dict[str, str]]:
    headers = headers or [f"Header {index}" for index in range(len(chunks))]
    contextual = []
    for index, chunk in enumerate(chunks):
        contextual.append(
            {
                "chunk": chunk,
                "header": headers[index],
                "context": f"context around {chunk}",
            }
        )
    return contextual


def build_summary_artifacts(chunks: list[str], max_chars: int = 30) -> list[dict[str, str]]:
    summaries = []
    for chunk in chunks:
        summary = chunk[:max_chars]
        summaries.append({"chunk": chunk, "summary": summary})
    return summaries
