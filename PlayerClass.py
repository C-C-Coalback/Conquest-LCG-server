import random
import copy

import ClickDetection
import FindCard
import pygame

import CardClasses

from Drawing import draw_all
from Inits import PlanetCardsInit


class Player:
    def __init__(self, name, number):
        self.number = number
        self.name_player = name
        self.has_initiative = True
        self.has_turn = True
        self.retreating = False
        self.phase = "Deploy"
        self.round_number = 1
        self.resources = 0
        self.cards = []
        self.victory_display = []
        self.icons_gained = [0, 0, 0]
        self.headquarters = []
        self.deck = []
        self.discard = []
        self.planets_in_play = [True, True, True, True, True, False, False]
        self.cards_in_play = [[] for _ in range(8)]
        self.images_on_screen = [[] for _ in range(11)]
        self.position_images = [[] for _ in range(11)]
        # i_o_s[0-6] = "Cards at Planets"
        # i_o_s[7] = "Hand"
        # i_o_s[8] = "HQ"
        # i_o_s[9] = "Top Discard"
        # i_o_s[10] = "Victory Display"

    def get_phase(self):
        return self.phase

    def set_phase(self, phase):
        self.phase = phase

    def get_retreating(self):
        return self.retreating

    def set_retreating(self, new_val):
        self.retreating = new_val

    def get_round_number(self):
        return self.round_number

    def increment_round_number(self):
        self.round_number += 1

    def get_has_turn(self):
        return self.has_turn

    def get_has_initiative(self):
        return self.has_initiative

    def set_has_turn(self, new_val):
        self.has_turn = new_val

    def get_planets_in_play(self):
        return self.planets_in_play

    def get_name_player(self):
        return self.name_player

    def get_position_images(self):
        return self.position_images

    def get_images_on_screen(self):
        return self.images_on_screen

    def get_number(self):
        return self.number

    def get_resources(self):
        return self.resources

    def get_cards(self):
        return self.cards

    def get_victory_display(self):
        return self.victory_display

    def get_icons_gained(self):
        return self.icons_gained

    def get_headquarters(self):
        return self.headquarters

    def get_deck(self):
        return self.deck

    def get_discard(self):
        return self.discard

    def toggle_planet_in_play(self, planet_id):
        self.planets_in_play[planet_id] = not self.planets_in_play[planet_id]

    def toggle_turn(self):
        self.has_turn = not self.has_turn

    def toggle_initiative(self):
        if self.has_initiative:
            self.has_initiative = False
        else:
            self.has_initiative = True

    def get_cards_in_play(self):
        return self.cards_in_play

    def get_planet_name_given_position(self, planet_id):
        return self.cards_in_play[0][planet_id]

    def init_planets_in_game(self, planets_in_game):
        for j in range(len(planets_in_game)):
            self.cards_in_play[0].append(planets_in_game[j])
            print(self.cards_in_play[0])

    def search_planets_in_game(self, planet_name):
        for j in range(len(self.cards_in_play[0])):
            if self.cards_in_play[0][j] == planet_name:
                print("Planet found")
                return j
        print("Planet not found")
        return -1

    def print_cards_in_play(self):
        print("No of planets:", len(self.cards_in_play[0]))
        for i in range(len(self.cards_in_play[0])):
            print("Cards at planet:", self.cards_in_play[0][i])
            if not self.cards_in_play[i + 1]:
                print("None")
            for j in range(len(self.cards_in_play[i + 1])):
                print(self.cards_in_play[i + 1][j].get_name())

    def pygame_print_cards_in_play(self, game_screen):
        print("No of planets:", len(self.cards_in_play[0]))
        x_first_planet = 60
        y_first_planet = 230
        x_increment = 62
        y_increment = -88
        if self.number == 1:
            y_first_planet = 385
            y_increment = 88
        for i in range(len(self.cards_in_play[0])):
            print("Cards at planet:", self.cards_in_play[0][i])
            x_current_planet = x_first_planet + (i * 165)
            y_current_planet = y_first_planet
            if not self.cards_in_play[i + 1]:
                print("None")
            for j in range(len(self.cards_in_play[i + 1])):
                print(self.cards_in_play[i + 1][j].get_name())
                card_string = self.cards_in_play[i + 1][j].get_name()
                for letter in card_string:
                    if letter == " ":
                        card_string = card_string.replace(letter, "_")
                card_image_name = "ResizedImages/" + card_string + ".jpg"
                if self.cards_in_play[i + 1][j].get_card_type() == "Warlord":
                    if self.cards_in_play[i + 1][j].get_bloodied():
                        card_image_name = "ResizedImages/" + card_string + "_bloodied.jpg"
                card_image = pygame.image.load(card_image_name).convert()
                if not self.cards_in_play[i + 1][j].get_ready():
                    card_image = pygame.transform.rotate(card_image, 270)
                game_screen.blit(card_image, (x_current_planet, y_current_planet))
                damage = self.cards_in_play[i + 1][j].get_damage()
                if 0 < damage < 10:
                    damage = str(damage)
                    damage_name = 'damagetokens/' + damage + '_Damage.png'
                    damage_image = pygame.image.load(damage_name).convert()
                    game_screen.blit(damage_image, (x_current_planet + 10, y_current_planet + 30))
                # pygame.display.flip()
                x_current_planet = x_current_planet + x_increment
                if x_current_planet > x_first_planet + 165 * i + x_increment:
                    x_current_planet = x_first_planet + 165 * i
                    y_current_planet = y_current_planet + y_increment

    def draw_victory_display(self, game_screen):
        x = 30
        y = 505
        inc_y = 10
        if self.get_number() == 2:
            x = 1057
            y = 125
        for i in range(len(self.get_victory_display())):
            card_string = self.victory_display[i].get_name()
            for letter in card_string:
                if letter == " ":
                    card_string = card_string.replace(letter, "_")
            card_image_name = "ResizedImages/" + card_string + ".jpg"
            card_image = pygame.image.load(card_image_name).convert()
            game_screen.blit(card_image, (x, y))
            y = y + inc_y

    def draw_discard(self, game_screen):
        number_in_discard = len(self.discard)
        if number_in_discard == 0:
            return 1
        card_string = self.discard[number_in_discard - 1]
        for letter in card_string:
            if letter == " ":
                card_string = card_string.replace(letter, "_")
        card_image_name = "ResizedImages/" + card_string + ".jpg"
        x = 1091
        y = 512
        if self.number == 2:
            x = 30
            y = 123
        card_image = pygame.image.load(card_image_name).convert()
        game_screen.blit(card_image, (x, y))
        return 0

    def print_cards_at_planet(self, planet_id):
        for j in range(len(self.cards_in_play[planet_id + 1])):
            print(self.cards_in_play[planet_id + 1][j].get_name())

    def get_number_of_cards_at_planet(self, planet_id):
        return len(self.cards_in_play[planet_id + 1])

    def check_for_warlord(self, planet_id):
        print("Looking for warlord at:", self.cards_in_play[0][planet_id])
        if not self.cards_in_play[planet_id + 1]:
            pass
        else:
            for j in range(len(self.cards_in_play[planet_id + 1])):
                print("Card is:", self.cards_in_play[planet_id + 1][j].get_name())
                print("Check if card is a warlord.")
                if self.cards_in_play[planet_id + 1][j].get_card_type() == "Warlord":
                    print("Card is a Warlord")
                    return 1
                else:
                    print("Card is not a Warlord")
        print("Warlord is not present")
        return 0

    def check_if_units_present(self, planet_id):
        print("Checking for cards at:", self.cards_in_play[0][planet_id])
        if not self.cards_in_play[planet_id + 1]:
            print("No cards present.")
            return 0
        print("Cards present.")
        return 1

    def count_command_at_planet(self, planet_id):
        command = 0
        for i in range(len(self.cards_in_play[planet_id])):
            print(self.cards_in_play[planet_id][i].get_command())
            if self.cards_in_play[planet_id][i].get_ready():
                command += self.cards_in_play[planet_id][i].get_command()
        return command

    def capture_planet(self, planet_id):
        planet_name = self.cards_in_play[0][planet_id]
        print("Attempting to capture planet.")
        print("Planet to capture:", planet_name)
        planet_cards = PlanetCardsInit.planet_cards_init()
        i = 0
        for letter in planet_name:
            if letter == "_":
                planet_name = planet_name.replace(letter, " ")
        while planet_cards[i].get_name() != "FINAL CARD":
            print(planet_cards[i].get_name(), planet_name)
            if planet_cards[i].get_name() == planet_name:
                self.victory_display.append(planet_cards[i])
                self.print_victory_display()
                self.print_icons_on_captured()
                return 0
            else:
                i += 1
        return -1

    def retreat_unit(self, planet_id, unit_id):
        # print("Name of card:", self.cards_in_play[planet_id + 1][unit_id].get_name())
        self.headquarters.append(copy.deepcopy(self.cards_in_play[planet_id + 1][unit_id]))
        del self.cards_in_play[planet_id + 1][unit_id]

    def rout_unit_from_planet(self, planet_id, unit_id):
        self.exhaust_given_pos(planet_id, unit_id)
        self.retreat_unit(planet_id, unit_id)

    def exhaust_card_in_hq(self, unit_id):
        self.headquarters[unit_id].exhaust_card()

    def pygame_retreat_combat_window(self, planet_id, game_screen):
        while True:
            unit_pos = ClickDetection.prompt_pos_unit_at_planet(self, planet_id, game_screen)
            if unit_pos == -1:
                return True
            else:
                self.exhaust_given_pos(planet_id, unit_pos)
                self.retreat_unit(planet_id, unit_pos)
                return False

    def retreat_all_at_planet(self, planet_id):
        while self.cards_in_play[planet_id + 1]:
            self.retreat_unit(planet_id, 0)
        self.print_cards_at_planet(planet_id + 1)
        self.print_headquarters()

    def retreat_warlord(self):
        for i in range(len(self.cards_in_play[0])):
            if not self.cards_in_play[i + 1]:
                pass
            else:
                j = 0
                while j < len(self.cards_in_play[i + 1]):
                    print("TEST", self.cards_in_play[0][i], "planet", i)
                    print(self.cards_in_play[0])
                    print(len(self.cards_in_play[i + 1]))
                    if self.cards_in_play[i + 1][j].get_card_type() == "Warlord":
                        self.retreat_unit(i, j)
                        j = j - 1
                    j = j + 1

    def print_victory_display(self):
        print("Cards in victory display:")
        for i in range(len(self.victory_display)):
            print(self.victory_display[i].get_name())

    def print_icons_on_captured(self):
        total_icons = [0, 0, 0]
        for i in range(len(self.victory_display)):
            if self.victory_display[i].get_red():
                total_icons[0] += 1
            if self.victory_display[i].get_blue():
                total_icons[1] += 1
            if self.victory_display[i].get_green():
                total_icons[2] += 1
        print("Total Icons:", total_icons)

    def find_card_in_hand(self, card_name_to_find):
        for i in range(len(self.cards)):
            if self.cards[i] == card_name_to_find:
                print("Card found")
                return i
        print("Card not found")
        return -1

    def search_card_at_planet(self, card_name, planet_id):
        for i in range(len(self.cards_in_play[planet_id + 1])):
            if self.cards_in_play[planet_id + 1][i].get_name() == card_name:
                print("Card found:", self.cards_in_play[planet_id + 1][i].get_name(),
                      "position:", i)
                # confirm = input("Confirm card selection.(y/n)")
                # if confirm == "y":
                return i
        return -1

    def exhaust_given_pos(self, planet_id, unit_id):
        self.cards_in_play[planet_id + 1][unit_id].exhaust_card()

    def check_warlord_given_pos(self, planet_id, unit_id):
        if self.cards_in_play[planet_id + 1][unit_id].get_card_type() == "Warlord":
            return True
        return False

    def ready_given_pos(self, planet_id, unit_id):
        self.cards_in_play[planet_id + 1][unit_id].ready_card()

    def ready_all_at_planet(self, planet_id):
        for i in range(len(self.cards_in_play[planet_id + 1])):
            self.ready_given_pos(planet_id, i)

    def ready_all_in_headquarters(self):
        for i in range(len(self.headquarters)):
            self.headquarters[i].ready_card()

    def ready_all_in_play(self):
        for i in range(len(self.cards_in_play[0])):
            self.ready_all_at_planet(i)
        self.ready_all_in_headquarters()

    def count_number_units_at_planet(self, planet_id):
        return len(self.cards_in_play[planet_id + 1])

    def count_number_units_at_hq(self):
        count = 0
        for i in range(len(self.headquarters)):
            if self.headquarters[i].get_card_type != "Support":
                count = count + 1
        return count

    def count_number_units_in_play(self):
        count = 0
        for i in range(len(self.cards_in_play[0])):
            count = count + self.count_number_units_at_planet(i)
        count = count + self.count_number_units_at_hq()
        print(count)
        return count

    def check_ready_pos(self, planet_id, unit_id):
        return self.cards_in_play[planet_id + 1][unit_id].get_ready()

    def get_attack_given_pos(self, planet_id, unit_id):
        attack_value = self.cards_in_play[planet_id + 1][unit_id].get_attack()
        if self.search_card_at_planet("Nazdreg", planet_id) != -1:
            if self.cards_in_play[planet_id + 1][unit_id].get_name() != "Nazdreg":
                self.cards_in_play[planet_id + 1][unit_id].set_brutal(True)
        if self.cards_in_play[planet_id + 1][unit_id].get_name() == "Goff Boyz":
            attack_value = attack_value + 3
        if self.cards_in_play[planet_id + 1][unit_id].get_brutal():
            attack_value = attack_value + self.cards_in_play[planet_id + 1][unit_id].get_damage()
        self.cards_in_play[planet_id + 1][unit_id].reset_brutal()
        attack_value += self.cards_in_play[planet_id + 1][unit_id].get_extra_attack_until_end_of_battle()
        return attack_value

    def get_shields_given_pos(self, pos_in_hand):
        shield_card_name = self.cards[pos_in_hand]
        card_object = FindCard.find_card(shield_card_name)
        return card_object.get_shields()

    def remove_damage_from_pos(self, planet_id, unit_id, amount):
        self.cards_in_play[planet_id + 1][unit_id].remove_damage(amount)

    def remove_damage_from_pos_headquarters(self, unit_id, amount):
        self.headquarters[unit_id].remove_damage(amount)

    def pygame_assign_damage_to_pos(self, planet_id, unit_id, damage, can_shield=True):
        damage_too_great = self.cards_in_play[planet_id + 1][unit_id].pygame_damage_card(self, damage, can_shield)
        return damage_too_great

    def suffer_area_effect_at_planet(self, attacker, amount, planet_id, game_screen):
        if planet_id == -1:
            return None
        i = 0
        while i < len(self.cards_in_play[planet_id + 1]):
            if self.number == 1:
                draw_all(game_screen, self, attacker, "Atrox Prime ability")
            else:
                draw_all(game_screen, attacker, self, "Atrox Prime ability")
            damage_to_great = self.pygame_assign_damage_to_pos(planet_id, i, amount)
            if damage_to_great == 1:
                if self.check_if_warlord(planet_id, i):
                    self.bloody_warlord_given_pos(planet_id, i)
                else:
                    self.remove_card_from_play(planet_id, i)
                i = i - 1
            i = i + 1

    def check_if_warlord(self, planet_id, unit_id):
        if self.cards_in_play[planet_id + 1][unit_id].get_card_type() == "Warlord":
            return True
        return False

    def bloody_warlord_given_pos(self, planet_id, unit_id):
        self.cards_in_play[planet_id + 1][unit_id].bloody_warlord()
        self.retreat_warlord()

    def print_state_of_unit(self, planet_id, unit_id):
        print("Name:", self.cards_in_play[planet_id + 1][unit_id].get_name())
        if self.cards_in_play[planet_id + 1][unit_id].get_ready():
            print("Ready")
        else:
            print("Exhausted")
        print("Damage:", self.cards_in_play[planet_id + 1][unit_id].get_damage())

    def commit_warlord_to_planet(self, planet_id):
        headquarters_list = self.get_headquarters()
        for i in range(len(headquarters_list)):
            if headquarters_list[i].get_card_type() == "Warlord":
                print(headquarters_list[i].get_name())
                self.cards_in_play[planet_id].append(copy.deepcopy(headquarters_list[i]))
                self.headquarters.remove(headquarters_list[i])
                self.commit_units_to_planet(planet_id)
                return 0
        return -1

    def commit_units_to_planet(self, planet_id):
        headquarters_list = self.get_headquarters()
        i = 0
        while i < len(headquarters_list):
            print("here", headquarters_list[i].get_name())
            if headquarters_list[i].get_card_type() == "Army" or headquarters_list[i].get_card_type() == "Token":
                print(headquarters_list[i].get_name())
                headquarters_list[i].exhaust_card()
                self.cards_in_play[planet_id].append(copy.deepcopy(headquarters_list[i]))
                self.headquarters.remove(headquarters_list[i])
                i = i - 1
            i = i + 1

    def move_unit_from_hq_to_planet(self, start_unit, end_planet):
        if self.headquarters[start_unit]:
            if self.headquarters[start_unit] == "Support":
                print("Supports may not leave HQ")
            else:
                self.cards_in_play[end_planet + 1].append(copy.deepcopy(self.headquarters[start_unit]))
                self.headquarters.remove(self.headquarters[start_unit])

    def move_unit_from_planet_to_planet(self, start_unit, start_planet, end_planet):
        if self.cards_in_play[start_planet + 1][start_unit]:
            self.cards_in_play[end_planet + 1].append(copy.deepcopy(self.cards_in_play[start_planet + 1][start_unit]))
            self.cards_in_play[start_planet + 1].remove(self.cards_in_play[start_planet + 1][start_unit])

    def count_discounts(self, card_to_play, planet_pos=None):
        discounts = 0
        for i in range(len(self.headquarters)):
            if self.headquarters[i].get_applies_discounts() and self.headquarters[i].get_ready():
                if self.headquarters[i].get_discount_match_factions():
                    if self.headquarters[i].get_faction() == card_to_play.get_faction():
                        discounts = discounts + self.headquarters[i].get_discount_amount()
                else:
                    discounts = discounts + self.headquarters[i].get_discount_amount()
        i = 0
        while i < len(self.cards):
            card_object = FindCard.find_card(self.cards[i])
            if card_object.get_applies_discounts():
                if card_object.get_discount_match_factions():
                    if card_object.get_faction() == card_to_play.get_faction():
                        discounts = discounts + card_object.get_discount_amount()
                else:
                    discounts = discounts + card_object.get_discount_amount()
            i += 1
        if planet_pos is None:
            pass
        else:
            for i in range(len(self.cards_in_play[planet_pos + 1])):
                if self.cards_in_play[planet_pos + 1][i].get_applies_discounts():
                    if self.cards_in_play[planet_pos + 1][i].get_discount_match_factions():
                        if self.cards_in_play[planet_pos + 1][i].get_faction() == card_to_play.get_faction():
                            discounts = discounts + self.cards_in_play[planet_pos + 1][i].get_discount_amount()
                    else:
                        discounts = discounts + self.cards_in_play[planet_pos + 1][i].get_discount_amount()
        print("Potential discount:", discounts)
        return discounts

    def pygame_play_card(self, card_to_play, other_player, game_screen):
        if FindCard.check_card_type(card_to_play, "Army"):
            planet_id = ClickDetection.prompt_pos_planet()
            if not self.planets_in_play[planet_id]:
                return -1
            card_cost = card_to_play.get_cost()
            max_discounts = self.count_discounts(card_to_play, planet_id)
            applied_discounts = 0
            damage_on_play = 0
            if max_discounts != 0:
                done_discounting = False
                for i in range(len(self.cards_in_play[planet_id + 1])):
                    if self.cards_in_play[planet_id + 1][i].get_applies_discounts():
                        applied_discounts = applied_discounts + self.cards_in_play[planet_id + 1][i].get_discount_amount()
                if applied_discounts == max_discounts:
                    done_discounting = True
                while not done_discounting:
                    if self.get_number() == 1:
                        draw_all(game_screen, self, other_player)
                    else:
                        draw_all(game_screen, other_player, self)
                    unit_pos, planet_pos = ClickDetection.prompt_pos_unit_anywhere(self, hand_is_option=True)
                    if unit_pos == -1 and planet_pos == -1:
                        done_discounting = True
                    elif unit_pos != -1 and planet_pos == -2:
                        card_object = FindCard.find_card(self.cards[unit_pos])
                        if card_object.get_applies_discounts():
                            if card_object.get_discount_match_factions():
                                if card_object.get_faction() == card_to_play.get_faction():
                                    applied_discounts += card_object.get_discount_amount()
                                    if card_object.get_name() == "Bigga is Betta":
                                        damage_on_play += 1
                                    self.discard_card_from_hand(unit_pos)
                    elif unit_pos != -1 and planet_pos == -1:
                        if self.headquarters[unit_pos].get_applies_discounts() and self.headquarters[unit_pos].get_ready():
                            if self.headquarters[unit_pos].get_discount_match_factions():
                                if self.headquarters[unit_pos].get_faction() == card_to_play.get_faction():
                                    self.headquarters[unit_pos].exhaust_card()
                                    applied_discounts += self.headquarters[unit_pos].get_discount_amount()
                            else:
                                self.headquarters[unit_pos].exhaust_card()
                                applied_discounts += self.headquarters[unit_pos].get_discount_amount()
                    if applied_discounts == max_discounts:
                        done_discounting = True
            card_cost = card_cost - applied_discounts
            if card_cost < 0:
                card_cost = 0
            if self.spend_resources(card_cost) == 0:
                if card_to_play.get_name() == "Weirdboy Maniak":
                    self.suffer_area_effect_at_planet(other_player, 1, planet_id, game_screen)
                    other_player.suffer_area_effect_at_planet(self, 1, planet_id, game_screen)
                self.cards_in_play[planet_id + 1].append(copy.deepcopy(card_to_play))
                while damage_on_play > 0:
                    played_unit_pos = len(self.cards_in_play[planet_id + 1]) - 1
                    if self.get_number() == 1:
                        draw_all(game_screen, self, other_player)
                    else:
                        draw_all(game_screen, other_player, self)
                    unit_dead = self.pygame_assign_damage_to_pos(planet_id, played_unit_pos, 1)
                    damage_on_play = damage_on_play - 1
                    if unit_dead == 1:
                        damage_on_play = 0
                self.cards.remove(card_to_play.get_name())
                print("Played card")
                return 0
            print("Insufficient resources")
            return -1
        elif FindCard.check_card_type(card_to_play, "Support"):
            if self.spend_resources((card_to_play.get_cost())) == 0:
                self.add_to_hq(card_to_play)
                self.cards.remove(card_to_play.get_name())
                print("Played card to HQ")
                for i in range(len(self.get_headquarters())):
                    print(self.get_headquarters()[i].get_name())
                return 0
            print("Insufficient resources")
            return -1
        elif FindCard.check_card_type(card_to_play, "Event"):
            if card_to_play.get_has_action_while_in_hand():
                allowed_phases = card_to_play.get_allowed_phases_while_in_hand()
                if allowed_phases == "All" or allowed_phases == self.phase:
                    if self.spend_resources((card_to_play.get_cost())) == 0:
                        self.add_card_name_to_discard(card_to_play.get_name())
                        self.cards.remove(card_to_play.get_name())
                        if card_to_play.get_name() == "Snotling Attack":
                            snotling = CardClasses.TokenCard("Snotlings", "", "Runt.", "Orks", 1, 1, "NO IMAGE")
                            for i in range(4):
                                if self.get_number() == 1:
                                    draw_all(game_screen, self, other_player)
                                else:
                                    draw_all(game_screen, other_player, self)
                                planet_pos = ClickDetection.prompt_pos_planet()
                                print(planet_pos)
                                if planet_pos != -1:
                                    self.cards_in_play[planet_pos + 1].append(copy.deepcopy(snotling))
                        elif card_to_play.get_name() == "Squig Bombin'":
                            if self.get_number() == 1:
                                draw_all(game_screen, self, other_player)
                                player_no, unit_pos, planet_pos = \
                                    ClickDetection.prompt_pos_unit_anywhere_all_players(self, other_player)
                            else:
                                draw_all(game_screen, other_player, self)
                                player_no, unit_pos, planet_pos = \
                                    ClickDetection.prompt_pos_unit_anywhere_all_players(other_player, self)
                            if planet_pos == -1 and unit_pos != -1:
                                if self.get_number() == player_no:
                                    self.destroy_card_in_hq(unit_pos, "Support")
                                else:
                                    other_player.destroy_card_in_hq(unit_pos, "Support")
                        elif card_to_play.get_name() == "Battle Cry":
                            print("Apply +2 ATK to all units")
                            for planet_pos in range(7):
                                for unit_pos in range(len(self.cards_in_play[planet_pos + 1])):
                                    self.cards_in_play[planet_pos + 1][unit_pos].\
                                        increase_extra_attack_until_end_of_battle(2)
                        if self.get_number() == 1:
                            draw_all(game_screen, self, other_player)
                        else:
                            draw_all(game_screen, other_player, self)
                        return 0
        print("not an army/support card")
        return -1

    def reset_all_extra_attack_until_end_of_battle(self):
        for planet_pos in range(7):
            for unit_pos in range(len(self.cards_in_play[planet_pos + 1])):
                self.cards_in_play[planet_pos + 1][unit_pos]. \
                    reset_extra_attack_until_end_of_battle()
        for card_pos in range(len(self.headquarters)):
            if self.headquarters[card_pos].get_card_type() != "Support":
                self.headquarters[card_pos].reset_extra_attack_until_end_of_battle()

    def destroy_card_in_hq(self, card_pos, card_type=None):
        if card_type is None:
            self.add_card_name_to_discard(self.headquarters[card_pos].get_name())
            del self.headquarters[card_pos]
            return 0
        if card_type == self.headquarters[card_pos].get_card_type():
            self.add_card_name_to_discard(self.headquarters[card_pos].get_name())
            del self.headquarters[card_pos]
            return 0
        return 1

    def play_unit_without_cost(self, card_to_play, forced_hq = False):
        if FindCard.check_card_type(card_to_play, "Army"):
            if forced_hq:
                self.headquarters.append(copy.deepcopy(card_to_play))
                self.cards.remove(card_to_play.get_name())
                print("Played card to HQ")
                return 0
            else:
                planet_id = ClickDetection.prompt_pos_planet()
                if not self.planets_in_play[planet_id]:
                    return -1
                self.cards_in_play[planet_id + 1].append(copy.deepcopy(card_to_play))
                self.cards.remove(card_to_play.get_name())
                print("Played card")
                return 0
        print("Not a unit")
        return -1

    def remove_card_from_play(self, planet_num, card_pos):
        # card_object = self.cards_in_play[planet_num + 1][card_pos]
        # self.discard_object(card_object)
        del self.cards_in_play[planet_num + 1][card_pos]

    def add_card_name_to_discard(self, card_name):
        self.discard.append(card_name)

    def add_card_to_deck(self, card_name):
        self.deck.append(card_name)

    def add_to_hq(self, card_object):
        self.headquarters.append(copy.deepcopy(card_object))

    def draw_card(self):
        if not self.deck:
            print("Deck is empty, you lose!")
        else:
            self.cards.append(self.deck[0])
            del self.deck[0]

    def draw_card_from_position_deck(self, n):
        if len(self.deck) < n:
            pass
        else:
            self.cards.append(self.deck[n])
            del self.deck[n]

    def top_n_cards(self, number):
        if len(self.deck) < number:
            return self.deck
        else:
            return self.deck[0:number]

    def remove_card_from_hand(self, card_pos):
        del self.cards[card_pos]

    def discard_card_from_hand(self, card_pos):
        self.discard.append(self.cards[card_pos])
        del self.cards[card_pos]

    def random_discard_from_hand(self):
        card_pos = random.randrange(len(self.cards))
        self.discard_card_from_hand(card_pos)

    def print_hand(self):
        print("Cards in hand:")
        for i in range(len(self.cards)):
            print(self.cards[i])

    def pygame_print_hand(self, game_screen):
        hand = self.get_cards()
        x_c = 300
        y_c = 595
        increment = 80
        if self.number == 2:
            x_c = 200
            y_c = 25
            increment = 80
        for i in range(len(hand)):
            card_image_name = "ResizedImages/" + hand[i] + ".jpg"
            for letter in card_image_name:
                if letter == " ":
                    card_image_name = card_image_name.replace(letter, "_")
            card_image = pygame.image.load(card_image_name).convert()
            game_screen.blit(card_image, (x_c, y_c))
            x_c += increment

    def pygame_print_hq(self, game_screen):
        hq = self.get_headquarters()
        x_c = 300
        y_c = 500
        increment = 80
        if self.number == 2:
            x_c = 300
            y_c = 125
            increment = 80
        for i in range(len(hq)):
            card_image_name = "ResizedImages/" + hq[i].get_name() + ".jpg"
            if hq[i].get_card_type() == "Warlord":
                if hq[i].get_bloodied():
                    card_image_name = "ResizedImages/" + hq[i].get_name() + "_bloodied.jpg"
            for letter in card_image_name:
                if letter == " ":
                    card_image_name = card_image_name.replace(letter, "_")
            card_image = pygame.image.load(card_image_name).convert()
            if not hq[i].get_ready():
                card_image = pygame.transform.rotate(card_image, 270)
            game_screen.blit(card_image, (x_c, y_c))
            card_type = hq[i].get_card_type()
            if card_type == "Army" or card_type == "Warlord" or card_type == "Token":
                damage = hq[i].get_damage()
                if 0 < damage < 10:
                    damage = str(damage)
                    damage_name = 'damagetokens/' + damage + '_Damage.png'
                    damage_image = pygame.image.load(damage_name).convert()
                    game_screen.blit(damage_image, (x_c + 10, y_c + 30))
            x_c += increment

    def print_deck(self):
        for i in range(len(self.deck)):
            print(self.deck[i])

    def print_headquarters(self):
        print("Headquarters:")
        for i in range(len(self.headquarters)):
            try:
                print(self.headquarters[i].get_name())
            except AttributeError:
                print("Attribute error")
                print(self.headquarters[i])

    def print_discard(self):
        for i in range(len(self.discard)):
            print(self.discard[i])

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def add_resources(self, amount):
        if amount > 0:
            self.resources += amount
            return 0
        else:
            print("Attempted to add", amount, "resources, may be an error")
            return -1

    def spend_resources(self, amount):
        if amount > self.resources:
            print("Attempted to spend more resources than you have.")
            return -1
        else:
            self.resources -= amount
            return 0
