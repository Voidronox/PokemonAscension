import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable
from core.database import MOVES

def damage_calc(lvl, mon_atk, mon_sp_atk, def_def, def_sp_def, move, status=1, stat=1, stab=1, ability=1, crit_rate=1):
    move_data = MOVES.get(move.lower())
    bp = move_data.get("power")
    category = move_data.get("category")

    is_crit = False
    if crit_rate == 1:
        is_crit = random.random() < (1/24)
    elif crit_rate == 2:
        is_crit = random.random() < (1/8)
    elif crit_rate == 3:
        is_crit = random.random() < (1/2)

    if is_crit and stat < 0:
        statmod = 1
    else:
        if stat >= 0:
            statmod = (2 + stat) / 2
        else:
            statmod = 2 / (2 - stat)

    if category == "status" or bp == 0 or bp is None:
        return 0
    elif category == "physical":
        atk = mon_atk
        opp_def = def_def
    elif category == "special":
        atk = mon_sp_atk
        opp_def = def_sp_def

    crit = 1.5 if is_crit else 1.0
    rand_variance = random.uniform(0.85, 1.00)

    return int(((((2 * lvl / 5) + 2) * (atk / opp_def) * (bp / 50)) + 2) * status * stab * statmod * ability * crit * rand_variance)