from cooked_lol.systems.systems import SpellRank, Stat, validate_rank
from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


# Source: in-game stats panel (level 1-20 range).
# Verified: stat_at_level(s, 20) reproduces the displayed L20 values exactly.
class KatarinaStats(metaclass=DataReadOnlyMeta):
    hp: Stat = Stat(672, 108)
    hp5: Stat = Stat(7.5, 0.7)
    ar: Stat = Stat(32, 4.7)
    mr: Stat = Stat(32, 2.05)
    ad: Stat = Stat(58, 3.2)
    bonus_as_pct: Stat = Stat(0, 2.74)
    ms: float = 335
    attack_range: float = 125
    base_as: float = 0.658
    windup_pct: float = 15
    crit_dmg_pct: float = 200


_DAGGER_BASE_BY_LEVEL = (
    68,
    72,
    77,
    82,
    89,
    96,
    103,
    112,
    121,
    131,
    142,
    154,
    166,
    180,
    194,
    208,
    224,
    240,
    257,
    275,
)


def dagger_damage(level: int, bonus_ad: float, ap: float) -> float:
    """
    Raw damage from a single dagger pickup (Sinister Steel).
    """
    base = _DAGGER_BASE_BY_LEVEL[level - 1]

    if level >= 16:
        ap_ratio = 1.00
    elif level >= 11:
        ap_ratio = 0.90
    elif level >= 6:
        ap_ratio = 0.80
    else:
        ap_ratio = 0.70

    return base + 0.60 * bonus_ad + ap_ratio * ap


def bouncing_blade(rank: SpellRank, ap: float) -> float:
    validate_rank(rank)
    return 45 + 35 * rank + 0.4 * ap


def shunpo(rank: SpellRank, bonus_ad: float, ap: float) -> float:
    validate_rank(rank)
    return 10 + (10 * rank) + 0.4 * bonus_ad + 0.25 * ap
