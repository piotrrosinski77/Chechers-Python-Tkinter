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
                    self.grid[row][col] = 'B'
        for row in range(5, 8):  # Białe pionki
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = 'W'

    def get_possible_moves(self, row, col):
        piece = self.grid[row][col]
        moves = []

        # Sprawdzenie ruchów dla czarnych pionków
        if piece == 'B':
            if row + 1 < 8:
                if col - 1 >= 0 and self.grid[row + 1][col - 1] is None:
                    moves.append((row + 1, col - 1))
                if col + 1 < 8 and self.grid[row + 1][col + 1] is None:
                    moves.append((row + 1, col + 1))

        # Sprawdzenie ruchów dla białych pionków
        if piece == 'W':
            if row - 1 >= 0:
                if col - 1 >= 0 and self.grid[row - 1][col - 1] is None:
                    moves.append((row - 1, col - 1))
                if col + 1 < 8 and self.grid[row - 1][col + 1] is None:
                    moves.append((row - 1, col + 1))

        return moves

    def move_piece(self, from_row, from_col, to_row, to_col):
        # Przenieś pionek z pozycji (from_row, from_col) do (to_row, to_col)
        self.grid[to_row][to_col] = self.grid[from_row][from_col]
        self.grid[from_row][from_col] = None
        # Dodatkowe zasady, takie jak usuwanie pionków w przypadku bicia, można dodać tutaj
