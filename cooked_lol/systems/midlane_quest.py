"""Patch 16.11 midlane reward: amplifies bonus AD and AP after quest completion."""

BONUS_AD_AMP = 0.08
AP_AMP = 0.08


def quest_bonus_ad(bonus_ad: float) -> float:
    return bonus_ad * (1 + BONUS_AD_AMP)


def quest_ap(ap: float) -> float:
    return ap * (1 + AP_AMP)
