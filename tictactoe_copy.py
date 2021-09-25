import os

def clear():
    os.system("clear")

class Board():
    
    def __init__(self):
        self.values = [' ' for x in range(10)]
        self.player_pos = ['X',"O"]
        self.player_scores = [0,0]

    # Create a board as a well a default matrix to show players where the positions are
    def display_board(self):
        print("\n")
        print("\t     |     |     \t|\t     |     |     ")
        print(f"\t  {self.values[1]}  |  {self.values[2]}  |  {self.values[3]}  \t|\t  1  |  2  |  3  ")
        print(("\t_____|_____|_____\t|\t_____|_____|_____"))

        print("\t     |     |     \t|\t     |     |     ")
        print(f"\t  {self.values[4]}  |  {self.values[5]}  |  {self.values[6]}  \t|\t  4  |  5  |  6  ")
        print(("\t_____|_____|_____\t|\t_____|_____|_____"))

        print("\t     |     |     \t|\t     |     |     ")
        print(f"\t  {self.values[7]}  |  {self.values[8]}  |  {self.values[9]}  \t|\t  7  |  8  |  9  ")
        print("\t     |     |     \t|\t     |     |     ")
        print("\n")

    # If player selects already filled position, it'll skip to the next player's turn
# PLEASE FIX THIS BUG.    
    def update_grid(self, grid_num, player):
        if self.values[grid_num] == " ":
            self.values[grid_num] = player

    # checks for winning combination
    def winner(self, player):
        for winning_combo in [[1,2,3], [4,5,6], [7,8,9], [1,4,7], [2,5,8], [3,6,9], [1,5,9], [3,5,7]]:
            result = True
            for grid_no in winning_combo:
                if self.values[grid_no] != player:
                    result = False
            if result == True:
                print(f"{player} wins!")
                return True
            
    def tie(self):
        used_space = 0
        for space in self.values:
            if space != " ":
                used_space += 1
        if used_space == 9:
            return True
        else:
            return False
    

    # resets the board if a winner is determined
    def reset(self):
        self.values = [' ' for x in range(10)]

    def exit_game(self):
        quit()



board = Board()

def print_header():
    print("+-------------------------------+-------------------------------+")
    print("|  Welcome to Tic-Tac-Toe 1.0   |        Coordinate Matrix      |")
    print("+-------------------------------+-------------------------------+")

    

def print_footer():
    print("+-------------------------------+-------------------------------+")
    print(f"   Score: {board.player_pos[0]} {board.player_scores[0]}, {board.player_pos[1]} {board.player_scores[1]}.")
    print("+-------------------------------+-------------------------------+")

def refresh_board():
    #clear the screen
    clear()
    #Show the header
    print_header()
    #Show the board
    board.display_board()
    #Show the score at the footer
    print_footer()


while True:
    refresh_board()

    #Get input from player "X"
    x_option = int(input(f"\n Player {board.player_pos[0]}, please choose 1 - 9. > "))

    # Update the board
    board.update_grid(x_option, "X")

    # Update the board
    refresh_board()

    # check for x winner 
    if board.winner("X"):
        play_choice = input("Would you like to play again? (Y/N) > ").upper()
        if play_choice == "Y":
            board.reset()
            continue
        else:
            board.exit_game()

    # check for tie game after X inputs
    if board.tie():
        print("\nTie game!\n")
        play_choice = input("Would you like to play again? (Y/N) > ").upper()
        if play_choice == "Y":
            board.reset()
            continue
        else:
            board.exit_game()
    
    #Get input from player "O"
    o_option = int(input(f"\n Player {board.player_pos[1]}, please choose 1 - 9. > "))

    # Update the board
    board.update_grid(o_option, "O")

    # check for x winner 
    if board.winner("O"):
        play_choice = input("Would you like to play again? (Y/N) > ").upper()
        if play_choice == "Y":
            board.reset()
            continue
        else:
            board.exit_game()

    # check for tie game after O inputs
    if board.tie():
        print("\nTie game!\n")
        play_choice = input("Would you like to play again? (Y/N) > ").upper()
        if play_choice == "Y":
            board.reset()
            continue
        else:
            board.exit_game()

