from constants import RED, GREEN
from collections import deque
from hex_utils import get_neighbors
from board import get_island_map


def get_connected_components(board, player_color):

    visited = set()
    components = []

    for pos, color in board.items():
        if color == player_color and pos not in visited:
            component = set()
            queue = deque([pos])
            visited.add(pos)
            component.add(pos)

            while queue:
                curr = queue.popleft()
                for neighbor in get_neighbors(curr):
                    if neighbor in board and board[neighbor] == player_color and neighbor not in visited:
                        visited.add(neighbor)
                        component.add(neighbor)
                        queue.append(neighbor)
            components.append(component)
    return components


def calculate_circular_distance(id1, id2, total_islands=12):
    if id1 == id2:
        return 1

    idx1 = id1 - 1
    idx2 = id2 - 1

    diff = abs(idx1 - idx2)

    path1 = diff + 1

    path2 = total_islands - diff + 1

    return min(path1, path2)


def check_victory(board, player_color, N, silent=False):

    island_map = get_island_map(N)

    components = get_connected_components(board, player_color)

    for comp in components:

        touched_islands = set()
        for pos in comp:
            if pos in island_map:
                touched_islands.add(island_map[pos])

        touched_list = list(touched_islands)

        if len(touched_list) < 2:
            continue

        for i in range(len(touched_list)):
            for j in range(i + 1, len(touched_list)):
                id_a = touched_list[i]
                id_b = touched_list[j]

                dist = calculate_circular_distance(id_a, id_b)

                if dist >= 7:
                    if not silent:
                        print(f"Pobedio je {player_color}!")
                        print(f"Spojena ostrva {id_a} i {id_b}.")
                        print(f"Distanca (broj ostrva): {dist}")
                    return True

    return False


def is_game_over(board, N, silent=False):
    if check_victory(board, RED, N, silent=silent):
        return True, RED
    if check_victory(board, GREEN, N, silent=silent):
        return True, GREEN

    from moves import get_all_valid_moves
    if not get_all_valid_moves(board):
        return True, "DRAW"

    return False, None