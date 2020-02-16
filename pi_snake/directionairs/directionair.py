from abc import ABC, abstractmethod

from pi_snake.board import Board
from typing import Any

from ..direction import Direction


class Directionair(ABC):

    def __init__(
            self,
            init_direction: Direction = Direction.right,
            *args: Any,
    ):
        self._direction = init_direction

    def start(self) -> None:
        pass

    def set_direction(self, direction: Direction) -> None:
        self._direction = direction

    def get_direction(self) -> Direction:
        return self._direction

    @abstractmethod
    def get_new_direction(self, board: Board) -> Direction:
        raise NotImplementedError()
