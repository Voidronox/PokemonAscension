from dataclasses import dataclass, field
from core.database import POKEMON
from math import floor

@dataclass
class Pokemon:
    species: str
    level: int
    max_hp: int
    hp: int
    stages: dict = field(default_factory=lambda: {
        "atk": 0, "def": 0, "spa": 0, "spd": 0, "spe": 0})

def calc_hp(base, level, iv=31, ev=0):
    return floor((2 * base + iv + ev // 4) * level / 100) + level + 10

def calc_stat(base, level, iv=31, ev=0, nature=1.0):
    return floor((floor((2 * base + iv + ev // 4) * level / 100) + 5) * nature)

def create_pokemon(species, level, iv, nature):
    base = POKEMON[species]
    hp = calc_hp(base, level, iv, 0)
    atk = calc_stat(base, level, iv, 0, nature)
    defense = calc_stat(base, level, iv, 0, nature)
    sp_atk = calc_stat(base, level, iv, 0, nature)
    sp_def = calc_stat(base, level, iv, 0, nature)
    spe = calc_stat(base, level, iv, 0, nature)
    return Pokemon(species, level, hp, atk, defense, sp_atk, sp_def, spe)
