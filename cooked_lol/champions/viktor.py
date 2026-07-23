from cooked_lol.systems.systems import Stat
from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


# Source: in-game stats panel (level 1-20 range).
# Verified: stat_at_level(s, 20) reproduces the displayed L20 values exactly.
class ViktorStats(metaclass=DataReadOnlyMeta):
    hp: Stat = Stat(600, 100)
    hp5: Stat = Stat(8, 0.65)
    mp: Stat = Stat(405, 45)
    mp5: Stat = Stat(8, 0.8)
    ar: Stat = Stat(23, 4.4)
    mr: Stat = Stat(30, 1.3)
    ad: Stat = Stat(53, 3)
    bonus_as_pct: Stat = Stat(0, 2.11)
    ms: float = 335
    attack_range: float = 525
    base_as: float = 0.658
    windup_pct: float = 18
    missile_speed: float = 2300
    crit_dmg_pct: float = 200
