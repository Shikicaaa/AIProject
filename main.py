import sys
from collections import deque

RED   = '\U0001F534' # 🔴
GREEN = '\U0001F7E2' # 🟢
WHITE = '\u26AA'     # ⚪
EMPTY = '  '         # dva razmaka


def get_neighbors(hex_pos):
    q, r = hex_pos
    vectors = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]
    return [(q + dq, r + dr) for dq, dr in vectors]


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


def check_victory(board, player_color, N):
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
                print(f"Pobedio je {player_color}! Povezana ostrva putanjom dužine {min_path}.")
                return True
                
    return False


def is_game_over(board, N):
    if check_victory(board, RED, N):
        return True, RED
    if check_victory(board, GREEN, N):
        return True, GREEN
    
    if not get_all_valid_moves(board):
        return True, "DRAW"
        
    return False, None


def get_all_valid_moves(board):
    moves = []
    for pos, val in board.items():
        if val == WHITE:
            moves.append(pos)
    return moves

def apply_move(board, move, player_color):
    # ovo je priprema za minmax kao cuvamo generisemo tablu za novi potez i proveravamo kako je tu
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


def generate_atoll_board(N):
    radius = N
    board = {}

    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            if abs(q + r) <= radius:
                board[(q, r)] = WHITE

    pattern = []
    for _ in range(radius // 2):
        pattern.append(RED)
    for _ in range(radius // 2):
        pattern.append(GREEN)

    current_q, current_r = -radius, 0

    vectors = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]

    for dq, dr in vectors:
        board[(current_q, current_r)] = EMPTY

        current_q += dq
        current_r += dr

        for i in range(radius - 1):
            color = pattern[i % len(pattern)]

            board[(current_q, current_r)] = color

            current_q += dq
            current_r += dr

    return board


def render_board(board, N):
    radius = N
    print(f"\nAtoll Board (N={N})\n")

    num_letters = 2 * N - 1
    
    letters = [chr(ord('A') + i) for i in range(num_letters)]

    for r in range(-radius, radius + 1):

        padding = "  " * abs(r)

        boban = f"{letters[num_letters] if (num_letters < 2 * N - 1 and num_letters >= 0) else ' '}"
        num_letters -= 1
        line_str = f"{boban} {padding}"

        q_min = max(-radius, -radius - r)
        q_max = min(radius, radius - r)

        for q in range(q_min, q_max + 1):
            val = board.get((q, r), EMPTY)
            line_str += val + "  "

        print(line_str)
    
    
    numbers = [str(i + 1) for i in range(2 * N - 1)]
    letters_str = "      \t" + "   " + "  ".join(numbers)
    print("\n" + letters_str + "\n")


def parse_coordinates(move_str, N):
    move_str = move_str.strip().upper()
    
    if len(move_str) < 2:
        return None

    letter = move_str[0]
    try:
        number = int(move_str[1:])
    except ValueError:
        return None

    col_idx = ord(letter) - ord('A')

    
    center_offset = N - 1
    
    q = col_idx - center_offset
    r = number - N 

    return (q, r)

def parse_move(move_str, N):
    move_str = move_str.strip().upper()
    if len(move_str) < 2:
        return None

    letter = move_str[0]
    try:
        number = int(move_str[1:])
    except ValueError:
        return None
    
    center_offset = N - 1
    
    q = number - N 

    col_index = ord(letter) - ord('A')
    r = center_offset - col_index

    return (q, r)


def play_move(board, move_str, N, player_color):
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
            return True #red
        elif choice =='2':
            return False #green
        else:
            print("Invald input,try again")
                    


if __name__ == "__main__":
    try:
        N = int(sys.argv[1]) if len(sys.argv) > 1 else int(input("Unesite dimenziju table: "))
    except:
        N = 5

    game_board = generate_atoll_board(N)

    vs_computer  = game_mode() 
    human_starts = first_player() if vs_computer else True 
    red_starts   = starting_color()

    

    current_color = RED if red_starts else GREEN
    
    print(f"\nIGRA POČINJE! Prvi igra: {current_color}")
    game_running = True

    while game_running:
        render_board(game_board, N)
        print(f"Na potezu je: {current_color}")

        current_color = RED if red_starts else GREEN

        print(f"Its turn: {'RED' if red_starts else 'GREEN'}")

        move = input("\nEnter move (e.g. E5) or 'exit': ")
        if move.lower() == 'exit':
           break
        
        if play_move(game_board, move, N, current_color):
            red_starts = not red_starts

        if check_victory(game_board, current_color, N):
            render_board(game_board, N)
            print(f"\n========================================")
            print(f" KRAJ IGRE! POBEDNIK JE {current_color}")
            print(f"========================================")
            game_running = False
            break
        
        if not get_all_valid_moves(game_board):
            render_board(game_board, N)
            print("\nNERESENO! Nema više slobodnih polja.")
            game_running = False
            break
        
           
