from cooked_lol.types.champion_stats import ChampionStats, Stat

# Source: in-game stats panel (level 1-20 range).
# Verified: stat_at_level(s, 20) reproduces the displayed L20 values exactly.
STATS = ChampionStats(
    name="Caitlyn",
    melee=False,
    hp=Stat(580, 107),
    hp5=Stat(3.5, 0.55),
    mp=Stat(315, 40),
    mp5=Stat(7.4, 0.7),
    ar=Stat(27, 4.7),
    mr=Stat(30, 1.3),
    ad=Stat(62, 3.8),
    bonus_as_pct=Stat(0, 4),
    ms=325,
    attack_range=650,
    base_as=0.681,
    as_ratio=0.625,
    windup_pct=17.708,
    missile_speed=2500,
    crit_dmg_pct=200,
)
