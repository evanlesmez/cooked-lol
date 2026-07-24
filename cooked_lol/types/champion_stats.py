"""Champion base stat shape: one const record per champion module.

Level-scaled stats are `Stat(base, growth)` and resolve through
`systems.systems.stat_at_level`. Flat stats are plain floats.

Zeros mean "does not apply": manaless champions carry `Stat(0, 0)` mana, and
melee champions carry `missile_speed = 0`.
"""

from dataclasses import dataclass
from typing import NamedTuple


class Stat(NamedTuple):
    base: float
    growth: float


ZERO = Stat(0.0, 0.0)


@dataclass(frozen=True, slots=True, kw_only=True)
class ChampionStats:
    name: str
    melee: bool

    # Level-scaled.
    hp: Stat = ZERO
    hp5: Stat = ZERO
    mp: Stat = ZERO
    mp5: Stat = ZERO
    ar: Stat = ZERO
    mr: Stat = ZERO
    ad: Stat = ZERO
    bonus_as_pct: Stat = ZERO

    # Flat.
    ms: float = 0.0
    attack_range: float = 0.0
    base_as: float = 0.0
    # 0 means the ratio equals base_as, which is the case for most champions.
    as_ratio: float = 0.0
    windup_pct: float = 0.0
    # 0 means no missile (melee basic attack).
    missile_speed: float = 0.0
    crit_dmg_pct: float = 200.0


def attack_speed_ratio(stats: ChampionStats) -> float:
    """Attack speed ratio, defaulting to base attack speed when unspecified."""
    return stats.as_ratio or stats.base_as
