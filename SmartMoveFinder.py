import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
checkMate = 1000
staleMate = 0

'''
Pick and return a random valid move from the list of valid moves.
'''
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

'''
Find the best move based on the current board state.
'''
def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = checkMate
    bestPlayerMove = None
    random.shuffle(validMoves) # randomize the order of valid moves to avoid always picking the same move
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentMoves = gs.getValidMoves()
        opponentMaxScore = -checkMate
        for opponentMove in opponentMoves:
            gs.makeMove(opponentMove)
            if gs.checkMate:
                score = -turnMultiplier * checkMate # if the opponent is in checkmate, then the player is in a good position
            elif gs.staleMate:
                score = staleMate
            else:
                score = -turnMultiplier * scoreMaterial(gs.board)
            if score > opponentMaxScore:
                opponentMaxScore = score
            gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove


'''
Score the board based on the material count.
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score