class Board:

    def __init__(self):
        # board 8x8, B = black, W = white
        # self.checkersAIModel = CheckersAIModel()
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

    def position_to_coords(self, pos):
        if not (1 <= pos <= 64):
            raise ValueError(
                # f"Nieprawidłowy numer pola: {pos}. Musi być w zakresie 1–64."
                f"Invalid field number: {pos}. Must be in the range 1–64."
            )

        r = (pos - 1) // 4
        c = ((pos - 1) % 4) * 2 + (1 if r % 2 == 0 else 0)
        return r, c
