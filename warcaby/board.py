from .piece import Piece

class Board:
    def __init__(self):
        # Plansza 8x8, puste pola oznaczone jako None, pionki jako 'B' (czarne) lub 'W' (białe)
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_pieces()

    def initialize_pieces(self):
        # Inicjalizacja pionków na planszy (czarne na górze, białe na dole)
        for row in range(3):  # Czarne pionki
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece('B')
        for row in range(5, 8):  # Białe pionki
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece('W')
