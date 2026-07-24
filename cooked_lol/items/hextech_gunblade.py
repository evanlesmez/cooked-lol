from cooked_lol.types.item import Item

ITEM = Item(name="Hextech Gunblade", cost=3000, ad=40, ap=80, omnivamp_pct=10.0)

# Active: Lightning Bolt - single-target magic damage + slow.
# Wiki: 175 - 253 (based on level), i.e. 175 + 78/17 * (level - 1).
ACTIVE_BASE_L1 = 175.0
ACTIVE_BASE_L18 = 253.0
ACTIVE_AP_RATIO = 0.30
ACTIVE_CD = 60.0
ACTIVE_RANGE = 700
ACTIVE_SLOW_PCT = 25.0
ACTIVE_SLOW_DURATION = 1.5


def active_damage(level: int, ap: float) -> float:
    """Pre-mitigation magic damage from Lightning Bolt.

    base = 175 + 78/17 * (level - 1); the wiki table keeps extrapolating
    past level 18 (e.g. 262.18 at level 20), so no cap is applied.
    """
    per_level = (ACTIVE_BASE_L18 - ACTIVE_BASE_L1) / 17
    base = ACTIVE_BASE_L1 + per_level * (level - 1)
    return base + ACTIVE_AP_RATIO * ap
