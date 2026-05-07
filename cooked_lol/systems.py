from dataclasses import dataclass


@dataclass(frozen=True)
class Stat:
    base: float
    growth: float


def stat_at_level(stat: Stat, level: int) -> float:
    """Standard LoL per-level scaling: base + growth * (L-1) * (0.7025 + 0.0175*(L-1))."""
    n = level - 1
    return stat.base + stat.growth * n * (0.7025 + 0.0175 * n)


def reduce_cooldown(base_cd: float, haste: int) -> float:
    """
    https://leagueoflegends.fandom.com/wiki/Haste
    """
    return round(base_cd * 100 / (100 + haste), 1)


def post_mitigation(raw_damage: float, resist: float) -> float:
    """
    Damage taken after armor or magic resist mitigation. Same formula for both.
    https://leagueoflegends.fandom.com/wiki/Armor
    """
    if resist >= 0:
        return raw_damage * 100 / (100 + resist)
    return raw_damage * (2 - 100 / (100 - resist))


def pre_mitigation(post_damage: float, resist: float) -> float:
    """Inverse of post_mitigation: raw damage required to deal given post-mit damage."""
    if resist >= 0:
        return post_damage * (1 + resist / 100)
    return post_damage / (2 - 100 / (100 - resist))
