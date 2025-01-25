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

    """
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
    """

    def get_possible_moves(self, row, col):
        piece = self.grid[row][col]
        if piece is None:
            return []

        directions = []
        if piece == "W":
            directions += [(-1, -1), (-1, 1)]
        elif piece == "B":
            directions += [(1, -1), (1, 1)]
        elif piece == "WK" or piece == "BK":
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        moves = []

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if self.grid[r][c] is None:
                    moves.append((r, c))
                    if piece == "WK" or piece == "BK":
                        r += dr
                        c += dc
                    else:
                        break
                elif self.grid[r][c] != piece:
                    r2, c2 = r + dr, c + dc
                    if 0 <= r2 < 8 and 0 <= c2 < 8 and self.grid[r2][c2] is None:
                        moves.append((r2, c2))
                    break
                else:
                    break
        return moves

    def move_piece(self, from_row, from_col, to_row, to_col):
        # move piece (from_row, from_col) do (to_row, to_col)
        self.grid[to_row][to_col] = self.grid[from_row][from_col]
        self.grid[from_row][from_col] = None
        # place to add additional rules...
        '''
        if piece_color == "B" and to_row == 7:
            self.board.grid[to_row][to_col] = "BK"
            print(f"Promoting black piece at {to_row, to_col} to king")
        '''
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

    def get_possible_captures(self, row, col):
        piece = self.grid[row][col]
        # if piece != "W":
        #   return []

        if piece is None:
            return []

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        captures = []

        for dr, dc in directions:
            mid_r, mid_c = row + dr, col + dc
            dest_r, dest_c = row + 2 * dr, col + 2 * dc

            if (
                0 <= mid_r < 8
                and 0 <= mid_c < 8
                and 0 <= dest_r < 8
                and 0 <= dest_c < 8
            ):
                mid_piece = self.grid[mid_r][mid_c]
                if (
                    mid_piece
                    and mid_piece != piece
                    and self.grid[dest_r][dest_c] is None
                ):
                    captures.append((dest_r, dest_c))

            if piece == "WK" or piece == "BK":
                mid_r += dr
                mid_c += dc
                dest_r += 2 * dr
                dest_c += 2 * dc

                for dr, dc in directions:
                    if (0 <= mid_r < 8 and 0 <= mid_c < 8 and 0 <= dest_r < 8 and 0 <= dest_c < 8):
                        mid_piece = self.grid[mid_r][mid_c]
                    if (
                        mid_piece
                        and mid_piece != piece
                        and self.grid[dest_r][dest_c] is None
                    ):
                        captures.append((dest_r, dest_c))
                        break
        return captures
        """
            if (
                0 <= mid_r < 8
                and 0 <= mid_c < 8
                and 0 <= dest_r < 8
                and 0 <= dest_c < 8
            ):
                mid_piece = self.grid[mid_r][mid_c]
                if (
                    mid_piece
                    and mid_piece != piece
                    and self.grid[dest_r][dest_c] is None
                ):
                    captures.append((dest_r, dest_c))

            if piece == "WK" or piece == "BK":
                mid_r += dr
                mid_c += dc
                dest_r += 2 * dr
                dest_c += 2 * dc
                captures.append((dest_r, dest_c))
        return captures
"""
