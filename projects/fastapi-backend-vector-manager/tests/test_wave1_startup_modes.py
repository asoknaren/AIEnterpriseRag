from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from app.main import create_app


def test_app_starts_in_all_supported_profiles(monkeypatch):
    for profile in ["postgres-only", "qdrant-only", "combined"]:
        monkeypatch.setenv("APP_PROFILE", profile)
        app = create_app()
        assert app.state.active_mode == profile
        assert len(app.state.adapters) >= 1
