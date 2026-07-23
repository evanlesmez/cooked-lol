from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class Shadowflame(metaclass=DataReadOnlyMeta):
    cost: int = 3200
    ap: int = 110
    magic_pen: int = 15
    # Cinderbloom: magic and true damage critically strike against low-HP enemies.
    passive_crit_pct: float = 120
    passive_hp_threshold_pct: float = 40


def apply_cinderbloom(raw_dmg: float, target_hp_pct: float) -> float:
    if target_hp_pct < Shadowflame.passive_hp_threshold_pct:
        return raw_dmg * Shadowflame.passive_crit_pct / 100
    return raw_dmg
