"""
Katarina AD on-hit 3-item cores.

Kat L16, Doran's Blade, 1 adaptive force (AD), Conqueror (AD), midlane quest done.
Skill order Q > E > W with R at 6/11/16 -> Q5 E5 W3 R3.
Melee: every damaging combo step grants 2 Conqueror stacks (cap 12).

Compares the two 3-item finishes off a Kraken > Bork core:
    Kraken > Bork > Terminus
    Kraken > Bork > LDR

Two combos, charted separately because their step counts differ:
    E > AA > P > Q > E > AA > P   the on-hit combo from the 2-item cook
    E > Q > P > R                 dagger drop into Death Lotus

The E > Q > P > R combo also runs both cores with Gunmetal Greaves added, since
Death Lotus' physical damage is the only thing in this model that scales with
bonus attack speed. The on-hit combo deliberately omits the boots variants: no
step there scales with attack speed, so they would be identical lines costing
1100 more gold.

Modelling notes for E > Q > P > R:
  - Q drops a dagger; P is Kat picking it up, so it resolves as the Sinister Steel
    dagger slash with a full on-hit proc. (W would resolve identically.)
  - R (Death Lotus) is 15 daggers over the full 2.5s channel. Each dagger deals
    its own physical + magic and applies on-hit effects at Death Lotus'
    effectiveness (35% at R3), so Kraken still procs every 3rd dagger and Bork
    scales off the target's falling current HP.

See cooks/combo_sim.py for how damage, on-hit ordering and overkill are resolved.
"""

import argparse
import sys
from typing import NamedTuple

from cooked_lol.champions import caitlyn, mordekaiser, viktor
from cooked_lol.champions.katarina import STATS as KAT
from cooked_lol.champions.katarina import (
    bouncing_blade,
    death_lotus,
    shunpo,
    sinister_steel,
)
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
    gunmetal_greaves,
    terminus,
    zhonyas_hourglass,
)
from cooked_lol.runes import conqueror, runes
from cooked_lol.systems.midlane_quest import quest_ap, quest_bonus_ad
from cooked_lol.systems.systems import SpellRank, stat_at_level
from cooked_lol.types.item import Item
from cooks import charts, config
from cooks.combo_sim import (
    SOURCE_BORK,
    SOURCE_KRAKEN,
    SOURCE_TERMINUS,
    Build,
    ComboResult,
    Hit,
    Target,
    magic_label,
    make_build,
    make_target,
    physical_label,
    rank_key,
    simulate,
)

KAT_LEVEL = 16
Q_RANK: SpellRank = 5
E_RANK: SpellRank = 5
R_RANK: SpellRank = 3
RUNE_AF_SHARDS = 1
CONQ_STACKS_PER_HIT = 2  # melee; every damaging combo step
R_CHANNEL_SECS = death_lotus.MAX_CHANNEL_SECS

START_HP_PCTS = (100.0, 50.0)


class ComboSpec(NamedTuple):
    label: str  # human-readable name for headings
    slug: str  # chart filename suffix
    steps: tuple[str, ...]
    builds: tuple[str, ...]  # ITEM_SETS keys to compare for this combo


_TERMINUS_CORE = (
    kraken_slayer.ITEM,
    blade_of_the_ruined_king.ITEM,
    terminus.ITEM,
)
_LDR_CORE = (
    kraken_slayer.ITEM,
    blade_of_the_ruined_king.ITEM,
    lord_dominiks_regards.ITEM,
)

ITEM_SETS: dict[str, tuple[Item, ...]] = {
    "Kraken>Bork>Terminus": _TERMINUS_CORE,
    "Kraken>Bork>LDR": _LDR_CORE,
    "Kraken>Bork>Terminus+Gunmetal": _TERMINUS_CORE + (gunmetal_greaves.ITEM,),
    "Kraken>Bork>LDR+Gunmetal": _LDR_CORE + (gunmetal_greaves.ITEM,),
}

CORE_BUILDS = ("Kraken>Bork>Terminus", "Kraken>Bork>LDR")
BOOTS_BUILDS = (
    "Kraken>Bork>Terminus",
    "Kraken>Bork>Terminus+Gunmetal",
    "Kraken>Bork>LDR",
    "Kraken>Bork>LDR+Gunmetal",
)

COMBOS = (
    ComboSpec("on-hit", "onhit", ("E", "AA", "P", "Q", "E", "AA", "P"), CORE_BUILDS),
    ComboSpec("E>Q>P>R", "eqpr", ("E", "Q", "P", "R"), BOOTS_BUILDS),
)

