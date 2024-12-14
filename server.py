import socket
from GameClass import Client
from threading import *


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8089))
game_array = []
client_array = []
server_socket.listen(20)

print('server started and listening')
i = 0
while True:
    connection, address = server_socket.accept()
    new_client = Client(connection, address)
    client_array.append(new_client)
    client_array[i].stored_message = "test"
    Thread(target=client_array[i].recv).start()
    i += 1
    if i == 2:
        break
