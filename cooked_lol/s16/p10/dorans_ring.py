import math
from dataclasses import dataclass


@dataclass(frozen=True)
class DoransRing:
    cost: int = 400
    ap: int = 18
    hp: int = 90
    # Drain: passive mana regen, doubled for 5s after damaging a champion.
    drain_mana_per_sec: int = 1
    drain_active_mana_per_sec: int = 2
    drain_active_duration: float = 5.0
    drain_manaless_heal_pct: float = 45
    # Helping Hand: bonus on-hit physical damage to minions.
    helping_hand_minion_dmg: int = 5


DORANS_RING = DoransRing()


def drain_mana_regen(item: DoransRing, in_champion_combat: bool) -> int:
    """Mana restored per second from Drain. Doubles for 5s after damaging a champ."""
    return item.drain_active_mana_per_sec if in_champion_combat else item.drain_mana_per_sec


def drain_heal_per_sec(item: DoransRing, in_champion_combat: bool) -> int:
    """For manaless champions: floor(value * 45%) heal per second instead of mana."""
    value = drain_mana_regen(item, in_champion_combat)
    return math.floor(value * item.drain_manaless_heal_pct / 100)
