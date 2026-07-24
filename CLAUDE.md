# cooked-lol conventions

## Data is fat structs: frozen records, logic in pure module-level functions

Two shared shapes live in `cooked_lol/types/`:

- `Item` (`types/item.py`) — union of flat stats every build aggregates
- `ChampionStats` (`types/champion_stats.py`) — `Stat(base, growth)` curves + flat stats

Both are `@dataclass(frozen=True, slots=True, kw_only=True)`. Fields an entity does
not grant are `0`, never missing, so cooks can sum any field across a build without
`getattr(it, "ad", 0)` probing.

One file per entity, module name is the namespace, exporting a single const:

```python
# cooked_lol/items/kraken_slayer.py
ITEM = Item(name="Kraken Slayer", cost=3000, ad=45, attack_speed_pct=40.0)

# cooked_lol/champions/viktor.py
STATS = ChampionStats(name="Viktor", melee=False, hp=Stat(600, 100), ...)
```

Never put a method on a data record. When touching a module that violates this,
strip the method into a free function as part of the change.

## Unique passives are module constants, not `Item` fields

`Item` only carries generic stats. Effect-specific numbers become UPPER_SNAKE
module constants next to the free functions that consume them, keeping the
effect-name prefix (an item can have two passives):

```python
BRING_IT_DOWN_MAX_STACKS = 2
BRING_IT_DOWN_BASE_L1 = 150.0

def bring_it_down_damage(level: int, target_missing_hp_pct: float) -> float: ...
```

Only introduce a dedicated struct if several items end up sharing a proc shape.

## Prefer `assert` over silent clamp for invalid inputs

Caller bugs (bad rank, stacks, channel time, missing-HP%, ...) should fail loud with
`assert`, not be hidden by `min`/`max` clamping.

Keep `min`/`max` only where the bound is a real game rule rather than a caller
mistake — e.g. Riftmaker stacks capping after 4s in combat, Liandry's monster tick
cap, or a cooldown flooring at 0.

## Tooling

```sh
env/bin/black cooked_lol cooks   # format
env/bin/pyright                  # type check, must stay at 0 errors
```

There are no tests. The regression check is the stdout of the cooks in `cooks/`:
capture it before a refactor and diff it after.
