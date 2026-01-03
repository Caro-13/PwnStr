import random
import time
from .PwnStr import *
from Bots.ChessBotList import register_chess_bot


# Our bot
# DO NOT MODIFY THIS FILE
# Bot v1 - 2026-01-02
def chess_bot(player_sequence, board, time_budget, **kwargs):
    start = time.perf_counter()

    color = player_sequence[1]
    print(f"\n---------- v1 Playing: {'white' if color == 'w' else 'black'} ----------")
    currentScore = checkMaterial(board)
    printCurrentScore(currentScore)

    allPossibleMoves = []

    for x in range(board.shape[0]-1):
        for y in range(board.shape[1]):
            if board[x][y] != "":
                if board[x][y][-1] != color:
                    continue
                pos = (x, y)
                piecePossibleMoves = checkMoves(pos, board, color)
                # print(board[x][y][0] + board[x][y][1], (x,y),piecePossibleMoves)
                allPossibleMoves.extend(piecePossibleMoves)
        # print("\n")

    bestMove = ((0,0),(0,0),0)
    for i in range(len(allPossibleMoves)):
        if allPossibleMoves[i][2] > bestMove[2]:
            bestMove = allPossibleMoves[i]
    while bestMove == ((0,0),(0,0),0):
        print("Random move")
        bestMove = allPossibleMoves[random.randint(0,len(allPossibleMoves)-1)]

    # Compute and display execution time
    end = time.perf_counter()
    execution_time = round(end - start, 5)
    print(f"Execution time: {execution_time}s")
    print("---------- v1 ----------")

    #return (0,0), (0,0) #de base
    return bestMove[0],bestMove[1]

#   Example how to register the function
# register_chess_bot("PwnStr_v1", chess_bot)
