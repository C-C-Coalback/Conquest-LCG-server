import socket
from threading import *
import pygame

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8089))

class Game:
    def __init__(self, client_one):
        self.client_one_sock = client_one.sock
        self.client_one_addr = client_one.addr
        self.stored_message_p_one = client_one.stored_message
        self.running = True
        self.c = Condition()

    def print_stored_1(self):
        print(self.stored_message_p_one)

class LittleGame:
    def __init__(self, client_one):
        self.client_one = client_one

    def get_stored_1(self):
        return self.client_one.stored_message

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
        Thread(target=self.send_info).start()

    def get_stored_message(self):
        self.c.acquire()
        self.c.notify_all()
        message = self.stored_message
        self.c.release()
        return message

    def send_info(self):
        try:
            while self.running:
                message = input("Enter message:")
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
                self.sock.send(bytes(message, 'UTF-8'))
        except OSError:
            print("Socket closed")

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
        except ConnectionResetError:
            print("Existing connection closed by host")

server_socket.listen(20)
print ('server started and listening')
client_array = []
game_array = []
while True:
    connection, address = server_socket.accept()
    new_client = Client(connection, address)
    client_array.append(new_client)
    client_array[0].stored_message = "test"
    game_object = Game(client_array[0])
    print(game_object.print_stored_1())
    _ = pygame.time.wait(1000)
    keep_server = "n"
    if keep_server == "n":
        break