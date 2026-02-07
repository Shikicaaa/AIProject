from constants import RED, GREEN
from islands import get_island_groups, get_shortest_path_length
from moves import get_all_valid_moves


def check_victory(board, player_color, N, silent=False):
    islands = get_island_groups(board, N, player_color)
    
    if len(islands) < 2:
        return False 
    for i in range(len(islands)):
        for j in range(i + 1, len(islands)):
            island_a = islands[i]
            island_b = islands[j]
            
            min_path = float('inf')
            max_path = 7 if N == 5 else (10 if N == 7 else 13)
            connected = False
            
            for start_node in island_a:
                length = get_shortest_path_length(board, start_node, island_b, player_color)
                if length > 0:
                    connected = True
                    if length < min_path:
                        min_path = length
            
            if connected and min_path >= max_path:
               if not silent:
                    print(f"Pobedio je {player_color}! Povezana ostrva putanjom duzine {min_path}.")
               return True
                
    return False


def is_game_over(board, N, silent=False):

    if check_victory(board, RED, N, silent=silent):
        return True, RED
    if check_victory(board, GREEN, N, silent=silent):
        return True, GREEN

    if not get_all_valid_moves(board):
        return True, "DRAW"

    return False, None
