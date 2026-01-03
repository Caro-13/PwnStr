import random

# CONST
boardLength = 8
endBoard = boardLength - 1


def checkMoves(pos, board, color):
    possibleMoves = []
    p = board[pos[0]][pos[1]][0]
    c = board[pos[0]][pos[1]][-1]
    # p = board[pos[0], pos[1]][0]
    # c = board[pos[0], pos[1]][-1]
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
        case _:
            return [((0, 0), (0, 0), 0)]
    return possibleMoves


def checkAllMoves(board, color):
    allPossibleMoves = []

    for x in range(len(board) - 1):
        for y in range(len(board[1])):
            # for x in range(board.shape[0] - 1):
            #     for y in range(board.shape[1]):
            if board[x][y] != "":
                if board[x][y][-1] != color:
                    continue
                else:
                    pos = (x, y)
                    piecePossibleMoves = checkMoves(pos, board, color)
                    # print(board[x][y][0] + board[x][y][1], (x, y), piecePossibleMoves)
                    allPossibleMoves.extend(piecePossibleMoves)
        # print("\n")
    return allPossibleMoves


def checkNextMoves(inputBoard, possibleMoves, color):
    bestMove = defaultMove(findBestMove(possibleMoves), possibleMoves)
    print(f"Lvl 1 best move: {bestMove}")

    # for move in possibleMoves:
    for i, move in enumerate(possibleMoves):
        board = newBoard(inputBoard, move)

        allPossibleMoves = checkAllMoves(board, toggleColor(color))
        if move[2] - findBestMove(allPossibleMoves)[2] < move[2]:
            possibleMoves[i] = (move[0], move[1], move[2] - findBestMove(allPossibleMoves)[2])
        # else:

    displayMoves(inputBoard, possibleMoves)
    bestMove = findBestMove(possibleMoves)
        # if findBestMove(checkAllMoves(board, toggleColor(color)))[2] > bestMove[2]:
        #     bestMove = move
        #     print(f"Next move: {bestMove}\n")
    return defaultMove(bestMove, possibleMoves)


def findBestMove(allPossibleMoves):
    # bestMove = ((0, 0), (0, 0), 0)
    #
    # for i in range(len(allPossibleMoves)):
    #     if allPossibleMoves[i][2] > bestMove[2]:
    #         bestMove = allPossibleMoves[i]

    bestMove = max(allPossibleMoves, key=lambda move: move[2], default=((0, 0), (0, 0), 0))

    return bestMove


def defaultMove(bestMove, allPossibleMoves):
    if len(allPossibleMoves) > 0:
        if bestMove == ((0, 0), (0, 0), 0) or bestMove[2] == 0:
            bestMove = allPossibleMoves[random.randint(0, len(allPossibleMoves) - 1)]
            while bestMove[2] < 0:
                bestMove = allPossibleMoves[random.randint(0, len(allPossibleMoves) - 1)]
            print(f"Random move {bestMove}")
        else:
            print(f"Best move: {bestMove}")
    else:
        bestMove = ((0, 0), (0, 0), 0)
    return bestMove


def newBoard(board, move):
    # move = [(1, 2), (2, 2)] = [(from), (to)]
    outBoard = [row.copy() for row in board]
    outBoard[move[1][0]][move[1][1]] = outBoard[move[0][0]][move[0][1]]
    outBoard[move[0][0]][move[0][1]] = ""
    return outBoard


def toggleColor(color):
    if color == "w":
        return "b"
    elif color == "b":
        return "w"


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


def pieceToString(p):
    match p:
        case "p":
            return "Pawn"
        case "n":
            return "Knight"
        case "b":
            return "Bishop"
        case "r":
            return "Rookie"
        case "q":
            return "Queen"
        case "k":
            return "King"
        case _:
            return "No name"


def colorToString(c):
    match c:
        case "w":
            return "White"
        case "b":
            return "Black"
        case _:
            return "No color"

def displayMoves(board, moves):
    print()
    for move in moves:
        p = board[move[0][0]][move[0][1]]
        print(f"{colorToString(p[1])} {pieceToString(p[0])} moves from ({move[0][0]}, {move[0][1]}) to ({move[1][0]}, {move[1][1]}) | value = {move[2]}")
    print()


def checkMaterial(board):
    # CurrentScore(0) = white score, currentScore(1) = black score
    currentScore = [0, 0]
    for x in range(len(board)):
        for y in range(len(board[1])):
            # for x in range(board.shape[0]):
            #     for y in range(board.shape[1]):
            if board[x][y] != '':
                p = checkValue(board[x][y][0])
                if board[x][y][-1] == 'w':
                    currentScore[0] += p
                elif board[x][y][-1] == 'b':
                    currentScore[1] += p

    return currentScore


def printCurrentScore(currentScore):
    print(f"Current score: white: {currentScore[0]}  |  black: {currentScore[1]}")


def printBoard(board):
    piece = ""
    print("\n")
    for x in range(len(board)):
        for y in range(len(board[1])):
            # for x in range(board.shape[0]):
            #     for y in range(board.shape[1]):
            if board[x][y] == '':
                piece += "' ' "
            else:
                piece += f"{board[x][y]}  "
                # piece += f"{board[x][y].string()}  "
        print(f"{piece}\n")
        piece = ""
    print("\n")


