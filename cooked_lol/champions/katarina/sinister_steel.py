"""Sinister Steel (P): dagger pickup slash."""

# 68–240 shown in-game for L1–18; table keeps L19–20 extrapolation.
_BASE_BY_LEVEL = (
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

BONUS_AD_RATIO = 0.60
DAGGER_GROUND_DURATION = 4.0
# Shunpo current-CD refund as fraction of total CD: 78/84/90/96% by level tier.
_SHUNPO_CDR_BY_TIER = (0.78, 0.84, 0.90, 0.96)


def _level_tier(level: int) -> int:
    if level >= 16:
        return 3
    if level >= 11:
        return 2
    if level >= 6:
        return 1
    return 0


def ap_ratio(level: int) -> float:
    """AP ratio: 70% / 80% / 90% / 100% (based on level)."""
    return 0.70 + 0.10 * _level_tier(level)


def damage(level: int, bonus_ad: float, ap: float) -> float:
    """Raw magic damage from a dagger pickup slash."""
    return _BASE_BY_LEVEL[level - 1] + BONUS_AD_RATIO * bonus_ad + ap_ratio(level) * ap


def shunpo_cdr_fraction(level: int) -> float:
    """Fraction of Shunpo's total CD refunded on dagger pickup."""
    return _SHUNPO_CDR_BY_TIER[_level_tier(level)]


def shunpo_cd_after_pickup(
    level: int, shunpo_total_cd: float, shunpo_current_cd: float
) -> float:
    """Shunpo current CD after a dagger pickup refund."""
    refund = shunpo_total_cd * shunpo_cdr_fraction(level)
    return max(0.0, shunpo_current_cd - refund)
