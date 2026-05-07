from dataclasses import dataclass


@dataclass(frozen=True)
class Shadowflame:
    cost: int = 3200
    ap: int = 110
    magic_pen: int = 15
    # Cinderbloom: magic and true damage critically strike against low-HP enemies.
    passive_crit_pct: float = 120
    passive_hp_threshold_pct: float = 40


SHADOWFLAME = Shadowflame()


def apply_cinderbloom(item: Shadowflame, magic_or_true_damage: float, target_hp_pct: float) -> float:
    """If target is below the HP threshold, scale the damage instance by the crit %."""
    if target_hp_pct < item.passive_hp_threshold_pct:
        return magic_or_true_damage * item.passive_crit_pct / 100
    return magic_or_true_damage
