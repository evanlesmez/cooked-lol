def reduce_cooldown(base_cd: float, haste: int) -> float:
    """
    https://leagueoflegends.fandom.com/wiki/Haste
    """
    return round(base_cd * 100 / (100 + haste), 1)
