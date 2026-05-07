from dataclasses import dataclass


@dataclass(frozen=True)
class SpellslingersShoes:
    cost: int = 1100
    magic_pen_pct: float = 8
    magic_pen: int = 18
    move_speed: int = 45


SPELLSLINGERS_SHOES = SpellslingersShoes()
