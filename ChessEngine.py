from shutil import move


class GameState():
    def __init__(self):
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
        self.moveFunction = {
            'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
            'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves
        }
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = () # (row, col) of the square where en passant is possible, empty if not possible

    '''
    Takes move as a parameter and execures it
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so that we can undo it later
        self.whiteToMove = not self.whiteToMove # swap the players
        # update the kings location
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
        
        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q' # promote to queen

        # en passant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--" # remove the pawn that was captured en passant
        
        # Update our enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: # Only on 2 square pawn advance
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.endCol) # the square behind the pawn that can be captured en passant
        else:
            self.enpassantPossible = () # reset en passant possible if not a pawn move or not a 2 square advance
    
    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # update the kings location
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            # Undo en passant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--" # remove the pawn that was captured en passant
                self.board[move.startRow][move.endCol] = move.pieceCaptured # restore the pawn that was captured en passant
                self.enpassantPossible = (move.endRow, move.endCol) # restore the en passant possible square
            # Undo a 2 square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

    
    '''
    All moves including checks
    '''
    def getValidMoves(self):
        moves = []
        tempEnpassantPossible = self.enpassantPossible
        if self.whiteToMove:
            kingRow, kingCol = self.whiteKingLocation
        else:
            kingRow, kingCol = self.blackKingLocation
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks() 
        if self.inCheck:
            if len(self.checks) == 1:
                # only one check, so we need to block it or move the king
                check = self.checks[0]
                checkRow, checkCol = check[0], check[1]
                pieceChecking = self.board[checkRow][checkCol] # the piece that is checking the king
                validSquares = [] # squares that piece can move to
                # if the piece is knight we have to capture it or move the king and otherwise we can block it
                if pieceChecking[1] == 'N': # knight
                    validSquares.append((checkRow, checkCol))
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) # check[2] and check[3] are the direction of the check
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: # we have reached the piece checking the king
                            break
                # remove all moves that do not block the check or move the king to a valid square
                for i in range(len(moves)-1, -1, -1): # when removing from a list go backwards through the list
                    if moves[i].pieceMoved[1] != 'K': # not a king move so it must block the check or capture the piece checking the king
                        if (moves[i].endRow, moves[i].endCol) not in validSquares: # the move does not block the check or capture the piece checking the king
                            moves.remove(moves[i])
            else: # more than one check, so we can only move the king
                self.getKingMoves(kingRow, kingCol, moves)
        else: # not in check, so we can make all possible moves
            moves = self.getAllPossibleMoves()
        self.enpassantPossible = tempEnpassantPossible # reset en passant possible after getting all moves
        return moves
    
    '''
    Determine if the current player in check
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
    
    '''
    Determine if the enemy can attack the square row, col
    '''
    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove
        opponentMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in opponentMoves:
            if move.endRow == row and move.endCol == col: # square is under attack
                return True
        return False

    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.moveFunction[piece](row, col, moves)
        return moves
    
    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self, row, col, moves):
        piecePinned = False
        pinDirection = () # direction the pinned piece is pinned from
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3]) # direction the pinned piece is pinned from
                self.pins.remove(self.pins[i]) # remove the pin since we are going to use it
                break

        if self.whiteToMove: # white pawn moves
            if self.board[row - 1][col] == "--": # 1 square pawn advance
                if not piecePinned or pinDirection == (-1, 0): # if not pinned or pinned in the same direction as the pawn move
                    moves.append(Move((row, col), (row - 1, col), self.board))
                    if row == 6 and self.board[row - 2][col] == "--": # 2 square pawn advance
                        moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0: # captures to the left
                if self.board[row - 1][col - 1][0] == 'b': # enemy piece to capture
                    if not piecePinned or pinDirection == (-1, -1): # if not pinned or pinned in the same direction as the pawn move
                        moves.append(Move((row, col), (row - 1, col - 1), self.board))
                elif (row - 1, col - 1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (-1, -1): # if not pinned or pinned in the same direction as the pawn move
                        moves.append(Move((row, col), (row - 1, col - 1), self.board, isEnpassantMove = True))
            if col + 1 <= 7: # captures to the right
                if self.board[row - 1][col + 1][0] == 'b': # enemy piece to capture
                    if not piecePinned or pinDirection == (-1, 1): # if not pinned or pinned in the same direction as the pawn move
                        moves.append(Move((row, col), (row - 1, col + 1), self.board))
                elif (row - 1, col + 1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (-1, 1): # if not pinned or pinned in the same direction as the pawn move
                        moves.append(Move((row, col), (row - 1, col + 1), self.board, isEnpassantMove = True))
        else: # black pawn moves
            if self.board[row + 1][col] == "--": # 1 square pawn advance
                if not piecePinned or pinDirection == (1, 0): # if not pinned or pinned in the same direction as the pawn move
                    moves.append(Move((row, col), (row + 1, col), self.board))
                    if row == 1 and self.board[row + 2][col] == "--": # 2 square pawn advance
                        moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0: # captures to the left
                if self.board[row + 1][col - 1][0] == 'w': # enemy piece to capture
                    if not piecePinned or pinDirection == (1, -1): # if not pinned or pinned in the same direction as the pawn move
                        moves.append(Move((row, col), (row + 1, col - 1), self.board))
                elif (row + 1, col - 1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (1, -1): # if not pinned or pinned in the same direction as the pawn move
                        moves.append(Move((row, col), (row + 1, col - 1), self.board, isEnpassantMove = True))
            if col + 1 <= 7: # captures to the right
                if self.board[row + 1][col + 1][0] == 'w': # enemy piece to capture
                    if not piecePinned or pinDirection == (1, 1): # if not pinned or pinned in the same direction as the pawn move
                        moves.append(Move((row, col), (row + 1, col + 1), self.board))
                elif (row + 1, col + 1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (1, 1): # if not pinned or pinned in the same direction as the pawn move
                        moves.append(Move((row, col), (row + 1, col + 1), self.board, isEnpassantMove = True))

    '''
    Get all the rook moves for the pawn located at row, col and add these moves to the list
    '''
    def getRookMoves(self, row, col, moves):
        pinnedPiece = False
        pinnedDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                pinnedPiece = True
                pinnedDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] == 'Q': # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i]) # remove the pin since we are going to use it
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # up, left, down, right
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8): # can move max 7 squares
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # On board
                    if not pinnedPiece or pinnedDirection == d or pinnedDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": # empty space valid
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: # enemy piece valid
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                            break
                        else: # friendly piece invalid
                            break
                else: # off the board
                    break

    '''
    Get all the knight moves for the pawn located at row, col and add these moves to the list
    '''
    def getKnightMoves(self, row, col, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                self.pins.remove(self.pins[i]) # remove the pin since we are going to use it
                break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = row + m[0]
            endCol = col + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: # not an ally (empty or an enemy piece)
                        moves.append(Move((row, col), (endRow, endCol), self.board))

    '''
    Get all the bishop moves for the pawn located at row, col and add these moves to the list
    '''
    def getBishopMoves(self, row, col, moves):
        piecePinned = False
        pinnedDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinnedDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i]) # remove the pin since we are going to use it
                break
    
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # up-left, up-right, down-left, down-right
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8): # can move max 7 squares
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # On board
                    if not piecePinned or pinnedDirection == d or pinnedDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": # empty space valid
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: # enemy piece valid
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                            break
                        else: # friendly piece invalid
                            break
                else: # off the board
                    break

    '''
    Get all the queen moves for the pawn located at row, col and add these moves to the list
    '''
    def getQueenMoves(self, row, col, moves):
        self.getRookMoves(row, col, moves)
        self.getBishopMoves(row, col, moves)

    '''
    Get all the king moves for the pawn located at row, col and add these moves to the list
    '''
    def getKingMoves(self, row, col, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1) # up-left, up, up-right, left, right, down-left, down, down-right
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = row + rowMoves[i]
            endCol = col + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally (empty or an enemy piece)
                    # place king on the square and check if it is under attack
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck: # king is not under attack
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    # place king back to its original position
                    if allyColor == 'w':
                        self.whiteKingLocation = (row, col)
                    else:
                        self.blackKingLocation = (row, col)

    '''
    Returns if the player is in check, a list of pins and a list of checks
    '''
    def checkForPinsAndChecks(self):
        pins = [] # Squares where the allied pinned piece is and direction pinned from
        checks = [] # squares where enemy is applying for a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allycolor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allycolor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = ((-1, 0), (0, -1), (1 ,0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () # reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allycolor and endPiece[1] != 'K': # Allied piece
                        if possiblePin == (): # 1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: # 2nd allied piece, so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        piece_type = endPiece[1]
                        # 5 Possibilities in this complex condition:
                        # 1.orthogonally away from king and piece is a rook
                        # 2.diagonally away from king and piece is a bishop
                        # 3.one square diagonally away from king and piece is a pawn
                        # 4.any direction and piece is a queen
                        # 5.any direction one square away and piece is a king(this is necessary to prevent a king move to square controlled by enemy king)
                        if (0 <= j <= 3 and piece_type == 'R') or \
                           (4 <= j <= 7 and piece_type == 'B') or \
                           (i == 1 and piece_type == 'p' and ((enemyColor == 'b' and j == 4) or (enemyColor == 'w' and j == 5))) or \
                           (piece_type == 'Q') or \
                           (i == 1 and piece_type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: # piece blocking so no pin
                                pins.append(possiblePin)
                                break
                        else: # enemy piece not applying for a check
                            break
                else:
                    break # off the board
        # check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N': # Enemy knight applying for a check
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks             
    
class Move():
    # maps keys to values
    # key : value
    ranksToRows = {
        "1": 7, "2": 6, "3": 5, "4": 4,
        "5": 3, "6": 2, "7": 1, "8": 0
    }
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {
        "a": 0, "b": 1, "c": 2, "d": 3,
        "e": 4, "f": 5, "g": 6, "h": 7
    }
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # Pawn promotion
        self.isPawnPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7)
        # En passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "bp" if self.pieceMoved == "wp" else "wp"
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    
    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)    

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]