def checkDiagonal(pos, board, color):
    x = pos[0]
    y = pos[1]
    p = board[x][y][0]
    possibleMoves = []

    rightBottom = min(x, y)
    rightUp = min(endBoard - x, y)

    leftBottom = min(x, endBoard - y)
    leftUp = min(endBoard - x, endBoard - y)

    def goDiagonal(horiz, vert, max_steps):
        for i in range(1, max_steps + 1):
            nextPos = (x + i * vert, y + i * horiz)
            # empty case
            if board[nextPos[0]][nextPos[1]] == '':
                possibleMoves.append((pos, nextPos, 0))
            # opponent piece
            elif board[nextPos[0]][nextPos[1]][-1] != color:
                # possibleMoves.append((pos, nextPos, checkValue(p[0])))
                possibleMoves.append((pos, nextPos, checkValue(board[nextPos[0]][nextPos[1]][0])))
                break
            # my piece
            elif board[nextPos[0]][nextPos[1]][-1] == color:
                break

    goDiagonal(-1, 1, rightUp)
    goDiagonal(-1, -1, rightBottom)
    goDiagonal(1, 1, leftUp)
    goDiagonal(1, -1, leftBottom)

    return possibleMoves


def goLine(horiz, vert, max_steps, pos, board, color):
    x = pos[0]
    y = pos[1]
    possibleMoves = []

    for i in range(1, max_steps):
        nextPos = (x + i * vert, y + i * horiz)
        # empty case
        if board[nextPos[0]][nextPos[1]] == '':
            possibleMoves.append((pos, nextPos, 0))
        # opponent piece
        elif board[nextPos[0]][nextPos[1]][-1] != color:
            nextP = board[nextPos[0]][nextPos[1]][0]
            possibleMoves.append((pos, nextPos, checkValue(nextP)))
            break
        # my piece
        elif board[nextPos[0]][nextPos[1]][-1] == color:
            break
    return possibleMoves


def checkHorizVerti(pos, board, color):
    x = pos[0]
    y = pos[1]
    possibleMoves = []
    endX = len(board)
    endY = len(board[1])
    # endX = board.shape[0]
    # endY = board.shape[1]

    possibleMoves.extend(goLine(1, 0, endY - y, pos, board, color))  # Check the line incrementing y
    possibleMoves.extend(goLine(-1, 0, y, pos, board, color))  # Check the line decrementing y
    possibleMoves.extend(goLine(0, 1, endX - x, pos, board, color))  # Check the line incrementing x
    possibleMoves.extend(goLine(0, -1, x, pos, board, color))  # Check the line decrementing x

    return possibleMoves


def checkL(pos, board, color):
    x = pos[0]
    y = pos[1]
    p = board[x][y][0]
    possibleMoves = []

    def goL(nextX, nextY):
        if (isNextPosOnBoard(nextX, nextY)):
            # empty case
            if board[nextX][nextY] == '':
                possibleMoves.append((pos, (nextX, nextY), 0))
            # opponent piece
            elif board[nextX][nextY][-1] != color:
                possibleMoves.append((pos, (nextX, nextY), checkValue(board[nextX][nextY][0])))

            # my piece
            elif board[nextX][nextY][-1] == color:
                pass

    goL(x + 2, y + 1)
    goL(x + 2, y - 1)
    goL(x - 2, y + 1)
    goL(x - 2, y - 1)
    goL(x + 1, y + 2)
    goL(x - 1, y + 2)
    goL(x + 1, y - 2)
    goL(x - 1, y - 2)

    return possibleMoves


def checkCarre(pos, board, color):
    x = pos[0]
    y = pos[1]
    possibleMoves = []
    if board[pos[0]][pos[1]] != "":
        possibleMoves.extend(goLine(1, 0, 1, pos, board, color))  # Check the line incrementing y
        possibleMoves.extend(goLine(-1, 0, 1, pos, board, color))  # Check the line decrementing y
        possibleMoves.extend(goLine(0, 1, 1, pos, board, color))  # Check the line incrementing x
        possibleMoves.extend(goLine(0, -1, 1, pos, board, color))  # Check the line decrementing x

        possibleMoves.extend(goLine(-1, 1, 1, pos, board, color))  # Check the line incrementing x and y
        possibleMoves.extend(goLine(1, -1, 1, pos, board, color))  # Check the line incrementing x and decrementing y
        possibleMoves.extend(goLine(1, 1, 1, pos, board, color))  # Check the line incrementing y and decrementing x
        possibleMoves.extend(goLine(-1, -1, 1, pos, board, color))  # Check the line decrementing x and y

    return possibleMoves


def checkPawn(pos, board, color):
    x = pos[0]
    y = pos[1]
    p = board[x][y][0]
    possibleMoves = []

    # move in front
    nextX, nextY = x + 1, y
    if isNextPosOnBoard(nextX, nextY):
        # empty case
        if board[nextX][nextY] == '':
            possibleMoves.append((pos, (nextX, nextY), 0))
        # oponnent piece
        elif board[nextX][nextY][-1] != color:
            pass
        # my piece
        elif board[nextX][nextY][-1] == color:
            pass

    # eat right
    rightX, rightY = x + 1, y - 1
    if isNextPosOnBoard(rightX, rightY):
        # empty case
        if board[rightX][rightY] == '':
            pass
        # oponnent piece
        elif board[rightX][rightY][-1] != color:
            possibleMoves.append((pos, (rightX, rightY), checkValue(board[rightX][rightY][0])))
        # my piece
        elif board[rightX][rightY][-1] == color:
            pass

    # eat left
    leftX, leftY = x + 1, y + 1
    if isNextPosOnBoard(leftX, leftY):
        # empty case
        if board[leftX][leftY] == '':
            pass
        # oponnent piece
        elif board[leftX][leftY][-1] != color:
            possibleMoves.append((pos, (leftX, leftY), checkValue(board[leftX][leftY][0])))
        # my piece
        elif board[leftX][leftY][-1] == color:
            pass

    return possibleMoves


def isNextPosOnBoard(nextX, nextY):
    if nextX < 0 or nextY < 0 or nextX > endBoard or nextY > endBoard:
        return False
    return True
