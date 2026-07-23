from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class RylaisCrystalScepter(metaclass=DataReadOnlyMeta):
    cost: int = 2600
    ap: int = 65
    hp: int = 400
    # Rimefrost: damaging abilities slow the target.
    slow_pct: float = 30.0
    slow_duration: float = 1.0
