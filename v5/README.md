# Develop and Implement an Algorithm in Python

1. Develop and describe an algorithmic solution for an application that utilises two way communication over a network (300 - 500 words)

Tic Tac Toe Network game is a simple two player game over the network. The server is default to player 1 and the client is defaulted to player 2. A Server class and Client class has been initialised in two separate files and a separate Board class python file has been created to handle the game board and checks for a winner or tie. 

The Server file should be opened first and listens for a client. Once the server accepts and connects to the client, the game will start. The Server will ask for a "move" as a string and sent over the sockets, but stored on the Server as an integer as "move_int". The game then checks the move_int for any handling errors otherwise, is stored in a dictionary in the initialised method. The Server board then gets updated and then waits for receiving message from the Client.

On the client side, the client is waiting for the Server to make a move. Like Server, the move is stored as a string and another variable "move_int" is stored as an int. The move is updated on the Client side and checks for winner. Note: it does not check for a tie because the Client will always have one move less than the Server. 




2. Develop a flowchart for an application that outlines the control flow of the app, and illustrates the operation of an algorithm based on the solution you have described.