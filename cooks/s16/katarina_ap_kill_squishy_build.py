"""
Focus on damage to a base resist squishy champ Caitlyn.
Mid game 2 item core.

2 adaptive force shards, dorans and dark seal (3 stacks), spellslinger shoes.
Midlane quest completed. Caitlyn has the scaling HP shard and a Doran's Blade.

Katarina lvl 12, combo = dagger
Caitlyn lvl 10.

Try different builds to see which 2 item spike is highest dmg.
Print graph of results. Include onhit and gb active if in build.
"""

from itertools import combinations, product
from pathlib import Path

import matplotlib.pyplot as plt

from cooked_lol.champions.caitlyn import STATS as CAIT
from cooked_lol.champions.katarina import STATS as KAT
from cooked_lol.champions.katarina import sinister_steel
from cooked_lol.items import (
    dark_seal,
    dorans_blade,
    dorans_ring,
    hextech_gunblade,
    liandrys_torment,
    lichbane,
    rabadons_deathcap,
    shadowflame,
    spellslingers_shoes,
    void_staff,
)
from cooked_lol.runes import runes
from cooked_lol.systems.midlane_quest import quest_ap, quest_bonus_ad
from cooked_lol.systems.systems import post_mitigation_damage, stat_at_level
from cooked_lol.types.item import Item

KAT_LEVEL = 12
CAIT_LEVEL = 10
DARK_SEAL_STACKS = 3
RUNE_AF_SHARDS = 2

CORE_ITEMS: dict[str, Item] = {
    "lichbane": lichbane.ITEM,
    "gunblade": hextech_gunblade.ITEM,
    "shadowflame": shadowflame.ITEM,
    "rabadons": rabadons_deathcap.ITEM,
    "voidstaff": void_staff.ITEM,
    "liandrys": liandrys_torment.ITEM,
}

FIXED_COST = dorans_ring.ITEM.cost + dark_seal.ITEM.cost + spellslingers_shoes.ITEM.cost

CAIT_HP = (
    stat_at_level(CAIT.hp, CAIT_LEVEL)
    + runes.scaling_hp_shard(CAIT_LEVEL)
    + dorans_blade.ITEM.hp
)
CAIT_MR = stat_at_level(CAIT.mr, CAIT_LEVEL)


def build_spike(
    item_a: str, item_b: str, gb_active: bool, sf_proc: bool
) -> tuple[float, float, int]:
    """Return (raw_damage, post_mit_damage, gold_cost) for a 2-item core under flag toggles."""
    chosen = (CORE_ITEMS[item_a], CORE_ITEMS[item_b])
    ids = {item_a, item_b}

    ap = (
        runes.ap_from_shards(RUNE_AF_SHARDS)
        + dorans_ring.ITEM.ap
        + dark_seal.ap_with_glory(DARK_SEAL_STACKS)
        + sum(it.ap for it in chosen)
    )
    if "rabadons" in ids:
        ap = rabadons_deathcap.apply_magical_opus(ap)
    ap = quest_ap(ap)
    bonus_ad = quest_bonus_ad(sum(it.ad for it in chosen))

    # Magic pen: Spellslinger's always; Void Staff %; Shadowflame flat.
    # Percent pen sources stack multiplicatively, then flat pen applies.
    pct_factor = 1 - spellslingers_shoes.ITEM.magic_pen_pct / 100
    if "voidstaff" in ids:
        pct_factor *= 1 - void_staff.ITEM.magic_pen_pct / 100
    flat_pen = spellslingers_shoes.ITEM.magic_pen
    if "shadowflame" in ids:
        flat_pen += shadowflame.ITEM.magic_pen
    eff_mr = max(0.0, CAIT_MR * pct_factor - flat_pen)

    raw = sinister_steel.damage(KAT_LEVEL, bonus_ad, ap)
    if "lichbane" in ids:
        kat_base_ad = stat_at_level(KAT.ad, KAT_LEVEL)
        raw += lichbane.spellblade_damage(kat_base_ad, ap)
    if "gunblade" in ids and gb_active:
        raw += hextech_gunblade.active_damage(KAT_LEVEL, ap)
    if "liandrys" in ids:
        raw += liandrys_torment.burn_damage(CAIT_HP)
    # Cinderbloom is a damage-instance multiplier; apply pre-mitigation.
    if "shadowflame" in ids and sf_proc:
        raw = shadowflame.apply_cinderbloom(raw, target_hp_pct=0)

    cost = FIXED_COST + chosen[0].cost + chosen[1].cost
    return raw, post_mitigation_damage(raw, eff_mr), cost


def main() -> None:
    print(
        f"Caitlyn L{CAIT_LEVEL}\ntotal HP (HP shard + Doran's Blade): {CAIT_HP:.1f}\nMR: {CAIT_MR: .1f}"
    )

    rows = []
    for a, b in combinations(CORE_ITEMS, 2):
        ids = {a, b}
        gb_opts = (True, False) if "gunblade" in ids else (False,)
        sf_opts = (True, False) if "shadowflame" in ids else (False,)
        for gb_active, sf_proc in product(gb_opts, sf_opts):
            raw, post, cost = build_spike(a, b, gb_active, sf_proc)
            tags = [t for t, on in (("GB", gb_active), ("SF", sf_proc)) if on]
            label = f"{a}+{b}" + (f" [{','.join(tags)}]" if tags else "")
            rows.append((label, raw, post, cost))
    rows.sort(key=lambda r: r[2], reverse=True)

    print(f"{'build':40s}  {'raw':>8s}  {'post-mit':>9s}  {'gold':>6s}")
    for label, raw, post, cost in rows:
        print(f"{label:40s}  {raw:8.1f}  {post:9.1f}  {cost:6d}")

    labels, posts, costs = zip(*[(r[0], r[2], r[3]) for r in rows])
    fig, ax = plt.subplots(figsize=(11, max(6.0, len(rows) * 0.35)))
    bars = ax.barh(labels, posts, color="tab:purple")
    ax.invert_yaxis()
    ax.set_xlabel("Post-mitigation damage")
    ax.set_title(
        f"Kat L{KAT_LEVEL} dagger passive 2-item spike vs Caitlyn L{CAIT_LEVEL} "
        f"({DARK_SEAL_STACKS} Dark Seal stacks)"
    )
    for bar, cost in zip(bars, costs):
        ax.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f" {cost}g",
            va="center",
            fontsize=9,
        )
    plt.tight_layout()
    out = Path(__file__).with_suffix(".png")
    plt.savefig(out)
    print(f"\nchart -> {out}")


if __name__ == "__main__":
    main()
