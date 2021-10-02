import socket

ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004

print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

res = ClientMultiSocket.recv(1024)
while True:
    Input = input('Hey there: ')
    ClientMultiSocket.send(str.encode(Input))
    res = ClientMultiSocket.recv(1024)
    print(res.decode('utf-8'))

ClientMultiSocket.close()

# import threading
# # create a separate thread to send and receive data from the server
# def create_thread(target):
#     thread = threading.Thread(target=target)
#     thread.daemon = True #thread that runs in the background to support main/non-daemon thread
#     thread.start() #this will start a separate thread

# import socket

# HOST = '127.0.0.1'
# PORT = 65432

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((HOST, PORT))

# def receive_data():
#     #receive data from server
#     while True:
#         data = sock.recv(1024)
#         print(data)

# create_thread(receive_data)