import random
import time

from .PwnStr import *

#   Example function to be implemented for
#       Single important function is next_best
#           color: a single character str indicating the color represented by this bot ('w' for white)
#           board: a 2d matrix containing strings as a descriptors of the board '' means empty location "XC" means a piece represented by X of the color C is present there
#           budget: time budget allowed for this turn, the function must return a pair (xs,ys) --> (xd,yd) to indicate a piece at xs, ys moving to xd, yd
#

#   Be careful with modules to import from the root (don't forget the Bots.)
from Bots.ChessBotList import register_chess_bot

#  our bot v_1

def chess_bot(player_sequence, board, time_budget, **kwargs):
    start = time.perf_counter()

    color = player_sequence[1]
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
                print(board[x][y][0] + board[x][y][1], (x,y),piecePossibleMoves)
                allPossibleMoves.extend(piecePossibleMoves)
        print("\n")

    bestMove = ((0,0),(0,0),0)
    for i in range(len(allPossibleMoves)):
        if allPossibleMoves[i][2] > bestMove[2]:
            bestMove = allPossibleMoves[i]
    while bestMove == ((0,0),(0,0),0):
        bestMove = allPossibleMoves[random.randint(0,len(allPossibleMoves)-1)]

    # Compute and display execution time
    end = time.perf_counter()
    execution_time = round(end - start, 5)
    print(f"Execution time: {execution_time}s")

    #return (0,0), (0,0) #de base
    return bestMove[0],bestMove[1]

#   Example how to register the function
register_chess_bot("PwnStr_V1", chess_bot)
