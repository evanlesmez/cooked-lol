from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class KrakenSlayer(metaclass=DataReadOnlyMeta):
    cost: int = 3000
    ad: int = 45
    attack_speed_pct: float = 40.0
    move_speed_pct: float = 4.0
    # Bring It Down: every 3rd on-hit deals bonus physical damage.
    bring_it_down_stack_duration: float = 3.0
    bring_it_down_max_stacks: int = 2
    # Melee base: 150 (L1-8), then +5/level to 210 at L20. Ranged is 80%.
    bring_it_down_base_l1: float = 150.0
    bring_it_down_base_l20: float = 210.0
    bring_it_down_scale_start_level: int = 8
    bring_it_down_ranged_pct: float = 80.0
    # +0%–75% damage amp from target missing HP (5% per 6.666...% missing).
    bring_it_down_max_amp_pct: float = 75.0


def bring_it_down_base(level: int, is_melee: bool = True) -> float:
    """Base Bring It Down damage before missing-HP amp."""
    per_level = (
        KrakenSlayer.bring_it_down_base_l20 - KrakenSlayer.bring_it_down_base_l1
    ) / (20 - KrakenSlayer.bring_it_down_scale_start_level)
    steps = max(0, level - KrakenSlayer.bring_it_down_scale_start_level)
    melee = KrakenSlayer.bring_it_down_base_l1 + per_level * steps
    if is_melee:
        return melee
    return melee * KrakenSlayer.bring_it_down_ranged_pct / 100


def bring_it_down_damage(
    level: int,
    target_missing_hp_pct: float,
    is_melee: bool = True,
) -> float:
    """Pre-mitigation bonus physical damage from a Bring It Down proc."""
    base = bring_it_down_base(level, is_melee)
    missing = max(0.0, min(target_missing_hp_pct, 100.0))
    amp = KrakenSlayer.bring_it_down_max_amp_pct / 100 * (missing / 100)
    return base * (1 + amp)
