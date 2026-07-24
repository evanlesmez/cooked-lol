from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class BladeOfTheRuinedKing(metaclass=DataReadOnlyMeta):
    cost: int = 3200
    ad: int = 40
    attack_speed_pct: float = 25.0
    life_steal_pct: float = 10.0
    # Mist's Edge: on-hit bonus physical damage = % of target's current HP.
    mists_edge_current_hp_pct_melee: float = 9.0
    mists_edge_current_hp_pct_ranged: float = 6.0
    mists_edge_minion_monster_cap: int = 100
    # Clawing Shadows: 3rd stack on-hit slows the target (champion only).
    clawing_shadows_stack_duration: float = 6.0
    clawing_shadows_max_stacks: int = 3
    clawing_shadows_slow_pct: float = 30.0
    clawing_shadows_slow_duration: float = 1.0
    clawing_shadows_cd: float = 15.0


def mists_edge_damage(
    target_current_hp: float,
    is_melee: bool,
    is_minion_or_monster: bool = False,
) -> float:
    """Pre-mitigation on-hit physical damage from Mist's Edge."""
    pct = (
        BladeOfTheRuinedKing.mists_edge_current_hp_pct_melee
        if is_melee
        else BladeOfTheRuinedKing.mists_edge_current_hp_pct_ranged
    )
    dmg = target_current_hp * pct / 100
    if is_minion_or_monster:
        dmg = min(dmg, BladeOfTheRuinedKing.mists_edge_minion_monster_cap)
    return dmg
