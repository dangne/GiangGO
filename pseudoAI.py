from Constants import *
from time import sleep
import random
import socket

class PseudoAI:
    is_replay   = True
    is_over     = False
    def __init__(self, port):
        self.setup_networking(port)

    def setup_networking(self, port): # Networking configuration 
        self.host = '127.0.0.1' 
        self.port = 5000 + port
        self.s = socket.socket()

        # Connect
        connect_success = False
        while not connect_success:
            try:
                self.s.connect((self.host, self.port))
                connect_success = True
            except:
                self.port += 1

        print("Connect successfully")

    def get_game_status(self):
        self.game_status = self.s.recv(1024)

    def get_valid_moves(self):
        self.valid_moves = []
        self.incoming_data = self.s.recv(1024)
        for i in range(0, len(self.incoming_data), 2):
            self.valid_moves.append([self.incoming_data[i], self.incoming_data[i+1]])

    def play(self):
        if len(self.valid_moves) > 0:
            self.move = random.choice(self.valid_moves)
        else:
            self.move = [9, 9] # Equivalent with pass
        self.s.send(bytes(self.move))

    def destroy(self):
        self.s.close()

def main():
    agent = PseudoAI(PLAYER_1)
    sleep(0.5) # This delay is crucial for AI vs AI mode, without it, two sockets may not connect successfully
    agent2 = PseudoAI(PLAYER_2)

    while agent.is_replay:
        while not agent.over:
            # Turn 1
            agent.get_game_status()
            agent.get_valid_moves()
            agent.play()

            # Turn 2
            agent2.get_game_status()
            agent2.get_valid_moves()
            agent2.play()

    agent.destroy()
    agent2.destroy()

if __name__ == "__main__":
