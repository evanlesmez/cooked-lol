"""
Katarina AD on-hit 2-item cores (no boots).

Kat L12, Doran's Blade, 1 adaptive force (AD), Conqueror (AD), midlane quest done.
Max Q then E -> Q5 E2. Melee: every combo hit grants 2 Conqueror stacks (cap 12).

Combo: E > AA > P > Q > E > AA > P
On-hit on all except Q (Shunpo and dagger pickup apply on-hit at 100%).

See cooks/combo_sim.py for how damage, on-hit ordering and overkill are resolved.
"""

import argparse
import sys

from cooked_lol.champions import caitlyn, mordekaiser, viktor
from cooked_lol.champions.katarina import STATS as KAT
from cooked_lol.champions.katarina import bouncing_blade, shunpo, sinister_steel
from cooked_lol.items import (
    blade_of_the_ruined_king,
    dorans_blade,
    dorans_ring,
    kraken_slayer,
    liandrys_torment,
    lord_dominiks_regards,
    plated_steelcaps,
    riftmaker,
    rylais_crystal_scepter,
    terminus,
)
from cooked_lol.runes import conqueror, runes
from cooked_lol.systems.midlane_quest import quest_ap, quest_bonus_ad
from cooked_lol.systems.systems import SpellRank, stat_at_level
from cooked_lol.types.item import Item
from cooks import charts, config
from cooks.combo_sim import Build, ComboResult, Hit, Target, make_build, simulate

KAT_LEVEL = 12
Q_RANK: SpellRank = 5
E_RANK: SpellRank = 2
RUNE_AF_SHARDS = 1
CONQ_STACKS_PER_HIT = 2  # melee; every combo instance

# Combo step kinds, in order. "Q" is the only step without on-hit.
COMBO = ("E", "AA", "P", "Q", "E", "AA", "P")

START_HP_PCTS = (100.0, 75.0, 40.0)

ITEM_SETS: dict[str, tuple[Item, ...]] = {
    "Kraken+Bork": (kraken_slayer.ITEM, blade_of_the_ruined_king.ITEM),
    "Kraken+LDR": (kraken_slayer.ITEM, lord_dominiks_regards.ITEM),
    "Kraken+Terminus": (kraken_slayer.ITEM, terminus.ITEM),
    "Bork+LDR": (blade_of_the_ruined_king.ITEM, lord_dominiks_regards.ITEM),
}

# Fixed colour per build so a build keeps its identity across every panel.
BUILD_COLORS = {
    "Kraken+Bork": "tab:blue",
    "Kraken+LDR": "tab:orange",
    "Kraken+Terminus": "tab:green",
    "Bork+LDR": "tab:red",
}
assert (
    BUILD_COLORS.keys() == ITEM_SETS.keys()
), f"BUILD_COLORS must cover exactly ITEM_SETS, got {BUILD_COLORS.keys() ^ ITEM_SETS.keys()}"


def build_for(name: str) -> Build:
    return make_build(
        name,
        ITEM_SETS[name],
        starter_bonus_ad=dorans_blade.ITEM.ad,
        shard_bonus_ad=runes.ad_from_shards(RUNE_AF_SHARDS),
        starter_cost=dorans_blade.ITEM.cost,
        champion_bonus_as_pct=stat_at_level(KAT.bonus_as_pct, KAT_LEVEL),
    )


def ads_at_stacks(base_bonus_ad: float, conq_stacks: int) -> tuple[float, float]:
    """Return (total_ad, bonus_ad) including Conqueror AD and midlane quest."""
    bonus_ad = quest_bonus_ad(
        base_bonus_ad + conqueror.bonus_ad(KAT_LEVEL, conq_stacks)
    )
    total_ad = stat_at_level(KAT.ad, KAT_LEVEL) + bonus_ad
    return total_ad, bonus_ad


def resolve_step(step: str, build: Build, conq_stacks: int) -> tuple[Hit, ...]:
    """Hits produced by one combo step."""
    total_ad, bonus_ad = ads_at_stacks(build.base_bonus_ad, conq_stacks)
    ap = quest_ap(0.0)  # bc no AP in build
    if step == "E":
        return (
            Hit(
                raw_magic=shunpo.damage(E_RANK, bonus_ad, ap),
                onhit_effectiveness=1.0,
                label="E Shunpo",
            ),
        )
    if step == "AA":
        return (
            Hit(
                raw_physical=total_ad,
                is_basic_attack=True,
                onhit_effectiveness=1.0,
                label="basic attack",
            ),
        )
    if step == "P":
        return (
            Hit(
                raw_magic=sinister_steel.damage(KAT_LEVEL, bonus_ad, ap),
                onhit_effectiveness=1.0,
                label="P dagger",
            ),
        )
    assert step == "Q", f"unknown combo step {step!r}"
    return (Hit(raw_magic=bouncing_blade.damage(Q_RANK, ap), label="Q Bouncing Blade"),)


