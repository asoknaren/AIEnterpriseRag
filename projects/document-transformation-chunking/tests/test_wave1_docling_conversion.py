from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from preprocessing.docling_converter import DoclingConverter


def test_supported_formats_convert_to_markdown():
    converter = DoclingConverter()
    fixture_dir = ROOT / "tests" / "fixtures" / "wave1"

    for name in ["sample.pdf", "sample.docx", "sample.html"]:
        result = converter.convert_file(fixture_dir / name)
        assert result.markdown.strip()
        assert len(result.mapping) >= 1
