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
        self.start()

    def run(self):
        while 1:
            message = self.sock.recv(1024).decode()
            print('Client sent:', message)
            self.sock.send(bytes("Confirm received", 'UTF-8'))
            self.stored_message = message.split(sep="#")
            print("Stored message:", self.stored_message)

server_socket.listen(20)
print ('server started and listening')
while True:
    connection, address = server_socket.accept()
    Client(connection, address)