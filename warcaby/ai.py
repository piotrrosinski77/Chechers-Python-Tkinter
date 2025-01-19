import os
import numpy as np
from .board import Board
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Input


class CheckersAIModel:
    def __init__(self):
        self.board = Board()  # Przechowywanie obiektu Board
        model_filepath = "trained_checkers_model.h5"
        if os.path.exists(model_filepath):
            self.model = self.load_model(model_filepath)
            # print("Wczytano poprawnie model z pliku")
            print("Successfully loaded model from file")
        else:
            self.model = self._create_model()
            # print("Utworzono nowy model")
            print("Created a new model")

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
        # print(f"Model załadowany z pliku: {filepath}")
        print(f"Model loaded from file: {filepath}")
        return model

    def save_model(self, filepath):
        self.model.save(filepath)
        # print(f"Model zapisany do pliku: {filepath}")
        print(f"Model saved to file: {filepath}")

    def train(self, X, y, epochs=1, batch_size=32):
        # print("Rozpoczynam trening modelu...")
        print("Starting model training...")
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size)
        # print("Trening zakończony!")
        print("Training completed!")

    def generate_valid_move(self, board_state, last_computer_move):
        # print("Rozpoczynam generowanie ruchu dla komputera...")
        print("Starting computer move generation...")
        board_array = self.convert_board_to_array(board_state)
        # print("Tablica reprezentująca planszę:", board_array)
        print("Board array representation:", board_array)

        predictions = self.model.predict(board_array)[0]
        # print("Predykcje modelu:", predictions)
        print("Model predictions:", predictions)

        sorted_indices = np.argsort(-predictions)
        # print("Indeksy posortowane według prawdopodobieństwa:", sorted_indices)
        print("Sorted indices by probability:", sorted_indices)

        black_positions = self.get_black_positions(board_state)
        # print("Pozycje czarnych pionków:", black_positions)
        print("Positions of black pieces:", black_positions)

        # Sprawdź możliwe bicia
        for from_pos in black_positions:

            captures = self.get_valid_captures(board_state, from_pos)
            print(f"board_state: {board_state}", f"from_pos: {from_pos}")
            if captures:
                # print(
                # f"Znaleziono możliwe bicia dla pionka na polu {from_pos}: {captures}"
                # )
                print(f"Found possible captures for piece at {from_pos}: {captures}")
                return captures[0]  # Wybieramy pierwsze bicie

        # Jeśli brak bić, wykonaj standardowy ruch
        for from_pos in black_positions:
            # print(f"Przetwarzam ruchy dla pionka na polu {from_pos}")
            print(f"Processing moves for piece at {from_pos}")
            for idx in sorted_indices:
                to_pos = idx % 64 + 1
                move = f"{from_pos}-{to_pos}"
                # print(f"Sprawdzam ruch: {move}")
                print(f"Checking move: {move}")

                if self.is_valid_move(board_state, move, last_computer_move):
                    # print("Znaleziono poprawny ruch:", move)
                    print("Found a valid move:", move)
                    return move

        # print("Nie znaleziono poprawnego ruchu.")
        print("No valid move found.")
        # raise ValueError("Nie można wygenerować prawidłowego ruchu.")
        raise ValueError("Cannot generate a valid move.")

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

    def is_valid_move(self, board, move, last_computer_move):

        # print(f"Sprawdzam poprawność ruchu: {move}")
        print(f"Checking move validity: {move}")
        try:
            fp, tp = map(int, move.split("-"))
            fr, fc = self.position_to_coords(fp)
            tr, tc = self.position_to_coords(tp)
            # print(f"Pola: Startowe ({fr}, {fc}), Docelowe ({tr}, {tc})")
            print(f"Positions: Start ({fr}, {fc}), Target ({tr}, {tc})")

            if board[fr][fc] != "B":
                # print(
                #    f"Nieprawidłowy ruch: Pole startowe {fp} nie zawiera czarnego pionka."
                #
                print(
                    f"Invalid move: Starting position {fp} does not contain a black piece."
                )
                return False
            if not (0 <= tr < 8 and 0 <= tc < 8):
                # print("Nieprawidłowy ruch: Pole docelowe poza planszą.")
                print("Invalid move: Target position is off the board.")
                return False
            if board[tr][tc] is not None:
                # print("Nieprawidłowy ruch: Pole docelowe jest zajęte.")
                print("Invalid move: Target position is occupied.")
                return False

            if last_computer_move is not None:

                last_computer_move = f"{last_computer_move[0]}-{last_computer_move[1]}"

                try:

                    if last_computer_move[3]:
                        r_last_computer_move = f"{last_computer_move[2]}{last_computer_move[3]}-{last_computer_move[0]}"

                except IndexError:

                    r_last_computer_move = (
                        f"{last_computer_move[2]}-{last_computer_move[0]}"
                    )

                print(f"Last computer move: {last_computer_move}")
                print(f"Reversed last computer move: {r_last_computer_move}")

                if move == last_computer_move or move == r_last_computer_move:
                    # print(
                    # "Nieprawidłowy ruch: Ruch jest taki sam jak poprzedni ruch komputera.")
                    print(
                        "Invalid move: Move is the same as the previous computer move."
                    )
                    return False

            else:
                print("No last computer move.")

            # Ruch standardowy
            if abs(fr - tr) == 1 and abs(fc - tc) == 1:
                # print("Ruch standardowy jest poprawny.")
                print("Standard move is valid.")
                return True

            # Ruch z biciem
            if abs(fr - tr) == 2 and abs(fc - tc) == 2:
                mr, mc = (fr + tr) // 2, (fc + tc) // 2
                # print(f"Pole środkowe: ({mr}, {mc})")
                print(f"Middle position: ({mr}, {mc})")
                if board[mr][mc] == "W":
                    # print("Ruch z biciem jest poprawny.")
                    print("Capture move is valid.")
                    return True

            # print("Nieprawidłowy ruch.")
            print("Invalid move.")
            return False
        except ValueError as e:
            # print(f"Nieprawidłowy ruch: {e}")
            print(f"Invalid move: {e}")
            return False

    def position_to_coords(self, pos):
        if not (1 <= pos <= 64):
            raise ValueError(
                # f"Nieprawidłowy numer pola: {pos}. Musi być w zakresie 1–64."
                f"Invalid position number: {pos}. Must be in the range 1–64."
            )

        r = (pos - 1) // 4
        c = ((pos - 1) % 4) * 2 + (1 if r % 2 == 0 else 0)
        return r, c

    def coords_to_position(self, row, col):
        if not (0 <= row < 8 and 0 <= col < 8):
            raise ValueError(
                # f"Nieprawidłowe współrzędne: ({row}, {col}). Muszą być w zakresie 0–7."
                f"Invalid coordinates: ({row}, {col}). Must be in the range 0–7."
            )

        if (row % 2 == 0 and col % 2 != 1) or (row % 2 == 1 and col % 2 != 0):
            raise ValueError(
                # f"Pole ({row}, {col}) nie jest czarnym polem na planszy."
                f"Position ({row}, {col}) is not a black square on the board."
            )

        pos = row * 4 + (col // 2) + 1
        return pos

    def train_model(self, history):
        X, y = [], []

        if X and y:
            X = np.array(X)
            y = np.array(y)
            self.train(X, y, epochs=1, batch_size=32)
            self.save_model("trained_checkers_model.h5")

    # def train_model(self, games):
    #    X = []
    #    y = []

    #    for game in games:
    #       for move in game:
    #            board_state, move_vector = self.process_move(move)
    #            if board_state is not None and move_vector is not None:
    #                X.append(board_state)
    #                y.append(move_vector)
    #        X = np.array(X)
    #        y = np.array(y)
    #    print(f"Liczba partii używanych do nauki modelu: {len(games)}")

    def get_black_positions(self, board_state):
        # print("Zaczynam identyfikację pozycji czarnych pionków...")
        print("Starting identification of black piece positions...")
        black_positions = []
        for row in range(8):
            for col in range(8):
                if board_state[row][col] == "B":
                    pos = self.coords_to_position(row, col)
                    black_positions.append(pos)
                    print(
                        # f"Znaleziono czarny pionek na polu: {pos} (współrzędne: {row}, {col})"
                        f"Found black piece at position: {pos} (coordinates: {row}, {col})"
                    )
        # print(f"Wszystkie pozycje czarnych pionków: {black_positions}")
        print("All black piece positions:", black_positions)
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
                    # print(f"Znaleziono możliwe bicie: {from_pos}x{to_pos}")
                    print(f"Found possible capture: {from_pos}x{to_pos}")
                    captures.append(f"{from_pos}x{to_pos}")
                    # Dokonujemy bicia na instancji board
                    # board.perform_capture(from_pos, to_pos)

        return captures
