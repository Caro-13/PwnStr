
def check_moves(pos, board, color):
    possibleMoves = []
    p = board[pos][0]
    match p:
        case "p":
            checkPawn(pos, board, color)
        case "n":
            checkL(pos, board, color)
        case "b":
            checkDiagonal(pos, board, color)
        case "r":
            checkHorizVerti(pos, board, color)
        case "q":
            checkHorizVerti(pos, board, color)
            checkDiagonal(pos, board, color)
        case "k":
            checkCarre(pos, board, color)
    return possibleMoves

def check_value(p):
    match p:
        case "p":
            v = 1
        case "n":
            v = 3
        case "b":
            v = 3
        case "r":
            v = 5
        case "q":
            v = 9
        case "k":
            v = 90
    return v

def print_board(board):
    piece = ""
    print("\n")
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            if board[x, y] == '':
                piece += "' ' "
            else:
                 piece += f"{board[x, y].string()}  "
        print(f"{piece}\n")
        piece = ""
    print("\n")
