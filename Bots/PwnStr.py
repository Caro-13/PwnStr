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

def checkMoves3(pos, board, color):
    possibleMoves = []
    p = board[pos[0]][pos[1]][0]
    c = board[pos[0]][pos[1]][-1]
    # p = board[pos[0], pos[1]][0]
    # c = board[pos[0], pos[1]][-1]
    match p:
        case "p":
            possibleMoves.extend(checkPawn3(pos, board, color))
        case "n":
            possibleMoves.extend(checkL3(pos, board, color))
        case "b":
            possibleMoves.extend(checkDiagonal3(pos, board, color))
        case "r":
            possibleMoves.extend(checkHorizVerti3(pos, board, color))
        case "q":
            possibleMoves.extend(checkHorizVerti3(pos, board, color))
            possibleMoves.extend(checkDiagonal3(pos, board, color))
        case "k":
            possibleMoves.extend(checkCarre3(pos, board, color))
        case _:
            return [((0, 0), (0, 0), 0)]
    return possibleMoves

def checkAllMoves(board, color):
    allPossibleMoves = []

    for x in range(len(board)):
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

def checkAllMoves3(board, color):
    allPossibleMoves = []

    for x in range(len(board)):
        for y in range(len(board[1])):
            # for x in range(board.shape[0] - 1):
            #     for y in range(board.shape[1]):
            if board[x][y] != "":
                if board[x][y][-1] != color:
                    continue
                else:
                    pos = (x, y)
                    piecePossibleMoves = checkMoves3(pos, board, color)
                    # print(board[x][y][0] + board[x][y][1], (x, y), piecePossibleMoves)
                    allPossibleMoves.extend(piecePossibleMoves)
        # print("\n")
    return allPossibleMoves

def minimax(board, depth, maximizing_player, color, return_move=False, alpha=-float('inf'), beta=float('inf')):
    if depth == 0:
        return evaluateBoard(board, color), None

    allMoves = checkAllMoves(board, color)

    # No moves available
    if not allMoves:
        return evaluateBoard(board, color)

    if maximizing_player:
        # MY turn - MAX score
        maxScore = -float('inf')
        bestMove = None
        for move in allMoves:
            newBoardState = newBoard(board, move)
            score, _ = minimax(newBoardState, depth - 1, False, color, False, alpha, beta)

            totalScore = move[2] + score

            if totalScore > maxScore:
                maxScore = totalScore
                bestMove = move

            alpha = max(alpha, totalScore)
            if beta <= alpha:
                break
        return maxScore, bestMove
    else:
        # OPPONENT turn - MIN score
        minScore = float('inf')
        bestMove = None

        for move in allMoves:
            newBoardState = newBoard(board, move)
            score, _ = minimax(newBoardState, depth - 1, True, toggleColor(color), False, alpha, beta)

            totalScore = move[2] + score

            if totalScore < minScore:
                minScore = totalScore
                bestMove = move

            beta = min(beta, totalScore)
            if beta <= alpha:
                break
        return minScore, bestMove


def evaluateBoard(board, myColor):
    # return positif if my color, negatif if opponent color
    myScore = 0
    opponentScore = 0
    myKingExists = False
    opponentKingExists = False

    for x in range(len(board)):
        for y in range(len(board[1])):
            if board[x][y] == '':
                continue

            piece = board[x][y]
            materialValue = checkValue(piece[0])
            positionValue = evaluatePosition((x, y), piece, board)

            if piece[-1] == myColor:
                myScore += materialValue + positionValue
                if piece[0] == 'k':
                    myKingExists = True
            else:
                opponentScore += materialValue + positionValue
                if piece[0] == 'k':
                    opponentKingExists = True

    # Check for game-ending conditions
    if not opponentKingExists:
        return 100000  # I win! Opponent's king is captured
    if not myKingExists:
        return -100000  # I lose! My king is captured

    return myScore - opponentScore

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
    return defaultMove(bestMove, possibleMoves)

def checkNextMoves3(inputBoard, possibleMoves, color):
    bestMove = defaultMove3(findBestMove(possibleMoves), possibleMoves)
    print(f"Lvl 1 best move: {bestMove}")

    def checkMoreMoves(inputBoard, possibleMoves):
        for i, move in enumerate(possibleMoves):
            board = newBoard(inputBoard, move)

            allPossibleMoves = checkAllMoves3(board, toggleColor(color))
            if move[2] - findBestMove(allPossibleMoves)[2] < move[2]:
                possibleMoves[i] = (move[0], move[1], move[2] - findBestMove(allPossibleMoves)[2])

    checkMoreMoves(inputBoard, possibleMoves)

    displayMoves(inputBoard, possibleMoves)
    bestMove = findBestMove(possibleMoves)
    return defaultMove3(bestMove, possibleMoves)


