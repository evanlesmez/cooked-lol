from cooked_lol.types.item import Item

ITEM = Item(
    name="Lich Bane",
    cost=2900,
    ap=100,
    ability_haste=10,
    move_speed_pct=6.0,
)

# Spellblade: next basic attack after an ability is empowered.
SPELLBLADE_CD_SECS = 1.5
SPELLBLADE_BASE_AD_RATIO = 0.75
SPELLBLADE_AP_RATIO = 0.45


def spellblade_damage(base_ad: float, ap: float) -> float:
    """Raw magic damage on a spellblade empowered onhit."""
    return SPELLBLADE_BASE_AD_RATIO * base_ad + SPELLBLADE_AP_RATIO * ap
