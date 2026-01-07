import random
import time
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Bots.ChessBotList import register_chess_bot


# Our bot with Iterative Deepening
def chess_bot(player_sequence, board, time_budget, **kwargs):
    random.seed(time.time())
    start = time.perf_counter()

    color = player_sequence[1]
    print(f"\n---------- vX Playing: {'white' if color == 'w' else 'black'} ----------")
    currentScore = checkMaterial(board)
    printCurrentScore(currentScore)

    # Iterative Deepening: keep searching deeper until time runs out
    time_limit = start + (time_budget * 0.9)  # Use 90% of time budget as safety margin
    bestMove = None
    bestScore = -float('inf')
    depth = 1

    while time.perf_counter() < time_limit:
        try:
            print(f"Searching depth {depth}...")
            score, move = minimax(board, depth=depth, maximizing_player=True,
                                  color=color, time_limit=time_limit)

            if move is not None:
                bestMove = move
                bestScore = score
                print(f"Depth {depth} complete: score={score}")

            # If we found a winning move, stop searching
            if score >= 999999:
                print(f"Winning move found at depth {depth}!")
                break

            depth += 1

            # Don't start a new depth if we have less than 10% time remaining
            if time.perf_counter() > start + (time_budget * 0.8):
                print(f"Time running low, stopping at depth {depth - 1}")
                break

        except TimeoutError:
            print(f"Timeout during depth {depth}, using previous best move")
            break

    print(f"FINAL RESULT: depth={depth - 1}, score={bestScore}, move={bestMove}")

    if bestMove is None:
        # Fallback: find any legal move
        allMoves = checkAllMoves(board, color)
        if allMoves:
            bestMove = allMoves[0]
            print("WARNING: Using fallback move!")
        else:
            bestMove = ((0, 0), (0, 0), 0)

    print()
    printBoard(board)
    print()
    if bestMove and bestMove != ((0, 0), (0, 0), 0):
        print(f"Returned move: {pieceToString(board[bestMove[0][0]][bestMove[0][1]][0])} moves {bestMove}")

    # Compute and display execution time
    end = time.perf_counter()
    execution_time = round(end - start, 5)
    print(f"Execution time: {execution_time}s / {time_budget}s budget")
    print("---------- vX ----------")

    return bestMove[0], bestMove[1]


# Register the function
register_chess_bot("Bot2", chess_bot)

# --------------------------------------------------------------------------------------------------------------------------------------------

# CONST
boardLength = 8
endBoard = boardLength - 1


def checkMoves(pos, board, color):
    possibleMoves = []
    p = board[pos[0]][pos[1]][0]
    c = board[pos[0]][pos[1]][-1]
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

    for x in range(len(board)):
        for y in range(len(board[1])):
            if board[x][y] != "":
                if board[x][y][-1] != color:
                    continue
                else:
                    pos = (x, y)
                    piecePossibleMoves = checkMoves(pos, board, color)
                    allPossibleMoves.extend(piecePossibleMoves)
    return allPossibleMoves


def minimax(board, depth, maximizing_player, color, alpha=-float('inf'), beta=float('inf'), time_limit=None):
    # Check time limit
    if time_limit and time.perf_counter() >= time_limit:
        raise TimeoutError("Time limit exceeded")

    if depth == 0:
        return evaluateBoard(board, color), None

    allMoves = checkAllMoves(board, color)

    # No moves available
    if not allMoves:
        return evaluateBoard(board, color), None

    if maximizing_player:
        # MY turn - MAX score
        maxScore = -float('inf')
        bestMove = None

        for move in allMoves:
            from_pos, to_pos, move_value = move

            # CHECK KING CAPTURE BEFORE MAKING THE MOVE
            target_piece = board[to_pos[0]][to_pos[1]]
            if target_piece != '' and target_piece[0] == 'k' and target_piece[-1] != color:
                return 999999, move  # Return immediately!

            newBoardState = newBoard(board, move)
            score, child_move = minimax(newBoardState, depth - 1, False, color, alpha, beta, time_limit)

            if score >= 999999:
                return score, move

            if score > maxScore:
                maxScore = score
                bestMove = move
            elif score == maxScore and score != 999999:
                if random.random() > 0.5:
                    bestMove = move

            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return maxScore, bestMove
    else:
        # OPPONENT turn - MIN score
        minScore = float('inf')
        bestMove = None

        opponentAllMoves = checkAllMoves(board, toggleColor(color))

        for move in opponentAllMoves:
            newBoardState = newBoard(board, move)
            score, child_move = minimax(newBoardState, depth - 1, True, color, alpha, beta, time_limit)

            if score <= -999999:
                return score, move

            if score < minScore:
                minScore = score
                bestMove = move
            elif score == minScore:
                if random.random() > 0.5:
                    bestMove = move

            beta = min(beta, score)
            if beta <= alpha:
                break
        return minScore, bestMove


