from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class HextechGunblade(metaclass=DataReadOnlyMeta):
    cost: int = 3000
    ad: int = 40
    ap: int = 80
    omnivamp_pct: float = 10.0
    # Active: Lightning Bolt - single-target magic damage + slow.
    # Wiki: 175 - 253 (based on level), i.e. 175 + 78/17 * (level - 1).
    active_base_l1: float = 175.0
    active_base_l18: float = 253.0
    active_ap_ratio: float = 0.30
    active_cd: float = 60.0
    active_range: int = 700
    active_slow_pct: float = 25.0
    active_slow_duration: float = 1.5


def active_damage(level: int, ap: float) -> float:
    """Pre-mitigation magic damage from Lightning Bolt.

    base = 175 + 78/17 * (level - 1); the wiki table keeps extrapolating
    past level 18 (e.g. 262.18 at level 20), so no cap is applied.
    """
    per_level = (HextechGunblade.active_base_l18 - HextechGunblade.active_base_l1) / 17
    base = HextechGunblade.active_base_l1 + per_level * (level - 1)
    return base + HextechGunblade.active_ap_ratio * ap
