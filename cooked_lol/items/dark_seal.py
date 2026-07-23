from cooked_lol.metaclass.metaclass import DataReadOnlyMeta


class DarkSeal(metaclass=DataReadOnlyMeta):
    cost: int = 350
    ap: int = 15
    hp: int = 50
    # Glory: takedown stacks grant AP; lose 5 on death. Preserved into Mejai's.
    glory_stacks_per_kill: int = 2
    glory_stacks_per_assist: int = 1
    glory_stacks_lost_on_death: int = 5
    glory_ap_per_stack: int = 4
    glory_max_stacks: int = 10


def ap_with_glory(stacks: int) -> int:
    """Total AP from item including current Glory stacks (capped at max)."""
    capped = min(max(stacks, 0), DarkSeal.glory_max_stacks)
    return DarkSeal.ap + DarkSeal.glory_ap_per_stack * capped
