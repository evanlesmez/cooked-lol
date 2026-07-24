from cooked_lol.types.item import Item

ITEM = Item(name="Zhonya's Hourglass", cost=3250, ap=105, armor=50)

# Time Stop: stasis for 2.5s, untargetable and invulnerable, but unable to move,
# basic attack, cast, use summoner spells or activate items.
# Purely defensive with no damage or stat component, so there is nothing to
# compute here - the numbers are the whole effect.
# Limitation: a build is limited to 1 Stasis item.
TIME_STOP_STASIS_DURATION = 2.5
TIME_STOP_CD = 120.0
