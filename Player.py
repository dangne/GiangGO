from Constants import *
from random import choice

class Player:
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind
        print("Player " + self.name + " say hello!")

    def recv_game_data(self, game_data):
        self.game_status = game_data[0]
        self.valid_moves = game_data[1]
        self.my_score, self.opponent_score = game_data[2]

    def play(self):
        return choice(self.valid_moves)

def main():
    pass

# For debugging purpose
if __name__ == "__main__":
    main()
