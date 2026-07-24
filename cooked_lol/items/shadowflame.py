from cooked_lol.types.item import Item

ITEM = Item(name="Shadowflame", cost=3200, ap=110, magic_pen=15)

# Cinderbloom: magic and true damage critically strike against low-HP enemies.
CINDERBLOOM_CRIT_PCT = 120
CINDERBLOOM_HP_THRESHOLD_PCT = 40


def apply_cinderbloom(raw_dmg: float, target_hp_pct: float) -> float:
    assert 0 <= target_hp_pct <= 100, f"target HP must be 0-100%, got {target_hp_pct}"
    if target_hp_pct < CINDERBLOOM_HP_THRESHOLD_PCT:
        return raw_dmg * CINDERBLOOM_CRIT_PCT / 100
    return raw_dmg
