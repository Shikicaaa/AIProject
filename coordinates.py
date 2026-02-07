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
