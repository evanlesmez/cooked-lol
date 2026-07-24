from cooked_lol.types.item import Item

ITEM = Item(name="Dark Seal", cost=350, ap=15, hp=50)

# Glory: takedown stacks grant AP; lose 5 on death. Preserved into Mejai's.
GLORY_STACKS_PER_KILL = 2
GLORY_STACKS_PER_ASSIST = 1
GLORY_STACKS_LOST_ON_DEATH = 5
GLORY_AP_PER_STACK = 4
GLORY_MAX_STACKS = 10


def ap_with_glory(stacks: int) -> float:
    """Total AP from item including current Glory stacks."""
    assert (
        0 <= stacks <= GLORY_MAX_STACKS
    ), f"Glory stacks must be 0-{GLORY_MAX_STACKS}, got {stacks}"
    return ITEM.ap + GLORY_AP_PER_STACK * stacks
