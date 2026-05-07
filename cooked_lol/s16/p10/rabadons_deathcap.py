from dataclasses import dataclass


@dataclass(frozen=True)
class RabadonsDeathcap:
    cost: int = 3500
    ap: int = 130
    # Magical Opus: multiplicative amplifier on total AP.
    passive_ap_amp_pct: float = 30


RABADONS_DEATHCAP = RabadonsDeathcap()


def apply_magical_opus(item: RabadonsDeathcap, total_ap: float) -> float:
    """Multiply total AP (including the cap's flat AP) by the Magical Opus amplifier."""
    return total_ap * (1 + item.passive_ap_amp_pct / 100)
