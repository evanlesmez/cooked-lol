from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class LordDominiksRegards(metaclass=DataReadOnlyMeta):
    cost: int = 3300
    ad: int = 35
    armor_pen_pct: float = 35.0
    crit_chance_pct: float = 25.0
    # Giant Slayer: increased damage vs champions based on their bonus HP.
    giant_slayer_max_amp_pct: float = 15.0
    giant_slayer_bonus_hp_for_max: int = 1500


def giant_slayer_amp_pct(target_bonus_hp: float) -> float:
    """Damage amp %% from Giant Slayer for the given target bonus HP."""
    if target_bonus_hp <= 0:
        return 0.0
    ratio = min(
        target_bonus_hp / LordDominiksRegards.giant_slayer_bonus_hp_for_max, 1.0
    )
    return LordDominiksRegards.giant_slayer_max_amp_pct * ratio


def apply_giant_slayer(raw_dmg: float, target_bonus_hp: float) -> float:
    """Apply Giant Slayer amp to damage dealt to an enemy champion."""
    return raw_dmg * (1 + giant_slayer_amp_pct(target_bonus_hp) / 100)
