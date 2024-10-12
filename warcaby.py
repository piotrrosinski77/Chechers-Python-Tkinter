import tkinter as tk
from tkinter import *
from tkinter import PhotoImage

# Klasa Board przechowuje stan planszy
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

# Klasa CheckersApp odpowiada za interfejs użytkownika
class CheckersApp:
    def __init__(self, master):
        self.master = master
        self.board = Board()  # Inicjalizacja planszy
        self.create_widgets()

    def create_widgets(self):
        # Tworzenie płótna o rozmiarach 600x600
        self.canvas = tk.Canvas(self.master, width=600, height=600)
        self.canvas.pack()

        # Rysowanie planszy
        self.draw_board()

        # Rysowanie pionków
        self.draw_pieces()

    def draw_board(self):
        # Rysowanie szachownicy, gdzie każde pole ma rozmiar 75x75 (600 / 8)
        for row in range(8):
            for col in range(8):
                color = 'white' if (row + col) % 2 == 0 else 'black'
                self.canvas.create_rectangle(col * 75, row * 75,
                                              (col + 1) * 75, (row + 1) * 75,
                                              fill=color)

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

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('600x600')  # Ustawienie rozmiaru okna na 600x600
    root.title("Warcaby")
    icon_path = 'img/icon.png'  # Upewnij się, że ta ścieżka jest poprawna
    icon_image = PhotoImage(file=icon_path)  # Tworzenie instancji PhotoImage
    root.call('wm', 'iconphoto', root._w, icon_image)  # Ustawienie ikony
    app = CheckersApp(root)
    root.mainloop()