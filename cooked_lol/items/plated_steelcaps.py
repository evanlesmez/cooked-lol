from cooked_lol.types.item import Item

ITEM = Item(name="Plated Steelcaps", cost=1200, armor=25, move_speed=45)

# Plating: reduces incoming basic damage (not turrets).
PLATING_BASIC_DMG_REDUCTION_PCT = 10.0


def apply_plating(raw_basic_dmg: float) -> float:
    """Incoming basic damage after Plating reduction."""
    return raw_basic_dmg * (1 - PLATING_BASIC_DMG_REDUCTION_PCT / 100)
