FORMAT = 'UTF-8'

class Player:

    def __init__(self, username, conn):
        """Constructor for player object"""
        self.username = username
        self.conn = conn
    
    def send(self, msg):
        """send a message through a players connection"""
        self.conn.send(msg)