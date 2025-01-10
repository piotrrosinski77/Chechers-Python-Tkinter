# from .ai import CheckersAIModel  # lub inny odpowiedni import, zależnie od struktury


class Board:
    def __init__(self):
        # board 8x8, B = black, W = white
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_pieces()

    def initialize_pieces(self):
        # white pieces are at the bottom of the window
        for row in range(3):  # black pieces
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = "B"
        for row in range(5, 8):  # white pieces
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = "W"

    def get_possible_moves(self, row, col):
        piece = self.grid[row][col]
        moves = []

        # check available moves for black pieces
        if piece == "B":
            if row + 1 < 8:
                if col - 1 >= 0 and self.grid[row + 1][col - 1] is None:
                    moves.append((row + 1, col - 1))
                if col + 1 < 8 and self.grid[row + 1][col + 1] is None:
                    moves.append((row + 1, col + 1))

        # check available moves for white pieces
        if piece == "W":
            if row - 1 >= 0:
                if col - 1 >= 0 and self.grid[row - 1][col - 1] is None:
                    moves.append((row - 1, col - 1))
                if col + 1 < 8 and self.grid[row - 1][col + 1] is None:
                    moves.append((row - 1, col + 1))

        return moves

    def move_piece(self, from_row, from_col, to_row, to_col):
        # move piece (from_row, from_col) do (to_row, to_col)
        self.grid[to_row][to_col] = self.grid[from_row][from_col]
        self.grid[from_row][from_col] = None
        # place to add additional rules...

    def remove_piece(self, row, col):
        self.grid[row][col] = None

    def perform_capture(self, from_pos, to_pos):
        fr, fc = self.position_to_coords(from_pos)
        tr, tc = self.position_to_coords(to_pos)

        # Wylicz pole środkowe
        mr, mc = (fr + tr) // 2, (fc + tc) // 2
        print(f"Bicie! Usuwam pionek przeciwnika z pola ({mr}, {mc})")

        # Usuwamy pionek przeciwnika
        self.remove_piece(mr, mc)

        # Przenosimy nasz pionek
        self.move_piece(fr, fc, tr, tc)
        print(f"Pionek przeniesiony z ({fr}, {fc}) na ({tr}, {tc})")
