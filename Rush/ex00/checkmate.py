def checkmate(board_str):
    board = [list(row) for row in board_str.split('\n')]

    king_pos = None
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'K':
                king_pos = (i, j)
                break
        if king_pos:
            break

    if not king_pos:
        print("Error: No King found on the board")
        return

    directions = {
        'R': [(0, 1), (0, -1), (1, 0), (-1, 0)],  
        'B': [(1, 1), (1, -1), (-1, 1), (-1, -1)],  
        'Q': [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)],  
        'P': [(-1, -1), (-1, 1)],
        'N': [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)],
        'K': [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    }

    for piece, dirs in directions.items():
        for d in dirs:
            x, y = king_pos
            while True:
                x += d[0]
                y += d[1]
                if x < 0 or x >= len(board) or y < 0 or y >= len(board):
                    break
                if board[x][y] == piece:
                    print("Success")
                    return
                if board[x][y] != '.':
                    break

    print("Fail")