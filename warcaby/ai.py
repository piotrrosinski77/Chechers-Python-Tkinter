import os
import numpy as np
import math
from .board import Board
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Input


class CheckersAIModel:
    def __init__(self):
        self.board = Board()  # Przechowywanie obiektu Board
        model_filepath = "trained_checkers_model.h5"
        if os.path.exists(model_filepath):
            self.model = self.load_model(model_filepath)
            print("Wczytano poprawnie model z pliku")
        else:
            self.model = self._create_model()
            print("Utworzono nowy model")

    def _create_model(self):
        model = Sequential(
            [
                Input(shape=(64,)),
                Dense(128, activation="relu"),
                Dense(128, activation="relu"),
                Dense(64, activation="softmax"),
            ]
        )
        model.compile(
            optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
        )
        return model

    def load_model(self, filepath):
        model = load_model(filepath)
        model.compile(
            optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
        )
        print(f"Model załadowany z pliku: {filepath}")
        return model

    def save_model(self, filepath):
        self.model.save(filepath)
        print(f"Model zapisany do pliku: {filepath}")

    def train(self, X, y, epochs=3, batch_size=32):
        print("Rozpoczynam trening modelu...")
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size)
        print("Trening zakończony!")

    def generate_valid_move(self, board_state):
        print("Rozpoczynam generowanie ruchu dla komputera...")
        board_array = self.convert_board_to_array(board_state)
        print("Tablica reprezentująca planszę:", board_array)

        predictions = self.model.predict(board_array)[0]
        print("Predykcje modelu:", predictions)

        sorted_indices = np.argsort(-predictions)
        print("Indeksy posortowane według prawdopodobieństwa:", sorted_indices)

        black_positions = self.get_black_positions(board_state)
        print("Pozycje czarnych pionków:", black_positions)

        # Sprawdź możliwe bicia
        for from_pos in black_positions:

            captures = self.get_valid_captures(board_state, from_pos)
            print(f"board_state: {board_state}", f"from_pos: {from_pos}")
            if captures:
                print(
                    f"Znaleziono możliwe bicia dla pionka na polu {from_pos}: {captures}"
                )
                return captures[0]  # Wybieramy pierwsze bicie

        # Jeśli brak bić, wykonaj standardowy ruch
        for from_pos in black_positions:
            print(f"Przetwarzam ruchy dla pionka na polu {from_pos}")
            for idx in sorted_indices:
                to_pos = idx % 64 + 1
                move = f"{from_pos}-{to_pos}"
                print(f"Sprawdzam ruch: {move}")

                if self.is_valid_move(board_state, move):
                    print("Znaleziono poprawny ruch:", move)
                    return move

        print("Nie znaleziono poprawnego ruchu.")
        raise ValueError("Nie można wygenerować prawidłowego ruchu.")

    def convert_board_to_array(self, board_state):
        board_array = np.zeros((1, 64), dtype=np.float32)
        for i, row in enumerate(board_state):
            for j, cell in enumerate(row):
                index = i * 8 + j
                if cell == "B":
                    board_array[0, index] = 1.0
                elif cell == "W":
                    board_array[0, index] = 2.0
        return board_array

    def is_valid_move(self, board, move):
        print(f"Sprawdzam poprawność ruchu: {move}")
        try:
            fp, tp = map(int, move.split("-"))
            fr, fc = self.position_to_coords(fp)
            tr, tc = self.position_to_coords(tp)
            print(f"Pola: Startowe ({fr}, {fc}), Docelowe ({tr}, {tc})")

            if board[fr][fc] != "B":
                print(
                    f"Nieprawidłowy ruch: Pole startowe {fp} nie zawiera czarnego pionka."
                )
                return False
            if not (0 <= tr < 8 and 0 <= tc < 8):
                print("Nieprawidłowy ruch: Pole docelowe poza planszą.")
                return False
            if board[tr][tc] is not None:
                print("Nieprawidłowy ruch: Pole docelowe jest zajęte.")
                return False

            # Ruch standardowy
            if abs(fr - tr) == 1 and abs(fc - tc) == 1:
                print("Ruch standardowy jest poprawny.")
                return True

            # Ruch z biciem
            if abs(fr - tr) == 2 and abs(fc - tc) == 2:
                mr, mc = (fr + tr) // 2, (fc + tc) // 2
                print(f"Pole środkowe: ({mr}, {mc})")
                if board[mr][mc] == "W":
                    print("Ruch z biciem jest poprawny.")
                    return True

            print("Nieprawidłowy ruch.")
            return False
        except ValueError as e:
            print(f"Nieprawidłowy ruch: {e}")
            return False

    def position_to_coords(self, pos):
        if not (1 <= pos <= 64):
            raise ValueError(
                f"Nieprawidłowy numer pola: {pos}. Musi być w zakresie 1–64."
            )

        r = (pos - 1) // 4
        c = ((pos - 1) % 4) * 2 + (1 if r % 2 == 0 else 0)
        return r, c

    def coords_to_position(self, row, col):
        if not (0 <= row < 8 and 0 <= col < 8):
            raise ValueError(
                f"Nieprawidłowe współrzędne: ({row}, {col}). Muszą być w zakresie 0–7."
            )

        if (row % 2 == 0 and col % 2 != 1) or (row % 2 == 1 and col % 2 != 0):
            raise ValueError(f"Pole ({row}, {col}) nie jest czarnym polem na planszy.")

        pos = row * 4 + (col // 2) + 1
        return pos

    def train_model(self, history):
        X, y = [], []

        if X and y:
            X = np.array(X)
            y = np.array(y)
            self.train(X, y, epochs=3, batch_size=32)
            self.save_model("trained_checkers_model.h5")

    def get_black_positions(self, board_state):
        print("Zaczynam identyfikację pozycji czarnych pionków...")
        black_positions = []
        for row in range(8):
            for col in range(8):
                if board_state[row][col] == "B":
                    pos = self.coords_to_position(row, col)
                    black_positions.append(pos)
                    print(
                        f"Znaleziono czarny pionek na polu: {pos} (współrzędne: {row}, {col})"
                    )
        print(f"Wszystkie pozycje czarnych pionków: {black_positions}")
        return black_positions

    def get_valid_captures(self, board, from_pos):
        fr, fc = self.position_to_coords(from_pos)
        captures = []

        # Przykładowa logika sprawdzania bicia
        directions = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        for dr, dc in directions:
            tr = fr + dr
            tc = fc + dc
            mr = (fr + tr) // 2
            mc = (fc + tc) // 2

            # Sprawdzamy, czy w polu (mr, mc) jest przeciwnik, i czy (tr, tc) jest puste
            if 0 <= tr < 8 and 0 <= tc < 8:
                if (
                    board[fr][fc] == "B"
                    and board[mr][mc] == "W"
                    and board[tr][tc] is None
                ):
                    to_pos = self.coords_to_position(tr, tc)
                    print(f"Znaleziono możliwe bicie: {from_pos}x{to_pos}")
                    captures.append(f"{from_pos}x{to_pos}")
                    # Dokonujemy bicia na instancji board
                    # board.perform_capture(from_pos, to_pos)

        return captures
