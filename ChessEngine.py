"""
This class is responsible for storing all the information about the chess game. It is also responsible for determining the valid moves. It will also keep a move log.
"""

class GameState():
    def __init__(self) -> None:
        # board is 8x8 2d list and each element in a list has 2 characters
        # first character represents the color of the piece, b for black and w for white
        # the second character represent the type rook, knight, bishop, queen, king and pawn
        ## "--" represents the empty box with no cell
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []

    '''
    Takes a Move as a parameter and executes it (this will not work for castling, en passant, and promoting)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove # swap players

    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: # make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startColumn] = move.pieceMoved
            self.board[move.endRow][move.endColumn] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # swap players

    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() # For now we will not consider checks

    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # Number of rows
            for c in range(len(self.board[r])): # Number of columns
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1] # type of piece
                    if piece == "p":
                        self.getPawnMoves(r, c, moves)
                    elif piece == "R":
                        self.getRookMoves(r, c, moves)
                    elif piece == "N":
                        self.getKnightMoves(r, c, moves)
                    elif piece == "B":
                        self.getBishopMoves(r, c, moves)
                    elif piece == "Q":
                        self.getQueenMoves(r, c, moves)
                    elif piece == "K":
                        self.getKingMoves(r, c, moves)
        return moves

    '''
    Get all the pawn moves for the pawn located at row, column and add these moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        pass

    '''
    Get all the rook moves for the pawn located at row, column and add these moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        pass

    '''
    Get all the knight moves for the pawn located at row, column and add these moves to the list
    '''
    def getKnightMoves(self, r, c, moves):
        pass

    '''
    Get all the bishop moves for the pawn located at row, column and add these moves to the list
    '''
    def getBishopMoves(self, r, c, moves):
        pass

    '''
    Get all the queen moves for the pawn located at row, column and add these moves to the list
    '''
    def getQueenMoves(self, r, c, moves):
        pass

    '''
    Get all the king moves for the pawn located at row, column and add these moves to the list
    '''
    def getKingMoves(self, r, c, moves):
        pass
    
class Move():
    # maps keys to values
    # key: value
    # "e4": (6, 4)
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToColumns = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    columnsToFiles = {v: k for k, v in filesToColumns.items()}

    def __init__(self, startSquare, endSquare, board):
        self.startRow = startSquare[0]
        self.startColumn = startSquare[1]
        self.endRow = endSquare[0]
        self.endColumn = endSquare[1]
        self.pieceMoved = board[startSquare[0]][startSquare[1]]
        self.pieceCaptured = board[endSquare[0]][endSquare[1]]
        self.moveId = self.startRow * 1000 + self.startColumn * 100 + self.endRow * 10 + self.endColumn

    '''
    Overriding the equals Method
    '''
    def __eq__(self, other) -> bool:
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False

    def getChessNotation(self):
        # you can add to make this like "e2e4" or "e7e8q" later
        return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)

    def getRankFile(self, row, column):
        return self.columnsToFiles[column] + self.rowsToRanks[row]
