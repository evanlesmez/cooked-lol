from cooked_lol.types.item import Item

ITEM = Item(
    name="Blade of the Ruined King",
    cost=3200,
    ad=40,
    attack_speed_pct=25.0,
    life_steal_pct=10.0,
)

# Mist's Edge: on-hit bonus physical damage = % of target's current HP.
MISTS_EDGE_CURRENT_HP_PCT_MELEE = 9.0
MISTS_EDGE_CURRENT_HP_PCT_RANGED = 6.0
MISTS_EDGE_MINION_MONSTER_CAP = 100

# Clawing Shadows: 3rd stack on-hit slows the target (champion only).
CLAWING_SHADOWS_STACK_DURATION = 6.0
CLAWING_SHADOWS_MAX_STACKS = 3
CLAWING_SHADOWS_SLOW_PCT = 30.0
CLAWING_SHADOWS_SLOW_DURATION = 1.0
CLAWING_SHADOWS_CD = 15.0


def mists_edge_damage(
    target_current_hp: float,
    is_melee: bool,
    is_minion_or_monster: bool = False,
) -> float:
    """Pre-mitigation on-hit physical damage from Mist's Edge."""
    pct = (
        MISTS_EDGE_CURRENT_HP_PCT_MELEE
        if is_melee
        else MISTS_EDGE_CURRENT_HP_PCT_RANGED
    )
    dmg = target_current_hp * pct / 100
    if is_minion_or_monster:
        dmg = min(dmg, MISTS_EDGE_MINION_MONSTER_CAP)
    return dmg
