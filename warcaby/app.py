"""
import tkinter as tk
import random
from tkinter import PhotoImage
from .board import Board
from .data import data_loader

# CheckersApp is responsible for GUI
class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()
        self.selected_piece = None
        self.possible_moves = []
        self.canvas = tk.Canvas(self.master, width=600, height=600)
        self.canvas.pack()
        self.draw_board()
        self.draw_pieces()
        self.canvas.bind("<Button-1>", self.on_click)
        self.historical_games = data_loader()  # load historical data
       
       
    def __init__(self, master):
        self.master = master
        self.board = Board() 
        self.create_widgets()

    def create_widgets(self):
        # size 600x600
        self.canvas = tk.Canvas(self.master, width=600, height=600)
        self.canvas.pack()

        self.draw_board()

        self.draw_pieces() 
        
def on_click(self, event):
    row = event.y // 75
    col = event.x // 75
    
    # Ensure the click is within the board limits
    if row < 0 or row >= len(self.board.grid) or col < 0 or col >= len(self.board.grid[row]):
        return  # Ignore clicks outside the board

    clicked_piece = self.board.grid[row][col]

    if clicked_piece and clicked_piece == 'W':  # Check if it's a white piece
        self.selected_piece = (row, col)
        self.possible_moves = self.board.get_possible_moves(row, col)
        self.draw_board()
        self.draw_pieces()
    elif (row, col) in self.possible_moves:
        # Move the piece to the selected position
        self.board.move_piece(self.selected_piece[0], self.selected_piece[1], row, col)
        self.selected_piece = None
        self.possible_moves = []

        # Let the computer take its turn
        self.handle_computer_move()

    def draw_board(self):
        # each square is 75x75 (600 / 8)
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                color = 'white' if (row + col) % 2 == 0 else 'black'
                self.canvas.create_rectangle(col * 75, row * 75,
                                              (col + 1) * 75, (row + 1) * 75,
                                              fill=color)
                # Zaznacz możliwe ruchy na planszy, tylko dla białych pionków
                if self.selected_piece and self.board.grid[self.selected_piece[0]][self.selected_piece[1]] == 'W':
                    if (row, col) in self.possible_moves:
                        self.canvas.create_rectangle(col * 75, row * 75,
                                                      (col + 1) * 75, (row + 1) * 75,
                                                      fill='green', stipple='gray50')

    def draw_pieces(self):
        # Rysowanie pionków na planszy z efektem 3D
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece is not None:
                    x = col * 75 + 37.5  # Środek pola w osi x
                    y = row * 75 + 37.5  # Środek pola w osi y
                    if piece == 'B':
                        self.draw_3d_piece(x, y, 'black', 'darkgray')
                    else:
                        self.draw_3d_piece(x, y, 'white', 'lightgray')

    def draw_3d_piece(self, x, y, color, shadow_color):
        # Rysowanie pionka z efektem 3D
        # Pionek z cieniem
        self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=shadow_color, outline=shadow_color)
        # Pionek główny
        self.canvas.create_oval(x - 27, y - 27, x + 27, y + 27, fill=color, outline='black')

def handle_computer_move(self):
    computer_move = self.get_computer_move()
    if computer_move:
        from_row, from_col, (to_row, to_col) = computer_move
        self.board.move_piece(from_row, from_col, to_row, to_col)

    # Draw the board and pieces after all moves
    self.draw_board()
    self.draw_pieces()

def get_computer_move(self):
    # Load historical games if not already done
    if not hasattr(self, 'historical_games'):
        self.historical_games = data_loader()

    # Randomly select a game and a move
    import random
    random_game = random.choice(self.historical_games)
    random_move = random.choice(random_game)

    # Extract the starting and ending coordinates
    from_row, from_col = random_move[0]
    to_row, to_col = random_move[1]

    # Ensure the move is valid before returning it
    if self.board.is_valid_move(from_row, from_col, to_row, to_col):
        return (from_row, from_col, (to_row, to_col))
    else:
        return None  # If the move is not valid, return None



# run the app
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Warcaby")
    icon_path = "img/icon.png"
    icon_image = PhotoImage(file=icon_path))
    root.call("wm", "iconphoto", root._w, icon_image)
    app = CheckersApp(root)
    root.mainloop()

class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()
        self.selected_piece = None
        self.possible_moves = []  
        self.historical_games = data_loader()
        self.create_widgets()

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
                color = 'white' if (row + col) % 2 == 0 else 'black'
                self.canvas.create_rectangle(col * 75, row * 75,
                                              (col + 1) * 75, (row + 1) * 75,
                                              fill=color)
                if self.selected_piece and self.board.grid[self.selected_piece[0]][self.selected_piece[1]] == 'W':
                    if (row, col) in self.possible_moves:
                        self.canvas.create_rectangle(col * 75, row * 75,
                                                      (col + 1) * 75, (row + 1) * 75,
                                                      fill='green', stipple='gray50')

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece is not None:
                    x = col * 75 + 37.5  # Środek pola w osi x
                    y = row * 75 + 37.5  # Środek pola w osi y
                    if piece == 'B':
                        self.draw_3d_piece(x, y, 'black', 'darkgray')
                    else:
                        self.draw_3d_piece(x, y, 'white', 'lightgray')

    def draw_3d_piece(self, x, y, color, shadow_color):
        self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=shadow_color, outline=shadow_color)
        # Pionek główny
        self.canvas.create_oval(x - 27, y - 27, x + 27, y + 27, fill=color, outline='black')

def on_click(self, event):
    row = event.y // 75
    col = event.x // 75
    clicked_piece = self.board.grid[row][col]

    if clicked_piece:
        if clicked_piece == 'W':
            self.selected_piece = (row, col)
            self.possible_moves = self.board.get_possible_moves(row, col)
        else:
            self.selected_piece = None
            self.possible_moves = []
    elif self.selected_piece and (row, col) in self.possible_moves:
        old_row, old_col = self.selected_piece
        self.board.grid[row][col] = 'W' 
        self.board.grid[old_row][old_col] = None

        self.selected_piece = None
        self.possible_moves = []

        self.draw_board()
        self.draw_pieces()

        self.handle_computer_move()

def handle_computer_move(self):
    computer_move = self.get_computer_move()

    if computer_move:
        from_row, from_col, (to_row, to_col) = computer_move
        # Sprawdź czy ruch jest poprawny zanim go wykonasz
        if self.board.is_valid_move(from_row, from_col, to_row, to_col):
            self.board.move_piece(from_row, from_col, to_row, to_col)
        
    self.draw_board()
    self.draw_pieces()

def get_computer_move(self):
    if not hasattr(self, 'historical_games'):
        self.historical_games = data_loader()

    import random
    random_game = random.choice(self.historical_games)
    random_move = random.choice(random_game)

    from_row, from_col = random_move[0]
    to_row, to_col = random_move[1]


    if self.board.is_valid_move(from_row, from_col, to_row, to_col):
        return (from_row, from_col, (to_row, to_col))
    else:
        return None

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Warcaby")
    icon_path = "img/icon.png"  
    icon_image = PhotoImage(file=icon_path)
    root.call("wm", "iconphoto", root._w, icon_image)  
    app = CheckersApp(root)
    root.mainloop()


import tkinter as tk
import random
from tkinter import PhotoImage
from .board import Board
from .data import data_loader


class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()  
        self.selected_piece = None  
        self.possible_moves = []
        self.historical_games = data_loader()
        self.create_widgets()

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
                color = 'white' if (row + col) % 2 == 0 else 'black'
                self.canvas.create_rectangle(col * 75, row * 75,
                                              (col + 1) * 75, (row + 1) * 75,
                                              fill=color)
                if self.selected_piece and self.board.grid[self.selected_piece[0]][self.selected_piece[1]] == 'W':
                    if (row, col) in self.possible_moves:
                        self.canvas.create_rectangle(col * 75, row * 75,
                                                      (col + 1) * 75, (row + 1) * 75,
                                                      fill='green', stipple='gray50')

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece is not None:
                    x = col * 75 + 37.5  # Środek pola w osi x
                    y = row * 75 + 37.5  # Środek pola w osi y
                    if piece == 'B':
                        self.draw_3d_piece(x, y, 'black', 'darkgray')
                    else:
                        self.draw_3d_piece(x, y, 'white', 'lightgray')

    def draw_3d_piece(self, x, y, color, shadow_color):
        # Pionek z cieniem
        self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=shadow_color, outline=shadow_color)
        self.canvas.create_oval(x - 27, y - 27, x + 27, y + 27, fill=color, outline='black')

    def on_click(self, event):
        row = event.y // 75
        col = event.x // 75

        # Ensure the click is within the board limits
        if row < 0 or row >= len(self.board.grid) or col < 0 or col >= len(self.board.grid[row]):
            return  # Ignore clicks outside the board

        clicked_piece = self.board.grid[row][col]

        if clicked_piece:
            if clicked_piece == 'W':
                self.selected_piece = (row, col)
                self.possible_moves = self.board.get_possible_moves(row, col)
            else:
                self.selected_piece = None
                self.possible_moves = []
        elif self.selected_piece and (row, col) in self.possible_moves:
            old_row, old_col = self.selected_piece
            self.board.grid[row][col] = 'W' 
            self.board.grid[old_row][old_col] = None

            self.selected_piece = None
            self.possible_moves = []

            self.draw_board()
            self.draw_pieces()

            self.handle_computer_move()

    def handle_computer_move(self):
        computer_move = self.get_computer_move()

        if computer_move:
            from_row, from_col, (to_row, to_col) = computer_move
            if self.board.is_valid_move(from_row, from_col, to_row, to_col):
                self.board.move_piece(from_row, from_col, to_row, to_col)

        self.draw_board()
        self.draw_pieces()

    def get_computer_move(self):
        if not hasattr(self, 'historical_games'):
            self.historical_games = data_loader()

        random_game = random.choice(self.historical_games)
        random_move = random.choice(random_game)

        from_row, from_col = random_move[0]
        to_row, to_col = random_move[1]

        if self.board.is_valid_move(from_row, from_col, to_row, to_col):
            return (from_row, from_col, (to_row, to_col))
        else:
            return None


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Warcaby")
    icon_path = "img/icon.png" 
    icon_image = PhotoImage(file=icon_path)
    root.call("wm", "iconphoto", root._w, icon_image)
    app = CheckersApp(root)
    root.mainloop()

import tkinter as tk
import random
from tkinter import PhotoImage
from .board import Board
from .data import data_loader



class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()  
        self.selected_piece = None  
        self.possible_moves = []    
        self.historical_games = data_loader() 
        self.create_widgets()

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
                color = 'white' if (row + col) % 2 == 0 else 'black'
                self.canvas.create_rectangle(col * 75, row * 75,
                                              (col + 1) * 75, (row + 1) * 75,
                                              fill=color)
                if self.selected_piece and (row, col) in self.possible_moves:
                    self.canvas.create_rectangle(col * 75, row * 75,
                                                  (col + 1) * 75, (row + 1) * 75,
                                                  fill='green', stipple='gray50')

    def draw_pieces(self):
        # Rysowanie pionków na planszy z efektem 3D
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece is not None:
                    x = col * 75 + 37.5  # Środek pola w osi x
                    y = row * 75 + 37.5  # Środek pola w osi y
                    if piece == 'B':
                        self.draw_3d_piece(x, y, 'black', 'darkgray')
                    else:
                        self.draw_3d_piece(x, y, 'white', 'lightgray')

    def draw_3d_piece(self, x, y, color, shadow_color):
        self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=shadow_color, outline=shadow_color)
        self.canvas.create_oval(x - 27, y - 27, x + 27, y + 27, fill=color, outline='black')

    def on_click(self, event):
        row = event.y // 75
        col = event.x // 75

        # Ensure the click is within the board limits
        if row < 0 or row >= len(self.board.grid) or col < 0 or col >= len(self.board.grid[row]):
            return  # Ignore clicks outside the board

        clicked_piece = self.board.grid[row][col]

        if clicked_piece == 'W':  # If the player clicks on a white piece
            # Select the piece and show possible moves
            self.selected_piece = (row, col)
            self.possible_moves = self.board.get_possible_moves(row, col)
        elif self.selected_piece and (row, col) in self.possible_moves:
            # If a valid move was clicked, move the piece
            old_row, old_col = self.selected_piece
            self.board.grid[row][col] = 'W' 
            self.board.grid[old_row][old_col] = None

            # Reset the selection and possible moves
            self.selected_piece = None
            self.possible_moves = []

            # Let the computer take its turn
            self.handle_computer_move()

        # Redraw the board and pieces after every click
        self.draw_board()
        self.draw_pieces()

    def handle_computer_move(self):
        # Pobierz ruch komputera
        computer_move = self.get_computer_move()

        if computer_move:
            from_row, from_col, (to_row, to_col) = computer_move
            # Sprawdź czy ruch jest poprawny zanim go wykonasz
            if self.board.is_valid_move(from_row, from_col, to_row, to_col):
                self.board.move_piece(from_row, from_col, to_row, to_col)

        # Rysuj planszę i pionki po ruchu komputera
        self.draw_board()
        self.draw_pieces()

    def get_computer_move(self):
        # Wczytaj historyczne gry, jeśli jeszcze tego nie zrobiłeś
        if not hasattr(self, 'historical_games'):
            self.historical_games = data_loader()

        random_game = random.choice(self.historical_games)
        random_move = random.choice(random_game)

        from_row, from_col = random_move[0]
        to_row, to_col = random_move[1]

        if self.board.is_valid_move(from_row, from_col, to_row, to_col):
            return (from_row, from_col, (to_row, to_col))
        else:
            return None


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Warcaby")
    icon_path = "img/icon.png"
    icon_image = PhotoImage(file=icon_path)
    root.call("wm", "iconphoto", root._w, icon_image)
    app = CheckersApp(root)
    root.mainloop()
"""

