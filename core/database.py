import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_json(name):
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)

POKEMON = load_json("pokemon.json")
ASC_POKEMON = load_json("ascensions.json")
MOVES = load_json("moves.json")