# Fixed colour per build so a build keeps its identity across every panel. Each
# core and its boots variant share a hue family so the pairs read together.
BUILD_COLORS = {
    "Kraken>Bork>Terminus": "tab:green",
    "Kraken>Bork>Terminus+Gunmetal": "tab:olive",
    "Kraken>Bork>LDR": "tab:orange",
    "Kraken>Bork>LDR+Gunmetal": "tab:red",
}
assert (
    BUILD_COLORS.keys() == ITEM_SETS.keys()
), f"BUILD_COLORS must cover exactly ITEM_SETS, got {BUILD_COLORS.keys() ^ ITEM_SETS.keys()}"
for _spec in COMBOS:
    assert set(_spec.builds) <= ITEM_SETS.keys(), (
        f"combo {_spec.slug!r} names builds outside ITEM_SETS: "
        f"{set(_spec.builds) - ITEM_SETS.keys()}"
    )

# Death Lotus tick chart: the dagger's own damage on the bottom split by damage
# type, then the on-hit procs above it. Orange is physical and blue is magic, which
# is the split LDR's armor pen acts on (physical only).
R_DAGGER_LABEL = "R dagger"
R_DAGGER_PHYS = physical_label(R_DAGGER_LABEL)
R_DAGGER_MAGIC = magic_label(R_DAGGER_LABEL)
SOURCE_ORDER = (
    R_DAGGER_PHYS,
    R_DAGGER_MAGIC,
    SOURCE_BORK,
    SOURCE_TERMINUS,
    SOURCE_KRAKEN,
)
SOURCE_COLORS = {
    R_DAGGER_PHYS: "tab:orange",
    R_DAGGER_MAGIC: "tab:blue",
    # Not cyan: it would sit directly above the blue magic band and blur into it.
    SOURCE_BORK: "tab:purple",
    SOURCE_TERMINUS: "tab:olive",
    SOURCE_KRAKEN: "tab:red",
}


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
    ap = quest_ap(0.0)  # no AP in any of these builds
    if step == "E":
        return (
            Hit(
                raw_magic=shunpo.damage(E_RANK, bonus_ad, ap),
                onhit_effectiveness=1.0,
                label="E Shunpo",
            ),
        )
    if step in ("W", "P"):
        # A dagger pickup: the Sinister Steel slash, a full on-hit proc. Q and W
        # both drop daggers, so either spelling of the step resolves the same way.
        return (
            Hit(
                raw_magic=sinister_steel.damage(KAT_LEVEL, bonus_ad, ap),
                onhit_effectiveness=1.0,
                label="dagger slash",
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
    if step == "Q":
        return (
            Hit(raw_magic=bouncing_blade.damage(Q_RANK, ap), label="Q Bouncing Blade"),
        )
    assert step == "R", f"unknown combo step {step!r}"
    return tuple(
        Hit(
            raw_physical=death_lotus.physical_per_dagger(bonus_ad, build.bonus_as_pct),
            raw_magic=death_lotus.magic_per_dagger(R_RANK, ap),
            onhit_effectiveness=death_lotus.onhit_effectiveness(R_RANK),
            label=R_DAGGER_LABEL,
        )
        for _ in range(death_lotus.daggers(R_CHANNEL_SECS))
    )


def target_morde() -> Target:
    level = 18
    return make_target(
        short=f"Morde L{level}",
        detail="HP shard + Doran's Ring + Rylai's + Riftmaker + Steelcaps + Liandry's",
        level=level,
        base_hp=stat_at_level(mordekaiser.STATS.hp, level),
        base_ar=stat_at_level(mordekaiser.STATS.ar, level),
        base_mr=stat_at_level(mordekaiser.STATS.mr, level),
        items=(
            dorans_ring.ITEM,
            rylais_crystal_scepter.ITEM,
            riftmaker.ITEM,
            plated_steelcaps.ITEM,
            liandrys_torment.ITEM,
        ),
    )


def target_viktor() -> Target:
    level = 16
    return make_target(
        short=f"Viktor L{level}",
        detail="HP shard + Doran's Ring + Liandry's + Zhonya's",
        level=level,
        base_hp=stat_at_level(viktor.STATS.hp, level),
        base_ar=stat_at_level(viktor.STATS.ar, level),
        base_mr=stat_at_level(viktor.STATS.mr, level),
        items=(dorans_ring.ITEM, liandrys_torment.ITEM, zhonyas_hourglass.ITEM),
    )


def target_caitlyn() -> Target:
    level = 14
    return make_target(
        short=f"Caitlyn L{level}",
        detail="HP shard, no items",
        level=level,
        base_hp=stat_at_level(caitlyn.STATS.hp, level),
        base_ar=stat_at_level(caitlyn.STATS.ar, level),
        base_mr=stat_at_level(caitlyn.STATS.mr, level),
    )


def run(spec: ComboSpec, build_name: str, target: Target, pct: float) -> ComboResult:
    return simulate(
        build_for(build_name),
        target,
        spec.steps,
        resolve_step,
        level=KAT_LEVEL,
        is_melee=KAT.melee,
        conq_stacks_per_step=CONQ_STACKS_PER_HIT,
        start_hp_pct=pct,
    )


def result_outcome(spec: ComboSpec, result: ComboResult) -> str:
    if result.killed_on_step is None:
        return f"survives, {result.hp_left:.1f} HP left"
    step = spec.steps[result.killed_on_step - 1]
    return f"KILL on {result.killed_on_step}/{len(spec.steps)} ({step})"


def print_table(spec: ComboSpec, target: Target, pct: float) -> None:
    results = sorted(
        (run(spec, name, target, pct) for name in spec.builds),
        key=rank_key,
        reverse=True,
    )
    start_hp = results[0].start_hp
    print(f"\n=== vs {target.name} @ {pct:g}% HP ===")
    print(
        f"start HP {start_hp:.1f} / max {target.max_hp:.1f} "
        f"(bonus {target.bonus_hp:.1f})  "
        f"AR {target.armor:.1f}  MR {target.mr:.1f}"
    )
    print(
        f"{'build':30s}  {'dealt':>8s}  {'%HP':>6s}  {'overkill':>8s}  "
        f"{'outcome':26s}  {'gold':>5s}"
    )
    for r in results:
        print(
            f"{r.build:30s}  {r.dealt:8.1f}  {r.dealt / start_hp * 100:5.1f}%  "
            f"{r.overkill:8.1f}  {result_outcome(spec, r):26s}  {r.cost:5d}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Katarina AD on-hit 3-item cores: print damage tables.",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="also write one HP-trajectory grid PNG per combo into cooks/assets/",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(
        f"Kat L{KAT_LEVEL}  Q{Q_RANK} E{E_RANK} R{R_RANK}  "
        f"Doran's Blade + 1 AF + Conqueror (AD) + midlane quest  "
        f"(+{CONQ_STACKS_PER_HIT} conq/damaging step, melee)"
    )
    print(
        f"R = {death_lotus.daggers(R_CHANNEL_SECS)} daggers over "
        f"{R_CHANNEL_SECS:g}s at {death_lotus.onhit_effectiveness(R_RANK) * 100:.0f}% "
        f"on-hit effectiveness"
    )
    targets = (target_morde(), target_viktor(), target_caitlyn())

    for spec in COMBOS:
        print(f"\n########## combo {'>'.join(spec.steps)} ##########")
        for pct in START_HP_PCTS:
            for target in targets:
                print_table(spec, target, pct)

    if args.plot:
        for spec in COMBOS:
            out = charts.plot_trajectory_grid(
                targets=targets,
                start_hp_pcts=START_HP_PCTS,
                build_names=spec.builds,
                build_colors=BUILD_COLORS,
                run=lambda name, target, pct, _s=spec: run(_s, name, target, pct),
                combo=spec.steps,
                title=(
                    f"Katarina L{KAT_LEVEL} AD on-hit 3-item cores  |  "
                    f"Q{Q_RANK} E{E_RANK} R{R_RANK}  |  "
                    f"combo {'>'.join(spec.steps)}\n"
                    "line stops where the target dies; "
                    "X below the axis marks the killing step"
                ),
                out=config.asset_path(f"katarina_ad_onhit_3item_{spec.slug}"),
            )
            # stderr so the tables on stdout stay a stable regression baseline.
            print(f"chart -> {out}", file=sys.stderr)

        channel = next(c for c in COMBOS if c.slug == "eqpr")
        r_step_no = channel.steps.index("R") + 1
        out = charts.plot_hit_ticks(
            targets=targets,
            build_names=channel.builds,
            run=lambda name, target: run(channel, name, target, 100.0),
            step_no=r_step_no,
            step_label="Death Lotus dagger",
            source_order=SOURCE_ORDER,
            source_colors=SOURCE_COLORS,
            title=(
                f"Katarina L{KAT_LEVEL} Death Lotus (R{R_RANK}) channel, tick by tick"
                f"  |  after {'>'.join(channel.steps[:r_step_no - 1])} from 100% HP\n"
                f"{death_lotus.daggers(R_CHANNEL_SECS)} daggers over "
                f"{R_CHANNEL_SECS:g}s, on-hit at "
                f"{death_lotus.onhit_effectiveness(R_RANK) * 100:.0f}% effectiveness"
            ),
            out=config.asset_path("katarina_ad_onhit_3item_r_ticks"),
        )
        print(f"chart -> {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
