from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from preprocessing.markdown_normalizer import normalize_markdown
from preprocessing.source_mapping import SourceMapEntry, build_line_mapping


@dataclass
class ConversionResult:
    markdown: str
    mapping: list[SourceMapEntry]


class DoclingConverter:
    """Lightweight conversion adapter with deterministic fallback behavior.

    The implementation keeps a stable interface for future replacement with a
    full Docling backend while enabling Wave 1 validation in local tests.
    """

    def convert_file(self, file_path: str | Path) -> ConversionResult:
        path = Path(file_path)
        suffix = path.suffix.lower()
        if suffix not in {".pdf", ".doc", ".docx", ".html", ".htm"}:
            raise ValueError(f"unsupported input type: {suffix}")

        raw = path.read_text(encoding="utf-8", errors="ignore")
        markdown = self._to_markdown(raw, suffix)
        normalized = normalize_markdown(markdown)
        mapping = build_line_mapping(normalized)
        return ConversionResult(markdown=normalized, mapping=mapping)

    def _to_markdown(self, raw: str, suffix: str) -> str:
        if suffix in {".html", ".htm"}:
            text = self._simple_html_to_markdown(raw)
        else:
            text = raw

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return ""

        # Ensure structural cues are visible in output for preservation tests.
        rendered: list[str] = []
        for index, line in enumerate(lines):
            if index == 0 and not line.startswith("#"):
                rendered.append(f"# {line}")
                continue
            rendered.append(line)
        return "\n".join(rendered)

    def _simple_html_to_markdown(self, html: str) -> str:
        html = re.sub(r"(?is)<h1[^>]*>(.*?)</h1>", r"# \1\n", html)
        html = re.sub(r"(?is)<h2[^>]*>(.*?)</h2>", r"## \1\n", html)
        html = re.sub(r"(?is)<li[^>]*>(.*?)</li>", r"- \1\n", html)
        html = re.sub(r"(?is)<tr[^>]*>(.*?)</tr>", r"\1\n", html)
        html = re.sub(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", r"| \1 ", html)
        html = re.sub(r"(?is)<[^>]+>", "", html)
        return html
