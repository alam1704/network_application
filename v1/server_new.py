import socket

# create class server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 65432
ADDR = (HOST, PORT)
FORMAT = 'UTF-8'

sock.bind(ADDR)
sock.listen(1)

conn, address = sock.accept()

while True:
    # create  two separate methods
    user_input=input("Command: ")
    conn.sendall(user_input.encode(FORMAT))

    print(conn.recv(1024).decode())