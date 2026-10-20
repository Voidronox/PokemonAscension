from dataclasses import dataclass
from math import floor
from core.database import POKEMON

NATURES = {  # name: (boosted, lowered)
    "Hardy": None, "Docile": None, "Serious": None, "Bashful": None, "Quirky": None,
    "Lonely": ("atk", "def"), "Brave": ("atk", "spe"), "Adamant": ("atk", "spa"), "Naughty": ("atk", "spd"),
    "Bold": ("def", "atk"), "Relaxed": ("def", "spe"), "Impish": ("def", "spa"), "Lax": ("def", "spd"),
    "Timid": ("spe", "atk"), "Hasty": ("spe", "def"), "Jolly": ("spe", "spa"), "Naive": ("spe", "spd"),
    "Modest": ("spa", "atk"), "Mild": ("spa", "def"), "Quiet": ("spa", "spe"), "Rash": ("spa", "spd"),
    "Calm": ("spd", "atk"), "Gentle": ("spd", "def"), "Sassy": ("spd", "spe"), "Careful": ("spd", "spa"),
}

def nature_mult(nature, stat):
    effect = NATURES[nature]
    if effect is None:
        return 1.0
    if stat == effect[0]:
        return 1.1
    if stat == effect[1]:
        return 0.9
    return 1.0

def calc_hp(base, level, iv=31, ev=0):
    return floor((2 * base + iv + ev // 4) * level / 100) + level + 10

def calc_stat(base, level, iv=31, ev=0, nature=1.0):
    return floor((floor((2 * base + iv + ev // 4) * level / 100) + 5) * nature)

@dataclass
class Pokemon:
    species: str
    level: int
    nature: str
    max_hp: int
    hp: int
    atk: int
    defense: int
    spa: int
    spd: int
    spe: int

def create_pokemon(species, level, nature="Hardy", iv=31):
    base = POKEMON[species]["base_stats"]   # adjust to your JSON
    hp = calc_hp(base["hp"], level, iv)
    stats = {s: calc_stat(base[s], level, iv, 0, nature_mult(nature, s))
             for s in ("atk", "def", "spa", "spd", "spe")}
    return Pokemon(species, level, nature, hp, hp,
                   stats["atk"], stats["def"], stats["spa"], stats["spd"], stats["spe"])