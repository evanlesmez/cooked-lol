from cooked_lol.types.item import Item

ITEM = Item(
    name="Kraken Slayer",
    cost=3000,
    ad=45,
    attack_speed_pct=40.0,
    move_speed_pct=4.0,
)

# Bring It Down: every 3rd on-hit deals bonus physical damage.
BRING_IT_DOWN_STACK_DURATION = 3.0
BRING_IT_DOWN_MAX_STACKS = 2
# Melee base: 150 (L1-8), then +5/level to 210 at L20. Ranged is 80%.
BRING_IT_DOWN_BASE_L1 = 150.0
BRING_IT_DOWN_BASE_L20 = 210.0
BRING_IT_DOWN_SCALE_START_LEVEL = 8
BRING_IT_DOWN_RANGED_PCT = 80.0
# +0%-75% damage amp from target missing HP (5% per 6.666...% missing).
BRING_IT_DOWN_MAX_AMP_PCT = 75.0


def bring_it_down_base(level: int, is_melee: bool = True) -> float:
    """Base Bring It Down damage before missing-HP amp."""
    per_level = (BRING_IT_DOWN_BASE_L20 - BRING_IT_DOWN_BASE_L1) / (
        20 - BRING_IT_DOWN_SCALE_START_LEVEL
    )
    steps = max(0, level - BRING_IT_DOWN_SCALE_START_LEVEL)
    melee = BRING_IT_DOWN_BASE_L1 + per_level * steps
    if is_melee:
        return melee
    return melee * BRING_IT_DOWN_RANGED_PCT / 100


def bring_it_down_damage(
    level: int,
    target_missing_hp_pct: float,
    is_melee: bool = True,
) -> float:
    """Pre-mitigation bonus physical damage from a Bring It Down proc."""
    assert (
        0 <= target_missing_hp_pct <= 100
    ), f"missing HP must be 0-100%, got {target_missing_hp_pct}"
    base = bring_it_down_base(level, is_melee)
    amp = BRING_IT_DOWN_MAX_AMP_PCT / 100 * (target_missing_hp_pct / 100)
    return base * (1 + amp)
