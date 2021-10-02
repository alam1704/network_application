import os, random, sys, socket, time

FORMAT = "UTF-8"

try:
    import winsound
    platform = "windows"
except:
    platform = "gnulinux"

def print_board():
    for n in range(0, 9, 3):
        print(board[n] + "|" + board[n+1] + "|" + board[n+2] + "  ", n+1, "|", n+2, "|", n+3, sep="")

def place(counter, i):
    if board[i] == empty:
        board[i] = counter
        return err_success
    else:
        return err_failure

def clear():
    if idle:
        print("\n"*80)
    else:
        if platform == "gnulinux":
            os.system("clear")
        else:
            os.system("cls")

def ai_place(c):
    available_spots = []
    for i in range(9):
        if board[i] == empty:
            available_spots.append(i)
    if available_spots:
        i = random.choice(available_spots)
        board[i] = c
        return err_success
    else:
        return err_failure

def check_win():
    b = board
    if b[0] == b[1] and b[0] == b[2] and b[0] != empty:
        return b[0]
    elif b[0] == b[3] and b[0] == b[6] and b[0] != empty:
        return b[0]
    elif b[0] == b[4] and b[0] == b[8] and b[0] != empty:
        return b[0]
    elif b[1] == b[4] and b[1] == b[7] and b[1] != empty:
        return b[1]
    elif b[2] == b[5] and b[2] == b[8] and b[2] != empty:
        return b[2]
    elif b[3] == b[4] and b[3] == b[5] and b[3] != empty:
        return b[3]
    elif b[6] == b[4] and b[6] == b[2] and b[6] != empty:
        return b[6]
    elif b[6] == b[7] and b[6] == b[8] and b[6] != empty:
        return b[6]
    else:
        return empty

def display_menu():
    for i, o in enumerate(options):
        print(i+1, ") ", o, sep = "")
    print()

def menu():
    display_menu()
    choice = ""
    while True:
        try:
            print("Choice: ", end="")
            choice = int(input())
            break
        except:
            clear()
            display_menu()
            continue
    if choice == 1: # find a match
        connect()
    elif choice == 2: # play offline
        offline()
    elif choice == 3: # quit
        quit()

def offline():
    moves = 0
    ai_moves = 0
    player_counter = "O"
    ai_counter = "X"
    winner = empty
    while True:
        clear()
        print_board()
        try:
            pos = int(input("Choose a position on the board: "))
        except:
            continue
        if pos not in range(1, 10):
            continue
        if place(player_counter, pos-1) == err_failure:
            continue
        moves += 1
        if check_win() == player_counter:
            winner = player_counter
            break
        if ai_place(ai_counter) == err_failure:
            break
        ai_moves += 1
        winner = check_win()
        if winner != empty:
            break
        
    clear()
    print_board()
    if winner == player_counter:
        print("You win!")
        print("Moves:", moves)
    elif winner != empty and winner != player_counter:
        print("You lose!")
    else:
        print("It's a tie!")
    input("Press enter to quit.")
    quit()

def connect():
    clear()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = ""
    while not server:
        server = input("Server address: ")
    port = 65432
    data_buf = 4096
    print("Attempting to connect to server...")
    try:
        s.connect((server, port))
    except:
        print("Unable to connect to server.")
        input("\nPress enter to quit.")
        quit()
    print("Connection established.")
    print("Searching for an opponent...")
    while True:
        data = s.recv(data_buf)
        if not data:
            break
        response = data.decode()
        if response == "ready":
            print("Opponent found.")
            print("Waiting for opponent to make the first move...")
            while True:
                data = s.recv(data_buf)
                if not data:
                    break
                response = data.decode("utf-8")
                clear()
                print_board()
                print("Waiting for opponent to make a move...")
                if "go" in response or "invalid_pos" in response:
                    c = response.split("||")[1] # counter
                    b = response.split("||")[2] # board raw data
                    bc = b.split(",") # board counters
                    i = 0
                    for nc in bc: # for counter in board counters
                        board[i] = nc# place them on the board
                        i += 1
                    print("It is your turn")
                    i = -1
                    clear()
                    print_board()
                    print("You are ", c)
                    while True:
                        try:
                            i = int(input("Choose a position: ")) - 1
                        except:
                            continue
                        if i not in range(9):
                            continue
                        break
                    s.send(str(i).encode())
                    place(c, i)
                    clear()
                    print_board()
                    print("Waiting for opponent to make a move...")
                elif "over" in response:
                    c = response.split("||")[1]  # counter
                    b = response.split("||")[2]  # board raw data
                    bc = b.split(",")  # board counters
                    i = 0
                    for nc in bc:  # for counter in board counters
                        board[i] = nc  # place them on the board
                        i += 1
                    clear()
                    print_board()
                    print("Game Over!")
                    print(c, "wins!")
                    input("Press enter to quit.")
                    quit()

        s.send("blah".encode(FORMAT))
    s.close()
    input("Lost connection to server. Press enter to quit.")
    quit()

if "idlelib.run" in sys.modules:
    idle = True
else:
    idle = False

err_failure = 1
err_success = 0

empty = " "
board = [empty, empty, empty,
         empty, empty, empty,
         empty, empty, empty]
options = ["Find a match",
           "Play offline",
           "Quit"]
# player_counter = "O"
menu()