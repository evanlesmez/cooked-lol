from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class VoidStaff(metaclass=DataReadOnlyMeta):
    cost: int = 3000
    ap: int = 95
    magic_pen_pct: float = 40
