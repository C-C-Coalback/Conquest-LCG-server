import FindCard

def load_deck(deck_string, player_object):
    print(deck_string)
    deck_string += "#"
    current_name = ""
    position = 1
    first_card = True
    while position < len(deck_string):
        while deck_string[position] != "#":
            current_name += deck_string[position]
            position += 1
        if first_card:
            player_object.add_to_hq(FindCard.find_card(current_name))
            first_card = False
        else:
            player_object.add_card_to_deck(current_name)
        current_name = ""
        position += 1
