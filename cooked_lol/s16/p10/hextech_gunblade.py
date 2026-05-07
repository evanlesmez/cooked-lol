from dataclasses import dataclass


@dataclass(frozen=True)
class HextechGunblade:
    cost: int = 3000
    ad: int = 40
    ap: int = 80
    omnivamp_pct: float = 10.0
    # Active: Lightning Bolt - single-target magic damage + slow.
    active_base_l1: float = 175.0
    active_base_l20: float = 262.18
    active_ap_ratio: float = 0.30
    active_cd: float = 60.0
    active_range: int = 700
    active_slow_pct: float = 25.0
    active_slow_duration: float = 1.5


HEXTECH_GUNBLADE = HextechGunblade()


def active_damage(item: HextechGunblade, level: int, ap: float) -> float:
    """Pre-mitigation magic damage from Lightning Bolt. Linear L1->L20 scaling."""
    base = item.active_base_l1 + (item.active_base_l20 - item.active_base_l1) * (level - 1) / 19
    return base + item.active_ap_ratio * ap
