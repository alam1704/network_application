import os
import time
from grid import Board

import threading

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()



import socket

HOST = '127.0.0.1'
PORT = 65432
connection_established = False
conn, addr = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

def receive_data():
    pass

def waiting_for_connection():
    global connection_established, conn, addr
    conn, addr = sock.accept()
    print("Client is connected.")
    connection_established = True
    receive_data()

create_thread(waiting_for_connection)

board=Board(player_pos, cur_player)

def clear():
    os.system("clear")

def refresh_board():
    #clear the screen
    clear()
    #Show the header
    board.print_header()
    #Show the board
    board.display_board()
    #Show the score at the footer
    #board.print_scoreboard(score_board)

def single_game(cur_player):
    
    # represents the board values in the game matrix
    values = board.values
    #stores the moves as a dictionary
    player_pos = {'X':[], 'O':[]}

# game loop for a single game of tic tac toe
    while True:
        refresh_board()
        # handle player input
        # TRY and EXCEPT block for move input
        try:
            print("Player ", cur_player, " turn. Please choose from 1 - 9. > ", end ="")
            move = int(input())
        except ValueError:
            print("wrong Input!! Try again")
            time.sleep(2)
            continue

        if move < 1 or move > 9:
            print("Wrong Input!! Try again.")
            time.sleep(2)
            continue

        if values[move] != ' ':
            print("Already filled. Try again")
            time.sleep(2)
            continue

        #update current grid status    
        values[move] = cur_player

        #update player positions by updating the list
        player_pos[cur_player].append(move)

        #check the result of the board
        if board.check_winner(player_pos, cur_player):
            #refresh_board()
            #print('Player', cur_player, ' has won the game!!\n')
            return cur_player

        if board.check_draw(player_pos):
            refresh_board()
            print("It's a tie!\n")
            return 'D'

        #switch current player
        if cur_player == 'X':
            cur_player = 'O'
        else:
            cur_player = 'X'        


if __name__ == "__main__":
    
    clear()

    # print("\nPlayer 1")
    # player1 = input("Enter the name: \n")

    # print("\nPlayer 2")
    # player2 = input("Enter the name: \n")

    #cur_player = player1

    player_option = {'X': '', 'O': ''}

    options = ['X','O']

    #score_board = {player1: 0, player2: 0}

    refresh_board()

    #Outer game loop for managing multiple matches

    while True:  
        
        #Player choice Menu
        print(f"""\nTurn to choose for {cur_player}
        Enter 1 for X
        Enter 2 for O
        Enter 3 to quit""")

        try:
            choice = int(input())
        except ValueError:
            print("Wrong Input!! Try again.\n")
            time.sleep(2)
            continue

        if choice == 1:
            player_option['X'] = cur_player
            if cur_player == player1:
                player_option['O'] = player2
            else:
                player_option['O'] = player1

        elif choice == 2:
            player_option['O'] = cur_player
            if cur_player == player1:
                player_option['X'] = player2
            else:
                player_option['X'] = player1

        elif choice == 3:
            clear()
            print("Final Scores")
            board.print_scoreboard(score_board)
            break

        else:
            print("Wrong choice!! Try again.\n")

        #execute match and store winning mark
        winner = single_game(options[choice-1])

        if winner != 'D':
            player_won = player_option[winner]
            #score_board[player_won] += 1
            refresh_board()
            print('Player', winner, ' has won the game!!\n')
        # if winner != 'D':
        #     score_board[player_option[winner]] += 1
            
        
        if cur_player == player1:
            cur_player = player2 
        else:
            cur_player = player1

        board.reset_board()


