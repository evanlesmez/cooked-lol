"""Shared chart rendering for combo cooks.

Matplotlib is imported lazily inside the plotting entry point: cooks default to
not plotting, and the import costs a couple hundred milliseconds.
"""

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from cooks.combo_sim import ComboResult, HitLog, Target

if TYPE_CHECKING:
    from matplotlib.axes import Axes

# Kill markers sit in a gutter below the axis rather than on y=0, because every
# killing build lands on exactly 0 HP and the markers would hide each other.
# They are also dodged sideways so builds that kill on the same step stay legible.
KILL_GUTTER_Y = -3.4
KILL_DODGE = 0.17

RunFn = Callable[[str, Target, float], ComboResult]


def plot_panel(
    ax: "Axes",
    target: Target,
    start_hp_pct: float,
    build_names: Sequence[str],
    build_colors: Mapping[str, str],
    run: RunFn,
) -> None:
    """One HP-depletion panel: a line per build over the combo steps."""
    for idx, name in enumerate(build_names):
        result = run(name, target, start_hp_pct)
        curve_pct = [hp / result.start_hp * 100 for hp in result.hp_curve]
        ax.plot(
            range(len(curve_pct)),
            curve_pct,
            color=build_colors[name],
            marker="o",
            markersize=3.5,
            linewidth=1.7,
            label=name,
            zorder=2,
        )
        if result.killed_on_step is not None:
            dodge = (idx - (len(build_names) - 1) / 2) * KILL_DODGE
            ax.plot(
                result.killed_on_step + dodge,
                KILL_GUTTER_Y,
                marker="X",
                markersize=9,
                color=build_colors[name],
                markeredgecolor="black",
                markeredgewidth=0.6,
                clip_on=False,
                zorder=3,
            )
    ax.axhline(0, color="black", linestyle="--", linewidth=0.9, zorder=1)
    ax.grid(True, alpha=0.3, linewidth=0.5)


def plot_trajectory_grid(
    *,
    targets: Sequence[Target],
    start_hp_pcts: Sequence[float],
    build_names: Sequence[str],
    build_colors: Mapping[str, str],
    run: RunFn,
    combo: Sequence[str],
    title: str,
    out: Path,
) -> Path:
    """Grid of HP-depletion panels: rows are targets, columns start-HP checkpoints."""
    assert set(build_names) <= set(build_colors), (
        "every build needs a colour, missing: "
        f"{set(build_names) - set(build_colors)}"
    )

    # Imported lazily: matplotlib costs ~230ms and only --plot runs need it.
    import matplotlib

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(
        len(targets),
        len(start_hp_pcts),
        figsize=(5.0 * len(start_hp_pcts), 3.2 * len(targets) + 1.4),
        sharex=True,
        sharey=True,
        squeeze=False,
    )
    for row, target in enumerate(targets):
        for col, start_hp_pct in enumerate(start_hp_pcts):
            ax: "Axes" = axes[row][col]
            plot_panel(ax, target, start_hp_pct, build_names, build_colors, run)
            if row == 0:
                ax.set_title(f"@ {start_hp_pct:g}% HP", fontsize=12)
            if col == 0:
                ax.set_ylabel(target.short, fontsize=12, fontweight="bold")

    # Shared axes, so configuring one configures all of them.
    axes[0][0].set_xticks(range(len(combo) + 1))
    axes[0][0].set_xticklabels(("start", *combo))
    axes[0][0].set_ylim(-6, 105)

    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(
        handles, labels, loc="lower center", ncol=len(build_names), frameon=False
    )
    fig.supylabel("Target HP remaining (% of start HP)")
    fig.supxlabel("Combo step", y=0.055)
    fig.suptitle(title, fontsize=14)
    fig.tight_layout(rect=(0.015, 0.05, 1, 0.97))

    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


TickRunFn = Callable[[str, Target], ComboResult]


def _step_hits(result: ComboResult, step_no: int) -> list[HitLog]:
    return [h for h in result.hits if h.step_no == step_no]


def plot_hit_ticks(
    *,
    targets: Sequence[Target],
    build_names: Sequence[str],
    run: TickRunFn,
    step_no: int,
    step_label: str,
    source_order: Sequence[str],
    source_colors: Mapping[str, str],
    title: str,
    out: Path,
) -> Path:
    """Zoom into one multi-hit step: stacked per-tick damage plus the HP curve.

    Rows are targets, columns builds. Each bar is one tick of the step, split by
    damage source, with target HP% overlaid on a right-hand axis. This is what
    makes a channel legible: Kraken spikes every third tick and Bork decays as the
    target's current HP falls, neither of which is visible when the whole step
    collapses into a single point on a trajectory chart.
    """
    assert set(source_order) <= set(source_colors), (
        "every source needs a colour, missing: "
        f"{set(source_order) - set(source_colors)}"
    )

    import matplotlib

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(
        len(targets),
        len(build_names),
        figsize=(6.4 * len(build_names), 3.3 * len(targets) + 1.6),
        sharex=True,
        squeeze=False,
    )

    hp_handles: list = []
    for row, target in enumerate(targets):
        for col, build_name in enumerate(build_names):
            ax: "Axes" = axes[row][col]
            result = run(build_name, target)
            hits = _step_hits(result, step_no)
            xs = list(range(1, len(hits) + 1))

            bottoms = [0.0] * len(hits)
            for source in source_order:
                values = [dict(h.components).get(source, 0.0) for h in hits]
                if not any(values):
                    continue
                ax.bar(
                    xs,
                    values,
                    bottom=bottoms,
                    color=source_colors[source],
                    label=source if (row == 0 and col == 0) else None,
                    width=0.78,
                    zorder=2,
                )
                bottoms = [b + v for b, v in zip(bottoms, values)]

            ax.set_axisbelow(True)
            ax.grid(True, axis="y", alpha=0.3, linewidth=0.5)
            if row == 0:
                ax.set_title(build_name, fontsize=12)
            if col == 0:
                ax.set_ylabel(f"{target.short}\npost-mit damage", fontsize=10)

            hp_pct = [h.hp_after / result.start_hp * 100 for h in hits]
            ax2 = ax.twinx()
            (hp_line,) = ax2.plot(
                xs,
                hp_pct,
                color="black",
                linewidth=1.6,
                marker="o",
                markersize=3.2,
                label="target HP %",
                zorder=3,
            )
            if row == 0 and col == 0:
                hp_handles.append(hp_line)
            ax2.set_ylim(0, 105)
            ax2.set_ylabel("HP left (%)", fontsize=9)
            if result.killed_on_step == step_no:
                ax2.annotate(
                    f"dead on tick {len(hits)}",
                    xy=(1.0, 1.0),
                    xycoords="axes fraction",
                    xytext=(-6, -8),
                    textcoords="offset points",
                    ha="right",
                    va="top",
                    fontsize=9,
                    fontweight="bold",
                    bbox={
                        "boxstyle": "round,pad=0.25",
                        "facecolor": "white",
                        "edgecolor": "0.6",
                        "linewidth": 0.6,
                    },
                )

    bar_handles, bar_labels = axes[0][0].get_legend_handles_labels()
    fig.legend(
        [*bar_handles, *hp_handles],
        [*bar_labels, *(h.get_label() for h in hp_handles)],
        loc="lower center",
        ncol=len(bar_labels) + len(hp_handles),
        frameon=False,
    )
    fig.supxlabel(f"{step_label} tick", y=0.055)
    fig.suptitle(title, fontsize=14)
    fig.tight_layout(rect=(0, 0.05, 1, 0.96))

    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out
