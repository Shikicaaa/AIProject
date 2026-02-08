import sys
import random
from constants import RED, GREEN
from board import generate_atoll_board, render_board
from setup import game_mode, first_player, starting_color, setup_custom_board, determine_next_player
from moves import get_all_valid_moves, process_turn
from victory import check_victory
from alfabeta import get_best_move


def main():
    try:
        N = int(sys.argv[1]) if len(sys.argv) > 1 else int(input("Unesite dimenziju table: "))
    except:
        N = 5

    AI_DEPTH = 4

    game_board = generate_atoll_board(N)

    vs_computer = game_mode() 

    computer_plays_first = first_player() if vs_computer else False
    
    red_starts = starting_color()

    print("\nDo you want set a state of the board? (y/n)")
    if input().lower() == 'y':
        setup_custom_board(game_board, N, red_starts)
        to_play_red = determine_next_player(game_board, red_starts)
    else:
        to_play_red = red_starts

    computer_color = None
    if vs_computer:
        if computer_plays_first:
            computer_color = RED if red_starts else GREEN
        else:
            if red_starts:
                computer_color = GREEN
            else:
                computer_color = RED
        
        print(f"Komp igra kao: {computer_color}")

    game_running = True

    while game_running:
        render_board(game_board, N)

        current_color = RED if to_play_red else GREEN
        print(f"Na potezu je: {'RED' if to_play_red else 'GREEN'} {current_color}")
        

        if vs_computer and current_color == computer_color:
            
            best_move = get_best_move(game_board, AI_DEPTH, computer_color, N)
            
            if best_move:
                game_board[best_move] = current_color
                print(f"Racunar je odigrao pametno na: {best_move}")
            else:
                print("Racunar nema validnih poteza!")
        else:
            process_turn(game_board, N, current_color)

        if check_victory(game_board, current_color, N, silent=True):
            render_board(game_board, N)
            print(f"\n========================================")
            print(f" KRAJ IGRE! POBEDNIK JE {current_color}")
            print(f"========================================")
            game_running = False
            break
        
        if not get_all_valid_moves(game_board):
            render_board(game_board, N)
            print("\nNERESENO! Nema vise slobodnih polja.")
            game_running = False
            break

        to_play_red = not to_play_red


if __name__ == "__main__":
    main()
