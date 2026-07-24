"""Shared cook output configuration.

Cooks write their charts into a single assets directory rather than next to the
script, so generated images stay in one place.
"""

from pathlib import Path

COOKS_DIR = Path(__file__).resolve().parent
ASSETS_DIR = COOKS_DIR / "assets"


def asset_path(name: str) -> Path:
    """Absolute path for a generated chart, creating the assets dir if needed.

    `name` is a bare stem; the .png suffix is added here so every cook agrees on
    the format.
    """
    assert not name.endswith(".png"), f"pass a bare stem, not a filename: {name!r}"
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    return ASSETS_DIR / f"{name}.png"
