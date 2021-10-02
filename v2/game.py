class Game:

    def __init__(self, player1, player2):
        """Initialise a game between two players"""
        self.player1 = player1
        self.player2 = player2
        self.turn = player1
        self.waiting = player2
        self.board = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.winning_combo = [(1,2,3), (4,5,6), (7,8,9), (1,4,7), (2,5,8), (3,6,9), (1,5,9), (3,5,7)]

    def display_board(self):
        return f"""
        \t     |     |     \t|\t     |     |     
        \t  {self.board[1]}  |  {self.board[2]}  |  {self.board[3]}  \t|\t  1  |  2  |  3  
        \t_____|_____|_____\t|\t_____|_____|_____
        \t     |     |     \t|\t     |     |     
        \t  {self.board[4]}  |  {self.board[5]}  |  {self.board[6]}  \t|\t  4  |  5  |  6  
        \t_____|_____|_____\t|\t_____|_____|_____
        \t     |     |     \t|\t     |     |     
        \t  {self.board[7]}  |  {self.board[8]}  |  {self.board[9]}  \t|\t  7  |  8  |  9  
        \t     |     |     \t|\t     |     |     
        """

    def change_turn(self):
        """Change player turns in main game loop"""
        if self.turn == self.player2:
            self.turn = self.player1
            self.waiting = self.player2
        else:
            self.turn = self.player2
            self.waiting = self.player1

    def player_move(self, move):
        """Add move to board and checks if game is finished
        Also takes an argument from 1 - 9."""
        move = int(move)
        if self.turn == self.player1:
            self.board[move]='X'
        else:
            self.board[move]='O'

        # Assume game is done with no winner
        finished = True
        winner = False

        # check if there are still moves to be made
        for grid in self.board[1:10]:
            if grid != 'X' or grid !='O':
                finished = False

        # check for winning combination
        for (a,b,c) in self.winning_combo:
            if self.board[a]==self.board[b]==self.board[c]:
                winner = True

        # return winner if there is a winner
        if winner:
            return "WINNER"

        # return finished if there is a draw
        elif finished:
            return "TIE"

        # NPT - Next Player Turn
        else:
            return "NPT"
        

# game = Game("player1", "player2")
# print(game.display_board())