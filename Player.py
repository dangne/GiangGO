import socket

# Player object for AI will act as a server
# The AI will be implemented in a different python program and it will act as a client
class Player:
    def __init__(self, name, is_human):
        self.name = name
        self.is_human = is_human
        print('Player', self.name, 'say hello!')

        if not is_human:
            self.setup_networking()

    def setup_networking(self):
        # Networking configuration
        self.host = '127.0.0.1'
        self.port = 5000

        # Create socket object
        self.s = socket.socket()
        self.s.bind((self.host, self.port))

        # Connect to AI
        self.s.listen(1) 
        print("Waiting for connection")

        # The program will wait until a connection is formed
        self.connection, address = self.s.accept()
        print("Connection successful")

    def make_move(self):
        if not self.is_human:
            move = self.connection.recv(1024)
            if move != b'q':
                move = [int(i) for i in str(move, 'utf-8').split()]
            return move

    def get_game_status(self, game_status):
        if not self.is_human:
            self.connection.send(bytes(game_status)) 

    def destroy(self):
        self.connection.close()

# For debugging purpose
if __name__ == "__main__":
    player = Player(name = 'Test agent', is_human = False)
    while 1:
        move = player.make_move()
        print(player.name, "just go", move)
        if move == b'q':
            break
    player.destroy()
