from dataclasses import dataclass


@dataclass(frozen=True)
class MidlaneQuest:
    """Patch 16.10 reward: amplifies bonus AD and AP after quest completion."""
    bonus_ad_amp_pct: float = 6
    ap_amp_pct: float = 6


MIDLANE_QUEST = MidlaneQuest()


def quest_bonus_ad(item: MidlaneQuest, bonus_ad: float) -> float:
    """Post-quest bonus AD: multiplies bonus AD by (1 + amp%)."""
    return bonus_ad * (1 + item.bonus_ad_amp_pct / 100)


def quest_ap(item: MidlaneQuest, ap: float) -> float:
    """Post-quest AP: multiplies AP by (1 + amp%)."""
    return ap * (1 + item.ap_amp_pct / 100)
