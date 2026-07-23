from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class SpellslingersShoes(metaclass=DataReadOnlyMeta):
    cost: int = 1100
    magic_pen_pct: float = 8
    magic_pen: int = 18
    move_speed: int = 45
