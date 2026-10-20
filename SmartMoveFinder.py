import random

def findRandomMove(validMoves):
    """
    Selects a random move from the list of valid moves.

    Parameters:
    validMoves (list): A list of valid moves.

    Returns:
    move: A randomly selected move from the valid moves.
    """
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gs, validMoves):
    return findRandomMove(validMoves)  # Placeholder for a more advanced algorithm in the future