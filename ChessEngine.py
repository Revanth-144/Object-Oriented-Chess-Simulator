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
        self.pins = [] # squares where the pinned piece is and the direction pinned from
        self.checks = [] # squares where the checking piece is and the direction of the check
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enPassantPossible = () # coordinates for the square where en passant capture is possible
        self.enPassantPossibleLog = [self.enPassantPossible]
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

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
        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endColumn] = move.pieceMoved[0] + 'Q' # promote to queen for now
        # en passant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endColumn] = "--" # capturing the pawn
        # update enPassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: # only on 2 square pawn advances
            self.enPassantPossible = ((move.startRow + move.endRow)//2, move.startColumn)
        else:
            self.enPassantPossible = ()
        # castle move
        if move.isCastleMove:
            if move.endColumn - move.startColumn == 2: # kingside castle move
                self.board[move.endRow][move.endColumn-1] = self.board[move.endRow][move.endColumn+1] # moves the rook
                self.board[move.endRow][move.endColumn+1] = "--" # erase old rook
            else: # queenside castle move
                self.board[move.endRow][move.endColumn+1] = self.board[move.endRow][move.endColumn-2] # moves the rook
                self.board[move.endRow][move.endColumn-2] = "--" # erase old rook
        self.enPassantPossibleLog.append(self.enPassantPossible) # log the en passant possible variable
        # update castling rights - whenever it is a rook or a king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

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
            # undo en passant move
            if move.isEnpassantMove:
                self.board[move.endRow][move.endColumn] = "--" # leave landing square blank
                self.board[move.startRow][move.endColumn] = move.pieceCaptured
            self.enPassantPossibleLog.pop() # get rid of the old en passant possible square
            self.enPassantPossible = self.enPassantPossibleLog[-1] # set the en passant possible square to the last one in the list
            # undo castling rights
            self.castleRightsLog.pop() # get rid of the new castle rights from the move we are undoing
            self.currentCastlingRight = CastleRights(self.castleRightsLog[-1].wks, self.castleRightsLog[-1].bks, self.castleRightsLog[-1].wqs, self.castleRightsLog[-1].bqs) # set the current castle rights to the last one in the list
            # undo castle move
            if move.isCastleMove:
                if move.endColumn - move.startColumn == 2: # kingside
                    self.board[move.endRow][move.endColumn+1] = self.board[move.endRow][move.endColumn-1]
                    self.board[move.endRow][move.endColumn-1] = "--"
                else: # queenside
                    self.board[move.endRow][move.endColumn-2] = self.board[move.endRow][move.endColumn+1]
                    self.board[move.endRow][move.endColumn+1] = "--"
            self.checkMate = False
            self.staleMate = False

    '''
    Update the castle rights given the move
    '''
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startColumn == 0: # left rook
                    self.currentCastlingRight.wqs = False
                elif move.startColumn == 7: # right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startColumn == 0: # left rook
                    self.currentCastlingRight.bqs = False
                elif move.startColumn == 7: # right rook
                    self.currentCastlingRight.bks = False
        # if a rook is captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endColumn == 0: # left rook
                    self.currentCastlingRight.wqs = False
                elif move.endColumn == 7: # right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endColumn == 0: # left rook
                    self.currentCastlingRight.bqs = False
                elif move.endColumn == 7: # right rook
                    self.currentCastlingRight.bks = False         

    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        tempEnPassantPossible = self.enPassantPossible # Store the current enPassantPossible value
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs) # Store the current castling rights
        # 1) Generate all possible moves
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
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
        self.enPassantPossible = tempEnPassantPossible # Restore the enPassantPossible value
        self.currentCastlingRight = tempCastleRights # Restore the castling rights
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
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove: # White pawn moves
            moveAmount = -1
            startRow = 6
            enemyColor = "b"
            kingRow, kingCol = self.whiteKingLocation
        else: # Black pawn moves
            moveAmount = 1
            startRow = 1
            enemyColor = "w"
            kingRow, kingCol = self.blackKingLocation

        if self.board[r + moveAmount][c] == "--": # 1 square pawn advance
            if not piecePinned or pinDirection == (moveAmount, 0):
                moves.append(Move((r, c), (r + moveAmount, c), self.board))
                if r == startRow and self.board[r + 2 * moveAmount][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2 * moveAmount, c), self.board))
        if c - 1 >= 0: # captures to the left
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor: # enemy piece to capture
                    moves.append(Move((r, c), (r + moveAmount, c - 1), self.board))
                elif (r + moveAmount, c - 1) == self.enPassantPossible:                        
                    attackingPiece = blockingPiece = False
                    if kingRow == r: # the king is on the same row as the pawn
                        if kingCol < c: # the king is left of the pawn
                            # inside between the king and pawn, outside is everything else
                            insideRange = range(kingCol + 1, c)
                            outsideRange = range(c + 1, 8)
                        else: # the king is right of the pawn
                            insideRange = range(kingCol - 1, c+1, -1)
                            outsideRange = range(c - 1, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--": # some other piece beside the pawn blocks
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == 'R' or square[1] == 'Q'): # enemy rook or queen on attack path
                                attackingPiece = True
                            elif square != "--": # some other piece beside the pawn blocks
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, isEnpassantMove=True))
        if c + 1 <= 7: # captures to the right
            if self.board[r + moveAmount][c + 1][0] == enemyColor: # enemy piece to capture
                if not piecePinned or pinDirection == (moveAmount, 1):
                    moves.append(Move((r, c), (r + moveAmount, c + 1), self.board))
            elif (r + moveAmount, c + 1) == self.enPassantPossible:
                if not piecePinned or pinDirection == (moveAmount, 1):
                    moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, isEnpassantMove=True))

    '''
    Get all the rook moves for the pawn located at row, column and add these moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: # enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: # friendly piece invalid
                            break
                else: # off board
                    break

    '''
    Get all the knight moves for the pawn located at row, column and add these moves to the list
    '''
    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
    Get all the bishop moves for the pawn located at row, column and add these moves to the list
    '''
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # 4 diagonals
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: # enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: # friendly piece invalid
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
    '''
    Get all the castle moves for the king located at row, column and add these moves to the list
    '''
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return # can't castle while we are in check
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)

    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks # white king side
        self.bks = bks # black king side
        self.wqs = wqs # white queen side
        self.bqs = bqs # black queen side

class Move():
    # maps keys to values
    # key: value
    # "e4": (6, 4)
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToColumns = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    columnsToFiles = {v: k for k, v in filesToColumns.items()}

    def __init__(self, startSquare, endSquare, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSquare[0]
        self.startColumn = startSquare[1]
        self.endRow = endSquare[0]
        self.endColumn = endSquare[1]
        self.pieceMoved = board[startSquare[0]][startSquare[1]]
        self.pieceCaptured = board[endSquare[0]][endSquare[1]]
        self.isPawnPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7)
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"
        # castle move
        self.isCastleMove = isCastleMove
        self.isCapture = self.pieceCaptured != "--"
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

    # overriding the str() method
    def __str__(self):
        # castle move
        if self.isCastleMove:
            return "O-O" if self.endColumn == 6 else "O-O-O"
        endSquare = self.getRankFile(self.endRow, self.endColumn)
        # pawn moves
        if self.pieceMoved[1] == "p":
            if self.isCapture:
                return self.columnsToFiles[self.startColumn] + "x" + endSquare
            else:
                return endSquare
            # pawn promotion
        # two of the same type of piece can move to the same square

        # also adding + for check and # for checkmate at the end of the move notation

        # piece moves
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += "x"
        return moveString + endSquare
