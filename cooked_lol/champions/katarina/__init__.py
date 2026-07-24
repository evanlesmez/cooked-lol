from cooked_lol.types.champion_stats import ChampionStats, Stat

from . import (
    bouncing_blade,
    death_lotus,
    preparation,
    shunpo,
    sinister_steel,
    voracity,
)

# Source: in-game stats panel (level 1-20 range).
# Manaless; abilities cost no resource.
STATS = ChampionStats(
    name="Katarina",
    melee=True,
    hp=Stat(672, 108),
    hp5=Stat(7.5, 0.7),
    ar=Stat(32, 4.7),
    mr=Stat(32, 2.05),
    ad=Stat(58, 3.2),
    bonus_as_pct=Stat(0, 2.74),
    ms=335,
    attack_range=125,
    base_as=0.658,
    windup_pct=15,
    crit_dmg_pct=200,
)

__all__ = [
    "STATS",
    "bouncing_blade",
    "death_lotus",
    "preparation",
    "shunpo",
    "sinister_steel",
    "voracity",
]
