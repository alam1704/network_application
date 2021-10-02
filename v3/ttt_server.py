# import socket module
import socket

#import threading
import threading

# import time module
import time

# import command line arguments
from sys import argv


class ttt_server:
    """ttt_server deals with networking and communcation with the ttt_client"""    
    # create a tcp/ip socket with the init method
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 65432
        self.ADDRESS = (self.HOST, self.PORT)
        self.FORMAT = 'UTF-8'

    
    def bind(self, port_number):
        """binds server with designated port and starts listening to binded address"""
        while True:
            try:
                # bind to an address with designated port
                self.server_socket.bind(self.ADDRESS)
                self.server_socket.listen(1)
                print(f"Listening to port {self.PORT}.")
                break
            except:
                print(f"There was an error when trying to bind to {self.PORT}.")
                choice = input("[A]bort, [C]hange port, or [R]etry?")
                if (choice.lower() == 'a'):
                    exit()
                elif (choice.lower() == 'c'):
                    self.PORT = input("Please enter the port:")

    def close(self):
        self.server_socket.close()

class ttt_server_game(ttt_server):
    """ttt_server_game deals with GAME LOGIC for server side"""

    def __init__(self):
        """initialises the server game object"""
        ttt_server.__init__(self)

    def start(self):
        """Starts server and accepts clients"""

        # create a list object to store connected players
        self.waiting_players = []

        # use lock top synchronise access when matching players
        self.lock_matching = threading.Lock()
        
        #starts main loop
        self.main_loop()

    def main_loop(self):
        """the main server loop"""
        #loop to recursively accept new clients
        while True:
            # accept connection from client
            connection, client_addr = self.server_socket.accept()
            print(f"Received connection from:{client_addr}")

            # initialise new player object to store all client information
            new_player = Player(connection)
            # add new player object to list
            self.waiting_players.append(new_player)

            try:
                # start new thread to deal with new client
                threading.Thread(target = self.client_thread, args=(new_player,)).start()
            except:
                print("Failed to create thread.")

    def client_thread(self, player):
        # client thread
        # wrapping entire client thread with try and except so server does not break if client breaks
        pass
            

class Player:
    """player class describes client with connection to server and in game"""
    count = 0
    pass