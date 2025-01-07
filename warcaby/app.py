import tkinter as tk
from tkinter import PhotoImage
from .board import Board

# Assuming both scripts are in the same directory
from .data import data_loader

from .ai import CheckersAIModel  # Importuj klasę z właściwego modułu

# import numpy as np


class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()
        self.selected_piece = None
        self.possible_moves = []
        self.player_turn = (
            # True if it's the player's turn, False if it's the computer's turn
            True
        )

        # Load historical moves using the data_loader function
        self.model = CheckersAIModel()
        self.historical_moves = data_loader()
        self.current_move = 0

        self.create_widgets()

        # Train the model with historical moves
        self.train_model()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=600, height=600)
        self.canvas.pack()

        self.draw_board()
        self.draw_pieces()

        # Bind the left mouse click to the on_click event
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "black"
                self.canvas.create_rectangle(
                    col * 75, row * 75, (col + 1) * 75,
                    (row + 1) * 75, fill=color
                )

                # Highlight possible moves in green
                if self.selected_piece and (row, col) in self.possible_moves:
                    self.canvas.create_rectangle(
                        col * 75,
                        row * 75,
                        (col + 1) * 75,
                        (row + 1) * 75,
                        fill="green",
                        stipple="gray50",
                    )

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece is not None:
                    x = col * 75 + 37.5  # center x-axis
                    y = row * 75 + 37.5  # center y-axis
                    if piece == "B":
                        self.draw_3d_piece(x, y, "black", "darkgray")
                    else:
                        self.draw_3d_piece(x, y, "white", "lightgray")

    def draw_3d_piece(self, x, y, color, shadow_color):
        self.canvas.create_oval(
            x - 30, y - 30, x + 30, y + 30, 
            fill=shadow_color, outline=shadow_color
        )
        self.canvas.create_oval(
            x - 27, y - 27, x + 27, y + 27, fill=color, outline="black"
        )

    def on_click(self, event):
        # Only allow the player to interact on their turn
        if not self.player_turn:
            print("Computer's turn - please wait.")  # Debugging message
            return

        row = event.y // 75
        col = event.x // 75

        if (
            row < 0
            or row >= len(self.board.grid)
            or col < 0
            or col >= len(self.board.grid[row])
        ):
            return  # Ignore clicks outside the board

        clicked_piece = self.board.grid[row][col]

        # Only allow selecting white pieces for the player
        if clicked_piece == "W":
            self.selected_piece = (row, col)
            self.possible_moves = self.board.get_possible_moves(row, col)
            print(f"Player selected piece at {self.selected_piece}")
            print(f"with moves {self.possible_moves}")
            # Debug output
        elif self.selected_piece and (row, col) in self.possible_moves:
            # Execute player's move
            old_row, old_col = self.selected_piece
            self.board.grid[row][col] = "W"
            self.board.grid[old_row][old_col] = None

            # Reset selection and moves
            self.selected_piece = None
            self.possible_moves = []

            # After player move, switch turn to the computer
            self.player_turn = False
            print(
                "Player's move completed, switching to computer's turn."
            )  # Debug output
            # self.handle_computer_move()
            self.draw_board()
            self.draw_pieces()

            # Trigger computer's move after the player
            self.master.after(1000, self.handle_computer_move)

        self.draw_board()
        self.draw_pieces()

    def position_to_coords(self, position):
        row = (position - 1) // 4
        col = ((position - 1) % 4) * 2 + (1 if row % 2 == 0 else 0)
        print(
            f"Converted position {position} to coordinates ({row}, {col})"
        )  # Debug output
        return row, col

    def handle_computer_move(self):
        if self.current_move < len(self.historical_moves):
            move = self.model.generate_valid_move(self.board.grid)
            print(f"Computer's move: {move}")  # Debug output
            self.process_move(move, "B")
            self.current_move += 1

            # After computer's move, switch back to player
            self.player_turn = True
            print(
                "Computer's move completed, switching to player's turn."
            )  # Debug output
            self.draw_board()
            self.draw_pieces()

    def process_move(self, segment, piece_color):
        print(
            f"Processing move segment: {segment} for piece color {piece_color}"
        )  # Debugging move processing

        if isinstance(segment, list):
            for part in segment:
                self.process_single_move(part, piece_color)
        else:
            self.process_single_move(segment, piece_color)

    def train_model(self):
        # Trening modelu z użyciem historycznych ruchów
        self.model.train_model(self.historical_moves)

    def process_single_move(self, move, piece_color):
        if "x" in move:
            # Multi-capture move
            positions = move.split("x")
            from_pos = int(positions[0])
            for to_pos_str in positions[1:]:
                to_pos = int(to_pos_str)

                # Calculate midpoint for the captured piece
                capture_pos = (from_pos + to_pos) // 2
                capture_coords = self.position_to_coords(capture_pos)

                if (
                    piece_color == "B"
                ):  # Only remove opponent pieces during computer's move
                    print(
                        f"Removing captured piece at {capture_coords}"
                    )  # Debug output
                    self.board.remove_piece(
                        capture_coords[0], capture_coords[1])

                from_coords = self.position_to_coords(from_pos)
                to_coords = self.position_to_coords(to_pos)

                self.board.move_piece(
                    from_coords[0], from_coords[1], to_coords[0], to_coords[1]
                )
                from_pos = to_pos
        else:
            # Regular move without capture
            from_pos, to_pos = map(int, move.split("-"))
            from_coords = self.position_to_coords(from_pos)
            to_coords = self.position_to_coords(to_pos)
            self.board.move_piece(
                from_coords[0], from_coords[1], to_coords[0], to_coords[1]
            )

        self.draw_board()
        self.draw_pieces()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Checkers")
    icon_path = "img/icon.png"
    icon_image = PhotoImage(file=icon_path)
    root.call("wm", "iconphoto", root._w, icon_image)
    app = CheckersApp(root)
    root.mainloop()