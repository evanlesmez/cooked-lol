"""
Katarina AD on-hit 2-item cores (no boots).

Kat L9, Doran's Blade, 1 adaptive force (AD), Conqueror (AD), midlane quest done.
Max Q then E -> Q5 E2. Melee: every combo hit grants 2 Conqueror stacks (cap 12).

Combo: E > AA > P > Q > E > AA > P
On-hit on all except Q (Shunpo and dagger pickup apply on-hit at 100%).
On-hit damage resolves before the trigger's own damage, so Mist's Edge and
Bring It Down read the target's HP from before that hit.

Damage is tracked against the target's actual HP pool: the combo stops at the
step that kills, and damage past 0 HP is reported as overkill instead of being
counted as damage dealt.
"""

from dataclasses import dataclass
from typing import Any, NamedTuple

from cooked_lol.champions.caitlyn import CaitlynStats
from cooked_lol.champions.katarina import (
    KatarinaStats,
    bouncing_blade,
    shunpo,
    sinister_steel,
)
from cooked_lol.champions.mordekaiser import MordekaiserStats
from cooked_lol.champions.viktor import ViktorStats
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
from cooked_lol.systems.systems import (
    SpellRank,
    post_mitigation_damage,
    stat_at_level,
)

# Item classes use DataReadOnlyMeta, so their fields are invisible to type checkers.
ItemData = Any

KAT_LEVEL = 9
Q_RANK: SpellRank = 5
E_RANK: SpellRank = 2
RUNE_AF_SHARDS = 1
CONQ_STACKS_PER_HIT = 2  # melee; every combo instance

# Combo step kinds, in order. "Q" is the only step without on-hit.
COMBO = ("E", "AA", "P", "Q", "E", "AA", "P")

ITEM_SETS = {
    "Kraken+Bork": (
        kraken_slayer.KrakenSlayer,
        blade_of_the_ruined_king.BladeOfTheRuinedKing,
    ),
    "Kraken+LDR": (
        kraken_slayer.KrakenSlayer,
        lord_dominiks_regards.LordDominiksRegards,
    ),
    "Kraken+Terminus": (kraken_slayer.KrakenSlayer, terminus.Terminus),
    "Bork+LDR": (
        blade_of_the_ruined_king.BladeOfTheRuinedKing,
        lord_dominiks_regards.LordDominiksRegards,
    ),
}


class Target(NamedTuple):
    name: str
    max_hp: float
    bonus_hp: float
    armor: float
    mr: float
    plating: bool


class Build(NamedTuple):
    """Static per-build inputs: which on-hit items are in, and Kat's flat bonus AD."""

    name: str
    cost: int
    base_bonus_ad: float
    has_kraken: bool
    has_bork: bool
    has_ldr: bool
    has_terminus: bool


@dataclass
class ComboState:
    """Mutable per-simulation state. Data only; the logic lives in the functions."""

    hp: float
    conq_stacks: int = 0
    kraken_stacks: int = 0
    # Light stacks only grant Kat resists, so only the Dark count and the
    # Light/Dark alternation matter for outgoing damage.
    terminus_dark: int = 0
    terminus_next_light: bool = True
    dealt: float = 0.0
    overkill: float = 0.0
    steps_used: int = 0
    killed_on_step: int | None = None


class ComboResult(NamedTuple):
    build: str
    cost: int
    start_hp: float
    dealt: float  # post-mitigation damage that actually removed HP
    overkill: float  # post-mitigation damage past 0 HP
    hp_left: float
    steps_used: int
    killed_on_step: int | None


def kat_base_bonus_ad(items: tuple[ItemData, ...]) -> float:
    """Bonus AD from items + AF shard (pre-quest, pre-Conqueror)."""
    return (
        dorans_blade.DoransBlade.ad
        + runes.ad_from_shards(RUNE_AF_SHARDS)
        + sum(getattr(it, "ad", 0) for it in items)
    )


def make_build(name: str, items: tuple[ItemData, ...]) -> Build:
    """ITEM_SETS holds item classes (DataReadOnlyMeta), not instances."""
    ids = {it.__name__ for it in items}
    return Build(
        name=name,
        cost=dorans_blade.DoransBlade.cost + sum(it.cost for it in items),
        base_bonus_ad=kat_base_bonus_ad(items),
        has_kraken="KrakenSlayer" in ids,
        has_bork="BladeOfTheRuinedKing" in ids,
        has_ldr="LordDominiksRegards" in ids,
        has_terminus="Terminus" in ids,
    )


