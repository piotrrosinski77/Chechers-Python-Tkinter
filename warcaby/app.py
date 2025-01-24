import tkinter as tk
from tkinter import PhotoImage
from .board import Board
from .data import data_loader
from .ai import CheckersAIModel
import math


class CheckersApp:
    def __init__(self, master):

        self.master = master
        self.master.configure(bg="black")
        self.game_label = tk.Label(
            self.master,
            text="Click on a white piece to start the game!🚀",
            font=("Helvetica", 16, "bold italic"),
            fg="#FFD700",
            bg="#2C2C2C",
            relief="ridge",
            bd=4,
            padx=8,
            pady=4,
        )

        if self.game_label.winfo_exists():
            self.animate_label()
        self.game_label.pack()
        self.board = Board()
        self.selected_piece = None
        self.possible_moves = []
        self.player_turn = True
        self.last_computer_move = None
        self.game_runs = False

        self.model = CheckersAIModel()
        self.historical_moves = data_loader()
        self.current_move = 0

        self.create_widgets()
        self.train_model()

    def wait(self):
        pass

    def animate_label(self):
        if self.game_label and self.game_label.winfo_exists():
            current_color = self.game_label.cget("fg")
            next_color = "gold" if current_color == "orange" else "orange"
            self.game_label.config(fg=next_color)
            self.master.after(250, self.animate_label)

    def update_game_label(self):
        if self.player_turn:
            self.game_label.config(text="Player's turn")
        else:
            self.game_label.config(text="Computer's turn")

    def game_over(self, winner):
        self.game_label.config(text=f"Game Over! {winner} wins!")
        # self.game_label.place(relx=0.5, rely=0.5, anchor="center")

    def check_game_over(self):
        white_pieces = sum(row.count("W") for row in self.board.grid)
        black_pieces = sum(row.count("B") for row in self.board.grid)

        if white_pieces == 0:
            self.game_over("Black")
            return True
        elif black_pieces == 0:
            self.game_over("White")
            return True

        if self.player_turn:
            possible_moves = any(
                self.board.get_possible_moves(row, col)
                for row in range(8)
                for col in range(8)
                if self.board.grid[row][col] == "W"
            )
            possible_captures = any(
                self.board.get_possible_captures(row, col)
                for row in range(8)
                for col in range(8)
                if self.board.grid[row][col] == "W"
            )
        else:
            possible_moves = any(
                self.board.get_possible_moves(row, col)
                for row in range(8)
                for col in range(8)
                if self.board.grid[row][col] == "B"
            )
            possible_captures = any(
                self.board.get_possible_captures(row, col)
                for row in range(8)
                for col in range(8)
                if self.board.grid[row][col] == "B"
            )

        if not possible_moves and not possible_captures:
            winner = "Black" if self.player_turn else "White"
            self.game_over(winner)
            return True

        return False

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=600, height=600)
        self.canvas.pack()

        self.draw_board()
        self.draw_pieces()

        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "black"
                self.canvas.create_rectangle(
                    col * 75, row * 75, (col + 1) * 75, (row + 1) * 75, fill=color
                )

                if self.selected_piece and (row, col) in self.possible_moves:
                    self.canvas.create_rectangle(
                        col * 75,
                        row * 75,
                        (col + 1) * 75,
                        (row + 1) * 75,
                        fill="lime",
                        stipple="gray50",
                    )

                if self.selected_piece and (row, col) in self.possible_captures:
                    self.canvas.create_rectangle(
                        col * 75,
                        row * 75,
                        (col + 1) * 75,
                        (row + 1) * 75,
                        fill="red",
                        stipple="gray50",
                    )

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece is not None:
                    x = col * 75 + 37.5
                    y = row * 75 + 37.5
                    if piece == "B":
                        self.draw_3d_piece(x, y, "black", "darkgray")
                    else:
                        self.draw_3d_piece(x, y, "white", "lightgray")

    def draw_3d_piece(self, x, y, color, shadow_color):
        self.canvas.create_oval(
            x - 30, y - 30, x + 30, y + 30, fill=shadow_color, outline=shadow_color
        )
        self.canvas.create_oval(
            x - 27, y - 27, x + 27, y + 27, fill=color, outline="black"
        )

    def on_click(self, event):

        if self.game_label.winfo_exists():
            self.update_game_label()

        if not self.player_turn:
            print("Computer's turn - please wait...")
            return

        row = event.y // 75
        col = event.x // 75

        if (
            row < 0
            or row >= len(self.board.grid)
            or col < 0
            or col >= len(self.board.grid[row])
        ):
            return

        clicked_piece = self.board.grid[row][col]

        if clicked_piece == "W":
            self.selected_piece = (row, col)
            self.possible_moves = self.board.get_possible_moves(row, col)
            self.possible_captures = self.board.get_possible_captures(row, col)
            print(f"Player selected piece at: {self.selected_piece}")
            print(f"with possible moves: {self.possible_moves}")
            print(f"with possible captures: {self.possible_captures}")

        if self.selected_piece:
            if (row, col) in self.possible_captures:
                old_row, old_col = self.selected_piece
                self.board.move_piece(old_row, old_col, row, col)

                # Znalezione bicie
                capture_row = (old_row + row) // 2
                capture_col = (old_col + col) // 2
                self.board.remove_piece(capture_row, capture_col)
                print(f"Captured piece at ({capture_row}, {capture_col})")
                self.possible_moves = []

                self.selected_piece = (row, col)
                self.possible_captures = self.board.get_possible_captures(row, col)

                if self.possible_captures:
                    print(f"Double capture possible at {self.possible_captures}")
                    self.draw_board()
                    self.draw_pieces()
                    return

                self.selected_piece = None
                self.possible_moves = []
                self.possible_captures = []

                if self.check_game_over():
                    return

                self.player_turn = False
                self.update_game_label()
                print("Player's move completed, switching to computer's turn.")
                self.draw_board()
                self.draw_pieces()

                self.master.after(2000, self.handle_computer_move)
            elif (row, col) in self.possible_moves:
                old_row, old_col = self.selected_piece
                self.board.move_piece(old_row, old_col, row, col)

                self.selected_piece = None
                self.possible_moves = []
                self.possible_captures = []

                if self.check_game_over():
                    return

                self.player_turn = False
                self.update_game_label()
                print("Player's move completed, switching to computer's turn.")
                self.draw_board()
                self.draw_pieces()

                self.master.after(2000, self.handle_computer_move)

        self.draw_board()
        self.draw_pieces()

    def position_to_coords(self, position):
        row = (position - 1) // 4
        col = ((position - 1) % 4) * 2 + (1 if (row % 2 == 0) else 0)
        print(f"Converted position {position} to coordinates ({row}, {col})")
        return row, col

    def handle_computer_move(self):
        def make_move():
            move = self.model.generate_valid_move(
                self.board.grid, self.last_computer_move
            )
            print(f"Computer's move: {move}")
            self.process_move(move, "B")
            self.current_move += 1

            if self.check_game_over():
                return

            if "-" in move:
                from_pos, to_pos = map(int, move.split("-"))
            elif "x" in move:
                from_pos, to_pos = map(int, move.split("x"))

            from_row, from_col = self.position_to_coords(from_pos)
            to_row, to_col = self.position_to_coords(to_pos)

            self.possible_captures = self.board.get_possible_captures(to_row, to_col)
            print(f"Possible captures after computer's move: {self.possible_captures}")

            if self.possible_captures:
                self.master.after(2000, make_move)
            else:
                self.player_turn = True
                self.update_game_label()
                print("Computer's move completed, switching to player's turn.")
                self.draw_board()
                self.draw_pieces()

        make_move()

    def process_move(self, segment, piece_color):
        print(f"Processing move segment: {segment} for piece color {piece_color}")

        if isinstance(segment, list):
            for part in segment:
                self.process_single_move(part, piece_color)
        else:
            self.process_single_move(segment, piece_color)

    def train_model(self):
        self.model.train_model(self.historical_moves)

    def process_single_move(self, move, piece_color):
        if "x" in move:

            positions = move.split("x")
            from_pos = int(positions[0])

            for to_pos_str in positions[1:]:

                to_pos = int(to_pos_str)

                if from_pos in (
                    5,
                    6,
                    7,
                    8,
                    13,
                    14,
                    15,
                    16,
                    21,
                    22,
                    23,
                    24,
                    29,
                    30,
                    31,
                    32,
                ):

                    capture_pos = int(math.floor((from_pos + to_pos) / 2))

                else:

                    capture_pos = int(math.ceil((from_pos + to_pos) / 2))

                capture_coords = self.position_to_coords(capture_pos)

                if piece_color == "B":
                    print(f"Removing captured piece at {capture_coords}")
                    self.board.remove_piece(capture_coords[0], capture_coords[1])

                from_coords = self.position_to_coords(from_pos)
                to_coords = self.position_to_coords(to_pos)

                self.board.move_piece(
                    from_coords[0], from_coords[1], to_coords[0], to_coords[1]
                )
                from_pos = to_pos
        else:
            from_pos, to_pos = map(int, move.split("-"))
            from_coords = self.position_to_coords(from_pos)
            to_coords = self.position_to_coords(to_pos)
            self.board.move_piece(
                from_coords[0], from_coords[1], to_coords[0], to_coords[1]
            )

        if piece_color == "B":
            self.last_computer_move = (from_pos, to_pos)

        self.draw_board()
        self.draw_pieces()


# TO DO:
# IMPORTANT!!!
###DONE#### - Add a way for the player to remove a piece from the board
###DONE### - Add a way for the player to move back not only forward

# optional:
# - Add a way for the player to reset the board to its initial state
# - Add a way for the player to undo the last move
# - Add a way for the player to redo the last move
# - Add a way for the player to save the current game state to a file
# - Add a way for the player to load a game state from a file
###DONE### - Change the color of the possible moves (it's much too dark)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("675x675")
    root.title("Checkers")
    icon_path = "img/icon.png"
    icon_image = PhotoImage(file=icon_path)
    root.call("wm", "iconphoto", root._w, icon_image)
    app = CheckersApp(root)
    root.mainloop()
