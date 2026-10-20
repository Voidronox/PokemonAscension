import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable
from core.database import MOVES
from data.type_chart import TYPE_CHART, get_effectiveness, dual_effectiveness

CRIT_CHANCE = [1/24, 1/8, 1/2, 1.0]

def stage_mult(n):
    return (2 + n) / 2 if n >= 0 else 2 / (2 - n)

def damage_calc(lvl, mon_atk, mon_sp_atk, def_def, def_sp_def, move,
                atk_stage=0, def_stage=0, stab=1, effectiveness=1,
                status=1, ability=1, crit_stage=0):
    move_data = MOVES[move.lower()]          # KeyError if the move is missing
    bp = move_data.get("power")
    category = move_data.get("category")
    if not bp or category not in ("physical", "special"):
        return 0, False
    if effectiveness == 0:
        return 0, False

    if category == "physical":
        atk, opp_def = mon_atk, def_def
    else:
        atk, opp_def = mon_sp_atk, def_sp_def

    is_crit = random.random() < CRIT_CHANCE[min(crit_stage, 3)]
    if is_crit:
        atk_stage = max(0, atk_stage)
        def_stage = min(0, def_stage)
    atk *= stage_mult(atk_stage)
    opp_def *= stage_mult(def_stage)

    dmg = ((2 * lvl / 5 + 2) * bp * atk / opp_def) / 50 + 2
    dmg *= (1.5 if is_crit else 1) * random.randint(85, 100) / 100
    dmg *= stab * effectiveness * status * ability
    return max(1, int(dmg)), is_crit
