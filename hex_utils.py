def get_neighbors(hex_pos):
    q, r = hex_pos
    vectors = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]
    return [(q + dq, r + dr) for dq, dr in vectors]
