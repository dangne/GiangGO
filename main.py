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



        # --------------- PLAYER 1 --------------- #
        print("Player 1 turn")
        score = game.score()
        print("Player 1 score:", score[0])
        print("Player 2 score:", score[1])
        if P1.kind == AI:
            P1.get_game_status(game.get_status())
        while game.turn == PLAYER_1:
            if P1.kind == AI:
                P1.get_valid_moves(game.get_valid_moves())
                game.read_console_input(P1.make_move())
            game.update()



        # --------------- PLAYER 2 --------------- #
        print("Player 1 turn")
        print("Player 2 turn")
        score = game.score()
        print("Player 1 score:", score[0])
        print("Player 2 score:", score[1])
        if P2.kind == AI:
            P2.get_game_status(game.get_status())
        while game.turn == PLAYER_2:
            if P2.kind == AI:
                P2.get_valid_moves(game.get_valid_moves())
                game.read_console_input(P2.make_move())
            game.update()

if __name__ == "__main__":
    main()
