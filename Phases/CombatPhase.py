import pygame

import FindCard
from Phases.PlanetBattleAbilities import resolve_planet_battle_effect
import ClickDetection
from Drawing import draw_all


def pygame_unit_attacks_unit(att, defe, planet_id, att_pos, defe_pos, game_screen):
    attack_value = att.get_attack_given_pos(planet_id, att_pos)
    if att.get_cards_in_play()[planet_id + 1][att_pos].get_name() == "Tankbusta Bommaz":
        if defe.get_cards_in_play()[planet_id + 1][defe_pos].check_for_a_trait("Vehicle."):
            attack_value = 2 * attack_value
    damage_too_great = defe.pygame_assign_damage_to_pos(planet_id, defe_pos, attack_value)
    if damage_too_great:
        print("Card must be discarded")
        #input("Hold attack")
        return 1
    #input("Hold attack")
    return 0




def pygame_combat_turn(attacker, defender, planet_id, game_screen):
    print(attacker.get_name_player(), '\'s turn to attack', sep='')
    if attacker.get_number() == 1:
        draw_all(game_screen, attacker, defender)
    else:
        draw_all(game_screen, defender, attacker)
    pos_attacker = ClickDetection.prompt_pos_unit_at_planet(attacker, planet_id, game_screen, pygame.Color("red"))
    if pos_attacker == -2:
        pos_unit, pos_planet = ClickDetection.prompt_pos_unit_anywhere(attacker, game_screen, hand_is_option=True)
        if pos_planet == -2:
            card_name_in_hand = attacker.get_cards()[pos_unit]
            card_object = FindCard.find_card(card_name_in_hand)
            if card_object.get_has_action_while_in_hand():
                attacker.pygame_play_card(card_object, defender, game_screen)
        elif pos_planet == -1:
            card_chosen = attacker.get_headquarters()[pos_unit]
            print("CHOSE CARD:", card_chosen.get_name())
            if card_chosen.get_has_action_while_in_play():
                if card_chosen.get_allowed_phases_while_in_play() == "Combat" or\
                        card_chosen.get_allowed_phases_while_in_play() == "All":
                    if card_chosen.get_name() == "Kraktoof Hall":
                        if card_chosen.get_ready():
                            pos_target1, pos_planet_action = ClickDetection.prompt_pos_unit_anywhere(
                                attacker, game_screen, color1=pygame.Color("red"))
                            if pos_planet_action != -1:
                                player_no, pos_target2, pos_planet_action_2 = ClickDetection.\
                                    prompt_pos_unit_anywhere_all_players(attacker, defender, game_screen)
                                if pos_planet_action_2 == pos_planet_action:
                                    attacker.remove_damage_from_pos(pos_planet_action, pos_target1, 1)
                                    defender.pygame_assign_damage_to_pos(pos_planet_action, pos_target2, 1, can_shield=False)
                                    attacker.exhaust_card_in_hq(pos_unit)
                                    if attacker.get_number() == 1:
                                        draw_all(game_screen, attacker, defender)
                                    else:
                                        draw_all(game_screen, defender, attacker)
        else:
            card_chosen = attacker.get_cards_in_play()[pos_planet + 1][pos_unit]
            if card_chosen.get_name() == "Nazdreg's Flash Gitz":
                if not card_chosen.get_ready() and not card_chosen.get_once_per_phase_used():
                    unit_dead = attacker.pygame_assign_damage_to_pos(pos_planet, pos_unit, 1)
                    if not unit_dead:
                        attacker.ready_given_pos(pos_planet, pos_unit)
        return pygame_combat_turn(attacker, defender, planet_id, game_screen)
    if pos_attacker == -1:
        return True
    pos_defender = ClickDetection.prompt_pos_unit_at_planet(defender, planet_id, game_screen, pygame.Color("blue"))
    if pos_defender == -1:
        return pygame_combat_turn(attacker, defender, planet_id, game_screen)
    print("position of unit:", pos_attacker)
    print("SUCCESS")

    if attacker.check_ready_pos(planet_id, pos_attacker):
        attacker.exhaust_given_pos(planet_id, pos_attacker)
        defender.print_state_of_unit(planet_id, pos_defender)
        unit_dead = pygame_unit_attacks_unit(attacker, defender, planet_id, pos_attacker, pos_defender, game_screen)
        defender.print_state_of_unit(planet_id, pos_defender)
        if unit_dead == 1:
            # defender.add_card_name_to_discard(defender_name)
            if defender.check_if_warlord(planet_id, pos_defender):
                defender.bloody_warlord_given_pos(planet_id, pos_defender)
            else:
                defender.remove_card_from_play(planet_id, pos_defender)
                defender.print_cards_at_planet(planet_id)
                defender.print_discard()
        if attacker.get_cards_in_play()[planet_id + 1][pos_attacker].get_name() == "Burna Boyz":
            if attacker.get_number() == 1:
                draw_all(game_screen, attacker, defender)
            else:
                draw_all(game_screen, defender, attacker)
            pos_defender_sweep = ClickDetection.prompt_pos_unit_at_planet(defender, planet_id, game_screen, pygame.Color("blue"))
            if pos_defender_sweep == -1:
                pass
            else:
                unit_dead = defender.pygame_assign_damage_to_pos(planet_id, pos_defender_sweep, 1)
                if unit_dead == 1:
                    if defender.check_if_warlord(planet_id, pos_defender_sweep):
                        defender.bloody_warlord_given_pos(planet_id, pos_defender_sweep)
                    else:
                        defender.remove_card_from_play(planet_id, pos_defender_sweep)
        attacker.toggle_turn()
        defender.toggle_turn()
        draw_all(game_screen, attacker, defender)
        return False
    else:
        print("Attacker not ready")
    # return to decide if player passed
    return pygame_combat_turn(attacker, defender, planet_id, game_screen)


