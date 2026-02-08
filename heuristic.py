from collections import deque
from constants import RED, GREEN, WHITE
from islands import get_island_groups, get_shortest_path_length
from hex_utils import get_neighbors
from victory import check_victory


def heuristic_evaluation(board, player_color, N):
    opponent = GREEN if player_color == RED else RED
    radius = N

    if check_victory(board, player_color, N, silent=True):
        return 100000
    if check_victory(board, opponent, N, silent=True):
        return -100000

    score = 0

    my_stones = set()
    opp_stones = set()
    empty_cells = set()
    for pos, val in board.items():
        if val == player_color:
            my_stones.add(pos)
        elif val == opponent:
            opp_stones.add(pos)
        elif val == WHITE:
            empty_cells.add(pos)

    my_islands = get_island_groups(board, N, player_color)
    opp_islands = get_island_groups(board, N, opponent)

    my_connectivity = _evaluate_island_connectivity(board, my_islands, player_color)
    opp_connectivity = _evaluate_island_connectivity(board, opp_islands, opponent)
    score += my_connectivity * 150
    score -= opp_connectivity * 150

    score += len(my_islands) * 20
    score -= len(opp_islands) * 20

    for pos in my_stones:
        q, r = pos
        dist = max(abs(q), abs(r), abs(q + r))
        if dist < radius:
            score += (radius - dist) * 5

    for pos in opp_stones:
        q, r = pos
        dist = max(abs(q), abs(r), abs(q + r))
        if dist < radius:
            score -= (radius - dist) * 5

    my_conn = _count_connections(board, my_stones, player_color)
    opp_conn = _count_connections(board, opp_stones, opponent)
    score += my_conn * 8
    score -= opp_conn * 8

    my_bridges = _count_bridges(board, my_stones, player_color)
    opp_bridges = _count_bridges(board, opp_stones, opponent)
    score += my_bridges * 12
    score -= opp_bridges * 12

    my_border_pot = _border_connection_potential(board, my_stones, my_islands, N)
    opp_border_pot = _border_connection_potential(board, opp_stones, opp_islands, N)
    score += my_border_pot * 10
    score -= opp_border_pot * 10

    score += (len(my_stones) - len(opp_stones)) * 3

    return score


def _evaluate_island_connectivity(board, islands, color):
    if len(islands) < 2:
        return 0

    max_path = 0
    connected_pairs = 0

    for i in range(len(islands)):
        for j in range(i + 1, len(islands)):
            group_a = islands[i]
            group_b = islands[j]

            min_path_between = float('inf')
            is_connected = False

            for start_node in group_a:
                length = get_shortest_path_length(board, start_node, group_b, color)
                if length > 0:
                    is_connected = True
                    if length < min_path_between:
                        min_path_between = length

            if is_connected:
                connected_pairs += 1
                if min_path_between > max_path:
                    max_path = min_path_between

    result = max_path                   
    result += connected_pairs * 2       

    return result


def _count_connections(board, stones, color):
    connections = 0
    for pos in stones:
        for neighbor in get_neighbors(pos):
            if neighbor in board and board[neighbor] == color:
                connections += 1
    return connections // 2  


def _count_bridges(board, stones, color):
    bridges = 0
    bridge_vectors = [
        ((1, 0), (0, 1)),       
        ((1, -1), (0, -1)),     
        ((1, -1), (1, 0)),      
        ((0, 1), (-1, 1)),      
        ((-1, 1), (-1, 0)),     
        ((-1, 0), (0, -1)),     

    ]

    for pos in stones:
        q, r = pos
        for (dq1, dr1), (dq2, dr2) in bridge_vectors:
            mid1 = (q + dq1, r + dr1)
            mid2 = (q + dq2, r + dr2)
            end = (q + dq1 + dq2, r + dr1 + dr2)

            if (end in board and board[end] == color and
                mid1 in board and board[mid1] == WHITE and
                mid2 in board and board[mid2] == WHITE):
                bridges += 1

    return bridges // 2  


def _border_connection_potential(board, stones, islands, N):
    radius = N
    potential = 0

    island_cells = set()
    for island in islands:
        island_cells.update(island)

    for pos in stones:
        if pos in island_cells:
            continue  # Preskoci kamenje koje je vec deo ostrva

        for neighbor in get_neighbors(pos):
            if neighbor in island_cells:
                potential += 2
                break

        q, r = pos
        dist_to_border = radius - max(abs(q), abs(r), abs(q + r))
        if dist_to_border <= 2:
            potential += 1

    return potential
