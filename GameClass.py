from threading import *
import PlayerClass
import random
import pygame
from UseInits import *
from Phases import DeployPhase
import HoldingArrays


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


class Game(Thread):
    def __init__(self, client_one, client_two):
        Thread.__init__(self)
        self.client_one_sock = client_one.sock
        self.client_one_addr = client_one.addr
        self.stored_message_p_one = client_one.stored_message
        self.client_two_sock = client_two.sock
        self.client_two_addr = client_two.addr
        self.stored_message_p_two = client_two.stored_message
        self.name_1 = client_one.display_name
        self.name_2 = client_two.display_name
        self.stored_deck_1 = None
        self.stored_deck_2 = None
        self.p1 = None
        self.p2 = None
        self.current_board_state = ""
        self.running = True
        self.c = Condition()
        self.start()

    def run(self):
        print("Thread started")
        planets_in_play_list = create_planets(planet_array)
        self.p1 = PlayerClass.Player(self.name_1, 1)
        self.p2 = PlayerClass.Player(self.name_2, 2)
        Thread(target=self.recv_1).start()
        Thread(target=self.recv_2).start()
        Thread(target=self.send_current_board_state_loop).start()
        print("waiting p1 deck")
        self.wait_deck_1()
        print("waiting p2 deck")
        self.wait_deck_2()
        print("not waiting on decks")
        self.p1.setup_player(self.stored_deck_1, planets_in_play_list)
        self.p2.setup_player(self.stored_deck_2, planets_in_play_list)
        self.p2.toggle_turn()
        self.p2.toggle_initiative()
        Thread(target=self.auto_update_board_loop).start()
        Thread(target=self.auto_update_stored_1).start()
        Thread(target=self.auto_update_stored_2).start()
        # Thread(target=self.temp_loop).start()
        DeployPhase.deploy_phase(self.p1, self.p2)

    def play_game(self):
        pass

    def temp_loop(self):
        self.p1.print_position_active()

    def auto_update_stored_1(self):
        while self.running:
            pygame.time.wait(200)
            self.c.acquire()
            self.c.notify_all()
            self.p1.set_active_position(self.stored_message_p_one)
            self.c.release()

    def auto_update_stored_2(self):
        while self.running:
            pygame.time.wait(200)
            self.c.acquire()
            self.c.notify_all()
            self.p1.set_active_position(self.stored_message_p_two)
            self.c.release()

    def print_stored_1(self):
        print(self.stored_message_p_one)

    def wait_deck_1(self):
        temp = True
        while temp:
            pygame.time.wait(100)
            self.c.acquire()
            self.c.notify_all()
            if self.stored_deck_1 is not None:
                temp = False
            self.c.release()

    def wait_deck_2(self):
        temp = True
        while temp:
            pygame.time.wait(100)
            self.c.acquire()
            self.c.notify_all()
            if self.stored_deck_2 is not None:
                temp = False
            self.c.release()

    def print_current_board_state(self):
        print(self.current_board_state)

    def recv_1(self):
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

    def recv_2(self):
        try:
            while self.running:
                message = self.client_two_sock.recv(1024).decode()
                if not message:
                    break
                print('Client sent:', message)
                self.c.acquire()
                self.c.notify_all()
                self.stored_message_p_two = message.split(sep="#")
                string_for_further_use = self.stored_message_p_two
                print("Stored message:", self.stored_message_p_two)
                self.c.release()
                if len(string_for_further_use) > 0:
                    if string_for_further_use[0] == "LOAD DECK":
                        print("Begin loading deck")
                        self.stored_deck_2 = string_for_further_use
                if message == "QUIT":
                    self.c.acquire()
                    self.c.notify_all()
                    self.running = False
                    self.client_two_sock.close()
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
                self.client_one_sock.send(bytes(message, 'UTF-8'))
                self.client_two_sock.send(bytes(message, 'UTF-8'))
                self.c.release()
        except OSError:
            self.c.acquire()
            self.c.notify_all()
            self.running = False
            self.c.release()
            print("Socket closed")

    def auto_update_board_loop(self):
        while self.running:
            pygame.time.wait(3000)
            self.c.acquire()
            self.c.notify_all()
            message = "10246#"
            message += str(self.p1.get_resources()) + "#" + str(self.p2.get_resources())
            message += self.p1.get_planets_in_play_for_message()
            message += self.p1.get_hand_for_message()
            message += self.p2.get_hand_for_message()
            message += self.p1.get_hq_for_message()
            message += self.p2.get_hq_for_message()
            message += self.p1.get_all_planets_for_message()
            message += self.p2.get_all_planets_for_message()
            message = message + "#" + self.p1.get_top_card_discard() + "#" + self.p2.get_top_card_discard()
            print(message)
            self.p1.toggle_turn()
            self.current_board_state = message
            self.c.release()
