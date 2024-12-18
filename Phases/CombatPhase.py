

def check_for_battle(p_one, p_two, planet_id, first_planet):
    planet_name = p_one.get_planet_name_given_position(planet_id - 1)
    print("Check for battle at:", planet_name)
    if first_planet:
        print(planet_name, "is first planet. Resolve battle")
    else:
        print(planet_name, "is not first planet. Check warlords")
        if p_one.check_for_warlord(planet_id - 1) or p_two.check_for_warlord(planet_id - 1):
            print("Battle is resolved at:", planet_name)

def combat_phase(p_one, p_two, round_number):
    p_one.set_phase("Combat")
    p_two.set_phase("Combat")
    index = round_number
    planets_counted = 0
    first_planet = True
    while planets_counted < 5 and index < 7:
        check_for_battle(p_one, p_two, index, first_planet)
        first_planet = False
        index += 1
        planets_counted += 1