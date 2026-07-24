from cooked_lol.types.champion_stats import ChampionStats, Stat

# Source: in-game stats panel (level 1-20 range).
# Verified: stat_at_level(s, 20) reproduces the displayed L20 values exactly.
STATS = ChampionStats(
    name="Smolder",
    melee=False,
    hp=Stat(575, 100),
    hp5=Stat(3.75, 0.6),
    mp=Stat(300, 40),
    mp5=Stat(8.5, 0.7),
    ar=Stat(24, 4.0),
    mr=Stat(30, 1.3),
    ad=Stat(58, 2.3),
    bonus_as_pct=Stat(0, 4.0),
    ms=330,
    attack_range=550,
    base_as=0.638,
    windup_pct=16.622,
    missile_speed=1800,
    crit_dmg_pct=200,
)
