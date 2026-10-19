"""
Main Driver file responsible for handling user input and displaying the current game state on the screen.
"""

import pygame as p
import ChessEngine

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
        IMAGES[piece] = p.transform.scale(p.image.load(piece + ".png"), (SquareSize, SquareSize))
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
    loadImages() # only do this once, before the while loop
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
    

'''
Responsible for all the graphics within a current game state.
'''    
def drawGameState(screen, gs):
    drawBoard(screen) # draw squares on the board
    # add in piece highlighting or move suggestions later
    drawPieces(screen, gs.board) # draw pieces on the board

'''
Draw the squares on the board. The top left square is always light.
'''
def drawBoard(screen):
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

if __name__ == "__main__":
    main()
