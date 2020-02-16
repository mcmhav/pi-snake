from abc import ABC, abstractmethod
from typing import List


class Drawer(ABC):

    @abstractmethod
    def draw(self, board: List) -> None:
        raise NotImplementedError()

    @abstractmethod
    def clear(self, game_summary: str) -> None:
        raise NotImplementedError()
