from type_chart import TYPE_CHART
from type_chart import get_effectiveness
from type_chart import dual_effectiveness

def invalid(reason):
    print(f"INVALID_INPUT:INVALID.{reason}")
    print("RESTARTING.PROGRAM")

inputs = True

while inputs == True:
    pokemon_name = str(input("Pokemon Name: ")[:30])
    level = int(input("Level (Between 1 to 100): "))
    if level < 0 or level > 100:
        invalid("LEVEL")
        continue
    pokemon_type1 = input("Pokemon Type 1: ").lower()
    pokemon_type2 = input("Pokemon Type 2 (type 'None' if only 1): ").lower()
    if pokemon_type2 == "none":
        pokemon_type2 = None
    pokemon_atk = int(input("Attack Stat of your Pokemon (After EVs and IVs): "))
    pokemon_sp_atk = int(input("Special Attack Stat of your Pokemon (After EVs and IVs): "))
    opp_def = int(input("Defense Stat of Opponent Pokemon (After EVs and IVs): "))
    opp_sp_def = int(input("Special Defense Stat of Opponent Pokemon (After EVs and IVs): "))
    opp_type1 = input("Opponent Pokemon Type 1: ").lower()
    opp_type2 = input("Opponent Pokemon Type 2 (type 'None' if only 1): ").lower()
    if pokemon_type2 == "none":
            pokemon_type2 = None
    move_name = str(input("Move Name: ")[:30])
    move_power = int(input("Base Move Power (Between 10 to 250): "))
    if move_power < 10 or move_power > 250:
        invalid("MOVE_POWER")
        continue
    move_category = str(input("Move Category (Special / Physical / Status): ")).lower()
    if move_category not in ("special", "physical", "status"):
        invalid("MOVE_TYPE")
        continue
    move_type = input("Move Type: ")
    atk_modifier = float(input("Attack stat modifiers (1 / 1.5 / 2 / 2.5 / 3 / 3.5 / 4): "))
    if atk_modifier not in (1, 1.5, 2, 2.5, 3, 3.5, 4):
        invalid("MODIFIER")
        continue
    sp_atk_modifier = float(input("Special Attack stat modifiers (1 / 1.5 / 2 / 2.5 / 3 / 3.5 / 4): "))
    if sp_atk_modifier not in (1, 1.5, 2, 2.5, 3, 3.5, 4):
        invalid("MODIFIER")
        continue
    pokemon_atk *= atk_modifier
    pokemon_sp_atk *= sp_atk_modifier
    opp_def_modifier = float(input("Opponent's Defense stat modifiers (1 (if no mods) / 1.5 / 2 / 2.5 / 3 / 3.5 / 4): "))
    if opp_def_modifier not in (1, 1.5, 2, 2.5, 3, 3.5, 4):
        invalid("MODIFIER")
        continue
    opp_sp_def_modifier = float(input("Opponent's Special Defense stat modifiers (1 (if no mods) / 1.5 / 2 / 2.5 / 3 / 3.5 / 4): "))
    if opp_sp_def_modifier not in (1, 1.5, 2, 2.5, 3, 3.5, 4):
        invalid("MODIFIER")
        continue
    opp_def *= opp_def_modifier
    opp_sp_def *= opp_sp_def_modifier
    if move_category == "physical":
        def_pokemon_atk = pokemon_atk
        def_opp_def = opp_def
    elif move_category == "special":
        def_pokemon_atk = pokemon_sp_atk
        def_opp_def = opp_sp_def
    else:
        def_pokemon_atk = 0
        def_opp_def = 1
    inputs = False

effect = dual_effectiveness(move_type, opp_type1, opp_type2)
if move_type == pokemon_type1 or move_type == pokemon_type2:
    stab = 1.5
else:
    stab = 1
total_damage = ((((2 * level / 5) + 2) * (def_pokemon_atk / def_opp_def) * (move_power / 50)) + 2) * effect * stab
print(f"{pokemon_name} used {move_name}!")
if effect == 4:
    print("It was extremely effective!")
elif effect == 2:
    print("It was super effective!")
elif effect == 0.5:
    print("It was not very effective...")
elif effect == 0.25:
    print("It was largely ineffective...")
print("Total Damage:", total_damage)