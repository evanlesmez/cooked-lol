from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class Terminus(metaclass=DataReadOnlyMeta):
    cost: int = 3000
    ad: int = 30
    attack_speed_pct: float = 35.0
    # Shadow: flat on-hit magic damage.
    shadow_onhit_magic: int = 30
    # Juxtaposition: alternate Light/Dark stacks on champion on-hits.
    juxtaposition_stack_duration: float = 5.0
    juxtaposition_max_stacks: int = 3
    # Light: bonus armor and MR per stack (6/7/8 at L1-7 / 8-12 / 13+).
    light_resist_l1: int = 6
    light_resist_l8: int = 7
    light_resist_l13: int = 8
    # Dark: % armor pen and magic pen per stack.
    dark_pen_pct_per_stack: float = 10.0


def light_resist_per_stack(level: int) -> int:
    """Bonus armor and MR granted per Light stack at the given level."""
    if level >= 13:
        return Terminus.light_resist_l13
    if level >= 8:
        return Terminus.light_resist_l8
    return Terminus.light_resist_l1


def light_resist_total(level: int, stacks: int) -> int:
    """Total bonus armor/MR from Light stacks."""
    stacks = max(0, min(stacks, Terminus.juxtaposition_max_stacks))
    return light_resist_per_stack(level) * stacks


def dark_pen_pct(stacks: int) -> float:
    """Armor pen and magic pen %% from Dark stacks."""
    stacks = max(0, min(stacks, Terminus.juxtaposition_max_stacks))
    return Terminus.dark_pen_pct_per_stack * stacks
