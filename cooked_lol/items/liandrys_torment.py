from cooked_lol.types.item import Item

ITEM = Item(name="Liandry's Torment", cost=3000, ap=60, hp=300)

# Torment: ability damage applies a burn that ticks max-HP% magic damage.
BURN_PCT_PER_TICK = 1.0
BURN_TICK_INTERVAL = 0.5
BURN_DURATION = 3.0
BURN_MONSTER_TICK_CAP = 20


def burn_damage(target_max_hp: float, is_monster: bool = False) -> float:
    """Total Torment burn over full duration (pre-mitigation magic damage)."""
    ticks = int(BURN_DURATION / BURN_TICK_INTERVAL)
    per_tick = target_max_hp * BURN_PCT_PER_TICK / 100
    if is_monster:
        per_tick = min(per_tick, BURN_MONSTER_TICK_CAP)
    return per_tick * ticks
