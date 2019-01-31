from Player import *
from Go import *
from Constants import *
from time import sleep

ENABLE_DELAY = True
def main():
    player_1 = Player(name = 'Dang', is_human = True)
    player_2 = Player(name = 'GiangGO', is_human = False)
    game = Go(game_mode = HUMAN_VS_AI)
    while not game.over:
        print("Game begin!")
        # Player1's turn
        print("Player 1 turn")
        while game.turn == PLAYER_1:
            if not player_1.is_human:
                player_1.get_game_status(game.get_status())
                game.read_console_input(player_1.make_move())
            game.update()
        if ENABLE_DELAY: sleep(0.01)

        # Player2's turn
        print("Player 2 turn")
        while game.turn == PLAYER_2:
            if not player_2.is_human:
                player_2.get_game_status(game.get_status())
                game.read_console_input(player_2.make_move())
            game.update()
        if ENABLE_DELAY: sleep(0.01)

if __name__ == "__main__":
    main()
