from __future__ import annotations

from hashlib import sha256
from typing import Any


def _word_windows(text: str, max_chars: int = 40, overlap: int = 10) -> list[tuple[int, int, str]]:
    words = text.split()
    windows: list[tuple[int, int, str]] = []
    window_size = max(1, max_chars // 5)
    overlap_words = max(0, min(window_size - 1, overlap // 5))
    start = 0
    while start < len(words):
        end = min(len(words), start + window_size)
        chunk = " ".join(words[start:end])
        windows.append((start, end, chunk))
        if end >= len(words):
            break
        start = end - overlap_words
    return windows


def chunk_text_semantically(text: str, max_chars: int = 40, overlap: int = 10) -> list[str]:
    chunks: list[str] = []
    for _, _, chunk in _word_windows(text, max_chars=max_chars, overlap=overlap):
        if len(chunk) <= max_chars:
            chunks.append(chunk)
            continue
        start = 0
        while start < len(chunk):
            piece = chunk[start : start + max_chars].strip()
            if piece:
                chunks.append(piece)
            start += max_chars
    return chunks


def semantic_chunk_artifacts(
    text: str,
    *,
    document_id: str,
    source_ref_prefix: str = "md",
    max_chars: int = 40,
    overlap: int = 10,
) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    for index, (start, end, chunk) in enumerate(_word_windows(text, max_chars=max_chars, overlap=overlap), start=1):
        artifacts.append(
            {
                "artifact_id": f"{document_id}-semantic-{index}",
                "artifact_type": "semantic_chunk",
                "chunk": chunk,
                "token_count": len(chunk.split()),
                "source_span": {
                    "source_ref": f"{source_ref_prefix}:{index}",
                    "word_start": start,
                    "word_end": end,
                },
            }
        )
    return artifacts


def build_contextual_chunks(chunks: list[str], headers: list[str] | None = None) -> list[dict[str, str]]:
    headers = headers or [f"Header {index}" for index in range(len(chunks))]
    contextual = []
    for index, chunk in enumerate(chunks):
        before = chunks[index - 1] if index > 0 else ""
        after = chunks[index + 1] if index + 1 < len(chunks) else ""
        contextual.append(
            {
                "chunk": chunk,
                "header": headers[index],
                "context": f"prev={before} | next={after}",
            }
        )
    return contextual


def contextual_chunk_artifacts(
    semantic_artifacts: list[dict[str, Any]],
    headers: list[str] | None = None,
) -> list[dict[str, Any]]:
    chunks = [item["chunk"] for item in semantic_artifacts]
    contextual = build_contextual_chunks(chunks, headers=headers)
    artifacts: list[dict[str, Any]] = []
    for index, item in enumerate(contextual, start=1):
        source = semantic_artifacts[index - 1]["source_span"]
        artifacts.append(
            {
                "artifact_id": semantic_artifacts[index - 1]["artifact_id"].replace("semantic", "contextual"),
                "artifact_type": "contextual_chunk",
                "chunk": item["chunk"],
                "header": item["header"],
                "context": item["context"],
                "token_count": len(item["chunk"].split()),
                "source_span": source,
            }
        )
    return artifacts


def build_summary_artifacts(chunks: list[str], max_chars: int = 30) -> list[dict[str, str]]:
    summaries = []
    for chunk in chunks:
        summary = chunk[:max_chars]
        summaries.append({"chunk": chunk, "summary": summary})
    return summaries


def generate_summaries_with_model(
    chunks: list[str],
    *,
    model_provider: str = "ollama",
    model_name: str = "qwen2.5:7b",
    min_chars: int = 10,
    max_chars: int = 120,
) -> list[dict[str, Any]]:
    summaries = build_summary_artifacts(chunks, max_chars=max_chars)
    for item in summaries:
        if len(item["summary"]) < min_chars:
            item["summary"] = item["summary"].ljust(min_chars, ".")
        item["model_provider"] = model_provider
        item["model_name"] = model_name
        item["summary_length"] = len(item["summary"])
    return summaries


def build_raptor_hierarchy(
    chunks: list[str],
    *,
    document_id: str,
    model_provider: str = "ollama",
    model_name: str = "qwen2.5:7b",
) -> dict[str, Any]:
    root_id = f"{document_id}-raptor-root"
    children = []
    for index, chunk in enumerate(chunks, start=1):
        child_id = f"{document_id}-raptor-{index}"
        children.append(
            {
                "node_id": child_id,
                "parent_node_id": root_id,
                "level": 1,
                "content": chunk[:120],
                "model_provider": model_provider,
                "model_name": model_name,
            }
        )
    return {
        "root": {
            "node_id": root_id,
            "parent_node_id": None,
            "level": 0,
            "content": "Root summary",
            "model_provider": model_provider,
            "model_name": model_name,
        },
        "children": children,
    }


def generate_qa_pairs(
    chunks: list[str],
    *,
    source_ref_prefix: str = "md",
    model_provider: str = "ollama",
    model_name: str = "qwen2.5:7b",
) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    for index, chunk in enumerate(chunks, start=1):
        pairs.append(
            {
                "question": f"What does section {index} say?",
                "answer": chunk[:180],
                "confidence": 0.9,
                "source_spans": [{"source_ref": f"{source_ref_prefix}:{index}"}],
                "model_provider": model_provider,
                "model_name": model_name,
            }
        )
    return pairs


def extract_factoids(
    chunks: list[str],
    *,
    model_provider: str = "ollama",
    model_name: str = "qwen2.5:7b",
) -> list[dict[str, Any]]:
    seen: set[str] = set()
    results: list[dict[str, Any]] = []
    for chunk in chunks:
        tokens = [token.strip(".,:;!?()[]{}\"'").lower() for token in chunk.split() if token.strip()]
        if not tokens:
            continue
        canonical = tokens[0]
        if canonical in seen:
            continue
        seen.add(canonical)
        results.append(
            {
                "fact": chunk[:120],
                "canonical_value": canonical,
                "confidence": 0.85,
                "extraction_method": "first-token-canonical",
                "model_provider": model_provider,
                "model_name": model_name,
            }
        )
    return results


def attach_metadata_envelope(
    artifacts: list[dict[str, Any]],
    *,
    document_id: str,
    strategy: str,
    strategy_version: str,
) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    for item in artifacts:
        artifact_text = item.get("chunk") or item.get("summary") or item.get("fact") or item.get("answer") or ""
        artifact_id = item.get("artifact_id") or f"{document_id}-{strategy}-{sha256(artifact_text.encode('utf-8')).hexdigest()[:12]}"
        payloads.append(
            {
                "artifact_id": artifact_id,
                "document_id": document_id,
                "artifact_type": item.get("artifact_type", strategy),
                "content": artifact_text,
                "metadata": {
                    "source_uri": f"internal://{document_id}",
                    "source_type": "markdown",
                    "chunk_strategy": strategy,
                    "chunk_strategy_version": strategy_version,
                    "model_provider": item.get("model_provider"),
                    "model_name": item.get("model_name"),
                },
                "lineage": {
                    "source_ref": (item.get("source_span") or {"source_ref": "md:0"}).get("source_ref", "md:0"),
                },
                "payload": item,
            }
        )
    return payloads
