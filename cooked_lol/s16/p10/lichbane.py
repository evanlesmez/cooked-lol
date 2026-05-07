from dataclasses import dataclass


@dataclass(frozen=True)
class LichBane:
    cost: int = 2900
    ap: int = 100
    mana: int = 600
    ability_haste: int = 10
    move_speed_pct: float = 5.0
    # Spellblade: next basic attack within 10s after an ability deals bonus magic damage.
    spellblade_base_ad_ratio: float = 0.75
    spellblade_ap_ratio: float = 0.50
    spellblade_cd: float = 1.5


LICHBANE = LichBane()


def spellblade_damage(item: LichBane, base_ad: float, ap: float) -> float:
    """Pre-mitigation bonus magic damage on a Spellblade-empowered basic attack."""
    return item.spellblade_base_ad_ratio * base_ad + item.spellblade_ap_ratio * ap
