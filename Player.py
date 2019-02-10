from Constants import *
import socket

# Player object for AI will act as a server
# The AI will be implemented in a different python program and it will act as a client
class Player:
    def __init__(self, name, kind, port):
        self.name = name
        self.kind = kind 
        print('Player', self.name, 'say hello!')

        if not self.kind == HUMAN:
            self.setup_networking(port)

    def setup_networking(self, port):
        # Networking configuration
        self.host = '127.0.0.1'
        self.port = 5000 + port
        self.s = socket.socket()

        # Connect
        connect_success = False
        while not connect_success:
            try:
                self.s.bind((self.host, self.port))
                connect_success = True
            except:
                self.port += 1

        # Connect to AI
        print("Bind " + self.name + " to socket successfully")

        self.s.listen(1) 
        print("Waiting for connection")
        print("Note: Run pseudoAI.py as a separate program to complete the connection")

        # The program will wait until a connection is formed
        self.connection, self.address = self.s.accept()
        print("Connection successful")
 
    def make_move(self):
        if self.kind != HUMAN:
            move = list(self.connection.recv(1024))
             
            return move

    def get_game_status(self, game_status):
        if self.kind != HUMAN:
            self.connection.send(bytes(game_status)) 

    def get_valid_moves(self, valid_moves):
        if self.kind != HUMAN:
            self.connection.send(bytes(valid_moves))

    def destroy(self):
        self.connection.close()

# For debugging purpose
if __name__ == "__main__":
    player = Player(name = 'Test agent', kind = AI)
    while 1:
        move = player.make_move()
        print(player.name, "just go", move)
        if move == b'q':
            break
    player.destroy()
