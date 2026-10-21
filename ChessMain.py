"""
Main Driver file responsible for handling user input and displaying the current game state on the screen.
"""

import pygame as p
import ChessEngine, SmartMoveFinder

Width = Height = 512 # 400 pixels is another alternative
DIMENSION = 8 # chessboard is 8x8
SquareSize = Height // DIMENSION
MAX_FPS = 15 # For animations later on
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main.
'''
def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (SquareSize, SquareSize))
    #Note: we can access an image by saying 'IMAGES['wp']'

'''
The main driver for our code. This will handle user input and updating the graphics.
'''
def main():
    p.init()
    screen = p.display.set_mode((Width, Height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # Flag variable when a move is made
    animate = False # Flag variable for when we should animate a move
    loadImages() # only do this once, before the while loop
    running = True
    squareSelected = () # no square is selected, keep track of the last click of the user (tuple: (row, column))
    playerClicks = [] # keep track of the player clicks (two tuples: [(6, 4), (4, 4)]
    gameOver = False
    playerOne = False # If a human is playing white, then this will be True. If an AI is playing, then this will be False.
    playerTwo = False # Same as above but for black.
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() # (x,y) coordinates of the mouse click
                    col = location[0] // SquareSize
                    row = location[1] // SquareSize
                    if squareSelected == (row, col): # the user clicked the same square twice
                        squareSelected = () # deselect
                        playerClicks = [] # clear the player clicks
                    else:
                        squareSelected = (row, col)
                        playerClicks.append(squareSelected) # append for both the first and second click
                    if len(playerClicks) == 2: # after 2 clicks
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                squareSelected = () # reset the square selected
                                playerClicks = [] # reset the player clicks
                        if not moveMade:    
                            playerClicks = [squareSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r: # reset the game when 'r' is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    squareSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
        # AI move finder logic
        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        drawGameState(screen, gs, validMoves, squareSelected)
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')
        clock.tick(MAX_FPS)
        p.display.flip()
    
'''
Highlights square selected and moves for piece selected.
'''
def highlightSquares(screen, gs, validMoves, squareSelected):
    if squareSelected != ():
        r, c = squareSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): # square selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SquareSize, SquareSize))
            s.set_alpha(100) # transparency value -> 0 transparent; 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SquareSize, r*SquareSize))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startColumn == c:
                    screen.blit(s, (move.endColumn*SquareSize, move.endRow*SquareSize))

'''
Responsible for all the graphics within a current game state.
'''    
def drawGameState(screen, gs, validMoves, squareSelected):
    drawBoard(screen) # draw squares on the board
    highlightSquares(screen, gs, gs.getValidMoves(), squareSelected) # highlight square selected and moves for piece selected
    drawPieces(screen, gs.board) # draw pieces on the board

'''
Draw the squares on the board. The top left square is always light.
'''
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SquareSize, r*SquareSize, SquareSize, SquareSize)) 

'''
Draw the pieces on the board.
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SquareSize, r*SquareSize, SquareSize, SquareSize))

'''
Animating a move
'''
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endColumn - move.startColumn
    framesPerSquare = 10 # frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startColumn + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.endRow + move.endColumn) % 2]
        endSquare = p.Rect(move.endColumn*SquareSize, move.endRow*SquareSize, SquareSize, SquareSize)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SquareSize, r*SquareSize, SquareSize, SquareSize))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, Width, Height).move(Width/2 - textObject.get_width()/2, Height/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()
