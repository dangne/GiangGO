from Player import *
from Go import *
from Constants import *
from time import sleep

def main():
    P1 = Player(name = 'Dang'   , kind = HUMAN, port = PLAYER_1)
    P2 = Player(name = 'GiangGO', kind = AI, port = PLAYER_2)
    game = Go(game_mode = (P1.kind, P2.kind))
    print("Game begin!")
    while not game.over:
        print("Player 1 turn")
        while game.turn == PLAYER_1:
            if not P1.kind:
                P1.get_game_status(game.get_status())
                game.read_console_input(P1.make_move())
            game.update()

        print("Player 2 turn")
        while game.turn == PLAYER_2:
            if not P2.kind:
                P2.get_game_status(game.get_status())
                game.read_console_input(P2.make_move())
            game.update()

if __name__ == "__main__":
    main()
