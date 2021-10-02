# import python libraries including socket and sys module.
# import grid from board
import socket
from grid import Board
from sys import exit

# create client class
class Client():
    """A class to repesent the Client
    
    Client deals with networking and communcation with the server
    
    Class attributes
    ----------------

    server_socket: creates a socket object to support the context manager type. The arguments pass through specify the address family (IPv4) and socket type (TCP).
    HOST: identifies the host name of the current system under which the Python code is executed.
    PORT: An integer; identitfies a port to listen on (non-privileged ports are > 1023)
    ADDRESS: A tuple of the HOST and PORT
    FORMAT: what format the .encode() method should be using
    Player: Server is set to player 2 as default
    connect(): method used to connect the open socket from the server. The method has the class attributes self.ADDRESS passed as a tuple
    If any error occurs, the method is handled with an except block.
    player_pos: carries/holds the position of the player inputs as a dictionary with lists.
    """
    def __init__(self):
        """Constructor for initialising a TCP/IP socket. Setting player2 as client
        Upon creating an instance object, we call the bind method."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 65432
        self.ADDR = (self.HOST, self.PORT)
        self.FORMAT = 'UTF-8'
        self.player2 = "Player2"
        self.connect()
        self.player_pos = {'X':[], 'O':[]}


    def connect(self):
        """Keeps connection to server and returns true if connected successfully
        

        """
        while True:
            try:
                print("Connecting to game server...")

                # connection will timeout 5 seconds
                # self.client_socket.settimeout(5)

                # connect to the specified host and port
                self.client_socket.connect(self.ADDR)
                return True
            except Exception as e:
                print(f"There is an error when trying to connect to {self.HOST}::{self.PORT}. Reason: {e}")
                self.connect_failed()

    def connect_failed(self):
        """call this method if connection fails"""
        choice = input("[A]bort or [R]etry?") # [C]hange address and port, 
        if (choice.lower() == "a"):
            exit()
        # elif(choice.lower() == "c"):
        #     self.HOST = input("Please enter the address:")
        #     self.PORT = input("Please enter the port:")

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
        # self.client_socket.shutdown(socket.SHUT_RDWR)
        # close socket
        self.client_socket.close()

board = Board()
client=Client()

while True:
    print(client.client_recv())
    break

for i in range(4):
    # handle player input from server
    # receive string version of input through sockets 
    # save move as integer on local machine
    # send string input and convert to int before saving onto local machine
    while True:
        try:
            board.refresh_board()
            print("[WAITING] Other player is choosing position...")
            move = client.client_recv()
            move_int = int(move)
            break
        except ValueError:
            print("Player1 disconnected")
            exit()
        except KeyboardInterrupt:
            print("\nGame Over.")
            client.close()
            exit()
    # print(f"{move_int} is.")

    # append server move on client side 
    client.player_pos['X'].append(move_int)
    # update board values on client side from server move
    board.values[move_int] = 'X'

    # print(client.player_pos) # display server move to client side
    # print(board.values) # check our current board status
    board.refresh_board()
    
    # check to see if there is a winner
    if board.check_winner(client.player_pos, 'X'):
        print("Player1 has won the game!!")
        client.close()
        exit()

    while True:
        try:
            print(client.player2, "'s turn. Please choose from 1-9 > ", end="")     
            move = input()
            move_int = int(move)
        except ValueError:
            print("Wrong input!! Try again.")
            continue
        except KeyboardInterrupt:
            print("\nGame Over")
            client.close()
            exit()   

        if move_int < 1 or move_int > 9:
            print("Wrong Input!! Try again.")
            continue

        if board.values[move_int] != ' ':
            print("Already filled. Try again")
            continue
        
        # append client move to player_pos on client side
        client.player_pos['O'].append(move_int)
        #update board values on client side
        board.values[move_int] = 'O'

        # print(client.player_pos) # display client move to client
        # print(board.values) # check our current board status
        board.refresh_board()

        #send move over socket
        client.client_send(move)

        # check to see if there is a winner
        if board.check_winner(client.player_pos, 'O'):
            print("You have won the game!!")
            client.close()
            exit()
        break
client.close()