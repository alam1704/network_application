# import socket module
import socket

# import command line arguments
from sys import argv

class ttt_client:
    """ttt_client deals with networking and communication with ttt_server"""

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 65432
        self.ADDRESS = (self.HOST, self.PORT)
        self.FORMAT = 'UTF-8'
        self.SIZE = 1024

    def connect(self):
        """keeps repeating connection to server and returns true if connected successfully"""
        while True:
            try:
                print("Connecting to game server...")

                # connection will timeout 5 seconds
                self.client_socket.settimeout(5)

                # connect to the specified host and port
                self.client_socket.connect(self.ADDRESS)
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

    def client_send(self, msg):
        """sends message to server with agreed command token to ensure message delivered safely"""
        try:
            self.client_socket.send((msg).encode())
        except:
            self.connection_lost()

    def client_recv(self):
        """receives packet with specified size from server then checks integrity"""
        try:
            msg = self.client_socket.recv(self.SIZE).decode()
            # return msg if anything unexpected happens
            return msg
        
        except:
            # if error occurs, connection lost
            self.connection_lost()
    
    def connection_lost(self):
        """This method will be called when connection is lost."""
        print("Error: Connection Lost.")
        try:
            self.client_socket.send("q".encode())
        except:
            pass
        # Raise an error to finish
        raise Exception

    def close(self):
        "Shutdown socket and close"
        # Shuts down the socket to prevent further send/receive signals
        self.client_socket.shutdown(socket.SHUT_RDWR)
        # close socket
        self.client_socket.close()

    
class ttt_client_game(ttt_client):
    """ttt_client_game deals with the GAME LOGIC on the client side"""
    
    def __init__(self):
        """Initialise the client game object"""
        ttt_client.__init__(self)

    def start_game(self):
        """starts game and gets basic information from server"""

        # receive player info from server
        self.player_id = int(self.client_recv())
        # confirm ID received
        self.client_send()

        # tell user connection establised
        self.connected()

        # receive assigned role from server
        self.role = str(self.client_recv(2, "R"))
        #confirm assigned role
        self.client_send("c", "2")

        

    def connected(self):
        pass