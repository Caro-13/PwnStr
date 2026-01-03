import random
import time
from .PwnStr import *
from Bots.ChessBotList import register_chess_bot


# Our bot
# DO NOT MODIFY THIS FILE
# Bot v1.1 - 2026-01-02
def chess_bot(player_sequence, board, time_budget, **kwargs):
    start = time.perf_counter()

    color = player_sequence[1]
    print(f"\n---------- v1.1 Playing: {'white' if color == 'w' else 'black'} ----------")
    currentScore = checkMaterial(board)
    printCurrentScore(currentScore)

    # Compute all possible moves
    allPossibleMoves = checkAllMoves(board, color)

    # Find the best move among all the possible moves:
    bestMove = defaultMove(findBestMove(allPossibleMoves), allPossibleMoves)

    # Compute and display execution time
    end = time.perf_counter()
    execution_time = round(end - start, 5)
    print(f"Execution time: {execution_time}s")
    print("---------- v1.1 ----------")

    # return (0,0), (0,0) #de base
    return bestMove[0], bestMove[1]


#   Example how to register the function
register_chess_bot("PwnStr_v11", chess_bot)
