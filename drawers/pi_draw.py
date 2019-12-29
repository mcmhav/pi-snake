from sense_hat import SenseHat

B = (0, 0, 0)
R = (255, 0, 0)


class Pihat():

    def __init__(self):
        self._sense = SenseHat()

    def draw(self, board):
        pixels = []

        for row in board:
            print(row)
            for cell in row:
                if cell == 's':
                    pixels.append(R)
                else:
                    pixels.append(B)

        print(len(pixels))

        self._sense.set_pixels(pixels)
