import pygame as p
import ChessEngine

width = height = 512
dimension = 8
square_size = height // dimension
max_fps = 15
images = {}

def loadImages():
    pieces = ['wp', 'bp', 'wR', 'bR', 'wN', 'bN', 'wB', 'bB', 'wQ', 'bQ', 'wK', 'bK']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load(piece + ".png"),(square_size,square_size))

def main():
    p.init()
    screen = p.display.set_mode((width,height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable when a move is made
    loadImages()
    running = True
    sqSelected = () # No square is selected initially, tuple indicates (x, y)
    playerClicks = [] # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of mouse
                col = location[0] // square_size
                row = location[1] // square_size
                if sqSelected == (row, col): # User clicking same square twice
                    sqSelected = () # deselect
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #append for both first and second clicks
                if len(playerClicks) == 2: #after second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]: # check if the move is valid
                            gs.makeMove(move)
                            moveMade = True
                            sqSelected = () # reset the user clicks
                            playerClicks = [] # clear player clicks
                    if not moveMade: # if the move was invalid
                        playerClicks = [sqSelected]
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(max_fps)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(dimension):
        for col in range(dimension):
            color = colors[(row + col)%2]
            p.draw.rect(screen, color, p.Rect(col*square_size,row*square_size,square_size,square_size))

def drawPieces(screen, board):
    for row in range(dimension):
        for col in range(dimension):
            piece = board[row][col]
            if piece != "--":
                screen.blit(images[piece], p.Rect(col*square_size, row*square_size, square_size, square_size))

if __name__ == "__main__":
    main()