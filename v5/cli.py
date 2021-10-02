# import socket module
import socket


# create client class
class Client():

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 65432
        self.ADDR = (self.HOST, self.PORT)
        self.FORMAT = 'UTF-8'
        self.player2 = "player2"
        self.connect()
        self.player_pos = {'X':[], 'O':[]}


    def connect(self):
        """keeps connection to server and returns true if connected successfully"""
        while True:
            try:
                print("Connecting to game server...")

                # connection will timeout 5 seconds
                # self.client_socket.settimeout(5)

                # connect to the specified host and port
                self.client_socket.connect(self.ADDR)
                return True
            except:
                print(f"There is an error when trying to connect to {self.HOST}::{self.PORT}")
                self.connect_failed()

    def connect_failed(self):
        choice = input("[A]bort, [C]hange address and port, or [R]etry?")
        if (choice.lower() == "a"):
            exit()
        elif(choice.lower() == "c"):
            self.HOST = input("Please enter the address:")
            self.PORT = input("Please enter the port:")

    def client_recv(self):
        """receives packet with specified size from server then checks integrity"""
        while True:
            try:
                msg = self.client_socket.recv(1024).decode()
                # return msg if anything unexpected happens
                # print(msg)
                return msg
            except Exception as e:
                # if error occurs, connection lost
                print(e)
                print("Error: Client can not receive.")
                pass

    def client_send(self, msg):
        """sends message to server with agreed command token to ensure message delivered safely"""
        try:
            self.client_socket.send(msg.encode(self.FORMAT))
            # print(msg)
        except:
            print("Error: Client can not send.")
            pass

    def close(self):
        "Shutdown socket and close"
        # Shuts down the socket to prevent further send/receive signals
        self.client_socket.shutdown(socket.SHUT_RDWR)
        # close socket
        self.client_socket.close()

client=Client()
while True:
    print(client.client_recv())
    break

for i in range(4):
    while True:
        # print("Hello world")
        move = client.client_recv()
        break
    print(f"{move} is.")
    client.player_pos['X'].append(move)
    print(client.player_pos)

    while True:
        move = input("Enter your move: ")
        client.player_pos['O'].append(move)
        print(client.player_pos)
        client.client_send(move)
        break
client.close()