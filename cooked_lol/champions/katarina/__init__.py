from cooked_lol.metaclass.metaclass import DataReadOnlyMeta
from cooked_lol.systems.systems import Stat

from . import (
    bouncing_blade,
    death_lotus,
    preparation,
    shunpo,
    sinister_steel,
    voracity,
)

# Source: in-game stats panel (level 1-20 range).


class KatarinaStats(metaclass=DataReadOnlyMeta):
    hp: Stat = Stat(672, 108)
    hp5: Stat = Stat(7.5, 0.7)
    ar: Stat = Stat(32, 4.7)
    mr: Stat = Stat(32, 2.05)
    ad: Stat = Stat(58, 3.2)
    bonus_as_pct: Stat = Stat(0, 2.74)
    ms: float = 335
    attack_range: float = 125
    base_as: float = 0.658
    windup_pct: float = 15
    crit_dmg_pct: float = 200
