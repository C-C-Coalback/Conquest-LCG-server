import FindCard
from random import shuffle
import pygame
import copy


class Player:
    def __init__(self, name, number, c):
        self.number = number
        self.name_player = name
        self.position_activated = []
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
        self.c = c
        self.deck = []
        self.discard = []
        self.planets_in_play = [True, True, True, True, True, False, False]
        self.cards_in_play = [[] for _ in range(8)]
        self.bonus_boxes = ""
        self.extra_text = "No advice"

    def setup_player(self, deck_list, planet_array):
        self.headquarters.append(FindCard.find_card(deck_list[1]))
        self.deck = deck_list[2:]
        self.shuffle_deck()
        self.cards_in_play[0] = planet_array
        self.resources = self.headquarters[0].get_starting_resources()
        for i in range(self.headquarters[0].get_starting_cards()):
            self.draw_card()
        print(self.resources)
        print(self.deck)
        print(self.cards_in_play)
        print(self.cards)

    def get_headquarters(self):
        return self.headquarters

    def toggle_turn(self):
        self.has_turn = not self.has_turn

    def get_turn(self):
        return self.has_turn

    def set_turn(self, new_turn):
        self.has_turn = new_turn

    def get_phase(self):
        return self.phase

    def set_phase(self, new_phase):
        self.phase = new_phase

    def get_top_card_discard(self):
        if not self.discard:
            return "NONE"
        else:
            return self.discard[-1]

    def spend_resources(self, amount):
        if amount > self.resources:
            return False
        else:
            self.resources = self.resources - amount
            return True

    def take_deploy_turn(self):
        self.position_activated = []
        while True:
            pygame.time.wait(500)
            self.c.acquire()
            self.c.notify_all()
            current_active = self.position_activated
            self.c.release()
            self.set_turn(True)
            self.extra_text = "Deploy turn"
            if len(current_active) > 0:
                if current_active[0] == "PASS":
                    print("PASS NEEDED")
                    self.set_turn(False)
                    return True
                if len(current_active) > 1:
                    print("GOT HERE + :", current_active)
                    if current_active[1] == "Hand" and int((current_active[0])[1]) == self.number:
                        if int(current_active[2]) < len(self.cards):
                            print("Card needs to be deployed")
                            print("Position of card: Player", current_active[0], "Hand pos:", current_active[2])
                            self.bonus_boxes = "Hand/" + current_active[0] + "/" + current_active[2] + "/green"
                            self.c.acquire()
                            self.c.notify_all()
                            self.position_activated = []
                            self.c.notify_all()
                            self.c.release()
                            card_object = FindCard.find_card(self.cards[int(current_active[2])])
                            if card_object.get_card_type() == "Army":
                                print("Card is an army unit")
                                self.extra_text = "Choose planet"
                                ret_val = self.select_planet_to_play_card(card_object)
                                self.bonus_boxes = ""
                                if ret_val != "PASS" and ret_val != "FAIL":
                                    print("Successfully played card")
                                    self.set_turn(False)
                                    return False
                                print("Cancelling playing the card.")
                            if card_object.get_card_type() == "Support":
                                print("Card is a support")
                                ret_val = self.play_card(None, card_object)
                                self.bonus_boxes = ""
                                if ret_val != "PASS" and ret_val != "FAIL":
                                    print("Successfully played card")
                                    return True
                                print("Cancelling playing the card.")

    def select_planet_to_play_card(self, card):
        while True:
            pygame.time.wait(125)
            current_active = self.position_activated
            if len(current_active) > 0:
                if current_active[0] == "PASS":
                    return "PASS"
                if current_active[0] == "Planet":
                    int_planet = int(current_active[1])
                    print("position of planet to deploy unit:", int_planet)
                    return self.play_card(int_planet, card)

    def play_card(self, position, card):
        self.c.acquire()
        if position is None:
            if self.spend_resources(card.get_cost()):
                self.add_to_hq(card)
                self.cards.remove(card.get_name())
                print("Played card to HQ")
                self.c.notify_all()
                self.c.release()
                return "SUCCESS"
            print("Insufficient resources")
            self.c.notify_all()
            self.c.release()
            return "FAIL"
        if not self.planets_in_play[position]:
            self.c.notify_all()
            self.c.release()
            return "FAIL"
        if self.spend_resources(card.get_cost()):
            self.cards_in_play[position + 1].append(copy.deepcopy(card))
            self.cards.remove(card.get_name())
            self.c.notify_all()
            self.c.release()
            return "SUCCESS"
        print("Insufficient resources")
        self.c.notify_all()
        self.c.release()
        return "FAIL"

    def commit_warlord_step(self):
        self.position_activated = []
        self.set_turn(True)
        while True:
            pygame.time.wait(125)
            self.c.acquire()
            self.c.notify_all()
            current_active = self.position_activated
            self.c.release()
            self.set_turn(True)
            self.extra_text = "Commit Warlord"
            if len(current_active) > 0:
                if current_active[0] == "Planet":
                    int_planet = int(current_active[1])
                    print("position of planet to commit warlord:", int_planet)
                    self.commit_warlord_to_planet(int_planet + 1)
                    self.set_turn(False)
                    return True



    def commit_warlord_to_planet(self, planet_pos):
        headquarters_list = self.get_headquarters()
        for i in range(len(headquarters_list)):
            if headquarters_list[i].get_card_type() == "Warlord":
                print(headquarters_list[i].get_name())
                self.cards_in_play[planet_pos].append(copy.deepcopy(headquarters_list[i]))
                self.headquarters.remove(headquarters_list[i])
                # self.commit_units_to_planet(planet_id)

    def print_position_active(self):
        while True:
            t = input("")
            if t == "STOP":
                break
            print("Player", self.number, "active position:", self.position_activated)

    def add_to_hq(self, card_object):
        self.headquarters.append(copy.deepcopy(card_object))

    def toggle_initiative(self):
        self.has_initiative = not self.has_initiative

    def get_initiative(self):
        return self.has_initiative

    def shuffle_deck(self):
        shuffle(self.deck)

    def get_active_position(self):
        return self.position_activated

    def set_active_position(self, new_val):
        self.position_activated = new_val

    def get_resources(self):
        return self.resources

    def get_planets_in_play_for_message(self):
        message = "#"
        for i in range(7):
            message += self.cards_in_play[0][i]
            if i != 6:
                message += "/"
        message += "#"
        for i in range(7):
            message += str(self.planets_in_play[i])
            if i != 6:
                message += "/"
        return message

    def get_hand_for_message(self):
        message = "#"
        for i in range(len(self.cards)):
            message += self.cards[i]
            if i != len(self.cards) - 1:
                message += "/"
        return message

    def get_hq_for_message(self):
        message = "#"
        if len(self.headquarters) == 0:
            message += "NONE"
        for i in range(len(self.headquarters)):
            message += self.headquarters[i].get_name()
            c_t = self.headquarters[i].get_card_type()
            message += "("
            if c_t == "Warlord":
                if self.headquarters[i].get_bloodied_state():
                    message += "B"
                else:
                    message += "H"
            else:
                message += "H"
            message += "!"
            if self.headquarters[i].get_ready():
                message += "R"
            else:
                message += "E"
            message += "!"
            damage = 0
            if c_t == "Warlord" or c_t == "Army" or c_t == "Token":
                damage += self.headquarters[i].get_damage()
            message += str(damage) + ")"
            if i != len(self.headquarters) - 1:
                message += "/"
        return message

    def get_all_planets_for_message(self):
        message = ""
        planet_num = 1
        while planet_num < 8:
            message += self.get_one_planet_for_message(planet_num)
            planet_num += 1
        return message


    def get_one_planet_for_message(self, planet_pos):
        message = "#"
        if len(self.cards_in_play[planet_pos]) == 0:
            message += "NONE"
        for i in range(len(self.cards_in_play[planet_pos])):
            message += self.cards_in_play[planet_pos][i].get_name()
            c_t = self.cards_in_play[planet_pos][i].get_card_type()
            message += "("
            if c_t == "Warlord":
                if self.cards_in_play[planet_pos][i].get_bloodied_state():
                    message += "B"
                else:
                    message += "H"
            else:
                message += "H"
            message += "!"
            if self.cards_in_play[planet_pos][i].get_ready():
                message += "R"
            else:
                message += "E"
            message += "!"
            damage = 0
            # if c_t == "Warlord" or c_t == "Army" or c_t == "Token":
            damage += self.cards_in_play[planet_pos][i].get_damage()
            message += str(damage) + ")"
            if i != len(self.cards_in_play[planet_pos]) - 1:
                message += "/"
        return message

    def draw_card(self):
        if not self.deck:
            print("Deck is empty, you lose!")
        else:
            self.cards.append(self.deck[0])
            del self.deck[0]

