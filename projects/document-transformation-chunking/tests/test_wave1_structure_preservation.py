from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from preprocessing.docling_converter import DoclingConverter


def test_structural_markers_are_preserved_in_markdown_output():
    converter = DoclingConverter()
    fixture = ROOT / "tests" / "fixtures" / "wave1" / "sample.html"

    result = converter.convert_file(fixture)
    markdown = result.markdown

    assert "#" in markdown
    assert "-" in markdown
    assert "|" in markdown
