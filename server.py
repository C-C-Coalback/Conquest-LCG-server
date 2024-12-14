import socket
from GameClass import Client


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8089))
game_array = []
client_array = []
server_socket.listen(20)

print('server started and listening')
while True:
    connection, address = server_socket.accept()
    new_client = Client(connection, address)
    client_array.append(new_client)
    client_array[0].stored_message = "test"
    keep_server = "n"
    if keep_server == "n":
        break