from cooked_lol.types.item import Item

ITEM = Item(name="Riftmaker", cost=3100, ap=70, hp=350, ability_haste=15)

# Void Corruption: each second in combat with champions adds a damage
# amp stack; at max stacks, gain omnivamp.
CORRUPTION_PCT_PER_STACK = 2.0
CORRUPTION_MAX_STACKS = 4
CORRUPTION_OMNIVAMP_PCT_MELEE = 10.0
CORRUPTION_OMNIVAMP_PCT_RANGED = 6.0

# Void Infusion: gain AP equal to a percentage of bonus health.
INFUSION_AP_PCT_BONUS_HP = 2.0


def void_corruption_amp_pct(seconds_in_combat: int) -> float:
    """Damage amp %% from Void Corruption after the given seconds in combat."""
    assert (
        seconds_in_combat >= 0
    ), f"seconds in combat cannot be negative, got {seconds_in_combat}"
    # Stacks legitimately cap out once combat runs past the max; not a caller bug.
    stacks = min(seconds_in_combat, CORRUPTION_MAX_STACKS)
    return CORRUPTION_PCT_PER_STACK * stacks


def void_infusion_ap(bonus_hp: float) -> float:
    """Bonus AP granted by Void Infusion from bonus health."""
    return bonus_hp * INFUSION_AP_PCT_BONUS_HP / 100
