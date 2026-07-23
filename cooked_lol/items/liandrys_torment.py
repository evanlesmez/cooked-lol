from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class LiandrysTorment(metaclass=DataReadOnlyMeta):
    cost: int = 3000
    ap: int = 60
    hp: int = 300
    # Torment: ability damage applies a burn that ticks max-HP% magic damage.
    burn_pct_per_tick: float = 1.0
    burn_tick_interval: float = 0.5
    burn_duration: float = 3.0
    burn_monster_tick_cap: int = 20


def burn_damage(target_max_hp: float, is_monster: bool = False) -> float:
    """Total Torment burn over full duration (pre-mitigation magic damage)."""
    ticks = int(LiandrysTorment.burn_duration / LiandrysTorment.burn_tick_interval)
    per_tick = target_max_hp * LiandrysTorment.burn_pct_per_tick / 100
    if is_monster:
        per_tick = min(per_tick, LiandrysTorment.burn_monster_tick_cap)
    return per_tick * ticks
