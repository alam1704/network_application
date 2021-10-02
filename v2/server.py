import socket
import sys

from _thread import *
from threading import RLock ### may not need this ###

from player import Player
from game import Game

import time

# define host and port
HOST = '127.0.0.1'
PORT = 65432
ADDR = (HOST, PORT)
FORMAT = 'UTF-8'

# create server socket object
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("[FAILED]: Could not create socket")

#Bind to port 65432
try:
    sock.bind(ADDR)
except socket.error:
    print('[FAILED]: Could not bind socket')
    sys.exit()

sock.listen(5)
print("[LISTENING]")

# keeps track of players currently in server
players = []

lock = RLock() ### may not need this ###

def connect(client_sock):
    """Run for each client that connects to the server
    handles messages sent from the client and sends corresponding responses"""

    # Opening message to client
    client_sock.send(b"""Welcome to Network TicTacToe!
    Please start by typing the 'help' command to see your options""")
    

    # Main connection loop - handles all messges FROM client
    while True:
        # Command sent by client
        command = client_sock.recv(2048).decode()

        # Log in with a username
        request = command.split(" ")
        print(request)


        if request[0] == 'login' and request[1]:
            username = request[1]
            found = False
            #check if username already exist
            for player in players:
                if player.username == username:
                    current_player = player
                    found = True
                    print (f"{current_player.username} logged in.")
            
            # Add a new player if no user with specified username exists
            if not found:
                lock.acquire()
                current_player = Player(username, client_sock)
                players.append(current_player)
                print(f"{current_player.username} created an account and logged in")
                lock.release()

            client_sock.send(f"Welcome {current_player.username}".encode())

        elif request[0] == "play":
            # Player will need to wait to find an opponent
            opponent = None
            while opponent is None:
                for opp in players:
                    if opp.username != current_player.username:
                        opponent = opp

                # Using a sleep function until opponent is found
                if opponent is None:
                    time.sleep(1)
                # Once opponent is found, create a game with the opponent and current player
                else:
                    game = Game(opponent, current_player)
                    start_game(game)

        elif request[0] == "help":
            client_sock.send(b"""Commands:
            login <username> - Enter 'login' followed by username of choice
            play - Starts a game once an opponent is found. Must be logged in to play
            move <position> - Select position according to board matrix. Position can be between 1-9. 
                              Must be logged in and in game to use command.  
            exit - Leave the server
            """)
        
        elif request[0] == "exit":
            print("Client disconnected")
            client_sock.send(b"DISC")
            client_sock.close()
            break

        else:
            client_sock.send(b"400 ERR")

def start_game(game):
    """ contains main game loop
    Takes Game Object as an argument"""
    #score_board = {{game.turn.username}:0, {game.waiting.username}:0 }
    gameover = False
    
    while not gameover:
        
        game.turn.send(("Your turn").encode(FORMAT))  
        game.waiting.send((f"[WAIT], {game.turn.username}'s turn").encode(FORMAT))
        move = (game.turn.conn.recv(2048)).decode()
        print(move)

        if check_move(game, move):
            response = game.player_move(move.split(" ")[1])
            print(response)

            #if move is valid and game is not over
            if response == "NPT":
                game.turn.send(("[WAIT]" + game.display_board()).encode(FORMAT))
                game.waiting.send(("[WAIT]" + game.display_board()).encode(FORMAT))
                game.change_turn()

            # if game is finished and no winner
            elif response == "TIE":
                gameover = True
                game.turn.send("No Winner")
                game.waiting.send("No Winner")

            elif response == "WINNER":
                gameover = True
                game.turn.send("Game over, you won!")
                game.waiting.send(f"Game over, {game.turn.username} won!")
                #score_board[game.turn.username] += 1

        else:
            continue

    return


def check_move(game,move):
    
    """takes a player move as argument and ensures move is valid"""
    try:
        statement, position = move.split(" ")
        position = int(position)
    except ValueError:
        return False
    
    # check that user correctly uses 'move' 
    if statement != "move":
        return False
    
    # check that the position is valid
    elif position < 1 or position > 9 or game.board[position] == 'X' or game.board[position] == 'O':
        return False

    else:
        return True

while True:
    client_sock, addr = sock.accept()
    print ("Connected to Client")

    start_new_thread(connect, (client_sock, ))

socket.close()