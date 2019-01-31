from Player import *
from Go import *
from Constants import *
from time import sleep

def main():
    player_1 = Player(name = 'Dang', is_human = True)
    player_2 = Player(name = 'Khoi', is_human = False)
    game = Go(game_mode = 0, display = True)
    while not game.is_over():
        game.make_move(player_1.play())
        game.make_move(player_2.play())
        game.update()
        game.root.update()
        sleep(0.01)

if __name__ == "__main__":
    main()
