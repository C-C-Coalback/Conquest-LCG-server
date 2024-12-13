import FindCard


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

    def setup_player(self, deck_list, planet_array):
        self.headquarters.append(FindCard.find_card(deck_list[1]))
        self.deck = deck_list[2:]
        self.cards_in_play[0] = planet_array
        self.resources = self.headquarters[0].get_starting_resources()
        print(self.resources)
        print(self.deck)
        print(self.cards_in_play)


