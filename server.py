import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8089))
server_socket.listen(20) # become a server socket, maximum 5 connections

while True:
    connection, address = server_socket.accept()
    buf = connection.recv(64)
    string = buf.decode("utf-8")
    string = string.split(sep="#")
    if len(string) > 0:
        print(string)
        for i in range(len(string)):
            print(string[i])
        break