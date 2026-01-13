import random
import time
from Bots.ChessBotList import register_chess_bot


# Our bot
def chess_bot(player_sequence, board, time_budget, **kwargs):
    start = time.perf_counter()

    color = player_sequence[1]
    print(f"\n---------- PwnStr v3.8 Playing: {'white' if color == 'w' else 'black'} ----------")

    # Compute all possible moves
    allPossibleMoves = checkAllMoves3(board, color)
    print(f"Possible moves: {len(allPossibleMoves)}")

    bestMove = checkNextMoves38(board, allPossibleMoves, color)
    print()
    printBoard(board)
    print()
    print(f"Returned move: {pieceToString(board[bestMove[0][0]][bestMove[0][1]][0])} moves {bestMove}")

    # Compute and display execution time
    end = time.perf_counter()
    execution_time = round(end - start, 5)
    print(f"Execution time: {execution_time}s")
    print("---------- PwnStr ----------")

    return bestMove[0], bestMove[1]


#   Example how to register the function
register_chess_bot("PwnStr", chess_bot)

#######################
#        Logic        #
#######################

# CONST
boardLength = 8
endBoard = boardLength - 1


def checkAllMoves3(board, color):
    allPossibleMoves = []

    for x in range(len(board)):
        for y in range(len(board[1])):
            if board[x][y] != "":
                if board[x][y][-1] != color:
                    continue
                else:
                    pos = (x, y)
                    piecePossibleMoves = checkMoves3(pos, board, color)
                    allPossibleMoves.extend(piecePossibleMoves)
    return allPossibleMoves


def checkMoves3(pos, board, color):
    possibleMoves = []
    p = board[pos[0]][pos[1]][0]
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


def checkNextMoves38(inputBoard, possibleMoves, color):
    for i, move in enumerate(possibleMoves):
        if inputBoard[move[1][0]][move[1][1]] != "":
            if inputBoard[move[1][0]][move[1][1]][0] == "k":
                displayMoves(inputBoard, possibleMoves)
                print("Take the King!!")
                return move
        else:
            board = newBoard(inputBoard, move)

            allPossibleMoves = checkAllMoves3(board, toggleColor(color))
            bestMoveVal = findBestMove38(allPossibleMoves)[2]
            # if move[2] - bestMoveVal < move[2]:
            possibleMoves[i] = (move[0], move[1], move[2] - bestMoveVal)

    displayMoves(inputBoard, possibleMoves)
    bestMove = findBestMove38(possibleMoves)
    return defaultMove38(bestMove, possibleMoves)


def findBestMove38(allPossibleMoves):
    for move in allPossibleMoves:
        if move[2] > 10:
            return move
    else:
        return max(allPossibleMoves, key=lambda move: move[2], default=((0, 0), (0, 0), 0))


def defaultMove38(bestMove, allPossibleMoves):
    if bestMove[2] > 10:
        return bestMove
    else:
        if not allPossibleMoves:
            return ((0, 0), (0, 0), 0)
        bestValue = bestMove[2]
        bestMoves = [move for move in allPossibleMoves if move[2] == bestValue]
        randIndex = random.randint(0, len(bestMoves) - 1)
        return bestMoves[randIndex]


#######################
#       Helpers       #
#######################

def newBoard(board, move):
    outBoard = [row.copy() for row in board]
    outBoard[move[1][0]][move[1][1]] = outBoard[move[0][0]][move[0][1]]
    outBoard[move[0][0]][move[0][1]] = ""
    return outBoard


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


def displayMoves(board, moves):
    print()
    for move in moves:
        p = board[move[0][0]][move[0][1]]
        print(
            f"{colorToString(p[1])} {pieceToString(p[0])} moves from ({move[0][0]}, {move[0][1]}) to ({move[1][0]}, {move[1][1]}) | value = {move[2]}")
    print()


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


def toggleColor(color):
    if color == "w":
        return "b"
    elif color == "b":
        return "w"


#######################
#     Pieces moves    #
#######################
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


def checkDiagonal3(pos, board, color):
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


def checkL3(pos, board, color):
    x = pos[0]
    y = pos[1]
    possibleMoves = []

    def goL(nextX, nextY):
        if (isNextPosOnBoard(nextX, nextY)):
            # empty case
            if board[nextX][nextY] == '':
                possibleMoves.append((pos, (nextX, nextY), 0))
            # opponent piece
            elif board[nextX][nextY][-1] != color:
                captureValue = checkValue(board[nextX][nextY][0])
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


def checkPawn3(pos, board, color):
    x = pos[0]
    y = pos[1]
    possibleMoves = []

    # move in front
    nextX, nextY = x + 1, y
    if isNextPosOnBoard(nextX, nextY):
        # empty case
        if board[nextX][nextY] == '':
            if nextX == endBoard:
                # If pawn reaches the end of the board, we win a queen
                possibleMoves.append((pos, (nextX, nextY), 8))
            else:
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
            # If pawn reaches the end of the board, we win a queen
            queenBonus = 0
            if rightX == endBoard:
                queenBonus = 8
            captureValue = checkValue(board[rightX][rightY][0])
            possibleMoves.append((pos, (rightX, rightY), captureValue + queenBonus))
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
            # If pawn reaches the end of the board, we win a queen
            queenBonus = 0
            if rightX == endBoard:
                queenBonus = 8
            captureValue = checkValue(board[leftX][leftY][0])
            possibleMoves.append((pos, (leftX, leftY), captureValue + queenBonus))
        # my piece
        elif board[leftX][leftY][-1] == color:
            pass

    return possibleMoves


def isNextPosOnBoard(nextX, nextY):
    if nextX < 0 or nextY < 0 or nextX > endBoard or nextY > endBoard:
        return False
    return True
