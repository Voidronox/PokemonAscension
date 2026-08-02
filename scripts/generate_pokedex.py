"""
Pulls stats/types/abilities/movepool/evolution data from PokeAPI for a list
of species names, and merges the result into data/pokemon.json and
data/moves.json.

Usage:
    1. Put one species name per line in data/champions_roster.txt
       (PokeAPI names are lowercase, hyphenated for forms, e.g. "mr-mime")
    2. Run: python scripts/generate_pokedex.py
    3. Check the console for any names it couldn't find, fix and re-run.

Existing entries in pokemon.json/moves.json are NOT overwritten — your
custom starters (decidueye_regional, clawvurin, kitsunova, etc.) are safe.
Anything auto-filled here still needs your review, especially:
  - evolves_from/evolves_to/evolution_level (regional forms and custom
    evolutions like Clawvurin/Kitsunova won't be known to PokeAPI)
  - ascension_id (always None here — you assign these by hand)
"""

import json
import time
from pathlib import Path
import urllib.request
import urllib.error

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
ROSTER_FILE = DATA_DIR / "champions_roster.txt"
POKEMON_FILE = DATA_DIR / "pokemon.json"
MOVES_FILE = DATA_DIR / "moves.json"

API_BASE = "https://pokeapi.co/api/v2"
REQUEST_DELAY = 0.1  # seconds between requests, be polite to the free API

STAT_NAME_MAP = {
    "hp": "hp",
    "attack": "atk",
    "defense": "def",
    "special-attack": "sp_atk",
    "special-defense": "sp_def",
    "speed": "speed",
}


def fetch_json(url):
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; PokemonAscensionDexGen/1.0)",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  ! failed: {url} ({e.code})")
        return None


def load_json(path):
    if path.exists():
        with open(path, encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            return {}  # file exists but is empty
        return json.loads(content)
    return {}


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def build_move_entry(move_name):
    data = fetch_json(f"{API_BASE}/move/{move_name}")
    if not data:
        return None
    effect = ""
    for entry in data.get("effect_entries", []):
        if entry["language"]["name"] == "en":
            effect = entry["short_effect"]
            break
    return {
        "name": data["name"].replace("-", " ").title(),
        "type": data["type"]["name"].title(),
        "category": data["damage_class"]["name"] if data.get("damage_class") else "status",
        "power": data.get("power"),
        "accuracy": data.get("accuracy"),
        "pp": data.get("pp"),
        "effect": effect,
    }


def get_evolution_info(species_data):
    """Best-effort evolves_from/evolves_to/evolution_level from the species
    endpoint's evolution chain. Regional forms and any evolution you've
    changed yourself won't be right here — check these by hand."""
    evolves_from = species_data.get("evolves_from_species")
    evolves_from_name = evolves_from["name"] if evolves_from else None

    chain_url = species_data.get("evolution_chain", {}).get("url")
    evolves_to_name = None
    evolution_level = None
    if chain_url:
        chain_data = fetch_json(chain_url)
        if chain_data:
            evolves_to_name, evolution_level = _walk_chain(
                chain_data.get("chain", {}), species_data["name"]
            )
    return evolves_from_name, evolves_to_name, evolution_level


def _walk_chain(node, target_name):
    if node.get("species", {}).get("name") == target_name:
        for nxt in node.get("evolves_to", []):
            level = None
            for detail in nxt.get("evolution_details", []):
                if detail.get("min_level"):
                    level = detail["min_level"]
            return nxt.get("species", {}).get("name"), level
        return None, None
    for child in node.get("evolves_to", []):
        result = _walk_chain(child, target_name)
        if result != (None, None):
            return result
    return None, None


def build_pokemon_entry(name, moves_db):
    data = fetch_json(f"{API_BASE}/pokemon/{name}")
    if not data:
        return None, None

    species_data = fetch_json(f"{API_BASE}/pokemon-species/{name}")
    evolves_from, evolves_to, evolution_level = (None, None, None)
    if species_data:
        evolves_from, evolves_to, evolution_level = get_evolution_info(species_data)

    base_stats = {}
    for s in data["stats"]:
        key = STAT_NAME_MAP.get(s["stat"]["name"])
        if key:
            base_stats[key] = s["base_stat"]

    types = [t["type"]["name"].title() for t in data["types"]]
    abilities = [a["ability"]["name"].replace("-", " ").title() for a in data["abilities"]]

    movepool = []
    for m in data["moves"]:
        for version_detail in m["version_group_details"]:
            if version_detail["move_learn_method"]["name"] == "level-up":
                move_id = m["move"]["name"].replace("-", "_")
                level = version_detail["level_learned_at"]
                movepool.append({"move": move_id, "level": level})
                if move_id not in moves_db:
                    print(f"    fetching move: {move_id}")
                    entry = build_move_entry(m["move"]["name"])
                    if entry:
                        moves_db[move_id] = entry
                    time.sleep(REQUEST_DELAY)
                break  # only need one match per move

    entry = {
        "name": data["name"].replace("-", " ").title(),
        "types": types,
        "base_stats": base_stats,
        "abilities": abilities,
        "movepool": movepool,
        "evolves_from": evolves_from,
        "evolves_to": evolves_to,
        "evolution_level": evolution_level,
        "ascension_id": None,  # assign these yourself
    }
    return data["name"], entry


def main():
    if not ROSTER_FILE.exists():
        print(f"Create {ROSTER_FILE} with one PokeAPI species name per line, then re-run.")
        return

    names = [
        line.strip().lower()
        for line in ROSTER_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    pokemon_db = load_json(POKEMON_FILE)
    moves_db = load_json(MOVES_FILE)

    not_found = []
    for i, name in enumerate(names, 1):
        if name in pokemon_db:
            print(f"[{i}/{len(names)}] {name}: already in pokemon.json, skipping")
            continue
        print(f"[{i}/{len(names)}] fetching {name}...")
        key, entry = build_pokemon_entry(name, moves_db)
        if entry:
            pokemon_db[key] = entry
        else:
            not_found.append(name)
        time.sleep(REQUEST_DELAY)

    save_json(POKEMON_FILE, pokemon_db)
    save_json(MOVES_FILE, moves_db)

    print(f"\nDone. {len(pokemon_db)} pokemon, {len(moves_db)} moves in the data files.")
    if not_found:
        print(f"Could not find ({len(not_found)}): {', '.join(not_found)}")
        print("Check spelling/hyphenation against pokeapi.co naming (e.g. 'mr-mime', 'nidoran-f').")


if __name__ == "__main__":
    main()