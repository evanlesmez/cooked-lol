"""Bouncing Blade (Q)."""

from cooked_lol.systems.systems import SpellRank, reduce_cooldown, validate_rank

CAST_TIME = 0.25
TARGET_RANGE = 625
EFFECT_RADIUS = 450
SPEED = 1600
BOUNCE_TRAVEL = 0.15
MAX_BOUNCES = 2
DAGGER_LAND_DELAY = 1.023
DAGGER_LAND_OFFSET = 350
AP_RATIO = 0.40


def damage(rank: SpellRank, ap: float) -> float:
    """Magic damage per hit: 80 / 115 / 150 / 185 / 220 (+ 40% AP)."""
    validate_rank(rank)
    return 45 + 35 * rank + AP_RATIO * ap


def cooldown(rank: SpellRank, haste: int = 0) -> float:
    """Cooldown: 11 / 10 / 9 / 8 / 7, reduced by ability haste."""
    validate_rank(rank)
    return reduce_cooldown(12 - rank, haste)
