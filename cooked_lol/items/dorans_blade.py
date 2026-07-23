from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class DoransBlade(metaclass=DataReadOnlyMeta):
    ad: int = 10
    hp: int = 80
    omnivamp_pct: float = 2.5
