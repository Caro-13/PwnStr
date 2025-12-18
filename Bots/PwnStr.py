# CONST
boardLength = 8
endBoard = boardLength-1


def checkMoves(pos, board, color):
    possibleMoves = []
    p = board[pos[0], pos[1]][0]
    c = board[pos[0],pos[1]][-1]
    match p:
        case "p":
            possibleMoves.extend(checkPawn(pos, board, color))
        case "n":
            possibleMoves.extend(checkL(pos, board, color))
        case "b":
            possibleMoves.extend(checkDiagonal(pos, board, color))
        #case "r":
        #    possibleMoves.extend(checkHorizVerti(pos, board, color))
        # case "q":
        #     possibleMoves.extend(checkHorizVerti(pos, board, color))
        #     possibleMoves.extend(checkDiagonal(pos, board, color))
        # case "k":
        #     possibleMoves.extend(checkCarre(pos, board, color))
        case _:
            return
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
    p = board[x][y][0]
    possibleMoves = []

    rightBottom = min(x,y)
    rightUp = min(endBoard-x,y)

    leftBottom = min (x, endBoard - y)
    leftUp = min(endBoard - x,endBoard - y)

    def goDiagonal(horiz, vert, max_steps):
        for i in range(1, max_steps + 1):
            nextPos = (x + i * vert, y + i * horiz)
            #empty case
            if board[nextPos[0], nextPos[1]] == '':
                possibleMoves.append((pos, nextPos, 0))
            #opponent piece
            elif board[nextPos[0], nextPos[1]][-1] != color:
                possibleMoves.append((pos, nextPos, checkValue(p[0])))
                break
            #my piece
            elif board[nextPos][-1] == color:
                break

    goDiagonal(-1, 1, rightUp)
    goDiagonal(-1, -1, rightBottom)
    goDiagonal(1, 1, leftUp)
    goDiagonal(1, -1, leftBottom)

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

    possibleMoves.append(goLine(1, 0, endY, 1, pos, board, color, 0, y))    # Check the line incrementing y
    possibleMoves.append(goLine(-1, 0, 0, -1, pos, board, color, 0, y))          # Check the line decrementing y
    possibleMoves.append(goLine(0, 1, endX, 1, pos, board, color, x, 0))    # Check the line incrementing x
    possibleMoves.append(goLine(0, -1, 0, -1, pos, board, color, x, 0))         # Check the line decrementing x

    return possibleMoves


# Caro
def checkL(pos, board, color):
    x = pos[0]
    y = pos[1]
    p = board[x][y][0]
    possibleMoves = []

    def goL(nextX,nextY):
        if (isNextPosOnBoard(nextX,nextY)):
            # empty case
            if board[nextX, nextY] == '':
                possibleMoves.append((pos, (nextX,nextY), 0))
            # opponent piece
            elif board[nextX,nextY][-1] != color:
                possibleMoves.append((pos, (nextX,nextY), checkValue(p[0])))

            # my piece
            elif board[nextX,][-1] == color:
                pass

    goL(x+2,y+1)
    goL(x+2,y-1)
    goL(x-2,y+1)
    goL(x-2,y-1)
    goL(x+1,y+2)
    goL(x-1,y+2)
    goL(x+1,y-2)
    goL(x-1,y-2)

    return possibleMoves

# Raphael
def checkCarre(pos, board, color):
    possibleMoves = []
    return possibleMoves

# Caro
def checkPawn(pos, board, color):
    x = pos[0]
    y = pos[1]
    p = board[x][y][0]
    possibleMoves = []

    nextX,nextY = x+1,y

    if isNextPosOnBoard(nextX, nextY):
        #empty case
        if board[nextX][nextY] == '':
            possibleMoves.append((pos, (nextX,nextY), 0))
        #opponent piece
        elif board[nextX][nextY][-1] != color:
            possibleMoves.append((pos, (nextX,nextY), checkValue(p[0])))
        # my piece
        elif board[nextX][nextY][-1] == color:
            pass

    return possibleMoves

def isNextPosOnBoard(nextX,nextY):
    if nextX < 0 or nextY < 0 or nextX > endBoard or nextY > endBoard:
        return False
    return True