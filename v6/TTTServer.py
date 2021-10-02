import socket, threading, random

clients = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
ADDR = (HOST, PORT)
SIZE = 2048
FORMAT = 'UTF-8'


server_socket.bind(ADDR)
print(f"""Starting server...
IP Address: {HOST}
Port: {PORT}
""")

class Client:
    
    def __init__(self, _client, addr):
        print(f"Initialising client object for {addr}")
        self.opponent = None
        self.turn = False
        self.counter = ""
        self._client = _client
        self.addr = addr
        self.active = True

    def get_data(self):
        try:
            data = self._client.recv(SIZE)
            return data
        except Exception as e:
            print(e)
            self.exit()

    def get_counter(self):
        return self.counter

    def set_counter(self, counter):
        self.counter = counter

    def get_addr(self):
        return self.addr

    def get_opponent(self):
        return self.opponent
        
    def set_opponent(self, addr):
        self.opponent = addr

    def exit(self):
        print(f"Client {self.get_addr()} has disconnected")

    def is_active(self):
        if self.active:
            return True
        else: 
            return False

def listen(server_socket):
    global clients
    while True:
        server_socket.listen(1)
        _client, addr = server_socket.accept()
        print(f"Connection received. Addr: {addr}")
        client_opp = Client(_client, addr)
        clients.append(client_opp)

def client():
    global clients
    while True:
        for client in clients:
            if client.is_active():
                if client.get_opponent() == None:
                    for match in clients:
                        if match.get_opponent() == None:
                            print("Matching", match.addr, "with", client.get_addr())
                            match.set_opponent(client.get_addr())
                            client.set_opponent(match.get_addr())
                            client._client.send("ready".encode()) # tell that clients to prepare for the game
                            match._client.send("ready".encode())
                            tg = threading.Thread(target=game, args=(client, match))
                            tg.start() # start the game thread

def game(player1, player2):

    def print_board(): # display this instance's board
        print("\n")
        print("\t     |     |     \t|\t     |     |     ")
        print(f"\t  {board[1]}  |  {board[2]}  |  {board[3]}  \t|\t  1  |  2  |  3  ")
        print(("\t_____|_____|_____\t|\t_____|_____|_____"))

        print("\t     |     |     \t|\t     |     |     ")
        print(f"\t  {board[4]}  |  {board[5]}  |  {board[6]}  \t|\t  4  |  5  |  6  ")
        print(("\t_____|_____|_____\t|\t_____|_____|_____"))

        print("\t     |     |     \t|\t     |     |     ")
        print(f"\t  {board[7]}  |  {board[8]}  |  {board[9]}  \t|\t  7  |  8  |  9  ")
        print("\t     |     |     \t|\t     |     |     ")
        print("\n")

    def check_win(): # check this instance's board for a win
        empty = " "
        b = board
        winner = ""
        if b[1] == b[2] and b[1] == b[3] and b[1] != empty:
            winner = b[1]
        elif b[1] == b[4] and b[1] == b[7] and b[1] != empty:
            winner = b[1]
        elif b[1] == b[5] and b[1] == b[9] and b[1] != empty:
            winner = b[1]
        elif b[2] == b[5] and b[2] == b[8] and b[2] != empty:
            winner = b[2]
        elif b[3] == b[6] and b[3] == b[9] and b[3] != empty:
            winner = b[3]
        elif b[4] == b[5] and b[4] == b[6] and b[4] != empty:
            winner = b[4]
        elif b[7] == b[5] and b[7] == b[3] and b[7] != empty:
            winner = b[7]
        elif b[7] == b[8] and b[7] == b[9] and b[7] != empty:
            winner = b[7]
        else:
            winner = empty
        return winner.strip()

    def game_over():
        player1._client.send(f"over||{winner}||{[x for x in board]}".encode(FORMAT))
        player2._client.send(f"over||{winner}||{[x for x in board]}".encode(FORMAT))

    def next_turn(this_turn):
        if this_turn == player1:
            this_turn = player2
        else:
            this_turn = player1
        return this_turn


    board = [' ' for x in range(10)]
    winner = None
    this_turn = random.choice((player1, player2)) # randomly select a player to go first

    this_turn.set_counter("X") # first turn always gets X
    if this_turn == player1:
        player2.set_counter("O")
    else:
        player1.set_counter("O")

    while not winner:
        this_turn._client.send("go||{}||{}".format(this_turn.get_counter(), ",".join(x for x in board)).encode(FORMAT))
        print("It is ", this_turn.get_addr(), "'s turn", sep="")
        ref = None
        while ref == None:
            data = this_turn.get_data()
            if not data:
                this_turn.exit()
            response = data.decode()
            if int(response) in range(10):
                ref = int(response)
                print("Got position:", ref + 1)
                if board[ref] == " ":
                    board[ref] = this_turn.get_counter()
                    print_board()
                    winner = check_win()
                    this_turn = next_turn(this_turn)
                else:
                    print("Invalid position.")
                    this_turn._client.send("invalid_pos||{}||{}".format(this_turn.get_counter(),
                                                                  ",".join(x for x in
                                                                           board)).encode())
            else:
                this_turn._client.send(
                    "invalid_pos||{}||{}".format(this_turn.get_counter(), ",".join(x for x in board)).encode())
    print(winner, "wins!")
    game_over()


try:
    thread_listen = threading.Thread(target = listen, args=(server_socket,))
    thread_listen.start()
    thread_client = threading.Thread(target = client)
    thread_client.start()
    print("""Server initialisation process complete.
    Now listening for connections...
    """)
except Exception as e:
    print(e)
    server_socket.close()





