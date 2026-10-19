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
