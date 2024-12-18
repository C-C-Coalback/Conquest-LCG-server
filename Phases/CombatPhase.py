

def resolve_battle(p_one, p_two, planet_id, first_planet):
    player_one_check = p_one.check_if_units_present(planet_id)
    player_two_check = p_two.check_if_units_present(planet_id)
    while player_one_check and player_two_check:
        print("Combat round happens!")
        input("Wait for input")
        # player_one_check = p_one.check_if_units_present(planet_id)
        # player_two_check = p_two.check_if_units_present(planet_id)
        player_one_check = False
        player_two_check = False
    if player_one_check and not player_two_check:
        print(p_one.get_name_player(), "has units,", p_two.get_name_player(), "doesn't")
        print(p_two.get_name_player(), "wins the battle")
        # resolve_planet_battle_effect(p_one, p_two, planet_id, game_screen)
        if first_planet:
            print("Planet needs to be captured")
    elif not player_one_check and player_two_check:
        print(p_two.get_name_player(), "has units,", p_one.get_name_player(), "doesn't")
        print(p_two.get_name_player(), "wins the battle")
        # resolve_planet_battle_effect(p_two, p_one, planet_id, game_screen)
        if first_planet:
            print("Planet needs to be captured")
        elif not player_one_check and not player_two_check:
            print("Neither player has units")
    if first_planet:
        p_one.toggle_planet_in_play(planet_id)
        p_two.toggle_planet_in_play(planet_id)

def check_for_battle(p_one, p_two, planet_id, first_planet):
    planet_name = p_one.get_planet_name_given_position(planet_id - 1)
    print("Check for battle at:", planet_name)
    if first_planet:
        print(planet_name, "is first planet. Resolve battle")
        resolve_battle(p_one, p_two, planet_id - 1, first_planet)
    else:
        print(planet_name, "is not first planet. Check warlords")
        if p_one.check_for_warlord(planet_id - 1) or p_two.check_for_warlord(planet_id - 1):
            print("Battle is resolved at:", planet_name)
            resolve_battle(p_one, p_two, planet_id - 1, first_planet)


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