from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class MidlaneQuest(metaclass=DataReadOnlyMeta):
    """Patch 16.11 reward: amplifies bonus AD and AP after quest completion."""

    bonus_ad_amp: float = 0.08
    ap_amp: float = 0.08


def quest_bonus_ad(bonus_ad: float) -> float:
    return bonus_ad * (1 + MidlaneQuest.bonus_ad_amp)


def quest_ap(ap: float) -> float:
    return ap * (1 + MidlaneQuest.ap_amp)
