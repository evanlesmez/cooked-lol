from cooked_lol.types.champion_stats import ChampionStats, Stat

# Source: in-game stats panel (level 1-20 range).
# Verified: stat_at_level(s, 20) reproduces the displayed L20 values exactly.
STATS = ChampionStats(
    name="Viktor",
    melee=False,
    hp=Stat(600, 100),
    hp5=Stat(8, 0.65),
    mp=Stat(405, 45),
    mp5=Stat(8, 0.8),
    ar=Stat(23, 4.4),
    mr=Stat(30, 1.3),
    ad=Stat(53, 3),
    bonus_as_pct=Stat(0, 2.11),
    ms=335,
    attack_range=525,
    base_as=0.658,
    windup_pct=18,
    missile_speed=2300,
    crit_dmg_pct=200,
)