def determine_combat_initiative(p_one, p_two, planet_id):
    p_one_has_warlord = p_one.check_for_warlord(planet_id)
    p_two_has_warlord = p_two.check_for_warlord(planet_id)
    if p_one_has_warlord == p_two_has_warlord:
        return p_one.get_has_initiative()
    return p_one_has_warlord


def pygame_combat_round(p_one, p_two, planet_id, game_screen):
    planet_name = p_two.get_planet_name_given_position(planet_id)
    p_one_passed = False
    p_two_passed = False
    print("Both have units present. Combat round begins at:", planet_name)
    print(p_one.get_name_player(), "units:")
    p_one.print_cards_at_planet(planet_id)
    print(p_two.get_name_player(), "units:")
    p_two.print_cards_at_planet(planet_id)
    while not p_one_passed or not p_two_passed:
        if determine_combat_initiative(p_one, p_two, planet_id):
            p_one.set_has_turn(True)
            p_two.set_has_turn(False)
            draw_all(game_screen, p_one, p_two)
            p_one_passed = pygame_combat_turn(p_one, p_two, planet_id, game_screen)
            if p_one_passed:
                p_one.set_has_turn(False)
                p_two.set_has_turn(True)
            draw_all(game_screen, p_one, p_two)
            p_two_passed = pygame_combat_turn(p_two, p_one, planet_id, game_screen)
        else:
            p_one.set_has_turn(False)
            p_two.set_has_turn(True)
            draw_all(game_screen, p_one, p_two)
            p_two_passed = pygame_combat_turn(p_two, p_one, planet_id, game_screen)
            if p_two_passed:
                p_one.set_has_turn(True)
                p_two.set_has_turn(False)
            draw_all(game_screen, p_one, p_two)
            p_one_passed = pygame_combat_turn(p_one, p_two, planet_id, game_screen)
    p_one.ready_all_at_planet(planet_id)
    p_two.ready_all_at_planet(planet_id)
    done_retreating = False
    p_one.set_retreating(True)
    p_two.set_retreating(True)
    while not done_retreating:
        if determine_combat_initiative(p_one, p_two, planet_id):
            p_one.set_has_turn(True)
            p_two.set_has_turn(False)
            draw_all(game_screen, p_one, p_two)
            done_retreating = p_one.pygame_retreat_combat_window(planet_id, game_screen)
        else:
            p_one.set_has_turn(False)
            p_two.set_has_turn(True)
            draw_all(game_screen, p_one, p_two)
            done_retreating = p_two.pygame_retreat_combat_window(planet_id, game_screen)
        draw_all(game_screen, p_one, p_two)
    done_retreating = False
    p_one.toggle_turn()
    p_two.toggle_turn()
    draw_all(game_screen, p_one, p_two)
    while not done_retreating:
        if determine_combat_initiative(p_one, p_two, planet_id):
            p_one.set_has_turn(False)
            p_two.set_has_turn(True)
            draw_all(game_screen, p_one, p_two)
            done_retreating = p_two.pygame_retreat_combat_window(planet_id, game_screen)
        else:
            p_one.set_has_turn(True)
            p_two.set_has_turn(False)
            draw_all(game_screen, p_one, p_two)
            done_retreating = p_one.pygame_retreat_combat_window(planet_id, game_screen)
        draw_all(game_screen, p_one, p_two)
    p_one.set_retreating(False)
    p_two.set_retreating(False)
    p_one.toggle_turn()
    p_two.toggle_turn()


