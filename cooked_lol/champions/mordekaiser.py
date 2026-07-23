from cooked_lol.systems.systems import Stat
from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


# Source: in-game stats panel (level 1-20 range).
# Verified: stat_at_level(s, 20) reproduces the displayed L20 values exactly.
# Manaless; secondary bar is Shield (Indestructible).
class MordekaiserStats(metaclass=DataReadOnlyMeta):
    hp: Stat = Stat(645, 104)
    hp5: Stat = Stat(5, 0.75)
    ar: Stat = Stat(37, 4.2)
    mr: Stat = Stat(32, 2.05)
    ad: Stat = Stat(61, 4)
    bonus_as_pct: Stat = Stat(0, 1)
    ms: float = 335
    attack_range: float = 175
    base_as: float = 0.625
    windup_pct: float = 21.133
    crit_dmg_pct: float = 200
