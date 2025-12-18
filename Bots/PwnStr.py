# CONST
boardLength = 8


def checkMoves(pos, board, color):
    possibleMoves = []
    p = board[pos][0]
    c = board[pos][1]
    for x in range(board.shape[0] - 1):
        for y in range(board.shape[1]):
            if c == color:
                match p:
                    case "p":
                        possibleMoves.extend(checkPawn(pos, board, color))
                    case "n":
                        possibleMoves.extend(checkL(pos, board, color))
                    case "b":
                        possibleMoves.extend(checkDiagonal(pos, board, color))
                    case "r":
                        possibleMoves.extend(checkHorizVerti(pos, board, color))
                    case "q":
                        possibleMoves.extend(checkHorizVerti(pos, board, color))
                        possibleMoves.extend(checkDiagonal(pos, board, color))
                    case "k":
                        possibleMoves.extend(checkCarre(pos, board, color))
    return possibleMoves


def checkValue(p):
    match p:
        case "p":
            return 1
        case "n":
            return 3
        case "b":
            return 3
        case "r":
            return 5
        case "q":
            return 9
        case "k":
            return 90
        case _:
            return 0


def printBoard(board):
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


# Caro
def checkDiagonal(pos, board, color):
    x = pos[0]
    y = pos[1]
    p = board(pos)[0]
    possibleMoves = []

    rightBottom = y if y < x else x
    rightUp = y if y < boardLength - x else boardLength - x

    leftBottom = boardLength - y if boardLength - y < x else x
    leftUp = boardLength - y if boardLength - y < boardLength - x else boardLength - x

    def goDiagonal(horiz, vert, borne, step):
        for i in range(x, borne, step):
            nextPos = (x + i * vert, y + i * horiz)
            if board[nextPos] == "":
                possibleMoves.append((pos, nextPos, checkValue(p)))

            if board[nextPos][-1] != color:
                possibleMoves.append((pos, nextPos, checkValue(p)))
                break

            if board[nextPos][-1] == color:
                break

    goDiagonal(-1, 1, rightUp, 1)
    goDiagonal(-1, -1, rightBottom, -1)
    goDiagonal(1, 1, leftUp, 1)
    goDiagonal(1, -1, leftBottom, -1)

    print(possibleMoves)
    return possibleMoves


def goLine(horiz, vert, borne, step, pos, board, color, x=0, y=0):
    p = board(pos)[0]
    possibleMoves = []

    a = x if x else y if y else 0
    for i in range(a, borne, step):
        nextPos = (x + (i * vert), y + (i * horiz))
        if board[nextPos] == "":
            possibleMoves.append((pos, nextPos, checkValue(p)))

        if board[nextPos][-1] != color:
            possibleMoves.append((pos, nextPos, checkValue(p)))
            break

        if board[nextPos][-1] == color:
            break
    return possibleMoves


# Raphael
def checkHorizVerti(pos, board, color):
    x = pos[0]
    y = pos[1]
    p = board(pos)[0]
    possibleMoves = []
    endX = board.shape[0]
    endY = board.shape[1]

    possibleMoves.extend(goLine(1, 0, endY, 1, pos, board, color, 0, y))    # Check the line incrementing y
    possibleMoves.extend(goLine(-1, 0, 0, -1, pos, board, color, 0, y))          # Check the line decrementing y
    possibleMoves.extend(goLine(0, 1, endX, 1, pos, board, color, x, 0))    # Check the line incrementing x
    possibleMoves.extend(goLine(0, -1, 0, -1, pos, board, color, x, 0))         # Check the line decrementing x

    return possibleMoves


# Caro
def checkL(pos, board, color):
    possibleMoves = []
    return possibleMoves


# Raphael
def checkCarre(pos, board, color):
    possibleMoves = []
    return possibleMoves


# Caro
def checkPawn(pos, board, color):
    possibleMoves = []
    return possibleMoves
