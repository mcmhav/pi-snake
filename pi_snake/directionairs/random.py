import random

from pi_snake.board import Board

from ..direction import Direction
from .directionair import Directionair

DIRECTIONS = {
    0: Direction.right,
    1: Direction.up,
    2: Direction.down,
    3: Direction.left,
}


class Random(Directionair):

    def __init__(
            self,
            init_direction: Direction = Direction.right,
            seed: int = 1,
    ):
        super().__init__(init_direction)
        self._seed = seed

    def _can_move_direction(
            self,
            previous_direction: Direction,
            next_direction: Direction,
    ) -> bool:
        if ((previous_direction == Direction.up
             and next_direction == Direction.down)
                or (previous_direction == Direction.down
                    and next_direction == Direction.up)
                or (previous_direction == Direction.right
                    and next_direction == Direction.left)
                or (previous_direction == Direction.left
                    and next_direction == Direction.right)):
            return False
        return True

    def get_new_direction(self, board: Board) -> Direction:
        new_direction = DIRECTIONS[random.randint(0, 3)]
        while not self._can_move_direction(self._direction, new_direction):
            new_direction = DIRECTIONS[random.randint(0, 3)]
        self._direction = new_direction
        return new_direction
