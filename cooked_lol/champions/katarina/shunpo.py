"""Shunpo (E)."""

from cooked_lol.systems.systems import SpellRank, reduce_cooldown, validate_rank

CAST_TIME = 0.15
AD_RATIO = 0.40
AP_RATIO = 0.25


def damage(rank: SpellRank, bonus_ad: float, ap: float) -> float:
    """Magic damage: 20 / 30 / 40 / 50 / 60 (+ 40% bonus AD) (+ 25% AP)."""
    validate_rank(rank)
    return 10 + 10 * rank + AD_RATIO * bonus_ad + AP_RATIO * ap


def cooldown(rank: SpellRank, haste: int = 0) -> float:
    """Cooldown: 12 / 11 / 10 / 9 / 8, reduced by ability haste."""
    validate_rank(rank)
    return reduce_cooldown(13 - rank, haste)
