from typing import List

from .drawer import Drawer

B = (0, 0, 0)
R = (255, 0, 0)
G = (0, 255, 0)


class Pihat(Drawer):

    def __init__(self):
        from sense_hat import SenseHat # pylint: disable=import-error
        self._sense = SenseHat()
        self._sense.set_rotation(180)

    def draw(self, board: List) -> None:
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

    def clear(self, game_summary: str) -> None:
        self._sense.show_message(game_summary)
        self._sense.clear()
