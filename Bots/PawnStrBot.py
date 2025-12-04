from decorator import append
boardLength = 8
from parso.python.tree import String

#
#   Example function to be implemented for
#       Single important function is next_best
#           color: a single character str indicating the color represented by this bot ('w' for white)
#           board: a 2d matrix containing strings as a descriptors of the board '' means empty location "XC" means a piece represented by X of the color C is present there
#           budget: time budget allowed for this turn, the function must return a pair (xs,ys) --> (xd,yd) to indicate a piece at xs, ys moving to xd, yd
#

#   Be careful with modules to import from the root (don't forget the Bots.)
from Bots.ChessBotList import register_chess_bot

#   Simply move the pawns forward and tries to capture as soon as possible
def chess_bot(player_sequence, board, time_budget, **kwargs):

    color = player_sequence[1]
    for x in range(board.shape[0]-1):
        for y in range(board.shape[1]):
            if board[x,y][-1] != color:
                continue
            print(board[x,y].string(), (x,y))

        print("\n")

    return (0,0), (0,0)

#   Example how to register the function
register_chess_bot("PwnStr", chess_bot)

def checkDiagonal(pos, board, color):
    x = pos[0]
    y = pos[1]
    possibleMoves = []

    rightBottum = y if y < x else x
    rightUp = y if y < boardLength-x else boardLength-x

    leftBottum = boardLength-y if boardLength-y < x else x
    leftUp =  boardLength-y if boardLength-y < boardLength-x else boardLength-x

    def goDiagonal(horiz,vert,borne,step):
        for i in range(x, borne,step):
            nextPos = (x + i*vert, y + i*horiz)
            if nextPos == "":
                possibleMoves.append((pos, nextPos))

            if board[nextPos][-1] != color:
                possibleMoves.append((pos, nextPos))
                break

            if board[nextPos][-1] == color:
                break

    goDiagonal(-1,1,rightUp,1)
    goDiagonal(-1,-1,rightBottum,-1)
    goDiagonal(1,1,leftUp,1)
    goDiagonal(1,-1,leftBottum,-1)


    return possibleMoves


def chechHorizVerti(pos, board, color):
    possibleMoves = []
    return possibleMoves

def checkL (pos, board, color):
    possibleMoves = []
    return possibleMoves

def checkCarre(pos, board, color):
    possibleMoves = []
    return possibleMoves

def checkPawn(pos, board, color):
    possibleMoves = []
    return possibleMoves


