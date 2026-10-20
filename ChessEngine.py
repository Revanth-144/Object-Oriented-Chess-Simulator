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
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    '''
    Takes a Move as a parameter and executes it (this will not work for castling, en passant, and promoting)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startColumn] = "--"
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove # swap players
        # update the king's location if moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endColumn)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endColumn)

    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: # make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startColumn] = move.pieceMoved
            self.board[move.endRow][move.endColumn] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # swap players
            # update the king's location if moved
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startColumn)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startColumn)

    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        # 1) Generate all possible moves
        moves = self.getAllPossibleMoves()
        # 2) For each move, make the move
        for i in range(len(moves)-1, -1, -1): # when removing from a list go backwards through that list
            self.makeMove(moves[i])
            # 3) Generate all opponent's moves
            # 4) For each of the opponent's moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) # 5) If they do attack your king, not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0: # either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves

    '''
    Determine if the current player is in check
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''
    Determine if the enemy can attack the square r, c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # switch to opponent's point of view
        opponentMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove # switch turns back
        for move in opponentMoves:
            if move.endRow == r and move.endColumn == c: # square is under attack
                return True
        return False
        
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
                    self.moveFunctions[piece](r, c, moves) # Calls the appropriate move finction based on the piece selected
        return moves

    '''
    Get all the pawn moves for the pawn located at row, column and add these moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # White pawn moves
            if self.board[r-1][c] == "--": # Empty square on one row advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0 and self.board[r-1][c-1][0] == "b": # Enemy piece to capture on the left
                moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7 and self.board[r-1][c+1][0] == "b": # Enemy piece to capture on the right
                moves.append(Move((r, c), (r-1, c+1), self.board))
        else: # Black pawn moves
            if self.board[r+1][c] == "--": # Empty square on one row advance
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0 and self.board[r+1][c-1][0] == "w": # Enemy piece to capture on the left
                moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7 and self.board[r+1][c+1][0] == "w": # Enemy piece to capture on the right
                moves.append(Move((r, c), (r+1, c+1), self.board))
        # Add pawn promotion later

    '''
    Get all the rook moves for the pawn located at row, column and add these moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # On board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # Empty space
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # Enemy piece
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # friendly piece
                        break
                else: # off board
                    break

    '''
    Get all the knight moves for the pawn located at row, column and add these moves to the list
    '''
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
    Get all the bishop moves for the pawn located at row, column and add these moves to the list
    '''
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # upleft, upright, downleft, downright
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # On board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # Empty space
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # Enemy piece
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # friendly piece
                        break
                else: # off board
                    break

    '''
    Get all the queen moves for the pawn located at row, column and add these moves to the list
    '''
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
    Get all the king moves for the pawn located at row, column and add these moves to the list
    '''
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    
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
