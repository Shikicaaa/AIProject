import sys

RED   = '\U0001F534' # 🔴
GREEN = '\U0001F7E2' # 🟢
WHITE = '\u26AA'     # ⚪
EMPTY = '  '         # dva razmaka


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


if __name__ == "__main__":
    try:
        N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    except:
        N = 5

    game_board = generate_atoll_board(N)

    to_play = True

    
    while True:
        render_board(game_board, N)
        move = input("\nEnter move (e.g. E5, F1) or 'exit': ")
        
        if move.lower() == 'exit':
            break
            
        play_move(game_board, move, N, RED if to_play else GREEN)
        to_play = not to_play