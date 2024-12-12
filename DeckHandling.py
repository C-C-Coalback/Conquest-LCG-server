import PromptText
from Inits import OrksCardsInit, ChaosCardsInit, NeutralCardsInit, FinalCardInit
import FindCard
from Drawing import draw_current_deck

orks_card_array = OrksCardsInit.orks_cards_init()
chaos_card_array = ChaosCardsInit.chaos_cards_init()
neutral_card_array = NeutralCardsInit.neutral_cards_init()
final_card_array = FinalCardInit.final_card_init()
card_array = orks_card_array + chaos_card_array + neutral_card_array + final_card_array



def write_deck_into_file(deck_string):
    file = open("deck_storage.txt", "a")
    file.write(deck_string)
    file.write("\n")
    file.close()

def check_ally(req_faction, ally):
    faction_wheel = ["Astra Militarum", "Space Marines", "Tau", "Eldar",
                     "Dark Eldar", "Chaos", "Orks"]
    pos_req_faction = -1
    pos_ally = -1
    for pos in [pos for pos,faction in enumerate(faction_wheel) if faction == req_faction]:
        pos_req_faction = pos
    for pos in [pos for pos,faction in enumerate(faction_wheel) if faction == ally]:
        pos_ally = pos
    if pos_req_faction == -1 or pos_ally == -1:
        return False
    pos_distance = abs(pos_req_faction - pos_ally)
    if pos_distance == 6 or pos_distance == 1:
        return True
    return False

def pygame_create_deck(game_screen):
    warlord_to_find = PromptText.prompt_text(game_screen, "Enter Warlord Name")
    warlord_card = FindCard.find_card(warlord_to_find)
    while not FindCard.check_card_type(warlord_card, "Warlord"):
        if FindCard.check_card_type(warlord_card, ""):
            print("Card not found.")
        else:
            print("Card is not a Warlord, card is a(n)", warlord_card.get_card_type(), "card")
        warlord_to_find = PromptText.prompt_text(game_screen, "Card does not exist/"
                                                              "is not a Warlord"
                                                              "\nEnter Warlord Name")
        warlord_card = FindCard.find_card(warlord_to_find)
    print("Card is a warlord!")
    deck_to_write = ""
    required_faction = ""
    ally = ""
    if warlord_card.get_name() == "Nazdreg":
        required_faction = "Orks"
        ally = PromptText.prompt_text(game_screen, "Enter faction to ally with")
        while not check_ally(required_faction, ally):
            ally = PromptText.prompt_text(game_screen, "Can not ally with faction\n"
                                                       "Enter faction to ally with")
        deck_to_write = PromptText.prompt_text(game_screen, "Enter a name for the deck")
        deck_to_write += "#Nazdreg"
        deck_to_write += "#Nazdreg's Flash Gitz"
        deck_to_write += "#Nazdreg's Flash Gitz"
        deck_to_write += "#Nazdreg's Flash Gitz"
        deck_to_write += "#Nazdreg's Flash Gitz"
        deck_to_write += "#Kraktoof Hall"
        deck_to_write += "#Bigga is Betta"
        deck_to_write += "#Bigga is Betta"
        deck_to_write += "#Cybork Body"
    if warlord_card.get_name() == "Zarathur, High Sorcerer":
        required_faction = "Chaos"
        ally = PromptText.prompt_text(game_screen, "Enter faction to ally with")
        while not check_ally(required_faction, ally):
            ally = PromptText.prompt_text(game_screen, "Can not ally with faction\n"
                                                       "Enter faction to ally with")
        deck_to_write = PromptText.prompt_text(game_screen, "Enter a name for the deck")
        deck_to_write += "#Zarathur, High Sorcerer"
        deck_to_write += "#Zarathur's Flamers"
        deck_to_write += "#Zarathur's Flamers"
        deck_to_write += "#Zarathur's Flamers"
        deck_to_write += "#Zarathur's Flamers"
        deck_to_write += "#Shrine of Warpflame"
        deck_to_write += "#Infernal Gateway"
        deck_to_write += "#Infernal Gateway"
        deck_to_write += "#Mark of Chaos"
    cards_added_array = []
    deck_size = 8
    while deck_size < 13:
        card_to_add = PromptText.prompt_text(game_screen, "Enter card name to add")
        if card_to_add == "Current Deck":
            draw_current_deck(game_screen, deck_to_write)
        card_object = FindCard.find_card(card_to_add)
        if FindCard.check_faction(card_object, required_faction):
            if FindCard.check_loyalty(card_object, "Signature"):
                print("Card is a signature card, may not be added.")
            else:
                already_added = False
                for cards_added in cards_added_array:
                    if cards_added == card_object.get_name():
                        already_added = True
                if already_added:
                    print("At least one copy of this card has already been added.")
                else:
                    copies_to_add = int(PromptText.prompt_text(game_screen, "Enter number of copies"))
                    if copies_to_add > 3:
                        print("Can only add a maximum of 3 copies of a card to a deck.")
                    elif copies_to_add < 0:
                        print("Invalid number entered.")
                    elif copies_to_add == 0:
                        print("Card not added.")
                    else:
                        print("Adding", copies_to_add, "copies of", card_object.get_name())
                        while copies_to_add != 0:
                            deck_to_write += "#"
                            deck_to_write += card_object.get_name()
                            deck_size = deck_size + 1
                            copies_to_add = copies_to_add - 1
                        cards_added_array.append(card_object.get_name())
        elif FindCard.check_faction(card_object, ally) or FindCard.check_faction(card_object, "Neutral"):
            if FindCard.check_loyalty(card_object, "Common"):
                already_added = False
                for cards_added in cards_added_array:
                    if cards_added == card_object.get_name():
                        already_added = True
                if already_added:
                    print("At least one copy of this card has already been added.")
                else:
                    copies_to_add = int(PromptText.prompt_text(game_screen, "Enter number of copies"))
                    if copies_to_add > 3:
                        print("Can only add a maximum of 3 copies of a card to a deck.")
                    elif copies_to_add < 0:
                        print("Invalid number entered.")
                    elif copies_to_add == 0:
                        print("Card not added.")
                    else:
                        print("Adding", copies_to_add, "copies of", card_object.get_name())
                        while copies_to_add != 0:
                            deck_to_write += "#"
                            deck_to_write += card_object.get_name()
                            deck_size = deck_size + 1
                            copies_to_add = copies_to_add - 1
                        cards_added_array.append(card_object.get_name())

    write_deck_into_file(deck_to_write)
