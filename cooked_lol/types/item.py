"""Item shape: one wide const record per item module.

Fat struct, C-style: the field layout is shared by every item, and stats an
item does not grant are zero rather than missing. Cooks can therefore sum any
field across a build without probing for attributes.

Only generic stats every build aggregates belong here. Unique passive/proc
constants (Mist's Edge, Bring It Down, Giant Slayer, ...) live as module-level
constants next to the free functions that use them in the item's own module.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class Item:
    name: str
    cost: int = 0

    # Offense.
    ad: float = 0.0
    ap: float = 0.0
    attack_speed_pct: float = 0.0
    crit_chance_pct: float = 0.0
    crit_dmg_pct: float = 0.0
    ability_haste: float = 0.0
    lethality: float = 0.0
    armor_pen_pct: float = 0.0
    magic_pen: float = 0.0
    magic_pen_pct: float = 0.0

    # Defense and sustain.
    hp: float = 0.0
    hp5: float = 0.0
    mana: float = 0.0
    mp5: float = 0.0
    armor: float = 0.0
    mr: float = 0.0
    life_steal_pct: float = 0.0
    omnivamp_pct: float = 0.0
    heal_shield_power_pct: float = 0.0
    tenacity_pct: float = 0.0

    # Utility.
    move_speed: float = 0.0
    move_speed_pct: float = 0.0
