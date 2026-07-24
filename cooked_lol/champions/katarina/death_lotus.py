from cooked_lol.systems.systems import SpellRank, reduce_cooldown, validate_rank

DAGGER_PER_SEC = 6
MAX_CHANNEL_SECS = 2.5


def daggers(channel_secs: float = MAX_CHANNEL_SECS) -> int:
    assert (
        channel_secs > 0 and channel_secs <= MAX_CHANNEL_SECS
    ), f"Received impossible channel time of '{channel_secs}' seconds. Max channel time is {MAX_CHANNEL_SECS} seconds."
    return int(channel_secs * DAGGER_PER_SEC)


def physical_per_dagger(bonus_ad: float, bonus_as_pct: float) -> float:
    return bonus_ad * (0.16 + 0.50 * (bonus_as_pct / 100))


def magic_per_dagger(rank: SpellRank, ap: float) -> float:
    validate_rank(rank)
    return 12.5 + 12.5 * rank + 0.19 * ap


def onhit_effectiveness(rank: SpellRank) -> float:
    validate_rank(rank)
    return (20 + 5 * rank) / 100


def physical(
    bonus_ad: float,
    bonus_as_pct: float,
    channel_secs: float = MAX_CHANNEL_SECS,
) -> float:
    return physical_per_dagger(bonus_ad, bonus_as_pct) * daggers(channel_secs)


def magic(
    rank: SpellRank,
    ap: float,
    channel_secs: float = MAX_CHANNEL_SECS,
) -> float:
    return magic_per_dagger(rank, ap) * daggers(channel_secs)


def cooldown(rank: SpellRank, haste: int = 0) -> float:
    validate_rank(rank)
    return reduce_cooldown(90 - 15 * rank, haste)
