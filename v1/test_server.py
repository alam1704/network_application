import socket
import os
from _thread import *

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0

server = socket.gethostbyname(socket.gethostname())
print (server)


try:
    # Connect the host and port to server
    ServerSideSocket.bind((host,port))
except socket.error as e:
    print(str(e))

print("Socket is listening..")
ServerSideSocket.listen(5)

def multi_threaded_client(connection):
    connection.send(str.encode("Server is working:"))
    while True:
        data = connection.recv(2048)
        response = "Server message: " + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(response))

    connection.close()


while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    print("Thread Number: " + str(ThreadCount))

ServerSideSocket.close()


# import threading
# # create a separate thread to send and receive data from the client
# def create_thread(target):
#     thread = threading.Thread(target=target)
#     thread.daemon = True #thread that runs in the background to support main/non-daemon thread
#     thread.start() #this will start a separate thread


# import socket

# HOST = '127.0.0.1'
# PORT = 65432

# connection_established = False
# connection, address = None, None

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #(IPV4, TCP)
# sock.bind((HOST, PORT))
# sock.listen(1)

# def receive_data():
#     pass

# def waiting_for_connection():
#     global connection_established, connection, address
#     connection, address = sock.accept() #wait for a connection, it is a blocking method. It essentially will wait for a connection
#     print("Client is connected")
#     connection_established = True
#     receive_data()

# create_thread(waiting_for_connection)