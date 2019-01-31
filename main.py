from Player import *
from Go import *
from GlobalVariables import *

def main():
    player_1 = Player('Dang')
    player_2 = Player('Khoi')
    game = Go()
    while not game.is_over():
        while not player_1.is_ready():
            game.make_move(player_1.play())
        while not player_2.is_ready():
            game.make_move(player_2.play())

if __name__ == "__main__":
    main()