def findBestMove(allPossibleMoves):
    return max(allPossibleMoves, key=lambda move: move[2], default=((0, 0), (0, 0), 0))

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

def defaultMove3(bestMove, allPossibleMoves):
    if not allPossibleMoves:
        return ((0, 0), (0, 0), 0)
    best_value = bestMove[2]
    best_moves = [move for move in allPossibleMoves if move[2] == best_value]
    return random.choice(best_moves)


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


def evaluatePosition(pos, piece, board):
    x, y = pos
    p = piece[0]  # piece type
    score = 0

    # Center control bonus
    center_distance = abs(x - endBoard/2) + abs(y - endBoard/2)
    score += (endBoard - center_distance) * 0.1  # Small bonus for center control

    # Pawn forward bonus --> closer to promot
    if p == "p":
        score += x * 0.2

    # knight + bishops forward (better than pawn)
    if p in ["n", "b"] and x > 0:
        score += 0.3

    return score

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
                piece += " .  "
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
                forwardBonus = evaluatePosition(nextPos, board[pos[0]][pos[1]], board)
                possibleMoves.append((pos, nextPos, 0 + forwardBonus))
            # opponent piece
            elif board[nextPos[0]][nextPos[1]][-1] != color:
                captureValue = checkValue(board[nextPos[0]][nextPos[1]][0])
                forwardBonus = evaluatePosition(nextPos, board[pos[0]][pos[1]], board)
                possibleMoves.append((pos, nextPos, captureValue + forwardBonus))
                break
            # my piece
            elif board[nextPos[0]][nextPos[1]][-1] == color:
                break

    goDiagonal(-1, 1, rightUp)
    goDiagonal(-1, -1, rightBottom)
    goDiagonal(1, 1, leftUp)
    goDiagonal(1, -1, leftBottom)

    return possibleMoves

def checkDiagonal3(pos, board, color):
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
                captureValue = checkValue(board[nextPos[0]][nextPos[1]][0])
                possibleMoves.append((pos, nextPos, captureValue))
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
    endX = len(board) - 1
    endY = len(board[1]) - 1

    for i in range(1, max_steps + 1):
        nextPos = (x + i * vert, y + i * horiz)
        if nextPos[0] < 0 or nextPos[1] < 0 or nextPos[0] > endX or nextPos[1] > endY:
            continue
        else:
            # empty case
            if board[nextPos[0]][nextPos[1]] == '':
                forwardBonus = evaluatePosition(nextPos, board[pos[0]][pos[1]], board)
                possibleMoves.append((pos, nextPos, 0 + forwardBonus))
            # opponent piece
            elif board[nextPos[0]][nextPos[1]][-1] != color:
                nextP = board[nextPos[0]][nextPos[1]][0]
                forwardBonus = evaluatePosition(nextPos, board[pos[0]][pos[1]], board)
                possibleMoves.append((pos, nextPos, checkValue(nextP)+forwardBonus))
                break
            # my piece
            elif board[nextPos[0]][nextPos[1]][-1] == color:
                break
            else:
                break
    return possibleMoves

def goLine3(horiz, vert, max_steps, pos, board, color):
    x = pos[0]
    y = pos[1]
    possibleMoves = []
    endX = len(board) - 1
    endY = len(board[1]) - 1

    for i in range(1, max_steps + 1):
        nextPos = (x + i * vert, y + i * horiz)
        if nextPos[0] < 0 or nextPos[1] < 0 or nextPos[0] > endX or nextPos[1] > endY:
            continue
        else:
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
            else:
                break
    return possibleMoves

def checkHorizVerti(pos, board, color):
    x = pos[0]
    y = pos[1]
    possibleMoves = []
    endX = len(board) - 1
    endY = len(board[1]) - 1

    possibleMoves.extend(goLine(1, 0, endY - y, pos, board, color))  # Check the line incrementing y
    possibleMoves.extend(goLine(-1, 0, y, pos, board, color))  # Check the line decrementing y
    possibleMoves.extend(goLine(0, 1, endX - x, pos, board, color))  # Check the line incrementing x
    possibleMoves.extend(goLine(0, -1, x, pos, board, color))  # Check the line decrementing x

    return possibleMoves

