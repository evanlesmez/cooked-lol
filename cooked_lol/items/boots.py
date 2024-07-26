class BerserkersGreaves:
    attack_speed = 0.35
    move_speed = 45
    gold = 1100


class SorcerersShoes:
    magic_pen = 18
    move_speed = 45
    gold = 1100


class LucidityBoots:
    haste = 15
    move_speed = 45
    summoner_spell_haste = 12
    gold = 900


class MercurysTreads:
    mr = 25
    move_speed = 45
    tenacity = 0.30
    gold = 1100


class PlatedSteelcaps:
    armor = 25
    move_speed = 45
    gold = 1000

    @staticmethod
    def plating(basic_attack_dmg: float) -> float:
        return basic_attack_dmg * 0.92


class SwiftyBoots:
    move_speed = 60
    slow_resist = 0.25
    gold = 900
