import socket
import sys

SERVER = ''
PORT = 65432
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'

# create socket object

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("[FAILED]: Could not create socket")

script, host = sys.argv #script will be client.py. Host can be generated running the get_host.py file on the server.

# connect to a remote socket at specified host address
sock.connect(ADDR)

response = "WAITING"

"""Client loop. Either waiting for further instructions and not taking user input
OR taking user input and returning server response."""

while True:
    while "WAITING" in response:
        response = sock.recv(2048).decode()
        print(response)

    # take user input from Command line interface

    user_input = input("command: ")
    if user_input =='':
        continue

    # send user input to server and collect response
    sock.send(user_input.encode(FORMAT))
    response = sock.recv(2048).decode()
    print(response)
    

    # Error handling
    if response == "400 ERR":
        print("Invalid command")

    # if response is valid
    else: 
        print(response)
        if response == "DISC":
            sys.exit()

socket.close()