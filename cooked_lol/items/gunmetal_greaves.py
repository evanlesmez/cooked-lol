from cooked_lol.types.item import Item

# Midlane Quest reward: Berserker's Greaves upgrades into these for free once the
# quest completes, so the cost is just Berserker's total with no extra combine.
# Limitation: limited to 1 boots item.
ITEM = Item(
    name="Gunmetal Greaves",
    cost=1100,
    attack_speed_pct=40.0,
    move_speed=45,
    life_steal_pct=5.0,
)
