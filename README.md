# Cooked League of Legends

A place to analyze data about champions to come up with strategies and build ideas.  
Only data source currently is https://lolwiki.com  

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

## Data layout

Items and champions are fat frozen structs: one file per entity exporting a single
const (`ITEM` for items, `STATS` for champions) built from the shared shapes in
`cooked_lol/types/`. Unique passives are UPPER_SNAKE module constants plus free
functions in the same module. See `CLAUDE.md`.

## TODOS: 
Plan better data organization so patches are less confusing
    Store all versions of an item in same file and give it a static patch string member
How to simplify damage combination data calculations
    Maybe write a function for each test combo in cooks
