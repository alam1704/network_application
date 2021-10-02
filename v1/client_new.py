import socket

# create client class

HOST = '127.0.0.1'
PORT = 65432
ADDR = (HOST, PORT)
FORMAT = 'UTF-8'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(ADDR)

while True:
    # create two separate functions
    print(sock.recv(1024).decode())
    user_input=input("Command: ")
    sock.sendall(user_input.encode(FORMAT))
