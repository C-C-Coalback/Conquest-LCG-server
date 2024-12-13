import socket
from threading import *
from Inits import OrksCardsInit, ChaosCardsInit, NeutralCardsInit, FinalCardInit, PlanetCardsInit
import PlayerClass
import pygame.time
import random

orks_card_array = OrksCardsInit.orks_cards_init()
chaos_card_array = ChaosCardsInit.chaos_cards_init()
neutral_card_array = NeutralCardsInit.neutral_cards_init()
final_card_array = FinalCardInit.final_card_init()
card_array = orks_card_array + chaos_card_array + neutral_card_array + final_card_array
planet_array = PlanetCardsInit.planet_cards_init()
faction_wheel = ["Astra Militarum", "Space Marines", "Tau", "Eldar",
                 "Dark Eldar", "Chaos", "Orks", "Astra Militarum", "Space Marines"]

def create_planets(planet_array_objects):
    planet_names = []
    for i in range(10):
        string = planet_array_objects[i].get_name()
        planet_names.append(string)
    random.shuffle(planet_names)
    planets_in_play_return = []
    for i in range(7):
        planets_in_play_return.append(planet_names[i])
    return planets_in_play_return

# import pygame

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8089))
game_array = []
client_array = []

class Game(Thread):
    def __init__(self, client_one):
        Thread.__init__(self)
        self.client_one_sock = client_one.sock
        self.client_one_addr = client_one.addr
        self.stored_message_p_one = client_one.stored_message
        self.stored_deck_1 = None
        self.p1 = None
        self.current_board_state = ""
        self.running = True
        self.c = Condition()
        self.start()

    def run(self):
        planets_in_play_list = create_planets(planet_array)
        self.p1 = PlayerClass.Player("Abe", 1)
        Thread(target=self.recv).start()
        Thread(target=self.send_current_board_state_loop).start()
        Thread(target=self.manual_update_board_loop).start()
        self.wait_deck()
        self.p1.setup_player(self.stored_deck_1, planets_in_play_list)

    def print_stored_1(self):
        print(self.stored_message_p_one)

    def wait_deck(self):
        temp = True
        while temp:
            pygame.time.wait(100)
            self.c.acquire()
            self.c.notify_all()
            if self.stored_deck_1 is not None:
                temp = False
            self.c.release()

    def print_current_board_state(self):
        print(self.current_board_state)

    def recv(self):
        try:
            while self.running:
                message = self.client_one_sock.recv(1024).decode()
                if not message:
                    break
                print('Client sent:', message)
                self.c.acquire()
                self.c.notify_all()
                self.stored_message_p_one = message.split(sep="#")
                string_for_further_use = self.stored_message_p_one
                print("Stored message:", self.stored_message_p_one)
                self.c.release()
                if len(string_for_further_use) > 0:
                    if string_for_further_use[0] == "LOAD DECK":
                        print("Begin loading deck")
                        self.stored_deck_1 = string_for_further_use
                if message == "QUIT":
                    self.c.acquire()
                    self.c.notify_all()
                    self.running = False
                    self.client_one_sock.close()
                    self.c.release()
        except ConnectionResetError:
            print("Existing connection closed by host")

    def send_current_board_state_loop(self):
        try:
            while self.running:
                _ = pygame.time.wait(3000)
                self.c.acquire()
                self.c.notify_all()
                message = self.current_board_state
                self.c.release()
                self.client_one_sock.send(bytes(message, 'UTF-8'))
        except OSError:
            self.c.acquire()
            self.c.notify_all()
            self.running = False
            self.c.release()
            print("Socket closed")

    def update_current_board_state_string(self, new_state):
        self.c.acquire()
        self.c.notify_all()
        self.current_board_state = new_state
        self.c.release()

    def manual_update_board_loop(self):
        while self.running:
            message = input("Enter text:")
            if message == "TEST BIG":
                message = ("10246#4#8#Plannum/Tarrus/Osus IV/Y'varn/Ferrin/Barlus/Iridial"
                           "#True/True/True/True/True/False/False#Nazdreg's Flash Gitz"
                           "/Nazdreg's Flash Gitz/Nazdreg's Flash Gitz/Kraktoof Hall/"
                           "Bigga is Betta/Cybork Body/Nazdreg's Flash Gitz#Bigga is Betta/"
                           "Cybork Body/Nazdreg's Flash Gitz/Nazdreg's Flash Gitz"
                           "/Kraktoof Hall/Nazdreg's Flash Gitz/Nazdreg's Flash Gitz"
                           "#Nazdreg(B!E!2)/Nazdreg's Flash Gitz(H!E!1)#Nazdreg(H!E!3)/Nazdreg's Flash Gitz(H!R!2)"
                           "#Chaos Fanatics(H!E!0)/Possessed(H!R!2)/Chaos Fanatics(H!R!0)#NONE#NONE#Shoota Mob(H!R!0)#NONE#NONE#Goff Boyz(H!R!1)"
                           "#Alpha Legion Infiltrator(H!R!0)/Goff Boyz(H!R!0)/Goff Boyz(H!R!1)#Goff Boyz(H!E!1)#NONE"
                           "#NONE#NONE#Rogue Trader(H!R!0)#NONE")
            self.c.acquire()
            self.c.notify_all()
            self.current_board_state = message
            self.c.release()
            print(self.running)

class Client(Thread):
    def __init__(self, class_socket, class_address):
        Thread.__init__(self)
        self.sock = class_socket
        self.addr = class_address
        self.stored_message = ""
        self.running = True
        self.c = Condition()
        self.start()

    def run(self):
        Thread(target=self.recv).start()

    def get_stored_message(self):
        self.c.acquire()
        self.c.notify_all()
        message = self.stored_message
        self.c.release()
        return message

    def recv(self):
        try:
            while self.running:
                message = self.sock.recv(1024).decode()
                if not message:
                    break
                print('Client sent:', message)
                self.c.acquire()
                self.c.notify_all()
                self.stored_message = message.split(sep="#")
                print("Stored message:", self.stored_message)
                self.c.release()
                if message == "QUIT":
                    self.running = False
                    self.sock.close()
                if message == "BEGIN GAME":
                    self.running = False
                    Game(self)
        except ConnectionResetError:
            print("Existing connection closed by host")

server_socket.listen(20)
print ('server started and listening')
while True:
    connection, address = server_socket.accept()
    new_client = Client(connection, address)
    client_array.append(new_client)
    client_array[0].stored_message = "test"
    keep_server = "n"
    if keep_server == "n":
        break