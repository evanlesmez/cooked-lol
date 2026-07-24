from cooked_lol.types.champion_stats import ChampionStats, Stat

# Source: in-game stats panel (level 1-20 range).
# Verified: stat_at_level(s, 20) reproduces the displayed L20 values exactly.
# Manaless; secondary bar is Shield (Indestructible).
STATS = ChampionStats(
    name="Mordekaiser",
    melee=True,
    hp=Stat(645, 104),
    hp5=Stat(5, 0.75),
    ar=Stat(37, 4.2),
    mr=Stat(32, 2.05),
    ad=Stat(61, 4),
    bonus_as_pct=Stat(0, 1),
    ms=335,
    attack_range=175,
    base_as=0.625,
    windup_pct=21.133,
    crit_dmg_pct=200,
)
