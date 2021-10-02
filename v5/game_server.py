# import socket module
import socket
from sys import exit
from grid import Board


class Server:
    """ttt_server deals with networking and communcation with the ttt_client"""    
    # create a tcp/ip socket with the init method
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 65432
        self.ADDRESS = (self.HOST, self.PORT)
        self.FORMAT = 'UTF-8'
        self.conn, self.addr = None, None
        self.player1 = "Player1"
        self.bind()
        self.player_pos = {'X':[], 'O':[]}

    
    def bind(self):
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
                choice = input("[A]bort or [R]etry?") # [C]hange port,
                if (choice.lower() == 'a'):
                    exit()
                # elif (choice.lower() == 'c'):
                #     self.PORT = input("Please enter the port:")

    def server_recv(self):
        """receives packet with specified size from server then checks integrity"""
        
        while True:
            try:
                msg = self.conn.recv(1024).decode()
                # return msg if anything unexpected happens
                return msg
            except:
                # if error occurs, connection lost
                print("Error: Server cannot receive.")
                pass

    def server_send(self, msg):
        """sends message to server with agreed command token to ensure message delivered safely"""
        # try:
        self.conn.send((msg).encode(self.FORMAT))
        # except:
            # print("Error: Server cannot send.")
            # pass

    def close(self):
        self.server_socket.close()


    def waiting_for_connection(self):
        self.conn, self.addr = self.server_socket.accept()
        print(f"Client {self.addr} is connected")
        # self.server_recv()
board=Board()
server= Server()

while True:
    try:
        server.waiting_for_connection()
    except KeyboardInterrupt:
        print("\nProgram Exited.")
        server.close()
        exit()
    server.server_send("welcome to server")
    break

for i in range(5):
    while True:

        # handle player input
        # send string version of input through sockets 
        # save move as integer on local machine
        # receive string input and convert to int before saving onto local machine
        try:
            print(server.player1, "'s turn. Please choose from 1-9 > ", end="")
            move = input()
            move_int = int(move)
        except ValueError:
            print("Wrong input!! Try again.")
            continue
        except KeyboardInterrupt:
            print("\nGame Over")
            server.close()
            exit()

        if move_int < 1 or move_int > 9:
            print("Wrong Input!! Try again.")
            continue

        if board.values[move_int] != ' ':
            print("Already filled. Try again")
            continue
        
        # append server move to player_pos on server side
        server.player_pos['X'].append(move_int)
        # update board values on server side
        board.values[move_int] = 'X'
        
        # print(server.player_pos) # display server move to server side
        # print(board.values) # check our current board status
        board.display_board()

        # send move over sockets
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
    while True:
        try:
            print("[WAITING] Other player is choosing position...")
            move = server.server_recv()
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
        board.display_board()

        if board.check_winner(server.player_pos, 'O'):
            print("Player 2 has won the game!")
            server.close()
            exit()

        break
server.close()