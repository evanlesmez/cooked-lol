from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class LichBane(metaclass=DataReadOnlyMeta):
    cost: int = 2900
    ap: int = 100
    ability_haste: int = 10
    move_speed_pct: float = 6.0
    spellblade_cd_secs: float = 1.5


def spellblade_damage(base_ad: float, ap: float) -> float:
    """Raw magic damage on a spellblade empowered onhit."""
    return 0.75 * base_ad + 0.45 * ap
