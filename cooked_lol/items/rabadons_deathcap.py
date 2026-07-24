from cooked_lol.types.item import Item

ITEM = Item(name="Rabadon's Deathcap", cost=3500, ap=130)

# Magical Opus: amplifies total AP.
MAGICAL_OPUS_AP_AMP = 0.3


def apply_magical_opus(total_ap: float) -> float:
    return total_ap * (1 + MAGICAL_OPUS_AP_AMP)
