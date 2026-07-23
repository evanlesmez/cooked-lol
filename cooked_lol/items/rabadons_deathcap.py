from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class RabadonsDeathcap(metaclass=DataReadOnlyMeta):
    cost: int = 3500
    ap: int = 130
    passive_ap_amp: float = 0.3


def apply_magical_opus(total_ap: float) -> float:
    return total_ap * (1 + RabadonsDeathcap.passive_ap_amp)
