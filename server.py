import socket
from threading import *
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
        self.current_board_state = ""
        self.running = True
        self.c = Condition()
        self.start()

    def run(self):
        Thread(target=self.recv).start()
        Thread(target=self.send_info).start()

    def print_stored_1(self):
        print(self.stored_message_p_one)

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
                print("Stored message:", self.stored_message_p_one)
                self.c.release()
                if message == "QUIT":
                    self.running = False
                    self.client_one_sock.close()
        except ConnectionResetError:
            print("Existing connection closed by host")

    def send_info(self):
        try:
            while self.running:
                # self.c.acquire()
                # self.c.notify_all()
                self.current_board_state = input("Enter message:")
                message = self.current_board_state
                # self.c.release()
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
                self.client_one_sock.send(bytes(message, 'UTF-8'))
        except OSError:
            print("Socket closed")

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
        # Thread(target=self.send_info).start()

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