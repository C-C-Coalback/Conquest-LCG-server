import FindCard
import PromptText


def find_pygame_deck(input_window):
    file_to_read = open("deck_storage.txt", "r")
    deck_name = PromptText.prompt_text(input_window, "Enter deck name")
    file_text = file_to_read.read()
    pos = 0
    current_deck = ""
    while pos < len(file_text):
        while file_text[pos] != "#":
            current_deck += file_text[pos]
            pos += 1
        if current_deck == deck_name:
            print("Deck found")
            file_to_read.close()
            return read_deck(pos)
        else:
            while file_text[pos] != "\n":
                pos += 1
            pos += 1
            current_deck = ""
    file_to_read.close()
    print("Deck not found")
    return find_pygame_deck(input_window)


def read_deck(pos):
    file_to_read = open("deck_storage.txt", "r")
    deck_contents = ""
    file_text = file_to_read.read()
    while file_text[pos] != "\n":
        deck_contents += file_text[pos]
        pos += 1
    return deck_contents


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
