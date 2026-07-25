"""on-hit combo simulator.

Damage is tracked against the target's actual HP pool: a combo stops at the hit
that kills, and damage past 0 HP is reported as overkill instead of being counted
as damage dealt.

A combo is a sequence of steps; a step resolves as one or more `Hit`s. Most steps
are a single hit, but Death Lotus (R) is a channel of many daggers that each
apply on-hit effects at reduced effectiveness, so steps are modelled as hit
lists rather than single damage instances.

On-hit effects resolve before the trigger's own damage, so Mist's Edge and Bring
It Down read the target's HP from before that hit.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import NamedTuple

from cooked_lol.items import (
    blade_of_the_ruined_king,
    kraken_slayer,
    lord_dominiks_regards,
    plated_steelcaps,
    terminus,
)
from cooked_lol.runes import conqueror, runes
from cooked_lol.systems.systems import post_mitigation_damage
from cooked_lol.types.item import Item


class Target(NamedTuple):
    name: str
    short: str  # chart row label
    max_hp: float
    bonus_hp: float
    armor: float
    mr: float
    plating: bool


class Build(NamedTuple):
    """Which on-hit items are in, plus Kat's flat bonus AD and bonus AS."""

    name: str
    cost: int
    base_bonus_ad: float
    bonus_as_pct: float
    has_kraken: bool
    has_bork: bool
    has_ldr: bool
    has_terminus: bool


# Damage-source labels used for per-hit attribution in charts. Bork's Mist's Edge
# and Kraken's Bring It Down are physical; Terminus' Shadow is magic.
SOURCE_BORK = "Bork Mist's Edge"
SOURCE_TERMINUS = "Terminus Shadow"
SOURCE_KRAKEN = "Kraken Bring It Down"


def physical_label(label: str) -> str:
    return f"{label} (physical)"


def magic_label(label: str) -> str:
    return f"{label} (magic)"


class Hit(NamedTuple):
    """One damage instance inside a combo step."""

    raw_physical: float = 0.0
    raw_magic: float = 0.0
    is_basic_attack: bool = False
    # 0.0 means the hit applies no on-hit effects at all; 1.0 is full
    # effectiveness. Death Lotus daggers land somewhere in between.
    onhit_effectiveness: float = 0.0
    # Attribution label for the hit's own damage, e.g. "R dagger".
    label: str = "ability"


class HitLog(NamedTuple):
    """Per-hit record used for charting; does not affect the simulation."""

    step_no: int  # 1-based index into the combo
    hit_no: int  # 1-based index within the step
    components: tuple[tuple[str, float], ...]  # (source, post-mit before clamp)
    hp_after: float


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
    # HP remaining at each step boundary, starting with the pre-combo value.
    curve: list[float] = field(default_factory=list)
    hits: list[HitLog] = field(default_factory=list)


class ComboResult(NamedTuple):
    build: str
    cost: int
    start_hp: float
    dealt: float  # post-mitigation damage that actually removed HP
    overkill: float  # post-mitigation damage past 0 HP
    hp_left: float
    steps_used: int
    killed_on_step: int | None
    # start_hp followed by HP after each resolved step, so it is len(combo) + 1
    # long unless the combo ended early on a kill.
    hp_curve: tuple[float, ...]
    # One entry per resolved hit, for per-tick charts of multi-hit steps.
    hits: tuple[HitLog, ...]


def rank_key(result: ComboResult) -> tuple[int, int, float, float]:
    """Sort key, best first under `reverse=True`.

    Kills first, then fewest steps, then most headroom, then most damage.

    `overkill` deliberately outranks `dealt`: on a kill every build has dealt
    exactly the target's starting HP, so `dealt` carries no information and its
    float-accumulation noise (~1e-12) would otherwise decide the order. On a
    survival `overkill` is zero for everyone, so `dealt` breaks the tie instead.
    """
    killed = result.killed_on_step is not None
    return int(killed), -result.steps_used, result.overkill, result.dealt


