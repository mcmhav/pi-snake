from typing import List

from .drawer import Drawer


class Sysout(Drawer):

    @staticmethod
    def draw(board: List) -> None:
        for row in board:
            print(row)

    @staticmethod
    def clear(game_summary: str) -> None:
        print(game_summary)
