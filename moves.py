import sys
from constants import WHITE


def get_all_valid_moves(board):
    moves = []
    for pos, val in board.items():
        if val == WHITE:
            moves.append(pos)
    return moves


def apply_move(board, move, player_color):
    new_board = board.copy()
    new_board[move] = player_color
    return new_board


def get_next_states(board, player_color):
    valid_moves = get_all_valid_moves(board)
    next_states = []
    
    for move in valid_moves:
        new_state = apply_move(board, move, player_color)
        next_states.append((move, new_state))
        
    return next_states


def play_move(board, move_str, N, player_color):
    from coordinates import parse_move
    
    coords = parse_move(move_str, N)
    
    if coords is None:
        print(f"Error: Invalid move format '{move_str}'. Try e.g. E5.")
        return False

    q, r = coords

    if (q, r) not in board:
        print(f"Error: Field {move_str} (q={q}, r={r}) does not exist on the board.")
        return False

    if board[(q, r)] != WHITE:
        print(f"Error: Field {move_str} is not free.")
        return False

    board[(q, r)] = player_color
    print(f"Placed at {move_str} (internal: {q}, {r})")
    return True


def process_turn(board, N, color):
    while True:
        move = input("\nEnter move (e.g. E5) or 'exit': ")

        if move.lower() == 'exit':
            sys.exit()

        if play_move(board, move, N, color):
            return

        print("Try again.")
