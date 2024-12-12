import socket
from threading import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8089))

class Client(Thread):
    def __init__(self, class_socket, class_address):
        Thread.__init__(self)
        self.sock = class_socket
        self.addr = class_address
        self.stored_message = ""
        self.running = True
        self.start()

    def run(self):
        Thread(target=self.recv).start()
        Thread(target=self.send_info).start()

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
                self.stored_message = message.split(sep="#")
                print("Stored message:", self.stored_message)
                if message == "QUIT":
                    self.running = False
                    self.sock.close()
        except ConnectionResetError:
            print("Existing connection closed by host")

server_socket.listen(20)
print ('server started and listening')
while True:
    connection, address = server_socket.accept()
    Client(connection, address)
    keep_server = "n"
    if keep_server == "n":
        break