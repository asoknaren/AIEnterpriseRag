from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PYTHON = sys.executable

projects = [
    ROOT / "projects" / "document-transformation-chunking",
    ROOT / "projects" / "fastapi-backend-vector-manager",
    ROOT / "projects" / "ingestion-storage-orchestration",
]

results: list[dict[str, object]] = []
for project in projects:
    proc = subprocess.run(
        [PYTHON, "-m", "pytest", "tests", "-q"],
        cwd=project,
        capture_output=True,
        text=True,
    )
    results.append(
        {
            "project": project.name,
            "returncode": proc.returncode,
            "stdout": proc.stdout[-4000:],
            "stderr": proc.stderr[-4000:],
        }
    )

report_path = ROOT / "wave1_m1_test_report.json"
report_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

if any(item["returncode"] != 0 for item in results):
    raise SystemExit(1)
