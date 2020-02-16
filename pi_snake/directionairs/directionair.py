from abc import ABC, abstractmethod

from pi_snake.board import Board

from ..direction import Direction


class Directionair(ABC):

    def start(self) -> None:
        pass

    @abstractmethod
    def set_direction(self, direction: Direction) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_direction(self) -> Direction:
        raise NotImplementedError()

    @abstractmethod
    def get_new_direction(self, board: Board) -> Direction:
        raise NotImplementedError()
