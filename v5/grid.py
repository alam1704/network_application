import os

class Board:
    
    def __init__(self):
        self.values = [' ' for x in range(10)]

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

    def check_winner(self, player_pos, cur_player):

        #loop through all possible winning combination to check if combination satisfied
        for winning_combo in [[1,2,3], [4,5,6], [7,8,9], [1,4,7], [2,5,8], [3,6,9], [1,5,9], [3,5,7]]:

            #returns True is all elements of iteration returns True        
            if all(combo in player_pos[cur_player] for combo in winning_combo):
                return True
        
        #return False if no winning combination satisfies.
        return False

    def check_draw(self, player_pos):
        if len(player_pos['X']) + len(player_pos['O']) == 9:
            return True
        return False

    def reset_board(self):
        self.values = [' ' for x in range(10)]

    def print_header(self):
        print("+-------------------------------+-------------------------------+")
        print("|  Welcome to Tic-Tac-Toe 1.0   |        Coordinate Matrix      |")
        print("+-------------------------------+-------------------------------+")

    def print_scoreboard(self, score_board):
        players = list(score_board.keys())
        print("+-------------------------------+-------------------------------+")
        print(f"   Score: {players[0]} {score_board[players[0]]}, {players[1]} {score_board[players[1]]}")
        print("+-------------------------------+-------------------------------+")
    
    def clear(self):
        os.system("clear")

    def exit(self):
        os.system('exit')

