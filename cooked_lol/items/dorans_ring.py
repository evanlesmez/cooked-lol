import math

from cooked_lol.types.item import Item

ITEM = Item(name="Doran's Ring", cost=400, ap=18, hp=90)

# Drain: passive mana regen, doubled for 5s after damaging a champion.
DRAIN_MANA_PER_SEC = 1
DRAIN_ACTIVE_MANA_PER_SEC = 2
DRAIN_ACTIVE_DURATION = 5.0
DRAIN_MANALESS_HEAL_PCT = 45

# Helping Hand: bonus on-hit physical damage to minions.
HELPING_HAND_MINION_DMG = 5


def drain_mana_regen(in_champion_combat: bool) -> int:
    """Mana restored per second from Drain. Doubles for 5s after damaging a champ."""
    return DRAIN_ACTIVE_MANA_PER_SEC if in_champion_combat else DRAIN_MANA_PER_SEC


def drain_heal_per_sec(in_champion_combat: bool) -> int:
    """For manaless champions: floor(value * 45%) heal per second instead of mana."""
    value = drain_mana_regen(in_champion_combat)
    return math.floor(value * DRAIN_MANALESS_HEAL_PCT / 100)
