import random
import time
from .PwnStr import *
from Bots.ChessBotList import register_chess_bot


# Our bot
def chess_bot(player_sequence, board, time_budget, **kwargs):
    start = time.perf_counter()

    color = player_sequence[1]
    print(f"\n---------- v3 Playing: {'white' if color == 'w' else 'black'} ----------")
    currentScore = checkMaterial(board)
    printCurrentScore(currentScore)

    # Compute all possible moves
    allPossibleMoves = checkAllMoves3(board, color)
    print(f"Possible moves: {len(allPossibleMoves)}")
    # displayMoves(board, allPossibleMoves)

    # Find the best move among all the possible moves:
    # bestMove = findBestMove(allPossibleMoves)
    bestMove = checkNextMoves3(board, allPossibleMoves, color)
    print()
    printBoard(board)
    print()
    print(f"Returned move: {pieceToString(board[bestMove[0][0]][bestMove[0][1]][0])} moves {bestMove}")

    # Compute and display execution time
    end = time.perf_counter()
    execution_time = round(end - start, 5)
    print(f"Execution time: {execution_time}s")
    print("---------- v3 ----------")

    # return (0,0), (0,0) #de base
    return bestMove[0], bestMove[1]


#   Example how to register the function
register_chess_bot("PwnStr_v3", chess_bot)
