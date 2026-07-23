from cooked_lol.systems.systems import Stat
from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


# Source: in-game stats panel (level 1-20 range).
# Verified: stat_at_level(s, 20) reproduces the displayed L20 values exactly.
class CaitlynStats(metaclass=DataReadOnlyMeta):
    hp: Stat = Stat(580, 107)
    hp5: Stat = Stat(3.5, 0.55)
    mp: Stat = Stat(315, 40)
    mp5: Stat = Stat(7.4, 0.7)
    ar: Stat = Stat(27, 4.7)
    mr: Stat = Stat(30, 1.3)
    ad: Stat = Stat(62, 3.8)
    bonus_as_pct: Stat = Stat(0, 4)
    ms: float = 325
    attack_range: float = 650
    base_as: float = 0.681
    as_ratio: float = 0.625
    windup_pct: float = 17.708
    missile_speed: float = 2500
    crit_dmg_pct: float = 200
