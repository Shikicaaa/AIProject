from constants import RED, GREEN
from islands import get_island_groups, get_shortest_path_length
from victory import check_victory


def heuristic_evaluation(board, player_color, N):
    opponent = GREEN if player_color == RED else RED
    
    if check_victory(board, player_color, N, silent=True):
        return 100000 
    if check_victory(board, opponent, N, silent=True):
        return -100000

    score = 0
    
    my_islands = get_island_groups(board, N, player_color)
    
    if len(my_islands) >= 2:
        max_path_len = 0
        
        for i in range(len(my_islands)):
            for j in range(i + 1, len(my_islands)):
                group_a = my_islands[i]
                group_b = my_islands[j]
                
                for start_node in group_a:
                    length = get_shortest_path_length(board, start_node, group_b, player_color)
                    if length > max_path_len:
                        max_path_len = length
        
        score += max_path_len * 100

    player_stones = 0
    opponent_stones = 0
    for val in board.values():
        if val == player_color:
            player_stones += 1
        elif val == opponent:
            opponent_stones += 1
            
    score += (player_stones - opponent_stones) * 10

    opp_islands = get_island_groups(board, N, opponent)
    if len(opp_islands) >= 2:
        opp_max_path = 0
        for i in range(len(opp_islands)):
            for j in range(i + 1, len(opp_islands)):
                group_a = opp_islands[i]
                group_b = opp_islands[j]
                for start_node in group_a:
                    length = get_shortest_path_length(board, start_node, group_b, opponent)
                    if length > opp_max_path:
                        opp_max_path = length
        
        score -= opp_max_path * 100

    return score
