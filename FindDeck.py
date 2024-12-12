from Inits import OrksCardsInit, ChaosCardsInit, NeutralCardsInit
from Inits.FinalCardInit import final_card_init

orks_card_array = OrksCardsInit.orks_cards_init()
chaos_card_array = ChaosCardsInit.chaos_cards_init()
neutral_card_array = NeutralCardsInit.neutral_cards_init()
final_card_array = final_card_init()
card_array = orks_card_array + chaos_card_array + neutral_card_array + final_card_array

def find_card(card_to_find):
    i = 0
    while card_array[i].get_shields() != -1:
        print(card_array[i].get_name())
        if card_to_find == card_array[i].get_name():
            # print("Card found! :", orks_card_array[i].get_name())
            return card_array[i]
        else:
            i = i + 1
    return card_array[i]