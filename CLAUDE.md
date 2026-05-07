# cooked-lol conventions

## Dataclasses are data-only; logic lives in pure module-level functions

- `@dataclass(frozen=True)` holds **only fields** — no methods.
- Expose a default singleton at module scope (e.g. `LICHBANE = LichBane()`).
  Constructing `LichBane()` directly works too; the singleton is convenience
  + a canonical import. Tweaked variants like `LichBane(spellblade_ap_ratio=0.45)`
  stay possible.
- Damage / scaling formulas are **pure module-level functions** that take the
  dataclass instance as the first argument.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Foo:
    a: float = 1.0
    b: float = 2.0


FOO = Foo()


def some_calc(item: Foo, x: float) -> float:
    return item.a * x + item.b
```

When touching a module that violates this (method on a dataclass), strip the
method into a free function as part of the change.