def checkHorizVerti3(pos, board, color):
    x = pos[0]
    y = pos[1]
    possibleMoves = []
    endX = len(board) - 1
    endY = len(board[1]) - 1

    possibleMoves.extend(goLine3(1, 0, endY - y, pos, board, color))  # Check the line incrementing y
    possibleMoves.extend(goLine3(-1, 0, y, pos, board, color))  # Check the line decrementing y
    possibleMoves.extend(goLine3(0, 1, endX - x, pos, board, color))  # Check the line incrementing x
    possibleMoves.extend(goLine3(0, -1, x, pos, board, color))  # Check the line decrementing x

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
                forwardBonus = evaluatePosition((nextX, nextY), board[pos[0]][pos[1]], board)
                possibleMoves.append((pos, (nextX, nextY), 0 + forwardBonus))
            # opponent piece
            elif board[nextX][nextY][-1] != color:
                captureValue =checkValue(board[nextX][nextY][0])
                forwardBonus = evaluatePosition((nextX, nextY), board[pos[0]][pos[1]], board)
                possibleMoves.append((pos, (nextX, nextY), captureValue + forwardBonus))

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

def checkL3(pos, board, color):
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
                captureValue =checkValue(board[nextX][nextY][0])
                possibleMoves.append((pos, (nextX, nextY), captureValue))

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

def checkCarre3(pos, board, color):
    possibleMoves = []
    if board[pos[0]][pos[1]] != "":
        possibleMoves.extend(goLine3(1, 0, 1, pos, board, color))  # Check the line incrementing y
        possibleMoves.extend(goLine3(-1, 0, 1, pos, board, color))  # Check the line decrementing y
        possibleMoves.extend(goLine3(0, 1, 1, pos, board, color))  # Check the line incrementing x
        possibleMoves.extend(goLine3(0, -1, 1, pos, board, color))  # Check the line decrementing x

        possibleMoves.extend(goLine3(-1, 1, 1, pos, board, color))  # Check the line incrementing x and y
        possibleMoves.extend(goLine3(1, -1, 1, pos, board, color))  # Check the line incrementing x and decrementing y
        possibleMoves.extend(goLine3(1, 1, 1, pos, board, color))  # Check the line incrementing y and decrementing x
        possibleMoves.extend(goLine3(-1, -1, 1, pos, board, color))  # Check the line decrementing x and y
    return possibleMoves

def checkPawn(pos, board, color):
    x = pos[0]
    y = pos[1]
    p = board[x][y][0]
    possibleMoves = []
    promotionBonus = 8 # - pawn + qween (9-1)

    # move in front
    nextX, nextY = x + 1, y
    if isNextPosOnBoard(nextX, nextY):
        # empty case
        if board[nextX][nextY] == '':
            if nextX == endBoard :
                forwardBonus = evaluatePosition((nextX, nextY), board[pos[0]][pos[1]], board)
                possibleMoves.append((pos, (nextX, nextY), promotionBonus+forwardBonus))
            else :
                forwardBonus = evaluatePosition((nextX, nextY), board[pos[0]][pos[1]], board)
                possibleMoves.append((pos, (nextX, nextY), 0 + forwardBonus))
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
            captureValue = checkValue(board[rightX][rightY][0])
            promotionBonus = 8 if rightX == endBoard else 0  # Add promotion bonus if reaching end
            forwardBonus = evaluatePosition((rightX,rightY),board[pos[0]][pos[1]], board)
            possibleMoves.append((pos, (rightX, rightY), captureValue + promotionBonus+ forwardBonus))
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
            captureValue = checkValue(board[leftX][leftY][0])
            promotionBonus = 8 if leftX == endBoard else 0  # Add promotion bonus if reaching end
            forwardBonus = evaluatePosition((leftX, leftY), board[pos[0]][pos[1]], board)
            possibleMoves.append((pos, (leftX, leftY), captureValue + promotionBonus+forwardBonus))
        # my piece
        elif board[leftX][leftY][-1] == color:
            pass

    return possibleMoves

def checkPawn3(pos, board, color):
    x = pos[0]
    y = pos[1]
    p = board[x][y][0]
    possibleMoves = []

    # move in front
    nextX, nextY = x + 1, y
    if isNextPosOnBoard(nextX, nextY):
        # empty case
        if board[nextX][nextY] == '':
            if nextX == endBoard :
                possibleMoves.append((pos, (nextX, nextY), 0))
            else :
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
            captureValue = checkValue(board[rightX][rightY][0])
            possibleMoves.append((pos, (rightX, rightY), captureValue))
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
            captureValue = checkValue(board[leftX][leftY][0])
            possibleMoves.append((pos, (leftX, leftY), captureValue))
        # my piece
        elif board[leftX][leftY][-1] == color:
            pass

    return possibleMoves

def isNextPosOnBoard(nextX, nextY):
    if nextX < 0 or nextY < 0 or nextX > endBoard or nextY > endBoard:
        return False
    return True