def evaluateBoard(board, myColor):
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
            positionValue = evaluatePosition((x, y), piece)

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


def newBoard(board, move):
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


def evaluatePosition(pos, piece):
    x, y = pos
    p = piece[0]
    score = 0
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
            return "Rook"
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


def checkMaterial(board):
    currentScore = [0, 0]
    for x in range(len(board)):
        for y in range(len(board[1])):
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
            if board[x][y] == '':
                piece += " .  "
            else:
                piece += f"{board[x][y]}  "
        print(f"{piece}\n")
        piece = ""
    print("\n")


def checkDiagonal(pos, board, color):
    x = pos[0]
    y = pos[1]
    possibleMoves = []

    rightBottom = min(x, y)
    rightUp = min(endBoard - x, y)
    leftBottom = min(x, endBoard - y)
    leftUp = min(endBoard - x, endBoard - y)

    def goDiagonal(horiz, vert, max_steps):
        for i in range(1, max_steps + 1):
            nextPos = (x + i * vert, y + i * horiz)
            if board[nextPos[0]][nextPos[1]] == '':
                possibleMoves.append((pos, nextPos, 0))
            elif board[nextPos[0]][nextPos[1]][-1] != color:
                captureValue = checkValue(board[nextPos[0]][nextPos[1]][0])
                possibleMoves.append((pos, nextPos, captureValue))
                break
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
            if board[nextPos[0]][nextPos[1]] == '':
                possibleMoves.append((pos, nextPos, 0))
            elif board[nextPos[0]][nextPos[1]][-1] != color:
                nextP = board[nextPos[0]][nextPos[1]][0]
                possibleMoves.append((pos, nextPos, checkValue(nextP)))
                break
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

    possibleMoves.extend(goLine(1, 0, endY - y, pos, board, color))
    possibleMoves.extend(goLine(-1, 0, y, pos, board, color))
    possibleMoves.extend(goLine(0, 1, endX - x, pos, board, color))
    possibleMoves.extend(goLine(0, -1, x, pos, board, color))

    return possibleMoves


def checkL(pos, board, color):
    x = pos[0]
    y = pos[1]
    possibleMoves = []

    def goL(nextX, nextY):
        if isNextPosOnBoard(nextX, nextY):
            if board[nextX][nextY] == '':
                possibleMoves.append((pos, (nextX, nextY), 0))
            elif board[nextX][nextY][-1] != color:
                captureValue = checkValue(board[nextX][nextY][0])
                possibleMoves.append((pos, (nextX, nextY), captureValue))

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
        possibleMoves.extend(goLine(1, 0, 1, pos, board, color))
        possibleMoves.extend(goLine(-1, 0, 1, pos, board, color))
        possibleMoves.extend(goLine(0, 1, 1, pos, board, color))
        possibleMoves.extend(goLine(0, -1, 1, pos, board, color))
        possibleMoves.extend(goLine(-1, 1, 1, pos, board, color))
        possibleMoves.extend(goLine(1, -1, 1, pos, board, color))
        possibleMoves.extend(goLine(1, 1, 1, pos, board, color))
        possibleMoves.extend(goLine(-1, -1, 1, pos, board, color))
    return possibleMoves


def checkPawn(pos, board, color):
    x = pos[0]
    y = pos[1]
    possibleMoves = []
    promotionBonus = 8

    # move in front
    nextX, nextY = x + 1, y
    if isNextPosOnBoard(nextX, nextY):
        if board[nextX][nextY] == '':
            if nextX == endBoard:
                possibleMoves.append((pos, (nextX, nextY), promotionBonus))
            else:
                possibleMoves.append((pos, (nextX, nextY), 0))

    # eat right
    rightX, rightY = x + 1, y - 1
    if isNextPosOnBoard(rightX, rightY):
        if board[rightX][rightY] != '' and board[rightX][rightY][-1] != color:
            captureValue = checkValue(board[rightX][rightY][0])
            promotionBonus = 8 if rightX == endBoard else 0
            possibleMoves.append((pos, (rightX, rightY), captureValue + promotionBonus))

    # eat left
    leftX, leftY = x + 1, y + 1
    if isNextPosOnBoard(leftX, leftY):
        if board[leftX][leftY] != '' and board[leftX][leftY][-1] != color:
            captureValue = checkValue(board[leftX][leftY][0])
            promotionBonus = 8 if leftX == endBoard else 0
            possibleMoves.append((pos, (leftX, leftY), captureValue + promotionBonus))

    return possibleMoves


def isNextPosOnBoard(nextX, nextY):
    if nextX < 0 or nextY < 0 or nextX > endBoard or nextY > endBoard:
        return False
    return True