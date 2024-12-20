# importuje bibliotekę NumPy (obliczenia numeryczne)
# import numpy as np

# importuje bibliotekę TensorFlow (sieci neuronowe)
from tensorflow.keras.models import Sequential

# Dense to warstwa gęsta
# Input definiuje kształt warstwy wejściowej
from tensorflow.keras.layers import Dense, Input

from tensorflow.keras.models import load_model


class CheckersAIModel:
    def __init__(self):
        self.model = self._create_model()

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

    def train(self, X, y, epochs=10, batch_size=32):

        print("Rozpoczynam trening modelu...")
        self.model.fit(X, y, epochs=10, batch_size=32)
        print("Trening zakończony!")

    def predict(self, board_state):

        board_state = board_state.reshape(1, -1)
        predictions = self.model.predict(board_state)
        return predictions

    def save_model(self, filepath):

        self.model.save(filepath)
        print(f"Model zapisany do pliku: {filepath}")

    def load_model(self, filepath):

        self.model = load_model(filepath)
        print(f"Model załadowany z pliku: {filepath}")

