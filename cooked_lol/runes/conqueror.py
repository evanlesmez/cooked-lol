# Precision keystone. Adaptive per stack; heal at max stacks vs champions.

MAX_STACKS = 12
STACK_DURATION = 5.0
# Ability/spell hits: 2 stacks, at most once per 4s per cast instance.
SPELL_STACKS = 2
SPELL_STACK_CD = 4.0
# Basic on-hit: melee 2 / ranged 1.
BASIC_ONHIT_STACKS_MELEE = 2
BASIC_ONHIT_STACKS_RANGED = 1
# Adaptive force per stack at L1 / L18 (AD is 60% of AP).
AD_PER_STACK_L1 = 1.08
AD_PER_STACK_L18 = 2.56
AP_PER_STACK_L1 = 1.8
AP_PER_STACK_L18 = 4.26
# Post-mit heal vs champions at max stacks.
HEAL_PCT_MELEE = 8.0
HEAL_PCT_RANGED = 5.0


def _scale(l1: float, l18: float, level: int) -> float:
    return l1 + (l18 - l1) / 17 * (level - 1)


def ad_per_stack(level: int) -> float:
    return _scale(AD_PER_STACK_L1, AD_PER_STACK_L18, level)


def ap_per_stack(level: int) -> float:
    return _scale(AP_PER_STACK_L1, AP_PER_STACK_L18, level)


def _validate_stacks(stacks: int) -> None:
    assert (
        0 <= stacks <= MAX_STACKS
    ), f"Conqueror stacks must be 0-{MAX_STACKS}, got {stacks}"


def bonus_ad(level: int, stacks: int) -> float:
    _validate_stacks(stacks)
    return ad_per_stack(level) * stacks


def bonus_ap(level: int, stacks: int) -> float:
    _validate_stacks(stacks)
    return ap_per_stack(level) * stacks


def basic_onhit_stacks(is_melee: bool) -> int:
    return BASIC_ONHIT_STACKS_MELEE if is_melee else BASIC_ONHIT_STACKS_RANGED


def heal(post_mit_damage: float, is_melee: bool, stacks: int = MAX_STACKS) -> float:
    _validate_stacks(stacks)
    if stacks < MAX_STACKS:
        return 0.0
    pct = HEAL_PCT_MELEE if is_melee else HEAL_PCT_RANGED
    return post_mit_damage * pct / 100
