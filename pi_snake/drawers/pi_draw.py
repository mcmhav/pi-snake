B = (0, 0, 0)
R = (255, 0, 0)
G = (0, 255, 0)


class Pihat():

    def __init__(self, sense):
        self._sense = sense

    def draw(self, board):
        pixels = []

        for row in board:
            for cell in row:
                if cell == 's':
                    pixels.append(R)
                elif cell == 'g':
                    pixels.append(G)
                else:
                    pixels.append(B)

        self._sense.set_pixels(pixels)

    def clear(self, game_summary):
        self._sense.show_message(game_summary)
        self._sense.clear()