"""
import tkinter as tk
import random
from tkinter import PhotoImage
from .board import Board
from .data import data_loader  # Assuming both scripts are in the same directory

class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()
        self.selected_piece = None  
        self.possible_moves = []

        # Load historical moves using the data_loader function
        self.historical_moves = data_loader()

        # You can use self.historical_moves for analyzing or playing games

        self.current_move = 0
        self.create_widgets()

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
                color = 'white' if (row + col) % 2 == 0 else 'black'
                self.canvas.create_rectangle(col * 75, row * 75,
                                              (col + 1) * 75, (row + 1) * 75,
                                              fill=color)

                if self.selected_piece and (row, col) in self.possible_moves:
                    self.canvas.create_rectangle(col * 75, row * 75,
                                                  (col + 1) * 75, (row + 1) * 75,
                                                  fill='green', stipple='gray50')

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece is not None:
                    x = col * 75 + 37.5  # middle point axis x
                    y = row * 75 + 37.5  # middle point axis y
                    if piece == 'B':
                        self.draw_3d_piece(x, y, 'black', 'darkgray')
                    else:
                        self.draw_3d_piece(x, y, 'white', 'lightgray')

    def draw_3d_piece(self, x, y, color, shadow_color):
        self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=shadow_color, outline=shadow_color)
        self.canvas.create_oval(x - 27, y - 27, x + 27, y + 27, fill=color, outline='black')

    def on_click(self, event):
        row = event.y // 75
        col = event.x // 75

        # Ensure the click is within the board limits
        if row < 0 or row >= len(self.board.grid) or col < 0 or col >= len(self.board.grid[row]):
            return  # Ignore clicks outside the board

        clicked_piece = self.board.grid[row][col]

        if clicked_piece == 'W':  # If the player clicks on a white piece
            # Select the piece and show possible moves
            self.selected_piece = (row, col)
            self.possible_moves = self.board.get_possible_moves(row, col)
        elif self.selected_piece and (row, col) in self.possible_moves:
            # If a valid move was clicked, move the piece
            old_row, old_col = self.selected_piece
            self.board.grid[row][col] = 'W'
            self.board.grid[old_row][old_col] = None

            # Reset the selection and possible moves
            self.selected_piece = None
            self.possible_moves = []

            # Let the computer take its turn
            self.handle_computer_move()

        # Redraw the board and pieces after every click
        self.draw_board()
        self.draw_pieces()

    # Helper to convert dataset move notation (1-32) to (row, col)
    def position_to_coords(self, position):
        row = (position - 1) // 4
        col = ((position - 1) % 4) * 2 + (1 if row % 2 == 0 else 0)
        return row, col

    def handle_computer_move(self):
    # Ensure the current move is within bounds of the historical moves
        if self.current_move < len(self.historical_moves):
        # Get the next move
            move = self.historical_moves[self.current_move]

        # If the move is a list, handle it as a sequence of moves
            if isinstance(move, list):
            # Process each move in the sequence
                for segment in move:
                # If it's a capture move
                    if 'x' in segment:
                    # Split by 'x' to get the positions of each capture
                        positions = segment.split('x')
                    
                    # Process each part of the capture
                        from_pos = int(positions[0])  # The starting position for the capture
                        for to_pos_str in positions[1:]:
                            to_pos = int(to_pos_str)

                        # Calculate the captured piece position (midpoint of from_pos and to_pos)
                            capture_pos = (from_pos + to_pos) // 2  # Midpoint for the captured piece
                            capture_coords = self.position_to_coords(capture_pos)

                        # Remove the captured piece from the board
                            self.board.remove_piece(capture_coords[0], capture_coords[1])

                        # Convert positions to board coordinates
                            from_coords = self.position_to_coords(from_pos)
                            to_coords = self.position_to_coords(to_pos)

                        # Perform the move on the board
                            self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])

                        # Update from_pos for the next capture in the sequence
                            from_pos = to_pos
                    else:  # Regular move (no capture)
                        from_pos, to_pos = map(int, segment.split('-'))

                    # Convert dataset positions to board coordinates
                        from_coords = self.position_to_coords(from_pos)
                        to_coords = self.position_to_coords(to_pos)

                    # Perform the move on the board
                        self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])
            else:
            # If it's a single move string, process it
                moves = move.split('x')  # This will split the move by capture notation

            # Process each segment of the move
                from_pos = None
                for segment in moves:
                    if from_pos is None:
                        from_pos, to_pos = map(int, segment.split('-'))
                    else:  # It's a subsequent capture move
                        to_pos = int(segment)

                # Convert dataset positions to board coordinates
                    from_coords = self.position_to_coords(from_pos)
                    to_coords = self.position_to_coords(to_pos)

                # Perform the move on the board
                    self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])

                # After each capture, remove the captured piece
                    if 'x' in segment:
                        capture_pos = (from_pos + to_pos) // 2  # Midpoint for the captured piece
                        capture_coords = self.position_to_coords(capture_pos)
                        self.board.remove_piece(capture_coords[0], capture_coords[1])

                # Update the `from_pos` for the next move in the sequence
                    from_pos = to_pos

        # Increment the move counter after all segments are processed
            self.current_move += 1

    # Redraw the board and pieces to reflect the updated state
        self.draw_board()
        self.draw_pieces()
"""

