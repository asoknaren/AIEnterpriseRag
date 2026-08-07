from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from preprocessing.docling_converter import DoclingConverter


def test_source_mapping_tracks_sections_and_line_positions():
    converter = DoclingConverter()
    fixture = ROOT / "tests" / "fixtures" / "wave1" / "sample.pdf"

    result = converter.convert_file(fixture)

    assert len(result.mapping) >= 3
    assert result.mapping[0].markdown_line == 1
    assert result.mapping[0].source_line == 1
    assert result.mapping[0].section_ref
