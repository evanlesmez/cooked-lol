# Cooked League of Legends

A place to analyze data about champions to come up with strategies and build ideas.  
Only data source currently is https://lolwiki.com  

<img width="640" height="360" alt="cooking-irelia" src="https://github.com/user-attachments/assets/fb224b6f-acbd-49a2-a999-07ed8c0a90a4" />

Future sources:
- https://www.communitydragon.org/  
- [lolalytics](https://lolalytics.com/lol) for global game data statistics.  
- [Riot API](https://developer.riotgames.com/apis)  


## Quickstart

```sh
python3 -m venv env
source env/bin/activate
pip install -e ".[dev]"
```

Dependencies live in `pyproject.toml`: runtime in `[project].dependencies`,
tooling (black, pyright) in the `dev` extra. Drop `[dev]` if you only want to run cooks.

```sh
env/bin/black cooked_lol cooks   # format
env/bin/pyright                  # type check, must stay at 0 errors
```

There are no tests. The regression check is cook stdout — capture it before a
refactor and diff it after:

```sh
python cooks/s16/katarina_ad_onhit_2item.py > /tmp/before.txt
```

## Cooks

Cooks print tables to stdout and take `--plot` to also write charts. Plotting is
off by default because matplotlib costs ~230ms to import and most runs only want
the tables.

```sh
python cooks/s16/katarina_ad_onhit_2item.py           # tables only
python cooks/s16/katarina_ad_onhit_3item.py --plot    # tables + charts
```

Charts land in `cooks/assets/` via `cooks.config.asset_path`; use that for any new
cook rather than writing next to the script. The chart path is printed to stderr so
stdout stays a clean regression baseline.

Shared cook code lives at the top of `cooks/`:

- `cooks/combo_sim.py` — on-hit combo engine (targets, builds, on-hit
  ordering, mitigation, overkill). Steps resolve to one or more `Hit`s, so a
  channel like Death Lotus can be 15 daggers that each apply on-hit effects.

## Data layout

Items and champions are fat frozen structs: one file per entity exporting a single
const (`ITEM` for items, `STATS` for champions) built from the shared shapes in
`cooked_lol/types/`. Unique passives are UPPER_SNAKE module constants plus free
functions in the same module. See `CLAUDE.md`.

## TODOS: 
- Plan better data organization so patches are less confusing  
  - Store all versions of an item in same file and give it a static patch string member
- How to simplify damage combination data calculations?