def ads_at_stacks(base_bonus_ad: float, conq_stacks: int) -> tuple[float, float]:
    """Return (total_ad, bonus_ad) including Conqueror AD and midlane quest."""
    bonus_ad = quest_bonus_ad(
        base_bonus_ad + conqueror.bonus_ad(KAT_LEVEL, conq_stacks)
    )
    total_ad = stat_at_level(KatarinaStats.ad, KAT_LEVEL) + bonus_ad
    return total_ad, bonus_ad


def target_viktor() -> Target:
    level = 9
    bonus_hp = (
        runes.scaling_hp_shard(level)
        + dorans_ring.DoransRing.hp
        + liandrys_torment.LiandrysTorment.hp
    )
    return Target(
        name=f"Viktor L{level} (HP shard + Doran's Ring + Liandry's)",
        max_hp=stat_at_level(ViktorStats.hp, level) + bonus_hp,
        bonus_hp=bonus_hp,
        armor=stat_at_level(ViktorStats.ar, level),
        mr=stat_at_level(ViktorStats.mr, level),
        plating=False,
    )


def target_caitlyn() -> Target:
    level = 8
    return Target(
        name=f"Caitlyn L{level} (no bonus HP)",
        max_hp=stat_at_level(CaitlynStats.hp, level),
        bonus_hp=0.0,
        armor=stat_at_level(CaitlynStats.ar, level),
        mr=stat_at_level(CaitlynStats.mr, level),
        plating=False,
    )


def target_mordekaiser() -> Target:
    level = 10
    bonus_hp = (
        runes.scaling_hp_shard(level)
        + dorans_ring.DoransRing.hp
        + rylais_crystal_scepter.RylaisCrystalScepter.hp
        + riftmaker.Riftmaker.hp
    )
    return Target(
        name=(
            f"Morde L{level} (HP shard + Doran's Ring + Rylai's + "
            f"Riftmaker + Steelcaps)"
        ),
        max_hp=stat_at_level(MordekaiserStats.hp, level) + bonus_hp,
        bonus_hp=bonus_hp,
        armor=(
            stat_at_level(MordekaiserStats.ar, level)
            + plated_steelcaps.PlatedSteelcaps.armor
        ),
        mr=stat_at_level(MordekaiserStats.mr, level),
        plating=True,
    )


def effective_resists(
    target: Target, build: Build, terminus_dark: int
) -> tuple[float, float]:
    """Target armor/MR after % penetration. Multiple pen sources multiply."""
    armor_pen_ratio = 1.0
    magic_pen_ratio = 1.0
    if build.has_ldr:
        armor_pen_ratio *= (
            1 - lord_dominiks_regards.LordDominiksRegards.armor_pen_pct / 100
        )
    if build.has_terminus:
        dark_ratio = 1 - terminus.dark_pen_pct(terminus_dark) / 100
        armor_pen_ratio *= dark_ratio
        magic_pen_ratio *= dark_ratio
    return target.armor * armor_pen_ratio, target.mr * magic_pen_ratio


def deal(
    state: ComboState,
    target: Target,
    build: Build,
    raw_phys: float,
    raw_magic: float,
    *,
    basic: bool = False,
) -> None:
    """Resolve one damage instance. Only HP actually removed counts as dealt."""
    if basic and target.plating:
        # Steelcaps reduces the basic attack's own damage, never on-hit damage.
        raw_phys = plated_steelcaps.apply_plating(raw_phys)
        raw_magic = plated_steelcaps.apply_plating(raw_magic)
    if build.has_ldr:
        raw_phys = lord_dominiks_regards.apply_giant_slayer(raw_phys, target.bonus_hp)
        raw_magic = lord_dominiks_regards.apply_giant_slayer(raw_magic, target.bonus_hp)
    armor, mr = effective_resists(target, build, state.terminus_dark)
    post = 0.0
    if raw_phys > 0:
        post += post_mitigation_damage(raw_phys, armor)
    if raw_magic > 0:
        post += post_mitigation_damage(raw_magic, mr)
    counted = min(post, state.hp)
    state.dealt += counted
    state.overkill += post - counted
    state.hp -= counted


