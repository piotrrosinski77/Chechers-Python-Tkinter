class Piece:
    def __init__(self, color):
        self.color = color

    def is_black(self):
        return self.color == 'B'

    def is_white(self):
        return self.color == 'W'
