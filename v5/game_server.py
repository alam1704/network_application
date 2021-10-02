# import python libraries including socket and sys module.
# import grid from board
import socket
from sys import exit
from grid import Board
import time

# create a server class
class Server:
    """A class to represent the Server
    
    The server deals with networking and communcation with the client
    
    Class attributes
    ----------

    server_socket: creates a socket object to support the context manager type. The arguments pass through specify the address family (IPv4) and socket type (TCP).
    HOST: identifies the host name of the current system under which the Python code is executed.
    PORT: An integer; identitfies a port to listen on (non-privileged ports are > 1023)
    ADDRESS: A tuple of the HOST and PORT
    FORMAT: what format the .encode() method should be using
    Player: Server is set to player 1 as default
    bind(): method used to associate the socket with a specific network interface and port number. The method has the class attributes self.ADDRESS passed as a tuple
    If any error occurs, the method is handled with an except block.
    player_pos: carries/holds the position of the player inputs as a dictionary with lists.
    """    
    # create a tcp/ip socket with the init method
    def __init__(self):
        """Constructor for initialising a TCP/IP socket. Setting player1 as client
        Upon creating an instance object, we call the bind method."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # class attributes
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 65432
        self.ADDRESS = (self.HOST, self.PORT)
        self.FORMAT = 'UTF-8'
        self.player1 = "Player1"
        self.bind()
        self.player_pos = {'X':[], 'O':[]}

    
    def bind(self):
        """Binds server with designated port and starts listening to binded address

        Raises
        ------
        Exception
            Cannot bind at specified HOST and PORT.
        

        """
        while True:
            try:
                # bind to an address with designated port
                self.server_socket.bind(self.ADDRESS)
                self.server_socket.listen(1)
                print(f"Listening to port {self.PORT}.")
                break
            except Exception as e:
                print(f"There was an error when trying to bind to {self.PORT}. Reason: {e}")
                choice = input("[A]bort or [R]etry?") # [C]hange port,
                if (choice.lower() == 'a'):
                    exit()
                # elif (choice.lower() == 'c'):
                #     self.PORT = input("Please enter the port:")

    def server_recv(self):
        """Receives packet with specified size from server then checks integrity
        
        Raises
        ------
        Exception
            Cannot bind at specified HOST and PORT.

        Returns
        -------
        msg
            A message as a string.
        """
        
        while True:
            try:
                msg = self.conn.recv(1024).decode()
                # return msg if anything unexpected happens
                return msg
            except Exception as e:
                # if error occurs, connection lost
                print("Error: Server cannot receive. Reason:", e)
                pass

    def server_send(self, msg):
        """Sends message to server with agreed command token to ensure message delivered safely
        
        Raises
        ------

        Exception
            When the server is unable to send msg.
        """
        try:
            self.conn.send((msg).encode(self.FORMAT))
        except Exception as e:
            print("Error: Server cannot send. Reason:", e)
            pass

    def close(self):
        """When the method is called upon, the socket is closed
        """
        self.server_socket.close()


    def waiting_for_connection(self):
        """Accept connections once connection is establised.
        """
        self.conn, self.addr = self.server_socket.accept()
        print(f"Client {self.addr} is connected")
        # self.server_recv()

board=Board() # create an instance object for Board
server= Server() # create an instance object for Server

# loop through until connection establised
while True:
    # created a try and except block to catch KeyBoardInterrupt.
    try:
        server.waiting_for_connection()
    except KeyboardInterrupt:
        print("\nProgram Exited.")
        server.close()
        exit()
    server.server_send("welcome to server")
    break

# Server move will always be 1 more than the client 
for i in range(5):
    while True:
        # handle player input
        try:
            board.refresh_board()
            print(server.player1, "'s turn. Please choose from 1-9 > ", end="")
            move = input()
            move_int = int(move) # save move as integer on local machine
        except ValueError:
            print("Wrong input!! Try again.")
            time.sleep(2)
            continue
        except KeyboardInterrupt:
            print("\nGame Over")
            time.sleep(2)
            server.close()
            exit()

        # create handling error for invalid inputs
        if move_int < 1 or move_int > 9:
            print("Wrong Input!! Try again.")
            time.sleep(2)
            continue

        if board.values[move_int] != ' ':
            print("Already filled. Try again")
            time.sleep(2)
            continue
        
        # append server move to player_pos on server side
        server.player_pos['X'].append(move_int)
        # update board values on server side
        board.values[move_int] = 'X'
        
        # print(server.player_pos) # display server move to server side
        # print(board.values) # check our current board status
        board.refresh_board()

        # send string version of input through sockets
        server.server_send(move)

        # check to see if there is a winner
        if board.check_winner(server.player_pos, "X"):
            print("You have won the game!!")
            server.close()
            exit()

        # Since there are only 9 moves, server will always have last move.
        if board.check_draw(server.player_pos):
            print("Its a tie!\n")

        break

    # 
    while True:
        try:
            print("[WAITING] Other player is choosing position...")
            move = server.server_recv() # receive string input and convert to int before saving onto local machine
            move_int = int(move)
        except ValueError:
            print("Player2 disconnected")
            server.close()
            exit()
        except KeyboardInterrupt:
            print("Game Over")
            server.close()
            exit()

        # append client move to player_pos on server side
        server.player_pos['O'].append(move_int)
        # update board values on server side from client move
        board.values[move_int] = 'O'

        # print(server.player_pos) # display client move to server side
        # print(board.values) # check our current board status
        board.refresh_board()

        if board.check_winner(server.player_pos, 'O'):
            print("Player 2 has won the game!")
            server.close()
            exit()

        break
server.close()