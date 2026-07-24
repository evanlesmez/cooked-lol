"""Voracity (P): takedown refunds ability cooldowns."""

EFFECT_RADIUS = 340
TAKEDOWN_WINDOW = 3.0
CD_REFUND = 15.0


def apply_cd_refund(current_cd: float) -> float:
    """Reduce a current cooldown by the Voracity refund (floored at 0)."""
    return max(0.0, current_cd - CD_REFUND)
