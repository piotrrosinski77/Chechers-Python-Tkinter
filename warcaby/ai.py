import os
import numpy as np
import math
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Input


class CheckersAIModel:
    def __init__(self):
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
        board_array = self.convert_board_to_array(board_state)
        predictions = self.model.predict(board_array)[0]
        sorted_indices = np.argsort(-predictions)

        black_positions = self.get_black_positions(board_state)
        black_positions.sort(key=lambda pos: self.distance_from_center(pos))

        for from_pos in black_positions:
            for idx in sorted_indices:
                to_pos = idx % 64 + 1
                try:
                    fr, fc = self.position_to_coords(from_pos)
                    tr, tc = self.position_to_coords(to_pos)

                    if not (0 <= tr < 8 and 0 <= tc < 8):
                        continue

                    move = f"{from_pos}-{to_pos}"
                    print(
                        f"Proponowany ruch dla czarnej figury na polu {from_pos}: {move} "
                        f"(szac. prawdopodobieństwo: {predictions[idx]:.4f})"
                    )

                    if self.is_valid_move(board_state, move):
                        print("Znaleziono poprawny ruch:", move)
                        return move

                except ValueError as e:
                    print(f"Błąd przy sprawdzaniu ruchu: {e}")
                    continue

        raise ValueError("Nie można wygenerować prawidłowego ruchu.")

    def distance_from_center(self, pos):

        r, c = self.position_to_coords(pos)
        center_r, center_c = 3.5, 3.5
        return math.sqrt((r - center_r) ** 2 + (c - center_c) ** 2)

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
        try:
            fp, tp = map(int, move.split("-"))
            fr, fc = self.position_to_coords(fp)
            tr, tc = self.position_to_coords(tp)
            if board[fr][fc] != "B":
                return False
            if board[tr][tc] is not None:
                return False
            if abs(fr - tr) == 1 and abs(fc - tc) == 1:
                return True
            if abs(fr - tr) == 2 and abs(fc - tc) == 2:
                mr = (fr + tr) // 2
                mc = (fc + tc) // 2
                if board[mr][mc] == "W":
                    return True
            return False
        except ValueError:
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
        black_positions = []
        for row in range(8):
            for col in range(8):
                if board_state[row][col] == "B":
                    pos = self.coords_to_position(row, col)
                    black_positions.append(pos)
        return black_positions
