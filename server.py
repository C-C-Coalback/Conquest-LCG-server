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