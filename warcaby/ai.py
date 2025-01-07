import os
import numpy as np
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

    @staticmethod
    def _create_model():
        model = Sequential(
            [
                Input(shape=(64,)),
                Dense(128, activation="relu"),
                Dense(128, activation="relu"),
                Dense(64, activation="softmax"),
            ]
        )
        model.compile(
            optimizer="adam", loss="categorical_crossentropy",
            metrics=["accuracy"]
        )
        return model

    @staticmethod
    def create_model():
        return CheckersAIModel._create_model()

    def train(self, X, y, epochs=1, batch_size=32):
        print("Rozpoczynam trening modelu...")
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size)
        print("Trening zakończony!")

    def predict(self, board_state):
        board_state = np.array(board_state).reshape(1, -1)
        predictions = self.model.predict(board_state)
        return predictions

    def save_model(self, filepath):
        self.model.save(filepath)
        print(f"Model zapisany do pliku: {filepath}")

    def load_model(self, filepath):
        model = load_model(filepath)
        model.compile(
            optimizer="adam", loss="categorical_crossentropy",
            metrics=["accuracy"]
        )
        print(f"Model załadowany z pliku: {filepath}")
        return model

    def train_model(self, games):
        X = []
        y = []

        for game in games:
            for move in game:
                # Przetwarzanie ruchów i dodanie do X i y
                board_state, move_vector = self.process_move(move)
                if board_state is not None and move_vector is not None:
                    X.append(board_state)
                    y.append(move_vector)

        X = np.array(X)
        y = np.array(y)

        print(f"Liczba partii używanych do nauki modelu: {len(games)}")

        self.train(X, y, epochs=1, batch_size=32)

        # Zapisz wytrenowany model do pliku
        model_filepath = "trained_checkers_model.h5"
        self.save_model(model_filepath)
        print(f"Wytrenowany model zapisany do pliku: {model_filepath}")

    def process_move(self, move):
        # Przetwarzanie ruchu na wektor
        # Zaimplementuj tę funkcję zgodnie z wymaganiami
        if move is None:
            return None, None
        board_state = np.zeros((64,))  # Przykładowa tablica stanu planszy
        move_vector = np.zeros((64,))  # Przykładowa tablica ruchu
        # Wypełnij board_state i move_vector odpowiednimi wartościami
        return board_state, move_vector

    def is_valid_move(self, board, move):
        fp, tp = map(int, move.split("-"))
        fr, fc = self.position_to_coords(fp)
        tr, tc = self.position_to_coords(tp)

        # Sprawdź, czy ruch jest w granicach planszy
        if not (0 <= fr < 8 and 0 <= fc < 8 and 0 <= tr < 8 and 0 <= tc < 8):
            return False

        # Sprawdź, czy na pozycji początkowej znajduje się pionek
        if board[fr][fc] is None:
            return False

        # Sprawdź, czy pozycja docelowa jest pusta
        if board[tr][tc] is not None:
            return False

        if abs(fr - tr) == 1 and abs(fc - tc) == 1:
            return True

        # Sprawdź, czy ruch jest ruchem skoku (przeskoczenie przeciwnika)
        if abs(fr - tr) == 2 and abs(fc - tc) == 2:
            mr = (fr + tr) // 2
            mc = (fc + tc) // 2
            if board[mr][mc] is not None and board[mr][mc] != board[fr][fc]:
                return True

        return False

    def position_to_coords(self, pos):
        r = (pos - 1) // 4
        c = ((pos - 1) % 4) * 2 + (1 if r % 2 == 0 else 0)
        return r, c

    def generate_valid_move(self, board_state):
        tm = set()
        while True:
            # Generuj ruch za pomocą modelu
            move = self.generate_move(board_state)
            if move not in tm and self.is_valid_move(board_state, move):
                return move
            tm.add(move)

    def generate_move(self, board_state):
        # Implementacja generowania ruchu za pomocą modelu
        board_state = np.array(board_state)
        predictions = self.model.predict(board_state.reshape(1, -1))
        move = self.decode_predictions(predictions)
        return move

    def decode_predictions(self, predictions):
        # Implementacja dekodowania przewidywań modelu na ruch
        move = "12-16"  # Przykładowy ruch
        return move
    