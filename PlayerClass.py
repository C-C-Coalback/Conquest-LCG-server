import FindCard
from random import shuffle

class Player:
    def __init__(self, name, number):
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
        self.deck = []
        self.discard = []
        self.planets_in_play = [True, True, True, True, True, False, False]
        self.cards_in_play = [[] for _ in range(8)]

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

    def toggle_turn(self):
        self.has_turn = not self.has_turn

    def get_turn(self):
        return self.has_turn

    def print_position_active(self):
        while True:
            t = input("")
            if t == "STOP":
                break
            print("Player", self.number, "active position:", self.position_activated)

    def toggle_initiative(self):
        self.has_initiative = not self.has_initiative

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
