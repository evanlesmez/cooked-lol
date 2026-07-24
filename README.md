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
tooling (black, mypy) in the `dev` extra. Drop `[dev]` if you only want to run cooks.

## TODOS: 
Plan better data organization so patches are less confusing
    Store all versions of an item in same file and give it a static patch string member
How to simplify damage combination data calculations
    Maybe write a function for each test combo in cooks
