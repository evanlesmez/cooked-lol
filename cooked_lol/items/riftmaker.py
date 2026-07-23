from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class Riftmaker(metaclass=DataReadOnlyMeta):
    cost: int = 3100
    ap: int = 70
    ability_haste: int = 15
    hp: int = 350
    # Void Corruption: each second in combat with champions adds a damage
    # amp stack; at max stacks, gain omnivamp.
    corruption_pct_per_stack: float = 2.0
    corruption_max_stacks: int = 4
    corruption_omnivamp_pct_melee: float = 10.0
    corruption_omnivamp_pct_ranged: float = 6.0
    # Void Infusion: gain AP equal to a percentage of bonus health.
    infusion_ap_pct_bonus_hp: float = 2.0


def void_corruption_amp_pct(seconds_in_combat: int) -> float:
    """Damage amp %% from Void Corruption after the given seconds in combat."""
    stacks = min(max(seconds_in_combat, 0), Riftmaker.corruption_max_stacks)
    return Riftmaker.corruption_pct_per_stack * stacks


def void_infusion_ap(bonus_hp: float) -> float:
    """Bonus AP granted by Void Infusion from bonus health."""
    return bonus_hp * Riftmaker.infusion_ap_pct_bonus_hp / 100
