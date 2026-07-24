from cooked_lol.types.item import Item

ITEM = Item(
    name="Lord Dominik's Regards",
    cost=3300,
    ad=35,
    armor_pen_pct=35.0,
    crit_chance_pct=25.0,
)

# Giant Slayer: increased damage vs champions based on their bonus HP.
GIANT_SLAYER_MAX_AMP_PCT = 15.0
GIANT_SLAYER_BONUS_HP_FOR_MAX = 1500


def giant_slayer_amp_pct(target_bonus_hp: float) -> float:
    """Damage amp %% from Giant Slayer for the given target bonus HP."""
    if target_bonus_hp <= 0:
        return 0.0
    ratio = min(target_bonus_hp / GIANT_SLAYER_BONUS_HP_FOR_MAX, 1.0)
    return GIANT_SLAYER_MAX_AMP_PCT * ratio


def apply_giant_slayer(raw_dmg: float, target_bonus_hp: float) -> float:
    """Apply Giant Slayer amp to damage dealt to an enemy champion."""
    return raw_dmg * (1 + giant_slayer_amp_pct(target_bonus_hp) / 100)
