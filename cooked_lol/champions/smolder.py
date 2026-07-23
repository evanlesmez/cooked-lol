from cooked_lol.metaclass.metaclass import DataReadOnlyMeta
from cooked_lol.systems.systems import Stat

# Source: in-game stats panel (level 1-20 range).
# Verified: stat_at_level(s, 20) reproduces the displayed L20 values exactly.


class SmolderStats(metaclass=DataReadOnlyMeta):
    hp: Stat = Stat(575, 100)
    hp5: Stat = Stat(3.75, 0.6)
    ar: Stat = Stat(24, 4.0)
    mr: Stat = Stat(30, 1.3)
    mp: Stat = Stat(300, 40)
    mp5: Stat = Stat(8.5, 0.7)
    ad: Stat = Stat(58, 2.3)
    bonus_as_pct: Stat = Stat(0, 4.0)
    ms: float = 330
    attack_range: float = 550
    base_as: float = 0.638
    windup_pct: float = 16.622
    crit_dmg_pct: float = 200
    missile_speed: float = 1800
