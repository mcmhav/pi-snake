from sense_hat import SenseHat

B = (0, 0, 0)
R = (255, 0, 0)


class Pihat():

    def __init__(self):
        self._sense = SenseHat()

    @staticmethod
    def draw(board):
        pixels = []

        for row in board:
            print(row)
            if row:
                pixels.append(R)
            else:
                pixels.append(B)

        self._sense.set_pixels(pixels)
