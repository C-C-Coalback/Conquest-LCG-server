from GameClass import Game
from threading import *
import random
import pygame
import HoldingArrays
import PlayerClass
from UseInits import *


class Client:
    def __init__(self, class_socket, class_address):
        self.sock = class_socket
        self.addr = class_address
        self.stored_message = ""
        self.display_name = ""
        self.currently_requesting_from = -1
        self.sent_a_req_and_is_awaiting_response = False
        self.currently_received_request = False
        self.running = True
        self.c = Condition()

    def send_lobby(self):
        self.c.acquire()
        self.c.notify_all()
        message = ""
        for i in range(len(HoldingArrays.client_array)):
            if HoldingArrays.client_array[i].get_display_name() != "":
                message += "#" + HoldingArrays.client_array[i].get_display_name()
        message = "LOBBY" + message
        self.sock.send(bytes(message, "UTF-8"))

    def send_display_name(self):
        self.c.acquire()
        self.c.notify_all()
        print(self.display_name)
        self.sock.send(bytes(self.display_name, "UTF-8"))
        self.c.release()

    def send_game_request(self, name):
        message = "GAME INVITE#" + name
        self.currently_received_request = True
        self.sock.send(bytes(message, "UTF-8"))

    def set_display_name(self, name):
        self.display_name = name

    def get_display_name(self):
        return self.display_name

    def recv(self):
        try:
            while self.running:
                message = self.sock.recv(1024).decode()
                if not message:
                    break
                print(self.display_name, 'Client sent:', message)
                self.c.acquire()
                self.c.notify_all()
                split_message = message.split(sep="#")
                self.stored_message = split_message
                print("Stored message:", self.stored_message)
                self.c.release()
                if message == "QUIT":
                    self.running = False
                    self.sock.close()
                if message == "SWITCH TO GAME MODE":
                    self.c.acquire()
                    self.c.notify_all()
                    self.running = False
                    self.c.release()
                if message == "REQUEST OWN USERNAME":
                    self.send_display_name()
                if message == "REQUEST LOBBY":
                    self.send_lobby()
                if len(split_message) == 2:
                    if split_message[0] == "SET NAME":
                        self.set_display_name(split_message[1])
                    if split_message[0] == "BEGIN GAME":
                        for i in range(len(HoldingArrays.client_array)):
                            if HoldingArrays.client_array[i].get_display_name() == split_message[1]:
                                print("Preparing to make game")
                                if self.get_display_name() == split_message[1]:
                                    print("issue")
                                temp = random.randint(1, 2)
                                print(temp)
                                if temp == 1:
                                    Game(self, HoldingArrays.client_array[i])
                                else:
                                    Game(HoldingArrays.client_array[i], self)
                                self.c.acquire()
                                self.c.notify_all()
                                self.sock.send(bytes("GAME IS STARTING", "UTF-8"))
                                HoldingArrays.client_array[i].sock.send(bytes("GAME IS STARTING", "UTF-8"))
                                self.running = False
                                HoldingArrays.client_array[i].running = False
                                self.c.notify_all()
                                self.c.release()
                                print("Running:", self.running, HoldingArrays.client_array[i].running)
                                break
                    if split_message[0] == "REFUSE REQUEST":
                        for i in range(len(HoldingArrays.client_array)):
                            if HoldingArrays.client_array[i].get_display_name() == split_message[1]:
                                print("Refusing received request")
                                self.currently_received_request = False
                                HoldingArrays.client_array[i].sent_a_req_and_is_awaiting_response = False
                                self.sock.send(bytes("REQUEST WAS REFUSED", "UTF-8"))
                                print(self.currently_received_request)
                                print(self.sent_a_req_and_is_awaiting_response)
                                print(HoldingArrays.client_array[i].currently_received_request)
                                print(HoldingArrays.client_array[i].sent_a_req_and_is_awaiting_response)
                                HoldingArrays.client_array[i].currently_requesting_from = -1
                                break
                    if split_message[0] == "REQUEST MATCH" and not self.sent_a_req_and_is_awaiting_response \
                            and not self.currently_received_request:
                        if split_message[1] != self.display_name:
                            for i in range(len(HoldingArrays.client_array)):
                                if HoldingArrays.client_array[i].get_display_name() == split_message[1]:
                                    print("Sending game request to", HoldingArrays.client_array[i].get_display_name())
                                    HoldingArrays.client_array[i].send_game_request(self.display_name)
                                    self.sent_a_req_and_is_awaiting_response = True
                                    self.currently_requesting_from = i
                                    break

        except ConnectionResetError:
            print("Existing connection closed by host")