def target_viktor() -> Target:
    level = 12
    bonus_hp = (
        runes.scaling_hp_shard(level) + dorans_ring.ITEM.hp + liandrys_torment.ITEM.hp
    )
    return Target(
        name=f"Viktor L{level} (HP shard + Doran's Ring + Liandry's)",
        short=f"Viktor L{level}",
        max_hp=stat_at_level(viktor.STATS.hp, level) + bonus_hp,
        bonus_hp=bonus_hp,
        armor=stat_at_level(viktor.STATS.ar, level),
        mr=stat_at_level(viktor.STATS.mr, level),
        plating=False,
    )


def target_caitlyn() -> Target:
    level = 11
    return Target(
        name=f"Caitlyn L{level} (no bonus HP)",
        short=f"Caitlyn L{level}",
        max_hp=stat_at_level(caitlyn.STATS.hp, level),
        bonus_hp=0.0,
        armor=stat_at_level(caitlyn.STATS.ar, level),
        mr=stat_at_level(caitlyn.STATS.mr, level),
        plating=False,
    )


def target_mordekaiser() -> Target:
    level = 14
    bonus_hp = (
        runes.scaling_hp_shard(level)
        + dorans_ring.ITEM.hp
        + rylais_crystal_scepter.ITEM.hp
        + riftmaker.ITEM.hp
    )
    return Target(
        name=(
            f"Morde L{level} (HP shard + Doran's Ring + Rylai's + "
            f"Riftmaker + Steelcaps)"
        ),
        short=f"Morde L{level}",
        max_hp=stat_at_level(mordekaiser.STATS.hp, level) + bonus_hp,
        bonus_hp=bonus_hp,
        armor=(
            stat_at_level(mordekaiser.STATS.ar, level) + plated_steelcaps.ITEM.armor
        ),
        mr=stat_at_level(mordekaiser.STATS.mr, level),
        plating=True,
    )


def run(build_name: str, target: Target, start_hp_pct: float) -> ComboResult:
    return simulate(
        build_for(build_name),
        target,
        COMBO,
        resolve_step,
        level=KAT_LEVEL,
        is_melee=KAT.melee,
        conq_stacks_per_step=CONQ_STACKS_PER_HIT,
        start_hp_pct=start_hp_pct,
    )


def result_outcome(result: ComboResult) -> str:
    if result.killed_on_step is None:
        return f"survives, {result.hp_left:.1f} HP left"
    step = COMBO[result.killed_on_step - 1]
    return f"KILL on {result.killed_on_step}/{len(COMBO)} ({step})"


def rank_key(result: ComboResult) -> tuple[int, int, float, float]:
    """Kills first (fewest steps, then most headroom), then by damage dealt."""
    killed = result.killed_on_step is not None
    return int(killed), -result.steps_used, result.dealt, result.overkill


def print_table(target: Target, start_hp_pct: float = 100.0) -> None:
    results = sorted(
        (run(name, target, start_hp_pct) for name in ITEM_SETS),
        key=rank_key,
        reverse=True,
    )
    start_hp = results[0].start_hp
    print(f"\n=== vs {target.name} @ {start_hp_pct:g}% HP ===")
    print(
        f"start HP {start_hp:.1f} / max {target.max_hp:.1f} "
        f"(bonus {target.bonus_hp:.1f})  "
        f"AR {target.armor:.1f}  MR {target.mr:.1f}"
    )
    print(
        f"{'build':16s}  {'dealt':>8s}  {'%HP':>6s}  {'overkill':>8s}  "
        f"{'outcome':24s}  {'gold':>5s}"
    )
    for r in results:
        pct = r.dealt / start_hp * 100
        print(
            f"{r.build:16s}  {r.dealt:8.1f}  {pct:5.1f}%  {r.overkill:8.1f}  "
            f"{result_outcome(r):24s}  {r.cost:5d}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Katarina AD on-hit 2-item cores: print damage tables.",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="also write the HP-trajectory grid PNG into cooks/assets/",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(
        f"Kat L{KAT_LEVEL}  Q{Q_RANK} E{E_RANK}  "
        f"Doran's Blade + 1 AF + Conqueror (AD) + midlane quest  |  "
        f"combo {'>'.join(COMBO)} (+{CONQ_STACKS_PER_HIT} conq/hit, melee)"
    )
    targets = (target_viktor(), target_caitlyn(), target_mordekaiser())
    for start_hp_pct in START_HP_PCTS:
        for target in targets:
            print_table(target, start_hp_pct=start_hp_pct)

    if args.plot:
        out = charts.plot_trajectory_grid(
            targets=targets,
            start_hp_pcts=START_HP_PCTS,
            build_names=tuple(ITEM_SETS),
            build_colors=BUILD_COLORS,
            run=run,
            combo=COMBO,
            title=(
                f"Katarina L{KAT_LEVEL} AD on-hit 2-item cores  |  "
                f"Q{Q_RANK} E{E_RANK}  |  combo {'>'.join(COMBO)}\n"
                "line stops where the target dies; "
                "X below the axis marks the killing step"
            ),
            out=config.asset_path("katarina_ad_onhit_2item"),
        )
        # stderr so the tables on stdout stay a stable regression baseline.
        print(f"chart -> {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
