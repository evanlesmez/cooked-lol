"""
Focus on damage to a base resist squishy champ Smolder.
Mid game 2 item core.

2 adaptive force runes and dorans and dark seal.
Spellslinger shoes.
mid quest.
3 darkseal stacks

Katarina lvl 11
Smolder lvl 10

Try different builds to see which 2 item spike is highest dmg
Print graph of results
Include onhit and gb active if in build
"""
from itertools import combinations, product
from pathlib import Path

import matplotlib.pyplot as plt

from cooked_lol.s16.p10 import (
    dark_seal,
    dorans_ring,
    hextech_gunblade,
    liandrys_torment,
    lichbane,
    midlane_quest,
    rabadons_deathcap,
    runes,
    shadowflame,
    spellslingers_shoes,
    void_staff,
)
from cooked_lol.s16.p10.katarina import KATARINA, dagger_damage
from cooked_lol.s16.p10.smolder import SMOLDER
from cooked_lol.systems import post_mitigation, stat_at_level

KAT_LEVEL = 11
SMOLDER_LEVEL = 10
DARK_SEAL_STACKS = 3
RUNE_AF_SHARDS = 2

CORE_ITEMS = {
    "lichbane": lichbane.LICHBANE,
    "gunblade": hextech_gunblade.HEXTECH_GUNBLADE,
    "shadowflame": shadowflame.SHADOWFLAME,
    "rabadons": rabadons_deathcap.RABADONS_DEATHCAP,
    "voidstaff": void_staff.VOID_STAFF,
    "liandrys": liandrys_torment.LIANDRYS_TORMENT,
}

FIXED_COST = (
    dorans_ring.DORANS_RING.cost
    + dark_seal.DARK_SEAL.cost
    + spellslingers_shoes.SPELLSLINGERS_SHOES.cost
)


def build_spike(
    item_a: str, item_b: str, gb_active: bool, sf_proc: bool
) -> tuple[float, float, int]:
    """Return (raw_damage, post_mit_damage, gold_cost) for a 2-item core under flag toggles."""
    chosen = (CORE_ITEMS[item_a], CORE_ITEMS[item_b])
    ids = {item_a, item_b}

    rune_ap = runes.ap_from_shards(runes.ADAPTIVE_FORCE_SHARD, RUNE_AF_SHARDS)
    fixed_ap = (
        rune_ap
        + dorans_ring.DORANS_RING.ap
        + dark_seal.ap_with_glory(dark_seal.DARK_SEAL, DARK_SEAL_STACKS)
    )
    flat_ap = sum(getattr(it, "ap", 0) for it in chosen)
    ap = fixed_ap + flat_ap

    if "rabadons" in ids:
        ap = rabadons_deathcap.apply_magical_opus(rabadons_deathcap.RABADONS_DEATHCAP, ap)
    ap = midlane_quest.quest_ap(midlane_quest.MIDLANE_QUEST, ap)

    bonus_ad = sum(getattr(it, "ad", 0) for it in chosen)
    bonus_ad = midlane_quest.quest_bonus_ad(midlane_quest.MIDLANE_QUEST, bonus_ad)

    # Magic pen: Spellslinger's always; Void Staff %; Shadowflame flat.
    pct_factor = 1 - spellslingers_shoes.SPELLSLINGERS_SHOES.magic_pen_pct / 100
    if "voidstaff" in ids:
        pct_factor *= 1 - void_staff.VOID_STAFF.magic_pen_pct / 100
    flat_pen = spellslingers_shoes.SPELLSLINGERS_SHOES.magic_pen
    if "shadowflame" in ids:
        flat_pen += shadowflame.SHADOWFLAME.magic_pen

    smolder_mr = stat_at_level(SMOLDER.mr, SMOLDER_LEVEL)
    eff_mr = max(0.0, smolder_mr * pct_factor - flat_pen)

    raw = dagger_damage(KAT_LEVEL, bonus_ad, ap)
    if "lichbane" in ids:
        kat_base_ad = stat_at_level(KATARINA.ad, KAT_LEVEL)
        raw += lichbane.spellblade_damage(lichbane.LICHBANE, kat_base_ad, ap)
    if "gunblade" in ids and gb_active:
        raw += hextech_gunblade.active_damage(
            hextech_gunblade.HEXTECH_GUNBLADE, KAT_LEVEL, ap
        )
    if "liandrys" in ids:
        smolder_hp = stat_at_level(SMOLDER.hp, SMOLDER_LEVEL)
        raw += liandrys_torment.burn_damage(liandrys_torment.LIANDRYS_TORMENT, smolder_hp)

    # Cinderbloom is a damage-instance multiplier; apply pre-mitigation.
    if "shadowflame" in ids and sf_proc:
        raw = shadowflame.apply_cinderbloom(shadowflame.SHADOWFLAME, raw, target_hp_pct=0)

    post = post_mitigation(raw, eff_mr)

    cost = FIXED_COST + chosen[0].cost + chosen[1].cost
    return raw, post, cost


def main() -> None:
    rows = []
    for a, b in combinations(CORE_ITEMS, 2):
        ids = {a, b}
        gb_opts = (True, False) if "gunblade" in ids else (False,)
        sf_opts = (True, False) if "shadowflame" in ids else (False,)
        for gb_active, sf_proc in product(gb_opts, sf_opts):
            raw, post, cost = build_spike(a, b, gb_active, sf_proc)
            tags = []
            if "gunblade" in ids:
                tags.append("GB" if gb_active else "-GB")
            if "shadowflame" in ids:
                tags.append("SF" if sf_proc else "-SF")
            label = f"{a}+{b}" + (f" [{','.join(tags)}]" if tags else "")
            rows.append((label, raw, post, cost))

    rows.sort(key=lambda r: r[2], reverse=True)

    print(f"{'build':40s}  {'raw':>8s}  {'post-mit':>9s}  {'gold':>6s}")
    for label, raw, post, cost in rows:
        print(f"{label:40s}  {raw:8.1f}  {post:9.1f}  {cost:6d}")

    labels = [r[0] for r in rows]
    posts = [r[2] for r in rows]
    costs = [r[3] for r in rows]

    fig, ax = plt.subplots(figsize=(11, max(6.0, len(rows) * 0.35)))
    bars = ax.barh(labels, posts, color="tab:purple")
    ax.invert_yaxis()
    ax.set_xlabel("Post-mitigation damage")
    ax.set_title(
        f"Kat L{KAT_LEVEL} 2-item spike vs Smolder L{SMOLDER_LEVEL} "
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
