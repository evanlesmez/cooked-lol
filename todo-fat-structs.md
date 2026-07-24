# Fat structs refactor

Living plan for moving off per-entity `DataReadOnlyMeta` classes toward C-like const records (Casey / data-oriented style).

## Motivation

**Today**

- One `DataReadOnlyMeta` class per item and per champion stats block
- Fields are ad hoc and sparse (only what that entity defines)
- Proc/passive constants often live on the same class as flat stats
- Class-as-value is freeze-friendly but is not a shared layout

**Target**

- **Struct = shape** (field layout + defaults/zeros)
- **Named consts = values** (`BORK = Item(...)`, `KATARINA = ChampionStats(...)`)
- Logic stays **pure module-level functions** (no methods on data)
- Wide rows for one domain: unused fields are `0` / `None`, not missing attributes

**Explicitly not**

- One god struct for items ∪ champions ∪ runes ∪ abilities
- Full ECS / entity ID space (unless we later build a real combat sim)

## Domain split

| Domain | Struct | Role |
|--------|--------|------|
| Champion base stats | `ChampionStats` | Level curves via `Stat(base, growth)` + flats (`ms`, `base_as`, `windup_pct`, …) |
| Item combat stats | `Item` | Union of stats cooks care about (`cost`, `ad`, `ap`, `hp`, pens, AS%, MS%, crit, …) |
| Uniques / procs | Side data | Effect-specific constants + free functions in the item (or ability) module |

Champions and items do not share lifecycle or access patterns. Keep separate fat structs.

Abilities (e.g. `katarina/death_lotus.py`) already follow the right pattern: module namespace + functions + constants. Leave them alone except where they read champ/item stats.

## Item layout (decided)

**One file per item**, still under `cooked_lol/items/`.

```text
blade_of_the_ruined_king.py
  BORK = Item(cost=3200, ad=40, attack_speed_pct=25, life_steal_pct=10, ...)
  def mists_edge_damage(...): ...
```

- Shared `Item` shape; each file exports a named const (and proc helpers if needed)
- Prefer short export names or keep full names consistently — pick one style at spike time
- Do **not** collapse all items into a single table module for this pass

Champion files similarly:

```text
champions/viktor.py
  VIKTOR = ChampionStats(hp=Stat(600, 100), ...)
```

## What stays the same

- Pure functions for damage, pen, quest amps, mitigation
- `stat_at_level`, `post_mitigation_damage`, midlane quest helpers
- Cook scripts compose builds; they should sum `Item` fields without `getattr(it, "ap", 0)` hacks once layout is uniform
- CLAUDE.md spirit: data-only records, logic free

## Freeze mechanism (open)

Pick one at spike time:

1. **Frozen dataclass** — defaults, `replace`, clear field list
2. **NamedTuple** — truly immutable, no defaults unless defaults factory pattern
3. **Slim meta / instances** — keep read-only enforcement if we still want class-level ergonomics

Preference lean: frozen dataclass for `Item` and `ChampionStats` unless we need stricter freeze than dataclass gives.

`DataReadOnlyMeta` can remain temporarily for non-migrated types, then shrink or die.

## Proc / unique data

Do **not** force every passive into `Item` if it is not a generic stat.

| Pattern | When |
|---------|------|
| Fields on `Item` | Flat stats every build aggregates (AD, AP, HP, % pen, …) |
| Module constants + functions | Unique math (Kraken bring-it-down, Bork mist’s edge, LDR giant slayer, Terminus juxta) |
| Small dedicated struct | Only if several items share the same proc shape later |

## Migration checklist

- [ ] Inventory all current item fields → draft full `Item` field list (zeros as default)
- [ ] Inventory champion stat fields → draft `ChampionStats` (keep `Stat`)
- [ ] Choose freeze mechanism; add types in e.g. `cooked_lol/types/` or `systems/`
- [ ] Spike: convert **one item** + **one champion**; update **one cook** end-to-end
- [ ] Bulk-convert remaining items (one file per item → const `Item`)
- [ ] Bulk-convert remaining champion stats blocks
- [ ] Move proc constants off stat rows into effect helpers where still mixed
- [ ] Replace `getattr(it, "ad", 0)`-style access in cooks with uniform field reads
- [ ] Remove per-entity `DataReadOnlyMeta` classes for migrated data
- [ ] Update `CLAUDE.md` for the new convention
- [ ] Smoke-run AP cook + AD on-hit cook

## Non-goals (this pass)

- Patch/version strings on every datum (README TODO — separate)
- Runtime inventory / shop sim
- Graphing / UI changes
- Merging runes into `Item` or `ChampionStats`

## Success criteria

- Adding a new item = one file, one `Item(...)` const, optional proc functions
- Cooks can loop items and sum stats without special cases for missing attributes
- No methods on data records
- Clear split: champion layout vs item layout vs effect code
