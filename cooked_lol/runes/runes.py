# Stat shards. Source: wiki rune page (Option 1 / 2 / 3 rows).

# Adaptive Force shard (Offense and Flex rows): 5.4 AD or 9 AP.
ADAPTIVE_FORCE_PER_SHARD = 9
AP_PER_ADAPTIVE_FORCE = 1.0
AD_PER_ADAPTIVE_FORCE = 0.6  # 9 AF -> 5.4 AD

# Offense row.
BONUS_AS_PCT_SHARD = 10.0
ABILITY_HASTE_SHARD = 8

# Flex row.
BONUS_MS_PCT_SHARD = 2.5

# Defense row.
FLAT_HP_SHARD = 65
TENACITY_PCT_SHARD = 15.0
SLOW_RESIST_PCT_SHARD = 15.0

# Scaling health shard (Flex and Defense rows): 10 - 200 based on level.
# Wiki formula: 10 + (180 - 10) / 17 * (level - 1), i.e. exactly 10 per level.
SCALING_HP_SHARD_PER_LEVEL = 10.0


def ap_from_shards(count: int) -> float:
    return ADAPTIVE_FORCE_PER_SHARD * AP_PER_ADAPTIVE_FORCE * count


def ad_from_shards(count: int) -> float:
    return ADAPTIVE_FORCE_PER_SHARD * AD_PER_ADAPTIVE_FORCE * count


def scaling_hp_shard(level: int) -> float:
    return SCALING_HP_SHARD_PER_LEVEL * level
