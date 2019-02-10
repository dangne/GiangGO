from Player import *
from Go import *
from Constants import *
from time import sleep

def main():
    # In training mode, delays are removed to enhance processing speed
    training_mode = True

    P1 = Player(name = 'Dang'   , kind = AI, port = PLAYER_1)
    P2 = Player(name = 'GiangGO', kind = AI, port = PLAYER_2)
    game = Go(game_mode = (P1.kind, P2.kind))
    print("Game begin!")
    while game.is_replay:
        while not game.over:
    
    
    
            # --------------- PLAYER 1 --------------- #
            score = game.score()
            print("--- Player 1 turn")
            print("Player 1 score:", score[0])
            print("Player 2 score:", score[1])
            game.is_pass = False
            if P1.kind == AI:
                P1.get_game_status(game.get_status())
            valid_moves = game.get_valid_moves()
            if len(valid_moves) == 0:
                game.over = True
            while not game.over and not game.is_pass and game.turn == PLAYER_1:
                if P1.kind == AI:
                    P1.get_valid_moves(valid_moves)
                    game.read_console_input(P1.make_move())
                game.update()
    
            if not game.is_pass: # If the player did not pass, reset the pass counter
                game.pass_cnt = 0
    
            if P1.kind == P2.kind == AI and not training_mode: 
                sleep(0.5)
    
            # --------------- PLAYER 2 --------------- #
            score = game.score()
            print("--- Player 2 turn")
            print("Player 1 score:", score[0])
            print("Player 2 score:", score[1])
            game.is_pass = False
            if P2.kind == AI:
                P2.get_game_status(game.get_status())
            valid_moves = game.get_valid_moves()
            if len(valid_moves) == 0:
                game.over = True
            while not game.over and not game.is_pass and game.turn == PLAYER_2:
                if P2.kind == AI:
                    P2.get_valid_moves(valid_moves)
                    game.read_console_input(P2.make_move())
                game.update()
    
            if not game.is_pass: # If the player did not pass, reset the pass counter
                game.pass_cnt = 0

            if P1.kind == P2.kind == AI and not training_mode: 
                sleep(0.5)
        game.result_and_replay()
        


if __name__ == "__main__":
    main()
