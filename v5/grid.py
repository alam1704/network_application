import os
import sys

class Board:
    """A class to represent the game board.

    The Board acts as  the main game class . It also contains the check_win and check_draw method to check the status of the game.

    Attributes
    ----------

    values: returns a list of empty elements that represent the empty spaces on the grid. 10 elements are used as the first element is used as a dead space.

    Methods
    -------

    display_board
        Prints the current status of the game board with a matrix beside it to help players know where to place their next position
    
    check_winner(player_pos, cur_player)
        checks what positions the 'X' and 'O' have returns True if a winning combination is found

    check_draw(player_pos)
        checks the combined length of the list the values that are stored in 'X' and 'O'

    """
    def __init__(self):
        """Initialising the board

        Attributes
        ----------

        values : list
            10 empty strings used to store 'X' or 'O' as moves
        """
        self.values = [' ' for x in range(10)]

    # Create a board as a well a default matrix to show players where the positions are
    def display_board(self):
        """Prints the current status of the game board with a matrix beside it to help players know where to place their next position
        """
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
        """checks what positions the 'X' and 'O' have returns True if a winning combination is found.
        
        It loops through all possible winning combination to check if combination satisfied

        Returns True if all elements of iteration returns True    

        Returns False if no winning combination satisfies.

        Parameters
        ----------

        player_pos : key in dict
            The position the players make are stored in a list in this dictionary containing 'X' or 'O'

        cur_player : value in dict
            Accesses the key:value pairing of the player_pos

        """
        for winning_combo in [[1,2,3], [4,5,6], [7,8,9], [1,4,7], [2,5,8], [3,6,9], [1,5,9], [3,5,7]]:  
            if all(combo in player_pos[cur_player] for combo in winning_combo):
                return True
        return False

    def check_draw(self, player_pos):
        """Checks the combined length of the list the values that are stored in 'X' and 'O'

        Parameters
        ----------
        player_pos : key in dict
            checks both the lengths of the 'X' and 'O'. If they add up to 9, 
            it means that the grid is full and no more moves can be accepted.
            The game is a draw, hence no winner
        """
        if len(player_pos['X']) + len(player_pos['O']) == 9:
            return True
        return False

    # def reset_board(self):
    #     self.values = [' ' for x in range(10)]

    def print_header(self):
        print("+-------------------------------+-------------------------------+")
        print("|  Welcome to Tic-Tac-Toe 1.0   |        Coordinate Matrix      |")
        print("+-------------------------------+-------------------------------+")

    # def print_scoreboard(self, score_board):
    #     players = list(score_board.keys())
    #     print("+-------------------------------+-------------------------------+")
    #     print(f"   Score: {players[0]} {score_board[players[0]]}, {players[1]} {score_board[players[1]]}")
    #     print("+-------------------------------+-------------------------------+")
    
    def clear(self):
        os.system("clear")

    def refresh_board(self):
        self.clear()
        self.print_header()
        self.display_board()