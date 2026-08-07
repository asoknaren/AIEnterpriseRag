from __future__ import annotations


def select_adapters(profile: str) -> list[str]:
    mapping = {
        "postgres-only": ["postgres"],
        "qdrant-only": ["qdrant"],
        "combined": ["postgres", "qdrant"],
    }
    if profile not in mapping:
        raise ValueError(f"unknown profile: {profile}")
    return mapping[profile]
