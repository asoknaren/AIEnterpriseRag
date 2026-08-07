from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SourceMapEntry:
    markdown_line: int
    source_line: int
    section_ref: str


def build_line_mapping(markdown_text: str) -> list[SourceMapEntry]:
    mapping: list[SourceMapEntry] = []
    current_section = "root"
    for index, line in enumerate(markdown_text.splitlines(), start=1):
        if line.startswith("#"):
            current_section = line.lstrip("# ").strip() or "root"
        mapping.append(SourceMapEntry(markdown_line=index, source_line=index, section_ref=current_section))
    return mapping