def make_target(
    *,
    short: str,
    detail: str,
    level: int,
    base_hp: float,
    base_ar: float,
    base_mr: float,
    items: tuple[Item, ...] = (),
) -> Target:
    """Build a Target by summing the item fields the target actually carries.

    Every target is assumed to run the scaling health shard, so bonus HP is never
    zero. Keeping this in one place is deliberate: hand-rolling each target is how
    the cooks previously drifted into three different Caitlyns.
    """
    bonus_hp = runes.scaling_hp_shard(level) + sum(it.hp for it in items)
    return Target(
        name=f"{short} ({detail})",
        short=short,
        max_hp=base_hp + bonus_hp,
        bonus_hp=bonus_hp,
        armor=base_ar + sum(it.armor for it in items),
        mr=base_mr + sum(it.mr for it in items),
        plating=plated_steelcaps.ITEM in items,
    )


def make_build(
    name: str,
    items: tuple[Item, ...],
    *,
    starter_bonus_ad: float,
    shard_bonus_ad: float,
    starter_cost: int,
    champion_bonus_as_pct: float,
) -> Build:
    return Build(
        name=name,
        cost=starter_cost + sum(it.cost for it in items),
        base_bonus_ad=starter_bonus_ad + shard_bonus_ad + sum(it.ad for it in items),
        bonus_as_pct=champion_bonus_as_pct + sum(it.attack_speed_pct for it in items),
        has_kraken=kraken_slayer.ITEM in items,
        has_bork=blade_of_the_ruined_king.ITEM in items,
        has_ldr=lord_dominiks_regards.ITEM in items,
        has_terminus=terminus.ITEM in items,
    )


def effective_resists(
    target: Target, build: Build, terminus_dark: int
) -> tuple[float, float]:
    """Target armor/MR after % penetration. Multiple pen sources multiply."""
    armor_pen_ratio = 1.0
    magic_pen_ratio = 1.0
    if build.has_ldr:
        armor_pen_ratio *= 1 - lord_dominiks_regards.ITEM.armor_pen_pct / 100
    if build.has_terminus:
        dark_ratio = 1 - terminus.dark_pen_pct(terminus_dark) / 100
        armor_pen_ratio *= dark_ratio
        magic_pen_ratio *= dark_ratio
    return target.armor * armor_pen_ratio, target.mr * magic_pen_ratio


def mitigated_damage(
    state: ComboState,
    target: Target,
    build: Build,
    raw_phys: float,
    raw_magic: float,
    *,
    basic: bool = False,
) -> float:
    """Post-mitigation damage of one instance, before clamping to remaining HP.

    Mitigation is linear in raw damage, so callers can mitigate a combined
    instance or its individual sources and get the same total. That is what makes
    the per-source attribution in `apply_on_hit` exact rather than an estimate.
    """
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
    return post


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
    post = mitigated_damage(state, target, build, raw_phys, raw_magic, basic=basic)
    counted = min(post, state.hp)
    state.dealt += counted
    state.overkill += post - counted
    state.hp -= counted


