from Player import *
from Go import *
from Constants import *

def main():
    # Instantiate Game and Players objects
    P1 = Player(name = 'Dang'   , kind = HUMAN)
    P2 = Player(name = 'GiangGO', kind = HUMAN)
    game = Go(game_mode = (P1.kind, P2.kind), display = True, delay = False)
    print("Game begin!")

    # Main game
    while game.replay:
        while not game.over:
            # --------------- PLAYER 1 --------------- #

            # Print current score
            score = game.score()

            # Receive player's move
            if P1.kind == AI:
                # For AI: no need to wait
                P1.recv_game_data(game.get_game_data())
                game.read_console_input(P1.play())
                game.update()
            else:
                # For HUMAN: the game waits until player make its move
                while game.turn == PLAYER_1:
                    game.update()


            # --------------- PLAYER 2 --------------- #

            # Print current score
            score = game.score()

            # Receive player's move
            if P2.kind == AI:
                # For AI: no need to wait
                P2.recv_game_data(game.get_game_data())
                game.read_console_input(P2.play())
                game.update()
            else:
                # For HUMAN: the game waits until player make its move
                while game.turn == PLAYER_2:
                    game.update()

        game.result_and_replay()

if __name__ == "__main__":
    main()
