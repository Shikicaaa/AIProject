from collections import deque
from hex_utils import get_neighbors


def get_island_groups(board, N, color):
    radius = N
    visited = set()
    islands = []
    
    for pos, val in board.items():
        q, r = pos
        if val == color and pos not in visited:
            if abs(q) == radius or abs(r) == radius or abs(q + r) == radius:
                group = set()
                queue = deque([pos])
                visited.add(pos)
                group.add(pos)
                
                while queue:
                    curr = queue.popleft()
                    for neighbor in get_neighbors(curr):
                        if (neighbor in board and board[neighbor] == color and 
                            neighbor not in visited):
                           
                            nq, nr = neighbor
                            if abs(nq) == radius or abs(nr) == radius or abs(nq + nr) == radius:
                                visited.add(neighbor)
                                group.add(neighbor)
                                queue.append(neighbor)
                islands.append(group)
    return islands


def get_shortest_path_length(board, start_node, target_group, color):
    queue = deque([(start_node, 1)])
    visited = {start_node}
    
    while queue:
        curr, length = queue.popleft()
        
        if curr in target_group:
            return length
        
        for neighbor in get_neighbors(curr):
            if neighbor in board and board[neighbor] == color and neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, length + 1))
    return 0
