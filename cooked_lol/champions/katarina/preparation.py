"""Preparation (W)."""

from cooked_lol.systems.systems import SpellRank, reduce_cooldown, validate_rank

DAGGER_LAND_TIME = 1.25


def bonus_ms_pct(rank: SpellRank) -> float:
    """Bonus movement speed %: 50 / 60 / 70 / 80 / 90."""
    validate_rank(rank)
    return 40 + 10 * rank


def cooldown(rank: SpellRank, haste: int = 0) -> float:
    """Cooldown: 15 / 14 / 13 / 12 / 11, reduced by ability haste."""
    validate_rank(rank)
    return reduce_cooldown(16 - rank, haste)
