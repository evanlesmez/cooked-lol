from dataclasses import dataclass


@dataclass(frozen=True)
class VoidStaff:
    cost: int = 3000
    ap: int = 95
    magic_pen_pct: float = 40


VOID_STAFF = VoidStaff()
