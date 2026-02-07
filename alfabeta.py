import math
import random
from constants import RED, GREEN, WHITE
from moves import get_all_valid_moves, apply_move
from heuristic import heuristic_evaluation
from victory import is_game_over

TRANSPOSITION_TABLE = {}

def board_to_tuple(board):
    return tuple(sorted(board.items()))

def evaluate_move_potential(board, move):
    q, r = move
    neighbors = [(q+1, r-1), (q+1, r), (q, r+1), (q-1, r+1), (q-1, r), (q, r-1)]
    score = 0
    for n in neighbors:
        if n in board and board[n] != WHITE:
            score += 1
    return score

def get_best_move(board, depth, player_color, N):
    global TRANSPOSITION_TABLE
    TRANSPOSITION_TABLE = {}
    
    print(f"AI ({player_color}) razmislja na dubini {depth}...")
    
    valid_moves = get_all_valid_moves(board)
    if not valid_moves:
        return None

    valid_moves.sort(key=lambda m: evaluate_move_potential(board, m), reverse=True)

    best_move = None
    alpha = -math.inf
    beta = math.inf
    best_val = -math.inf
    
    if len(valid_moves) == len(board):
        return random.choice(valid_moves)

    for move in valid_moves:
        new_board = apply_move(board, move, player_color)
        
        move_val = minimax(new_board, depth - 1, alpha, beta, False, player_color, N)
        
        if move_val > best_val:
            best_val = move_val
            best_move = move
        
        alpha = max(alpha, best_val)
        
    print(f"Najbolja procena poteza: {best_val}")
    return best_move

def minimax(board, depth, alpha, beta, maximizing_player, player_color, N):
    board_key = (board_to_tuple(board), maximizing_player)
    if board_key in TRANSPOSITION_TABLE:
        return TRANSPOSITION_TABLE[board_key]

    game_over, winner = is_game_over(board, N)
    if game_over:
        if winner == player_color:
            return 100000 + depth
        else:
            return -100000 - depth
    if depth == 0:
        score = heuristic_evaluation(board, player_color, N)
        TRANSPOSITION_TABLE[board_key] = score
        return score

    valid_moves = get_all_valid_moves(board)
    if not valid_moves:
        return 0
    if depth > 1:
        valid_moves.sort(key=lambda m: evaluate_move_potential(board, m), reverse=True)

    opponent = GREEN if player_color == RED else RED

    if maximizing_player:
        max_eval = -math.inf
        for move in valid_moves:
            new_board = apply_move(board, move, player_color)
            eval = minimax(new_board, depth - 1, alpha, beta, False, player_color, N)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        
        TRANSPOSITION_TABLE[board_key] = max_eval
        return max_eval
    else:
        min_eval = math.inf
        for move in valid_moves:
            new_board = apply_move(board, move, opponent)
            eval = minimax(new_board, depth - 1, alpha, beta, True, player_color, N)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        
        TRANSPOSITION_TABLE[board_key] = min_eval
        return min_eval