def pygame_resolve_battle(p_one, p_two, planet_id, first_planet, game_screen):
    player_one_check = p_one.check_if_units_present(planet_id)
    player_two_check = p_two.check_if_units_present(planet_id)
    while player_one_check and player_two_check:
        pygame_combat_round(p_one, p_two, planet_id, game_screen)
        draw_all(game_screen, p_one, p_two)
        player_one_check = p_one.check_if_units_present(planet_id)
        player_two_check = p_two.check_if_units_present(planet_id)
    if player_one_check and not player_two_check:
        print(p_one.get_name_player(), "has units,", p_two.get_name_player(), "doesn't")
        print(p_two.get_name_player(), "wins the battle")
        resolve_planet_battle_effect(p_one, p_two, planet_id, game_screen)
        if first_planet:
            p_one.retreat_all_at_planet(planet_id)
            p_one.capture_planet(planet_id)
    elif not player_one_check and player_two_check:
        print(p_two.get_name_player(), "has units,", p_one.get_name_player(), "doesn't")
        print(p_two.get_name_player(), "wins the battle")
        resolve_planet_battle_effect(p_two, p_one, planet_id, game_screen)
        if first_planet:
            p_two.retreat_all_at_planet(planet_id)
            p_two.capture_planet(planet_id)
    elif not player_one_check and not player_two_check:
        print("Neither player has units")
    if first_planet:
        p_one.toggle_planet_in_play(planet_id)
        p_two.toggle_planet_in_play(planet_id)
    p_one.reset_all_extra_attack_until_end_of_battle()
    p_two.reset_all_extra_attack_until_end_of_battle()


def pygame_check_for_battle(p_one, p_two, planet_id, first_planet, game_screen):
    planet_name = p_two.get_planet_name_given_position(planet_id - 1)
    if first_planet:
        print("First planet. Resolve battle at:", planet_name)
        pygame_resolve_battle(p_one, p_two, planet_id - 1, first_planet, game_screen)
    elif not first_planet:
        print("Not first planet. Check for Warlords at:", planet_name)
        if p_one.check_for_warlord(planet_id - 1):
            print("Battle is resolved at:", planet_name)
            pygame_resolve_battle(p_one, p_two, planet_id - 1, first_planet, game_screen)
        elif p_two.check_for_warlord(planet_id - 1):
            print("Battle is resolved at:", planet_name)
            pygame_resolve_battle(p_one, p_two, planet_id - 1, first_planet, game_screen)
    draw_all(game_screen, p_one, p_two)


def pygame_combat_phase(round_number, p_one, p_two, game_screen):
    print("combat:", round_number)
    p_one.set_phase("Combat")
    p_two.set_phase("Combat")
    index = round_number
    planets_counted = 0
    first_planet = True
    draw_all(game_screen, p_one, p_two)
    while planets_counted < 5 and index < 7:
        pygame_check_for_battle(p_one, p_two, index, first_planet, game_screen)
        first_planet = False
        index += 1
        planets_counted += 1
    p_one.retreat_warlord()
    p_two.retreat_warlord()
    p_one.print_headquarters()
    p_two.print_headquarters()
