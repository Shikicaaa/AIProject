import sys
from constants import RED, GREEN, WHITE
from coordinates import parse_move


def game_mode():
    while True:
        print("\n---Select mode---")
        print("1.Human vs Human")
        print("2.Human vs Computer")
        choice = input("1 or 2:")

        if choice == '1':
            return False
        elif choice =='2':
            return True
        else:
            print("Invald input,try again")


def first_player():
    while True:
        print("\n---Who plays first?---")
        print("1.Human")
        print("2.Computer")
        choice = input("1 or 2:")

        if choice == '1':
            return False
        elif choice =='2':
            return True
        else:
            print("Invald input,try again")


def starting_color():
    while True:
        print("\n---Which color starts?---") 
        print(f"1.Red({RED})")      
        print(f"2.Green{GREEN}")
        choice = input("1 or 2:")

        if choice == '1':
            return True
        elif choice =='2':
            return False
        else:
            print("Invald input,try again")


def setup_custom_board(board, N, red_starts):
    while True:
        print("\nEnter the state sequence (e.g., 'e2 g e4 g a5 r'):")
        raw_input = input("Input: ").strip().lower()

        if not raw_input:
            print("Starting with an empty board.")
            break

        parts = raw_input.split()

        if len(parts) % 2 != 0:
            print("Error: Invalid sequence. Each position must have a color (R or G).")
            continue

        temp_moves = []
        is_valid = True

        count_r = 0
        count_g = 0

        for i in range(0, len(parts), 2):
            pos_str = parts[i]
            color_code = parts[i + 1].upper()

            if color_code == 'R':
                color = RED
                count_r += 1
            elif color_code == 'G':
                color = GREEN
                count_g += 1
            else:
                print(f"Error: Invalid color code '{color_code}'.")
                is_valid = False
                break

            coords = parse_move(pos_str, N)
            if coords is None or coords not in board:
                print(f"Error: Position '{pos_str}' is invalid.")
                is_valid = False
                break

            if board[coords] != WHITE:
                print(f"Error: Position '{pos_str}' is not a free field.")
                is_valid = False
                break

            temp_moves.append((coords, color))

        if is_valid:
            diff = count_r - count_g

            if red_starts:
                if not (diff == 0 or diff == 1):
                    print(f"Error: Invalid stone count. Red started, but Red has {count_r} and Green has {count_g}.")
                    is_valid = False
            else:
                if not (diff == 0 or diff == -1):
                    print(f"Error: Invalid stone count. Green started, but Green has {count_g} and Red has {count_r}.")
                    is_valid = False

        if is_valid:
            for coords, color in temp_moves:
                board[coords] = color
            print("State successfully set!")
            break
        else:
            print("Please re-enter the entire sequence correctly.")


def determine_next_player(board, red_starts):
    red_count = 0
    green_count = 0

    for color in board.values():
        if color == RED:
            red_count += 1
        elif color == GREEN:
            green_count += 1

    if red_starts:
        if red_count == green_count:
            return True
        elif red_count > green_count:
            return False
    else:
        if green_count == red_count:
            return False
        elif green_count > red_count:
            return True

    return True if red_count <= green_count else False
