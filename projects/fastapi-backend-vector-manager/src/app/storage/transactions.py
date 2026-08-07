from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from app.storage.in_memory_db import InMemoryDatabase


@contextmanager
def transaction(db: InMemoryDatabase) -> Iterator[None]:
    checkpoint = db.snapshot()
    try:
        yield
    except Exception:
        db.restore(checkpoint)
        raise
