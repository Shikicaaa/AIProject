from constants import RED, GREEN, WHITE, EMPTY


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
