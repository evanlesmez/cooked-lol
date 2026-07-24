from cooked_lol.types.item import Item

ITEM = Item(name="Terminus", cost=3000, ad=30, attack_speed_pct=35.0)

# Shadow: flat on-hit magic damage.
SHADOW_ONHIT_MAGIC = 30

# Juxtaposition: alternate Light/Dark stacks on champion on-hits.
JUXTAPOSITION_STACK_DURATION = 5.0
JUXTAPOSITION_MAX_STACKS = 3

# Light: bonus armor and MR per stack (6/7/8 at L1-7 / 8-12 / 13+).
LIGHT_RESIST_L1 = 6
LIGHT_RESIST_L8 = 7
LIGHT_RESIST_L13 = 8

# Dark: % armor pen and magic pen per stack.
DARK_PEN_PCT_PER_STACK = 10.0


def light_resist_per_stack(level: int) -> int:
    """Bonus armor and MR granted per Light stack at the given level."""
    if level >= 13:
        return LIGHT_RESIST_L13
    if level >= 8:
        return LIGHT_RESIST_L8
    return LIGHT_RESIST_L1


def _validate_stacks(stacks: int) -> None:
    assert (
        0 <= stacks <= JUXTAPOSITION_MAX_STACKS
    ), f"Juxtaposition stacks must be 0-{JUXTAPOSITION_MAX_STACKS}, got {stacks}"


def light_resist_total(level: int, stacks: int) -> int:
    """Total bonus armor/MR from Light stacks."""
    _validate_stacks(stacks)
    return light_resist_per_stack(level) * stacks


def dark_pen_pct(stacks: int) -> float:
    """Armor pen and magic pen %% from Dark stacks."""
    _validate_stacks(stacks)
    return DARK_PEN_PCT_PER_STACK * stacks
