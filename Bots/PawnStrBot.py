import random
import time
from .PwnStr import *
from Bots.ChessBotList import register_chess_bot


# Our bot
def chess_bot(player_sequence, board, time_budget, **kwargs):
    random.seed(time.time())
    start = time.perf_counter()

    color = player_sequence[1]
    print(f"\n---------- vX Playing: {'white' if color == 'w' else 'black'} ----------")
    currentScore = checkMaterial(board)
    printCurrentScore(currentScore)

    allPossibleMoves = checkAllMoves(board, color)
    #check if can take opponent king in one move
    for move in allPossibleMoves:
        targetPos = move[1]  # Where we're moving to
        targetPiece = board[targetPos[0]][targetPos[1]]
        # yes : do it now !!!!!
        if targetPiece != '' and targetPiece[0] == 'k' and targetPiece[-1] != color:
            print(f"Returned move: {pieceToString(board[move[0][0]][move[0][1]][0])} captures KING at {move}")
            end = time.perf_counter()
            execution_time = round(end - start, 5)
            print(f"Execution time: {execution_time}s")
            print("---------- vX ----------")
            return move[0], move[1]

    # No : do min-max
    score, bestMove = minimax(board, depth=3, maximizing_player=True, color=color)


    print()
    printBoard(board)
    print()
    print(f"Returned move: {pieceToString(board[bestMove[0][0]][bestMove[0][1]][0])} moves {bestMove}")

    # Compute and display execution time
    end = time.perf_counter()
    execution_time = round(end - start, 5)
    print(f"Execution time: {execution_time}s")
    print("---------- vX ----------")

    # return (0,0), (0,0) #de base
    return bestMove[0], bestMove[1]


#   Example how to register the function
register_chess_bot("PwnStr", chess_bot)
