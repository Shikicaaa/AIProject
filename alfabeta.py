import math
import random
from constants import RED, GREEN, WHITE
from moves import get_all_valid_moves, apply_move
from heuristic import heuristic_evaluation
from victory import is_game_over

EXACT = 0
LOWER_BOUND = 1
UPPER_BOUND = 2

HISTORY_TABLE = {}

KILLER_MOVES = {}


def board_to_tuple(board):
    return tuple(sorted(board.items()))


def evaluate_move_potential(board, move, player_color, opponent_color, N):

    q, r = move
    radius = N
    score = 0

    neighbors = [(q+1, r-1), (q+1, r), (q, r+1), (q-1, r+1), (q-1, r), (q, r-1)]

    own_neighbors = 0
    for n in neighbors:
        if n in board:
            if board[n] == player_color:
                own_neighbors += 1
                score += 3
            elif board[n] == opponent_color:
                score += 1

    if abs(q) == radius or abs(r) == radius or abs(q + r) == radius:
        score += 5

    distance_from_center = max(abs(q), abs(r), abs(q + r))
    score += max(0, radius - distance_from_center)

    if own_neighbors >= 2:
        score += 4

    if move in HISTORY_TABLE:
        score += HISTORY_TABLE[move]

    return score


def order_moves(board, moves, player_color, depth, N):
    opponent = GREEN if player_color == RED else RED

    scored_moves = []
    killer_set = set(KILLER_MOVES.get(depth, []))

    for move in moves:
        score = evaluate_move_potential(board, move, player_color, opponent, N)

        # Killer potez bonus - ovi potezi su izazvali odsecanje na istoj dubini
        if move in killer_set:
            score += 100

        scored_moves.append((score, move))

    scored_moves.sort(reverse=True)
    return [m for _, m in scored_moves]


def store_killer_move(depth, move):
    if depth not in KILLER_MOVES:
        KILLER_MOVES[depth] = []
    killers = KILLER_MOVES[depth]
    if move not in killers:
        killers.insert(0, move)
        if len(killers) > 2:
            killers.pop()


def get_best_move(board, max_depth, player_color, N):
    global HISTORY_TABLE, KILLER_MOVES
    HISTORY_TABLE = {}
    KILLER_MOVES = {}
    transposition_table = {}

    print(f"AI ({player_color}) razmislja na dubini {max_depth}...")

    valid_moves = get_all_valid_moves(board)
    if not valid_moves:
        return None

    white_count = sum(1 for v in board.values() if v == WHITE)
    colored_count = sum(1 for v in board.values() if v in (RED, GREEN))
    if white_count > 0 and colored_count > 0:
        ratio = white_count / (white_count + colored_count - (6 * N))
        if ratio > 0.95:  # Skoro prazna tabla
            center_moves = [(q, r) for q, r in valid_moves
                            if max(abs(q), abs(r), abs(q+r)) <= N // 2 + 1]
            if center_moves:
                return random.choice(center_moves)

    best_move = valid_moves[0]
    best_val = -math.inf

    for current_depth in range(1, max_depth + 1):
        current_best_move = None
        current_best_val = -math.inf
        alpha = -math.inf
        beta = math.inf

        ordered_moves = order_moves(board, valid_moves, player_color, 0, N)

        if best_move in ordered_moves:
            ordered_moves.remove(best_move)
            ordered_moves.insert(0, best_move)

        for i, move in enumerate(ordered_moves):
            new_board = apply_move(board, move, player_color)

            if i == 0:
                move_val = minimax(new_board, current_depth - 1, alpha, beta,
                                   False, player_color, N, transposition_table)
            else:
                move_val = minimax(new_board, current_depth - 1, alpha, alpha + 1,
                                   False, player_color, N, transposition_table)
                if alpha < move_val < beta:
                    move_val = minimax(new_board, current_depth - 1, alpha, beta,
                                       False, player_color, N, transposition_table)

            if move_val > current_best_val:
                current_best_val = move_val
                current_best_move = move

            alpha = max(alpha, move_val)

        if current_best_move is not None:
            best_move = current_best_move
            best_val = current_best_val

        print(f"  Dubina {current_depth}: procena = {best_val}")

        if best_val >= 50000:
            break

    print(f"Najbolja procena poteza: {best_val}")
    return best_move


def minimax(board, depth, alpha, beta, maximizing_player, player_color, N, tt):
    original_alpha = alpha

    board_key = (board_to_tuple(board), maximizing_player)
    if board_key in tt:
        tt_depth, tt_flag, tt_value = tt[board_key]
        if tt_depth >= depth:
            if tt_flag == EXACT:
                return tt_value
            elif tt_flag == LOWER_BOUND:
                alpha = max(alpha, tt_value)
            elif tt_flag == UPPER_BOUND:
                beta = min(beta, tt_value)
            if alpha >= beta:
                return tt_value

    game_over, winner = is_game_over(board, N, silent=True)
    if game_over:
        if winner == player_color:
            return 100000 + depth   
        elif winner == "DRAW":
            return 0
        else:
            return -100000 - depth

    if depth == 0:
        score = heuristic_evaluation(board, player_color, N)
        tt[board_key] = (depth, EXACT, score)
        return score

    valid_moves = get_all_valid_moves(board)
    if not valid_moves:
        return 0

    opponent = GREEN if player_color == RED else RED
    current_color = player_color if maximizing_player else opponent

    if depth > 1:
        ordered_moves = order_moves(board, valid_moves, current_color, depth, N)
    else:
        ordered_moves = valid_moves

    if maximizing_player:
        max_eval = -math.inf
        for move in ordered_moves:
            new_board = apply_move(board, move, player_color)
            eval_score = minimax(new_board, depth - 1, alpha, beta,
                                 False, player_color, N, tt)

            if eval_score > max_eval:
                max_eval = eval_score
            alpha = max(alpha, eval_score)

            if beta <= alpha:
                store_killer_move(depth, move)
                HISTORY_TABLE[move] = HISTORY_TABLE.get(move, 0) + depth * depth
                break

        if max_eval <= original_alpha:
            tt_flag = UPPER_BOUND   
        elif max_eval >= beta:
            tt_flag = LOWER_BOUND   
        else:
            tt_flag = EXACT         

        tt[board_key] = (depth, tt_flag, max_eval)
        return max_eval
    else:
        min_eval = math.inf
        for move in ordered_moves:
            new_board = apply_move(board, move, opponent)
            eval_score = minimax(new_board, depth - 1, alpha, beta,
                                 True, player_color, N, tt)

            if eval_score < min_eval:
                min_eval = eval_score
            beta = min(beta, eval_score)

            if beta <= alpha:
                store_killer_move(depth, move)
                HISTORY_TABLE[move] = HISTORY_TABLE.get(move, 0) + depth * depth
                break

        if min_eval <= original_alpha:
            tt_flag = UPPER_BOUND
        elif min_eval >= beta:
            tt_flag = LOWER_BOUND
        else:
            tt_flag = EXACT

        tt[board_key] = (depth, tt_flag, min_eval)
        return min_eval