def apply_on_hit(state: ComboState, target: Target, build: Build) -> None:
    """On-hit effects, resolved before the trigger's own damage."""
    raw_phys = 0.0
    raw_magic = 0.0
    snap_hp = state.hp

    if build.has_bork:
        raw_phys += blade_of_the_ruined_king.mists_edge_damage(snap_hp, is_melee=True)

    if build.has_terminus:
        raw_magic += terminus.Terminus.shadow_onhit_magic

    if build.has_kraken:
        if state.kraken_stacks >= kraken_slayer.KrakenSlayer.bring_it_down_max_stacks:
            missing_pct = (1 - snap_hp / target.max_hp) * 100
            raw_phys += kraken_slayer.bring_it_down_damage(
                KAT_LEVEL, missing_pct, is_melee=True
            )
            state.kraken_stacks = 0
        else:
            state.kraken_stacks += 1

    deal(state, target, build, raw_phys, raw_magic)

    if build.has_terminus:
        # Stack is granted by this on-hit, so its pen applies from the trigger
        # damage onward.
        if not state.terminus_next_light:
            state.terminus_dark = min(
                state.terminus_dark + 1, terminus.Terminus.juxtaposition_max_stacks
            )
        state.terminus_next_light = not state.terminus_next_light


def step_damage(
    step: str, build: Build, conq_stacks: int
) -> tuple[float, float, bool, bool]:
    """(raw_phys, raw_magic, is_basic, applies_on_hit) for one combo step."""
    total_ad, bonus_ad = ads_at_stacks(build.base_bonus_ad, conq_stacks)
    ap = quest_ap(0.0)
    if step == "E":
        return 0.0, shunpo.damage(E_RANK, bonus_ad, ap), False, True
    if step == "AA":
        return total_ad, 0.0, True, True
    if step == "P":
        return 0.0, sinister_steel.damage(KAT_LEVEL, bonus_ad, ap), False, True
    assert step == "Q", f"unknown combo step {step!r}"
    return 0.0, bouncing_blade.damage(Q_RANK, ap), False, False


def simulate(
    build: Build,
    target: Target,
    start_hp_pct: float = 100.0,
) -> ComboResult:
    assert (
        0 < start_hp_pct <= 100
    ), f"start_hp_pct must be in (0, 100], got {start_hp_pct}"
    start_hp = target.max_hp * start_hp_pct / 100
    state = ComboState(hp=start_hp)

    for step_no, step in enumerate(COMBO, start=1):
        raw_phys, raw_magic, basic, applies_on_hit = step_damage(
            step, build, state.conq_stacks
        )
        if applies_on_hit:
            apply_on_hit(state, target, build)
        deal(state, target, build, raw_phys, raw_magic, basic=basic)
        state.steps_used = step_no
        if state.hp <= 0:
            state.killed_on_step = step_no
            break
        state.conq_stacks = min(
            state.conq_stacks + CONQ_STACKS_PER_HIT, conqueror.MAX_STACKS
        )

    return ComboResult(
        build=build.name,
        cost=build.cost,
        start_hp=start_hp,
        dealt=state.dealt,
        overkill=state.overkill,
        hp_left=state.hp,
        steps_used=state.steps_used,
        killed_on_step=state.killed_on_step,
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
        (
            simulate(make_build(name, items), target, start_hp_pct=start_hp_pct)
            for name, items in ITEM_SETS.items()
        ),
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


def main() -> None:
    print(
        f"Kat L{KAT_LEVEL}  Q{Q_RANK} E{E_RANK}  "
        f"Doran's Blade + 1 AF + Conqueror (AD) + midlane quest  |  "
        f"combo {'>'.join(COMBO)} (+{CONQ_STACKS_PER_HIT} conq/hit, melee)"
    )
    targets = (target_viktor(), target_caitlyn(), target_mordekaiser())
    for start_hp_pct in (100.0, 75.0, 40.0):
        for target in targets:
            print_table(target, start_hp_pct=start_hp_pct)


if __name__ == "__main__":
    main()
