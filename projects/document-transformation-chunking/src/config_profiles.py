from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StrategyConfig:
    profile_name: str
    semantic_max_chars: int
    semantic_overlap: int
    summary_max_chars: int


DEFAULT_PROFILE = StrategyConfig(
    profile_name="default",
    semantic_max_chars=40,
    semantic_overlap=10,
    summary_max_chars=120,
)

ALTERNATE_PROFILE = StrategyConfig(
    profile_name="compact",
    semantic_max_chars=30,
    semantic_overlap=5,
    summary_max_chars=90,
)


def validate_profile(profile: StrategyConfig) -> bool:
    return (
        profile.semantic_max_chars > 0
        and profile.semantic_overlap >= 0
        and profile.summary_max_chars > 0
        and profile.semantic_overlap < profile.semantic_max_chars
    )
