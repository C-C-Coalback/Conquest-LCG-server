import socket
from ClientClass import Client
from threading import *
import HoldingArrays


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8089))

server_socket.listen(20)

print('server started and listening')
i = 0
while True:
    connection, address = server_socket.accept()
    new_client = Client(connection, address)
    HoldingArrays.client_array.append(new_client)
    HoldingArrays.client_array[i].stored_message = "test"
    Thread(target=HoldingArrays.client_array[i].recv).start()
    i += 1
    if i == 2:
        break
