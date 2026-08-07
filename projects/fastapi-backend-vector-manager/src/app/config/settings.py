from __future__ import annotations

import os
from dataclasses import dataclass


SUPPORTED_PROFILES = {"postgres-only", "qdrant-only", "combined"}


@dataclass
class AppSettings:
    profile: str = "combined"

    @classmethod
    def from_env(cls) -> "AppSettings":
        profile = os.getenv("APP_PROFILE", "combined").strip().lower()
        if profile not in SUPPORTED_PROFILES:
            raise ValueError(f"unsupported APP_PROFILE: {profile}")
        return cls(profile=profile)