def apply_on_hit(
    state: ComboState,
    target: Target,
    build: Build,
    level: int,
    is_melee: bool,
    effectiveness: float = 1.0,
) -> list[tuple[str, float]]:
    """On-hit effects, resolved before the trigger's own damage.

    `effectiveness` scales on-hit damage (Death Lotus applies on-hits at reduced
    effectiveness). Stack bookkeeping is unaffected: a reduced-effectiveness hit
    still counts as a proc for Kraken and Terminus.

    Returns the per-source post-mitigation contributions for charting. The sources
    are still dealt as one combined instance, so overkill accounting is unchanged.
    """
    assert effectiveness > 0, f"on-hit effectiveness must be > 0, got {effectiveness}"
    phys: list[tuple[str, float]] = []
    magic: list[tuple[str, float]] = []
    snap_hp = state.hp

    if build.has_bork:
        phys.append(
            (
                SOURCE_BORK,
                blade_of_the_ruined_king.mists_edge_damage(snap_hp, is_melee=is_melee)
                * effectiveness,
            )
        )

    if build.has_terminus:
        magic.append((SOURCE_TERMINUS, terminus.SHADOW_ONHIT_MAGIC * effectiveness))

    if build.has_kraken:
        if state.kraken_stacks >= kraken_slayer.BRING_IT_DOWN_MAX_STACKS:
            missing_pct = (1 - snap_hp / target.max_hp) * 100
            phys.append(
                (
                    SOURCE_KRAKEN,
                    kraken_slayer.bring_it_down_damage(
                        level, missing_pct, is_melee=is_melee
                    )
                    * effectiveness,
                )
            )
            state.kraken_stacks = 0
        else:
            state.kraken_stacks += 1

    components = [
        (src, mitigated_damage(state, target, build, raw, 0.0)) for src, raw in phys
    ] + [(src, mitigated_damage(state, target, build, 0.0, raw)) for src, raw in magic]

    deal(
        state,
        target,
        build,
        sum(raw for _, raw in phys),
        sum(raw for _, raw in magic),
    )

    if build.has_terminus:
        # Stack is granted by this on-hit, so its pen applies from the trigger
        # damage onward.
        if not state.terminus_next_light:
            state.terminus_dark = min(
                state.terminus_dark + 1, terminus.JUXTAPOSITION_MAX_STACKS
            )
        state.terminus_next_light = not state.terminus_next_light

    return components


def simulate(
    build: Build,
    target: Target,
    combo: tuple[str, ...],
    resolve_step: Callable[[str, Build, int], tuple[Hit, ...]],
    *,
    level: int,
    is_melee: bool,
    conq_stacks_per_step: int,
    start_hp_pct: float = 100.0,
) -> ComboResult:
    """Run a combo, resolving each step's hits as it goes.

    `resolve_step(step, build, conq_stacks)` is called per step rather than up
    front because damage formulas depend on Conqueror stacks, which ramp as the
    combo runs and so are only known mid-simulation.
    """
    assert (
        0 < start_hp_pct <= 100
    ), f"start_hp_pct must be in (0, 100], got {start_hp_pct}"
    start_hp = target.max_hp * start_hp_pct / 100
    state = ComboState(hp=start_hp, curve=[start_hp])

    for step_no, step in enumerate(combo, start=1):
        for hit_no, hit in enumerate(resolve_step(step, build, state.conq_stacks), 1):
            components: list[tuple[str, float]] = []
            if hit.onhit_effectiveness:
                components += apply_on_hit(
                    state,
                    target,
                    build,
                    level=level,
                    is_melee=is_melee,
                    effectiveness=hit.onhit_effectiveness,
                )
            # Logged as two components so charts can separate the damage types.
            # Mitigation is linear, so splitting does not change the total.
            own_phys = mitigated_damage(
                state, target, build, hit.raw_physical, 0.0, basic=hit.is_basic_attack
            )
            own_magic = mitigated_damage(
                state, target, build, 0.0, hit.raw_magic, basic=hit.is_basic_attack
            )
            if own_phys > 0:
                components.append((physical_label(hit.label), own_phys))
            if own_magic > 0:
                components.append((magic_label(hit.label), own_magic))
            deal(
                state,
                target,
                build,
                hit.raw_physical,
                hit.raw_magic,
                basic=hit.is_basic_attack,
            )
            state.hits.append(
                HitLog(step_no, hit_no, tuple(components), max(state.hp, 0.0))
            )
            if state.hp <= 0:
                break
        state.steps_used = step_no
        state.curve.append(state.hp)
        if state.hp <= 0:
            state.killed_on_step = step_no
            break
        state.conq_stacks = min(
            state.conq_stacks + conq_stacks_per_step, conqueror.MAX_STACKS
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
        hp_curve=tuple(state.curve),
        hits=tuple(state.hits),
    )
