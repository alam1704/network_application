# import socket module
import socket

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
        self.player1 = "player1"
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
                choice = input("[A]bort, [C]hange port, or [R]etry?")
                if (choice.lower() == 'a'):
                    exit()
                elif (choice.lower() == 'c'):
                    self.PORT = input("Please enter the port:")

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
        
server= Server()
while True:
    server.waiting_for_connection()
    server.server_send("welcome to server")
    break

for i in range(5):
    while True:
        move = input("Enter your move: ")
        server.player_pos['X'].append(move)
        print(server.player_pos)
        server.server_send(move)
        break
    while True:
        move = server.server_recv()
        server.player_pos['O'].append(move)
        print(server.player_pos)
        break
server.close()