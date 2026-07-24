from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class PlatedSteelcaps(metaclass=DataReadOnlyMeta):
    cost: int = 1200
    armor: int = 25
    move_speed: int = 45
    # Plating: reduces incoming basic damage (not turrets).
    plating_basic_dmg_reduction_pct: float = 10.0


def apply_plating(raw_basic_dmg: float) -> float:
    """Incoming basic damage after Plating reduction."""
    return raw_basic_dmg * (1 - PlatedSteelcaps.plating_basic_dmg_reduction_pct / 100)