"""if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Warcaby")
    app = CheckersApp(root)
    root.mainloop()
"""

"""
import tkinter as tk
import random
from tkinter import PhotoImage
from .board import Board
from .data import data_loader  # Assuming both scripts are in the same directory

class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()
        self.selected_piece = None  
        self.possible_moves = []

        # Load historical moves using the data_loader function
        self.historical_moves = data_loader()

        # You can use self.historical_moves for analyzing or playing games
        self.current_move = 0
        self.create_widgets()

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
                color = 'white' if (row + col) % 2 == 0 else 'black'
                self.canvas.create_rectangle(col * 75, row * 75,
                                              (col + 1) * 75, (row + 1) * 75,
                                              fill=color)

                if self.selected_piece and (row, col) in self.possible_moves:
                    self.canvas.create_rectangle(col * 75, row * 75,
                                                  (col + 1) * 75, (row + 1) * 75,
                                                  fill='green', stipple='gray50')

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece is not None:
                    x = col * 75 + 37.5  # middle point axis x
                    y = row * 75 + 37.5  # middle point axis y
                    if piece == 'B':
                        self.draw_3d_piece(x, y, 'black', 'darkgray')
                    else:
                        self.draw_3d_piece(x, y, 'white', 'lightgray')

    def draw_3d_piece(self, x, y, color, shadow_color):
        self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=shadow_color, outline=shadow_color)
        self.canvas.create_oval(x - 27, y - 27, x + 27, y + 27, fill=color, outline='black')

    def on_click(self, event):
        row = event.y // 75
        col = event.x // 75

        # Ensure the click is within the board limits
        if row < 0 or row >= len(self.board.grid) or col < 0 or col >= len(self.board.grid[row]):
            return  # Ignore clicks outside the board

        clicked_piece = self.board.grid[row][col]

        if clicked_piece == 'W':  # If the player clicks on a white piece
            # Select the piece and show possible moves
            self.selected_piece = (row, col)
            self.possible_moves = self.board.get_possible_moves(row, col)
        elif self.selected_piece and (row, col) in self.possible_moves:
            # If a valid move was clicked, move the piece
            old_row, old_col = self.selected_piece
            self.board.grid[row][col] = 'W'
            self.board.grid[old_row][old_col] = None

            # Reset the selection and possible moves
            self.selected_piece = None
            self.possible_moves = []

            # Let the computer take its turn
            self.handle_computer_move()

        # Redraw the board and pieces after every click
        self.draw_board()
        self.draw_pieces()

    # Helper to convert dataset move notation (1-32) to (row, col)
    def position_to_coords(self, position):
        row = (position - 1) // 4
        col = ((position - 1) % 4) * 2 + (1 if row % 2 == 0 else 0)
        return row, col

    def handle_computer_move(self):
        # Ensure the current move is within bounds of the historical moves
        if self.current_move < len(self.historical_moves):
            # Get the next move
            move = self.historical_moves[self.current_move]

            # If the move is a list, handle it as a sequence of moves
            if isinstance(move, list):
                # Process each move in the sequence
                for segment in move:
                    self.process_move(segment)
            else:
                # Single move (possibly with captures)
                self.process_move(move)

            # Increment the move counter after all segments are processed
            self.current_move += 1

            # Switch turn to the player
            self.selected_piece = None
            self.possible_moves = []
            self.draw_board()
            self.draw_pieces()

    def process_move(self, segment):
        # Process a move, handling both regular moves and captures
        if 'x' in segment:
            # Multi-capture move, split by 'x'
            positions = segment.split('x')
            from_pos = int(positions[0])
            for to_pos_str in positions[1:]:
                to_pos = int(to_pos_str)

                # Calculate the captured piece position (midpoint of from_pos and to_pos)
                capture_pos = (from_pos + to_pos) // 2  # Midpoint for the captured piece
                capture_coords = self.position_to_coords(capture_pos)

                # Remove the captured piece from the board
                self.board.remove_piece(capture_coords[0], capture_coords[1])

                # Convert positions to board coordinates
                from_coords = self.position_to_coords(from_pos)
                to_coords = self.position_to_coords(to_pos)

                # Perform the move on the board
                self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])

                # Update from_pos for the next capture in the sequence
                from_pos = to_pos
        else:
            # Regular move (no capture)
            from_pos, to_pos = map(int, segment.split('-'))

            # Convert dataset positions to board coordinates
            from_coords = self.position_to_coords(from_pos)
            to_coords = self.position_to_coords(to_pos)

            # Perform the move on the board
            self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])

        self.draw_board()
        self.draw_pieces()

"""
"""
import tkinter as tk
import random
from tkinter import PhotoImage
from .board import Board
from .data import data_loader  # Assuming both scripts are in the same directory

class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()
        self.selected_piece = None  
        self.possible_moves = []

        # Load historical moves using the data_loader function
        self.historical_moves = data_loader()

        # You can use self.historical_moves for analyzing or playing games
        self.current_move = 0
        self.create_widgets()

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
                color = 'white' if (row + col) % 2 == 0 else 'black'
                self.canvas.create_rectangle(col * 75, row * 75,
                                              (col + 1) * 75, (row + 1) * 75,
                                              fill=color)

                if self.selected_piece and (row, col) in self.possible_moves:
                    self.canvas.create_rectangle(col * 75, row * 75,
                                                  (col + 1) * 75, (row + 1) * 75,
                                                  fill='green', stipple='gray50')

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece is not None:
                    x = col * 75 + 37.5  # middle point axis x
                    y = row * 75 + 37.5  # middle point axis y
                    if piece == 'B':
                        self.draw_3d_piece(x, y, 'black', 'darkgray')
                    else:
                        self.draw_3d_piece(x, y, 'white', 'lightgray')

    def draw_3d_piece(self, x, y, color, shadow_color):
        self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=shadow_color, outline=shadow_color)
        self.canvas.create_oval(x - 27, y - 27, x + 27, y + 27, fill=color, outline='black')

    def on_click(self, event):
        row = event.y // 75
        col = event.x // 75

        # Ensure the click is within the board limits
        if row < 0 or row >= len(self.board.grid) or col < 0 or col >= len(self.board.grid[row]):
            return  # Ignore clicks outside the board

        clicked_piece = self.board.grid[row][col]

        if clicked_piece == 'W':  # If the player clicks on a white piece
            # Select the piece and show possible moves
            self.selected_piece = (row, col)
            self.possible_moves = self.board.get_possible_moves(row, col)
        elif self.selected_piece and (row, col) in self.possible_moves:
            # If a valid move was clicked, move the piece
            old_row, old_col = self.selected_piece
            self.board.grid[row][col] = 'W'
            self.board.grid[old_row][old_col] = None

            # Reset the selection and possible moves
            self.selected_piece = None
            self.possible_moves = []

            # Let the computer take its turn
            self.handle_computer_move()

        # Redraw the board and pieces after every click
        self.draw_board()
        self.draw_pieces()

    # Helper to convert dataset move notation (1-32) to (row, col)
    def position_to_coords(self, position):
        row = (position - 1) // 4
        col = ((position - 1) % 4) * 2 + (1 if row % 2 == 0 else 0)
        return row, col

    def handle_computer_move(self):
        # Ensure the current move is within bounds of the historical moves
        if self.current_move < len(self.historical_moves):
            # Get the next move
            move = self.historical_moves[self.current_move]

            # If the move is a list, handle it as a sequence of moves
            if isinstance(move, list):
                # Process each move in the sequence
                for segment in move:
                    self.process_move(segment)
            else:
                # Single move (possibly with captures)
                self.process_move(move)

            # Increment the move counter after all segments are processed
            self.current_move += 1

            # Switch turn to the player (reset selection and possible moves)
            self.selected_piece = None
            self.possible_moves = []
            self.draw_board()
            self.draw_pieces()

    def process_move(self, segment):
        print(f"Processing move: {segment}")  # Debugging move processing
        # Process a move, handling both regular moves and captures
        if 'x' in segment:
            # Multi-capture move, split by 'x'
            positions = segment.split('x')
            from_pos = int(positions[0])
            for to_pos_str in positions[1:]:
                to_pos = int(to_pos_str)

                # Calculate the captured piece position (midpoint of from_pos and to_pos)
                capture_pos = (from_pos + to_pos) // 2  # Midpoint for the captured piece
                capture_coords = self.position_to_coords(capture_pos)

                # Remove the captured piece from the board
                print(f"Removing captured piece at {capture_coords}")  # Debugging captured piece removal
                self.board.remove_piece(capture_coords[0], capture_coords[1])

                # Convert positions to board coordinates
                from_coords = self.position_to_coords(from_pos)
                to_coords = self.position_to_coords(to_pos)

                # Perform the move on the board
                self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])

                # Update from_pos for the next capture in the sequence
                from_pos = to_pos
        else:
            # Regular move (no capture)
            from_pos, to_pos = map(int, segment.split('-'))

            # Convert dataset positions to board coordinates
            from_coords = self.position_to_coords(from_pos)
            to_coords = self.position_to_coords(to_pos)

            # Perform the move on the board
            self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])

        self.draw_board()
        self.draw_pieces()
"""
'''
import tkinter as tk
import random
from tkinter import PhotoImage
from .board import Board
from .data import data_loader  # Assuming both scripts are in the same directory

class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()
        self.selected_piece = None  
        self.possible_moves = []

        # Load historical moves using the data_loader function
        self.historical_moves = data_loader()

        # You can use self.historical_moves for analyzing or playing games
        self.current_move = 0
        self.create_widgets()

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
                color = 'white' if (row + col) % 2 == 0 else 'black'
                self.canvas.create_rectangle(col * 75, row * 75,
                                              (col + 1) * 75, (row + 1) * 75,
                                              fill=color)

                if self.selected_piece and (row, col) in self.possible_moves:
                    self.canvas.create_rectangle(col * 75, row * 75,
                                                  (col + 1) * 75, (row + 1) * 75,
                                                  fill='green', stipple='gray50')

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece is not None:
                    x = col * 75 + 37.5  # middle point axis x
                    y = row * 75 + 37.5  # middle point axis y
                    if piece == 'B':
                        self.draw_3d_piece(x, y, 'black', 'darkgray')
                    else:
                        self.draw_3d_piece(x, y, 'white', 'lightgray')

    def draw_3d_piece(self, x, y, color, shadow_color):
        self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=shadow_color, outline=shadow_color)
        self.canvas.create_oval(x - 27, y - 27, x + 27, y + 27, fill=color, outline='black')

    def on_click(self, event):
        row = event.y // 75
        col = event.x // 75

        # Ensure the click is within the board limits
        if row < 0 or row >= len(self.board.grid) or col < 0 or col >= len(self.board.grid[row]):
            return  # Ignore clicks outside the board

        clicked_piece = self.board.grid[row][col]

        if clicked_piece == 'W':  # If the player clicks on a white piece
            # Select the piece and show possible moves
            self.selected_piece = (row, col)
            self.possible_moves = self.board.get_possible_moves(row, col)
        elif self.selected_piece and (row, col) in self.possible_moves:
            # If a valid move was clicked, move the piece
            old_row, old_col = self.selected_piece
            self.board.grid[row][col] = 'W'
            self.board.grid[old_row][old_col] = None

            # Reset the selection and possible moves
            self.selected_piece = None
            self.possible_moves = []

            # Let the computer take its turn
            self.handle_computer_move()

        # Redraw the board and pieces after every click
        self.draw_board()
        self.draw_pieces()

    # Helper to convert dataset move notation (1-32) to (row, col)
    def position_to_coords(self, position):
        row = (position - 1) // 4
        col = ((position - 1) % 4) * 2 + (1 if row % 2 == 0 else 0)
        return row, col

    def handle_computer_move(self):
        # Ensure the current move is within bounds of the historical moves
        if self.current_move < len(self.historical_moves):
            # Get the next move
            move = self.historical_moves[self.current_move]

            # If the move is a list, handle it as a sequence of moves
            if isinstance(move, list):
                # Process each move in the sequence
                for segment in move:
                    self.process_move(segment, 'B')  # 'B' for black (computer's piece)
            else:
                # Single move (possibly with captures)
                self.process_move(move, 'B')  # 'B' for black (computer's piece)

            # Increment the move counter after all segments are processed
            self.current_move += 1

            # Switch turn to the player (reset selection and possible moves)
            self.selected_piece = None
            self.possible_moves = []
            self.draw_board()
            self.draw_pieces()

    def process_move(self, segment, piece_color):
        """
        Processes a move or sequence of moves for a given piece color ('W' for player, 'B' for computer).
        """
        print(f"Processing move: {segment}")  # Debugging move processing
        # Process a move, handling both regular moves and captures
        if 'x' in segment:
            # Multi-capture move, split by 'x'
            positions = segment.split('x')
            from_pos = int(positions[0])
            for to_pos_str in positions[1:]:
                to_pos = int(to_pos_str)

                # Calculate the captured piece position (midpoint of from_pos and to_pos)
                capture_pos = (from_pos + to_pos) // 2  # Midpoint for the captured piece
                capture_coords = self.position_to_coords(capture_pos)

                # Remove the captured piece from the board (if it's the opponent's piece)
                if piece_color == 'B':  # Only remove black pieces during computer's turn
                    print(f"Removing captured piece at {capture_coords}")  # Debugging captured piece removal
                    self.board.remove_piece(capture_coords[0], capture_coords[1])

                # Convert positions to board coordinates
                from_coords = self.position_to_coords(from_pos)
                to_coords = self.position_to_coords(to_pos)

                # Perform the move on the board
                self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])

                # Update from_pos for the next capture in the sequence
                from_pos = to_pos
        else:
            # Regular move (no capture)
            from_pos, to_pos = map(int, segment.split('-'))

            # Convert dataset positions to board coordinates
            from_coords = self.position_to_coords(from_pos)
            to_coords = self.position_to_coords(to_pos)

            # Perform the move on the board
            self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])

        self.draw_board()
        self.draw_pieces()
'''
'''
import tkinter as tk
import random
from tkinter import PhotoImage
from .board import Board
from .data import data_loader  # Assuming both scripts are in the same directory

class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()
        self.selected_piece = None  
        self.possible_moves = []

        # Load historical moves using the data_loader function
        self.historical_moves = data_loader()

        # You can use self.historical_moves for analyzing or playing games
        self.current_move = 0
        self.create_widgets()

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
                color = 'white' if (row + col) % 2 == 0 else 'black'
                self.canvas.create_rectangle(col * 75, row * 75,
                                              (col + 1) * 75, (row + 1) * 75,
                                              fill=color)

                if self.selected_piece and (row, col) in self.possible_moves:
                    self.canvas.create_rectangle(col * 75, row * 75,
                                                  (col + 1) * 75, (row + 1) * 75,
                                                  fill='green', stipple='gray50')

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece is not None:
                    x = col * 75 + 37.5  # middle point axis x
                    y = row * 75 + 37.5  # middle point axis y
                    if piece == 'B':
                        self.draw_3d_piece(x, y, 'black', 'darkgray')
                    else:
                        self.draw_3d_piece(x, y, 'white', 'lightgray')

    def draw_3d_piece(self, x, y, color, shadow_color):
        self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=shadow_color, outline=shadow_color)
        self.canvas.create_oval(x - 27, y - 27, x + 27, y + 27, fill=color, outline='black')

    def on_click(self, event):
        row = event.y // 75
        col = event.x // 75

        # Ensure the click is within the board limits
        if row < 0 or row >= len(self.board.grid) or col < 0 or col >= len(self.board.grid[row]):
            return  # Ignore clicks outside the board

        clicked_piece = self.board.grid[row][col]

        if clicked_piece == 'W':  # If the player clicks on a white piece
            # Select the piece and show possible moves
            self.selected_piece = (row, col)
            self.possible_moves = self.board.get_possible_moves(row, col)
        elif self.selected_piece and (row, col) in self.possible_moves:
            # If a valid move was clicked, move the piece
            old_row, old_col = self.selected_piece
            self.board.grid[row][col] = 'W'
            self.board.grid[old_row][old_col] = None

            # Reset the selection and possible moves
            self.selected_piece = None
            self.possible_moves = []

            # Let the computer take its turn
            self.handle_computer_move()

        # Redraw the board and pieces after every click
        self.draw_board()
        self.draw_pieces()

    # Helper to convert dataset move notation (1-32) to (row, col)
    def position_to_coords(self, position):
        row = (position - 1) // 4
        col = ((position - 1) % 4) * 2 + (1 if row % 2 == 0 else 0)
        return row, col

    def handle_computer_move(self):
        # Ensure the current move is within bounds of the historical moves
        if self.current_move < len(self.historical_moves):
            # Get the next move (this move will always be black's move)
            move = self.historical_moves[self.current_move]

            # Process the move only if it's black's move
            if isinstance(move, list):
                # Process each move in the sequence (all should be black's moves)
                for segment in move:
                    self.process_move(segment, 'B')  # 'B' for black (computer's piece)
            else:
                # Single move (possibly with captures)
                self.process_move(move, 'B')  # 'B' for black (computer's piece)

            # Increment the move counter after all segments are processed
            self.current_move += 1

            # Switch turn to the player (reset selection and possible moves)
            self.selected_piece = None
            self.possible_moves = []
            self.draw_board()
            self.draw_pieces()

    def process_move(self, segment, piece_color):
        """
        Processes a move or sequence of moves for a given piece color ('W' for player, 'B' for computer).
        """
        print(f"Processing move: {segment}")  # Debugging move processing
        # Process a move, handling both regular moves and captures
        if 'x' in segment:
            # Multi-capture move, split by 'x'
            positions = segment.split('x')
            from_pos = int(positions[0])
            for to_pos_str in positions[1:]:
                to_pos = int(to_pos_str)

                # Calculate the captured piece position (midpoint of from_pos and to_pos)
                capture_pos = (from_pos + to_pos) // 2  # Midpoint for the captured piece
                capture_coords = self.position_to_coords(capture_pos)

                # Remove the captured piece from the board (if it's the opponent's piece)
                if piece_color == 'B':  # Only remove black pieces during computer's turn
                    print(f"Removing captured piece at {capture_coords}")  # Debugging captured piece removal
                    self.board.remove_piece(capture_coords[0], capture_coords[1])

                # Convert positions to board coordinates
                from_coords = self.position_to_coords(from_pos)
                to_coords = self.position_to_coords(to_pos)

                # Perform the move on the board
                self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])

                # Update from_pos for the next capture in the sequence
                from_pos = to_pos
        else:
            # Regular move (no capture)
            from_pos, to_pos = map(int, segment.split('-'))

            # Convert dataset positions to board coordinates
            from_coords = self.position_to_coords(from_pos)
            to_coords = self.position_to_coords(to_pos)

            # Perform the move on the board
            self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])

        self.draw_board()
        self.draw_pieces()
'''
'''
import tkinter as tk
import random
from tkinter import PhotoImage
from .board import Board
from .data import data_loader  # Assuming both scripts are in the same directory

class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()
        self.selected_piece = None  
        self.possible_moves = []

        # Load historical moves using the data_loader function
        self.historical_moves = data_loader()

        # You can use self.historical_moves for analyzing or playing games
        self.current_move = 0
        self.create_widgets()

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
                color = 'white' if (row + col) % 2 == 0 else 'black'
                self.canvas.create_rectangle(col * 75, row * 75,
                                              (col + 1) * 75, (row + 1) * 75,
                                              fill=color)

                if self.selected_piece and (row, col) in self.possible_moves:
                    self.canvas.create_rectangle(col * 75, row * 75,
                                                  (col + 1) * 75, (row + 1) * 75,
                                                  fill='green', stipple='gray50')

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece is not None:
                    x = col * 75 + 37.5  # middle point axis x
                    y = row * 75 + 37.5  # middle point axis y
                    if piece == 'B':
                        self.draw_3d_piece(x, y, 'black', 'darkgray')
                    else:
                        self.draw_3d_piece(x, y, 'white', 'lightgray')

    def draw_3d_piece(self, x, y, color, shadow_color):
        self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=shadow_color, outline=shadow_color)
        self.canvas.create_oval(x - 27, y - 27, x + 27, y + 27, fill=color, outline='black')

    def on_click(self, event):
        row = event.y // 75
        col = event.x // 75

        # Ensure the click is within the board limits
        if row < 0 or row >= len(self.board.grid) or col < 0 or col >= len(self.board.grid[row]):
            return  # Ignore clicks outside the board

        clicked_piece = self.board.grid[row][col]

        if clicked_piece == 'W':  # If the player clicks on a white piece
            # Select the piece and show possible moves
            self.selected_piece = (row, col)
            self.possible_moves = self.board.get_possible_moves(row, col)
        elif self.selected_piece and (row, col) in self.possible_moves:
            # If a valid move was clicked, move the piece
            old_row, old_col = self.selected_piece
            self.board.grid[row][col] = 'W'
            self.board.grid[old_row][old_col] = None

            # Reset the selection and possible moves
            self.selected_piece = None
            self.possible_moves = []

            # Let the computer take its turn
            self.handle_computer_move()

        # Redraw the board and pieces after every click
        self.draw_board()
        self.draw_pieces()

    # Helper to convert dataset move notation (1-32) to (row, col)
    def position_to_coords(self, position):
        row = (position - 1) // 4
        col = ((position - 1) % 4) * 2 + (1 if row % 2 == 0 else 0)
        return row, col

    def handle_computer_move(self):
        # Ensure the current move is within bounds of the historical moves
        if self.current_move < len(self.historical_moves):
            # Get the next move (this move will always be black's move)
            move = self.historical_moves[self.current_move]

            # Skip white moves: White pieces moves are at odd index (0-based)
            if self.current_move % 2 == 0:
                # This is white's move, skip it
                self.current_move += 1
                self.handle_computer_move()  # Recursively call the next move
                return

            # Process the move only if it's black's move
            if isinstance(move, list):
                # Process each move in the sequence (all should be black's moves)
                for segment in move:
                    self.process_move(segment, 'B')  # 'B' for black (computer's piece)
            else:
                # Single move (possibly with captures)
                self.process_move(move, 'B')  # 'B' for black (computer's piece)

            # Increment the move counter after all segments are processed
            self.current_move += 1

            # Switch turn to the player (reset selection and possible moves)
            self.selected_piece = None
            self.possible_moves = []
            self.draw_board()
            self.draw_pieces()

    def process_move(self, segment, piece_color):
        """
        Processes a move or sequence of moves for a given piece color ('W' for player, 'B' for computer).
        """
        print(f"Processing move: {segment}")  # Debugging move processing
        # Process a move, handling both regular moves and captures
        if 'x' in segment:
            # Multi-capture move, split by 'x'
            positions = segment.split('x')
            from_pos = int(positions[0])
            for to_pos_str in positions[1:]:
                to_pos = int(to_pos_str)

                # Calculate the captured piece position (midpoint of from_pos and to_pos)
                capture_pos = (from_pos + to_pos) // 2  # Midpoint for the captured piece
                capture_coords = self.position_to_coords(capture_pos)

                # Remove the captured piece from the board (if it's the opponent's piece)
                if piece_color == 'B':  # Only remove black pieces during computer's turn
                    print(f"Removing captured piece at {capture_coords}")  # Debugging captured piece removal
                    self.board.remove_piece(capture_coords[0], capture_coords[1])

                # Convert positions to board coordinates
                from_coords = self.position_to_coords(from_pos)
                to_coords = self.position_to_coords(to_pos)

                # Perform the move on the board
                self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])

                # Update from_pos for the next capture in the sequence
                from_pos = to_pos
        else:
            # Regular move (no capture)
            from_pos, to_pos = map(int, segment.split('-'))

            # Convert dataset positions to board coordinates
            from_coords = self.position_to_coords(from_pos)
            to_coords = self.position_to_coords(to_pos)

            # Perform the move on the board
            self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])

        self.draw_board()
        self.draw_pieces()
'''
'''
import tkinter as tk
import random
from tkinter import PhotoImage
from .board import Board
from .data import data_loader  # Assuming both scripts are in the same directory

class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()
        self.selected_piece = None  
        self.possible_moves = []

        # Load historical moves using the data_loader function
        self.historical_moves = data_loader()

        # The current move index: 0 means it's the player's turn, 1 means it's the computer's turn
        self.current_move = 0
        self.create_widgets()

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
                color = 'white' if (row + col) % 2 == 0 else 'black'
                self.canvas.create_rectangle(col * 75, row * 75,
                                              (col + 1) * 75, (row + 1) * 75,
                                              fill=color)

                if self.selected_piece and (row, col) in self.possible_moves:
                    self.canvas.create_rectangle(col * 75, row * 75,
                                                  (col + 1) * 75, (row + 1) * 75,
                                                  fill='green', stipple='gray50')

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece is not None:
                    x = col * 75 + 37.5  # middle point axis x
                    y = row * 75 + 37.5  # middle point axis y
                    if piece == 'B':
                        self.draw_3d_piece(x, y, 'black', 'darkgray')
                    else:
                        self.draw_3d_piece(x, y, 'white', 'lightgray')

    def draw_3d_piece(self, x, y, color, shadow_color):
        self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=shadow_color, outline=shadow_color)
        self.canvas.create_oval(x - 27, y - 27, x + 27, y + 27, fill=color, outline='black')

    def on_click(self, event):
        row = event.y // 75
        col = event.x // 75

        # Ensure the click is within the board limits
        if row < 0 or row >= len(self.board.grid) or col < 0 or col >= len(self.board.grid[row]):
            return  # Ignore clicks outside the board

        clicked_piece = self.board.grid[row][col]

        if clicked_piece == 'W':  # If the player clicks on a white piece
            # Select the piece and show possible moves
            self.selected_piece = (row, col)
            self.possible_moves = self.board.get_possible_moves(row, col)
        elif self.selected_piece and (row, col) in self.possible_moves:
            # If a valid move was clicked, move the piece
            old_row, old_col = self.selected_piece
            self.board.grid[row][col] = 'W'
            self.board.grid[old_row][old_col] = None

            # Reset the selection and possible moves
            self.selected_piece = None
            self.possible_moves = []

            # Let the computer take its turn after the player's move
            self.handle_computer_move()

        # Redraw the board and pieces after every click
        self.draw_board()
        self.draw_pieces()

    # Helper to convert dataset move notation (1-32) to (row, col)
    def position_to_coords(self, position):
        row = (position - 1) // 4
        col = ((position - 1) % 4) * 2 + (1 if row % 2 == 0 else 0)
        return row, col

    def handle_computer_move(self):
        # Ensure the current move is within bounds of the historical moves
        if self.current_move < len(self.historical_moves):
            # Get the next move (this will always be black's move after the player)
            move = self.historical_moves[self.current_move]

            # Skip white moves (player's moves)
            if self.current_move % 2 == 0:
                # This is white's move (player's turn), so skip it
                self.current_move += 1
                return  # The player is making this move, so don't process it

            # Process black moves (computer's move)
            print(f"Processing computer's move: {move}")  # Debugging move processing
            if isinstance(move, list):
                # Process each move in the sequence (all black's moves)
                for segment in move:
                    self.process_move(segment, 'B')  # 'B' for black (computer's piece)
            else:
                # Single move (possibly with captures)
                self.process_move(move, 'B')  # 'B' for black (computer's piece)

            # Increment the move counter after processing the move
            self.current_move += 1

            # After the computer's move, switch back to the player's turn
            self.selected_piece = None
            self.possible_moves = []
            self.draw_board()
            self.draw_pieces()

    def process_move(self, segment, piece_color):
        """
        Processes a move or sequence of moves for a given piece color ('W' for player, 'B' for computer).
        """
        print(f"Processing move: {segment}")  # Debugging move processing
        # Process a move, handling both regular moves and captures
        if 'x' in segment:
            # Multi-capture move, split by 'x'
            positions = segment.split('x')
            from_pos = int(positions[0])
            for to_pos_str in positions[1:]:
                to_pos = int(to_pos_str)

                # Calculate the captured piece position (midpoint of from_pos and to_pos)
                capture_pos = (from_pos + to_pos) // 2  # Midpoint for the captured piece
                capture_coords = self.position_to_coords(capture_pos)

                # Remove the captured piece from the board (if it's the opponent's piece)
                if piece_color == 'B':  # Only remove black pieces during computer's turn
                    print(f"Removing captured piece at {capture_coords}")  # Debugging captured piece removal
                    self.board.remove_piece(capture_coords[0], capture_coords[1])

                # Convert positions to board coordinates
                from_coords = self.position_to_coords(from_pos)
                to_coords = self.position_to_coords(to_pos)

                # Perform the move on the board
                self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])

                # Update from_pos for the next capture in the sequence
                from_pos = to_pos
        else:
            # Regular move (no capture)
            from_pos, to_pos = map(int, segment.split('-'))

            # Convert dataset positions to board coordinates
            from_coords = self.position_to_coords(from_pos)
            to_coords = self.position_to_coords(to_pos)

            # Perform the move on the board
            self.board.move_piece(from_coords[0], from_coords[1], to_coords[0], to_coords[1])

        self.draw_board()
        self.draw_pieces()
'''
'''
import tkinter as tk
from tkinter import PhotoImage
from .board import Board
from .data import data_loader  # Assuming both scripts are in the same directory


class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()
        self.selected_piece = None
        self.possible_moves = []

        # Load historical moves using the data_loader function
        self.historical_moves = data_loader()

        # Track the current move index in the dataset
        self.current_move = 0
        self.create_widgets()

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
                # Only color black squares for playable positions
                color = "white" if (row + col) % 2 == 0 else "black"
                self.canvas.create_rectangle(
                    col * 75, row * 75, (col + 1) * 75, (row + 1) * 75, fill=color
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
        # Draw 3D-like effect for the piece
        self.canvas.create_oval(
            x - 30, y - 30, x + 30, y + 30, fill=shadow_color, outline=shadow_color
        )
        self.canvas.create_oval(
            x - 27, y - 27, x + 27, y + 27, fill=color, outline="black"
        )

    def on_click(self, event):
        row = event.y // 75
        col = event.x // 75

        # Ensure the click is within the board limits
        if (
            row < 0
            or row >= len(self.board.grid)
            or col < 0
            or col >= len(self.board.grid[row])
        ):
            return  # Ignore clicks outside the board

        clicked_piece = self.board.grid[row][col]

        if clicked_piece == "W":  # If the player clicks on a white piece
            # Select the piece and show possible moves
            self.selected_piece = (row, col)
            self.possible_moves = self.board.get_possible_moves(row, col)
            print(
                f"Selected piece at {self.selected_piece} with moves {self.possible_moves}"
            )  # Debug output
        elif self.selected_piece and (row, col) in self.possible_moves:
            # If a valid move was clicked, move the piece
            old_row, old_col = self.selected_piece
            self.board.grid[row][col] = "W"
            self.board.grid[old_row][old_col] = None

            # Reset the selection and possible moves
            self.selected_piece = None
            self.possible_moves = []

            # After the player's move, let the computer make one move
            self.handle_computer_move()

        # Redraw the board and pieces after every click
        self.draw_board()
        self.draw_pieces()

    def position_to_coords(self, position):
        """
        Helper function to convert dataset notation (1-32) to (row, col).
        """
        row = (position - 1) // 4
        col = ((position - 1) % 4) * 2 + (1 if row % 2 == 0 else 0)
        print(
            f"Converted position {position} to coordinates ({row}, {col})"
        )  # Debug output
        return row, col

    def handle_computer_move(self):
        if self.current_move < len(self.historical_moves):
            move = self.historical_moves[self.current_move]

            if self.current_move % 2 == 0:
                # Player's move, so increment to the next move for computer
                self.current_move += 1
                return

            print(f"Computer's move: {move}")  # Debug output
            self.process_move(move, "B")

            self.current_move += 1

            # Reset selection and redraw after computer's move
            self.selected_piece = None
            self.possible_moves = []
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

                # Remove captured piece if opponent's piece
                if piece_color == "B":
                    print(
                        f"Removing captured piece at {capture_coords}"
                    )  # Debugging captured piece removal
                    self.board.remove_piece(capture_coords[0], capture_coords[1])

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

        # Redraw the board
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
'''
import tkinter as tk
from tkinter import PhotoImage
from .board import Board
from .data import data_loader  # Assuming both scripts are in the same directory


class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()
        self.selected_piece = None
        self.possible_moves = []
        self.player_turn = (
            True  # True if it's the player's turn, False if it's the computer's turn
        )

        # Load historical moves using the data_loader function
        self.historical_moves = data_loader()
        self.current_move = 0
        self.create_widgets()

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
                    col * 75, row * 75, (col + 1) * 75, (row + 1) * 75, fill=color
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
            x - 30, y - 30, x + 30, y + 30, fill=shadow_color, outline=shadow_color
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

        if clicked_piece == "W":  # Only allow selecting white pieces for the player
            self.selected_piece = (row, col)
            self.possible_moves = self.board.get_possible_moves(row, col)
            print(
                f"Player selected piece at {self.selected_piece} with moves {self.possible_moves}"
            )  # Debug output
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
            move = self.historical_moves[self.current_move]

            # Skip white moves in the dataset (even index = player's move)
            # if self.current_move % 2 == 0:
            # self.current_move += 1
            # return

            print(f"Computer's move: {move[0]}")  # Debug output
            self.process_move(move[0], "B")

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
                    self.board.remove_piece(capture_coords[0], capture_coords[1])

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
