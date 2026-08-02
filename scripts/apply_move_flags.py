"""
Applies gameplay-mechanic flags to moves already in data/moves.json.

Unlike generate_pokedex.py, this doesn't hit an API — PokeAPI doesn't expose
"bypasses protect" or "semi-invulnerable turn" as clean fields, so this is a
curated list based on known move mechanics instead.

Only moves that need a flags block get one; everything else is left as-is
(battle_engine.py should treat a missing flags key as all-false/0 via
move.get("flags", {}).get("some_flag", False)).

This list is a solid starting point, not guaranteed exhaustive — review it
and add anything specific to your dex (e.g. custom moves) by hand.

Usage: python scripts/apply_move_flags.py
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MOVES_FILE = DATA_DIR / "moves.json"

# Two-turn "vanish then strike" moves — invulnerable on the charge turn.
SEMI_INVULNERABLE = {
    "fly": False,
    "dig": False,
    "dive": False,
    "bounce": False,
    "sky_drop": False,
    "phantom_force": True,   # True = also bypasses Protect/Detect
    "shadow_force": True,
}

# Two-turn charge moves that are NOT semi-invulnerable (user is still
# hittable on the charge turn — e.g. Solar Beam in bad weather).
CHARGE_ONLY = [
    "solar_beam",
    "skull_bash",
    "sky_attack",
    "razor_wind",
    "geomancy",
    "electro_shot",
]

# Moves that bypass Protect/Detect but aren't two-turn moves themselves.
BYPASSES_PROTECT_ONLY = [
    "feint",
]

# Multi-hit moves (2-5 hits unless noted) — useful for damage calc later.
MULTI_HIT = {
    "double_slap": (2, 5),
    "comet_punch": (2, 5),
    "fury_attack": (2, 5),
    "pin_missile": (2, 5),
    "spike_cannon": (2, 5),
    "fury_swipes": (2, 5),
    "bone_rush": (2, 5),
    "icicle_spear": (2, 5),
    "rock_blast": (2, 5),
    "bullet_seed": (2, 5),
    "double_kick": (2, 2),
    "double_hit": (2, 2),
    "twineedle": (2, 2),
    "dual_chop": (2, 2),
    "dragon_darts": (2, 2),
    "population_bomb": (1, 10),
    "water_shuriken": (2, 5),
}

RECOIL = {
    "take_down": 0.25,
    "brave_bird": 0.33,
    "double_edge": 0.25,
    "flare_blitz": 0.33,
    "head_smash": 0.5,
    "light_of_ruin": 0.5,
    "submission": 0.25,
    "wild_charge": 0.25,
    "wave_crash": 0.33,
    "wood_hammer": 0.33,
}


def load_moves():
    if not MOVES_FILE.exists():
        print(f"{MOVES_FILE} not found — run generate_pokedex.py first.")
        return None
    with open(MOVES_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_moves(data):
    with open(MOVES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    moves = load_moves()
    if moves is None:
        return

    applied = 0
    missing = []

    for move_id, bypasses in SEMI_INVULNERABLE.items():
        if move_id not in moves:
            missing.append(move_id)
            continue
        moves[move_id].setdefault("flags", {})
        moves[move_id]["flags"]["semi_invulnerable_turn"] = True
        moves[move_id]["flags"]["bypasses_protect"] = bypasses
        moves[move_id]["flags"]["charge_turns"] = 1
        applied += 1

    for move_id in CHARGE_ONLY:
        if move_id not in moves:
            missing.append(move_id)
            continue
        moves[move_id].setdefault("flags", {})
        moves[move_id]["flags"]["charge_turns"] = 1
        applied += 1

    for move_id in BYPASSES_PROTECT_ONLY:
        if move_id not in moves:
            missing.append(move_id)
            continue
        moves[move_id].setdefault("flags", {})
        moves[move_id]["flags"]["bypasses_protect"] = True
        applied += 1

    for move_id, (min_hits, max_hits) in MULTI_HIT.items():
        if move_id not in moves:
            missing.append(move_id)
            continue
        moves[move_id].setdefault("flags", {})
        moves[move_id]["flags"]["min_hits"] = min_hits
        moves[move_id]["flags"]["max_hits"] = max_hits
        applied += 1

    save_moves(moves)
    print(f"Applied flags to {applied} moves.")
    if missing:
        # not in moves.json yet — likely a move no Pokemon on your dex learns
        print(f"Skipped ({len(missing)}, not found in moves.json): {', '.join(sorted(set(missing)))}")


if __name__ == "__main__":
    main()