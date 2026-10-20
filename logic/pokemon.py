from dataclasses import dataclass, field
from math import floor
from core.database import POKEMON
import random

NATURES = {  # name: (boosted, lowered)
    "Hardy": None, "Docile": None, "Serious": None, "Bashful": None, "Quirky": None,
    "Lonely": ("atk", "def"), "Brave": ("atk", "speed"), "Adamant": ("atk", "sp_atk"), "Naughty": ("atk", "sp_def"),
    "Bold": ("def", "atk"), "Relaxed": ("def", "speed"), "Impish": ("def", "sp_atk"), "Lax": ("def", "sp_def"),
    "Timid": ("speed", "atk"), "Hasty": ("speed", "def"), "Jolly": ("speed", "sp_atk"), "Naive": ("speed", "sp_def"),
    "Modest": ("sp_atk", "atk"), "Mild": ("sp_atk", "def"), "Quiet": ("sp_atk", "speed"), "Rash": ("sp_atk", "sp_def"),
    "Calm": ("sp_def", "atk"), "Gentle": ("sp_def", "def"), "Sassy": ("sp_def", "speed"), "Careful": ("sp_def", "sp_atk"),
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

SHINY_ODDS = 4096

@dataclass
class Pokemon:
    species: str
    level: int
    nature: str
    max_hp: int
    hp: int
    atk: int
    defense: int
    sp_atk: int
    sp_def: int
    speed: int
    ability: str = ""
    moves: list[str] = field(default_factory=list)
    shiny: bool = False

def create_pokemon(species, level, nature="Hardy", iv=31):
    base = POKEMON[species.lower()]["base_stats"]   # adjust to your JSON
    hp = calc_hp(base["hp"], level, iv)
    stats = {s: calc_stat(base[s], level, iv, 0, nature_mult(nature, s))
             for s in ("atk", "def", "sp_atk", "sp_def", "speed")}
    return Pokemon(species, level, nature, hp, hp,
                   stats["atk"], stats["def"], stats["sp_atk"], stats["sp_def"], stats["speed"])

def spawn_wild(species, level, shiny=None):
    mon = create_pokemon(species, level, nature=random.choice(list(NATURES)), iv=random.randint(0, 31))
    if shiny is None:
        mon.shiny = random.randrange(SHINY_ODDS) == 0
    else:
        mon.shiny = shiny
    return mon

if __name__ == "__main__":
    name = input("Enter Pokemon name here: ")
    lvl = int(input("Enter Pokemon level here: "))
    print(spawn_wild(name, lvl, None))